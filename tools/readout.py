#!/usr/bin/env python3
"""readout.py: read an Ads Manager export and say which decision rule fired for each ad.

  python -I readout.py --workspace DIR --csv export.csv [--thresholds plan/thresholds.json]

Column names in Meta exports vary by account and language; this tool matches them loosely
(ad name, amount spent, impressions, link clicks, 3-second video plays, thruplays, results,
cost per result, frequency). Thresholds are member-set in plan/thresholds.json; defaults are
starting points, not benchmarks, and the output says so. Writes plan/readouts/<date>.md.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import adlab_common as C  # noqa: E402

DEFAULTS = {"impression_floor": 2000, "min_hook_rate": 0.25, "min_hold_rate": 0.25, "min_ctr": 0.008,
            "max_frequency": 3.0, "judge_after_conversions": 20, "target_cpa": None, "kill_cpa_multiple": 1.5,
            "_note": "starting points set by Ad Lab, not benchmarks; replace with your own after the first readouts"}

# Other spellings of the threshold keys (library/finance/decision-rules.md and older plans use these).
KEY_ALIASES = {"hook_rate_min": "min_hook_rate", "hook_rate_floor": "min_hook_rate", "hold_rate_min": "min_hold_rate",
               "hold_rate_floor": "min_hold_rate", "ctr_min": "min_ctr", "ctr_floor": "min_ctr",
               "frequency_ceiling": "max_frequency", "min_conversions": "judge_after_conversions"}


def load_thresholds(data: dict) -> dict:
    """Defaults, then the member's file. A key set to null means 'not set by the member': its rule is skipped."""
    t = dict(DEFAULTS)
    for k, v in (data or {}).items():
        t[KEY_ALIASES.get(k, k)] = v
    return t


def below(value, threshold):
    return value is not None and threshold is not None and value < threshold


ALIASES = {
    "name": ["ad name", "ad_name", "ad"],
    "spend": ["amount spent", "spend", "cost"],
    "impressions": ["impressions"],
    "clicks": ["link clicks", "outbound clicks", "clicks (all)", "clicks"],
    "plays3": ["3-second video plays", "3 second video plays", "video plays at 3 seconds", "3-second"],
    "thruplays": ["thruplays", "thru plays", "video plays at 15", "15-second"],
    "results": ["results", "purchases", "leads", "trial", "website purchases", "conversions"],
    "frequency": ["frequency"],
    "reach": ["reach"],
}


def pick(headers, keys):
    low = {h.lower(): h for h in headers}
    for k in keys:
        for h in low:
            if k in h:
                return low[h]
    return None


def num(v):
    if v in (None, ""):
        return None
    try:
        return float(str(v).replace(",", "").replace("$", "").replace("%", ""))
    except Exception:
        return None


