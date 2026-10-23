#!/usr/bin/env python3
"""scan.py: list every line in a workspace's ad bank that a reviewer has to check against its source.

  python -I scan.py --workspace DIR                 writes analysis/scan.md and prints the counts
  python -I scan.py --workspace DIR --out FILE      writes the list somewhere else

Reads bank/entries.jsonl: the copy fields (hook, primary text at every length, headline, description,
CTA), the hooks list, the on-image text in layout_fields, and carousel cards. Flags numbers, prices and
percentages; words the truth rules and ad policies care about (guarantees and risk-free, income and
results, counts of members, customers or reviews, ratings, scarcity and urgency, superlatives, free and
discounts, testimonials); and every competitor named in competitors/roster.json. A hit is not a problem
by itself: "no guarantees" and a fee printed on the member's own terms page are hits too. The critic
resolves each one against its source during /adlab:review.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import adlab_common as C  # noqa: E402

FIELDS = ["hook", "primary_text_short", "primary_text_medium", "primary_text_long", "headline", "description", "cta"]

CATEGORIES = [
    ("number", r"\$\s?\d[\d,.]*|\d+(?:\.\d+)?\s?%|\b\d[\d,]*(?:\.\d+)?\b"),
    ("guarantee", r"\bguarant\w*|\brisk[- ]free\b|\bmoney[- ]back\b|\bwarrant\w*"),
    ("income or results", r"\bearn\w*|\bincome\b|\brevenue\b|\bprofit\w*|\bresults?\b|\bROI\b|\bsav(?:e|es|ed|ing)\b|\bclients? in\b"),
    ("counts and ratings", r"\bmembers?\b|\bcustomers?\b|\breviews?\b|\brat(?:ed|ing)\b|\bstars?\b|\bjoin(?:ed)? \d|\bpeople\b"),
    ("scarcity or urgency", r"\blimited\b|\bonly\b|\btoday\b|\btonight\b|\bhurry\b|\blast chance\b|\bends?\b|\bsold out\b|\bin stock\b|\bspots? left\b|\bdeadline\b|\bgoing up\b|\brises?\b"),
    ("superlative", r"\bbest\b|#1\b|\bnumber one\b|\bproven\b|\bguru\b|\bultimate\b|\bworld[- ]class\b"),
    ("free or discount", r"\bfree\b|\boff\b|\bdiscount\w*|\bcode\b|\bdeal\b|\bsale\b"),
    ("testimonial", r"\btestimonial\w*|\bsaid\b|\bsays\b|\"[^\"]{8,}\""),
]


def competitor_pattern(ws: Path):
    p = ws / "competitors" / "roster.json"
    names = set()
    if p.exists():
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            data = {}
        items = data.get("advertisers", data) if isinstance(data, dict) else data
        for a in items if isinstance(items, list) else []:
            for n in [a.get("name")] + list(a.get("page_names") or []):
                if n and len(n.strip()) >= 3:
                    names.add(n.strip())
                    first = n.split()[0]
                    if len(first) >= 5 and first.lower() not in {"maker", "build", "learn", "thread", "the", "ai"}:
                        names.add(first)
    if not names:
        return None
    return re.compile(r"\b(" + "|".join(re.escape(n) for n in sorted(names, key=len, reverse=True)) + r")\b")


def texts(entry: dict):
    """Yield (where, text) for every piece of ad copy and on-image text in one entry."""
    for f in FIELDS:
        if entry.get(f):
            yield f, str(entry[f])
    for i, h in enumerate(entry.get("hooks") or []):
        yield "hooks[%d]" % (i + 1), str(h)
    lf = entry.get("layout_fields") or {}
    if isinstance(lf, dict):
        for k, v in lf.items():
            if k == "cards" and isinstance(v, list):
                for c in v:
                    for ck, cv in (c or {}).items():
                        if isinstance(cv, str) and ck != "template":
                            yield "image card %s %s" % (c.get("step", "?"), ck), cv
            elif isinstance(v, str) and not k.endswith("_image"):
                yield "image " + k, v


def scan(ws: Path):
    entries = C.read_jsonl(ws / "bank" / "entries.jsonl")
    comp = competitor_pattern(ws)
    pats = [(name, re.compile(rx, re.I if name != "testimonial" else 0)) for name, rx in CATEGORIES]
    if comp:
        pats.append(("competitor name", comp))
    hits, per_cat = [], Counter()
    for e in entries:
        for where, text in texts(e):
            for name, rx in pats:
                found = sorted({m.group(0) for m in rx.finditer(text)}, key=str.lower)
                if found:
                    per_cat[name] += 1
                    hits.append({"entry_id": e.get("entry_id", "?"), "status": e.get("status", ""), "where": where,
                                 "category": name, "terms": found, "text": re.sub(r"\s+", " ", text)[:220]})
    return entries, hits, per_cat


def group(hits):
    """One row per distinct (category, text), listing every entry and field that carries it."""
    rows = {}
    for h in hits:
        k = (h["category"], h["text"])
        r = rows.setdefault(k, {"category": h["category"], "text": h["text"], "terms": set(), "where": [], "statuses": set()})
        r["terms"].update(h["terms"])
        r["where"].append("%s %s" % (h["entry_id"], h["where"]))
        r["statuses"].add(h["status"] or "draft")
    return list(rows.values())


def to_markdown(ws: Path, entries, hits, per_cat) -> str:
    live = {"ready", "rendered", "testing"}
    rows = group(hits)
    n_ready = sum(1 for e in entries if e.get("status") in live)
    lines = ["# Scan of the ad bank", "",
             "Written %s by `tools/scan.py` from `bank/entries.jsonl` (%d entries, %d ready, rendered or testing). "
             "Each row is a distinct line of ad copy or on-image text that contains a number, a word the truth rules or ad policies care about, "
             "or a competitor's name, with every entry that carries it. A row is not a finding: the critic checks each one against its source "
             "in `/adlab:review` and says whether it is sourced or a problem." % (C.today(), len(entries), n_ready), "",
             "| Category | Distinct lines | In ready entries |", "|---|---:|---:|"]
    for name, _ in CATEGORIES + [("competitor name", "")]:
        rs = [r for r in rows if r["category"] == name]
        if rs:
            lines.append("| %s | %d | %d |" % (name, len(rs), sum(1 for r in rs if r["statuses"] & live)))
    for title, sel in (("Lines in ready, rendered or testing entries", lambda r: r["statuses"] & live),
                       ("Lines only in draft or held entries", lambda r: not (r["statuses"] & live))):
        part = sorted([r for r in rows if sel(r)], key=lambda r: (r["category"], r["text"]))
        lines += ["", "## " + title, ""]
        if not part:
            lines.append("None.")
            continue
        lines += ["| Category | Terms | Text | Where |", "|---|---|---|---|"]
        for r in part:
            where = ", ".join(sorted(set(r["where"])))
            lines.append("| %s | %s | %s | %s |" % (r["category"], ", ".join(sorted(r["terms"], key=str.lower)).replace("|", "/"),
                                                    r["text"].replace("|", "/"), where.replace("|", "/")))
    return "\n".join(lines) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--workspace", help="workspace folder (default: ./adlab-workspace)")
    ap.add_argument("--out", help="where to write the list (default: <workspace>/analysis/scan.md)")
    args = ap.parse_args(argv)
    ws = C.workspace(args.workspace)
    if not (ws / "bank" / "entries.jsonl").exists():
        C.die("no bank/entries.jsonl in %s (run /adlab:bank first)" % ws)
    entries, hits, per_cat = scan(ws)
    out = Path(args.out) if args.out else ws / "analysis" / "scan.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(to_markdown(ws, entries, hits, per_cat), encoding="utf-8")
    rows = group(hits)
    for name, n in Counter(r["category"] for r in rows).most_common():
        print("%-20s %d distinct lines" % (name, n))
    print("scanned %d entries, %d distinct lines to check; wrote %s" % (len(entries), len(rows), out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
