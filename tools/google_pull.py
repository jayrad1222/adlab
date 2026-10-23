#!/usr/bin/env python3
"""google_pull.py: read-only Google Ads Transparency Center pull (headless Playwright, no login).

Same manners as meta_pull.py: headless Chromium, desktop user agent, no login, one page at a
time, 2 to 4 second pauses, nothing is clicked that posts, likes or follows. The only typing is
the advertiser name in the site's own search box, which is how the Center resolves a name to
its advertiser ids.

What the site exposes (checked live October 2026)
  The Center is a JavaScript app that calls RPC endpoints under /anji/_/rpc/. The responses
  are JSON with numbered protobuf field names, readable enough to use:
    SearchService/SearchSuggestions   advertiser name -> [{name, AR id, country, ad count}]
    SearchService/SearchCreatives     advertiser or domain page -> 40 creatives per page with
                                      advertiser id, creative id, format code (1 text, 2 image,
                                      3 video), first and last shown timestamps, advertiser name
                                      and a preview-script URL
    LookupService/GetCreativeById     creative page -> variant previews, format code, regions
                                      with a last-shown date per region
  The creative's media is not in the RPC. The preview script (a GET to
  displayads-formats.googleusercontent.com) carries the YouTube thumbnail id for video ads and
  the static image URL for image ads, and the rendered creative page shows "Last shown",
  "Format", the region scope and "N of M variations". This tool reads all of those. Image
  creatives built as responsive HTML (no single image) only get card.png. Video ads record the
  YouTube URL in video_hd_url and the video is not downloaded. Field numbers may change; the
  raw RPC objects are kept in raw_snapshot so nothing is lost when they do.

Usage
  python -I google_pull.py --advertisers "Notion" --out <workspace>/ads
  python -I google_pull.py --domains notion.so --out <workspace>/ads
  python -I google_pull.py --advertiser-ids AR01024198173649797121 --out DIR
  python -I google_pull.py --advertisers "Notion" --out DIR --dry-run   (prints the URLs it would visit)

Outputs in --out: ads.jsonl (all ads, deduped on ad_id, records from other sources kept),
searches.csv, run.log, and <advertiser_slug>/<ad_id>/{ad.json, card.png, media/...}
"""
from __future__ import annotations

import argparse
import csv
import json
import random
import re
import sys
import time
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import adlab_common as C  # noqa: E402
import meta_pull as M  # noqa: E402

UA = M.UA
BASE = "https://adstransparency.google.com"
FORMAT_CODES = {1: "text", 2: "image", 3: "video"}
FETCH_CREATIVE_JS = """async ([adv, cr]) => {
  const body = 'f.req=' + encodeURIComponent(JSON.stringify({"1": adv, "2": cr, "5": {"1": 1, "2": 0, "3": 2840}}));
  const r = await fetch('/anji/_/rpc/LookupService/GetCreativeById?authuser=', {method: 'POST', credentials: 'include',
     headers: {'content-type': 'application/x-www-form-urlencoded;charset=UTF-8', 'x-framework-xsrf-token': ''}, body: body});
  return [r.status, await r.text()];
}"""
SEARCH_COLS = ["timestamp", "group", "label", "search_type", "query", "url", "ads_found", "reported_result_count",
               "new_unique_ads", "term_hits", "notes"]


# ----------------------------------------------------------------------------- url builders

def home_url(region):
    return BASE + "/?region=" + urllib.parse.quote(region)


def domain_url(domain, region):
    return BASE + "/?region=" + urllib.parse.quote(region) + "&domain=" + urllib.parse.quote(domain)


def advertiser_url(adv_id, region):
    return BASE + "/advertiser/" + adv_id + "?region=" + urllib.parse.quote(region)


def creative_url(adv_id, cr_id, region):
    return BASE + "/advertiser/" + adv_id + "/creative/" + cr_id + "?region=" + urllib.parse.quote(region)


# ----------------------------------------------------------------------------- parsing helpers

def ts_to_date(ts):
    """Google gives seconds since the epoch as a string in field "1" of a timestamp object."""
    if isinstance(ts, dict):
        ts = ts.get("1")
    if not ts:
        return None
    try:
        return datetime.fromtimestamp(int(ts), tz=timezone.utc).strftime("%Y-%m-%d")
    except Exception:
        return None


