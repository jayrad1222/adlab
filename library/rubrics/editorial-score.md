# Editorial score

## Purpose

A quick, repeatable way to decide which bank entries to render and test first. Adapted from the Operators Workshop improvement system, with the sixth dimension changed from community fit to fit with the offer so it applies to any member's business.

An editorial score is a recording priority and never a performance claim. It says "make this one first". It does not say "this one will convert", and it is not a forecast, a causal test or a probability.

Score the hook plus its planned first visual and its payoff together, not the hook alone. Two reviewers (two agents, or the critic and the member) score independently; disagreements are resolved by checking the asset and the evidence, not by averaging. A false claim with a high score is still a false claim.

Related: [`bank-entry-schema.md`](bank-entry-schema.md), [`two-second-stranger-test.md`](two-second-stranger-test.md), [`critic-checklist.md`](critic-checklist.md), [`../copy/harry-dry-three-tests.md`](../copy/harry-dry-three-tests.md), [`evidence-integrity.md`](evidence-integrity.md).

## The six dimensions (0, 1 or 2 each)

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Recognizable situation | No understandable situation; the viewer cannot tell who this is about | A broad interest or a general problem ("busy owners") | A specific person recognizes a task, a moment or a decision they have actually had ("matching receipts at 11pm") |
| Specificity | An abstract promise ("grow faster", "take control") | Names a topic or a category ("bookkeeping", "launches") | Names an object, an action, a number with a source, or a comparison ("the shoebox", "one receipt photographed", "two tools versus one") |
| Curiosity with a payoff | Empty intrigue; a tease the body never answers | A question with a loose or vague answer | A clear question the ad or the landing page answers, and the viewer can tell that it will |
| Visual fit | No supporting visual, or stock imagery unrelated to the line | A relevant but generic visual (a laptop, a smiling person) | The first visual directly demonstrates the opening line (the object, the moment, the demo) |
| Credibility | An unsupported assertion; a number with no source; a claim the member cannot back | A plausible explanation that needs qualification or a proof the catalog partly supports | A demonstrable example or a properly documented case from the asset catalog, with consent cleared |
| Fit with the offer | Implies the wrong product, outcome or service; attracts the poor-fit persona | Related to the offer but the bridge to it is weak or late | The ad's promise is the offer's actual promise, for the persona the offer serves, at the right awareness stage |

Total is 0 to 12.

## Triage bands

| Total | Band | What happens |
|---|---|---|
| 10 to 12 | Shortlist | Render and include in the first test batch, subject to the critic's pass |
| 7 to 9 | Revise or reserve | Fix the lowest dimension and rescore, or hold for a later batch |
| 0 to 6 | Rebuild | Return to the concept brief; the idea or the proof is not there yet |

The cutoffs organize work. They are not externally validated and do not predict results.

## Overrides that ignore the score

- Any unsupported claim, unverified testimonial, unverified scarcity or urgency, or policy flag blocks the entry whatever it scores. The critic's block stands until fixed.
- An entry whose proof depends on a case or asset that does not yet exist stays on hold until it exists, whatever it scores.
- An entry that fails the two-second stranger test is capped at the "revise" band until the first visual or the hook is fixed.
- A hook that fails Harry Dry's three tests is rewritten before scoring.

## How to record it

Write the six numbers and the total in the bank entry's `editorial_score` column as the total, and the per-dimension scores with the reviewer's initials or agent name in the entry's changelog line, for example `2026-10-22 scored 2/2/1/2/1/2 = 10 (critic); 2/1/1/2/1/2 = 9 (member)`. When reviewers differ by two or more on one dimension, the critic checks the evidence and records which score stood and why.

After a readout exists, never relabel an editorial score as a result. A measured winner is a separate label, used only for a defined comparison with real data and its stated limitations (see `../finance/decision-rules.md`).
