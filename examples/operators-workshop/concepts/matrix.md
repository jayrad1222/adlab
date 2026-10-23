# Coverage matrix: Operators Workshop

Written 2026-10-23 for `/adlab:angles` from the six persona files, `personas/coverage.md`, `analysis/market-map.md`, `analysis/conventions.md` and `business/interrogation.md`. `assets/catalog.md` exists with 0 rows (no files were supplied), so proof is limited to what the brief and the About page show (observed) and what the founders' standing brief says (owner-provided). The founders say they hold "dated warehouse and store photographs, real software screens, approved account screenshots with strict meaning, and one honest rejected-result demonstration" (interrogation answer 12, owner-provided; the screens are not described as dated); none of them is cataloged, so every cell that needs one is **held**, not open. Counts are advertisers of the 12 roster Pages (market map section 1), never ads. Nothing here is performance data; every cell is a hypothesis.

## How to read a cell

- `proof → format`: the cell is usable now. Proof is what the ad can stand on today: `situation` (names a moment, makes no claim), `policy` (a rule the founders hold, owner-provided: no done-for-you, no guarantees, no build reviews, no response-time promises, no income claims), `page` (a fact on the About page, observed), `founders` (who the founders are and what they run, owner-provided).
- `held (needs X) → format`: usable once the named asset is cataloged with consent, or once the named decision is made. The concept can be written; it cannot be `ready`.
- `rej: CODE`: rejected, with the reason.
  - `NP` no proof available: the cell needs a member result, a testimonial, a customer quote or a sourced number, and none exists.
  - `PR` policy risk: personal attributes, fear-first or shaming framing, income or results implication (`library/platform/meta-policy-pitfalls.md`).
  - `RULE` ruled out by the standing brief (income, guarantees, done-for-you, build reviews, response-time promises).
  - `ST` wrong stage for this persona at this awareness level.
  - `SAT n` crowded: n of 12 roster advertisers already run this angle at this persona.
- **OPEN** marks a cell the market leaves empty (market map section 4 uncontested claims, section 5 persona coverage, section 8 format gaps).
- `→ cNN` marks the cell a concept fills.

Format slugs follow `library/copy/format-taxonomy.md`: `static-problem-card`, `static-text-only-ugly`, `static-founder-note`, `static-us-vs-them`, `static-three-reasons`, `static-offer-card`, `static-email-screenshot`, `static-whats-inside`, `static-faq-card`, `video-pov`, `video-screen-pip`, `video-mistakes-and-lessons`, `video-mini-doc`, `video-comparison-alone`, `carousel-tutorial-steps`.

## The matrix

Rows are persona x awareness stage, two stages per persona where the persona file puts most of its people (`personas/coverage.md`, awareness table). Columns are the twelve angle families (`library/copy/angle-families.md`).

