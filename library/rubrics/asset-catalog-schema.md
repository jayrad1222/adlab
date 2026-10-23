# Asset catalog schema (`assets/catalog.md`)

## Purpose

The catalog is the inventory of what the member actually has: photos, clips, screenshots, documents, quotes, numbers. It is the only place the bank may draw proof from. Every claim in a concept or bank entry traces to a row here; if the row does not exist, the claim is a hypothesis or it is cut. The catalog is a three-column conversation: the member says what an asset is for, Claude says what it sees, and the two are reconciled into a revised read. The permissions column blocks use until consent is known.

Related: [`concept-brief-schema.md`](concept-brief-schema.md), [`bank-entry-schema.md`](bank-entry-schema.md), [`evidence-integrity.md`](evidence-integrity.md), [`../platform/ftc-endorsements.md`](../platform/ftc-endorsements.md), [`../platform/creator-category-truth-rules.md`](../platform/creator-category-truth-rules.md), [`../platform/specs-and-safe-zones.md`](../platform/specs-and-safe-zones.md), [`../psychology/make-the-invisible-visible.md`](../psychology/make-the-invisible-visible.md).

## Row fields

In this order. One row per file. A folder of similar photos is still one row per file; a video gets one row plus a note on which frames matter.

| Field | Allowed values or format | How to fill it |
|---|---|---|
| File | Relative path under `assets/` | Exact filename. Videos also list the contact sheet and transcript paths produced by `process`. |
| Type | `photo`, `video`, `screenshot`, `document`, `quote`, `number`, `logo-or-brand`, `audio`, `other:<text>` | A screenshot of a review is `screenshot`, not `quote`; the quote inside it gets its own row if it will be used as text. |
| What it shows (observed) | Free text, descriptive only | What is literally in the frame or file: objects, people, text visible, setting, duration, the number and its unit. No interpretation here. For a video, timestamp the moments that matter. |
| What it can prove and what it cannot | Two short lists | "Can prove: the product exists in this colour; the founder was in a workshop on this date." "Cannot prove: that the result shown is typical; that the person is a customer; that the number is current." Be strict: a demonstration is not a deployment, a screenshot of a dashboard is not a verified result, a happy face is not a testimonial. |
| Quality at phone size | `usable`, `usable-with-crop`, `marginal`, `unusable`, plus a reason | Judge at 1080 wide on a phone: focus, lighting, legibility of any text, noise, orientation, safe zones for 9:16. See `../platform/specs-and-safe-zones.md`. |
| Persona and angle fit | Persona ids and angle family slugs, or `none-yet` | Which personas this asset would be credible to and which angles it serves. A kitchen-table shot fits a problem-led angle for the after-hours persona; a trade-show banner does not. |
| Needed edit | Free text or `none` | Crop, caption, blur a bystander, add the wordmark, trim to a moment, re-shoot. If the edit would change what the asset proves (for example cropping out context that qualifies a result), say so and do not do it. |
| The member's note | Free text, verbatim from the member, labeled owner-provided | What the member says the asset is, when it was made, what it was for, who is in it. Not edited by Claude. |
| Claude's read | Free text, labeled inferred | What Claude sees and infers, written before reading the member's note where possible, so the two are independent. Include anything the member did not mention: a visible competitor logo, an out-of-date price, a person who may not have consented. |
| The revised read | Free text | The reconciled description after the member and Claude compare notes, dated. Where they still disagree, record both and mark the asset `hold`. |
| Permissions (who is in it, consent status) | Names or roles of every identifiable person; consent status one of `granted`, `requested`, `unknown`, `declined`, `not-applicable` | Written consent to appear in paid ads is `granted`; a verbal yes is `requested` until documented. Any `unknown` or `declined` blocks use of that asset in the bank. Also note ownership: did the member make it, buy it, or receive it from a customer, and on what terms. |
| Status | `cataloged`, `hold`, `cleared`, `used`, `retired` | `cleared` requires a revised read, a permissions value of `granted` or `not-applicable`, and a quality of at least `usable-with-crop`. `used` lists the bank entry ids. |

## Template row

Copy this block into `assets/catalog.md` once per asset.

```
### <file>

- File:
- Type:
- What it shows (observed):
- What it can prove and what it cannot:
  - Can prove:
  - Cannot prove:
- Quality at phone size:
- Persona and angle fit:
- Needed edit:
- The member's note (owner-provided):
- Claude's read (inferred):
- The revised read (<date>):
- Permissions (who is in it, consent status):
- Status:
```

## Per-item deep dive

On request the `assets` skill goes deeper on one row: frame-by-frame for a video with the transcript beside it, a line-by-line read of a document, or a check of a number against its source. The deep dive is appended under the row with a date and does not change the row's observed description.

## Rules

- The catalog never contains an asset that does not exist on disk. A planned shoot is a note in the concept brief, not a catalog row.
- Numbers get their own rows with the source document attached (an export, a statement, a screenshot with the date visible). A number with no source is cataloged as `hold` and cannot be used.
- Customer quotes need the customer's consent to be used in advertising, separately from any consent to be quoted in a review. Record both.
- Generated media is cataloged like any other asset, with Type `other:ai-generated` and a note of the prompt and model, and can only ever prove "this is what we imagined", nothing about the business.
