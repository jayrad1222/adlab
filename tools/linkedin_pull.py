#!/usr/bin/env python3
"""linkedin_pull.py: read-only LinkedIn Ad Library pull (headless Playwright, no login).

Same manners as meta_pull.py: headless Chromium, desktop user agent, no login, one page at a
time, 2 to 4 second pauses, nothing is clicked that posts, likes or follows.

What the site exposes (checked live October 2026, no login)
  https://www.linkedin.com/ad-library/search?accountOwner=<company>  (also keyword=, payer=,
  countries=XX) returns server-rendered HTML: a "N ads match your search criteria" count and
  one <li class="search-result-item"> card per ad with the creative type, advertiser, body
  text (truncated), headline, image or video poster and the detail link. Further pages are
  HTML fragments at /ad-library/searchPaginationFragment?...&paginationToken=<token>, the token
  coming from a hidden <code id="paginationMetadata"> block. The detail page
  /ad-library/detail/<id> shows the full body, headline, CTA, the video sources and poster, the
  ad type ("Video Ad", "Single Image Ad", ...), the advertiser's company page and "Paid for by".
  Run dates and impressions appear only for ads that ran in the EU; where the page shows none
  the record keeps start_date, end_date and days_active null. The destination URL is not
  exposed on the public page unless the card links out, so link_url is usually null.
  If a login wall appears the run writes a note to searches.csv and stops cleanly.

Usage
  python -I linkedin_pull.py --advertisers "Notion" "Asana" --out <workspace>/ads
  python -I linkedin_pull.py --keywords "project management" --out <workspace>/ads
  python -I linkedin_pull.py --advertisers "Notion" --out DIR --dry-run   (prints the URLs it would visit)

Outputs in --out: ads.jsonl (all ads, deduped on ad_id, records from other sources kept),
searches.csv, run.log, and <advertiser_slug>/<ad_id>/{ad.json, card.png, media/...}
"""
from __future__ import annotations

import argparse
import csv
import html as htmlmod
import json
import random
import re
import sys
import time
import urllib.parse
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import adlab_common as C  # noqa: E402
import meta_pull as M  # noqa: E402

UA = M.UA
BASE = "https://www.linkedin.com/ad-library"
SEARCH_COLS = ["timestamp", "group", "label", "search_type", "query", "url", "ads_found", "reported_result_count",
               "new_unique_ads", "term_hits", "notes"]
TYPE_TO_FORMAT = {
    "SPONSORED_VIDEO": "video",
    "SPONSORED_STATUS_UPDATE": "image",
    "SPONSORED_UPDATE_CAROUSEL": "carousel",
    "SPONSORED_UPDATE_NATIVE_DOCUMENT": "unknown",
    "TEXT_AD": "text",
    "SPONSORED_INMAIL": "text",
    "SPONSORED_MESSAGE": "text",
}
LABEL_TO_FORMAT = {"video ad": "video", "single image ad": "image", "carousel ad": "carousel", "text ad": "text",
                   "document ad": "unknown", "event ad": "unknown", "message ad": "text", "conversation ad": "text"}


# ----------------------------------------------------------------------------- url builders

def search_query(kind, q, country=None):
    key = {"name": "accountOwner", "keyword": "keyword", "payer": "payer"}[kind]
    qs = key + "=" + urllib.parse.quote(q)
    if country:
        qs += "&countries=" + urllib.parse.quote(country)
    return qs


def search_url(kind, q, country=None):
    return BASE + "/search?" + search_query(kind, q, country)


def fragment_url(kind, q, token, country=None):
    return BASE + "/searchPaginationFragment?" + search_query(kind, q, country) + "&paginationToken=" + urllib.parse.quote(token)


def detail_url(ad_id):
    return BASE + "/detail/" + str(ad_id)


# ----------------------------------------------------------------------------- parsing helpers

def clean(s):
    if s is None:
        return None
    s = htmlmod.unescape(re.sub(r"<[^>]+>", " ", s))
    s = re.sub(r"[ \t\r\f\v]+", " ", s)
    s = re.sub(r"\s*\n\s*", "\n", s).strip()
    return s or None


def attr(tag, name):
    m = re.search(r'\s' + re.escape(name) + r'="([^"]*)"', tag)
    return htmlmod.unescape(m.group(1)) if m else None


def img_src(tag):
    return attr(tag, "src") or attr(tag, "data-delayed-url")


