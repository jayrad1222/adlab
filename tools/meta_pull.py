#!/usr/bin/env python3
"""meta_pull.py: read-only Meta Ad Library pull (headless Playwright, no login).

Port of the October 2026 Operators Workshop scraper, generalized. Reads the JSON embedded in the
Ad Library page plus intercepted /api/graphql/ responses. One search at a time, 2 to 4 second
pauses, desktop user agent, never logs in, never likes, follows or messages. Media is downloaded
immediately because Meta's CDN URLs expire.

Usage
  python -I meta_pull.py --plan plan.json --out <workspace>/ads
  python -I meta_pull.py --advertisers "Brand A" "Brand B" --out <workspace>/ads
  python -I meta_pull.py --ids 123456789 987654321 --out <workspace>/ads
  python -I meta_pull.py --plan plan.json --out DIR --dry-run     (prints the URLs it would visit)

Plan items (JSON list): {"kind": "keyword|exact|name|page|id|cobrand", "q": "...",
  "label": "...", "group": "...", "advertiser": "<roster name>"}
  keyword  unordered keyword search               exact  exact-phrase search
  name     keyword search, then typeahead pages   page   view_all_page_id
  id       the ad detail page (also captures the EU transparency block)
  cobrand  exact search for "<q> with <platform page>" for each --cobrand-pages entry

Outputs in --out: ads.jsonl (all ads, deduped on ad_id), searches.csv, run.log, and
<advertiser_slug>/<ad_id>/{ad.json, card.png, media/...}
"""
from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys
import time
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import adlab_common as C  # noqa: E402

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36")
LIB = "https://www.facebook.com/ads/library/"

CARD_JS = """(id) => {
  const want = 'Library ID: ' + id;
  const el = [...document.querySelectorAll('span,div')].find(e => e.childElementCount === 0 && e.textContent.trim() === want);
  if (!el) return false;
  let n = el;
  while (n && n.parentElement) {
    n = n.parentElement;
    const r = n.getBoundingClientRect();
    if (r.height > 420 && r.width > 250 && r.width < 700) { n.setAttribute('data-adlab-card', id); return true; }
    if (r.width >= 700) return false;
  }
  return false;
}"""


# ----------------------------------------------------------------------------- parsing helpers

def iso(ts):
    if not ts:
        return None
    try:
        return datetime.fromtimestamp(int(ts), tz=timezone.utc).strftime("%Y-%m-%d")
    except Exception:
        return None


def walk_ads(o, acc):
    if isinstance(o, dict):
        if "ad_archive_id" in o and "snapshot" in o:
            acc.append(o)
            return
        for v in o.values():
            walk_ads(v, acc)
    elif isinstance(o, list):
        for v in o:
            walk_ads(v, acc)


def find_key(o, key, acc):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == key:
                acc.append(v)
            find_key(v, key, acc)
    elif isinstance(o, list):
        for v in o:
            find_key(v, key, acc)


def parse_json_blobs(text):
    out = []
    for chunk in text.split("\n"):
        chunk = chunk.strip()
        if chunk.startswith("for (;;);"):
            chunk = chunk[9:]
        if not chunk.startswith("{"):
            continue
        try:
            out.append(json.loads(chunk))
        except Exception:
            pass
    return out


def decode_link(u):
    if not u:
        return u
    p = urllib.parse.urlparse(u)
    if p.netloc.endswith("l.facebook.com") and p.path.startswith("/l.php"):
        q = urllib.parse.parse_qs(p.query).get("u")
        if q:
            return q[0]
    return u