def yyyymmdd(n):
    try:
        s = str(int(n))
        return s[:4] + "-" + s[4:6] + "-" + s[6:8]
    except Exception:
        return None


def parse_search_creatives(obj):
    """SearchCreatives RPC body -> list of creative summaries."""
    out = []
    if not isinstance(obj, dict):
        return out
    for it in obj.get("1") or []:
        if not isinstance(it, dict) or not it.get("2"):
            continue
        preview, preview_html = None, None
        try:
            preview = it["3"]["1"]["4"]
        except Exception:
            pass
        try:
            preview_html = it["3"]["3"]["2"]
        except Exception:
            pass
        code = it.get("4")
        out.append({
            "advertiser_id": it.get("1"),
            "creative_id": it.get("2"),
            "format_code": code,
            "format": FORMAT_CODES.get(code, "unknown"),
            "first_shown": ts_to_date(it.get("6")),
            "last_shown": ts_to_date(it.get("7")),
            "advertiser": it.get("12"),
            "preview_url": preview,
            "preview_html": preview_html,
            "raw": it,
        })
    return out


def parse_suggestions(obj):
    """SearchSuggestions RPC body -> (advertisers, domains)."""
    advs, doms = [], []
    if not isinstance(obj, dict):
        return advs, doms
    for it in obj.get("1") or []:
        a = it.get("1") if isinstance(it, dict) else None
        if isinstance(a, dict) and a.get("2"):
            count = None
            try:
                count = int(a["4"]["2"]["1"])
            except Exception:
                pass
            advs.append({"name": a.get("1"), "advertiser_id": a.get("2"), "country": a.get("3"), "ad_count": count})
        d = it.get("2") if isinstance(it, dict) else None
        if isinstance(d, dict) and d.get("1"):
            doms.append(d["1"])
    return advs, doms


def parse_creative_detail(obj):
    """GetCreativeById RPC body -> dict with variants, regions, format code, dates."""
    if not isinstance(obj, dict) or not isinstance(obj.get("1"), dict):
        return {}
    c = obj["1"]
    variants = []
    for v in c.get("5") or []:
        if not isinstance(v, dict):
            continue
        html = None
        try:
            html = v["3"]["2"]
        except Exception:
            pass
        purl = None
        try:
            purl = v["1"]["4"]
        except Exception:
            pass
        variants.append({"html": html, "preview_url": purl})
    regions = []
    for r in c.get("17") or []:
        if isinstance(r, dict):
            regions.append({"region_code": r.get("1"), "last_shown": yyyymmdd(r.get("5")) if r.get("5") else None})
    code = c.get("8")
    return {
        "advertiser_id": c.get("1"), "creative_id": c.get("2"),
        "last_shown": ts_to_date(c.get("4")),
        "format_code": code, "format": FORMAT_CODES.get(code, "unknown"),
        "variants": variants, "regions": regions,
        "advertiser": (c.get("22") or {}).get("1") if isinstance(c.get("22"), dict) else None,
    }


def js_unescape(s):
    """Decode the JS string literal escapes the preview script uses (\\x3c, \\u003d, \\', \\n)."""
    def rep(m):
        t = m.group(0)
        if t.startswith("\\x"):
            return chr(int(t[2:], 16))
        if t.startswith("\\u"):
            return chr(int(t[2:], 16))
        return {"\\n": "\n", "\\r": "", "\\t": "\t", "\\'": "'", '\\"': '"', "\\\\": "\\", "\\/": "/"}.get(t, t[1:])
    return re.sub(r"\\x[0-9a-fA-F]{2}|\\u[0-9a-fA-F]{4}|\\.", rep, s)


def strip_tags(html):
    t = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html or "", flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    t = t.replace("&nbsp;", " ").replace("&amp;", "&").replace("&quot;", '"').replace("&#39;", "'")
    return re.sub(r"\s+", " ", t).strip()