def is_login_wall(url, html):
    u = (url or "").lower()
    if any(k in u for k in ("/login", "/authwall", "/checkpoint", "/uas/", "signup")):
        return True
    h = html or ""
    return ("authwall" in h and "search-result-item" not in h) or ("Join LinkedIn" in h and "ad-preview" not in h)


def parse_pagination(html):
    m = re.search(r'id="paginationMetadata"><!--(\{.*?\})-->', html or "", re.S)
    if not m:
        return {}
    try:
        return json.loads(htmlmod.unescape(m.group(1)))
    except Exception:
        return {}


def parse_result_count(html):
    m = re.search(r"([\d,]+)\s+ads?\s+match", html or "")
    return int(m.group(1).replace(",", "")) if m else None


def parse_search_cards(html):
    """Search page or pagination fragment HTML -> list of card dicts."""
    out = []
    for li in re.findall(r'<li class="search-result-item.*?</li>', html or "", re.S):
        m = re.search(r"/ad-library/detail/(\d+)", li)
        if not m:
            continue
        card = {"ad_id": m.group(1), "creative_type": None, "advertiser": None, "ad_type_label": None,
                "body_text": None, "headline": None, "image_url": None, "logo_url": None, "detail_url": detail_url(m.group(1))}
        t = re.search(r'data-creative-type="([^"]+)"', li)
        if t:
            card["creative_type"] = t.group(1)
        a = re.search(r'class="base-ad-preview-card[^"]*"\s+aria-label="([^"]*)"', li)
        if a:
            parts = [p.strip() for p in htmlmod.unescape(a.group(1)).split(",")]
            if len(parts) >= 3 and parts[-1].lower() == "view details":
                card["ad_type_label"] = parts[-2]
                card["advertiser"] = ", ".join(parts[:-2])
        if not card["advertiser"]:
            n = re.search(r'<div class="block text-md text-color-text font-bold[^"]*">(.*?)</div>', li, re.S)
            card["advertiser"] = clean(n.group(1)) if n else None
        b = re.search(r'<p class="commentary__content[^"]*">(.*?)</p>', li, re.S)
        if b:
            card["body_text"] = clean(b.group(1))
        h = re.search(r'sponsored-content-headline.*?<h2[^>]*>(.*?)</h2>', li, re.S)
        if h:
            card["headline"] = clean(h.group(1))
        for tag in re.findall(r"<img[^>]*>", li):
            if "ad-preview__dynamic-dimensions-image" in tag and not card["image_url"]:
                card["image_url"] = img_src(tag)
            elif "hue-web-entity__image" in tag and not card["logo_url"]:
                card["logo_url"] = img_src(tag)
        out.append(card)
    return out


def parse_detail(html):
    """Ad detail page HTML -> dict of what the public page shows."""
    d = {"creative_type": None, "advertiser": None, "company_id": None, "company_url": None, "body_text": None,
         "headline": None, "cta_text": None, "image_url": None, "poster_url": None, "video_sources": [],
         "ad_type_label": None, "paid_for_by": None, "about_text": None, "start_date": None, "end_date": None,
         "impressions_text": None, "link_url": None}
    if not html:
        return d
    t = re.search(r'data-creative-type="([^"]+)"', html)
    if t:
        d["creative_type"] = t.group(1)
    m = re.search(r'href="https://www\.linkedin\.com/company/(\d+)[^"]*"[^>]*aria-label="View organization page for ([^"]*)"', html)
    if m:
        d["company_id"], d["advertiser"] = m.group(1), htmlmod.unescape(m.group(2)).strip()
        d["company_url"] = "https://www.linkedin.com/company/" + m.group(1)
    if not d["advertiser"]:
        m = re.search(r'aria-label="View organization page for ([^"]*)"', html)
        if m:
            d["advertiser"] = htmlmod.unescape(m.group(1)).strip()
    b = re.search(r'<p class="commentary__content[^"]*">(.*?)</p>', html, re.S)
    if b:
        d["body_text"] = clean(b.group(1))
    h = re.search(r'sponsored-content-headline.*?<h2[^>]*>(.*?)</h2>', html, re.S)
    if h:
        d["headline"] = clean(h.group(1))
    c = re.search(r'data-tracking-control-name="ad_library_ad_detail_cta"[^>]*>(.*?)</button>', html, re.S)
    if c:
        d["cta_text"] = clean(c.group(1))
    v = re.search(r'data-poster-url="([^"]*)"', html)
    if v:
        d["poster_url"] = htmlmod.unescape(v.group(1))
    s = re.search(r'data-sources="([^"]*)"', html)
    if s:
        try:
            srcs = json.loads(htmlmod.unescape(s.group(1)))
            d["video_sources"] = [{"src": x.get("src"), "type": x.get("type"), "bitrate": x.get("bitrate")} for x in srcs if x.get("src")]
        except Exception:
            pass
    for tag in re.findall(r"<img[^>]*>", html):
        if "ad-preview__dynamic-dimensions-image" in tag:
            d["image_url"] = img_src(tag)
            break
    about = re.search(r"About the ad(.*?)</section>", html, re.S)
    if about:
        txt = clean(about.group(1)) or ""
        d["about_text"] = txt
        lines = [ln.strip() for ln in txt.split("\n") if ln.strip()]
        if lines:
            d["ad_type_label"] = lines[0]
        p = re.search(r"Paid for by\s*(.+)", txt)
        if p:
            d["paid_for_by"] = p.group(1).strip()
        dates = re.findall(r"([A-Z][a-z]{2,8} \d{1,2}, \d{4})", txt)
        iso = []
        for x in dates:
            for fmt in ("%b %d, %Y", "%B %d, %Y"):
                try:
                    iso.append(datetime.strptime(x, fmt).strftime("%Y-%m-%d"))
                    break
                except Exception:
                    pass
        if iso:
            d["start_date"] = iso[0]
            d["end_date"] = iso[1] if len(iso) > 1 else None
        imp = re.search(r"(Impressions[^\n]*(?:\n[^\n]*)?)", txt)
        if imp:
            d["impressions_text"] = imp.group(1).strip()
    for href in re.findall(r'href="(https?://[^"]+)"', html):
        href = htmlmod.unescape(href)
        host = urllib.parse.urlparse(href).netloc.lower()
        if not any(k in host for k in ("linkedin.com", "licdn.com", "lnkd.in")) and "trk=ad_library" not in href:
            d["link_url"] = href
            break
    return d