| Persona, stage | problem | desire | mechanism | identity | proof | offer | contrarian | news | comparison | story | education | cost-of-inaction |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| p1 owner at the desk, problem | **OPEN** situation → static-problem-card, video-pov → **c01** | rej: NP (the evening back is a results claim) | held (needs a real software screen, dated, from the founders' business) → video-screen-pip | founders → static-us-vs-them (better at solution, see c07) | held (needs a real software screen; a quote email is hypothetical until the founders confirm one) → static-before-and-after (better at solution, see c02) | rej: ST | rej: ST (p1 has not seen the conventions) | rej: ST | held (needs by-hand and with-AI footage) → video-comparison-alone, format gap s8 | founders → static-founder-note | rej: ST | rej: NP, PR (the cost of a late quote has no source) |
| p1 owner at the desk, solution | covered by row above | rej: NP | held (needs dated screen) → video-screen-pip; generic demos at 5 of 12 | **OPEN** founders, page → static-us-vs-them (0 of 12 address the owner who wants to run an existing business better with AI; market map s5, inferred) | **OPEN** held (needs a real software screen from the founders' own business, with what the AI got wrong marked; a quote email is hypothetical until the founders confirm one) → video-screen-pip → **c02** | rej: ST | policy → static-text-only-ugly (conventions row 3 inverse; carried by c07) | rej: SAT 4, ST | **OPEN** founders, page → static-us-vs-them (10 of 12 sell the route to clients or creator income; market map s4) → **c07** | held (needs rejected-result demo) → video-mistakes-and-lessons | situation → carousel-tutorial-steps (sibling of c09) | rej: NP, PR |
| p2 truck is the office, unaware | rej: ST (an unaware owner does not read AI into the problem) | rej: NP | rej: ST | **OPEN** founders → static-text-only-ugly, static-problem-card → **c03** | held (needs dated shop schedule; the filmed founder's consent) → static-email-screenshot | rej: ST | rej: ST | rej: ST | rej: ST | held (needs shop footage; the filmed founder's consent) → video-mini-doc, format gap s8 | rej: ST | rej: NP, PR |
| p2 truck is the office, problem | held (needs a real shop photograph) → static-problem-card with photo | rej: NP | held (needs phone footage; "works from the cab" is unverified) → video-screen-pip | covered by c03 | held (needs dated gear list or quote; the filmed founder's consent) → static-email-screenshot | rej: ST | policy → "if you already run something" (conventions row 3; carried by c03) | rej: ST | held (needs footage) → video-comparison-alone | held (needs hands-at-screen footage; the filmed founder's consent) → video-mini-doc | rej: ST | rej: NP, PR |
| p3 solo seller, problem (operations) | **OPEN** founders (they sell on four marketplaces) → static-problem-card, video-pov → **c04** | rej: NP | held (needs seller inbox screen, customer data hidden) → video-screen-pip | founders → static-text-only-ugly (sibling of c04) | held (needs payout-versus-cost screen with strict caption) → static-email-screenshot | rej: ST | situation → "content is the smallest part of running a shop" (carried by c04 hooks) | rej: ST | rej: NP (needs claims about competitors' outcomes) | held (needs dated store photographs) → photo-hook | held (needs founders to confirm the Business Tactics track covers seller numbers; deposit screen) → carousel-tutorial-steps | rej: NP, PR |
| p3 solo seller, solution (content-aware) | covered by row above | rej: SAT 2 (shop and brand owners addressed as content buyers: AI Video Bootcamp, Arcads; corrected 2026-10-23), NP | held → video-screen-pip | rej: SAT 2 (the content-buyer identity is served: AI Video Bootcamp, Arcads) | held (deposit screen, strict caption) → static-email-screenshot | rej: ST | situation → static-problem-card (carried by c04) | rej: SAT 4 | rej: NP | held → photo-hook | held → carousel-tutorial-steps | rej: PR |
| p4 nights-and-weekends builder, solution | rej: SAT 2 (course-fatigue cards: AI Operator CLUB 1617270070414246, CTtheDisrupter) | rej: RULE (the desire sold to p4 is income) | held (needs a real build end to end) → video-screen-pip | founders → static-founder-note (sibling of c05) | held (needs rejected-result demo) → video-mistakes-and-lessons (see c06 for p6) | rej: ST | **OPEN** policy → static-founder-note, static-text-only-ugly (income refusal at 0 of 12; conventions row 2) → **c05** | rej: SAT 4 | founders → static-us-vs-them (routes; sibling of c07) | held (needs rejected-result demo) → video-mistakes-and-lessons | rej: PR (teaching "how to judge a course" reads as an attack on named competitors) | rej: PR |
| p4 nights-and-weekends builder, product (said no to competitors) | rej: ST | rej: RULE | rej: ST | rej: SAT 2 (Maker School retargeting callouts) | rej: NP (no member result) | **OPEN** policy, page → static-text-only-ugly (nobody says who it is not for; guarantees at 5 of 12, market map s3 as corrected) → **c11** | policy → covered by c05 and c11 | rej: SAT 4 | rej: PR (naming competitors) | rej: NP | rej: ST | rej: PR (lapsed-checkout urgency, conventions row 7) |
| p5 nervous beginner, unaware | rej: PR (the "behind" fear is the shaming convention: 1101916785561103, 1123979320082708) | rej: NP | rej: ST | rej: SAT 3 (gentle callouts: Hashtag NoCode, The Claude Club, AI Operator CLUB), PR | rej: NP | rej: ST | rej: ST | rej: ST | rej: ST | held (needs a founder's true first-build story) → static-founder-note | rej: ST | rej: PR |
| p5 nervous beginner, problem | rej: PR | rej: NP | rej: SAT 3 (slow walk-throughs and lesson lists) | rej: SAT 3 | held (needs rejected-result demo) → video-mistakes-and-lessons | held (needs week one defined: an offer decision, answer 6) → static-three-reasons, static-whats-inside → **c10** | held (needs a paid first week defined; conventions row 8) → static-text-only-ugly | rej: ST | rej: SAT 7 (free entry is table stakes, market map s3) | held → static-founder-note | rej: NP ("you are not behind" needs a source) | rej: PR |
| p6 ChatGPT tab, problem (the stall) | rej: SAT 3 (stall-naming: Skool for Claude Code Club 2032976233999151, 852511001188204; Maker School; The Claude Club) | rej: NP | **OPEN** situation, page → carousel-tutorial-steps (nobody asks the viewer to bring their own task) → **c09** | rej: SAT 3 | held (needs a dated prompt beside its process) → static-email-screenshot | rej: ST | situation → "no new tool; the one in your tab is enough" (candidate, not chosen this round) | rej: SAT 4 (tool news is this viewer's feed) | situation → static-us-vs-them, tutorials versus one built task (candidate, not chosen) | **OPEN** held (needs rejected-result demo) → video-mistakes-and-lessons → **c06** | situation → carousel (candidate) | rej: PR |
| p6 ChatGPT tab, solution and most aware | covered by row above | rej: NP | covered by c09 | rej: SAT 3 | held → static-email-screenshot | **OPEN** page (price, trial, cancel) → static-offer-card without a strikethrough (strikethrough at 6 of 12; conventions row 1) → **c08** | page → static-offer-card (carried by c08) | rej: SAT 4 | rej: PR (price comparison against a named tool) | covered by c06 | situation → carousel (candidate) | rej: PR |

## Cells the market leaves open

From the market map's uncontested claims (section 4), persona coverage (section 5) and format gaps (section 8):

- The owner of an existing business who wants to run it better with AI, at every stage: 0 of 12 roster advertisers (market map s5, inferred from the rows; adjacent ads name owners but sell a workshop, a placement or content: 1101916785561103, 710487895220380). Rows p1, p2, p3.
- A dated operating artifact as proof: none in the copy, on-screen text and stills read (market map section 4; spoken tracks not heard). Held for every persona until the founders' screens are cataloged.
- Mistakes language: absent from the copy, on-screen text and stills of all 106 roster ads; spoken tracks were not heard (section 4, evidence rule 9). Held until the rejected-result demonstration is cataloged.
- An income refusal: none in the copy, on-screen text and stills read. A "who it is not for" line that names the delivery promises refused: none; the nearest is The Claude Club's audience line "Strictly for job professionals & business owners. No students." (1101916785561103).
- Formats nobody uses: founder note, text-only ugly, comparison with doing it alone, mini-documentary of a real business, two-founder dialogue (section 8).

## Chosen cells and the concepts that fill them

Eleven concepts, one per cell, each a different idea (not a different hook). Eight can be made `ready` from what the page and the standing brief already prove; three are held by a missing asset or an offer decision and say so.

| Concept | Persona, stage | Angle family | The cell's proof today | Can it be `ready` now? |
|---|---|---|---|---|
| c01 the quote still in drafts | p1, problem | problem | situation, page | yes |
| c02 the Tuesday screen and what the AI got wrong | p1, solution | proof | held: a real software screen, cataloged | no: needs the asset cataloged |
| c03 AI ads are made for desks | p2, unaware | identity | founders | after the critic: the founder-note static yes once the gates clear; the text-only static also waits on the named founder's OK |
| c04 the shop is not the content | p3, problem | problem | founders, page | yes, once the gates clear |
| c05 the ad with no income number | p4, solution | contrarian | policy | no: blocked after the critic until the About page drops "earn more" |
| c06 it did not stick the first time | p6, problem | story | held: rejected-result demo | no: needs the asset cataloged |
| c07 use it on the business you already run | p1, solution | comparison | founders, page | yes |
| c08 ninety-seven dollars, and the reason | p6, most | offer | page | yes |
| c09 bring the task you keep redoing | p6, problem | mechanism | situation, page | yes |
| c10 week one, in three steps | p5, problem | offer | held: week one is not defined | no: an offer decision first |
| c11 the list of what we do not do | p4, product | offer | policy, page | yes |

**After the critic's review (2026-10-23).** Every brief was reviewed and revised to version 2 (notes, author's replies and changelogs are in the files). Two changes to the column above: c05 is now blocked, because its landing contradicts it until the About page drops "earn more"; and every concept, ready-capable or not, waits on the About-page decisions named in `business/interrogation.md` ("Before any test runs": "earn more", "even after it rises to $129", "Get direct answers and support from us") and on the founders confirming that builds are shared as they happen today. Ready-capable after those gates: c01, c03 (the founder-note static; the text-only static also waits on the named founder's OK to be named), c04, c07, c08 (retargeting or the R4 test only), c09, c11. Held: c02, c06 (assets), c10 (week one). Blocked: c05.

Ugly or native concepts: c01 (text-only and POV), c03 (text-only), c05 (founder note), c11 (text-only), c06 (screen recording). From the opposite pass: c05 (convention 2), c07 (convention 3), c08 (convention 1). See `opposite-pass.md`.

Persona spread: p1 three (c01, c02, c07), p2 one (c03), p3 one (c04), p4 two (c05, c11), p5 one (c10, held), p6 three (c06, c08, c09). p2 and p3 get one each because nearly every proof they need is held (the filmed founder's consent gates any still or voice of any founder; the seller screens are not cataloged); the next round adds concepts for them as assets arrive. p5 gets one held concept because the interrogation's R3 asks the founders whether to leave p5 out of batch one; that decision is theirs.

## Evidence limits

- No asset catalog: proof is the About page, the standing brief and the founders' policies. No customer language and no transcripts exist in this run; no cell rests on either.
- Awareness splits are the persona-builder's inference, with no survey.
- Saturation counts come from `analysis/stats-roster.md` and the market map; they count advertisers in an active-only, capped sample.

## Corrections

- 2026-10-23, after the release critic: concept names aligned with the files; the readiness column now reflects the critic (c05 blocked, c03 split); the quote-email cells now ask for a real software screen (a quote email is hypothetical); the p3 content-buyer count corrected from 3 to 2 advertisers; the open-cells list scoped to what was read and The Claude Club's audience line named.