def parse_preview_script(text):
    """Preview content.js -> {youtube_id, image_urls, dest_url, kind, width, height, creative_type}."""
    out = {"youtube_id": None, "image_urls": [], "dest_url": None, "kind": None, "width": None, "height": None,
           "creative_type": None}
    if not text:
        return out
    m = re.search(r"ytimg\.com/vi/([A-Za-z0-9_-]{11})/", text)
    if m:
        out["youtube_id"] = m.group(1)
    body = text
    m = re.search(r"insertPreviewHtmlContent\('[^']*', '[^']*', '((?:[^'\\]|\\.)*)'", text)
    if m:
        out["kind"] = "html"
        body = js_unescape(m.group(1))
    elif "insertPreviewImageContent" in text:
        out["kind"] = "image"
    imgs = []
    for u in re.findall(r"https?://[^\s'\"<>\\)]+", body):
        u = u.replace("&amp;", "&")
        if re.search(r"googlesyndication\.com/(?:archive/)?simgad/\d+", u) or "googleusercontent.com" in u \
                and "displayads-formats" not in u:
            u = re.split(r"[\"'&]quot;", u)[0]
            if u not in imgs:
                imgs.append(u)
    out["image_urls"] = imgs
    m = re.search(r"adurl=([^&'\"\\\s]+)", body)
    if m and m.group(1):
        out["dest_url"] = urllib.parse.unquote(m.group(1))
    m = re.search(r'"previewMetadata":\[\{[^}]*\}', text)
    if m:
        try:
            meta = json.loads(m.group(0)[len('"previewMetadata":['):] )
            out["width"], out["height"], out["creative_type"] = meta.get("width"), meta.get("height"), meta.get("creativeType")
        except Exception:
            pass
    return out


def parse_creative_dom(text):
    """innerText of the creative-details element -> {last_shown, format, region_text, variant_index, variant_count}."""
    out = {"last_shown": None, "format": None, "region_text": None, "variant_index": None, "variant_count": None}
    if not text:
        return out
    m = re.search(r"Last shown:\s*([A-Za-z]{3,9} \d{1,2}, \d{4})", text)
    if m:
        for fmt in ("%b %d, %Y", "%B %d, %Y"):
            try:
                out["last_shown"] = datetime.strptime(m.group(1), fmt).strftime("%Y-%m-%d")
                break
            except Exception:
                pass
    m = re.search(r"Format:\s*([A-Za-z]+)", text)
    if m:
        out["format"] = m.group(1).lower()
    m = re.search(r"(Shown (?:anywhere|in [^\n]+))", text)
    if m:
        out["region_text"] = m.group(1).strip()
    m = re.search(r"(\d+) of (\d+) variations?", text)
    if m:
        out["variant_index"], out["variant_count"] = int(m.group(1)), int(m.group(2))
    return out


def blank_record():
    keys = ["source", "ad_id", "advertiser", "advertiser_id", "advertiser_slug", "platforms", "start_date", "end_date",
            "is_active", "days_active", "variant_count", "collation_id", "format", "body_text", "title",
            "link_description", "caption", "cta_text", "cta_type", "link_url", "image_url", "video_preview_image_url",
            "video_hd_url", "video_sd_url", "cards", "page_like_count", "page_profile_uri", "page_categories", "byline",
            "term_hits", "eu", "library_url", "raw_snapshot", "link_domain", "link_path", "dest_type"]
    return {k: None for k in keys}


