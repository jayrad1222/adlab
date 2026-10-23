# Evidence integrity rules

## Purpose

These rules apply to everything Ad Lab writes: rubric rows, the market map, personas, the interrogation, concepts, bank entries, renders, plans and readouts. The `critic` agent enforces them and blocks anything that breaks one. They exist because the product's value is that a member can trust every line; one invented number spends that trust for the whole workspace.

Each rule below has a one-line example of a violation and the corrected wording.

Related: [`critic-checklist.md`](critic-checklist.md), [`per-ad-rubric.md`](per-ad-rubric.md), [`market-map-template.md`](market-map-template.md), [`editorial-score.md`](editorial-score.md), [`../platform/creator-category-truth-rules.md`](../platform/creator-category-truth-rules.md), [`../platform/ftc-endorsements.md`](../platform/ftc-endorsements.md), [`../prompts/house-style.md`](../prompts/house-style.md).

## The rules

1. **Observed, owner-provided, inferred and hypothetical are labeled separately.** Every statement about a customer, a competitor or a result carries one of the four labels, in the text or in the field's label.
   - Violation: "Customers in this category hate monthly fees."
   - Corrected: "Inferred: three of eight captured ads (ids m-101, m-114, m-120) lead with 'no monthly fee', which suggests fee resistance; no customer said this to us."

2. **No invented results.** A number describing an outcome (time saved, revenue, growth, conversion) appears only with a source the member can show.
   - Violation: "Save six hours a week."
   - Corrected: "Hypothetical: if the first-week workflow holds, the time saved is the member's own estimate of about six hours (owner-provided, unmeasured); do not run this line until a measured case exists."

3. **No invented testimonials.** A quote attributed to a customer must exist, with the person's consent recorded in the asset catalog.
   - Violation: "'This changed my business.' A happy member."
   - Corrected: "Language bank phrase from a public review dated 2026-08-03 (catalog row q-004, consent for advertising use: unknown, so not usable in an ad yet)."

4. **No invented member counts, audience sizes or social proof.** "Join 1,200 others" needs the count and its date from the member's own system.
   - Violation: "Trusted by hundreds of shops."
   - Corrected: "Owner-provided: 38 paying customers as of 2026-10-01 (catalog row n-002). The line can say 'used by 38 shops' or say nothing."

5. **No invented scarcity or urgency.** A deadline, a cap or a closing date must be real and the member must intend to enforce it.
   - Violation: "Only five spots left this month."
   - Corrected: "The member has not set a cap. Remove the scarcity line, or have the member set and document a real cap in `offer.md` before it is used."

6. **Longevity is not profitability.** An ad's days active says it kept running, not that it made money.
   - Violation: "Their best-performing ad has run for 212 days."
   - Corrected: "Their longest-running captured ad (id m-088) has been active 212 days as of 2026-10-20; whether it is profitable is unknown."

7. **Active-only samples cannot estimate survival.** A sample of currently active ads says nothing about how many ads were tried and killed, so it cannot yield a hit rate, a typical lifespan or a fatigue curve.
   - Violation: "Most of their ads last over 60 days."
   - Corrected: "Of the 31 active ads captured, 19 show more than 60 days active; killed ads are not in this sample, so no survival rate can be stated."

8. **Variants from one advertiser are not independent evidence.** Several versions of one concept from one page count as one observation of that concept.
   - Violation: "Seven ads use the founder-to-camera format, so it is the category standard."
   - Corrected: "Seven ads use founder-to-camera, but six are variants from one advertiser (ids m-030 to m-035); that is two advertisers using the format, not seven independent cases."

9. **Never say a video was watched if only the poster or the transcript was read.** `inspection_coverage` is the ceiling on every claim about an ad.
   - Violation: "The video opens on a before-and-after and ends with a guarantee."
   - Corrected: "Still-reviewed: the poster frame shows a split before-and-after layout; the ending was not inspected (video not watched)."

10. **A demonstration is not a deployment.** Showing something work in a demo, a test account or a screen recording is not the same as it running for a customer.
    - Violation: "The system handles their lead replies automatically."
    - Corrected: "The ad (id g-017) shows a screen recording of an automated reply in what appears to be a demo account; whether it is deployed for customers is unknown."

11. **Correlation is not causation.** Two things that co-occur in the sample (a format and long run time, a hook type and many variants) are a pattern to test, not a cause.
    - Violation: "Specific-number hooks work in this category because they dominate the leaderboard."
    - Corrected: "Specific-number hooks appear in six of the ten longest-running captured ads; that is a correlation in a small active-only sample and the hypothesis is worth a test, not a conclusion."

12. **Every borrowed pattern has a source and an observation distinct from the interpretation.** Say what was seen, where, and then separately what it is taken to mean.
    - Violation: "Competitors use the shoebox to trigger guilt."
    - Corrected: "Observed: a shoebox of receipts appears in the first two seconds of ids m-101 and m-114. Inferred: it is a concrete object the after-hours persona owns and may read as a guilt cue; that reading is the analyst's."

## Rules that follow from the twelve

13. **"Studies show" needs a named study.** A claimed research finding names the author, the work and the year, or it is cut. Contested findings are marked contested.
    - Violation: "Research shows people respond better to loss framing."
    - Corrected: "Kahneman and Tversky's prospect theory (1979) describes losses weighing more than equivalent gains; the size of the effect varies by context and some applications have failed to replicate, so treat it as a prior to test."

14. **Percentages from agency blogs are vendor claims.** Platform-behaviour numbers that are not from the platform's own documentation are labeled as the source's claim.
    - Violation: "Andromeda cut CPAs by 30% for consolidated accounts."
    - Corrected: "Several agency posts in October 2026 report CPA improvements from consolidated structures; the figures vary and are vendor claims, not Meta documentation. The direction is consensus; the size is not."

15. **An editorial score is a priority, never a performance claim.** See `editorial-score.md`.
    - Violation: "Entry b014 is our strongest ad (score 11)."
    - Corrected: "Entry b014 scored 11 of 12 on the editorial rubric, so it is first in the recording queue; no performance data exists yet."

16. **Unknown stays unknown.** Blank data is not zero, a missing baseline is not a baseline, and ambiguity goes in an unknown category rather than a favourable one.
    - Violation: "Trial-to-paid: 0% (no data yet)."
    - Corrected: "Trial-to-paid: unknown; no trials have run. The worked example uses a labeled placeholder."

## How the critic applies them

For each item reviewed, the critic names the rule number, quotes the offending line, and gives the corrected wording or the reason it cannot be corrected. A rule 2, 3, 4, 5 or 9 breach is a block. The others are a revise unless the breach is load-bearing for the recommendation, in which case it is also a block. The critic never fixes the line silently; the author fixes it and the change goes in the changelog.
