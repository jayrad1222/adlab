#!/usr/bin/env python3
"""finance.py: turn business/finance.md into the economics every concept must beat.

Reads YAML-style frontmatter from <workspace>/business/finance.md, prints every formula with its
result, and writes <workspace>/plan/economics.md. Numbers are only as good as the inputs; the
output says so.

  python -I finance.py --workspace DIR
  python -I finance.py --file path/to/finance.md [--out economics.md]
  python -I finance.py --example membership | --example product        (the two worked examples)

Frontmatter keys (see library/finance/inputs.md):
  model: membership | product | service
  price, gross_margin (0 to 1), refund_rate (0 to 1)
  product: aov, units_per_order
  membership: trial_to_paid (0 to 1), months_retained OR monthly_churn, period_price
  payback_months, profit_fraction (0 to 1, the share of contribution you want to keep)
  monthly_test_budget, judge_after_conversions (default 20), higgsfield_credit_floor, apify_budget_usd
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import adlab_common as C  # noqa: E402

EXAMPLES = {
    "membership": {"model": "membership", "price": 97, "period_price": 97, "gross_margin": 0.95, "refund_rate": 0.02,
                   "trial_to_paid": 0.6, "months_retained": 4, "payback_months": 4, "profit_fraction": 0.4,
                   "monthly_test_budget": 1500, "judge_after_conversions": 20},
    "product": {"model": "product", "price": 60, "aov": 78, "units_per_order": 1.3, "gross_margin": 0.55,
                "refund_rate": 0.04, "payback_months": 1, "profit_fraction": 0.3, "monthly_test_budget": 2000,
                "judge_after_conversions": 20},
}


def f(x, nd=2):
    if x is None:
        return "n/a"
    if isinstance(x, float) and abs(x) < 10:
        return ("%." + str(nd) + "f") % x
    return "%s" % (round(x, nd) if isinstance(x, float) else x)


def compute(d: dict) -> "tuple[dict, list]":
    """Returns (results, lines). Every line names the formula and the numbers that went in."""
    lines, r = [], {}
    model = (d.get("model") or "product").lower()
    price = float(d.get("price") or 0)
    gm = float(d.get("gross_margin") if d.get("gross_margin") is not None else 0.5)
    refund = float(d.get("refund_rate") or 0)
    payback = float(d.get("payback_months") or 1)
    keep = float(d.get("profit_fraction") if d.get("profit_fraction") is not None else 0.3)
    judge = int(d.get("judge_after_conversions") or 20)
    budget = float(d.get("monthly_test_budget") or 0)
    lines.append("Inputs: model=%s price=%s gross_margin=%s refund_rate=%s payback_months=%s profit_fraction=%s"
                 % (model, f(price), f(gm), f(refund), f(payback), f(keep)))

    if model == "membership":
        period = float(d.get("period_price") or price)
        ttp = float(d.get("trial_to_paid") if d.get("trial_to_paid") is not None else 1.0)
        months = d.get("months_retained")
        churn = d.get("monthly_churn")
        if months is None and churn:
            months = 1.0 / float(churn)
            lines.append("months_retained = 1 / monthly_churn = 1 / %s = %s" % (f(float(churn)), f(months)))
        months = float(months or 1)
        churn_est = (1.0 / months) if months else None
        window = min(months, payback)
        contrib_paid = period * gm * window * (1 - refund)
        lines.append("contribution per paid member over the payback window = period_price x gross_margin x min(months_retained, payback_months) x (1 - refund_rate)")
        lines.append("  = %s x %s x min(%s, %s) x (1 - %s) = %s" % (f(period), f(gm), f(months), f(payback), f(refund), f(contrib_paid)))
        ltv = period * gm * months * (1 - refund)
        lines.append("simple LTV (ceiling, not a target) = period_price x gross_margin x months_retained x (1 - refund_rate) = %s" % f(ltv))
        be_paid = contrib_paid
        be_trial = be_paid * ttp
        lines.append("breakeven CPA per paid member = contribution over the payback window = %s" % f(be_paid))
        lines.append("breakeven cost per trial start = breakeven CPA x trial_to_paid = %s x %s = %s" % (f(be_paid), f(ttp), f(be_trial)))
        tgt_paid = be_paid * (1 - keep)
        tgt_trial = be_trial * (1 - keep)
        lines.append("target CPA per paid member = breakeven x (1 - profit_fraction) = %s x (1 - %s) = %s" % (f(be_paid), f(keep), f(tgt_paid)))
        lines.append("target cost per trial start = %s" % f(tgt_trial))
        r.update({"contribution_per_customer": contrib_paid, "ltv_simple": ltv, "breakeven_cpa": be_paid,
                  "breakeven_cost_per_trial": be_trial, "target_cpa": tgt_paid, "target_cost_per_trial": tgt_trial,
                  "monthly_churn_estimate": churn_est, "primary_event": "trial start" if ttp < 1 else "paid member",
                  "target_cost_per_primary_event": tgt_trial if ttp < 1 else tgt_paid})
    else:
        aov = float(d.get("aov") or price * float(d.get("units_per_order") or 1))
        contrib = aov * gm * (1 - refund)
        lines.append("contribution per order = aov x gross_margin x (1 - refund_rate) = %s x %s x (1 - %s) = %s" % (f(aov), f(gm), f(refund), f(contrib)))
        repeat = d.get("repeat_orders_in_payback")
        window_contrib = contrib * (1 + float(repeat or 0))
        if repeat:
            lines.append("contribution over the payback window = contribution per order x (1 + repeat_orders_in_payback) = %s" % f(window_contrib))
        be = window_contrib
        tgt = be * (1 - keep)
        lines.append("breakeven CPA = contribution over the payback window = %s" % f(be))
        lines.append("target CPA = breakeven x (1 - profit_fraction) = %s x (1 - %s) = %s" % (f(be), f(keep), f(tgt)))
        r.update({"contribution_per_customer": window_contrib, "breakeven_cpa": be, "target_cpa": tgt,
                  "primary_event": "purchase", "target_cost_per_primary_event": tgt})
    tgt_ev = r["target_cost_per_primary_event"]
    per_concept = tgt_ev * judge
    lines.append("test budget per concept = target cost per primary event x conversions needed to judge = %s x %d = %s" % (f(tgt_ev), judge, f(per_concept)))
    concepts = int(budget // per_concept) if per_concept > 0 and budget else None
    if budget:
        lines.append("concepts the monthly test budget can judge = floor(monthly_test_budget / test budget per concept) = floor(%s / %s) = %s" % (f(budget), f(per_concept), concepts))
    r.update({"test_budget_per_concept": per_concept, "concepts_affordable_per_month": concepts, "judge_after_conversions": judge})
    if budget and concepts == 0:
        lines.append("the monthly test budget cannot carry one concept to a CPA verdict: judge concepts on hook rate, hold rate and CTR first, or raise the budget, or lower judge_after_conversions and accept a noisier read")
    lines.append("payback months at target CPA = target CPA / monthly contribution; for a one-time purchase this is the window itself.")
    lines.append("MER = revenue / ad spend; nCAC = ad spend / new customers. Both are read from Ads Manager and the store, not predicted here.")
    return r, lines


def render_md(d: dict, r: dict, lines: list, source: str) -> str:
    out = ["# Economics", "", "Computed " + C.now_iso() + " from " + source + ".", "",
           "Every number below is only as good as the inputs in finance.md. Placeholders produce placeholder answers. Replace them with observed values and rerun.", "",
           "## Results", "", "| Measure | Value |", "|---|---:|"]
    for k, v in r.items():
        out.append("| %s | %s |" % (k.replace("_", " "), f(v) if not isinstance(v, str) else v))
    out += ["", "## Formulas and the numbers that went in", ""]
    out += ["- " + l for l in lines]
    out += ["", "## What this can and cannot tell you", "",
            "- Breakeven CPA is the most you can pay per primary event and lose nothing over the payback window. Target CPA keeps the profit fraction you set.",
            "- Judge CPA only after the conversions-to-judge count; before that, read hook rate, hold rate and CTR (see library/finance/decision-rules.md).",
            "- Retention, trial-to-paid and refund inputs are hypotheses until you have cohorts. Mark them so in finance.md."]
    return "\n".join(out) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--workspace")
    ap.add_argument("--file")
    ap.add_argument("--out")
    ap.add_argument("--example", choices=list(EXAMPLES))
    args = ap.parse_args(argv)
    if args.example:
        d, source = dict(EXAMPLES[args.example]), "the built-in %s example (placeholders)" % args.example
        outp = Path(args.out) if args.out else None
    else:
        ws = C.workspace(args.workspace)
        fp = Path(args.file) if args.file else ws / "business" / "finance.md"
        if not fp.exists():
            C.die("finance.md not found at %s (run /adlab:intake first)" % fp)
        d, _ = C.read_frontmatter(fp)
        source = str(fp)
        outp = Path(args.out) if args.out else ws / "plan" / "economics.md"
    r, lines = compute(d)
    md = render_md(d, r, lines, source)
    print(md)
    if outp:
        outp.parent.mkdir(parents=True, exist_ok=True)
        outp.write_text(md, encoding="utf-8")
        print("wrote", outp)
    return 0


if __name__ == "__main__":
    sys.exit(main())