def judge(row, t):
    imp, spend, clicks = row.get("impressions") or 0, row.get("spend") or 0, row.get("clicks")
    p3, thru, res, freq = row.get("plays3"), row.get("thruplays"), row.get("results"), row.get("frequency")
    hook = (p3 / imp) if (p3 is not None and imp) else None
    hold = (thru / p3) if (thru is not None and p3) else None
    ctr = (clicks / imp) if (clicks is not None and imp) else None
    cpa = (spend / res) if (res) else None
    m = {"hook_rate": hook, "hold_rate": hold, "ctr": ctr, "cpa": cpa}
    if t.get("impression_floor") is not None and imp < t["impression_floor"]:
        return "too early", "under the impression floor (%d < %d); keep running" % (imp, t["impression_floor"]), m
    if below(hook, t.get("min_hook_rate")):
        return "kill or new hook", "hook rate %.1f%% under %.0f%%: the angle or the first 3 seconds did not select anyone" % (hook * 100, t["min_hook_rate"] * 100), m
    if below(hold, t.get("min_hold_rate")):
        return "iterate body", "hook held but hold rate %.1f%% under %.0f%%: the body loses them; keep the hook, change the middle" % (hold * 100, t["min_hold_rate"] * 100), m
    if below(ctr, t.get("min_ctr")):
        return "iterate offer or CTA", "people watched but CTR %.2f%% under %.2f%%: the promise or the CTA is not pulling" % (ctr * 100, t["min_ctr"] * 100), m
    judge_n = t.get("judge_after_conversions") or 20
    if res is None or res < judge_n:
        return "upstream only", "only %s conversions; judge hook, hold and CTR, not CPA, until %d" % (int(res or 0), judge_n), m
    tgt = t.get("target_cpa")
    if tgt:
        if cpa is not None and cpa <= tgt and t.get("max_frequency") is None:
            return "hold", "CPA %.2f within target %.2f, but max_frequency is not set: set it in plan/thresholds.json before scaling" % (cpa, tgt), m
        if cpa is not None and cpa <= tgt and (freq is None or freq <= t["max_frequency"]):
            return "scale", "CPA %.2f within target %.2f and frequency %s: raise budget in steps" % (cpa, tgt, freq), m
        if cpa is not None and t.get("kill_cpa_multiple") and cpa > tgt * t["kill_cpa_multiple"]:
            return "kill", "CPA %.2f is over %.1fx the target %.2f" % (cpa, t["kill_cpa_multiple"], tgt), m
        if cpa is not None:
            return "iterate landing or offer", "CPA %.2f above target %.2f but not by much: fix the landing continuation or the offer" % (cpa, tgt), m
    if freq is not None and t.get("max_frequency") is not None and freq > t["max_frequency"]:
        return "refresh", "frequency %.1f over %.1f: fatigue; rotate concept" % (freq, t["max_frequency"]), m
    return "hold", "no rule fired; keep running and re-read", m


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--workspace")
    ap.add_argument("--csv", required=True)
    ap.add_argument("--thresholds")
    args = ap.parse_args(argv)
    ws = C.workspace(args.workspace)
    tp = Path(args.thresholds) if args.thresholds else ws / "plan" / "thresholds.json"
    t = load_thresholds(json.loads(tp.read_text(encoding="utf-8")) if tp.exists() else {})
    if not t.get("target_cpa"):
        ej = ws / "plan" / "economics.md"
        if ej.exists():
            for line in ej.read_text(encoding="utf-8").splitlines():
                if line.startswith("| target cost per primary event |"):
                    t["target_cpa"] = num(line.split("|")[2])
    with open(args.csv, encoding="utf-8-sig") as f:
        rd = csv.DictReader(f)
        headers = rd.fieldnames or []
        cols = {k: pick(headers, v) for k, v in ALIASES.items()}
        rows = []
        for r in rd:
            row = {k: (num(r[c]) if c and k != "name" else (r.get(c) if c else None)) for k, c in cols.items()}
            if row.get("name") is None:
                row["name"] = r.get(headers[0]) if headers else "?"
            rows.append(row)
    lines = ["# Readout " + C.today(), "", "Source: %s. Columns matched: %s." % (args.csv, {k: v for k, v in cols.items() if v}), "",
             "Thresholds: " + ", ".join("%s=%s" % (k, v) for k, v in t.items() if not k.startswith("_")), "",
             "These thresholds are starting points, not benchmarks. Replace them in plan/thresholds.json after your first readouts.", "",
             ] + (["Not set by the member, so these rules are skipped: " + ", ".join(k for k in ("min_hook_rate", "min_hold_rate", "min_ctr", "max_frequency") if t.get(k) is None) + ".", ""]
                  if any(t.get(k) is None for k in ("min_hook_rate", "min_hold_rate", "min_ctr", "max_frequency")) else []) + [
             "| Ad | Spend | Impr. | Hook | Hold | CTR | Results | CPA | Rule | Why |", "|---|---:|---:|---:|---:|---:|---:|---:|---|---|"]
    for row in rows:
        rule, why, m = judge(row, t)
        pct = lambda x: ("%.1f%%" % (x * 100)) if x is not None else ""  # noqa: E731
        lines.append("| %s | %s | %s | %s | %s | %s | %s | %s | **%s** | %s |" % (
            row.get("name"), ("%.0f" % row["spend"]) if row.get("spend") is not None else "", ("%.0f" % row["impressions"]) if row.get("impressions") is not None else "",
            pct(m["hook_rate"]), pct(m["hold_rate"]), pct(m["ctr"]), ("%.0f" % row["results"]) if row.get("results") is not None else "",
            ("%.2f" % m["cpa"]) if m["cpa"] is not None else "", rule, why))
    lines += ["", "Reading order: hook rate, then hold rate, then CTR, then CPA at volume. See library/finance/decision-rules.md."]
    out = ws / "plan" / "readouts" / (C.today() + ".md")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print("\nwrote", out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
