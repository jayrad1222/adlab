# Economics

Computed 2026-10-23T08:28:04+00:00 from examples/ridge-wallet/business/finance.md.

Every number below is only as good as the inputs in finance.md. Placeholders produce placeholder answers. Replace them with observed values and rerun.

## Results

| Measure | Value |
|---|---:|
| contribution per customer | 67.68 |
| breakeven cpa | 67.68 |
| target cpa | 47.38 |
| primary event | purchase |
| target cost per primary event | 47.38 |
| test budget per concept | 1184.4 |
| concepts affordable per month | 5 |
| judge after conversions | 25 |

## Formulas and the numbers that went in

- Inputs: model=product price=110.0 gross_margin=0.60 refund_rate=0.06 payback_months=1.00 profit_fraction=0.30
- contribution per order = aov x gross_margin x (1 - refund_rate) = 120.0 x 0.60 x (1 - 0.06) = 67.68
- breakeven CPA = contribution over the payback window = 67.68
- target CPA = breakeven x (1 - profit_fraction) = 67.68 x (1 - 0.30) = 47.38
- test budget per concept = target cost per primary event x conversions needed to judge = 47.38 x 25 = 1184.4
- concepts the monthly test budget can judge = floor(monthly_test_budget / test budget per concept) = floor(6000.0 / 1184.4) = 5
- payback months at target CPA = target CPA / monthly contribution; for a one-time purchase this is the window itself.
- MER = revenue / ad spend; nCAC = ad spend / new customers. Both are read from Ads Manager and the store, not predicted here.

## What this can and cannot tell you

- Breakeven CPA is the most you can pay per primary event and lose nothing over the payback window. Target CPA keeps the profit fraction you set.
- Judge CPA only after the conversions-to-judge count; before that, read hook rate, hold rate and CTR (see library/finance/decision-rules.md).
- Retention, trial-to-paid and refund inputs are hypotheses until you have cohorts. Mark them so in finance.md.
