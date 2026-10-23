---
name: evidence-rules
description: Internal. The evidence-integrity rules every Ad Lab output follows. Preloaded into the critic, psychologist, copywriter and persona-builder agents; not a command.
user-invocable: false
---
# Evidence integrity (internal)

Full reference: `${CLAUDE_PLUGIN_ROOT}/library/rubrics/evidence-integrity.md`. Critic checklist: `${CLAUDE_PLUGIN_ROOT}/library/rubrics/critic-checklist.md`.

1. Label every claim: **observed** (seen in an ad, a page, a file), **owner-provided** (the member said it), **inferred** (your read, with the evidence it rests on), **hypothetical** (a guess to test).
2. Never invent results, testimonials, member counts, revenue, savings, scarcity or urgency. If the asset catalog has no proof for a claim, the claim does not go in an ad.
3. Longevity is not profitability. An ad running 200 days is a clue, not a verdict. Say "has run N days" and nothing more.
4. Active-only samples cannot estimate survival or win rates. Do not compute "X% of ads last 60 days" from an active-only pull.
5. Variants from one advertiser are not independent evidence. Count advertisers, not ads, when you say "the market does X".
6. Never say a video was watched when only its poster or transcript was read. Use the inspection_coverage field honestly.
7. A demonstration is not a deployment; a prototype is not a result; deposits are not profit; business spend is not ad spend.
8. Correlation is not causation. "Advertisers who do X run longer" is an observation, not a recommendation, until a mechanism explains it.
9. Every borrowed pattern names its source (ad ids) and separates the observation from your interpretation.
10. Editorial scores are recording priorities, never performance claims. Nothing is a "winner" until a readout says so.
11. Agency and vendor percentages are claims, not benchmarks. Name them as such.
12. Unknown stays unknown. Do not fill a field to make a table look complete.

The critic writes notes (pass, revise with reason, block with reason). The critic never edits silently.
