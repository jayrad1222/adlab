# The opposite pass

## What it is

Rory Sutherland's rule: the opposite of a good idea can also be a good idea. Red Bull launched with a small can, a strange taste and a high price, every one of them the inverse of the soft-drink conventions of its time, and every one of them read as a signal of potency. The opposite pass is the mandatory step in `/adlab:angles` and Part D of the interrogation where the category's conventions are inverted on purpose and each inversion is tested for a mechanism before it is allowed to become a concept.

The pass is not "be contrarian". An inversion with no mechanism is noise. An inversion with a mechanism, a persona and a cheap test is a concept candidate that competitors are unlikely to copy, because they would have to admit their convention is arbitrary.

Related: [`../psychology/opposite-pass.md`](../psychology/opposite-pass.md), [`../psychology/test-counterintuitive-things.md`](../psychology/test-counterintuitive-things.md), [`../psychology/costly-signaling.md`](../psychology/costly-signaling.md), [`../psychology/price-is-information.md`](../psychology/price-is-information.md), [`../psychology/shotton-illusion-of-choice.md`](../psychology/shotton-illusion-of-choice.md) (the red sneakers effect, the pratfall effect), [`../rubrics/market-map-template.md`](../rubrics/market-map-template.md), [`../rubrics/concept-brief-schema.md`](../rubrics/concept-brief-schema.md).

## Inputs

- `analysis/market-map.md`, sections 3 (table-stakes claims), 6 (proof arms race), 7 (price and positioning), 8 (format mix) and 10 (conventions worth inverting).
- `analysis/ads.csv` for the ids behind each convention.
- The persona files, for who an inversion would speak to.
- `business/offer.md` and `assets/catalog.md`, for whether the member can truthfully do the inverse.

## Procedure

1. **Pick the top five conventions.** From the market map, choose the five most common patterns across these kinds: a claim (what most ads promise), a format (how most ads look), a proof type (what most ads show as evidence), a price signal (how price is framed or hidden), a tone (how most ads sound). Each convention is stated with its count and ids. If the market map does not have five clear conventions, say so and work with what it has; do not invent a convention to invert.

2. **Write the inverse.** For each convention, state the literal opposite in one sentence. Then write at least one non-literal inverse, because the literal opposite is sometimes the wrong axis (the opposite of "fast" might be "slow", but it might be "no deadline at all", or "we tell you when it will be done and we are never early").

3. **Ask whether the inverse is also a good idea.** Not whether it is interesting. The test is: is there a named mechanism by which the inverse would make a specific persona more likely to feel the thing the ad needs them to feel? Candidate mechanisms: costly signaling (the inverse is visibly more effortful), price as information (the inverse signals quality), satisficing (the inverse removes a fear the convention creates), the pratfall effect (admitting what the convention hides raises trust), the red sneakers effect (nonconformity reads as confidence when the business could clearly conform), distinctiveness (the inverse is the odd one out and is remembered), context change (the inverse moves the product to a different reference frame).

4. **Name the persona.** Which persona file does the inverse speak to, and at which awareness stage? An inversion that speaks to no persona is cut.

5. **Check that it is true.** Can the member actually do the inverse, from `offer.md` and the catalog? An inversion the member cannot deliver is a lie with a mechanism. Cut it or note what would have to change in the offer first.

6. **Write the cheapest test.** The smallest, lowest-budget way to see whether the inverse selects anyone: usually one static or one 15-second video in the first test batch, read on hook rate and hold rate per `../finance/decision-rules.md`. State the falsifier: what result sends the inverse back to the shelf.

7. **Reject what is merely contrarian.** Any row whose mechanism column is empty, vague ("it stands out"), or restates the inverse ("because nobody says slow") is rejected and the rejection reason is written in the table. Rejections stay in the document; they tell the next round what was already tried.

8. **Promote survivors.** Each inverse that survives all steps becomes a candidate line in the angles coverage matrix and, if it fills a cell the matrix needs, a concept brief with the inverse as the one idea and this table row as its competitor evidence.

## Output table template

Copy into the market map section 10 and into Part D of the interrogation.

| # | Convention (kind) | Count and ids | Literal inverse | Non-literal inverse | Is the inverse also a good idea? | Persona and stage | Mechanism (library file) | Member can truthfully do it? | Cheapest test and falsifier | Decision |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | | | | | | | | | | promote / reject: <reason> |
| 2 | | | | | | | | | | |
| 3 | | | | | | | | | | |
| 4 | | | | | | | | | | |
| 5 | | | | | | | | | | |

Every row is hypothetical until a readout exists. Label the table as such at the top: "All inversions below are hypotheses; none has been tested."

## Example row (fictional category and ads)

| # | Convention (kind) | Count and ids | Literal inverse | Non-literal inverse | Is the inverse also a good idea? | Persona and stage | Mechanism | Member can truthfully do it? | Cheapest test and falsifier | Decision |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | "Set up in minutes" (claim) | 9 of 12 advertisers; fict-001, fict-004, fict-007 and six more | "Set up takes a week" | "We set it up with you on a call; it takes an hour and you never touch the settings" | Yes for the persona who has already abandoned two tools during a rushed self-setup | p1, solution-aware | Satisficing (removes the fear of another failed setup); costly signaling (a human hour is a visible investment); pratfall (admits the category's "minutes" is not the real cost) | Yes: onboarding calls are already in the offer (offer.md, owner-provided) | One 15-second founder video: "every tool says minutes; here is what the first hour with us actually looks like." Falsifier: hook rate below the batch median after the impression floor | promote |

The example advertiser, ids, counts and persona are invented to show the form and must not be cited.
