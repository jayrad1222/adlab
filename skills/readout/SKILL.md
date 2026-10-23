---
name: readout
description: Read an Ads Manager CSV export after a test runs, compute hook rate, hold rate, CTR, CPA and frequency per ad, apply the decision rules against the member's thresholds, and say which rule fired and what to do next for each concept.
argument-hint: "<path/to/export.csv>"
allowed-tools: Bash(python3 -I ${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python3 -I "${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python -I ${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python -I "${CLAUDE_PLUGIN_ROOT}/tools/*), Read, Write, Edit
---
# /adlab:readout

**Purpose.** Close the loop with real numbers. Rules: `${CLAUDE_PLUGIN_ROOT}/library/finance/decision-rules.md`. Glossary: `${CLAUDE_PLUGIN_ROOT}/library/finance/signals-glossary.md`.

## Steps

1. The member exports from Ads Manager at the ad level with these columns if they can: ad name, amount spent, impressions, link clicks, 3-second video plays, ThruPlays, results, cost per result, frequency. Tell them once how to export (Ads Manager, Reports, ad level, the columns above, export CSV). Never ask for screenshots of the account.
2. Run `python3 -I "${CLAUDE_PLUGIN_ROOT}/tools/readout.py" --workspace <ws> --csv "$ARGUMENTS"`. It matches columns loosely and writes `plan/readouts/<date>.md`.
3. Explain each rule that fired in plain words, tied to the concept and persona, and what the next version is (new hook, new body, new offer, scale in steps, retire). Where a concept is "upstream only", say what number it needs to reach before a CPA verdict.
4. Update statuses in `bank/entries.jsonl` (testing, retired) and append the learning to `changelog.md`. Have the `librarian` append observed patterns (with ad ids) to `${CLAUDE_PLUGIN_ROOT}/library/observed/` only if the member agrees to share patterns from their own ads; default is no.
5. Mark the step done.

## Outputs

`plan/readouts/<date>.md`, updated statuses, changelog.

## Report

finished / doing now / next; one line per concept with the rule and the action.