def blank_record():
    keys = ["source", "ad_id", "advertiser", "advertiser_id", "advertiser_slug", "platforms", "start_date", "end_date",
            "is_active", "days_active", "variant_count", "collation_id", "format", "body_text", "title",
            "link_description", "caption", "cta_text", "cta_type", "link_url", "image_url", "video_preview_image_url",
            "video_hd_url", "video_sd_url", "cards", "page_like_count", "page_profile_uri", "page_categories", "byline",
            "term_hits", "eu", "library_url", "raw_snapshot", "link_domain", "link_path", "dest_type"]
    return {k: None for k in keys}


def map_format(creative_type, label):
    if creative_type and creative_type in TYPE_TO_FORMAT:
        return TYPE_TO_FORMAT[creative_type]
    if label and label.lower() in LABEL_TO_FORMAT:
        return LABEL_TO_FORMAT[label.lower()]
    ct = (creative_type or "").upper()
    for k, v in (("VIDEO", "video"), ("CAROUSEL", "carousel"), ("IMAGE", "image"), ("TEXT", "text")):
        if k in ct:
            return v
    return "unknown"


def normalize(card, detail, terms):
    """Search card + detail page dict -> Ad Lab record."""
    detail = detail or {}
    name = detail.get("advertiser") or card.get("advertiser") or "unknown"
    label = detail.get("ad_type_label") or card.get("ad_type_label")
    fmt = map_format(detail.get("creative_type") or card.get("creative_type"), label)
    body = detail.get("body_text") or card.get("body_text")
    title = detail.get("headline") or card.get("headline")
    srcs = sorted(detail.get("video_sources") or [], key=lambda x: x.get("bitrate") or 0)
    hd = srcs[-1]["src"] if srcs else None
    sd = srcs[0]["src"] if len(srcs) > 1 else None
    poster = detail.get("poster_url") or (card.get("image_url") if fmt == "video" else None)
    image = None if fmt == "video" else (detail.get("image_url") or card.get("image_url"))
    link = detail.get("link_url")
    start, end = detail.get("start_date"), detail.get("end_date")
    blob = " ".join(str(x) for x in [name, body, title, detail.get("cta_text"), detail.get("paid_for_by")] if x).lower()
    hits = [t for t in (terms or []) if t and t.lower() in blob]
    rec = blank_record()
    rec.update({
        "source": "linkedin",
        "ad_id": "li-" + str(card["ad_id"]),
        "advertiser": name,
        "advertiser_id": str(detail.get("company_id") or ""),
        "advertiser_slug": C.slugify(name),
        "platforms": ["linkedin"],
        "start_date": start,
        "end_date": end,
        "is_active": None,
        "days_active": C.days_between(start, end) if start else None,
        "variant_count": None,
        "format": fmt,
        "body_text": body,
        "title": title,
        "cta_text": detail.get("cta_text"),
        "link_url": link,
        "image_url": image,
        "video_preview_image_url": poster,
        "video_hd_url": hd,
        "video_sd_url": sd,
        "cards": [],
        "page_profile_uri": detail.get("company_url"),
        "byline": detail.get("paid_for_by"),
        "term_hits": hits,
        "library_url": detail_url(card["ad_id"]),
        "raw_snapshot": {"card": card, "detail": detail},
        "creative_type": detail.get("creative_type") or card.get("creative_type"),
        "ad_type_label": label,
        "impressions_text": detail.get("impressions_text"),
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
            if r.get("source") == "linkedin":
                self.per_adv[r.get("advertiser_slug")] = self.per_adv.get(r.get("advertiser_slug"), 0) + 1
        self.terms = args.terms or []
        self.walled = False

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

    def li_count(self):
        return sum(1 for r in self.ads.values() if r.get("source") == "linkedin")

    def download(self, ctx, url, base, max_bytes=None):
        for ext in (".jpg", ".png", ".webp", ".gif", ".mp4"):
            if base.with_suffix(ext).exists():
                return base.with_suffix(ext)
        base.parent.mkdir(parents=True, exist_ok=True)
        try:
            r = ctx.request.get(url, timeout=60000)
            if not r.ok:
                return None
            body = r.body()
            if max_bytes and len(body) > max_bytes:
                return None
            ct = r.headers.get("content-type", "")
            ext = ".mp4" if "mp4" in ct or "video" in ct else ".png" if "png" in ct else ".webp" if "webp" in ct \
                else ".gif" if "gif" in ct else ".jpg"
            p = base.with_suffix(ext)
            p.write_bytes(body)
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
        vid = rec.get("video_hd_url") or rec.get("video_sd_url")
        if vid and not self.args.no_videos and not files.get("video"):
            p = self.download(ctx, vid, d / "video", max_bytes=self.args.video_max_mb * 1024 * 1024)
            if p:
                files["video"] = str(p.relative_to(self.out))
            else:
                self.log("video skipped or failed for " + rec["ad_id"])

    # ---- one search (page 1 by browser, further pages by GET fragments)
    def run_search(self, ctx, page, kind, q, group, label):
        url = search_url(kind, q, self.args.country)
        note = ""
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
        except Exception as e:
            note = "goto error: " + str(e)[:120]
        time.sleep(4)
        html = page.content()
        if is_login_wall(page.url, html):
            self.walled = True
            self.write_search_row({"timestamp": C.now_iso(), "group": group, "label": label, "search_type": kind, "query": q,
                                   "url": url, "ads_found": 0, "reported_result_count": "", "new_unique_ads": 0,
                                   "term_hits": 0, "notes": "login wall at " + page.url[:100]})
            self.log("LinkedIn showed a login wall at %s; stopping without retrying." % page.url[:100])
            return []
        reported = parse_result_count(html)
        cards = parse_search_cards(html)
        meta = parse_pagination(html)
        pages = 1
        while (len(cards) < self.args.max_per_search and meta.get("paginationToken") and not meta.get("isLastPage")
               and pages < self.args.max_pages_per_search):
            self.pause()
            furl = fragment_url(kind, q, meta["paginationToken"], self.args.country)
            try:
                r = ctx.request.get(furl, timeout=60000)
                if not r.ok:
                    note += " fragment http %d" % r.status
                    break
                frag = r.text()
            except Exception as e:
                note += " fragment error " + str(e)[:60]
                break
            more = parse_search_cards(frag)
            meta = parse_pagination(frag)
            pages += 1
            if not more:
                break
            cards += more
        seen, uniq = set(), []
        for c in cards:
            if c["ad_id"] not in seen:
                seen.add(c["ad_id"])
                uniq.append(c)
        if kind == "name" and not self.args.loose:
            uniq = [c for c in uniq if M.Puller.name_matches(q, c.get("advertiser"))]
        self.log("[%s] %r (%s) -> %d cards on %d pages, reported=%s %s" % (group, label, kind, len(uniq), pages, reported, note))

        new, hits_n, this_ids, capped = 0, 0, [], 0
        for c in uniq:
            aid = "li-" + c["ad_id"]
            if aid in self.ads:
                prev = self.ads[aid]
                if [group, label] not in prev.get("found_via", []):
                    prev.setdefault("found_via", []).append([group, label])
                this_ids.append(aid)
                if prev.get("term_hits"):
                    hits_n += 1
                continue
            slug = C.slugify(c.get("advertiser") or "unknown")
            cnt = self.per_adv.get(slug, 0)
            if cnt >= self.args.max_per_advertiser or self.li_count() >= self.args.max_total:
                capped += 1
                continue
            self.pause()
            try:
                rec = self.run_detail(ctx, page, c)
            except Exception as e:
                self.log("detail failed %s: %s" % (c["ad_id"], str(e)[:120]))
                continue
            if rec is None:
                break
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
            "ads_found": len(this_ids), "reported_result_count": reported if reported is not None else "",
            "new_unique_ads": new, "term_hits": hits_n,
            "notes": (note + (" capped %d" % capped if capped else "") + (" login wall" if self.walled else "")).strip(),
        })
        self.log("[%s] %r -> %d ads, %d new, capped=%d, linkedin total=%d" % (group, label, len(this_ids), new, capped, self.li_count()))
        return this_ids

    # ---- one detail page
    def run_detail(self, ctx, page, card):
        page.goto(card["detail_url"], wait_until="domcontentloaded", timeout=60000)
        time.sleep(3)
        html = page.content()
        if is_login_wall(page.url, html):
            self.walled = True
            self.log("LinkedIn showed a login wall at %s; stopping without retrying." % page.url[:100])
            return None
        detail = parse_detail(html)
        rec = normalize(card, detail, self.terms)
        if not self.args.no_cards:
            p = self.ad_dir(rec) / "card.png"
            p.parent.mkdir(parents=True, exist_ok=True)
            for sel in (".ad-preview-container", ".ad-detail-left-rail", "main"):
                try:
                    page.locator(sel).first.screenshot(path=str(p), timeout=10000)
                    rec.setdefault("files", {})["card"] = str(p.relative_to(self.out))
                    break
                except Exception:
                    continue
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
                if self.walled:
                    break
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
        self.log("done in %ds, linkedin ads in file %d%s" % (int(time.time() - t0), self.li_count(),
                                                             " (stopped at a login wall)" if self.walled else ""))


