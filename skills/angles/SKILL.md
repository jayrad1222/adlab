---
name: angles
description: Build the coverage matrix (persona x awareness x angle family x proof x format) with rejected cells explained, run the opposite pass, and write eight to twelve genuinely distinct concept briefs with the critic's note on each.
argument-hint: "[--concepts 10]"
allowed-tools: Bash(python3 -I ${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python3 -I "${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python -I ${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python -I "${CLAUDE_PLUGIN_ROOT}/tools/*), Read, Write, Edit, Agent
---
# /adlab:angles

**Purpose.** The strategic unit is the angle. One working angle yields many hooks; one hook yields one ad. Distinct concepts beat variants (`${CLAUDE_PLUGIN_ROOT}/library/strategy/denney-concept-vs-iteration.md`, `.../andromeda-implications.md`). Families: `${CLAUDE_PLUGIN_ROOT}/library/copy/angle-families.md`. Brief schema: `${CLAUDE_PLUGIN_ROOT}/library/rubrics/concept-brief-schema.md`. Mark running.

## Steps

1. Read the personas, the market map, the interrogation and the asset catalog if it exists (`assets/catalog.md`; if not, proof is limited to what the brief and the site show, and say so).
2. **Coverage matrix** `concepts/matrix.md`: rows persona x awareness stage; columns angle family; each cell gets a proof type and a format or the word `rejected` with the reason (no proof available, policy risk, wrong stage for this persona, competitor saturation with the count). Mark the cells the market leaves open (from the uncontested claims and persona coverage sections).
3. **Opposite pass**: for the top five conventions in `analysis/conventions.md`, write the inverse and judge it (mechanism, persona, cheapest test); keep the ones with a mechanism.
4. **Concepts**: choose `--concepts` (default 10, range 8 to 12) distinct cells. Distinct means a different idea, not a different hook. Each gets `concepts/cNN-<slug>.md` per the schema: persona, awareness stage, angle family, the one idea, mechanism with library citations, competitor evidence (ids) and how this differs, proof available (with the claim-to-evidence ledger), formats planned, six hooks, the CTA, landing continuation, policy and truth risk flags, the CPA it must beat (blank until `/adlab:plan`), status `draft`. Include at least two "ugly" or native concepts and at least one from the opposite pass.
5. `critic` on every brief: pass, revise with reason, or block. Apply revisions; keep blocks blocked with the reason visible.
6. Mark done with the count.

## Outputs

`concepts/matrix.md`, `concepts/opposite-pass.md`, `concepts/cNN-<slug>.md`.

## Report

finished / doing now / next; list the concepts in one line each. Suggest `/adlab:bank`.
