---
name: bank
description: "Produce the ad bank from the concept briefs: copy at three lengths, headlines, descriptions, six hooks, 15/30/60 second scripts with shot lists, static layout choices, carousel cards, UGC briefs and landing notes per concept; the critic reviews every entry; export the board (bank/ad-bank.html) and the CSV."
argument-hint: "[--only c03] [--formats static,video]"
allowed-tools: Bash(python3 -I ${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python3 -I "${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python -I ${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python -I "${CLAUDE_PLUGIN_ROOT}/tools/*), Read, Write, Edit, Agent
---
# /adlab:bank

**Purpose.** Evidence-backed copy with the reasoning shown. Entry schema: `${CLAUDE_PLUGIN_ROOT}/library/rubrics/bank-entry-schema.md`. Tests every line must pass: `${CLAUDE_PLUGIN_ROOT}/library/copy/harry-dry-three-tests.md`. Formats: `${CLAUDE_PLUGIN_ROOT}/library/copy/format-taxonomy.md`. Editorial score: `${CLAUDE_PLUGIN_ROOT}/library/rubrics/editorial-score.md`. Mark running.

## Steps

1. For each concept brief (or `--only`), the `copywriter` agent writes: primary text in three lengths (under 125 characters, about 300, long), five headlines (under 40 characters), two descriptions, six hooks (from the brief, tightened), the CTA, and the landing continuation note. The `creative-director` agent writes per concept: a 15, 30 and 60 second script with shot list and on-screen text; the static layout choice (a template under `${CLAUDE_PLUGIN_ROOT}/templates/` and the field values); carousel cards when the concept suits; a UGC brief from `${CLAUDE_PLUGIN_ROOT}/library/copy/ugc-brief-structure.md`. Every claim maps to proof in `assets/catalog.md` or the brief; otherwise it is cut.
2. Write entries to `bank/entries.jsonl`, one JSON object per entry with the schema fields plus `hooks` (list), `competitor_refs` (list of ad ids), `risk_flags` (list), `renders` (empty list until render), `script` (for video entries), `layout_template` and `layout_fields` (for statics). `why_it_should_work` names the mechanism (library file), the persona and the evidence ids. Briefs per concept also go to `bank/briefs/cNN.md` for humans.
3. `critic` on every entry: the three tests, the two-second stranger test, policy flags, the claim-to-evidence check. Write its note into `critic_note`; set `status` to `ready` only on pass. Score with the editorial rubric; the score is a priority, never a prediction.
4. Export: `python3 -I "${CLAUDE_PLUGIN_ROOT}/tools/export.py" --workspace <ws>` builds `bank/ad-bank.html` and `bank/ad-bank.csv`. Open the board path for the member.
5. Mark done with the entry count and the ready count.

## Outputs

`bank/entries.jsonl`, `bank/briefs/cNN.md`, `bank/ad-bank.html`, `bank/ad-bank.csv`.

## Report

finished / doing now / next; entries ready versus needing revision. Suggest `/adlab:assets` if the catalog is empty, else `/adlab:render` or `/adlab:plan`.
