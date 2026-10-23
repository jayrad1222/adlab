# Worked example: membership

Purpose: walk the seed's $97 per month community through every formula in [formulas.md](formulas.md), one step at a time, so the finance skill's output has a reference shape. Every number below is a placeholder; replace with your inputs. The $97 example is illustrative only and nothing in it is a benchmark.

## Inputs (placeholder; replace with your inputs)

```yaml
period_price: 97.00          # placeholder
gross_margin: 0.95           # placeholder; after payment processing
refund_rate: 0.00            # placeholder; the seed example ignores refunds
trial_to_paid: 0.60          # placeholder; a hypothesis until measured
months_retained: 4           # placeholder; a hypothesis until measured
payback_months: 4            # placeholder; the member chose to wait four months
profit_fraction: 0.40        # placeholder; the member wants to keep 40%
conversions_to_judge: 30     # placeholder
monthly_test_budget: 4000    # placeholder
```

## Step 1: monthly contribution

```
monthly_contribution = period_price x gross_margin
                     = 97.00 x 0.95
                     = 92.15        (placeholder; replace with your inputs)
```

## Step 2: contribution over the payback window, flat method

The seed's example assumes every member stays exactly four months.

```
contribution_per_customer = monthly_contribution x months_retained - period_price x refund_rate
                          = 92.15 x 4 - 97.00 x 0.00
                          = 368.60     (placeholder; replace with your inputs)
```

The seed rounds this to about $369.

## Step 3: breakeven and target CPA per paid member

```
breakeven_cpa = 368.60                        (placeholder)
target_cpa    = 368.60 x (1 - 0.40) = 221.16  (placeholder)
```

Breakeven is the most the member can pay for one paid member and break even over four months. Target is the figure that leaves 40% of contribution as profit.

## Step 4: the per-trial-start variant

Ads Manager reports trial starts, not paid members, so the targets are scaled by `trial_to_paid`.

```
breakeven_cost_per_trial_start = 368.60 x 0.60 = 221.16   (placeholder)
target_cost_per_trial_start    = 221.16 x 0.60 = 132.70   (placeholder)
```

The seed rounds these to about $221 and about $133. These are the two numbers the readout compares against the cost per trial start column.

## Step 5: the LTV ceiling

```
monthly_churn ≈ 1 / months_retained = 0.25             (placeholder)
ltv_simple    = 92.15 x (1 / 0.25)  = 368.60           (placeholder)
```

With a four-month window and four-month retention, LTV and window contribution coincide. With a longer window they would not, and LTV would be the larger number. It stays a ceiling.

## Step 6: the same window with a churn curve

If the member has a real monthly churn figure, the conservative version is:

```
survival sum over 4 months = 1 + 0.75 + 0.5625 + 0.4219 = 2.7344
contribution_per_customer  = 92.15 x 2.7344 = 251.97     (placeholder)
breakeven_cost_per_trial_start = 251.97 x 0.60 = 151.18   (placeholder)
target_cost_per_trial_start    = 151.18 x 0.60 = 90.71    (placeholder)
```

The two methods differ by a wide margin on the same inputs. The flat method assumes nobody leaves before month four; the churn curve assumes a quarter leave each month from month two. The finance skill prints both and labels which one the member's retention data supports.

## Step 7: test budget per concept

```
test_budget_per_concept = target_cost_per_trial_start x conversions_to_judge
                        = 132.70 x 30 = 3,981.00         (placeholder)
concepts_per_month      = floor(4000 / 3981) = 1          (placeholder)
```

On these placeholders the member can judge one concept per month on CPA. Other concepts in the same month are judged on hook rate, hold rate and CTR only, per [decision rules](decision-rules.md).

## Step 8: reading an actual result

Suppose a concept has produced 30 trial starts at $150 each (placeholder). Against the flat method it is inside breakeven and outside target. Against the churn curve it is just inside breakeven and far outside target. The readout says both, names the method, and applies the iterate-offer rule rather than the scale rule.

```
payback_months_actual = CPA_per_paid_member / monthly_contribution
                      = (150 / 0.60) / 92.15 = 2.71 months   (placeholder)
```

## What this example cannot tell you

- Whether 60% trial-to-paid holds for ad traffic. It is a hypothesis until this ad's trials have ended.
- Whether four months retention holds for members who arrived through an ad.
- Anything about cash. A four-month payback means four months of ad spend carried before it returns.

## Related

- [Inputs](inputs.md)
- [Formulas](formulas.md)
- [Worked example, product](worked-example-product.md)
- [Decision rules](decision-rules.md)
