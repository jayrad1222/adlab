# Finance inputs

Purpose: define every number the finance gate needs, say where a member finds it, and give the frontmatter template for `business/finance.md`. The formulas in [formulas.md](formulas.md) use these key names exactly. Nothing in the bank is scored for spend until this file is filled with the member's own numbers.

## Definitions and where to find them

- `price`: what one customer pays for one purchase. For a one-time product, the list price. For a membership, leave this blank and use `period_price`. Found on the checkout page.
- `gross_margin`: the fraction of price left after direct costs of delivering the sale (goods, shipping, payment processing, platform fees). Written as a decimal, 0.55 for 55%. Found in the accounting system or by subtracting cost of goods and fees from price on one order.
- `refund_rate`: the fraction of orders refunded or charged back. Decimal. Found in the payment processor's disputes and refunds report over the last ninety days or longer.
- `aov`: average order value. Total revenue divided by number of orders over the same period. Found in the store or payment dashboard. If every order is one unit, `aov` equals `price`.
- `units_per_order`: average number of units in an order. Used to derive `aov` when the member knows price and units but not the average. Found in the store's order export.
- `trial_to_paid`: for memberships with a trial, the fraction of trial starts that become paying members. Decimal. Found in the membership platform's trial report. If there is no trial, set to 1.0.
- `months_retained`: the average number of paid months a member stays. Found in the membership platform's retention or cohort report. Use this or `monthly_churn`, not both.
- `monthly_churn`: the fraction of paying members who cancel in a month. Decimal. Roughly 1 divided by `months_retained`. Found in the same report.
- `period_price`: the price per billing period for a membership. Found on the checkout page.
- `payback_months`: how many months the member will wait to recover the cost of acquiring a customer. A decision, not a measurement. One month means ads must pay back on the first order. Longer windows need cash to carry.
- `monthly_test_budget`: the ad spend the member will put into testing new concepts each month, separate from spend on proven ads. A decision.
- `higgsfield_credit_floor`: the Higgsfield credit balance below which the render pipeline stops producing new video. Each member sets their own floor.
- `apify_budget_usd`: the monthly dollar cap on Apify scraping of ad libraries and comments. A decision.

Optional but useful: `profit_fraction`, the share of contribution the member keeps after ad cost (the seed's example uses 0.40), and `conversions_to_judge`, the conversions a concept needs before CPA is trusted (the seed says tens, not single digits).

## Frontmatter template for `business/finance.md`

```yaml
---
# Pricing and margin
price: 60.00                # one-time product price; blank for memberships
gross_margin: 0.55          # decimal
refund_rate: 0.04           # decimal
aov: 78.00                  # average order value; or derive from price x units_per_order
units_per_order: 1.3

# Memberships (leave blank for one-time products)
period_price:               # price per billing period
trial_to_paid:              # decimal; 1.0 if no trial
months_retained:            # use this or monthly_churn
monthly_churn:              # decimal

# Decisions
payback_months: 1           # months allowed to recover acquisition cost
profit_fraction: 0.30       # share of contribution to keep after ad cost
conversions_to_judge: 30    # conversions before CPA is trusted
monthly_test_budget: 3000   # USD per month on new concepts

# Pipeline caps
higgsfield_credit_floor: 150
apify_budget_usd: 50
---
```

Every value above is a placeholder. The finance skill refuses to compute a target CPA when `gross_margin`, `refund_rate` and either `price` or `period_price` are blank.

## Pricing psychology checklist for the offer

The inputs above take the price as given. Before it is given, run the price through this list. Each item is a lever the offer line can pull; none is a rule.

- Anchoring: show the reference price before the actual price. The first number seen sets the scale.
- Decoy: a third option that makes the target option look like the sensible choice.
- Goldilocks tiers: three tiers, with the middle one as the intended purchase.
- Charm versus round: prices ending in 7 or 9 signal value; round numbers signal premium. Pick the one that matches the positioning.
- Price as a signal: a higher price can raise expected efficacy. Sutherland's point, and it cuts both ways in a trust-poor category.
- Per-day or per-use reframe: the same price restated in the unit the viewer feels least.
- Free: its own category in the viewer's mind, not the low end of a scale. Use it for the first step, not the product.
- Pain-of-paying smoothing: annual billing, bundles, one payment instead of many.
- Guarantees: unconditional, conditional, performance-based, or "keep the bonuses if you refund." Each answers a different trust objection.
- Bonuses: each bonus should remove one named objection. A bonus that removes nothing is noise.
- Scarcity and urgency: only when true, with the reason stated.
- Offer naming, after Hormozi: a reason the offer exists now, who it is for, the goal it reaches, the time it takes, and the container it comes in. Rewrite the offer line with all five, then cut what the ad does not need.

## Related

- [Formulas](formulas.md)
- [Decision rules](decision-rules.md)
- [Hormozi value equation](../strategy/hormozi-value-equation.md)
- [Hormozi offer stack](../strategy/hormozi-offer-stack.md)
- [Anchoring and framing](../psychology/anchoring-and-framing.md)
- [Power of free and decoy](../psychology/power-of-free-and-decoy.md)
- [Price is information](../psychology/price-is-information.md)
