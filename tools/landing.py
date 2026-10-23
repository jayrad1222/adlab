#!/usr/bin/env python3
"""landing.py: capture a landing page for an ad or for the member's own site.

  python -I landing.py --url https://example.com/offer --out <dir>            (one page)
  python -I landing.py --all <workspace>/ads [--max 60]                       (every ad with a link_url and no landing/ yet)
  python -I landing.py --site https://member-site.com --out <workspace>/business/site   (home + likely pricing/about/reviews pages)

Writes <out>/landing/page.txt (visible text), fold.png (first screen, phone size), full.png (full page),
meta.json (title, h1, prices seen, buttons, forms, word count). Read-only; never submits a form.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import adlab_common as C  # noqa: E402

UA = ("Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 "
      "(KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1")
PRICE = re.compile(r"(?:\$|£|€)\s?\d[\d,]*(?:\.\d{2})?(?:\s?/\s?(?:mo|month|year|yr|day|week))?", re.I)
LIKELY = ["pricing", "price", "plans", "about", "reviews", "testimonials", "faq", "how-it-works", "shop", "products", "join"]


def capture(page, url: str, out: Path, settle: float = 4.0) -> dict:
    out = out / "landing"
    out.mkdir(parents=True, exist_ok=True)
    note = ""
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=45000)
    except Exception as e:
        note = "goto error: " + str(e)[:120]
    time.sleep(settle)
    try:
        page.screenshot(path=str(out / "fold.png"))
    except Exception:
        pass
    try:
        page.screenshot(path=str(out / "full.png"), full_page=True)
    except Exception:
        pass
    try:
        text = page.inner_text("body")
    except Exception:
        text = ""
    (out / "page.txt").write_text(text, encoding="utf-8")
    meta = {"url": url, "final_url": page.url, "title": "", "h1": [], "prices": [], "buttons": [], "forms": 0,
            "word_count": len(text.split()), "captured": C.now_iso(), "note": note}
    try:
        meta["title"] = page.title()
        meta["h1"] = [t.strip() for t in page.locator("h1").all_inner_texts()][:5]
        btns = page.locator("button, a[role=button], input[type=submit], a.btn, a[class*=button], a[class*=cta]").all_inner_texts()
        meta["buttons"] = sorted({b.strip() for b in btns if b.strip()})[:25]
        meta["forms"] = page.locator("form").count()
    except Exception:
        pass
    meta["prices"] = sorted(set(m.group(0).strip() for m in PRICE.finditer(text)))[:20]
    (out / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    return meta


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--url")
    ap.add_argument("--out")
    ap.add_argument("--all")
    ap.add_argument("--site")
    ap.add_argument("--max", type=int, default=60)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    jobs = []
    if args.url:
        jobs.append((args.url, Path(args.out or ".")))
    if args.all:
        n = 0
        for ad_json in sorted(Path(args.all).glob("*/*/ad.json")):
            d = ad_json.parent
            if (d / "landing" / "meta.json").exists():
                continue
            try:
                rec = json.loads(ad_json.read_text(encoding="utf-8"))
            except Exception:
                continue
            u = rec.get("link_url")
            if u and u.startswith("http"):
                jobs.append((u, d))
                n += 1
            if n >= args.max:
                break
    site_pages = []
    if args.site:
        base = args.site.rstrip("/")
        site_pages = [base] + [base + "/" + s for s in LIKELY]
    if args.dry_run:
        for u, o in jobs:
            print("landing", u, "->", o)
        for u in site_pages:
            print("site", u)
        return 0
    if not jobs and not site_pages:
        ap.error("give --url, --all or --site")
    C.need_playwright()
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        ctx = b.new_context(user_agent=UA, viewport={"width": 390, "height": 844}, device_scale_factor=2, locale="en-US")
        page = ctx.new_page()
        for u, o in jobs:
            m = capture(page, u, o)
            print("%s -> %s (%d words, prices %s)" % (u[:70], o, m["word_count"], m["prices"][:3]))
            time.sleep(2)
        if site_pages:
            out = Path(args.out or C.workspace() / "business" / "site")
            found = []
            for u in site_pages:
                slug = C.slugify(urllib.parse.urlparse(u).path or "home") or "home"
                try:
                    r = page.goto(u, wait_until="domcontentloaded", timeout=30000)
                    if r and r.status >= 400:
                        continue
                except Exception:
                    continue
                m = capture(page, u, out / slug, settle=2.5)
                found.append({"url": u, "dir": str(out / slug), "title": m["title"], "words": m["word_count"]})
                print("site page", u, m["word_count"], "words")
            (out / "pages.json").write_text(json.dumps(found, indent=1), encoding="utf-8")
        b.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
