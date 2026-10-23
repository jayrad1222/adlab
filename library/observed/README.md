# Observed patterns

This folder holds patterns the `librarian` agent notices during member runs: a hook type that keeps appearing in one category, a proof format nobody in the library describes yet, a policy rejection and what fixed it, a convention inversion that survived a readout. It is the library's field notes. The canonical files in `psychology/`, `strategy/`, `copy/`, `sales/`, `finance/`, `platform/`, `rubrics/` and `prompts/` are never edited by the librarian; anything that should change a canonical file is written here first and promoted by a person after review.

## How the librarian writes here

- One file per observation, named `YYYY-MM-DD-<slug>.md`. Append-only: a later observation about the same pattern is a new dated file that links back, not an edit.
- Every file carries the ad ids (or bank entry ids, or readout dates) the observation rests on, the workspace or example run it came from, and the `inspection_coverage` level behind each id.
- Every file separates the observation from the interpretation, per `../rubrics/evidence-integrity.md` rule 12: what was seen, with ids, then what the librarian takes it to mean, labeled inferred or hypothetical.
- Counts state their denominator and whether the sample was active-only. Variants from one advertiser are counted as one observation.
- No member-identifying data: no member names, no customer names, no numbers from a member's `finance.md`. Ad ids from public ad libraries are fine; a member's own bank entries are referenced by id only.
- A suggested change to a canonical file is written as "Proposed addition to `../copy/hook-taxonomy.md`: ..." and left for review. The librarian does not make the change.

## File template

```
# <pattern in one line>

Observed: <YYYY-MM-DD>, run: <example run or workspace label>, librarian.

## What was seen
- <ad id>, <advertiser>, <coverage level>: <the cue, quoted or described>
- ...

## Count
<n of N ads, m of M advertisers; active-only: yes/no; variants collapsed: yes>

## What it might mean (inferred or hypothetical)
<the reading, with the library file it relates to>

## Proposed change to a canonical file (optional, for human review)
<file path and the proposed text>

## Related
<links to earlier observed files on the same pattern>
```

## Reading this folder

Agents may read these files as context, with the understanding that they are field notes, not library doctrine: lower confidence than the canonical files, higher recency. Cite them by filename when used.
