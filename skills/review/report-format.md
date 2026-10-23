# analysis/critic-report.md format

The critic returns this text in full; `/adlab:review` writes it to `analysis/critic-report.md` unchanged. Plain words, no em dashes, no hype. Every finding quotes the exact line and names the file. A score is a recording priority, never a prediction. Worked examples: `examples/operators-workshop/analysis/critic-report.md` and `examples/ridge-wallet/analysis/critic-report.md` in the plugin.

## First review

```
# Critic report: <business name>

Reviewed <date> by critic.

**What was reviewed.** <the interrogation (version), N concept briefs plus the matrix and opposite pass, N bank entries (by status), the renders opened, the test plan and thresholds, the scan (N distinct lines)>.

**Sources used.** <the captured pages, business/*.md, assets/catalog.md (rows), analysis/*, personas/*; that every cited ad id was checked in analysis/ads.csv>.

## Verdict

<One paragraph. First sentence: whether any invented proof survives anywhere in the run (a result, testimonial, customer quote, member or customer count, review count or rating, revenue, saving, scarcity or urgency, a claim about what a video says aloud); name it if so. Then the overall verdict and the count of open blocks by kind.>

## Interrogation

<Skip with "No interrogation in this workspace." if there is none. Otherwise a table: item | finding | fixed, partly fixed or open. If the file carries an earlier critic note, re-check each of its numbered items.>

## Concepts

| Concept | Status | Critic verdict | What is still open |
|---|---|---|---|

<Then any wrong count, id or label in concepts/matrix.md and concepts/opposite-pass.md, quoted.>

## Bank

Counts by status and by verdict. Then:

| Entry | Format | Status | Why it is not ready (or "ready") |
|---|---|---|---|

Ready and rendered entries with their editorial score (a recording priority). Every ready entry must have a critic pass and no blocking flag; any that does not is a finding.

## Scan results

<Every line in analysis/scan.md from a ready, rendered or testing entry, resolved: "sourced: <file and words>" or "problem: <why>". Lines only in held entries may be summarized by kind, but any that would be a problem when the entry is released are listed.>

## Test plan

<Placeholders labeled; no forecast, ROAS or "winner"; only ready concepts in the first batch; thresholds marked starting points and using the keys tools/readout.py reads; the plan's rules agree with what readout.py does.>

## Evidence limits that bind this run

<Transcripts (watched or still-reviewed), customer language (none, or what and from where), assets cataloged (rows), placeholders in finance.md, anything captured after intake.>

## Open items for the member

- <one line each: who does it (the member, a founder, the client), what, and what it unlocks>

Overall: pass | revise | block. Reviewed <date> by critic.
```

## Re-review (appended to an existing report)

```
## Re-review (<date>)

Re-checked against the files as they stand: <what changed since the last review>.

- <each item the last report or re-review left open>: fixed | partly fixed (quote what remains) | open.
- <anything new found>.

Overall: pass | revise | block. Reviewed <date> by critic.
```

## Verdicts

- **block**: invented proof anywhere, including a test arm; a ready entry with a blocking flag or no critic pass; a claim that outruns its source in a ready entry; a broken landing for a ready entry.
- **revise**: wrong counts, ids, labels or quotes; a gate missing from a status; scan lines that need a fix but sit only in held entries; plan text that disagrees with the tools.
- **pass**: none of the above. Holds that are marked as holds (an asset, consent, a landing or an owner decision still missing) are open items, not blocks against the run.