def classify_link(u):
    if not u:
        return {"link_domain": None, "link_path": None, "dest_type": "none"}
    p = urllib.parse.urlparse(u)
    host = p.netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    path = p.path or "/"
    t = "website"
    for k, v in [("calendly", "booking"), ("typeform", "form"), ("youtube", "youtube"), ("youtu.be", "youtube"),
                 ("fb.me", "facebook"), ("facebook.com", "facebook"), ("instagram.com", "instagram"),
                 ("m.me", "messenger"), ("wa.me", "whatsapp"), ("apps.apple.com", "app-store"),
                 ("play.google.com", "app-store"), ("skool.com", "skool"), ("amazon.", "amazon"),
                 ("etsy.com", "etsy"), ("shopify", "shopify"), ("linktr.ee", "linktree")]:
        if k in host:
            t = v
            break
    hp = (host + path).lower()
    if t == "website" and any(x in hp for x in ["vsl", "webinar", "training", "masterclass", "workshop", "apply", "book", "call", "quiz"]):
        t = "funnel"
    elif t == "website" and any(x in hp for x in ["product", "products", "collections", "shop", "store", "cart"]):
        t = "product-page"
    return {"link_domain": host, "link_path": path, "dest_type": t}


def normalize(a, terms):
    """Meta search-result ad object -> Ad Lab record."""
    s = a.get("snapshot") or {}
    cards = s.get("cards") or []
    body = (s.get("body") or {}).get("text")
    link = decode_link(s.get("link_url"))
    if not link:
        for c in cards:
            if c.get("link_url"):
                link = decode_link(c["link_url"])
                break
    imgs = s.get("images") or []
    vids = s.get("videos") or []
    image_url = None
    if imgs:
        image_url = imgs[0].get("original_image_url") or imgs[0].get("resized_image_url")
    video_preview = vids[0].get("video_preview_image_url") if vids else None
    video_hd = vids[0].get("video_hd_url") if vids else None
    video_sd = vids[0].get("video_sd_url") if vids else None
    card_out = []
    for c in cards:
        card_out.append({
            "body": c.get("body"), "title": c.get("title"), "link_description": c.get("link_description"),
            "link_url": decode_link(c.get("link_url")), "cta_text": c.get("cta_text"), "cta_type": c.get("cta_type"),
            "caption": c.get("caption"),
            "original_image_url": c.get("original_image_url"), "resized_image_url": c.get("resized_image_url"),
            "video_preview_image_url": c.get("video_preview_image_url"),
            "video_hd_url": c.get("video_hd_url"), "video_sd_url": c.get("video_sd_url"),
        })
        if not image_url:
            image_url = c.get("original_image_url") or c.get("resized_image_url")
        if not video_preview:
            video_preview = c.get("video_preview_image_url")
            video_hd = video_hd or c.get("video_hd_url")
            video_sd = video_sd or c.get("video_sd_url")
    fmt = (s.get("display_format") or "unknown").lower()
    if fmt == "multi_images":
        fmt = "carousel"
    text_blob = " ".join(str(x) for x in [body, s.get("title"), s.get("link_description"), s.get("caption"),
                                           s.get("page_name")] + [c.get("body") for c in card_out] if x).lower()
    hits = [t for t in (terms or []) if t and t.lower() in text_blob]
    page_name = a.get("page_name") or s.get("page_name") or "unknown"
    platforms = a.get("publisher_platform") or []
    if isinstance(platforms, str):
        platforms = [platforms]
    start = iso(a.get("start_date"))
    end = iso(a.get("end_date"))
    rec = {
        "source": "meta",
        "ad_id": str(a["ad_archive_id"]),
        "advertiser": page_name,
        "advertiser_id": str(a.get("page_id") or s.get("page_id") or ""),
        "advertiser_slug": C.slugify(page_name),
        "platforms": [str(p).lower() for p in platforms],
        "start_date": start,
        "end_date": end,
        "is_active": a.get("is_active"),
        "days_active": C.days_between(start, end if a.get("is_active") is False else None),
        "variant_count": a.get("collation_count"),
        "collation_id": a.get("collation_id"),
        "format": fmt,
        "body_text": body,
        "title": s.get("title"),
        "link_description": s.get("link_description"),
        "caption": s.get("caption"),
        "cta_text": s.get("cta_text"),
        "cta_type": s.get("cta_type"),
        "link_url": link,
        "image_url": image_url,
        "video_preview_image_url": video_preview,
        "video_hd_url": video_hd,
        "video_sd_url": video_sd,
        "cards": card_out,
        "page_like_count": s.get("page_like_count"),
        "page_profile_uri": s.get("page_profile_uri"),
        "page_categories": s.get("page_categories"),
        "byline": s.get("byline"),
        "term_hits": hits,
        "eu": None,
        "library_url": LIB + "?id=" + str(a["ad_archive_id"]),
        "raw_snapshot": s,
    }
    rec.update(classify_link(link))
    return rec


