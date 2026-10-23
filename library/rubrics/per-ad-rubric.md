# Per-ad rubric (`analysis/ads.csv`)

## Purpose

One row per competitor ad. The `ad-analyst` agent fills it from the ad's `ad.md` (copy, transcript, on-screen text, landing summary), the poster frame and contact sheet, and the landing page capture. The row is the unit of evidence for the market map, the personas, the interrogation and every "nine of twelve competitors do X" sentence that follows. A row that guesses is worse than a row that says unknown.

Three rules apply to every row:

1. Write only what was looked at. The `inspection_coverage` column says how much of the ad was inspected, and the other columns may not claim more than that.
2. Separate what was observed from what was inferred. Columns that ask for an inference (`persona_inferred`, `emotional_lever`, `biases_used`, `sutherland_lens`) must be backed by a cue the analyst can point to in copy, transcript or frames, and the cue goes in the matching evidence column or in `works` and `weak`.
3. Use the fixed vocabularies. Free text goes only in the columns marked free text.

Related: [`evidence-integrity.md`](evidence-integrity.md), [`market-map-template.md`](market-map-template.md), [`../copy/hook-taxonomy.md`](../copy/hook-taxonomy.md), [`../copy/angle-families.md`](../copy/angle-families.md), [`../copy/format-taxonomy.md`](../copy/format-taxonomy.md), [`../strategy/schwartz-awareness-stages.md`](../strategy/schwartz-awareness-stages.md), [`../strategy/schwartz-market-sophistication.md`](../strategy/schwartz-market-sophistication.md).

## The unknown convention

- If a value cannot be determined from what was inspected, write `unknown`. Never leave a cell blank; a blank is ambiguous between "not applicable" and "not checked".
- If a column does not apply (for example `duration_s` on a static), write `n/a`.
- If a value is an inference rather than an observation, prefix it with `inferred:` in free-text columns. Enumerated columns do not take prefixes; if the enumerated value is an inference, say so in `persona_evidence`, `works` or `weak`.
- Never write a value that would require a higher `inspection_coverage` than the row carries. A `copy-only` row cannot have a `visual_hook`, a `production_style` other than `unknown`, or a transcript-based `hook_text`.

## Columns

Columns are listed in the exact order of the CSV header. "Free text" means a short phrase or sentence; keep it under about 30 words so the CSV stays readable.

