# Critic report: Operators Workshop example run

Date: 2026-10-23. Reviewer: critic (release pass, BUILD-CHECKLIST "Truth rules verified by the critic"; HANDOFF item 3). The critic wrote notes only. No run artifact was edited; this file is the only file written.

## What was reviewed

- `business/interrogation.md`, version 2: the 23 numbered corrections from the first critic note, the three item-level blocks, and anything the revision introduced.
- 11 concept briefs, `concepts/c01` to `concepts/c11`, all version 2, each with its critic note and author's reply; plus `concepts/matrix.md` and `concepts/opposite-pass.md`.
- `bank/entries.jsonl`: all 32 entries (copy fields, `hooks`, `layout_fields`, `risk_flags`, `status`, `status_hint`, `critic_note`, `changelog`), the 21 layout files and the 11 video scripts. `bank/ad-bank.csv` matches the JSONL on hook, headline, status, score, CTA and long text for all 32 rows.
- Renders: 9 PNGs under `bank/renders/` (c01-e01, c07-e01, c08-e04 at 1:1, 4:5 and 9:16). Six were opened and checked against `fields.json`, the layout file and the entry.
- `plan/test-plan.md`, `plan/thresholds.json`, and `plan/economics.md` for the figures they copy; `tools/readout.py` for how the thresholds are used.
- The machine scan `scan-A.txt`: 279 hit lines (221 in copy fields, 58 in on-image text) across 32 entries.

