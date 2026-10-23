# Economics

Computed 2026-10-23T08:28:04+00:00 from examples/operators-workshop/business/finance.md.

Every number below is only as good as the inputs in finance.md. Placeholders produce placeholder answers. Replace them with observed values and rerun.

## Results

| Measure | Value |
|---|---:|
| contribution per customer | 270.92 |
| ltv simple | 361.23 |
| breakeven cpa | 270.92 |
| breakeven cost per trial | 135.46 |
| target cpa | 162.55 |
| target cost per trial | 81.28 |
| monthly churn estimate | 0.25 |
| primary event | trial start |
| target cost per primary event | 81.28 |
| test budget per concept | 1625.53 |
| concepts affordable per month | 0 |
| judge after conversions | 20 |

## Formulas and the numbers that went in

- Inputs: model=membership price=97.0 gross_margin=0.95 refund_rate=0.02 payback_months=3.00 profit_fraction=0.40
- contribution per paid member over the payback window = period_price x gross_margin x min(months_retained, payback_months) x (1 - refund_rate)
-   = 97.0 x 0.95 x min(4.00, 3.00) x (1 - 0.02) = 270.92
- simple LTV (ceiling, not a target) = period_price x gross_margin x months_retained x (1 - refund_rate) = 361.23
- breakeven CPA per paid member = contribution over the payback window = 270.92
- breakeven cost per trial start = breakeven CPA x trial_to_paid = 270.92 x 0.50 = 135.46
- target CPA per paid member = breakeven x (1 - profit_fraction) = 270.92 x (1 - 0.40) = 162.55
- target cost per trial start = 81.28
- test budget per concept = target cost per primary event x conversions needed to judge = 81.28 x 20 = 1625.53
- concepts the monthly test budget can judge = floor(monthly_test_budget / test budget per concept) = floor(1500.0 / 1625.53) = 0
- the monthly test budget cannot carry one concept to a CPA verdict: judge concepts on hook rate, hold rate and CTR first, or raise the budget, or lower judge_after_conversions and accept a noisier read
- payback months at target CPA = target CPA / monthly contribution; for a one-time purchase this is the window itself.
- MER = revenue / ad spend; nCAC = ad spend / new customers. Both are read from Ads Manager and the store, not predicted here.

## What this can and cannot tell you

- Breakeven CPA is the most you can pay per primary event and lose nothing over the payback window. Target CPA keeps the profit fraction you set.
- Judge CPA only after the conversions-to-judge count; before that, read hook rate, hold rate and CTR (see library/finance/decision-rules.md).
- Retention, trial-to-paid and refund inputs are hypotheses until you have cohorts. Mark them so in finance.md.