| Column | Allowed values or format | How to fill it |
|---|---|---|
| `ad_id` | The platform's ad id (Meta `ad_archive_id`, Google creative id, LinkedIn id, TikTok id) or the `manual-NNN` id assigned in Lite mode | Copy from `ad.md`. Never invent or renumber. |
| `advertiser` | Free text, the advertiser's name as the ad library shows it | From the ad library record. Keep the same spelling across all rows for one advertiser. |
| `page_or_account` | Page id, account handle or URL | From the ad library record. `unknown` if the library did not expose it. |
| `platforms` | Pipe-separated list from: `facebook`, `instagram`, `messenger`, `audience-network`, `threads`, `whatsapp`, `google-search`, `youtube`, `google-display`, `linkedin`, `tiktok` | From the ad library record's placements field. Do not infer from the aspect ratio. |
| `first_seen` | `YYYY-MM-DD` | The start date the ad library reports. `unknown` if not reported. |
| `days_active_at_capture` | Integer or `unknown` | Capture date minus `first_seen`. If `first_seen` is unknown, this is unknown. This is a count of days, not a judgment of success. |
| `status` | `active`, `inactive`, `unknown` | From the ad library record at capture time. |
| `variant_count` | Integer or `unknown` | How many versions of this ad the library grouped under one id or one creative. `1` when the library shows no grouping. |
| `variant_type` | `copy-test`, `creative-test`, `placement`, `none` | `copy-test` when variants differ in text only; `creative-test` when the image or video differs; `placement` when the same creative is cut for different placements; `none` when `variant_count` is 1. Needs the variants to have been viewed; otherwise `unknown`. |
| `format` | One value from the format taxonomy in `../copy/format-taxonomy.md`, written as its slug (for example `static-text-only-ugly`, `video-founder-to-camera`, `carousel-tutorial-steps`) | From the media type and what the poster or frames show. A video seen only as its poster can be tagged `video-unknown`. |
| `duration_s` | Integer seconds, `n/a` for statics and carousels, `unknown` if the video was not fetched | From `media.py` output in `ad.md`. |
| `hook_text` | Free text, verbatim | For video: the first spoken line or first on-screen card, whichever appears first, taken from the transcript or frames. For statics: the largest text on the image, or the first line of primary text if the image has no text. Quote exactly; do not paraphrase. Mark the source in brackets at the end: `[transcript]`, `[on-screen]`, `[primary text]`, `[headline]`. |
| `hook_type` | One slug from the 26-type menu below | Classify the `hook_text`. If two apply, pick the one doing the most work and note the second in `works`. |
| `angle_family` | One slug from the angle families below | The strategic idea of the whole ad, not just the hook. |
| `awareness_stage` | `unaware`, `problem`, `solution`, `product`, `most` | Who the opening is written for. `most`: it opens with the offer or the price. `product`: it opens with the brand's difference or proof. `solution`: it opens with a mechanism or how-it-works. `problem`: it names a problem before any solution. `unaware`: it opens with a story or identity and the product arrives late. See `../strategy/schwartz-awareness-stages.md`. |
| `sophistication_move` | `claim`, `bigger-claim`, `mechanism`, `better-mechanism`, `identification` | Which Schwartz move the ad is making. `claim`: a simple direct promise. `bigger-claim`: the same promise with a larger number, faster time or stronger adjective than peers. `mechanism`: it explains how it works. `better-mechanism`: it contrasts its mechanism with the category's. `identification`: the ad is about who the buyer is or the feeling of using it. See `../strategy/schwartz-market-sophistication.md`. |
| `persona_inferred` | Free text, a situation (for example `two-person service shop drowning in quotes at night`) | Who the ad is talking to, phrased as a situation, not a demographic. Prefix with `inferred:`. |
| `persona_evidence` | Free text | The exact cue that supports `persona_inferred`: a callout line, a prop in frame, a setting, a job title in the transcript, a pain named in words. Quote it. If there is no cue, write `none, persona unknown` and set `persona_inferred` to `unknown`. |
| `emotional_lever` | One or two from: `relief`, `fear-of-loss`, `status`, `belonging`, `curiosity`, `pride`, `guilt`, `hope`, `anger`, `amusement`, `safety`, `control`, `unknown` | What the ad wants the viewer to feel before the rational case lands. Point to the cue in `works` or `weak`. |
| `biases_used` | Pipe-separated slugs from `../psychology/` (for example `social-proof|anchoring-and-framing|loss-aversion-and-prospect-theory`) or `none-detected` | Only tag a bias when the file's detection cue is visibly present. Tagging a bias on a hunch is a violation of rule 3 in `evidence-integrity.md`. |
| `proof_type` | `demo`, `testimonial`, `data`, `authority`, `social-proof`, `press`, `ugc`, `none` | The strongest proof shown. `demo` means the product is shown doing the thing. `data` means a number with a stated source. A number with no source is a claim, not proof; tag `none` and note it in `weak`. |
| `offer_elements` | Pipe-separated from: `price`, `discount`, `trial`, `guarantee`, `bonus`, `scarcity`, `urgency`, `payment-plan`, `free-resource`, `none` | What the ad itself states. Do not pull offer elements from the landing page into this column; those go in `landing_type` and `landing_continuity`. |
| `price_framing` | Free text or `not-shown` | How the price is presented if shown: `charm` ($97), `round` ($100), `per-day`, `anchored-against X`, `tiers`, `free`. See `../psychology/price-is-information.md`. |
| `cta` | Verbatim button or spoken CTA text | From the ad library record or the transcript. `unknown` if the capture did not include it. |
| `landing_type` | `sales-page`, `lead-form`, `checkout`, `app-store`, `booking`, `community-page`, `homepage`, `article`, `quiz`, `dm`, `unknown` | From the landing capture in `ad.md`. `unknown` if the landing page was not fetched. |
| `landing_continuity` | `strong`, `weak`, `broken`, `unknown` | `strong`: the landing headline repeats the ad's promise and the same persona. `weak`: same product, different promise or persona. `broken`: a different offer, a dead link or a generic homepage. `unknown` if not fetched. |
| `production_style` | `polished`, `native`, `ugly`, `ugc`, `founder`, `screen-rec` | What the frames or poster show. `polished`: studio, graded, designed. `native`: looks like an organic post. `ugly`: deliberately plain text or crude layout. `ugc`: a non-founder person filming themselves. `founder`: the owner to camera. `screen-rec`: a screen recording leads. Requires at least `still-reviewed`. See `../strategy/hott-ugly-ads.md`. |
| `visual_hook` | Free text | What is on screen in the first frame or on the static that would stop a scroll: the object, the face, the text card, the motion. Requires at least `still-reviewed`; otherwise `unknown`. |
| `on_screen_text_density` | `none`, `low`, `medium`, `high` | `none`: no text on the creative. `low`: one short line. `medium`: a headline and a support line. `high`: a paragraph, a list or a table on the creative. Requires at least `still-reviewed`. |
| `distinctive_assets` | Free text or `none-visible` | Any recurring brand asset: a face, a colour, a wordmark, a sound, a set, a character. See `../strategy/sharp-mental-physical-availability.md`. |
| `sutherland_lens` | Free text, one sentence | Which psycho-logical job the ad is doing beyond its rational claim (status, context shift, uncertainty removal, costly signal, ritual, making the invisible visible). Name the concept file. Prefix with `inferred:`. |
| `works` | Free text, up to three points | What is specifically effective, each tied to a cue. "Good hook" is not acceptable; "opens on the invoice pile at 11pm, names the problem before the product" is. |
| `weak` | Free text, up to three points | What is specifically weak, each tied to a cue, including unsupported numbers and policy risks. |
| `verdict` | `adapt`, `avoid`, `monitor` | `adapt`: a mechanism worth testing for the member. `avoid`: a pattern that is policy-risky, untrue for the member, or already saturated. `monitor`: unclear; check on refresh. |
| `adaptation_idea` | Free text, one sentence | For `adapt` rows only: the member's version of the mechanism, without copying the competitor's words. `n/a` otherwise. |
| `inspection_coverage` | `copy-only`, `still-reviewed`, `video-watched` | See the honesty rule below. |