# ----------------------------------------------------------------------------- cli

def build_plan(args):
    plan = []
    for n in args.advertisers or []:
        plan.append({"kind": "name", "q": n, "label": n, "group": "roster"})
    for k in args.keywords or []:
        plan.append({"kind": "keyword", "q": k, "label": "keyword " + k, "group": "keywords"})
    for p in args.payers or []:
        plan.append({"kind": "payer", "q": p, "label": "payer " + p, "group": "roster"})
    return plan


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--advertisers", nargs="*", help="company or advertiser names (accountOwner search)")
    ap.add_argument("--keywords", nargs="*", help="words or phrases (keyword search)")
    ap.add_argument("--payers", nargs="*", help="payer names (payer search)")
    ap.add_argument("--out", required=True, help="output folder, usually <workspace>/ads")
    ap.add_argument("--country", help="two-letter country code filter, default all")
    ap.add_argument("--max-per-advertiser", type=int, default=40)
    ap.add_argument("--max-total", type=int, default=400)
    ap.add_argument("--max-per-search", type=int, default=60)
    ap.add_argument("--max-pages-per-search", type=int, default=5)
    ap.add_argument("--loose", action="store_true", help="keep cards whose advertiser name does not match the query")
    ap.add_argument("--terms", nargs="*", help="brand or category terms to flag in term_hits")
    ap.add_argument("--no-media", action="store_true", help="do not download images, posters or videos")
    ap.add_argument("--no-videos", action="store_true", help="download images and posters only")
    ap.add_argument("--video-max-mb", type=int, default=60)
    ap.add_argument("--no-cards", action="store_true", help="skip card screenshots")
    ap.add_argument("--pause-min", type=float, default=2.0)
    ap.add_argument("--pause-max", type=float, default=4.0)
    ap.add_argument("--headed", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    plan = build_plan(args)
    if not plan:
        ap.error("give --advertisers, --keywords or --payers")
    if args.dry_run:
        print("dry run: %d plan items, out=%s" % (len(plan), Path(args.out)))
        for it in plan:
            print("  %-8s" % it["kind"], search_url(it["kind"], it["q"], args.country))
        print("  then pages via " + fragment_url("name", "<q>", "<token>", args.country))
        print("  then each ad: " + detail_url("<id>"))
        return 0
    C.need_playwright()
    Puller(args).run(plan)
    return 0


if __name__ == "__main__":
    sys.exit(main())
