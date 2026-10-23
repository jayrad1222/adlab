# Worked example: physical product

Purpose: walk a one-time physical product through every formula in [formulas.md](formulas.md), step by step, so the finance skill's output has a reference shape for non-subscription businesses. Every number below is a placeholder; replace with your inputs. Nothing here is a benchmark.

## Inputs (placeholder; replace with your inputs)

```yaml
price: 60.00                 # placeholder
gross_margin: 0.55           # placeholder; after goods, shipping, processing
refund_rate: 0.04            # placeholder
units_per_order: 1.3         # placeholder
payback_months: 1            # placeholder; ads must pay back on the first order
profit_fraction: 0.30        # placeholder; the member wants to keep 30%
conversions_to_judge: 30     # placeholder
monthly_test_budget: 3000    # placeholder
```

## Step 1: average order value

```
aov = price x units_per_order
    = 60.00 x 1.3
    = 78.00        (placeholder; replace with your inputs)
```

If the store export gives a real `aov`, use that and skip this step.

## Step 2: gross contribution per order

```
gross_contribution = aov x gross_margin
                   = 78.00 x 0.55
                   = 42.90        (placeholder)
```

## Step 3: refund cost per order

```
refund_cost = aov x refund_rate
            = 78.00 x 0.04
            = 3.12         (placeholder)
```

This assumes a refunded order loses its full revenue and the goods are not recovered. If returned goods are resold, the refund term is `aov x gross_margin x refund_rate = 1.72` (placeholder) instead, and contribution rises to 41.18. The finance skill asks which case applies.

## Step 4: contribution per customer

With a one-month payback window there is one order inside the window. Repeat purchases are not counted.

```
contribution_per_customer = gross_contribution - refund_cost
                          = 42.90 - 3.12
                          = 39.78        (placeholder)
```

## Step 5: breakeven and target CPA

```
breakeven_cpa = 39.78                         (placeholder)
target_cpa    = 39.78 x (1 - 0.30) = 27.85    (placeholder)
```

The member can pay up to $39.78 per purchase and break even on the first order. At $27.85 per purchase they keep 30% of contribution.

## Step 6: breakeven and target ROAS

For members who read the ROAS column:

```
breakeven_roas = aov / breakeven_cpa = 78.00 / 39.78 = 1.96   (placeholder)
target_roas    = aov / target_cpa    = 78.00 / 27.85 = 2.80   (placeholder)
```

Ads Manager ROAS counts attributed revenue only. A concept at 2.80 attributed ROAS is at target; the business-level check is MER, below.

## Step 7: test budget per concept

```
test_budget_per_concept = target_cpa x conversions_to_judge
                        = 27.85 x 30 = 835.50             (placeholder)
concepts_per_month      = floor(3000 / 835.50) = 3         (placeholder)
```

Three concepts a month can be judged on CPA. A fourth would run short of conversions and is judged on upstream signals only.

## Step 8: reading an actual result

Suppose a concept has 30 purchases at $33 each (placeholder) after $990 of spend (placeholder). That is inside breakeven and outside target. The readout applies the iterate-offer rule: the ad brings buyers at a cost that does not lose money but does not leave the profit the member asked for.

```
payback_months_actual = CPA / contribution_per_customer
                      = 33.00 / 39.78 = 0.83 months        (placeholder)
```

Under one month, so the window is met.

Suppose instead the month's total revenue was $9,000 across all channels (placeholder) on $2,800 of total ad spend (placeholder):

```
MER  = 9000 / 2800 = 3.21     (placeholder)
nCAC = 2800 / new_customers   (placeholder; needs the new customer count from the store)
```

MER above `breakeven_roas` says the business as a whole covers its ads. It says nothing about which ad is working.

## What this example cannot tell you

- Whether buyers return. A one-month window ignores repeat orders on purpose. If the member has repeat data, lengthen `payback_months` and add the expected repeat contribution.
- Whether the refund rate holds for ad buyers. Cold traffic often refunds more than warm traffic.
- Whether $78 holds as the average order for ad traffic. Check `aov` on ad-attributed orders separately once there are enough.

## Related

- [Inputs](inputs.md)
- [Formulas](formulas.md)
- [Worked example, membership](worked-example-membership.md)
- [Signals glossary](signals-glossary.md)
- [Decision rules](decision-rules.md)