## The hook-type menu (26 types)

Full definitions and detection cues are in [`../copy/hook-taxonomy.md`](../copy/hook-taxonomy.md). The slugs accepted in `hook_type` are:

1. `callout` ("if you run a...")
2. `question`
3. `bold-claim`
4. `specific-number`
5. `curiosity-gap`
6. `pattern-interrupt`
7. `contrarian-or-myth` ("stop doing X")
8. `negative-or-warning`
9. `confession-or-pratfall`
10. `story-opener`
11. `pov`
12. `three-reasons`
13. `today-years-old` ("I was today years old")
14. `nobody-talks-about`
15. `comparison` ("X vs Y")
16. `news-or-new`
17. `social-proof` ("why 1,214 people...")
18. `authority` ("as a...")
19. `demonstration` ("watch this")
20. `problem-naming` ("the 11pm invoice pile")
21. `identification` ("for the two-person shop")
22. `offer` ("free until Friday")
23. `what-i-wish-i-knew`
24. `the-real-reason`
25. `unpopular-opinion`
26. `day-1-vs-day-30`

## Angle families (12)

Full definitions in [`../copy/angle-families.md`](../copy/angle-families.md). Slugs accepted in `angle_family`:

`problem`, `desire`, `mechanism`, `identity`, `proof`, `offer`, `contrarian`, `news-or-trend`, `comparison`, `story-or-origin`, `education-or-insight`, `cost-of-inaction`

`cost-of-inaction` carries a policy caution: see [`../platform/meta-policy-pitfalls.md`](../platform/meta-policy-pitfalls.md).

## Awareness and sophistication values

- `awareness_stage`: `unaware`, `problem`, `solution`, `product`, `most`.
- `sophistication_move`: `claim`, `bigger-claim`, `mechanism`, `better-mechanism`, `identification`.

Both are read off the ad's opening, not off the advertiser's reputation. The same advertiser can run ads at several stages; that is itself a finding for the market map.

## The `inspection_coverage` honesty rule

This column is the ceiling on every other column in the row.

