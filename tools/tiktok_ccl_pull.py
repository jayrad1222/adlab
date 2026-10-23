#!/usr/bin/env python3
"""tiktok_ccl_pull.py: read-only TikTok Commercial Content Library pull (headless Playwright, no login).

Same manners as meta_pull.py: headless Chromium, desktop user agent, no login, one page at a
time, 2 to 4 second pauses, nothing is clicked that posts, likes or follows. The only click is
the library's own "View more" button to load the next page of results.

Coverage: the Commercial Content Library only lists ads shown in the EEA, Switzerland and the
UK. An advertiser with no European delivery shows nothing here even if it runs TikTok ads
elsewhere; use the assisted Creative Center flow for that.

What the site exposes (checked live October 2026)
  Loading https://library.tiktok.com/ads?region=all&adv_name=<query>&query_type=1&... makes the
  page POST to /api/v1/search and this tool reads that response: {"data": [...], "total": N,
  "has_more": bool, "search_id": ...}. Each item has id, name (advertiser), first_shown_date and
  last_shown_date (ms), videos[{video_url, cover_img}], image_urls, title, subject, type,
  audit_status, estimated_audience, show_mode. query_type=1 is an advertiser-name search (fuzzy:
  "Skool" matched Vans Old Skool); query_type=2 is a keyword search (--keywords). The detail
  page /ads/detail/?ad_id=<id> calls /api/v1/items/<id>/details and that adds the advertiser's
  business id, registered location and TikTok account, the sponsor ("Paid for by"), an app or
  download URL, and the targeting block (age, gender, audience size per region), which is the
  EU transparency signal and is stored in the record's eu field. Cover images are downloaded;
  videos are not (the video_url is a signed, expiring CDN proxy and is kept in video_hd_url).
  The site is slow headless (10 to 90 s before its first search fires) and throttles repeated
  automated loads with HTTP 421 "system busy"; when that happens the detail pass comes back
  empty, searches.csv says so in notes, and the records still carry everything the search
  response gave. Rerun later with --max-per-advertiser small; records already in ads.jsonl
  are skipped, not refetched.

Usage
  python -I tiktok_ccl_pull.py --advertisers "Duolingo" --out <workspace>/ads
  python -I tiktok_ccl_pull.py --keywords "language learning" --out <workspace>/ads
  python -I tiktok_ccl_pull.py --advertisers "Duolingo" --out DIR --dry-run   (prints the URLs it would visit)

Outputs in --out: ads.jsonl (all ads, deduped on ad_id, records from other sources kept),
searches.csv, run.log, and <advertiser_slug>/<ad_id>/{ad.json, card.png, media/...}
"""
from __future__ import annotations

import argparse
import csv
import json
import random
import sys
import time
import urllib.parse
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import adlab_common as C  # noqa: E402
import meta_pull as M  # noqa: E402

UA = M.UA
BASE = "https://library.tiktok.com"
FETCH_DETAIL_JS = """async (id) => {
  const r = await fetch('/api/v1/items/' + id + '/details?lang=en-US', {credentials: 'include'});
  return [r.status, await r.text()];
}"""
SEARCH_COLS = ["timestamp", "group", "label", "search_type", "query", "url", "ads_found", "reported_result_count",
               "new_unique_ads", "term_hits", "notes"]


# ----------------------------------------------------------------------------- url builders

def window_ms(days):
    end = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
    start = end - timedelta(days=days + 1)
    return int(start.timestamp() * 1000), int(end.timestamp() * 1000)


def search_url(q, kind, region, start_ms, end_ms):
    qt = "1" if kind == "name" else "2"
    return (BASE + "/ads?region=" + urllib.parse.quote(region) + "&start_time=%d&end_time=%d" % (start_ms, end_ms)
            + "&adv_name=" + urllib.parse.quote(q) + "&adv_biz_ids=&query_type=" + qt + "&sort_type=last_shown_date,desc")


def detail_url(ad_id):
    return BASE + "/ads/detail/?ad_id=" + str(ad_id)


# ----------------------------------------------------------------------------- parsing helpers

def ms_to_date(ms):
    if not ms:
        return None
    try:
        return datetime.fromtimestamp(int(ms) / 1000.0, tz=timezone.utc).strftime("%Y-%m-%d")
    except Exception:
        return None


def parse_search(obj):
    """/api/v1/search body -> (items, total, has_more)."""
    if not isinstance(obj, dict):
        return [], None, None
    items = [d for d in (obj.get("data") or []) if isinstance(d, dict) and d.get("id")]
    return items, obj.get("total"), obj.get("has_more")


