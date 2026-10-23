---
name: refresh
description: Re-pull the roster, diff against the last pull (new ads, ads that stopped, ads crossing 30, 60 and 90 days, new advertisers using the category's language), and append the findings to changelog.md and analysis/refresh-<date>.md.
argument-hint: "[--max 40]"
disable-model-invocation: true
allowed-tools: Bash(python3 -I ${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python3 -I "${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python -I ${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python -I "${CLAUDE_PLUGIN_ROOT}/tools/*), Read, Write, Edit
---
# /adlab:refresh

**Purpose.** The market moves; see what moved. 20 to 60 minutes unattended. Mark running.

## Steps

1. Snapshot the current `ads/ads.jsonl` to `ads/_snapshots/<date>.jsonl`.
2. Run the Meta pull again with the same plan plus `--include-inactive` so stopped ads show: `python3 -I "${CLAUDE_PLUGIN_ROOT}/tools/run.py" meta_pull --plan <ws>/ads/plan.json --out <ws>/ads --include-inactive --max-per-advertiser <max>` (background). Run the other sources used last time.
3. Diff by ad id: new ads (first_seen after the snapshot), ads now `is_active: false`, ads whose `days_active` crossed 30, 60 or 90 since the snapshot, and advertisers in the discovery keyword searches that were not in the snapshot.
4. Write `analysis/refresh-<date>.md`: the four lists with ids, advertiser, hook text, and a one-line read of what changed in the market (new angles, dropped angles, new proof types), with the caveat that an ad stopping is not evidence it failed. Send only the genuinely new ads through the rubric (`/adlab:analyze --only` or a small batch) and append rows to `analysis/ads.csv`.
5. Append a summary line to `changelog.md`. Mark done.

## Outputs

`ads/_snapshots/<date>.jsonl`, `analysis/refresh-<date>.md`, updated `analysis/ads.csv`.

## Report

finished / doing now / next; the three most important changes in one line each.
