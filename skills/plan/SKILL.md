---
name: plan
description: "Turn finance.md into the economics every concept must beat (breakeven and target CPA, test budget per concept) and write the test plan: one broad ad set, six to twelve concepts, three to six hooks each, the reading order of signals, the decision rules and the refresh cadence. A hypothesis-testing plan, not a forecast."
allowed-tools: Bash(python3 -I ${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python3 -I "${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python -I ${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python -I "${CLAUDE_PLUGIN_ROOT}/tools/*), Read, Write, Edit, Agent
---
# /adlab:plan

**Purpose.** Money gates the creative. Formulas: `${CLAUDE_PLUGIN_ROOT}/library/finance/formulas.md`. Rules: `${CLAUDE_PLUGIN_ROOT}/library/finance/decision-rules.md`. Mark running.

## Steps

1. Check `business/finance.md`. Any placeholder left? Ask for the three that matter most (price, gross margin, and either trial-to-paid plus months retained, or AOV) in one message with defaults; proceed with placeholders if the member says so, and label the outputs placeholder.
2. Run `python3 -I "${CLAUDE_PLUGIN_ROOT}/tools/finance.py" --workspace <ws>`; it writes `plan/economics.md` with every formula and the numbers that went in.
3. The `finance-analyst` agent writes `plan/test-plan.md`: the primary event; breakeven and target CPA (or cost per trial start); test budget per concept and how many concepts the monthly budget can carry to a verdict; the structure (one campaign, one broad ad set, the ready concepts from the bank, three to six hooks each, no interest stacking); what to read first (hook rate, hold rate, CTR, then CPA at volume); the decision rules as if-then with the member's thresholds; a refresh cadence in weeks; what would make this plan wrong. Write `plan/thresholds.json` with the starting thresholds (marked starting points) and `target_cpa` from economics. Use the keys `tools/readout.py` reads: `impression_floor`, `min_hook_rate`, `min_hold_rate`, `min_ctr`, `max_frequency`, `judge_after_conversions`, `target_cpa`, `kill_cpa_multiple`; a threshold the member has not set is `null`, and the readout skips that rule and says so.
4. Fill `cpa_to_beat` in every concept brief and `bank/briefs/*.md` from economics; set it in `bank/entries.jsonl` as `cpa_to_beat`. Re-export the board.
5. Mark done.

## Outputs

`plan/economics.md`, `plan/test-plan.md`, `plan/thresholds.json`; updated concepts and bank.

## Report

finished / doing now / next with the target CPA in one line and the number of concepts the budget can judge. Suggest `/adlab:review` before any ad goes live. Say what to do after the first week: export the Ads Manager report and run `/adlab:readout`.
