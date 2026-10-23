---
name: review
description: "Run the critic's whole-run review of a workspace before anything goes live: the interrogation, every concept, every bank entry and its renders, the test plan, and a scan of every ad line for numbers, prices, guarantees, counts, urgency and competitor names. Writes analysis/critic-report.md; run it again after fixes to add a re-review."
argument-hint: "[--workspace <path>] [--client <name>]"
allowed-tools: Bash(python3 -I ${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python3 -I "${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python -I ${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python -I "${CLAUDE_PLUGIN_ROOT}/tools/*), Read, Write, Agent
---
# /adlab:review

**Purpose.** The check before a member or a client runs anything. The `critic` agent reads everything that would reach an ad, checks every claim against its source, and returns one report the member can act on. Nothing in the run is edited: fixes go back to the step that made the item, and this command runs again. Truth rules: the preloaded `evidence-rules` and `${CLAUDE_PLUGIN_ROOT}/library/rubrics/evidence-integrity.md`. Checklist: `${CLAUDE_PLUGIN_ROOT}/library/rubrics/critic-checklist.md`. Report format: `${CLAUDE_PLUGIN_ROOT}/skills/review/report-format.md`.

## Workspace

`--workspace <path>` reviews any folder, for example a client's workspace or one of the plugin's `examples/`. `--client <name>` uses `./adlab-workspace/clients/<slug>`. Otherwise use `./adlab-workspace/ACTIVE_CLIENT` if it exists, else `./adlab-workspace`. If `bank/entries.jsonl` is missing, stop and say so: the review needs a bank (`/adlab:bank` first). Mark running: `python3 -I "${CLAUDE_PLUGIN_ROOT}/tools/progress.py" --workspace <ws> set --step review --status running`.

## Steps

1. **Scan.** `python3 -I "${CLAUDE_PLUGIN_ROOT}/tools/scan.py" --workspace <ws>` writes `analysis/scan.md`: every distinct line of ad copy or on-image text with a number, a price, a guarantee, an income or results word, a count or rating, scarcity or urgency, a superlative, "free" or a discount, a quote, or a competitor's name, with the entries that carry it. Lines from ready entries come first.
2. **Standing rules.** Read `business/brief.md`, `business/offer.md` and `business/interrogation-answers.md` for the rules this business holds (what it never promises, who must consent before appearing, what it never claims). Quote each with its file. These go to the critic with the truth rules.
3. **First review or re-review.** If `analysis/critic-report.md` does not exist, ask for a first review. If it does, ask for a re-review: every item the report or its last re-review left open, plus anything changed since its date (bank entries with a higher `version`, files edited since).
4. **The critic.** Give the `critic` agent: the workspace path, `report-format.md`, `analysis/scan.md`, the standing rules, and the scope: `business/interrogation.md` if present (re-check its earlier critic note item by item); every `concepts/c*.md` with its critic note and author's reply, plus `concepts/matrix.md` and `concepts/opposite-pass.md`; every line of `bank/entries.jsonl` with its `critic_note`, `status`, `risk_flags`, copy fields, layout or script file, and the PNGs in its `renders` (open them); `plan/test-plan.md` and `plan/thresholds.json`; the scan. Tell it to verify every claim against the captured pages under `business/site/`, the business files, `assets/catalog.md` and `analysis/ads.csv`; to edit nothing; and to return the whole report (or the re-review section) as text in the format given. With more than about 40 bank entries, give the bank to two critic agents split by concept, then merge their tables under one verdict.
5. **Write it.** First review: write the critic's text to `analysis/critic-report.md` unchanged. Re-review: append the section to the end of the file unchanged. The critic does not write files; you do, word for word.
6. **Change nothing else.** Statuses, copy and notes stay as they are. Each revise or block names where its fix belongs (`/adlab:bank` for an entry, `/adlab:angles` for a brief, `/adlab:plan` for the plan, the member for an asset, consent, a landing page or a decision).
7. Mark done: `progress.py ... set --step review --status done --note "<overall verdict>; <n> open blocks; <n> revise items"`.

## Outputs

`analysis/scan.md`, `analysis/critic-report.md`.

## Report

finished / doing now / next. One line with the overall verdict and whether any invented proof was found (name it if so). Open blocks by kind (asset, consent, landing page, owner decision). One-line asks for what only the member or the client can do. For each revise item, the command that fixes it, and: run `/adlab:review` again after the fixes.