| Value | What it means | What the row may contain |
|---|---|---|
| `copy-only` | Only the ad library text fields were read: primary text, headline, description, CTA, link. No image, poster or video was viewed. | `hook_text` from primary text or headline only. `format` may only be `static-unknown`, `video-unknown` or `carousel-unknown`. `production_style`, `visual_hook`, `on_screen_text_density`, `distinctive_assets` must be `unknown`. `proof_type` may only reflect proof stated in text. |
| `still-reviewed` | The static image, or the video's poster frame and contact sheet, was viewed. The video was not played and no transcript was read. | Everything above plus what a still can show. `hook_text` for a video must come from on-screen text in the first frame or from primary text, and must be marked `[on-screen]` or `[primary text]`, never `[transcript]`. `duration_s` from metadata is fine. Claims about what is said in the video are not. |
| `video-watched` | The video was played through, or its full transcript with timestamps was read alongside the frames. | All columns may be filled from the full content. |

Reading a transcript without frames counts as `video-watched` only if the frames or contact sheet were also viewed; otherwise record `still-reviewed` and note "transcript read, frames not viewed" in `weak`. Never record `video-watched` for a video that was only summarized by another agent. If in doubt, record the lower level.

## Example row (fictional)

This advertiser, ad and every value below are invented to show the format. They are not data and must not be cited.

| Column | Value |
|---|---|
| `ad_id` | `fict-000001` |
| `advertiser` | Ridgeline Bookkeeping Co (fictional) |
| `page_or_account` | `fict-page-9001` |
| `platforms` | `facebook\|instagram` |
| `first_seen` | `2026-07-14` |
| `days_active_at_capture` | `100` |
| `status` | `active` |
| `variant_count` | `3` |
| `variant_type` | `copy-test` |
| `format` | `video-founder-to-camera` |
| `duration_s` | `34` |
| `hook_text` | "It's 11pm and you're still matching receipts. Give me 30 seconds." [transcript] |
| `hook_type` | `problem-naming` |
| `angle_family` | `problem` |
| `awareness_stage` | `problem` |
| `sophistication_move` | `mechanism` |
| `persona_inferred` | inferred: solo trades owner doing their own books after hours |
| `persona_evidence` | "you're still matching receipts" at 0:00; a kitchen table and a shoebox of receipts in frame at 0:02 |
| `emotional_lever` | `relief\|guilt` |
| `biases_used` | `make-the-invisible-visible\|satisficing` |
| `proof_type` | `demo` |
| `offer_elements` | `trial\|guarantee` |
| `price_framing` | `not-shown` |
| `cta` | Start free |
| `landing_type` | `lead-form` |
| `landing_continuity` | `strong` |
| `production_style` | `founder` |
| `visual_hook` | founder at a kitchen table holding a shoebox of receipts, phone-shot, no graphics |
| `on_screen_text_density` | `low` |
| `distinctive_assets` | the shoebox appears in two other ads from this advertiser |
| `sutherland_lens` | inferred: removes the fear of looking disorganized in front of an accountant (satisficing); shows the work (make the invisible visible) |
| `works` | names the moment before the product; the shoebox is a concrete object the persona owns; the first step shown is tiny (photograph one receipt) |
| `weak` | "most owners save six hours a week" at 0:19 has no source; the guarantee terms are not stated in the ad |
| `verdict` | `adapt` |
| `adaptation_idea` | open on the member's equivalent 11pm object and show the first step taking under a minute, with no unsourced time-saving number |
| `inspection_coverage` | `video-watched` |

## CSV header line (verbatim)

```
ad_id,advertiser,page_or_account,platforms,first_seen,days_active_at_capture,status,variant_count,variant_type,format,duration_s,hook_text,hook_type,angle_family,awareness_stage,sophistication_move,persona_inferred,persona_evidence,emotional_lever,biases_used,proof_type,offer_elements,price_framing,cta,landing_type,landing_continuity,production_style,visual_hook,on_screen_text_density,distinctive_assets,sutherland_lens,works,weak,verdict,adaptation_idea,inspection_coverage
```

Pipe characters separate multiple values inside one cell so commas stay reserved for the CSV. Quote any cell that contains a comma or a line break.
