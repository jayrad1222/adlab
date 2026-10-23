# Critic checklist

## Purpose

The ordered pass the `critic` agent runs on every concept brief and every bank entry before status can move from `draft` to `ready`, and again on the two example banks before release. The critic writes notes; it never edits the item. The author (copywriter, creative director, psychologist or persona builder) makes the change and records it in the changelog, and the critic re-runs the failed items.

Run the items in this order. Stop at the first block only if the fix would change everything downstream (a false core claim); otherwise finish the pass so the author gets every note at once.

Related: [`evidence-integrity.md`](evidence-integrity.md), [`two-second-stranger-test.md`](two-second-stranger-test.md), [`editorial-score.md`](editorial-score.md), [`asset-catalog-schema.md`](asset-catalog-schema.md), [`../platform/meta-policy-pitfalls.md`](../platform/meta-policy-pitfalls.md), [`../platform/ftc-endorsements.md`](../platform/ftc-endorsements.md), [`../platform/creator-category-truth-rules.md`](../platform/creator-category-truth-rules.md), [`../copy/harry-dry-three-tests.md`](../copy/harry-dry-three-tests.md), [`../psychology/berger-stepps.md`](../psychology/berger-stepps.md), [`../psychology/heath-success.md`](../psychology/heath-success.md).

## The checklist

### 1. Truth labels

For every factual statement in the item (about the customer, the competitor, the member's business, a result): is it labeled observed, owner-provided, inferred or hypothetical, and is the label right? Check the `why_it_should_work` field, the mechanism section and every number. Apply `evidence-integrity.md` rules 1 to 16 and name the rule number in the note.

Block if: any invented result, testimonial, count, scarcity or urgency (rules 2 to 5); any claim that a video was watched when it was not (rule 9).

### 2. Policy flags

Read the copy, the hook, the on-screen text plan and the visual description against [`../platform/meta-policy-pitfalls.md`](../platform/meta-policy-pitfalls.md), [`../platform/ftc-endorsements.md`](../platform/ftc-endorsements.md) and [`../platform/creator-category-truth-rules.md`](../platform/creator-category-truth-rules.md). Look specifically for:

- second-person personal attributes ("are you struggling with your weight", "if you're depressed", "as a single mum")
- before-and-after imagery in health, body or financial contexts
- income, earnings or results claims, including implied ones ("replace your salary", "clients are booking out")
- sensational, fear-first or shaming language and imagery
- endorsements or testimonials without a real person, consent and, where needed, a disclosure
- undisclosed generated media where the platform requires disclosure
- a scripted founder presented as a customer; a demo presented as a deployed system; deposits presented as profit; business spend presented as ad spend

Note each flag with the line that triggers it and the `risk_flags` value it maps to. Block on any flag the member cannot remove without changing the idea; revise otherwise.

### 3. Cliché and generic-claim detection

Read every line and ask whether a competitor could run it unchanged. Flag:

- hype words and empty intensifiers (see the list in [`../prompts/house-style.md`](../prompts/house-style.md))
- category clichés the market map lists as table stakes, used without a twist
- promises with no object ("transform", "unlock", "take control", "level up")
- "we" sentences about the member instead of "you" sentences about the persona
- a reason-why that is a feature list rather than a mechanism
- any line that appears in a captured competitor ad in the same or nearly the same words (quote the id)

Revise on each; block if the hook itself is generic, because a generic hook makes the rest unreachable.

### 4. Harry Dry's three tests

On every hook and headline, and on the first line of primary text: can you visualize it; can you falsify it; could nobody else say it? Record pass or fail per test per line. A line that fails all three is deleted, not revised. A line that fails one is revised with the failing test named. See [`../copy/harry-dry-three-tests.md`](../copy/harry-dry-three-tests.md).

### 5. The two-second stranger test

Run [`two-second-stranger-test.md`](two-second-stranger-test.md) on each planned format: the static at phone size, and the first three seconds of each video script with its first visual. Record who the stranger would think it is for and what it is about, in the stranger's words, and whether those match the persona and the one idea. Fail caps the editorial band at "revise".

### 6. Claim-to-evidence check against the asset catalog

Open the concept's claim-to-evidence ledger and the entry's `asset_refs`. For every claim: does the catalog row exist, is its status `cleared`, does "what it can prove" cover the claim as written, and is consent `granted` or `not-applicable` for everyone in it? A claim that outruns its asset is rewritten down to what the asset proves or labeled hypothetical. A number with no catalog row is `unsourced-number` and blocks. An asset with permissions `unknown` or `declined` blocks.

### 7. Continuity and fit

Does the CTA match the awareness stage? Does the landing continuation repeat the promise and the persona (strong), or does it break? Does the format suit the persona's T-E-E-P stage as the persona file states? Does the entry's persona equal the concept's persona? Revise on mismatch; block on a `broken` landing.

### 8. Stickiness and spread (advisory)

Run Berger's STEPPS and the Heaths' SUCCESs as a quick scan: is there social currency, a trigger, a high-arousal emotion, visible use, practical value, a story; is it simple, unexpected, concrete, credible, emotional, a story? These are notes to strengthen the item, not grounds to block.

### 9. Editorial score

If items 1 to 7 produced no block, score the item per [`editorial-score.md`](editorial-score.md) and record the six numbers and the total in the changelog line. Say in the note that the score is a recording priority.

## Output format

One note per checklist item, in order, in the item's `critic_note` field (bank entry) or "The critic's note" section (concept). Each note is one of:

- `PASS` with nothing else, or a short reason if the pass was close.
- `REVISE: <reason>` with the line quoted, the rule or test that failed, and what a passing version would need to contain (not the rewrite itself).
- `BLOCK: <reason>` with the line quoted, the rule or flag, and what must be true before the item can be re-reviewed.

Then a closing line: `Overall: pass | revise | block. Editorial score: <n>/12 or unscored. Reviewed <date> by critic.`

The critic never edits the copy, the hook, the script or the layout. If the critic can see the fix, it describes the fix in the note. If the author disagrees, the author writes a dated reply under the note and the critic re-reviews; the disagreement stays in the file.

## Example note (fictional entry)

```
1 Truth labels: REVISE. "Most owners save six hours a week" (primary_text_long) has no source; rule 2. A passing version states the member's own estimate as owner-provided and unmeasured, or drops the number.
2 Policy: PASS.
3 Cliché: REVISE. "Take control of your books" (headline) is table stakes per market-map section 3 (ids m-101, m-114, m-120). Needs an object the persona owns.
4 Three tests: hook PASS/PASS/PASS. Headline FAIL visualize, FAIL nobody-else. Rewrite required.
5 Stranger test: PASS. Stranger read "someone who does their own receipts at night; some kind of bookkeeping thing". Matches p1.
6 Claim-to-evidence: BLOCK. asset_refs lists ph-012 whose permissions are unknown (a second person at the table). Needs consent granted or a crop that removes them, re-cataloged.
7 Continuity: PASS.
8 STEPPS/SUCCESs: concrete and practical; no trigger. Consider a weekday-evening trigger in the body.
9 Editorial score: unscored (block on 6).
Overall: block. Editorial score: unscored. Reviewed 2026-10-22 by critic.
```