def normalize(item, detail, preview, dom, terms, region="anywhere"):
    """Creative summary + GetCreativeById + preview script + DOM text -> Ad Lab record."""
    detail = detail or {}
    preview = preview or {}
    dom = dom or {}
    adv_id = item.get("advertiser_id") or detail.get("advertiser_id") or ""
    cr_id = item.get("creative_id") or detail.get("creative_id")
    name = item.get("advertiser") or detail.get("advertiser") or "unknown"
    fmt = dom.get("format") or item.get("format") or detail.get("format") or "unknown"
    if fmt not in ("image", "video", "text", "carousel"):
        fmt = "unknown"
    start = item.get("first_shown")
    end = dom.get("last_shown") or item.get("last_shown") or detail.get("last_shown")
    yt = preview.get("youtube_id")
    image_url = None
    for u in preview.get("image_urls") or []:
        image_url = u
        break
    if not image_url:
        for h in [item.get("preview_html")] + [v.get("html") for v in detail.get("variants") or []]:
            m = re.search(r'src="([^"]+)"', h or "")
            if m:
                image_url = m.group(1)
                break
    body = dom.get("frame_text") or None
    if not body and fmt == "text":
        texts = [strip_tags(v.get("html")) for v in detail.get("variants") or [] if v.get("html")]
        texts = [t for t in texts if t]
        body = texts[0] if texts else None
    link = preview.get("dest_url")
    blob = " ".join(str(x) for x in [name, body, link] if x).lower()
    hits = [t for t in (terms or []) if t and t.lower() in blob]
    rec = blank_record()
    rec.update({
        "source": "google",
        "ad_id": "g-" + str(cr_id),
        "advertiser": name,
        "advertiser_id": str(adv_id),
        "advertiser_slug": C.slugify(name),
        "platforms": ["youtube"] if (fmt == "video" or yt) else ["google"],
        "start_date": start,
        "end_date": end,
        "is_active": None,
        "days_active": C.days_between(start, end),
        "variant_count": dom.get("variant_count") or (len(detail["variants"]) if detail.get("variants") else None),
        "format": fmt,
        "body_text": body,
        "link_url": link,
        "image_url": image_url if not yt else image_url,
        "video_preview_image_url": ("https://i.ytimg.com/vi/%s/hqdefault.jpg" % yt) if yt else None,
        "video_hd_url": ("https://www.youtube.com/watch?v=%s" % yt) if yt else None,
        "cards": [],
        "term_hits": hits,
        "library_url": creative_url(adv_id, cr_id, region),
        "raw_snapshot": {"search_item": item.get("raw"), "detail": detail, "preview": preview, "dom": dom},
        "youtube_id": yt,
        "format_code": item.get("format_code") or detail.get("format_code"),
        "region_text": dom.get("region_text"),
        "regions": detail.get("regions"),
    })
    rec.update(M.classify_link(link))
    return rec


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
            if r.get("source") == "google":
                self.per_adv[r.get("advertiser_id")] = self.per_adv.get(r.get("advertiser_id"), 0) + 1
        self.terms = args.terms or []
        self.visited_advertisers = set()

    def log(self, msg):
        C.log(msg, self.logfile)

    def pause(self):
        time.sleep(random.uniform(self.args.pause_min, self.args.pause_max))

    def save(self):
        C.write_jsonl(self.ads_path, self.ads.values())

    def write_search_row(self, row):
        new = not self.search_path.exists()
        with self.search_path.open("a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=SEARCH_COLS)
            if new:
                w.writeheader()
            w.writerow(row)

    def ad_dir(self, rec):
        return self.out / rec["advertiser_slug"] / rec["ad_id"]

    def write_ad_json(self, rec):
        d = self.ad_dir(rec)
        d.mkdir(parents=True, exist_ok=True)
        (d / "ad.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")

    def google_count(self):
        return sum(1 for r in self.ads.values() if r.get("source") == "google")

    # ---- network helpers
    @staticmethod
    def rpc_bodies(responses, name):
        out = []
        for r in responses:
            if name in r.url:
                try:
                    out.append(json.loads(r.text()))
                except Exception:
                    pass
        return out

    @staticmethod
    def wait_until(pred, timeout):
        t0 = time.time()
        while time.time() - t0 < timeout:
            if pred():
                return True
            time.sleep(0.5)
        return False

    def fetch_text(self, ctx, url):
        try:
            r = ctx.request.get(url, timeout=30000)
            if r.ok:
                return r.text()
        except Exception as e:
            self.log("fetch failed %s: %s" % (url[:60], str(e)[:80]))
        return None

    def download(self, ctx, url, base):
        for ext in (".jpg", ".png", ".webp", ".gif"):
            if base.with_suffix(ext).exists():
                return base.with_suffix(ext)
        base.parent.mkdir(parents=True, exist_ok=True)
        try:
            r = ctx.request.get(url, timeout=30000)
            if not r.ok:
                return None
            ct = r.headers.get("content-type", "")
            ext = ".png" if "png" in ct else ".webp" if "webp" in ct else ".gif" if "gif" in ct else ".jpg"
            p = base.with_suffix(ext)
            p.write_bytes(r.body())
            return p
        except Exception as e:
            self.log("download failed %s: %s" % (base.name, str(e)[:80]))
            return None

    def download_media(self, ctx, rec):
        if self.args.no_media:
            return
        files = rec.setdefault("files", {})
        d = self.ad_dir(rec) / "media"
        if rec.get("image_url") and not files.get("creative"):
            p = self.download(ctx, rec["image_url"], d / "creative")
            if p:
                files["creative"] = str(p.relative_to(self.out))
        if rec.get("video_preview_image_url") and not files.get("poster"):
            p = self.download(ctx, rec["video_preview_image_url"], d / "poster")
            if p:
                files["poster"] = str(p.relative_to(self.out))

    # ---- name -> advertiser ids via the site's own search box
    def resolve_name(self, page, name):
        got = []
        page.on("response", lambda r: got.append(r) if "/anji/_/rpc/" in r.url else None)
        try:
            page.goto(home_url(self.args.region), wait_until="domcontentloaded", timeout=60000)
            time.sleep(3)
            inp = page.locator("input").first
            inp.click(timeout=10000)
            inp.fill("")
            inp.type(name, delay=80)
            seen = lambda: any("SearchSuggestions" in r.url for r in got)  # noqa: E731
            tries = 0
            while not self.wait_until(seen, 10) and tries < 3:
                # the app sometimes attaches its listener after the first keystrokes; retype the last one
                tries += 1
                page.keyboard.press("Backspace")
                time.sleep(0.4)
                page.keyboard.type(name[-1], delay=90)
            time.sleep(2)
        except Exception as e:
            self.log("typeahead error for %r: %s" % (name, str(e)[:100]))
        advs, doms = [], []
        for j in self.rpc_bodies(got, "SearchSuggestions"):
            a, d = parse_suggestions(j)
            advs += a
            doms += d
        C.append_jsonl(self.out / "typeahead.jsonl", {"source": "google", "query": name, "advertisers": advs, "domains": doms})
        uniq = {}
        for a in advs:
            if a["advertiser_id"] not in uniq and M.Puller.name_matches(name, a["name"]):
                uniq[a["advertiser_id"]] = a
        hits = sorted(uniq.values(), key=lambda a: -(a.get("ad_count") or 0))[: self.args.max_advertisers_per_name]
        self.log("   typeahead for %r -> %s" % (name, [(a["name"], a["advertiser_id"], a["ad_count"]) for a in hits]))
        return hits

    # ---- one listing page (advertiser or domain)
    def run_listing(self, ctx, page, url, group, label, stype, query, roster=None, only_adv=None):
        got = []
        handler = lambda r: got.append(r) if "/anji/_/rpc/" in r.url else None  # noqa: E731
        page.on("response", handler)
        note = ""
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
        except Exception as e:
            note = "goto error: " + str(e)[:120]
        self.wait_until(lambda: any("SearchCreatives" in r.url for r in got), 20)
        time.sleep(3)
        if "accounts.google.com" in page.url:
            note += " redirected to sign-in"

        def items():
            seen, out = set(), []
            for j in self.rpc_bodies(got, "SearchCreatives"):
                for it in parse_search_creatives(j):
                    if it["creative_id"] not in seen:
                        seen.add(it["creative_id"])
                        out.append(it)
            return out

        found = items()
        stale = 0
        while len(found) < self.args.max_per_advertiser and stale < 2:
            n0 = len(found)
            try:
                page.mouse.wheel(0, 8000)
                time.sleep(1.5)
                page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
            except Exception:
                pass
            time.sleep(3)
            found = items()
            stale = stale + 1 if len(found) == n0 else 0
        page.remove_listener("response", handler)
        if only_adv:
            found = [it for it in found if it["advertiser_id"] == only_adv]
        self.log("[%s] %r (%s) listing -> %d creatives %s" % (group, label, stype, len(found), note))

        new, hits_n, this_ids, capped = 0, 0, [], 0
        for it in found:
            aid = "g-" + str(it["creative_id"])
            if aid in self.ads:
                prev = self.ads[aid]
                if [group, label] not in prev.get("found_via", []):
                    prev.setdefault("found_via", []).append([group, label])
                this_ids.append(aid)
                if prev.get("term_hits"):
                    hits_n += 1
                continue
            cnt = self.per_adv.get(it["advertiser_id"], 0)
            if cnt >= self.args.max_per_advertiser or self.google_count() >= self.args.max_total:
                capped += 1
                continue
            self.pause()
            try:
                rec = self.run_creative(ctx, page, it)
            except Exception as e:
                self.log("creative failed %s: %s" % (it["creative_id"], str(e)[:120]))
                continue
            if roster:
                rec["roster_advertiser"] = roster
            rec["found_via"] = [[group, label]]
            rec["first_seen_utc"] = C.now_iso()
            self.ads[aid] = rec
            self.per_adv[it["advertiser_id"]] = cnt + 1
            new += 1
            this_ids.append(aid)
            if rec.get("term_hits"):
                hits_n += 1
            self.download_media(ctx, rec)
            self.write_ad_json(rec)
            self.save()
        self.save()
        self.write_search_row({
            "timestamp": C.now_iso(), "group": group, "label": label, "search_type": stype, "query": query,
            "url": url, "ads_found": len(this_ids), "reported_result_count": "", "new_unique_ads": new,
            "term_hits": hits_n, "notes": (note + (" capped %d" % capped if capped else "")).strip(),
        })
        self.log("[%s] %r -> %d ads, %d new, capped=%d, google total=%d" % (group, label, len(this_ids), new, capped, self.google_count()))
        return this_ids

    @staticmethod
    def frame_text(page):
        """Visible text of the rendered creative (same-origin /adframe iframes), CSS and script lines dropped."""
        texts = []
        for fr in page.frames:
            try:
                if "/adframe" not in fr.url:
                    continue
                t = fr.evaluate("() => document.body ? document.body.innerText : ''")
            except Exception:
                continue
            lines = [ln.strip() for ln in (t or "").split("\n")]
            lines = [ln for ln in lines if ln and "{" not in ln and "}" not in ln and not ln.startswith("window.")]
            if lines:
                texts.append(" | ".join(lines))
        return texts[0][:2000] if texts else None

    # ---- one creative page
    def run_creative(self, ctx, page, it):
        url = creative_url(it["advertiser_id"], it["creative_id"], self.args.region)
        got = []
        handler = lambda r: got.append(r) if "/anji/_/rpc/" in r.url else None  # noqa: E731
        page.on("response", handler)
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        self.wait_until(lambda: any("GetCreativeById" in r.url for r in got), 30)
        time.sleep(4)
        detail = {}
        for j in self.rpc_bodies(got, "GetCreativeById"):
            detail = parse_creative_detail(j)
            if detail:
                break
        page.remove_listener("response", handler)
        if not detail:
            # the app often issues this RPC from a worker Playwright does not observe; ask from the page itself
            try:
                st, txt = page.evaluate(FETCH_CREATIVE_JS, [it["advertiser_id"], it["creative_id"]])
                if st == 200:
                    detail = parse_creative_detail(json.loads(txt))
            except Exception as e:
                self.log("in-page GetCreativeById failed %s: %s" % (it["creative_id"], str(e)[:80]))
        dom_text = ""
        try:
            dom_text = page.locator("creative-details").first.inner_text(timeout=8000)
        except Exception:
            try:
                dom_text = page.evaluate("() => document.body.innerText")
            except Exception:
                pass
        dom = parse_creative_dom(dom_text)
        dom["frame_text"] = self.frame_text(page)
        preview = {}
        purl = it.get("preview_url")
        if not purl and detail.get("variants"):
            purl = detail["variants"][0].get("preview_url")
        if purl:
            preview = parse_preview_script(self.fetch_text(ctx, purl))
        rec = normalize(it, detail, preview, dom, self.terms, self.args.region)
        if not self.args.no_cards:
            try:
                p = self.ad_dir(rec) / "card.png"
                p.parent.mkdir(parents=True, exist_ok=True)
                page.locator("creative-details").first.screenshot(path=str(p), timeout=15000)
                rec.setdefault("files", {})["card"] = str(p.relative_to(self.out))
            except Exception as e:
                self.log("card screenshot failed %s: %s" % (it["creative_id"], str(e)[:80]))
        return rec

    # ---- main loop
    def run(self, plan):
        from playwright.sync_api import sync_playwright
        t0 = time.time()
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=not self.args.headed)
            ctx = browser.new_context(user_agent=UA, viewport={"width": 1440, "height": 1000}, locale="en-US")
            page = ctx.new_page()
            for item in plan:
                kind, q, group, label = item["kind"], item["q"], item.get("group", "roster"), item.get("label", item["q"])
                try:
                    if kind == "name":
                        hits = self.resolve_name(page, q)
                        if not hits:
                            self.write_search_row({"timestamp": C.now_iso(), "group": group, "label": label, "search_type": "name",
                                                   "query": q, "url": home_url(self.args.region), "ads_found": 0,
                                                   "reported_result_count": "", "new_unique_ads": 0, "term_hits": 0,
                                                   "notes": "no advertiser matched in typeahead"})
                        for a in hits:
                            if a["advertiser_id"] in self.visited_advertisers:
                                continue
                            self.visited_advertisers.add(a["advertiser_id"])
                            self.pause()
                            self.run_listing(ctx, page, advertiser_url(a["advertiser_id"], self.args.region), group,
                                             "%s -> %s (%s)" % (q, a["name"], a["advertiser_id"]), "advertiser",
                                             a["advertiser_id"], roster=q, only_adv=a["advertiser_id"])
                    elif kind == "advertiser":
                        self.visited_advertisers.add(q)
                        self.run_listing(ctx, page, advertiser_url(q, self.args.region), group, label, "advertiser", q, only_adv=q)
                    elif kind == "domain":
                        self.run_listing(ctx, page, domain_url(q, self.args.region), group, label, "domain", q)
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
            browser.close()
        self.save()
        self.log("done in %ds, google ads in file %d" % (int(time.time() - t0), self.google_count()))