def eu_block(blobs):
    found = []
    for j in blobs:
        find_key(j, "aaa_info", found)
    for info in found:
        if not isinstance(info, dict):
            continue
        keep = {k: info.get(k) for k in ("eu_total_reach", "age_country_gender_reach_breakdown", "location_audience",
                                        "gender_audience", "age_audience", "is_aaa_eligible", "payer_beneficiary_data")
                if info.get(k) not in (None, [], {})}
        if keep:
            return keep
    return None


# ----------------------------------------------------------------------------- the puller

class Puller:
    def __init__(self, args):
        self.args = args
        self.out = Path(args.out)
        self.out.mkdir(parents=True, exist_ok=True)
        self.ads_path = self.out / "ads.jsonl"
        self.search_path = self.out / "searches.csv"
        self.logfile = self.out / "run.log"
        self.ads = {}
        for r in C.read_jsonl(self.ads_path):
            self.ads[r["ad_id"]] = r
        self.per_adv = {}
        for r in self.ads.values():
            self.per_adv[r["advertiser_id"]] = self.per_adv.get(r["advertiser_id"], 0) + 1
        self.visited_pages = set()
        self.search_rows = []
        self.terms = args.terms or []

    def log(self, msg):
        C.log(msg, self.logfile)

    # ---- url builders
    def base(self):
        status = "all" if self.args.include_inactive else "active"
        return (LIB + "?active_status=" + status + "&ad_type=all&country=" + urllib.parse.quote(self.args.country)
                + "&media_type=" + self.args.media_type)

    def url_for(self, kind, q):
        if kind in ("keyword", "name"):
            return self.base() + "&search_type=keyword_unordered&q=" + urllib.parse.quote(q)
        if kind == "exact":
            return self.base() + "&search_type=keyword_exact_phrase&q=" + urllib.parse.quote('"' + q + '"')
        if kind == "page":
            return self.base() + "&search_type=page&view_all_page_id=" + str(q)
        if kind == "id":
            return LIB + "?id=" + str(q)
        raise ValueError(kind)

    # ---- persistence
    def save(self):
        C.write_jsonl(self.ads_path, self.ads.values())

    def write_search_row(self, row):
        cols = ["timestamp", "group", "label", "search_type", "query", "url", "ads_found", "reported_result_count",
                "new_unique_ads", "term_hits", "notes"]
        new = not self.search_path.exists()
        import csv
        with self.search_path.open("a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            if new:
                w.writeheader()
            w.writerow(row)

    def ad_dir(self, rec):
        return self.out / rec["advertiser_slug"] / rec["ad_id"]

    def download_media(self, ctx, rec):
        if self.args.no_media:
            return
        d = self.ad_dir(rec) / "media"
        files = rec.setdefault("files", {})
        src = rec.get("image_url") or rec.get("video_preview_image_url")
        if src and not files.get("creative"):
            p = self._dl(ctx, src, d / "creative")
            if p:
                files["creative"] = str(p.relative_to(self.out))
        if rec.get("video_preview_image_url") and rec.get("image_url") and not files.get("poster"):
            p = self._dl(ctx, rec["video_preview_image_url"], d / "poster")
            if p:
                files["poster"] = str(p.relative_to(self.out))
        vid = rec.get("video_hd_url") or rec.get("video_sd_url")
        if vid and not self.args.no_videos and not files.get("video"):
            target = d / "video.mp4"
            p = C.http_download(vid, target, max_bytes=self.args.video_max_mb * 1024 * 1024)
            if p:
                files["video"] = str(p.relative_to(self.out))
            else:
                self.log("video skipped or failed for " + rec["ad_id"])
        # carousel card images
        for i, c in enumerate(rec.get("cards") or []):
            u = c.get("original_image_url") or c.get("resized_image_url")
            key = "card%d" % i
            if u and not files.get(key) and i < 10:
                p = self._dl(ctx, u, d / ("card-%d" % i))
                if p:
                    files[key] = str(p.relative_to(self.out))

    def _dl(self, ctx, url, base: Path):
        for ext in (".jpg", ".png", ".webp"):
            if base.with_suffix(ext).exists():
                return base.with_suffix(ext)
        base.parent.mkdir(parents=True, exist_ok=True)
        try:
            r = ctx.request.get(url, timeout=30000)
            if not r.ok:
                return None
            ct = r.headers.get("content-type", "")
            ext = ".png" if "png" in ct else ".webp" if "webp" in ct else ".jpg"
            p = base.with_suffix(ext)
            p.write_bytes(r.body())
            return p
        except Exception as e:
            self.log("download failed %s: %s" % (base.name, str(e)[:80]))
            return None

    def write_ad_json(self, rec):
        d = self.ad_dir(rec)
        d.mkdir(parents=True, exist_ok=True)
        (d / "ad.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")

    # ---- one page load
    def run_page(self, ctx, page, url, group, label, stype, query, advertiser=None, collect_eu=False, neighbor_cap=None):
        captured = []
        neighbors_saved = 0

        def on_resp(r):
            if "/api/graphql" in r.url:
                try:
                    captured.append(r.text())
                except Exception:
                    pass

        page.on("response", on_resp)
        note = ""
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
        except Exception as e:
            note = "goto error: " + str(e)[:120]
        time.sleep(5)
        if "login" in page.url or "checkpoint" in page.url:
            note += " redirected to " + page.url[:80]
        html = page.content()
        blobs_txt = re.findall(r'<script type="application/json"[^>]*>(.*?)</script>', html, re.S)

        def all_json():
            out = []
            for t in blobs_txt + captured:
                out.extend(parse_json_blobs(t))
            return out

        def collect():
            found = []
            for j in all_json():
                walk_ads(j, found)
            return found

        raw = collect()
        seen = {str(a["ad_archive_id"]) for a in raw}
        if stype != "id":
            stale = 0
            while len(seen) < self.args.max_per_search and stale < 3:
                n0 = len(seen)
                page.mouse.wheel(0, 6000)
                time.sleep(1.2)
                try:
                    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
                except Exception:
                    pass
                time.sleep(2.5)
                raw = collect()
                seen = {str(a["ad_archive_id"]) for a in raw}
                stale = stale + 1 if len(seen) == n0 else 0
        counts, filter_pages = [], []
        for j in all_json():
            conn = []
            find_key(j, "search_results_connection", conn)
            for c in conn:
                if isinstance(c, dict) and isinstance(c.get("count"), int):
                    counts.append(c["count"])
            fo = []
            find_key(j, "dynamic_filter_options", fo)
            for d in fo:
                for pg in (d or {}).get("pages") or []:
                    filter_pages.append({"page_id": pg.get("key"), "name": pg.get("display_name"), "count": pg.get("count"), "src": "filter"})
        eu = eu_block(all_json()) if (collect_eu or stype == "id") else None
        page.remove_listener("response", on_resp)

        by_id = {}
        for a in raw:
            by_id.setdefault(str(a["ad_archive_id"]), a)
        if stype == "id":
            # a detail page also lists the Page's other ads; keep only the one that was asked for
            by_id = {k: v for k, v in by_id.items() if k == str(query)}
        new, hits_n, this_ids, capped = 0, 0, [], 0
        for aid, a in by_id.items():
            if a.get("is_active") is False and not self.args.include_inactive:
                continue
            rec = normalize(a, self.terms)
            match = self.match_kind(rec, stype, advertiser)
            rec["match"] = match
            if advertiser and match in ("advertiser-page", "cobrand"):
                rec["roster_advertiser"] = advertiser
            elif advertiser:
                rec["candidate_for"] = advertiser
            if aid in self.ads:
                prev = self.ads[aid]
                if [group, label] not in prev.get("found_via", []):
                    prev.setdefault("found_via", []).append([group, label])
                if eu and not prev.get("eu"):
                    prev["eu"] = eu
                rec = prev
            else:
                cnt = self.per_adv.get(rec["advertiser_id"], 0)
                if cnt >= self.args.max_per_advertiser:
                    capped += 1
                    continue
                if len(self.ads) >= self.args.max_total:
                    capped += 1
                    continue
                if match == "keyword-neighbor" and neighbor_cap is not None and neighbors_saved >= neighbor_cap:
                    capped += 1
                    continue
                if match == "keyword-neighbor":
                    neighbors_saved += 1
                rec["found_via"] = [[group, label]]
                rec["first_seen_utc"] = C.now_iso()
                rec["eu"] = eu
                self.ads[aid] = rec
                self.per_adv[rec["advertiser_id"]] = cnt + 1
                new += 1
            this_ids.append(aid)
            if rec.get("term_hits"):
                hits_n += 1
            self.download_media(ctx, rec)
        shots = 0
        if not self.args.no_cards:
            for aid in this_ids:
                rec = self.ads[aid]
                if rec.get("files", {}).get("card"):
                    continue
                try:
                    if page.evaluate(CARD_JS, aid):
                        p = self.ad_dir(rec) / "card.png"
                        p.parent.mkdir(parents=True, exist_ok=True)
                        page.locator('[data-adlab-card="%s"]' % aid).first.screenshot(path=str(p), timeout=8000)
                        rec.setdefault("files", {})["card"] = str(p.relative_to(self.out))
                        shots += 1
                except Exception:
                    pass
        for aid in this_ids:
            self.write_ad_json(self.ads[aid])
        self.save()
        reported = max(counts) if counts else ""
        self.write_search_row({
            "timestamp": C.now_iso(), "group": group, "label": label, "search_type": stype, "query": query,
            "url": url, "ads_found": len(this_ids), "reported_result_count": reported, "new_unique_ads": new,
            "term_hits": hits_n, "notes": (note + (" capped %d" % capped if capped else "")).strip(),
        })
        self.log("[%s] %r (%s) -> %d ads, %d new, reported=%s, cards=%d, capped=%d, total=%d %s"
                 % (group, label, stype, len(this_ids), new, reported or "?", shots, capped, len(self.ads), note))
        return this_ids, filter_pages

    def match_kind(self, rec, stype, advertiser):
        """advertiser-page: seen on the matched Page; cobrand: run by a platform Page and names the advertiser;
        keyword-neighbor: came up in a keyword search (an attention competitor, not the roster advertiser)."""
        if stype == "page":
            return "advertiser-page"
        if stype == "id":
            return "detail"
        platforms = [p.lower() for p in (self.args.cobrand_pages or [])]
        if advertiser and rec.get("advertiser", "").lower() in platforms:
            blob = " ".join(str(x) for x in [rec.get("body_text"), rec.get("title"), rec.get("link_url"), rec.get("caption")] if x).lower()
            if self.name_matches(advertiser, blob) or C.slugify(advertiser) in blob.replace(" ", "-"):
                return "cobrand"
        if advertiser and self.name_matches(advertiser, rec.get("advertiser")):
            return "advertiser-page"
        return "keyword-neighbor"

    def typeahead_pages(self, page, name):
        got = []

        def on_resp(r):
            if "/api/graphql" in r.url:
                try:
                    got.append(r.text())
                except Exception:
                    pass

        page.on("response", on_resp)
        try:
            page.mouse.wheel(0, -50000)
            time.sleep(1)
            inp = page.locator("input[type=search]").first
            inp.click(timeout=8000)
            inp.fill("")
            time.sleep(0.5)
            inp.type(name, delay=90)
            time.sleep(4.5)
        except Exception as e:
            self.log("typeahead error " + str(e)[:80])
        page.remove_listener("response", on_resp)
        pages = []
        for t in got:
            for j in parse_json_blobs(t):
                pr = []
                find_key(j, "page_results", pr)
                for lst in pr:
                    for p in lst or []:
                        p = dict(p)
                        p["src"] = "typeahead"
                        pages.append(p)
        uniq = {}
        for p in pages:
            uniq.setdefault(p.get("page_id"), p)
        return list(uniq.values())

    @staticmethod
    def name_matches(name, cand):
        def norm(s):
            return set(re.sub(r"[^a-z0-9 ]", " ", (s or "").lower()).split()) - {"the", "with", "by", "for", "and", "of", "com", "official"}
        a, b = norm(name), norm(cand)
        if not a or not b:
            return False
        return len(a & b) >= max(1, min(2, len(a)))

    def pause(self):
        time.sleep(random.uniform(self.args.pause_min, self.args.pause_max))

    # ---- main loop
    def run(self, plan):
        from playwright.sync_api import sync_playwright
        t0 = time.time()
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=not self.args.headed)
            ctx = browser.new_context(user_agent=UA, viewport={"width": 1440, "height": 1000}, locale="en-US")
            page = ctx.new_page()
            for item in plan:
                kind, q = item["kind"], str(item["q"])
                group = item.get("group", "A")
                label = item.get("label", q)
                adv = item.get("advertiser")
                try:
                    if kind == "cobrand":
                        for platform in (self.args.cobrand_pages or ["Skool"]):
                            both = "%s %s" % (q, platform)
                            self.run_page(ctx, page, self.url_for("keyword", both), group, "cobrand: " + both, "keyword", both, adv, neighbor_cap=0)
                            self.pause()
                            phrase = "%s with %s" % (q, platform)
                            self.run_page(ctx, page, self.url_for("exact", phrase), group, "cobrand: " + phrase, "exact", phrase, adv, neighbor_cap=0)
                            self.pause()
                        continue
                    if kind == "page":
                        self.visited_pages.add(q)
                    url = self.url_for(kind, q)
                    ncap = self.args.max_neighbors_per_name if kind in ("name", "keyword", "exact") else None
                    _, fpages = self.run_page(ctx, page, url, group, label, kind, q, adv, collect_eu=(kind == "id"), neighbor_cap=ncap)
                    if kind == "name":
                        sugg = self.typeahead_pages(page, q) + fpages
                        hits, seen_pid = [], set()
                        for s_ in sugg:
                            if s_.get("page_id") and s_.get("page_id") not in seen_pid and self.name_matches(q, s_.get("name")):
                                seen_pid.add(s_.get("page_id"))
                                hits.append(s_)
                        hits = hits[: self.args.max_pages_per_name]
                        self.log("   typeahead for %r matched %s" % (q, [s.get("name") for s in hits]))
                        C.append_jsonl(self.out / "typeahead.jsonl", {"query": q, "suggestions": [{k: v for k, v in s.items() if k != "image_uri"} for s in sugg], "matched": [s.get("page_id") for s in hits]})
                        for s in hits:
                            pid = str(s.get("page_id"))
                            if pid in self.visited_pages:
                                continue
                            self.visited_pages.add(pid)
                            self.pause()
                            self.run_page(ctx, page, self.url_for("page", pid), group, "%s -> page: %s (%s)" % (q, s.get("name"), pid), "page", pid, adv)
                except Exception as e:
                    self.log("item failed %r: %s" % (q, str(e)[:160]))
                    self.write_search_row({"timestamp": C.now_iso(), "group": group, "label": label, "search_type": kind,
                                           "query": q, "url": "", "ads_found": "", "reported_result_count": "",
                                           "new_unique_ads": "", "term_hits": "", "notes": "error: " + str(e)[:150]})
                    try:
                        page.close()
                    except Exception:
                        pass
                    page = ctx.new_page()
                self.pause()
            # optional EU detail pass
            if self.args.eu_details:
                todo = [r for r in self.ads.values() if not r.get("eu")][: self.args.eu_details]
                self.log("EU detail pass on %d ads" % len(todo))
                for r in todo:
                    try:
                        self.run_page(ctx, page, self.url_for("id", r["ad_id"]), "EU", "detail " + r["ad_id"], "id", r["ad_id"], r.get("roster_advertiser"), collect_eu=True)
                    except Exception as e:
                        self.log("detail failed %s: %s" % (r["ad_id"], str(e)[:100]))
                    self.pause()
            browser.close()
        self.save()
        self.write_summary()
        self.log("done in %ds, unique ads %d" % (int(time.time() - t0), len(self.ads)))

    def write_summary(self):
        from collections import Counter
        adv = Counter(r["advertiser"] for r in self.ads.values())
        lines = ["# Pull summary", "", "Captured " + C.now_iso(), "", "Unique ads: %d" % len(self.ads), "",
                 "| Advertiser | Ads | Videos | Oldest start | Median days active |", "|---|---:|---:|---|---:|"]
        for name, n in adv.most_common():
            rs = [r for r in self.ads.values() if r["advertiser"] == name]
            vids = sum(1 for r in rs if r.get("video_hd_url") or r.get("video_sd_url"))
            starts = sorted(r["start_date"] for r in rs if r.get("start_date"))
            days = sorted(r["days_active"] for r in rs if r.get("days_active") is not None)
            med = days[len(days) // 2] if days else ""
            lines.append("| %s | %d | %d | %s | %s |" % (name, n, vids, starts[0] if starts else "", med))
        lines += ["", "Counts are what loaded, not Meta's totals; see searches.csv for reported result counts.",
                  "Active-only samples cannot estimate how many ads were launched and stopped."]
        (self.out / "SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


# ----------------------------------------------------------------------------- plan builders

def plan_from_advertisers(names, cobrand):
    plan = []
    for n in names:
        plan.append({"kind": "name", "q": n, "label": n, "group": "roster", "advertiser": n})
        if cobrand:
            plan.append({"kind": "cobrand", "q": n, "label": n, "group": "roster", "advertiser": n})
    return plan


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--plan", help="plan JSON file")
    ap.add_argument("--advertisers", nargs="*", help="advertiser names (builds a name + cobrand plan)")
    ap.add_argument("--ids", nargs="*", help="ad ids to fetch from their detail pages")
    ap.add_argument("--out", required=True, help="output folder, usually <workspace>/ads")
    ap.add_argument("--max-per-advertiser", type=int, default=40)
    ap.add_argument("--max-total", type=int, default=400)
    ap.add_argument("--max-per-search", type=int, default=60)
    ap.add_argument("--max-pages-per-name", type=int, default=3)
    ap.add_argument("--max-neighbors-per-name", type=int, default=20, help="keyword-search ads from other advertisers kept per search")
    ap.add_argument("--country", default="ALL")
    ap.add_argument("--include-inactive", action="store_true")
    ap.add_argument("--media-type", default="all", choices=["all", "image", "video", "meme", "image_and_meme", "none"])
    ap.add_argument("--no-media", action="store_true", help="do not download images or videos")
    ap.add_argument("--no-videos", action="store_true", help="download images and posters only")
    ap.add_argument("--video-max-mb", type=int, default=60)
    ap.add_argument("--no-cards", action="store_true", help="skip card screenshots")
    ap.add_argument("--eu-details", type=int, default=0, help="visit detail pages for up to N ads to capture EU reach data")
    ap.add_argument("--terms", nargs="*", help="brand or category terms to flag in term_hits")
    ap.add_argument("--cobrand-pages", nargs="*", default=["Skool"], help="platform pages that run ads for their creators")
    ap.add_argument("--no-cobrand", action="store_true")
    ap.add_argument("--pause-min", type=float, default=2.0)
    ap.add_argument("--pause-max", type=float, default=4.0)
    ap.add_argument("--headed", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    plan = []
    if args.plan:
        plan += json.loads(Path(args.plan).read_text(encoding="utf-8"))
    if args.advertisers:
        plan += plan_from_advertisers(args.advertisers, not args.no_cobrand)
    if args.ids:
        plan += [{"kind": "id", "q": i, "label": "id " + i, "group": "ids"} for i in args.ids]
    if not plan:
        ap.error("give --plan, --advertisers or --ids")

    puller = Puller(args)
    if args.dry_run:
        print("dry run: %d plan items, out=%s" % (len(plan), puller.out))
        for it in plan:
            if it["kind"] == "cobrand":
                for platform in (args.cobrand_pages or ["Skool"]):
                    print("  keyword ", puller.url_for("keyword", "%s %s" % (it["q"], platform)))
                    print("  exact   ", puller.url_for("exact", "%s with %s" % (it["q"], platform)))
            else:
                print("  %-8s" % it["kind"], puller.url_for(it["kind"], it["q"]))
        return 0
    C.need_playwright()
    puller.run(plan)
    return 0


if __name__ == "__main__":
    sys.exit(main())
