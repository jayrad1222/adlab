---
name: analyze
description: "Decode every pulled ad with the per-ad rubric (subagents in batches), then write the market map: sophistication stage, table-stakes and uncontested claims, persona coverage, proof arms race, price map, format gaps, longevity leaderboard with caveats, conventions worth inverting, ten hypotheses, evidence limits."
argument-hint: "[--batch 15] [--only <advertiser-slug>]"
allowed-tools: Bash(python3 -I ${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python3 -I "${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python -I ${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python -I "${CLAUDE_PLUGIN_ROOT}/tools/*), Read, Write, Edit, Agent
---
# /adlab:analyze

**Purpose.** The decode. Unattended; the longest step (budget an hour for 200 ads). Rubric: the preloaded `rubric` skill and `${CLAUDE_PLUGIN_ROOT}/library/rubrics/per-ad-rubric.md`. Market map template: `${CLAUDE_PLUGIN_ROOT}/library/rubrics/market-map-template.md`. Sophistication procedure: `${CLAUDE_PLUGIN_ROOT}/library/strategy/schwartz-market-sophistication.md`. Mark running.

## Steps

1. List ads from `ads/ads.jsonl`. Separate `match` values: `advertiser-page` and `cobrand` are roster ads; `keyword-neighbor` and `_discovery` ads are attention competitors; `manual` stubs need reading first. Skip nothing, but tag the group.
2. **Per-ad rubric** via the `ad-analyst` agent, batches of `--batch` ads (default 15), each batch given the ad ids and told to read each `ad.md`, card and frames, and to return one CSV row per ad with the header from the rubric. Collect into `analysis/ads.csv` (write the header once; append rows; dedupe on ad_id). Spot-check two rows per batch yourself against the source; send a batch back if `inspection_coverage` is inflated or fields are filled without evidence.
3. **Per-advertiser notes** `analysis/competitor-<slug>.md` (you, not a subagent): how many ads, the angles they run, their dominant proof, their price signal, their distinctive assets or lack of them, their landing pattern, the oldest ads and what they have in common (a clue, not a verdict), two things to adapt and one to avoid, with ad ids.
4. **The market map** `analysis/market-map.md` from the template, every section, with ad ids behind every claim; call the sophistication stage with the procedure and name the required move; the longevity leaderboard prints the caveats; the "conventions worth inverting" section feeds `/adlab:angles`; the evidence-limits section says what was not inspected (videos without frames, capped counts, zero-return searches). Count advertisers, not ads, when you say "the market does X".
5. Persona coverage: which buying situations the ads talk to (from `persona_inferred`), who is ignored, who is overserved. This seeds `/adlab:personas`.
6. Mark done with the row count.

## Outputs

`analysis/ads.csv`, `analysis/competitor-<slug>.md` (one per roster advertiser), `analysis/market-map.md`, `analysis/conventions.md` (the inversion candidates, extracted).

## Report

finished / doing now / next, with the sophistication stage in one line and the three biggest white-space findings; suggest `/adlab:personas`.
