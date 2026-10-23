# Finance formulas

Purpose: every formula the finance gate uses, written out with the variable names from [inputs.md](inputs.md), and a plain statement of what each number can and cannot tell you. The finance skill prints the formula next to every result so the member can check it.

## Contribution per customer

One-time product, one order inside the payback window:

```
contribution_per_customer = aov x gross_margin - aov x refund_rate
```

where `aov = price x units_per_order` if `aov` is not supplied. The refund term assumes a refunded order loses all its revenue and the goods are not recovered. If goods come back resellable, use `aov x gross_margin x refund_rate` for the refund term instead.

Membership, summed over the payback window:

```
contribution_per_customer =
  sum for m = 1 to payback_months of
    (period_price x gross_margin x survival(m))
  - period_price x refund_rate
```

`survival(m)` is the fraction of paying members still paying in month m. Two ways to set it:

- Flat: `survival(m) = 1` for `m <= months_retained`, else 0. Every member stays exactly the average. Simple and optimistic.
- Churn curve: `survival(m) = (1 - monthly_churn) ^ (m - 1)`. More conservative over a fixed window because members leave from month two.

Use the flat version when the member only has an average retention figure. Use the churn curve when they have a real churn rate. Say which one was used.

What it tells you: the most the member can pay to acquire one customer and not lose money within the window. What it cannot tell you: anything about revenue after the window, or whether the churn figure will hold for customers who arrive through ads rather than referrals.

## Breakeven and target CPA

```
breakeven_cpa = contribution_per_customer
target_cpa    = breakeven_cpa x (1 - profit_fraction)
```

Breakeven is the ceiling. Target is where the member keeps the profit share they chose. A concept whose CPA sits between target and breakeven is not losing money; it is not making the profit the member asked for.

## Per-trial-start variant for memberships

Ads for a trial membership are judged on cost per trial start, not cost per paid member, because the paid event arrives after the trial ends.

```
breakeven_cost_per_trial_start = breakeven_cpa x trial_to_paid
target_cost_per_trial_start    = target_cpa x trial_to_paid
```

What it tells you: the ceiling and target for the number Ads Manager actually reports. What it cannot tell you: whether this ad's trials convert at the same rate as the historical `trial_to_paid`. Ad traffic often converts worse than organic. Recompute once this ad's own trials have run their course.

## Subscription LTV ceiling

```
ltv_simple = period_price x gross_margin x (1 / monthly_churn)
```

What it tells you: the total contribution an average member would produce if churn stayed constant forever. What it cannot tell you: when that money arrives. Treat it as a ceiling, never a target. Spending to LTV means waiting the full lifetime to get paid back, and most small businesses cannot.

## Efficiency ratios

```
MER   = total_revenue / total_ad_spend
nCAC  = ad_spend / new_customers
payback_months_actual = CPA / monthly_contribution
```

where `monthly_contribution = period_price x gross_margin` for memberships, or `contribution_per_customer / payback_months` for products with repeat purchase.

MER tells you whether the whole business is covering its ad spend, including organic and returning revenue. It cannot attribute anything to a single ad. nCAC tells you what each new customer cost across all spend. It cannot tell you which ad brought them. Payback months tells you how long cash is tied up per customer. It cannot tell you whether the member has the cash to wait.

## Test budget per concept

```
test_budget_per_concept = target_cpa x conversions_to_judge
concepts_per_month      = floor(monthly_test_budget / test_budget_per_concept)
```

For trial memberships substitute `target_cost_per_trial_start`.

`conversions_to_judge` is a member-set number. The seed's guidance: a practical floor is in the tens of conversions, not single digits. Below the floor, judge the concept on hook rate, hold rate and CTR only. See [decision rules](decision-rules.md).

What it tells you: how many new concepts the member can afford to judge fairly each month. What it cannot tell you: which concepts to test. If `concepts_per_month` is zero, the member either raises the budget, raises the price, or tests one concept at a time and accepts a slower read.

## Breakeven and target ROAS

A convenience for members who think in ROAS:

```
breakeven_roas = aov / breakeven_cpa
target_roas    = aov / target_cpa
```

ROAS inside Ads Manager counts attributed revenue only, so a true breakeven on this figure is a stricter test than MER.

## Related

- [Inputs](inputs.md)
- [Worked example, membership](worked-example-membership.md)
- [Worked example, product](worked-example-product.md)
- [Signals glossary](signals-glossary.md)
- [Decision rules](decision-rules.md)
- [Hormozi value equation](../strategy/hormozi-value-equation.md)
