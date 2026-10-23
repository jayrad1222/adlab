---
name: personas
description: Build three to seven buying-situation personas from the brief, the interrogation answers, the competitor targeting evidence in analysis/ads.csv, mined customer language and the member's own customers; the member reviews and the files are revised with versions kept.
argument-hint: "[--count 5] [--revise p2 \"note\"]"
allowed-tools: Bash(python3 -I ${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python3 -I "${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python -I ${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python -I "${CLAUDE_PLUGIN_ROOT}/tools/*), Read, Write, Edit, WebFetch, WebSearch, Agent
---
# /adlab:personas

**Purpose.** Personas as situations, not demographics. Schema: `${CLAUDE_PLUGIN_ROOT}/library/rubrics/persona-schema.md`. Forces: `${CLAUDE_PLUGIN_ROOT}/library/psychology/jtbd-four-forces.md`. Formats by stage: `${CLAUDE_PLUGIN_ROOT}/library/strategy/levinger-three-realities-teep.md`. Mark running.

## Steps

1. Gather the evidence: `business/brief.md`, `business/interrogation-answers.md` (the five customers), `analysis/market-map.md` (persona coverage section), `analysis/ads.csv` (`persona_inferred` and `persona_evidence` columns, grouped), and customer language. For language, have the `researcher` agent mine reviews, comments, community threads and the competitor landing pages already captured under `ads/*/*/landing/page.txt`; collect verbatim phrases with source and date. Never invent quotes.
2. Draft candidates with the `persona-builder` agent: it proposes 3 to 7 situations, each with the schema filled, every field labeled observed / owner-provided / inferred / hypothetical, a language bank of real phrases, and the list of competitor ads that already speak to it (ids) and what nobody says to it yet.
3. Challenge overlaps: merge two personas when their push, anxiety and objections are the same; split when the proof they need differs. Write `personas/pN-<slug>.md` (frontmatter: `id`, `name`, `version`, `status`) and `personas/coverage.md` (a table: persona x competitor coverage x awareness distribution x proof needed).
4. **Member review.** Show the names and one line each. Ask: "Which of these is wrong, missing, or someone you would not sell to?" Apply `--revise pN "note"` by writing a new version (`version: 2`) and keeping the old file as `pN-<slug>.v1.md`. Note revisions in the changelog.
5. Mark done with the count.

## Outputs

`personas/pN-<slug>.md`, `personas/coverage.md`.

## Report

finished / doing now / next; one-line ask: the review. Suggest `/adlab:interrogate`.
