# Bank entry schema (`bank/ad-bank.csv`)

## Purpose

One row per finished ad unit in the member's bank: a static, a video script, a carousel, a UGC brief. Rows are written by the `copywriter` and `creative-director` for each concept, reviewed by the `critic`, scored for recording priority, and exported to the board (`bank/ad-bank.html`) by `export.py`. Every row shows its reasoning, its competitor references and its risk flags, so a member can read why a line exists before deciding to run it.

Related: [`concept-brief-schema.md`](concept-brief-schema.md), [`editorial-score.md`](editorial-score.md), [`critic-checklist.md`](critic-checklist.md), [`evidence-integrity.md`](evidence-integrity.md), [`../copy/copy-formulas.md`](../copy/copy-formulas.md), [`../copy/cta-patterns.md`](../copy/cta-patterns.md), [`../copy/ugc-brief-structure.md`](../copy/ugc-brief-structure.md), [`../platform/specs-and-safe-zones.md`](../platform/specs-and-safe-zones.md).

## Columns

In header order. Free text under about 40 words unless the column is a copy field.

| Column | Allowed values or format | How to fill it |
|---|---|---|
| `entry_id` | `cNN-eNN` (the concept id, then the entry number within it), assigned once, never reused | Sequential within the concept. A revision keeps its id and bumps `version`. This is the id `/adlab:render --only` takes. |
| `concept_id` | `cNN` matching a file in `concepts/` | Every entry belongs to exactly one concept. |
| `persona` | `pN`, the `id` in a persona file's frontmatter under `personas/` | Must equal the concept's persona. The board shows the persona's name from that file. |
| `format` | One slug from `../copy/format-taxonomy.md` | One format per row. A concept rendered in three formats is three rows. |
| `aspect_ratio` | `1:1`, `4:5`, `9:16`, or pipe-separated if the same layout is cut for several | See `../platform/specs-and-safe-zones.md`. |
| `hook` | Copy field, verbatim | The first line spoken, the first on-screen card, or the largest text on the static. Tag the hook type in brackets at the end, for example `[problem-naming]`. |
| `primary_text_short` | Copy field, under about 125 characters | The above-the-fold primary text for feed placements. |
| `primary_text_long` | Copy field | The full primary text with the reason-why and the first step. Line breaks allowed; quote the cell. |
| `headline` | Copy field, under about 40 characters | The link headline. |
| `description` | Copy field, under about 30 characters, or `n/a` | The link description where the placement shows one. |
| `cta` | Platform button text (for example `Learn more`, `Sign up`, `Get offer`) | Must match the awareness stage of the concept. |
| `script_or_layout_ref` | Relative path | For video: the script file with shot list and on-screen text (`bank/scripts/<entry_id>.md`). For statics: the template name in `templates/` and the fields JSON (`bank/layouts/<entry_id>.json`). For carousels: the cards file. For UGC: the brief file. |
| `asset_refs` | Pipe-separated catalog row ids from `assets/catalog.md`, or `none` | Every real image, clip, screenshot or quote the entry uses. `none` means the entry uses only text or generated mood media, which must then be flagged in `risk_flags` as `ai-generated-media`. |
| `why_it_should_work` | Free text, two or three sentences | The mechanism in plain words with the library file, the persona cue it answers (quote from the language bank), and the awareness stage logic. Not "it is punchy". |
| `competitor_refs` | Pipe-separated ad ids from `analysis/ads.csv`, or `none` | The ads this entry was built against: what it borrows as a mechanism and what it does differently. Never copied wording. |
| `risk_flags` | Pipe-separated from: `none`, `personal-attribute`, `before-after`, `income-claim`, `results-claim`, `sensational`, `unsourced-number`, `testimonial-unverified`, `scarcity-unverified`, `urgency-unverified`, `ai-generated-media`, `consent-unknown`, `landing-mismatch`, `other:<text>` | Set by the copywriter, checked by the critic. A row with `testimonial-unverified`, `consent-unknown` or `scarcity-unverified` cannot move past `draft`. |
| `critic_note` | Free text, written by the critic only | Pass, revise with reason, or block with reason, per `critic-checklist.md`. Blank until the critic has run; a blank note means status stays `draft`. |
| `editorial_score` | Integer 0 to 12, or `unscored` | The six-dimension total from `editorial-score.md`. It is a recording priority, never a performance claim. |
| `status` | `draft`, `ready`, `rendered`, `testing`, `retired` | `ready` requires a critic pass and no blocking flags. `rendered` means files exist under `bank/renders/`. `testing` and `retired` follow the test plan and the decision rules. |
| `version` | Integer starting at 1 | Bumped on every change to a copy field, the hook, the format or the asset refs. |
| `changelog` | Free text | One line per version: date, what changed, why (the critic note, a readout rule, a member edit). Prior wording is preserved in the script or layout file, never deleted. |

## Rules that apply to every row

- A number in any copy field needs a source in `asset_refs` or it becomes `unsourced-number` in `risk_flags` and the critic blocks it.
- A quote presented as a customer's words needs a catalog row with consent status `granted`.
- "Observed", "owner-provided", "inferred" and "hypothetical" apply to `why_it_should_work`: say which the mechanism claim is.
- A hook that fails any of Harry Dry's three tests is rewritten before the row is saved, and the failing version is kept in the changelog.
- Generated media (Higgsfield or any image model) is mood and b-roll only, carries `ai-generated-media`, and is disclosed where platform policy requires. It never depicts a customer, a result or a screenshot.

## CSV header line (verbatim)

```
entry_id,concept_id,persona,format,aspect_ratio,hook,primary_text_short,primary_text_long,headline,description,cta,script_or_layout_ref,asset_refs,why_it_should_work,competitor_refs,risk_flags,critic_note,editorial_score,status,version,changelog
```

Pipe characters separate multiple values inside one cell. Quote any cell that contains a comma or a line break.
