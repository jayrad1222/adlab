---
name: interrogate
description: "Run the Sutherland-style interrogation of the business, grounded in the decode: diagnose which problem it really is (perception, trust, category, status, context, price signal, social proof, ritual, legibility), seven recommendations with mechanism, evidence, cheapest test and falsifier, three moonshots, and the opposite pass on the top five conventions."
allowed-tools: Bash(python3 -I ${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python3 -I "${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python -I ${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python -I "${CLAUDE_PLUGIN_ROOT}/tools/*), Read, Write, Agent
---
# /adlab:interrogate

**Purpose.** The grilling, with receipts. Prompt: `${CLAUDE_PLUGIN_ROOT}/library/prompts/interrogation.md` (the member's original stance plus the grounding rule and output schema). Opposite pass: `${CLAUDE_PLUGIN_ROOT}/library/prompts/opposite-pass.md`. Mark running.

## Steps

1. Give the `psychologist` agent: the interrogation prompt, `business/brief.md`, `offer.md`, `finance.md`, `interrogation-answers.md`, `analysis/market-map.md`, `analysis/conventions.md`, and every `personas/pN-*.md`. Tell it that every challenge must cite ad ids or persona files, that ruthless is fine and invented is not, and that the output schema is fixed.
2. Receive and check: nine-problem diagnosis in order with evidence; exactly seven recommendations, each with mechanism (a library file), evidence (ids), cheapest test, falsifier, risk; three psychological moonshots; the opposite pass table on the top five conventions from the market map. Send it back if a recommendation has no falsifier or no evidence.
3. Run the `critic` on the result for invented facts and policy risk. Attach its notes.
4. Write `business/interrogation.md`. Mark done.

## Outputs

`business/interrogation.md`.

## Report

finished / doing now / next; name the diagnosed problem in one line. Suggest `/adlab:angles`.
