# Asset catalog: Operators Workshop

Written 2026-10-23 by `/adlab:assets` per `library/rubrics/asset-catalog-schema.md`.

**No files were supplied for this example run.** `assets/` holds no photographs, clips, screenshots, documents, quotes or numbers, so the catalog has no rows. Under the schema's first rule, the catalog never lists an asset that is not on disk, so nothing below is a row and nothing below can be cited as proof by a concept or a bank entry.

What this means downstream:

- Every concept and bank entry draws its claims from the About page (observed, `business/site/about/landing/page.txt`) and the founders' standing brief (owner-provided, `business/brief.md`) only. Anything that needs a picture, a screen, a quote or a number stays `held` until the file exists here with a revised read and a permissions value.
- No entry may show a person, a customer's words or a business number. Every entry's `asset_refs` is `none`.
- Nothing synthetic stands in for a missing asset. Generated media, if any is ever made, is cataloged as `other:ai-generated` and proves only "this is what we imagined".

## Assets the founders say exist (not cataloged; not usable yet)

Interrogation answer 12 (owner-provided) lists: "dated warehouse and store photographs, real software screens, approved account screenshots with strict meaning (deposits are not profit; spend is not ad spend), and one honest rejected-result demonstration." None was supplied. When the founders drop them into `assets/`, `/adlab:assets` writes one row per file with every schema field. Three checks will matter most:

| Asset named | What it would unlock | What must be recorded before use |
|---|---|---|
| Real software screens | c02 (the screen and what the AI got wrong), the screen-recording formats | the date on the screen; customer names and data hidden; who made it; whether it is a demonstration or a running system (a demonstration is not a deployment) |
| The rejected-result demonstration | c06 (it did not stick the first time) | that it is shown as a demonstration; the date; who is on screen or speaking |
| Dated warehouse and store photographs | the photo versions of c03 and c04 | who appears (any person other than the founders stays `consent: unknown` and blocks use); the date |
| Account screenshots | none this round | the strict caption (deposits are not profit; business spend is not ad spend); they are the easiest assets to misread and are not used in any concept |
| Anything showing a founder | the shop and two-founder formats | that founder's written consent to appear in paid ads; until then any footage, still or voice of that founder is blocked |

## Row template (for the first real file)

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

## Counts

Items cataloged: 0. Awaiting consent: 0. Named by the founders but not supplied: 5 kinds.
