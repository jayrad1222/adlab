#!/usr/bin/env python3
"""manual_pull.py: Lite mode input. Turn pasted ad library links or a folder of screenshots into ad records.

  python -I manual_pull.py --urls URL [URL ...] --out <workspace>/ads            (Meta Ad Library links: fetches each detail page)
  python -I manual_pull.py --file links.txt --out DIR                             (one URL per line; Meta, Google, LinkedIn, TikTok)
  python -I manual_pull.py --screenshots DIR --out <workspace>/ads [--advertiser "Name"]
  python -I manual_pull.py --urls ... --out DIR --dry-run

Meta links are fetched through meta_pull.py's detail-page path when Playwright is available; otherwise,
and for other libraries, a stub record is written with the link so Claude can read the page or the
screenshot itself. Screenshot stubs have source "manual-screenshot" and inspection_coverage
"still-reviewed" once Claude has read them.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import adlab_common as C  # noqa: E402

IMG = {".png", ".jpg", ".jpeg", ".webp"}


def meta_id(url):
    q = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
    if q.get("id"):
        return q["id"][0]
    m = re.search(r"[?&]id=(\d+)", url)
    return m.group(1) if m else None


def stub(ad_id, source, advertiser, url=None, card=None):
    return {"source": source, "ad_id": ad_id, "advertiser": advertiser or "unknown", "advertiser_id": "",
            "advertiser_slug": C.slugify(advertiser or "unknown"), "platforms": [], "start_date": None, "end_date": None,
            "is_active": None, "days_active": None, "variant_count": None, "format": "unknown", "body_text": None,
            "title": None, "link_description": None, "caption": None, "cta_text": None, "cta_type": None, "link_url": None,
            "image_url": None, "video_preview_image_url": None, "video_hd_url": None, "video_sd_url": None, "cards": [],
            "term_hits": [], "eu": None, "library_url": url, "raw_snapshot": {}, "match": "manual",
            "found_via": [["manual", source]], "first_seen_utc": C.now_iso(), "files": ({"card": card} if card else {}),
            "needs_reading": True}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--urls", nargs="*")
    ap.add_argument("--file")
    ap.add_argument("--screenshots")
    ap.add_argument("--advertiser")
    ap.add_argument("--out", required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    urls = list(args.urls or [])
    if args.file:
        urls += [l.strip() for l in Path(args.file).read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    existing = {r["ad_id"]: r for r in C.read_jsonl(out / "ads.jsonl")}
    meta_ids, stubs = [], []
    for u in urls:
        if "facebook.com/ads/library" in u and meta_id(u):
            meta_ids.append(meta_id(u))
        elif "adstransparency.google.com" in u:
            stubs.append(stub("g-" + C.slugify(u.rsplit("/", 1)[-1][:40]), "google-manual", args.advertiser, u))
        elif "linkedin.com/ad-library" in u:
            stubs.append(stub("li-" + C.slugify(u.rsplit("/", 1)[-1][:40]), "linkedin-manual", args.advertiser, u))
        elif "library.tiktok.com" in u:
            q = urllib.parse.parse_qs(urllib.parse.urlparse(u).query)
            stubs.append(stub("tt-" + (q.get("ad_id", ["x"])[0]), "tiktok-manual", args.advertiser, u))
        else:
            stubs.append(stub("link-" + C.slugify(u)[:40], "link-manual", args.advertiser, u))
    if args.screenshots:
        for p in sorted(Path(args.screenshots).iterdir()):
            if p.suffix.lower() in IMG:
                aid = "shot-" + C.slugify(p.stem)
                d = out / C.slugify(args.advertiser or "screenshots") / aid
                d.mkdir(parents=True, exist_ok=True)
                target = d / ("card" + p.suffix.lower())
                if not args.dry_run:
                    target.write_bytes(p.read_bytes())
                stubs.append(stub(aid, "manual-screenshot", args.advertiser, None, str(target.relative_to(out))))
    if args.dry_run:
        print("meta ids:", meta_ids)
        print("stubs:", [s["ad_id"] for s in stubs])
        return 0
    if meta_ids:
        try:
            import meta_pull
            C.need_playwright()
            meta_pull.main(["--ids"] + meta_ids + ["--out", str(out), "--max-total", str(10000), "--no-cards"])
            existing = {r["ad_id"]: r for r in C.read_jsonl(out / "ads.jsonl")}
        except SystemExit:
            for i in meta_ids:
                stubs.append(stub(i, "meta-manual", args.advertiser, "https://www.facebook.com/ads/library/?id=" + i))
    new = 0
    for s in stubs:
        if s["ad_id"] in existing:
            continue
        existing[s["ad_id"]] = s
        d = out / s["advertiser_slug"] / s["ad_id"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "ad.json").write_text(json.dumps(s, ensure_ascii=False, indent=1), encoding="utf-8")
        new += 1
    C.write_jsonl(out / "ads.jsonl", existing.values())
    print("manual: %d meta ids fetched or stubbed, %d stubs written, total %d" % (len(meta_ids), new, len(existing)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