# ----------------------------------------------------------------------------- cli

def build_plan(args):
    plan = []
    for n in args.advertisers or []:
        plan.append({"kind": "name", "q": n, "label": n, "group": "roster"})
    for a in args.advertiser_ids or []:
        plan.append({"kind": "advertiser", "q": a, "label": "advertiser " + a, "group": "roster"})
    for d in args.domains or []:
        plan.append({"kind": "domain", "q": d, "label": "domain " + d, "group": "domains"})
    return plan


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--advertisers", nargs="*", help="advertiser names, resolved through the site's typeahead")
    ap.add_argument("--advertiser-ids", nargs="*", help="advertiser ids (AR...) to pull directly")
    ap.add_argument("--domains", nargs="*", help="domains to search (?domain=...)")
    ap.add_argument("--out", required=True, help="output folder, usually <workspace>/ads")
    ap.add_argument("--region", default="anywhere", help="region filter, default anywhere")
    ap.add_argument("--max-per-advertiser", type=int, default=40)
    ap.add_argument("--max-total", type=int, default=400)
    ap.add_argument("--max-advertisers-per-name", type=int, default=2)
    ap.add_argument("--terms", nargs="*", help="brand or category terms to flag in term_hits")
    ap.add_argument("--no-media", action="store_true", help="do not download images or posters")
    ap.add_argument("--no-cards", action="store_true", help="skip card screenshots")
    ap.add_argument("--pause-min", type=float, default=2.0)
    ap.add_argument("--pause-max", type=float, default=4.0)
    ap.add_argument("--headed", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    plan = build_plan(args)
    if not plan:
        ap.error("give --advertisers, --advertiser-ids or --domains")
    if args.dry_run:
        print("dry run: %d plan items, out=%s" % (len(plan), Path(args.out)))
        for it in plan:
            if it["kind"] == "name":
                print("  name      ", home_url(args.region), "(type %r in the search box, then each matched /advertiser/<AR>)" % it["q"])
            elif it["kind"] == "advertiser":
                print("  advertiser", advertiser_url(it["q"], args.region))
            else:
                print("  domain    ", domain_url(it["q"], args.region))
        print("  then each creative: " + creative_url("<AR>", "<CR>", args.region))
        return 0
    C.need_playwright()
    Puller(args).run(plan)
    return 0


if __name__ == "__main__":
    sys.exit(main())