Sources used for every claim: `business/site/about/landing/page.txt` (verbatim, captured 2026-10-23), `business/brief.md` (no addendum exists), `business/offer.md`, `business/interrogation-answers.md`, `business/finance.md`, `assets/catalog.md` (0 rows), `analysis/market-map.md`, `analysis/conventions.md`, `analysis/stats-roster.md`, `analysis/ads.csv` (every cited ad id was checked: all ids cited in the interrogation, the 11 concepts, the matrix, the opposite pass and every entry's `competitor_refs` exist), and `personas/*`. Every library file cited in those documents exists. The 113 `transcript.md` files under `ads/` all read "No transcription backend is installed"; no transcript exists.

## Verdict

No invented proof survives anywhere in this run. No ad field, layout, script or render carries an invented result, testimonial, member or customer count, review count, rating, revenue, saving, scarcity or urgency. The "$1.5M" line appears in no ad: it occurs only in critic notes and in two briefs' exclusion lists. No customer's words are used; the one quoted customer-style line ("Is this in stock?", c09) is labeled "Example (made up)". Nothing claims what a video says aloud. Demonstrations are labeled as demonstrations, deposits and spend appear in no ad, no editorial score is presented as a prediction, and nothing is called a winner. No ad relies on guarantees, done-for-you work, build reviews, support or response-time promises, or income; c11 and c05 name them only to refuse them. founders appear in text only, as the About page names him; every footage, still or voice of any founder is held for his written consent. The 13 ready or rendered entries trace every claim to page.txt or to the founders' standing brief, and every founder statement in them is gated on a confirmation the status_hint names. What remains is bookkeeping and synchronization: three c08 entries are marked ready while carrying `urgency-unverified` (a flag that describes the landing page, not the ad), several concept briefs, the matrix and the opposite pass still carry wording the later bank review corrected, and the test plan cuts hook variants whose on-image versions were never rendered or stranger-tested. The 24 open blocks are all holds for missing assets, consent or founder decisions, or landing blocks, and each is marked as such. Overall: revise.

## Interrogation

Re-review of version 2 against the first critic note (2026-10-23).

| # | Correction | Result |
|---|---|---|
| 1 | R6 absence claim limited to copy, on-screen text and stills | Fixed (R6 Evidence and header) |
| 2 | R4 card B urgency arm | Fixed: card B is the bare "$97 a month, 7-day free trial, cancel anytime" card; no urgency arm; the $129 line is a founders' decision under "Before any test runs" |
| 3 | R2 "$1.5M" control | Fixed: plain offer card; "The $1.5M line appears in no ad arm" |
| 4 | Assets named beyond answer 12 | Fixed: A3 names answer 12's assets only; quote email hypothetical; consent unknown until cataloged |
| 5 | Owner row "0 of 12 ... observed" | Fixed: narrower row, labeled inferred, adjacent owner rows named |
| 6 | "every claim" on the page | Fixed: "most", four claims named |
| 7 | Ambiguity-averse unlabeled | Fixed: labeled hypothetical |
| 8 | A7 quote not verbatim | Fixed |
| 9 | M2 wrong id and persona stated as fact | Fixed: 1013033575121449 and 1416360690414714; labeled hypothetical |
| 10 | "two advertisers keep running" urgency | Fixed in R4 Risk and A4 (one advertiser, 146 days). Partly: A4 still says "conventions.md row 7 also names Maker School"; conventions.md row 7 has since been corrected to one advertiser, so the sentence is stale |
| 11 | conventions.md ids | Fixed |
| 12 | Card A wording | Fixed: the About page's own line, observed, truth today pending founders |
| 13 | Maker School retargeting premise | Fixed: one advertiser's premise, inferred |
| 14 | 1020236937432064 shape; retargeting pool | Fixed |
| 15 | Falsifiers against a cohort that does not exist | Fixed: arms compared; first cohort sets the baseline |
| 16 | Who is filmed | Fixed: Jared proposed per arm; the filmed founder's written consent gates any footage, still or voice |
| 17 | Rejected result shown as a demo | Fixed |
| 18 | "Fixed by R6" | Fixed: "Addressed by R6 (hypothesis)" |
| 19 | "unsourced" counts | Fixed in A3 and Part D row 4 |
| 20 | Rule numbers by file | Fixed |
| 21 | Part D truth and dated count | Fixed: "5 members as of 23 October 2026"; per-row pending confirmation |
| 22 | Unlabeled causal lines | Fixed: R5 and R7 labeled hypothetical |
| 23 | Guarantees 4 versus 5 (upstream) | Fixed upstream; A3 and R5 say 5 of 12 with the five ids |

The three item-level blocks (item 1 rule 9, item 2 urgency arm, item 6 unsourced number) are all fixed. Items 3, 4 and 7 are answered: the deleted Part D lines are gone, the "Before any test runs" list carries the page decisions, and the new lines pass or are conditional ("Here is what we did last Tuesday" passes only with a dated artifact on screen).

Left or introduced by the revision:
- R2 Evidence: "section 6, proof types none 9, demo 7, data 1". Market map section 6 was corrected after this revision to none 10, demo 8, social-proof 3, authority 3, testimonial 2, data 1. Update the cited counts.
- A4: "conventions.md row 7 also names Maker School, but no Maker School urgency ad is in the roster rows." Stale since conventions.md was corrected; cut or reword.
- Part D row 2: "Income implication (4; 1761940881625624, 1013033575121449, 1129626886138176, 1506202640947121)". The count is 4 advertisers but the ids cover three (Maker School: AI Automation; AI Video Bootcamp twice; AI Operator CLUB). The fourth is Hashtag NoCode 1467334001994239 (lesson 4, "Ganhando dinheiro com Claude"), which c05 now cites. Rule 8.
- "Before any test runs" names one support line, "Get direct answers and support from us". The page has a second, "If you're new to AI, we're here to assist you!", which c11 treats as part of the same decision. Add it.
- A3 and Part D row 4 rest on market map section 3's "member or team count, 6 of 12", whose example ids still include 2032976233999151, which correction 19 found is a "210+ skills" count. The count should be rechecked upstream.
- Advisory: card A's reason line fails the visualize test as a largest-text line (the c08 critic found the same). It runs as the offer line in c08-e04, which is fine.

Interrogation overall: revise (minor). No block remains.

## Concepts

All 11 briefs read "Status: draft, version 2" and "awaits re-review". This is that re-review.

| Concept | Status in file | Critic verdict (this review) | Still open |
|---|---|---|---|
| c01 the quote still in drafts | draft v2 | revise | All v1 items answered. Hook 6 in the brief still reads "No prompt course needed first: the quote in drafts already holds the customer, the job and the price.", which the bank's critic cut as unsourced; the entries carry the fixed line. Sync the brief. Gates: page edits; builds shared today. Video held for footage and Jared's recorded agreement. |
| c02 the Tuesday screen | draft v2, held | block (held) | All v1 items answered on paper. Held until two real dated screens are cataloged with consent (the founder's in writing if from the founders' software or fabrication business). The brief's kicker predates the bank's v2 kicker. Entry headline and long first line still fail nobody-else; kicker legibility unresolved. |
| c03 AI ads are made for desks | draft v2 | block (held) | All v1 items answered. Held for the named founder's OK to be named with their business type, the founders' confirmation that all three businesses are run today, and Jared's approval of the note. Mini-doc needs footage and the filmed founder's written consent. |
| c04 the shop is not the content | draft v2 | revise | All v1 items answered. The brief still says "AI for running the shop, not for making more videos" (text-only body) and "not making videos" (POV strip); the bank's critic found this contradicts the page's "content" item, and the entries now say "not only for making videos". Sync the brief. Gate: four marketplaces confirmed current. |
| c05 the ad with no income number | draft v2, blocked | block | Landing block stands while the tagline says "earn more" (and the page still says "even after it rises to $129", against "no deadline"). The brief's hook 3 still reads "One number in this note: $97 a month", which the bank's critic found false beside "7 days"; the entries say "One dollar figure". Entry hooks, headlines and stranger tests still fail. |
| c06 it did not stick the first time | draft v2, held | block (held) | All v1 items answered. Held until the rejected-result demonstration is cataloged (date, task, what produced it, what changed, data hidden, consent). The name holds only if the recording shows a stalled build. |
| c07 use it on the business you already run | draft v2 | pass (gated) | All v1 items answered. Gates: page edits; R3; the quoted line "Here, you learn from the AI processes we build and use in our businesses." true today. Hook 6 waits on which businesses have a build shown and on the named founder's OK. |
| c08 ninety-seven dollars, and the reason | draft v2 | revise | All v1 items answered. The brief's offer-card kicker ("Operators Workshop: AI, from founders who run businesses") and text-only body ("AI builds from founders who run businesses.") are the versions the bank's critic failed on the stranger test; the entries carry the p6 kicker. Sync the brief. Card B is not in the bank. Hooks 4 and 6 held. No retargeting pool exists. |
| c09 bring the task you keep redoing | draft v2 | pass (gated) | All v1 items answered: worked example labeled made up, member quote off the cards, builds line gated with a fallback the entries use. Gate: page edits. |
| c10 week one, in three steps | draft v2, held and blocked | block | Landing block stands: week one is not written and not on the page (R1); R3 must keep p5 in batch one. Steps are visible held markers; nothing is invented. |
| c11 the list of what we do not do | draft v2 | pass (gated) | All v1 items answered: scoped to the founders, The Claude Club named as the nearest "not for" case, hook 6's reason labeled hypothetical. Gates: page edits including both support lines (if the founders keep them, continuity breaks and this becomes a block); the four "no" items confirmed in practice; builds today. Hooks 3 and 6 held. |

`concepts/matrix.md`:
- Concept names differ from the files: "c03 AI ads are made for people at desks" (file: "AI ads are made for desks"), "c05 we will not tell you what you will earn" (file: "the ad with no income number"), "c06 it did not stick for us the first time either" (file: "it did not stick the first time"), "c10 week one, in three dated steps" (file: "week one, in three steps").
- The "Can it be ready now?" column still says "yes" for c03 and c05. The paragraph below it corrects both; the column does not.
- p1 row, proof cell: "held (needs dated quote email) → static-email-screenshot (better at solution, see c02)"; and the mechanism cell "needs dated quote screen". A quote email is hypothetical (interrogation correction 4) and c02 moved to static-before-and-after. The c02 author flagged this for the builder; it is not done.
- p3 solution row: "rej: SAT 3 (content buyers: AI Video Bootcamp, Arcads, AI Video-Academy)". Two advertisers; AI Video-Academy's only row (2341052899967522) addresses an aspiring creator (c04 critic item 1b). `personas/coverage.md` p3 "served on content (3)" has the same error.
- Header: "The founders say they hold dated screens". Answer 12 says "real software screens", not dated.
- "Cells the market leaves open": "A dated operating artifact as proof: nobody in the sample (section 6)" should cite section 4 and be limited to copy, on-screen text and stills read. "An income refusal and a 'who it is not for' line: 0 of 12" needs the same scope, and The Claude Club's "Strictly for job professionals & business owners. No students." (1101916785561103) is a "not for" line by audience.

`concepts/opposite-pass.md`:
- Row 2: "4 of 12" with ids from three advertisers (as in the interrogation's Part D row 2); "1761940881625624 (Maker School)" is Maker School: AI Automation, not the Maker School pottery studio; the falsifier "below the batch median" should compare arms (the problem card), as the interrogation now does.
- Row 4: ids include 2032976233999151 (a skills count); "the founders hold dated screens, answer 12" and "a real quote email" outrun answer 12; "5 members as of 23 October" lacks the year the interrogation now uses.
- Row 5: "a shop floor or a typed letter moves the product out of the course category before a word is read" reads as fact. The table header labels every inversion a hypothesis, so it passes, but the interrogation now labels the same line hypothetical in place; align.

## Bank

Counts: 32 entries. By status: rendered 3, ready 10, draft 19. By critic verdict: pass 13 (every ready or rendered entry), block 19 (every draft entry), revise 0. Every entry has a critic note, `asset_refs: none` and `ai_media: false`. Every ready entry carries `landing-mismatch` and names its gates in `status_hint`.

Ready and rendered entries (editorial score is a recording priority, never a prediction):

| Entry | Persona, format | Status | Editorial score | Role and gates |
|---|---|---|---|---|
| c01-e01 | p1, static-problem-card | rendered | 8 | lead for c01; page edits; builds shared today |
| c01-e02 | p1, static-text-only-ugly | ready | 8 | second wave; same gates |
| c04-e01 | p3, static-problem-card | ready | 8 | lead for c04; page edits; four marketplaces current |
| c04-e02 | p3, static-text-only-ugly | ready | 8 | second wave; same gates |
| c07-e01 | p1, static-us-vs-them | rendered | 9 | lead for c07; page edits; R3; processes line true today |
| c07-e02 | p1, static-text-only-ugly | ready | 8 | second wave; same gates |
| c08-e01 | p6, static-offer-card | ready | 9 | retargeting only, Sign up; page edits; reason line true today; no pool exists |
| c08-e02 | p6, static-text-only-ugly | ready | 8 | retargeting only; same gates |
| c08-e04 | p6, static-offer-card | rendered | 9 | cold R4 card A, Learn more, CTR only; needs card B, not yet written |
| c09-e01 | p6, carousel-tutorial-steps | ready | 9 | lead for c09; page edits |
| c09-e02 | p6, static-text-only-ugly | ready | 8 | second wave; page edits |
| c11-e01 | p4, static-text-only-ugly | ready | 8 | second wave; page edits incl. both support lines; four items; builds today |
| c11-e02 | p4, static-faq-card | ready | 9 | lead for c11; same gates |

Claims re-checked on the 13: price, "7 days free", "Cancel anytime", "Private", "Skool", the founders' names, "We run real businesses" (quoted without the revenue clause), "Our builds as they happen: the prompts, systems, wins and mistakes behind the work.", "We've made expensive mistakes. Save yourself some headaches.", the two track lines, and "Here, you learn from the AI processes we build and use in our businesses." are verbatim in page.txt. The four marketplaces are owner-provided (brief.md: their ecommerce brand on Etsy, Amazon, Shopify, TikTok) and gated on "current". The four refusals are owner-provided (brief.md; answer 8) and gated on confirmation. Situations (the quote at 10pm, the packing table, the chat tab) are hypothetical and stated as situations, not facts. No number appears without a source, except the held hook "day 8" (see scan).

Findings on the ready entries:
- c08-e01, c08-e02 and c08-e04 are ready or rendered while carrying `urgency-unverified`. The ad copy has no urgency ("No struck-through price above it. No countdown under it."); the flag tracks the landing's "even after it rises to $129". The schema says `ready` requires no blocking flags, and the editorial-score overrides say unverified urgency blocks whatever the score. Revise: move the concern to the landing flag it already has (`landing-mismatch` plus the page-edit gate), or hold the three entries at draft until the page edit ships. Not a truth breach in the ad.
- The `hooks` arrays of ready entries hold lines not cleared to run: c08 hook 6 ("the $97 is charged on day 8", inferred), c08 hook 4 (a failed build), c11 hook 3 ("At 2pm on a Tuesday"), c11 hook 6 (the kitchen-table reason, hypothetical), c07 hook 6 (business types and naming), c04 hook 3 (present tense). Status_hint and the test plan hold them out, but the board shows them beside cleared hooks. Advisory: mark held hooks in the field itself.
- c04-e01 and c04-e02 keep `other:returns-restock-coverage-unsourced` for a line that is gone. Advisory.
- Renders: on-image text equals `fields.json`, the layout file and `layout_fields` for c01-e01, c07-e01 and c08-e04; render reports show no warnings and smallest text about 13 to 14 px at phone width. c08-e04 shows "$97" largest, with the founders' line as the offer line. c07-e01 at 1:1: the offer line sits against the bottom of the two panels with no gap. Advisory.

Entries not ready (all draft, all block):

| Entry | Format | Reason |
|---|---|---|
| c01-e03 | video-pov | Held: reenactment not shot or cataloged; Jared's agreement not recorded; builds today; page edits. The v3 storyboard and notes fix came after the last note; re-reviewed here and accepted; hold stands |
| c02-e01 | static-before-and-after | Held: no cataloged dated screens; headline and long first line fail nobody-else; kicker unreadable over a light screen |
| c02-e02 | video-screen-pip | Held: no screen; Jared's bubble not recorded; headline fails nobody-else; stranger test partial |
| c03-e01 | static-text-only-ugly | Held: the named founder's OK to be named with their business type; three businesses run today |
| c03-e02 | static-founder-note | Held: Jared's approval of the note; the named founder's OK; three businesses today |
| c03-e03 | video-mini-doc | Held: no shop footage; the filmed founder's written consent; crew consent. The v3 headline ("One founder runs a fabrication shop") came after the last note; re-reviewed here and accepted (P/P/P, gated); hold stands |
| c04-e03 | video-pov | Held: reenactment not filmed; Julianna's agreement not recorded. The v3 headline ("The packing table before anything ships") and hook 3 came after the last note; accepted, no coverage claim; hold stands |
| c05-e01 | static-founder-note | Broken landing ("earn more", "$129"); headline fails nobody-else; stranger test fails; Jared's approval; builds today and no-income-to-members confirmations |
| c05-e02 | static-text-only-ugly | Broken landing; hook fails visualize and nobody-else; stranger test fails |
| c05-e03 | video-founder-to-camera | Broken landing; headline fails visualize; stranger test; not filmed; format outside the brief. v3 added the builds gate only; block stands |
| c06-e01 | video-mistakes-and-lessons | Held: demonstration not cataloged. v3 adds a p6 cue to the first-frame strip; accepted on paper, the stranger test waits on real frames; hold stands |
| c06-e02 | carousel-before-during-after | Held: as c06-e01; hook fails nobody-else; kicker backing unresolved. v3 adds the p6 cue; hold stands |
| c07-e03 | video-comparison-alone | Held: dated screen recording of one real task; headline "From founders who run businesses" fails visualize |
| c08-e03 | video-founder-to-camera | Held: Jared not filmed with the real sticky note; hook field carries a stage direction; stranger test partial |
| c09-e03 | video-pov | Held: hands-only shoot and dated sent-folder recording; its long text states the builds line as fact, gated in status_hint |
| c10-e01 | static-three-reasons | Week one not written; broken landing ("Read week one on the About page" points at nothing); R3 |
| c10-e02 | static-whats-inside | As c10-e01 |
| c10-e03 | video-founder-to-camera | As c10-e01, plus filming |
| c11-e03 | video-objection-handling | Held: Jared not filmed. The v3 headline ("The founders will not fix your build") came after the last note; accepted (P/P/P, gated on the four items); hold stands |

## Scan results

The scan flagged 279 lines. Each is resolved below by entry and field. "Page" means verbatim or near-verbatim in `business/site/about/landing/page.txt` ("$97/month", "7 days free, then $97/month", "START FREE TRIAL", "Cancel anytime"). Recurring false positive: every `cta [earn]` hit is the substring in the button "Learn more" (27 entries), not a claim.

| Entry | Hits (field: tokens) | Resolution |
|---|---|---|
| c01-e01 rendered | short, description: 7, free; medium, long: $97, 7, free, customer(s); hooks[5]: customer; image offer_line: $97, 7, free; cta: earn | Legitimate. Price and trial: page. "holds the customer, the job and the price" describes a quote, no claim. "find and keep customers": page track line, verbatim. CTA: "Learn more". |
| c01-e02 ready | as c01-e01; image body: $97, 7, free | Legitimate, as c01-e01. |
| c01-e03 draft | as c01-e01 | Legitimate, as c01-e01 (entry held for footage). |
| c02-e01 draft | short, medium: 7, free, $97; long: $97, 7, free, Customer, saves; image offer_line: $97, 7, free; cta: earn | Legitimate. Price: page. "Customer details are hidden" is a redaction instruction, true only once the screens are cataloged (held). "that AI saves time" sits inside "What they do not show", a refusal. |
| c02-e02 draft | as c02-e01; description: 7, free | Legitimate, as c02-e01. |
| c03-e01 draft | medium: $97, 7, free, customers; long: also income, tonight; hooks[5]: tonight; image body: $97, 7, free; cta: earn | Legitimate. "find and keep customers": page. "It sells no route to clients and no side income.": a refusal, no income claim. "tonight": the viewer's situation ("which one waits until tonight?"), not urgency. Held for the named founder's OK. |
| c03-e02 draft | as c03-e01; description: 7, free; image body: customers; image offer_line: $97, 7, free | Legitimate. Image body quotes the track line ("find and keep customers"). Held. |
| c03-e03 draft | as c03-e01 | Legitimate, as c03-e01. Held. |
| c04-e01 ready | short: 7, free; medium, long: $97, 7, free, customer, only; hooks[0]: customer; image offer_line: $97, 7, free; cta: earn | Legitimate. "last night's customer message": the seller's situation. "not only for making videos": not scarcity; "only" here limits a claim. Price: page. |
| c04-e02 ready | hook, hooks[0], image hook: customer; short, medium, long, image body: $97, 7, free, only; headline: 4; description: 7, free | Legitimate. Headline "Two founders sell on 4 marketplaces": owner-provided (brief.md, their ecommerce brand on Etsy, Amazon, Shopify, TikTok), present tense gated on the founders confirming it is current. |
| c04-e03 draft | short: 7, free, only; medium, long: $97, 7, free, customer, only; hooks[0]: customer; description: 7, free | Legitimate, as c04-e01. Held. |
| c05-e01 draft | medium: $97, 7, free, income; long: also guarantee, result; headline, hooks[2]: $97; image body: income; image offer_line: $97, 7, free | Legitimate as words: "This is not an income plan", "The ad promises no income, no client and no result. There is no guarantee." are refusals; "$97" is the page price. Entry blocked on the landing ("earn more"). |
| c05-e02 draft | hook, hooks[2], image hook: $97; medium, long: as c05-e01; description: 7, free; image body: guarantee ("No client guarantee") | Legitimate as words (refusals, page price). Blocked as c05-e01. |
| c05-e03 draft | as c05-e01 | Legitimate as words. Blocked. |
| c06-e01 draft | hook, headline, hooks[0] to [5], short, medium, long: result; price and trial: $97, 7, free | Legitimate. "a result the founders rejected" is the output of a labeled demonstration, not a performance result; the long text says "Both versions are demonstrations ... The recording does not show the changed version running in a business." Held until the demonstration is cataloged. |
| c06-e02 draft | as c06-e01; image card steps: 1, 2, 3, 4; card 1 kicker: never; card 1 and 3 hooks: result; card 4 offer_line: $97, 7, free | Legitimate. Step numbers are card order. "never became a system" is the p6 situation (inferred). Held. |
| c07-e01 rendered | medium: $97, 7, free, earn; long: also end, today; description: $97, 7, free; hooks[2]: customers; image us_2: today; us_3: end; image offer_line: $97, 7, free; cta: earn | Legitimate. "earn" is inside "learn" in the page quote "Here, you learn from the AI processes we build and use in our businesses." "today's jobs" and "month end" are the viewer's objects, not deadlines. "already has customers" is an identification hook. |
| c07-e02 ready | as c07-e01; image body: $97, 7, free | Legitimate, as c07-e01. |
| c07-e03 draft | as c07-e01 | Legitimate. Held. |
| c08-e01 ready | hook, short, medium, headline, hooks[0] to [4]: $97, 7, free; long: also Save; hooks[5]: $97, 8, free; image kicker: never; image hook, price, terms: $97, 7, free | Legitimate except one. Price, trial, cancel: page. "Save yourself some headaches": page, verbatim. Kicker "never became a system": p6 situation. Problem, held: hooks[5] "the $97 is charged on day 8" is inferred from "7 days free", not on the page; it stays out of every cut until the founders confirm the billing day (status_hint, test plan). Hooks[2] "a new post from the founders each time they build" rides the reason-line gate. |
| c08-e02 ready | as c08-e01; image body: never | As c08-e01; hooks[5] "day 8" is the same held problem. |
| c08-e03 draft | as c08-e01 | As c08-e01. Held. |
| c08-e04 rendered | as c08-e01; cta: earn | As c08-e01; hooks[5] "day 8" held. Only hook 1 runs (test plan). |
| c09-e01 ready | medium: in stock; long: $97, 1, 2, 3, 4, 7, free, customer, in stock, never, review; hooks[0]: customer; image cards 01 to 05 steps: 01 to 05; card 01 body: in stock; card 02 body: 1, 2, 3; card 03 hook: never; card 03 body: 3; card 04 body: customer; card 05 offer_line: $97, 7, free | Legitimate. "Is this in stock?" is labeled "Example (made up)"; not a customer's words. Numbers are step order. "the step that never changes" is an instruction. "customer's name taken out" is a privacy instruction. "The founders do not build it for you or review it." is a refusal (owner-provided). |
| c09-e02 ready | as c09-e01 copy; description: $97, 7, free | Legitimate, as c09-e01. |
| c09-e03 draft | as c09-e01 copy | Legitimate. Held. |
| c10-e01 draft | short: 7, free; medium: $97, 1, 2, 3, 7, free; long: also Save; hooks[1], [3]: 7; hooks[2]: free; hooks[4]: 7, free; image reason_1 to 3: 1, 2, 3; offer_line: $97, 7, free | Legitimate as words. "Step 1: FOUNDERS TO WRITE" and "[held: step 1 ...]" are visible held markers, not invented steps. "The free AI lesson list" describes competitors' offers. "Save yourself some headaches": page. Blocked (week one undefined, broken landing). |
| c10-e02 draft | as c10-e01; hook, image hook: 7, free; image offer_line: $97 | As c10-e01. Blocked. |
| c10-e03 draft | as c10-e01; hook: 7 | As c10-e01. Blocked. |
| c11-e01 ready | hook, headline, hooks[0], hooks[4], image hook: guarantee; short: guarantee, review; medium: $97, 7, free, guarantees, reviews; long: $97, 7, free, guarantee(s); hooks[1]: 7; hooks[5]: guarantee; image body: guarantees, reviews | Legitimate. Every "guarantee" and "review" is a refusal ("No guarantees", "no build reviews"), owner-provided (brief.md; answer 8), gated on the founders confirming the four items. "Before the 7-day trial": page. Problem, held: hooks[5] "The real reason there is no guarantee here: the build happens at your kitchen table, not ours." gives the founders a reason they have not stated (hypothetical); it stays out of every run field (status_hint). |
| c11-e02 ready | short, medium, long, hooks: as c11-e01; image body: members, review | Legitimate. "No. The founders do not review or build members' work." is a refusal; "members" is not a count. Hooks[5] held as in c11-e01. |
| c11-e03 draft | as c11-e01 copy | As c11-e01. Held. |

Numbers and time words the scan did not flag, checked by hand:
- "10pm" (c01, 19 places): the viewer's situation, hypothetical, stated as a situation. Legitimate.
- "At 2pm on a Tuesday the founders are inside their own businesses" (c11 hook 3): founders to confirm; out of batch one. Held.
- "by Friday" (c11 hook 4): the viewer's hypothetical plan, not a deadline. Legitimate.
- "Two founders", "three people who run businesses", "Two tracks": page (three names; two tracks) and brief (two founders sell on the marketplaces). Legitimate, gated where present tense.
- "One real screen. One date. One line the AI got wrong." (c02 hook 5): true only once cataloged. Held.
- "New on the About page: week one" (c10 hook 6): false until R1 ships. Blocked with c10.

No competitor is named in any copy field. No "limited", "only N", "today only", "results", "members" count, percentage, rating or revenue figure appears in any ready entry.

## Test plan

- Placeholders labeled: pass. The five placeholders (gross margin, refund rate, trial-to-paid, months retained, monthly test budget) are named; 81.28, 135.46 and 1,625.53 are marked placeholder-dependent; payback and profit fraction are carried as "owner choice".
- No forecast: pass. Advisory: section 3's "the whole month would yield about 18 trial starts" is conditional arithmetic and labeled so; keep it framed as an upper bound ("at most, if every dollar bought a trial at the target cost"), not an expectation.
- No ROAS: pass. ROAS appears only in "Nothing here predicts ROAS".
- Only ready concepts in the first batch: partly. All 13 batch-one entries passed the critic. But all six batch-one concept briefs still read "draft, awaits re-review". After this review c07, c09 and c11 can move to ready (gated); c01, c04 and c08 need the brief sync above first. c08's cold arm cannot run until card B is written.
- Hook variants: revise. The plan cuts four or five hooks per lead static as separate ads ("Each would be cut as a separate ad"). On a static the hook is the largest on-image text, and only each entry's own hook has a layout, a render and a stranger test. The other hooks need their own layout, render and stranger test before they are cut, or they run only in the primary text with the image unchanged (then the test reads primary text, not the hook). The lead entries' own on-image hooks for c09-e01 ("Before the chat tab: open your sent folder.") and c11-e02 ("Will the founders check my AI build before I use it?") are missing from the cut list, so the critic-passed ads themselves are not in the batch as written.
- Thresholds marked starting points: pass (`"label": "starting points, not benchmarks"`; every rule says "starting point"). Revise on behavior: with `max_frequency: null`, `tools/readout.py` fires "scale" on CPA alone (`freq is None or t.get("max_frequency") is None` passes), so the plan's "Rule 5 ... cannot fire until the founders set one" and the JSON's "_unset" note are wrong for that rule. Set `max_frequency`, or change the plan's sentence. Also: between target and the kill multiple, readout.py returns "iterate landing or offer" while the plan's Rule 7 says hold; and the JSON's `source` names keys `kill_if_cpa_over` and `scale_if_cpa_under` that the file does not contain.
- Gate 1 omits the second support line, "If you're new to AI, we're here to assist you!", which c11's status names.
- Small: "No entry in batch one is a video (see section 5)" should point to section 4.
- Good: the cold set excludes the retargeting entries, and the second ad set is flagged as an exception for the founders to approve; the pixel check is listed as an owner action.

## Evidence limits that bind this run

- No transcripts. All 156 rows are still-reviewed; the 113 transcript files are stubs. Every claim about what an ad contains covers copy, on-screen text and stills only, and every absence claim is scoped that way.
- Customer language: none in run A. All six language banks hold no customer verbatim (coverage.md); market-voiced lines come from competitors' ad copy and are used as insight, never quoted as a customer. Run B (Ridge), per the task line, uses five featured reviews as insight only; it is not reviewed in this report.
- No assets cataloged. `assets/catalog.md` has 0 rows; every `asset_refs` is `none`. The answer-12 assets (store photographs, software screens, deposit and spend screenshots, the rejected-result demonstration) are owner-provided and unverified, with consent unknown.
- Placeholders in finance.md: gross_margin 0.95, refund_rate 0.02, trial_to_paid 0.5, months_retained 4 and monthly_test_budget 1500 are placeholders. payback_months 3 and profit_fraction 0.4 are "owner choice for the example", not the founders' decisions. judge_after_conversions 20 and apify_budget_usd 0 carry no label. Every cost figure in the plan inherits them.
- The "of 12" denominator: `stats-roster.md` counts 12 advertisers that include the Maker School pottery studio (a name collision the market map excludes from synthesis) and Arcads AI's two Pages separately, and leaves out CTtheDisrupter (8 rows). Market map section 1 lists a different set. "N of 12" counts are approximate to that extent; no ad cites one.
- Active-only, capped sample (15 ads per advertiser): days active is not profitability, and no survival rate can be stated.
- The About page was captured on 2026-10-23; "5 members" and the price terms can change.
- No founder was interviewed. Every persona and every "why they buy" line is hypothetical or inferred.

## Open items for the member

- Founders: decide "earn more", "even after it rises to $129", "Get direct answers and support from us" and "If you're new to AI, we're here to assist you!", and ship the page edit before any test.
- Founders: confirm builds are shared as they happen today (gates c01, c07, c08, c11 and the c09 card 5 wording).
- Founders: answer R3 (the category, and whether p5 is in batch one).
- Founders: confirm "Here, you learn from the AI processes we build and use in our businesses." is true today (c07).
- Jared and Julianna: confirm their ecommerce brand sells on Etsy, Amazon, Shopify and TikTok today (c04).
- Founders: confirm no done-for-you, no guarantees, no build reviews and no reply-time promises hold in practice (c11).
- Founders: confirm the billing day before c08 hook 6, and a posted failed build before c08 hook 4.
- Jared: write c08's card B with the same kicker and hook as c08-e04.
- Each founder who appears: written consent, yes or no, to footage, stills or voice, and OK to be named with their business type (c03, c07 hook 6).
- Jared: catalog the answer-12 assets with dates, consent and permissions (unlocks c02, c06 and the videos).
- Jared and Julianna: write week one as three steps true today (c10, R1).
- Founders: set max_frequency and min_ctr, or accept that readout.py scales without a frequency check while max_frequency is null.
- Founders: choose between raising the test budget, lowering judge_after_conversions, or reading direction only.
- Owner: confirm the trial-start event fires on the Skool checkout path.
- Builder: sync c01 hook 6, c04's "not for making more videos", c05 hook 3 and c08's kicker and text body in the briefs to the bank's wording.
- Builder: fix matrix.md names, the ready column, the quote-email cells, the SAT 3 count and the absence scopes; fix opposite-pass rows 2, 4 and 5.
- Builder: in the interrogation, update R2's section 6 counts, A4's conventions sentence and Part D row 2's ids, and add the second support line.
- Builder: rescope `urgency-unverified` on c08-e01, c08-e02 and c08-e04, or hold them at draft until the page edit ships.
- Builder: give every extra static hook its own layout, render and stranger test before cutting it, and add the c09-e01 and c11-e02 on-image hooks to batch one.
- Builder: mark held hooks inside the `hooks` field of ready entries.
- Analyst: recheck market map section 3's member-count row (2032976233999151 is a skills count), the roster denominator, coverage.md's p3 content count, and p4's "urgency cards at 2 advertisers".

Open blocks: 24 (19 draft bank entries; concepts c02, c03, c05, c06 and c10). Each is a hold for a missing asset, consent or founder decision, or a landing block, and is marked as such. This review adds no new block.

Overall: revise. Reviewed 2026-10-23 by critic.

## Re-review (2026-10-23)

Each item raised above, checked against the files as they now stand.

- Interrogation R2 section 6 counts: fixed (none 10, demo 8, social-proof 3, authority 3, testimonial 2, data 1).
- Interrogation A4 conventions row 7 sentence: fixed.
- Interrogation Part D row 2 ids: fixed (five ids, four advertisers, Hashtag NoCode 1467334001994239 added).
- Interrogation second support line in "Before any test runs": fixed; the list and asks name four lines. Advisory: that bullet now reads "They contradict ... and is the drift"; "is" should be "are".
- Member-count row behind A3 and Part D row 4: partly fixed. Market map section 3 drops 2032976233999151, but the count still reads 6 with two example ids; the six advertisers are not named or rechecked.
- c01 hook 6 sync: fixed ("The quote in drafts is not a blank page: ...").
- c04 "not for making more videos" sync: fixed.
- c05 hook 3 sync: fixed ("One dollar figure in this note: $97 a month.").
- c08 kicker and text-only body sync: fixed (the p6 kicker and body from c08-e01 and c08-e02).
- Concept briefs still read "draft, awaits re-review": open (bookkeeping). With the syncs, this re-review passes c01, c04 and c08 (gated) alongside c07, c09 and c11, so all six batch-one briefs can be marked ready; c02, c03, c05, c06 and c10 stay blocked or held.
- matrix.md concept names: fixed.
- matrix.md readiness column: fixed.
- matrix.md quote-email cells: fixed (p1 cells now ask for a real software screen; quote email labeled hypothetical).
- matrix.md header "dated screens": fixed (answer 12 quoted).
- matrix.md absence scopes and The Claude Club line: fixed.
- p3 content-buyer count: partly fixed. matrix.md desire cell and coverage.md's persona table say 2, but matrix.md's p3 identity cell still reads "rej: SAT 3 (the content-buyer identity is served)" and coverage.md's awareness table still says "high for content (3 advertisers reach them)".
- opposite-pass.md row 2: fixed (four advertisers by id; falsifier compares arms).
- opposite-pass.md row 4: fixed (2032976233999151 dropped; count dated 2026; screens no longer called dated; quote email hypothetical).
- opposite-pass.md row 5: fixed (labeled hypothetical).
- c08-e01, c08-e02, c08-e04 `urgency-unverified` on ready entries: fixed (now `other:landing-carries-the-129-rise-line-until-the-page-edit-ships`; ad-bank.csv matches).
- Held hooks inside ready entries' `hooks`: fixed (c04 hook 3, c07 hook 6, c08 hooks 2 to 6, c11 hooks 3, 5 and 6 carry "(held: ...)"; c08 hook 6 "day 8" names the billing-day confirmation).
- c04-e01 and c04-e02 stale flag `other:returns-restock-coverage-unsourced`: open (advisory).
- c07-e01 1:1 offer line tight against the panels: open (advisory).
- Test plan hook variants and the missing c09-e01 and c11-e02 on-image hooks: fixed (batch one is the five lead on-image hooks plus c08's cold arm; other hooks are candidates needing their own layout, render and stranger test).
- readout.py scaling with max_frequency null: fixed (returns "hold" with "set it ... before scaling"; plan Rule 5 updated).
- readout.py "iterate landing or offer" between target and the kill multiple versus the plan's Rule 7 "hold": open.
- thresholds.json `source` names keys `kill_if_cpa_over` and `scale_if_cpa_under` that the file does not contain: open.
- Test plan gate 1 second support line: fixed.
- Test plan "(see section 5)" should point to section 4: open.
- Test plan "about 18 trial starts" framed as an upper bound: open (advisory).
- Roster denominator (stats-roster's 12 includes the pottery studio and both Arcads Pages, omits CTtheDisrupter): open (evidence limit; no ad cites an "of 12" count).
- p4 "urgency cards at 2 advertisers": fixed (now 1, AI Automation Society).
- The seven draft entries revised after their last note: re-reviewed in the bank table above; text fixes accepted, holds stand.
- Founder and owner decisions in "Open items for the member": open, unchanged (page lines, builds today, R3, marketplaces, four refusals, billing day, card B, the filmed founder's consent, catalog, week one, min_ctr and max_frequency, budget path, pixel check).

Open blocks: 24 (19 draft bank entries; concepts c02, c03, c05, c06 and c10), all holds for assets, consent or founder decisions, or landing blocks, each marked as such. No truth-rule breach remains anywhere in the run; the open non-founder items are bookkeeping and advisories.

Overall: pass. Reviewed 2026-10-23 by critic.