def parse_detail(obj):
    """/api/v1/items/<id>/details body -> {ad, advertiser, sponsor, targeting, display_mode}."""
    if not isinstance(obj, dict):
        return {}
    d = obj.get("data") if isinstance(obj.get("data"), dict) else obj
    ad = d.get("ad") if isinstance(d.get("ad"), dict) else {}
    adv = d.get("advertiser") if isinstance(d.get("advertiser"), dict) else {}
    return {
        "ad": ad,
        "advertiser": adv,
        "sponsor": d.get("sponsor") or adv.get("sponsor") or None,
        "targeting": d.get("targeting") if isinstance(d.get("targeting"), dict) else None,
        "display_mode": d.get("display_mode"),
    }


def blank_record():
    keys = ["source", "ad_id", "advertiser", "advertiser_id", "advertiser_slug", "platforms", "start_date", "end_date",
            "is_active", "days_active", "variant_count", "collation_id", "format", "body_text", "title",
            "link_description", "caption", "cta_text", "cta_type", "link_url", "image_url", "video_preview_image_url",
            "video_hd_url", "video_sd_url", "cards", "page_like_count", "page_profile_uri", "page_categories", "byline",
            "term_hits", "eu", "library_url", "raw_snapshot", "link_domain", "link_path", "dest_type"]
    return {k: None for k in keys}


