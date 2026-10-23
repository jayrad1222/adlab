# Concept brief schema (`concepts/cNN-<slug>.md`)

## Purpose

A concept is one idea for one persona at one awareness stage. It is the unit Meta's ranking rewards (a distinct concept, not another variant) and the unit the test plan budgets. The `angles` step writes eight to twelve per round; the `bank` step expands each into copy, scripts and layouts; the `critic` reviews each; the `plan` step fills the CPA. A concept with a field left blank is `draft`, not `ready`.

Related: [`persona-schema.md`](persona-schema.md), [`bank-entry-schema.md`](bank-entry-schema.md), [`asset-catalog-schema.md`](asset-catalog-schema.md), [`critic-checklist.md`](critic-checklist.md), [`../strategy/denney-concept-vs-iteration.md`](../strategy/denney-concept-vs-iteration.md), [`../strategy/andromeda-implications.md`](../strategy/andromeda-implications.md), [`../copy/angle-families.md`](../copy/angle-families.md), [`../copy/hook-taxonomy.md`](../copy/hook-taxonomy.md), [`../finance/decision-rules.md`](../finance/decision-rules.md).

Copy everything below the line into `concepts/cNN-<slug>.md` and replace the italic instructions. Fields appear in this order. The file opens with a short frontmatter block, because `tools/export.py` reads `concept_id` and `name` from it to label the board, and `/adlab:plan` fills `cpa_to_beat` there and in the section of the same name.

---

```
---
concept_id: cNN
name: <the slug as words>
persona: pN
awareness: <unaware | problem | solution | product | most>
angle_family: <slug>
status: draft
version: 1
cpa_to_beat:
---
```

# cNN: <slug as a short idea, not a format>

Status: draft. Version 1, <YYYY-MM-DD>.

## Persona

*The persona file this concept serves (`personas/pN-<slug>.md`). One persona. If the idea serves two, write two concepts and note the sibling.*

## Awareness stage

*One of unaware, problem, solution, product, most. State why this stage: which cell of the coverage matrix the concept fills and whether that cell was empty, thin or crowded in the market map.*

## Angle family

*One slug from `../copy/angle-families.md`. If `cost-of-inaction`, the policy flag below is mandatory.*

## The one idea

*One sentence a stranger could repeat. Not a hook, not a format: the idea the hooks and formats will carry. Test: if the sentence could sit on a competitor's brief unchanged, it is not an idea yet.*

## The mechanism

*Why this idea should move this persona, citing the library files by relative path (for example `../psychology/satisficing.md`, `../sales/voss-toolkit.md`). Name the psychological job (what the viewer must feel is true before the rational case lands) and the copy move. A mechanism is not "it is relatable"; it is the named effect and the cue that triggers it.*

## Competitor evidence and the difference

*Ad ids from `analysis/ads.csv` that are nearest to this idea, what they do, and the specific difference in ours (a different persona, a different stage, a proof they lack, an inversion from the opposite pass). If no competitor ad is near, say which market-map section shows the gap. Never copy a competitor's wording.*

## Proof available

*From `assets/catalog.md` only. For each claim the concept will make, the asset that supports it and what the asset can and cannot prove. This is the claim-to-evidence ledger; the critic checks it line by line.*

| Claim the concept makes | Asset (catalog row) | What it proves | What it cannot prove | Label |
|---|---|---|---|---|
| | | | | observed / owner-provided / inferred / hypothetical |

*A claim with no asset either becomes a hypothesis stated as one, or is cut.*

## Formats planned

*Two to four formats from `../copy/format-taxonomy.md`, with aspect ratios and the reason each suits the persona's T-E-E-P stage. At least one native or ugly format across the round's concepts.*

## Six hooks

*Six hooks, each tagged with its hook type from `../copy/hook-taxonomy.md`, each written for the first three seconds or the largest text on the static. Each must pass Harry Dry's three tests (visualize, falsify, nobody else could say it). Vary the type; six hooks of one type is iteration, not coverage.*

1. (`hook-type`)
2. (`hook-type`)
3. (`hook-type`)
4. (`hook-type`)
5. (`hook-type`)
6. (`hook-type`)

## The CTA

*The button text and the spoken or written call to action, matched to the awareness stage (a most-aware CTA on a problem-aware concept is a continuity break). See `../copy/cta-patterns.md`.*

## Landing continuation

*Where the click goes and how the first screen repeats the ad's promise and persona. If the landing page does not yet exist or does not match, say so; the concept cannot be `ready` with a `broken` continuation.*

## Policy and truth risk flags

*Every flag from `../platform/meta-policy-pitfalls.md`, `../platform/ftc-endorsements.md` and `../platform/creator-category-truth-rules.md` that could apply, with the line that triggers it and the fix. Write `none identified` only after checking each file.*

## The critic's note

*Written by the `critic` agent only. Pass, revise with reason, or block with reason, per item in `critic-checklist.md`. The copywriter and creative director do not edit this section; they respond under it with a dated reply.*

## The CPA it must beat

*Left blank until the `plan` step fills it from `plan/economics.md`. When filled: the target CPA, the breakeven CPA, the formula reference, and the test budget per concept. Numbers here come only from the member's `finance.md`.*

## Status

*One of: draft (fields missing or critic not run), ready (all fields filled, critic passed or revisions applied), testing (live in a test per the plan), retired (killed per decision rules or superseded; keep the file and say why).*
