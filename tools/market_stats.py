#!/usr/bin/env python3
"""market_stats.py: aggregate analysis/ads.csv for the market map, counting advertisers as well as ads.

  python -I market_stats.py --workspace DIR [--roster-only] [--md analysis/stats.md]

Prints, and optionally writes, tables for: ads and videos per advertiser; hook types, angle families,
awareness stages, sophistication moves, proof types, formats, production styles, emotional levers,
offer elements and price framing (each with ad count and advertiser count); the persona_inferred
strings grouped by advertiser; the longevity leaderboard (days active, with the caveats printed);
verdict and inspection-coverage counts. Counting advertisers keeps one prolific advertiser from
looking like "the market".
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import adlab_common as C  # noqa: E402

COLS = ["hook_type", "angle_family", "awareness_stage", "sophistication_move", "proof_type", "format", "production_style",
        "emotional_lever", "offer_elements", "price_framing", "landing_type", "landing_continuity", "on_screen_text_density", "variant_type"]


def split(v):
    return [x.strip() for x in (v or "").replace("|", ",").replace(";", ",").split(",") if x.strip()]


def table(title, counter_ads, counter_adv, total_adv):
    lines = ["### " + title, "", "| Value | Ads | Advertisers (of %d) |" % total_adv, "|---|---:|---:|"]
    for k, n in counter_ads.most_common():
        lines.append("| %s | %d | %d |" % (k, n, counter_adv[k]))
    return lines + [""]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--workspace")
    ap.add_argument("--roster-only", action="store_true", help="only ads whose ads.jsonl match is advertiser-page or cobrand")
    ap.add_argument("--md")
    args = ap.parse_args(argv)
    ws = C.workspace(args.workspace)
    rows = list(csv.DictReader((ws / "analysis" / "ads.csv").open(encoding="utf-8")))
    meta = {r["ad_id"]: r for r in C.read_jsonl(ws / "ads" / "ads.jsonl")}
    if args.roster_only:
        rows = [r for r in rows if meta.get(r["ad_id"], {}).get("match") in ("advertiser-page", "cobrand")]
    advs = Counter(r["advertiser"] for r in rows)
    total_adv = len(advs)
    out = ["# Market stats", "", "Computed %s from %d rubric rows across %d advertisers%s." % (C.today(), len(rows), total_adv, " (roster ads only)" if args.roster_only else ""), "",
           "Counts are of the ads that loaded, not of everything an advertiser runs. Advertiser counts show how many distinct advertisers do a thing; that is the number to quote for 'the market does X'.", "",
           "## Ads per advertiser", "", "| Advertiser | Ads | Video ads | Still-reviewed | Match |", "|---|---:|---:|---:|---|"]
    for a, n in advs.most_common():
        rs = [r for r in rows if r["advertiser"] == a]
        vids = sum(1 for r in rs if r["format"].startswith("video"))
        still = sum(1 for r in rs if r["inspection_coverage"] == "still-reviewed")
        match = Counter(meta.get(r["ad_id"], {}).get("match", "?") for r in rs).most_common(1)[0][0]
        out.append("| %s | %d | %d | %d | %s |" % (a, n, vids, still, match))
    out.append("")
    out.append("## Distributions")
    out.append("")
    for col in COLS:
        c_ads, c_adv = Counter(), Counter()
        seen = defaultdict(set)
        for r in rows:
            for v in split(r.get(col)):
                c_ads[v] += 1
                seen[v].add(r["advertiser"])
        for v, s in seen.items():
            c_adv[v] = len(s)
        out += table(col, c_ads, c_adv, total_adv)
    out += ["## Personas inferred (grouped by advertiser)", ""]
    per = defaultdict(list)
    for r in rows:
        per[r["advertiser"]].append(r.get("persona_inferred", "")[:90])
    for a in advs:
        uniq = sorted(set(per[a]))
        out.append("- **%s**: %s" % (a, " / ".join(uniq[:4])))
    out += ["", "## Longevity leaderboard (days active at capture)", "",
            "Caveats printed on purpose: an ad running N days has run N days; it is not evidence of profit. This is an active-only sample, so it cannot say how many ads were launched and stopped. Several variants from one advertiser are one piece of evidence, not several.", "",
            "| Ad | Advertiser | Days | Hook | Variants |", "|---|---|---:|---|---:|"]
    def dnum(r):
        try:
            return int(float(r.get("days_active_at_capture") or 0))
        except Exception:
            return 0
    for r in sorted(rows, key=dnum, reverse=True)[:20]:
        out.append("| %s | %s | %d | %s | %s |" % (r["ad_id"], r["advertiser"], dnum(r), (r.get("hook_text") or "")[:70].replace("|", "/"), r.get("variant_count") or ""))
    out += ["", "## Verdicts and coverage", ""]
    out += table("verdict", Counter(r["verdict"] for r in rows), Counter(), total_adv)[:-1]
    out += table("inspection_coverage", Counter(r["inspection_coverage"] for r in rows), Counter(), total_adv)
    text = "\n".join(out) + "\n"
    print(text)
    if args.md:
        Path(args.md).write_text(text, encoding="utf-8")
        print("wrote", args.md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
