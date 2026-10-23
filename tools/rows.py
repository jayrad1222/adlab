#!/usr/bin/env python3
"""rows.py: batch ads for the analysts and merge their rubric rows into analysis/ads.csv safely.

  python -I rows.py --workspace DIR batches [--batch 15] [--only <advertiser-slug>] [--pending]
      prints one block per batch: batch number, then one line per ad: ad_id | advertiser | folder | coverage hints
      (--pending lists only ads with no row in analysis/ads.csv yet)
  python -I rows.py --workspace DIR merge --in batch.csv
      validates each row against the rubric header (36 columns, allowed values for the enum columns),
      appends new rows, replaces rows for ad ids already present, writes analysis/ads.csv, prints a report
  python -I rows.py --workspace DIR header
      prints the rubric CSV header
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import adlab_common as C  # noqa: E402

HEADER = ("ad_id,advertiser,page_or_account,platforms,first_seen,days_active_at_capture,status,variant_count,variant_type,format,"
          "duration_s,hook_text,hook_type,angle_family,awareness_stage,sophistication_move,persona_inferred,persona_evidence,"
          "emotional_lever,biases_used,proof_type,offer_elements,price_framing,cta,landing_type,landing_continuity,production_style,"
          "visual_hook,on_screen_text_density,distinctive_assets,sutherland_lens,works,weak,verdict,adaptation_idea,inspection_coverage").split(",")

ENUMS = {
    "variant_type": {"copy-test", "creative-test", "placement", "none", "unknown"},
    "awareness_stage": {"unaware", "problem", "solution", "product", "most", "unknown"},
    "sophistication_move": {"claim", "bigger-claim", "mechanism", "better-mechanism", "identification", "unknown"},
    "angle_family": {"problem", "desire", "mechanism", "identity", "proof", "offer", "contrarian", "news", "comparison", "story", "education", "cost-of-inaction", "unknown"},
    "proof_type": {"demo", "testimonial", "data", "authority", "social-proof", "press", "ugc", "none", "unknown"},
    "landing_continuity": {"strong", "weak", "broken", "unknown"},
    "production_style": {"polished", "native", "ugly", "ugc", "founder", "screen-rec", "unknown"},
    "on_screen_text_density": {"none", "low", "medium", "high", "unknown"},
    "verdict": {"adapt", "avoid", "monitor"},
    "inspection_coverage": {"copy-only", "still-reviewed", "video-watched"},
    "hook_type": {"callout", "question", "bold-claim", "specific-number", "curiosity-gap", "pattern-interrupt", "contrarian", "warning",
                  "confession", "story", "pov", "three-reasons", "today-years-old", "nobody-talks-about", "comparison", "news",
                  "social-proof", "authority", "demonstration", "problem-naming", "identification", "offer-led", "wish-i-knew",
                  "real-reason", "unpopular-opinion", "day-1-vs-30", "unknown"},
}


SYNONYMS = {
    "hook_type": {"story-opener": "story", "news-or-new": "news", "new": "news", "bold claim": "bold-claim", "specific number": "specific-number", "question-hook": "question",
                  "call-out": "callout", "number": "specific-number", "pov-hook": "pov", "demo": "demonstration", "proof": "social-proof",
                  "offer": "offer-led", "problem": "problem-naming", "warning-hook": "warning", "contrarian-hook": "contrarian", "contrarian-or-myth": "contrarian", "myth": "contrarian"},
    "angle_family": {"cost-of-inaction-led": "cost-of-inaction", "insight": "education", "educational": "education", "origin": "story",
                     "education-or-insight": "education", "story-or-origin": "story", "news-or-trend": "news", "desire-led": "desire"},
    "proof_type": {"social proof": "social-proof", "testimonials": "testimonial", "demonstration": "demo", "none-detected": "none"},
    "production_style": {"screen-recording": "screen-rec", "screen recording": "screen-rec", "founder-to-camera": "founder"},
    "verdict": {"adopt": "adapt", "watch": "monitor"},
    "inspection_coverage": {"copy only": "copy-only", "still": "still-reviewed", "video": "video-watched", "image-reviewed": "still-reviewed"},
}


def normalize(col: str, val: str) -> str:
    v = (val or "").strip().lower().replace(" ", "-")
    if col == "angle_family" and v.endswith("-led"):
        v = v[:-4]
    v = SYNONYMS.get(col, {}).get(v, v)
    return v


def load_ads(ws: Path):
    return C.read_jsonl(ws / "ads" / "ads.jsonl")


def cmd_batches(ws, args):
    ads = load_ads(ws)
    have = set()
    p = ws / "analysis" / "ads.csv"
    if p.exists():
        with p.open(encoding="utf-8") as f:
            have = {r["ad_id"] for r in csv.DictReader(f)}
    rows = []
    skipped = []
    for a in ads:
        if args.only and a.get("advertiser_slug") != args.only:
            continue
        if args.pending and a["ad_id"] in have:
            continue
        if args.skip_noise and a.get("match") == "keyword-neighbor" and not a.get("term_hits"):
            skipped.append((a["ad_id"], a.get("advertiser")))
            continue
        d = ws / "ads" / a["advertiser_slug"] / a["ad_id"]
        hints = []
        if (d / "ad.md").exists():
            hints.append("ad.md")
        if (d / "card.png").exists() or (d / "media" / "creative.jpg").exists():
            hints.append("image")
        if (d / "frames" / "contact.jpg").exists():
            hints.append("frames")
        if (d / "transcript.md").exists() and "No transcription backend" not in (d / "transcript.md").read_text(encoding="utf-8")[:200]:
            hints.append("transcript")
        rows.append((a["ad_id"], a.get("advertiser"), a.get("match", ""), str(d), ",".join(hints) or "copy-only"))
    rows.sort(key=lambda r: (r[1] or "", r[0]))
    n = max(1, args.batch)
    for i in range(0, len(rows), n):
        print("## batch %d (%d ads)" % (i // n + 1, min(n, len(rows) - i)))
        for r in rows[i:i + n]:
            print("%s | %s | %s | %s | %s" % r)
        print()
    print("total ads to analyze: %d" % len(rows))
    if skipped:
        print("skipped as noise (keyword neighbors with no term hit): %d" % len(skipped))
        for aid, adv in skipped:
            print("  %s | %s" % (aid, adv))
    return 0


def cmd_merge(ws, args):
    text = Path(args.inp).read_text(encoding="utf-8")
    lines = [l for l in text.splitlines() if l.strip() and not l.startswith("#")]
    buf = io.StringIO("\n".join(lines))
    rd = csv.reader(buf)
    first = next(rd, None)
    if first is None:
        C.die("empty input")
    new = []
    bad = []
    rows_iter = [first] + list(rd) if first != HEADER else list(rd)
    for i, row in enumerate(rows_iter, 1):
        if len(row) != len(HEADER):
            bad.append((i, "has %d columns, need %d" % (len(row), len(HEADER))))
            continue
        rec = dict(zip(HEADER, row))
        for k in ENUMS:
            if rec.get(k, "").strip():
                rec[k] = normalize(k, rec[k])
        probs = [k for k, allowed in ENUMS.items() if rec.get(k, "").strip() and rec[k].strip() not in allowed]
        if probs:
            bad.append((i, "bad values in " + ", ".join("%s=%r" % (k, rec[k]) for k in probs)))
            continue
        if not rec["ad_id"].strip():
            bad.append((i, "empty ad_id"))
            continue
        new.append(rec)
    p = ws / "analysis" / "ads.csv"
    existing = {}
    if p.exists():
        with p.open(encoding="utf-8") as f:
            for r in csv.DictReader(f):
                existing[r["ad_id"]] = r
    replaced = sum(1 for r in new if r["ad_id"] in existing)
    for r in new:
        existing[r["ad_id"]] = r
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HEADER)
        w.writeheader()
        for r in existing.values():
            w.writerow(r)
    print("merged %d rows (%d replaced), rejected %d; ads.csv now has %d rows" % (len(new), replaced, len(bad), len(existing)))
    for i, why in bad:
        print("  rejected line %d: %s" % (i, why))
    return 0 if not bad else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--workspace")
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("batches")
    b.add_argument("--batch", type=int, default=15)
    b.add_argument("--only")
    b.add_argument("--pending", action="store_true")
    b.add_argument("--skip-noise", action="store_true", help="leave out keyword-neighbor ads with no --terms hit (listed separately as skipped)")
    m = sub.add_parser("merge")
    m.add_argument("--in", dest="inp", required=True)
    sub.add_parser("header")
    args = ap.parse_args(argv)
    ws = C.workspace(args.workspace)
    if args.cmd == "header":
        print(",".join(HEADER))
        return 0
    if args.cmd == "batches":
        return cmd_batches(ws, args)
    return cmd_merge(ws, args)


if __name__ == "__main__":
    sys.exit(main())
