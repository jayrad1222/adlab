#!/usr/bin/env python3
"""apify_pull.py: optional paid pull through an Apify actor, normalized into Ad Lab's ads.jsonl.

  python -I apify_pull.py --actor curious_coder/facebook-ads-library-scraper --input input.json --out <workspace>/ads
  python -I apify_pull.py --actor ... --input input.json --out DIR --dry-run        (prints the price and the input, sends nothing)
  python -I apify_pull.py --price --actor ...                                        (reads the actor's listed price)

Needs an Apify token (run /adlab:setup --keys). The input JSON is the actor's own input schema; see the
actor's page on apify.com. The estimated price (from the actor listing) and the member's apify_budget_usd
in business/finance.md are printed before any run; --yes confirms. Output records are normalized with
source "meta-apify" and the same fields as meta_pull.py where the actor provides them.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import adlab_common as C  # noqa: E402

API = "https://api.apify.com/v2"


def get(url, token):
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + token} if token else {})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode())


def actor_price(actor, token):
    try:
        info = get("%s/acts/%s" % (API, actor.replace("/", "~")), token).get("data", {})
    except Exception as e:
        return None, "could not read the actor listing: %s" % str(e)[:100]
    infos = info.get("pricingInfos") or []
    if not infos:
        return None, "actor lists no price (usage-billed by compute)"
    last = infos[-1]
    return last, "%s: %s %s per %s" % (last.get("pricingModel"), last.get("pricePerUnitUsd", "?"), "USD", last.get("unitName", "unit"))


def first(d, *keys):
    for k in keys:
        if k in d and d[k] not in (None, ""):
            return d[k]
    return None


def normalize(item):
    snap = item.get("snapshot") or {}
    aid = str(first(item, "adArchiveID", "ad_archive_id", "adArchiveId", "id", "ad_id") or "")
    page = first(item, "pageName", "page_name") or snap.get("page_name") or "unknown"
    body = first(item, "bodyText", "body_text", "text") or (snap.get("body") or {}).get("text")
    start = first(item, "startDate", "start_date", "startDateFormatted")
    if isinstance(start, (int, float)):
        from datetime import datetime, timezone
        start = datetime.fromtimestamp(int(start), tz=timezone.utc).strftime("%Y-%m-%d")
    rec = {
        "source": "meta-apify", "ad_id": aid, "advertiser": page, "advertiser_id": str(first(item, "pageId", "page_id") or ""),
        "advertiser_slug": C.slugify(page), "platforms": first(item, "publisherPlatform", "publisher_platform") or [],
        "start_date": (str(start)[:10] if start else None), "end_date": None, "is_active": first(item, "isActive", "is_active"),
        "days_active": C.days_between(str(start)[:10]) if start else None,
        "variant_count": first(item, "collationCount", "collation_count"), "format": (first(item, "displayFormat", "display_format") or snap.get("display_format") or "unknown").lower(),
        "body_text": body, "title": first(item, "title") or snap.get("title"), "link_description": snap.get("link_description"),
        "caption": snap.get("caption"), "cta_text": first(item, "ctaText", "cta_text") or snap.get("cta_text"), "cta_type": snap.get("cta_type"),
        "link_url": first(item, "linkUrl", "link_url") or snap.get("link_url"), "image_url": first(item, "imageUrl", "image_url"),
        "video_preview_image_url": first(item, "videoPreviewImageUrl"), "video_hd_url": first(item, "videoHdUrl", "video_hd_url"),
        "video_sd_url": first(item, "videoSdUrl"), "cards": snap.get("cards") or [], "page_like_count": snap.get("page_like_count"),
        "page_categories": snap.get("page_categories"), "byline": snap.get("byline"), "term_hits": [], "eu": None,
        "library_url": "https://www.facebook.com/ads/library/?id=" + aid if aid else None, "raw_snapshot": item,
        "match": "apify", "found_via": [["apify", "actor"]], "first_seen_utc": C.now_iso(), "files": {},
    }
    return rec


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--actor", required=True)
    ap.add_argument("--input")
    ap.add_argument("--out")
    ap.add_argument("--workspace")
    ap.add_argument("--price", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--yes", action="store_true")
    ap.add_argument("--timeout", type=int, default=600)
    args = ap.parse_args(argv)
    token = C.load_config().get("apify_token")
    last, how = actor_price(args.actor, token)
    print("actor price:", how)
    ws = C.workspace(args.workspace)
    fp = ws / "business" / "finance.md"
    if fp.exists():
        fm, _ = C.read_frontmatter(fp)
        if fm.get("apify_budget_usd") is not None:
            print("budget from finance.md: $%s" % fm["apify_budget_usd"])
    if args.price:
        return 0
    if not args.input or not args.out:
        ap.error("--input and --out are required to run")
    inp = json.loads(Path(args.input).read_text(encoding="utf-8"))
    print("input:", json.dumps(inp)[:300])
    if not token:
        print("no Apify token configured (run /adlab:setup --keys); dry run only")
        return 0
    if args.dry_run:
        print("dry run: nothing sent")
        return 0
    if not args.yes:
        print("add --yes to confirm the run")
        return 3
    url = "%s/acts/%s/run-sync-get-dataset-items?token=%s&timeout=%d" % (API, args.actor.replace("/", "~"), urllib.parse.quote(token), args.timeout)
    req = urllib.request.Request(url, data=json.dumps(inp).encode(), headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=args.timeout + 30) as r:
        items = json.loads(r.read().decode())
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    existing = {r["ad_id"]: r for r in C.read_jsonl(out / "ads.jsonl")}
    new = 0
    for it in items:
        rec = normalize(it)
        if not rec["ad_id"] or rec["ad_id"] in existing:
            continue
        existing[rec["ad_id"]] = rec
        d = out / rec["advertiser_slug"] / rec["ad_id"]
        d.mkdir(parents=True, exist_ok=True)
        src = rec.get("image_url") or rec.get("video_preview_image_url")
        if src:
            p = C.http_download(src, d / "media" / "creative.jpg")
            if p:
                rec["files"]["creative"] = str(p.relative_to(out))
        (d / "ad.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
        new += 1
    C.write_jsonl(out / "ads.jsonl", existing.values())
    print("apify: %d items, %d new, total %d" % (len(items), new, len(existing)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
