# Signals glossary

Purpose: define each signal the readout skill reads from an Ads Manager export, how it is computed from the export's columns, what it tells you and what it does not. Column names follow Meta Ads Manager; see [platform differences](../platform/tiktok-youtube-differences.md) for TikTok and YouTube. Every threshold is member-set; none is given here.

## CPM

Definition: cost per thousand impressions.

Computed: `Amount spent / Impressions x 1000`. Meta exports a CPM column directly.

Tells you: how expensive the audience and auction are right now, and whether the platform thinks the ad is relevant enough to serve cheaply.

Does not tell you: whether anyone watched, clicked or bought. A low CPM on a bad ad is cheap waste.

## Hook rate

Definition: the share of impressions that became a 3-second video play.

Computed: `3-second video plays / Impressions`.

Tells you: whether the first frames selected anyone. This is the first number read on a new concept, because a concept that stops nobody cannot be judged on anything downstream.

Does not tell you: whether the right people stopped, or whether they stayed. A shock opener produces hook rate without an audience.

## Hold rate

Definition: the share of people who started watching and stayed.

Computed: `ThruPlays / 3-second video plays`. Where the export has 15-second plays, `15-second plays / 3-second video plays` is the stricter read for long videos.

Tells you: whether the body kept the people the hook selected. Good hook and poor hold means the promise of the first seconds was not kept.

Does not tell you: anything for statics, which have no play events, and little for videos under 15 seconds, where ThruPlay and completion are the same thing.

## CTR

Definition: link click-through rate.

Computed: `Link clicks / Impressions`. Use the link version, not "CTR (all)," which counts clicks on the profile and the like button.

Tells you: whether the offer and CTA pulled. On a static this is the first real signal after CPM.

Does not tell you: whether the click was worth anything. Curiosity hooks produce clicks that bounce.

## CPC

Definition: cost per link click.

Computed: `Amount spent / Link clicks`.

Tells you: the price of a visit, which combines CPM and CTR. Useful for comparing two ads to the same page.

Does not tell you: anything the CPM and CTR did not already say. It is a derived number.

## Landing conversion rate

Definition: the share of visits that became the conversion event.

Computed: `Results / Landing page views`. If landing page views are not tracked, `Results / Link clicks`, which runs lower because some clicks never load the page.

Tells you: whether the page did its job for the traffic this ad sent. Good CTR and poor landing conversion points at the page or the offer, not the ad.

Does not tell you: whether the page is bad in general. Each ad sends a different crowd.

## CPA

Definition: cost per acquisition, or cost per result for the chosen conversion event.

Computed: `Amount spent / Results`. Make sure "Results" is the purchase, trial start or lead the finance gate was built on, not an upstream event.

Tells you: what the member paid per customer from this ad, under the platform's attribution window.

Does not tell you: anything reliable at low volume; see the minimum-volume rule in [decision rules](decision-rules.md). Nor whether the attributed conversions would have happened anyway.

## ROAS

Definition: attributed revenue divided by spend.

Computed: `Purchase conversion value / Amount spent`. Meta exports a ROAS column.

Tells you: the return on this ad under platform attribution, comparable to `target_roas` from the formulas.

Does not tell you: the business's actual return. Attribution windows, view-through counting and organic overlap all move it.

## MER

Definition: marketing efficiency ratio; total revenue over total ad spend.

Computed: not from the Ads Manager export. `Total revenue (store or payment processor) / Total ad spend (all platforms)` for the same period.

Tells you: whether the business as a whole is covering its ads, including organic and returning revenue.

Does not tell you: which ad, concept or platform did the work. It moves with everything.

## nCAC

Definition: new customer acquisition cost.

Computed: `Total ad spend / New customers`, with the new customer count from the store or CRM, not from Ads Manager.

Tells you: what each genuinely new customer cost, free of attribution games.

Does not tell you: which ad brought them, or anything per concept.

## Frequency

Definition: average number of times each person reached saw the ad.

Computed: `Impressions / Reach`. Meta exports a frequency column.

Tells you: whether the ad is reaching new people or re-serving the same ones. Rising frequency with rising CPA is the usual sign of creative wearing out.

Does not tell you: how many people saw it (that is reach), or whether repeat views were useful. Some offers need several exposures.

## Reading order

For a new concept: hook rate, then hold rate, then CTR, then CPA, and CPA only at sufficient volume. For a static, skip the two video signals. The order exists because each signal depends on the one before it: there is no hold without a hook, no click without a view, no purchase without a click. See [decision rules](decision-rules.md) for what to do at each step.

## Related

- [Decision rules](decision-rules.md)
- [Formulas](formulas.md)
- [Denney concept versus iteration](../strategy/denney-concept-vs-iteration.md)
- [Hook taxonomy](../copy/hook-taxonomy.md)
- [TikTok and YouTube differences](../platform/tiktok-youtube-differences.md)