def normalize(item, detail, terms):
    """Search item + detail dict -> Ad Lab record."""
    detail = detail or {}
    ad = detail.get("ad") or {}
    adv = detail.get("advertiser") or {}
    name = item.get("name") or ad.get("name") or adv.get("name") or "unknown"
    videos = item.get("videos") or ad.get("videos") or []
    images = item.get("image_urls") or ad.get("image_urls") or []
    cover = None
    video_url = None
    if videos and isinstance(videos[0], dict):
        cover = videos[0].get("cover_img")
        video_url = videos[0].get("video_url")
    if videos:
        fmt = "video"
    elif images:
        fmt = "image"
    else:
        fmt = "unknown"
    image_url = images[0] if images else cover
    start = ms_to_date(item.get("first_shown_date") or ad.get("first_shown_date"))
    end = ms_to_date(item.get("last_shown_date") or ad.get("last_shown_date"))
    link = ad.get("download_url") or None
    tt = adv.get("tt_user") if isinstance(adv.get("tt_user"), dict) else {}
    eu = None
    if detail:
        eu = {k: v for k, v in {
            "estimated_audience": item.get("estimated_audience") or ad.get("estimated_audience"),
            "target_audience_size": (detail.get("targeting") or {}).get("target_audience_size"),
            "targeting": detail.get("targeting"),
            "impression": item.get("impression") if item.get("impression") not in (None, 0) else None,
            "spent": item.get("spent") or None,
        }.items() if v not in (None, "", "-", {}, [])} or None
    title = item.get("title") or ad.get("title")
    blob = " ".join(str(x) for x in [name, title, item.get("subject"), detail.get("sponsor"), tt.get("username"), link] if x).lower()
    hits = [t for t in (terms or []) if t and t.lower() in blob]
    rec = blank_record()
    rec.update({
        "source": "tiktok-ccl",
        "ad_id": "tt-" + str(item["id"]),
        "advertiser": name,
        "advertiser_id": str(adv.get("adv_biz_ids") or ""),
        "advertiser_slug": C.slugify(name),
        "platforms": ["tiktok"],
        "start_date": start,
        "end_date": end,
        "is_active": None,
        "days_active": C.days_between(start, end),
        "variant_count": None,
        "format": fmt,
        "title": title,
        "link_url": link,
        "image_url": image_url if fmt != "video" else None,
        "video_preview_image_url": cover if fmt == "video" else None,
        "video_hd_url": video_url,
        "cards": [],
        "page_profile_uri": tt.get("profile_web_link"),
        "page_categories": [item.get("subject")] if item.get("subject") else None,
        "byline": detail.get("sponsor") or None,
        "term_hits": hits,
        "eu": eu,
        "library_url": detail_url(item["id"]),
        "raw_snapshot": {"search_item": item, "detail": detail},
        "tiktok_username": tt.get("username"),
        "registry_location": adv.get("registry_location"),
        "audit_status": item.get("audit_status"),
        "ad_type_code": item.get("type"),
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
            if r.get("source") == "tiktok-ccl":
                self.per_adv[r.get("advertiser_slug")] = self.per_adv.get(r.get("advertiser_slug"), 0) + 1
        self.terms = args.terms or []
        self.start_ms, self.end_ms = window_ms(args.days)
        self.empty_details = 0

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

    def tt_count(self):
        return sum(1 for r in self.ads.values() if r.get("source") == "tiktok-ccl")

    @staticmethod
    def wait_until(pred, timeout):
        t0 = time.time()
        while time.time() - t0 < timeout:
            if pred():
                return True
            time.sleep(0.5)
        return False

    @staticmethod
    def wait_for_search(page, got, timeout):
        t0 = time.time()
        while time.time() - t0 < timeout:
            if got:
                return True
            time.sleep(5)
            try:
                page.mouse.wheel(0, 600)
                time.sleep(0.5)
                page.mouse.wheel(0, -600)
            except Exception:
                pass
        return len(got) > 0

    @staticmethod
    def bodies(responses, needle):
        out = []
        for r in responses:
            if needle in r.url:
                try:
                    out.append(json.loads(r.text()))
                except Exception:
                    pass
        return out

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

    # ---- one search page
    def run_search(self, ctx, page, kind, q, group, label):
        url = search_url(q, kind, self.args.region, self.start_ms, self.end_ms)
        got = []
        handler = lambda r: got.append(r) if "/api/v1/search" in r.url else None  # noqa: E731
        page.on("response", handler)
        note = ""
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
        except Exception as e:
            note = "goto error: " + str(e)[:120]
        # the app fires its search only after it has fully loaded, which takes 10 to 90 s headless;
        # poll with small scroll nudges, and reload once if nothing comes
        if not self.wait_for_search(page, got, 90):
            try:
                page.reload(wait_until="domcontentloaded", timeout=60000)
            except Exception:
                pass
            if not self.wait_for_search(page, got, 60):
                note += " no search response after 150s and one reload"
        time.sleep(2)

        def collect():
            seen, items, total = set(), [], None
            for j in self.bodies(got, "/api/v1/search"):
                its, tot, _ = parse_search(j)
                total = tot if tot is not None else total
                for it in its:
                    if str(it["id"]) not in seen:
                        seen.add(str(it["id"]))
                        items.append(it)
            return items, total

        items, total = collect()
        clicks = 0
        while len(items) < self.args.max_per_search and clicks < self.args.max_pages_per_search:
            n_resp = len(got)
            try:
                btn = page.get_by_text("View more", exact=False).first
                btn.scroll_into_view_if_needed(timeout=5000)
                btn.click(timeout=5000)
            except Exception:
                break
            clicks += 1
            self.wait_until(lambda: len(got) > n_resp, 60)
            time.sleep(1.5)
            n0 = len(items)
            items, total = collect()
            if len(items) == n0:
                break
            self.pause()
        page.remove_listener("response", handler)
        if kind == "name" and not self.args.loose:
            items = [it for it in items if M.Puller.name_matches(q, it.get("name"))]
        self.log("[%s] %r (%s) -> %d items, total=%s, clicks=%d %s" % (group, label, kind, len(items), total, clicks, note))

        new, hits_n, this_ids, capped = 0, 0, [], 0
        for it in items:
            aid = "tt-" + str(it["id"])
            if aid in self.ads:
                prev = self.ads[aid]
                if [group, label] not in prev.get("found_via", []):
                    prev.setdefault("found_via", []).append([group, label])
                this_ids.append(aid)
                if prev.get("term_hits"):
                    hits_n += 1
                continue
            slug = C.slugify(it.get("name") or "unknown")
            cnt = self.per_adv.get(slug, 0)
            if cnt >= self.args.max_per_advertiser or self.tt_count() >= self.args.max_total:
                capped += 1
                continue
            detail = {}
            rec = None
            if not self.args.no_details:
                self.pause()
                try:
                    detail, rec = self.run_detail(page, it)
                except Exception as e:
                    self.log("detail failed %s: %s" % (it["id"], str(e)[:120]))
            if rec is None:
                rec = normalize(it, detail, self.terms)
            if kind == "name":
                rec["roster_advertiser"] = q
            rec["found_via"] = [[group, label]]
            rec["first_seen_utc"] = C.now_iso()
            self.ads[aid] = rec
            self.per_adv[rec["advertiser_slug"]] = self.per_adv.get(rec["advertiser_slug"], 0) + 1
            new += 1
            this_ids.append(aid)
            if rec.get("term_hits"):
                hits_n += 1
            self.download_media(ctx, rec)
            self.write_ad_json(rec)
            self.save()
        self.save()
        self.write_search_row({
            "timestamp": C.now_iso(), "group": group, "label": label, "search_type": kind, "query": q, "url": url,
            "ads_found": len(this_ids), "reported_result_count": total if total is not None else "",
            "new_unique_ads": new, "term_hits": hits_n,
            "notes": (note + (" capped %d" % capped if capped else "")
                      + (" details empty for %d ads (library slow or throttled, rerun later)" % self.empty_details
                         if self.empty_details else "")).strip(),
        })
        self.empty_details = 0
        self.log("[%s] %r -> %d ads, %d new, capped=%d, tiktok total=%d" % (group, label, len(this_ids), new, capped, self.tt_count()))
        return this_ids

    # ---- one detail page
    def run_detail(self, page, it):
        got = []
        handler = lambda r: got.append(r) if "/api/v1/items/" in r.url else None  # noqa: E731
        page.on("response", handler)
        page.goto(detail_url(it["id"]), wait_until="domcontentloaded", timeout=60000)
        self.wait_until(lambda: any("/details" in r.url for r in got), 90)
        time.sleep(3)
        detail = {}
        for j in self.bodies(got, "/details"):
            detail = parse_detail(j)
            if detail.get("ad"):
                break
        page.remove_listener("response", handler)
        if not detail.get("ad"):
            # not observed (or throttled): ask the page itself; the library answers 421 "system busy" when throttling
            try:
                st, txt = page.evaluate(FETCH_DETAIL_JS, str(it["id"]))
                if st == 200:
                    detail = parse_detail(json.loads(txt))
                else:
                    self.log("detail %s: http %s %s" % (it["id"], st, (txt or "")[:60]))
            except Exception as e:
                self.log("in-page detail fetch failed %s: %s" % (it["id"], str(e)[:80]))
        if not detail.get("ad"):
            self.empty_details += 1
        rec = normalize(it, detail, self.terms)
        if not self.args.no_cards:
            try:
                p = self.ad_dir(rec) / "card.png"
                p.parent.mkdir(parents=True, exist_ok=True)
                page.screenshot(path=str(p), full_page=False)
                rec.setdefault("files", {})["card"] = str(p.relative_to(self.out))
            except Exception as e:
                self.log("card screenshot failed %s: %s" % (it["id"], str(e)[:80]))
        return detail, rec

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
                    self.run_search(ctx, page, kind, q, group, label)
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
        self.log("done in %ds, tiktok ads in file %d" % (int(time.time() - t0), self.tt_count()))


# ----------------------------------------------------------------------------- cli

def build_plan(args):
    plan = []
    for n in args.advertisers or []:
        plan.append({"kind": "name", "q": n, "label": n, "group": "roster"})
    for k in args.keywords or []:
        plan.append({"kind": "keyword", "q": k, "label": "keyword " + k, "group": "keywords"})
    return plan


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--advertisers", nargs="*", help="advertiser names (query_type=1)")
    ap.add_argument("--keywords", nargs="*", help="keywords (query_type=2)")
    ap.add_argument("--out", required=True, help="output folder, usually <workspace>/ads")
    ap.add_argument("--region", default="all", help="library region filter, default all (EEA, CH and UK only)")
    ap.add_argument("--days", type=int, default=365, help="look-back window for first/last shown, default 365")
    ap.add_argument("--max-per-advertiser", type=int, default=40)
    ap.add_argument("--max-total", type=int, default=400)
    ap.add_argument("--max-per-search", type=int, default=60)
    ap.add_argument("--max-pages-per-search", type=int, default=5, help="how many times to press View more")
    ap.add_argument("--loose", action="store_true", help="keep results whose advertiser name does not match the query")
    ap.add_argument("--no-details", action="store_true", help="skip detail pages (no advertiser id, link, targeting or card)")
    ap.add_argument("--terms", nargs="*", help="brand or category terms to flag in term_hits")
    ap.add_argument("--no-media", action="store_true", help="do not download cover images")
    ap.add_argument("--no-cards", action="store_true", help="skip card screenshots")
    ap.add_argument("--pause-min", type=float, default=2.0)
    ap.add_argument("--pause-max", type=float, default=4.0)
    ap.add_argument("--headed", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    plan = build_plan(args)
    if not plan:
        ap.error("give --advertisers or --keywords")
    if args.dry_run:
        s, e = window_ms(args.days)
        print("dry run: %d plan items, out=%s" % (len(plan), Path(args.out)))
        for it in plan:
            print("  %-8s" % it["kind"], search_url(it["q"], it["kind"], args.region, s, e))
        print("  then each ad: " + detail_url("<id>"))
        return 0
    C.need_playwright()
    Puller(args).run(plan)
    return 0


if __name__ == "__main__":
    sys.exit(main())
