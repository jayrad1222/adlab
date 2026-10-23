# Test plan: Operators Workshop

This is a hypothesis-testing plan, not a forecast. Every number rests on `business/finance.md`, whose inputs are placeholders where marked (gross margin, refund rate, trial-to-paid, months retained, monthly test budget). Nothing here predicts ROAS, revenue, conversion rates or results. No concept is judged until a readout says so.

Computed figures come from `plan/economics.md` (2026-10-23). Where this plan says placeholder, replace the input in finance.md with an observed value and rerun `tools/finance.py`.

## 1. Primary event and why

The primary event is a **trial start** (economics.md: "primary event = trial start"). Operators Workshop is a $97 a month Skool community with a 7-day free trial. A trial start is the first event an ad can cause, and it is readable within days. A paid member only exists after day 7, so cost per paid member cannot be read in a week-long test. The step from trial to paid rests on `trial_to_paid = 0.5`, which is a placeholder (hypothesis, no cohort yet).

## 2. Breakeven and target cost per primary event

Formula lines copied from economics.md. Inputs: model=membership, price=97.0, gross_margin=0.95 (placeholder), refund_rate=0.02 (placeholder), payback_months=3.00 (owner choice), profit_fraction=0.40 (owner choice), trial_to_paid=0.50 (placeholder), months_retained=4.00 (placeholder).

- contribution per paid member over the payback window = period_price x gross_margin x min(months_retained, payback_months) x (1 - refund_rate) = 97.0 x 0.95 x min(4.00, 3.00) x (1 - 0.02) = 270.92
- breakeven CPA per paid member = contribution over the payback window = 270.92
- breakeven cost per trial start = breakeven CPA x trial_to_paid = 270.92 x 0.50 = **135.46** (placeholder-dependent)
- target CPA per paid member = breakeven x (1 - profit_fraction) = 270.92 x (1 - 0.40) = 162.55
- target cost per trial start = **81.28** (placeholder-dependent)
- test budget per concept = target cost per primary event x conversions needed to judge = 81.28 x 20 = **1625.53**

`judge_after_conversions = 20` is set in finance.md and is not marked placeholder. Simple LTV (361.23) is a ceiling, not a target, and this plan does not use it.

## 3. How many concepts the monthly budget can carry to a CPA verdict

**Zero.** economics.md: floor(monthly_test_budget / test budget per concept) = floor(1500.0 / 1625.53) = 0. The $1,500 monthly test budget is a placeholder, and at that figure it cannot carry one concept to a CPA verdict.

A second way to see it, my arithmetic from the same lines: $1,500 / $81.28 = 18.45. If every dollar bought a trial start at exactly the target cost, the whole month would yield about 18 trial starts across all concepts together, fewer than the 20 one concept needs.

What the plan reads instead, in this order:

1. Hook rate and hold rate, for video only. No entry in batch one is a video (see section 4), so these two do not apply to batch one.
2. Link CTR, once a concept passes the impression floor.
3. Trial starts and cost per trial start, as a **direction, not a verdict**. Compare each concept's cost per trial start with 81.28 and 135.46 and say "above", "between" or "below", then print "CPA not yet judged" until conversions reach 20.

To get a CPA verdict the options are (economics.md): raise the budget, or lower judge_after_conversions and accept a noisier read. Both are the founders' call. This plan does not lower either on their behalf.

Starting split, arithmetic on the placeholder budget: $1,500 / 5 concepts in the cold ad set = $300 each, or $250 each if the sixth joins. This is a division of a placeholder, not an expected result. The plan sets no daily budget per ad because CPM is unknown until ads deliver.

## 4. Structure

One campaign. One broad ad set. No interest stacking. Optimize for the primary event (trial start) once the pixel or event is confirmed to fire; until then the campaign cannot be read on trial starts.

### Gates that must clear before any ad runs

Batch one is **ready once these gates clear**. Nothing runs before them. Every entry below passed the critic (status `ready` or `rendered`), and every one still waits on the first gate.

1. **About-page edits** named in `business/interrogation.md` ("Before any test runs"). The founders decide each, and the page edit ships before any test:
   - the tagline's "earn more", an income implication the ads cannot sit beside;
   - "even after it rises to $129", a stated rise with no date or commitment in offer.md;
   - "Get direct answers and support from us", the support line, which contradicts the ads' no-response-time position;
   - the second support line, "If you're new to AI, we're here to assist you!", which has the same problem (added after the release critic, 2026-10-23).
2. **Founders confirm a line is true today**, per concept (listed in section 5).
3. **Pixel or event check**: trial start fires on the Skool checkout path. Not verified in any file I read. Owner action.
4. **R3 answered** by the founders (the category decision), which c07 names as a gate.

### Batch one: ready concepts

All 13 entries are static or carousel. None is a video. Six concepts, 13 entries. Within a concept the entries are format arms of the same copy: the designed card and the text-only version, with identical hooks, so format is the only difference. **Lead entry** = the one cut first. The text-only entries run as a second wave, or earlier if the founders raise the budget.

Each lead entry's **on-image hook** (the hook already laid out on its card, from the entry's `hook` field) is the ad batch one cuts (added after the release critic, 2026-10-23). The lead entries' on-image hooks are: c01-e01 hook 1; c04-e01 hook 4; c07-e01 hook 1; c08-e04 hook 1; c09-e01 hook 3 (carousel card 1); c11-e02 hook 5 (the FAQ card's question). The c09 and c11 lines were first written into this section; they now sit in their concepts' hook lists (concept briefs v3), where the critic reviews them with the rest of the concept (moved 2026-10-23 after the `/adlab:review` run).

Every other hook listed below is a **candidate**, not a batch-one ad. Before a candidate is cut as its own static ad it needs its own layout, its own render and its own stranger test (added after the release critic, 2026-10-23). The lists are the candidates to build next, in the order a readout makes room for them.

**c01, the quote still in drafts** (entries c01-e01 static-problem-card, rendered; c01-e02 static-text-only-ugly, ready; lead c01-e01). Waits on the founders confirming builds are shared as they happen today.
- Hook 1: "The quote is still in drafts. It is 10pm." [problem-naming]
- Hook 3: "For the owner who writes every quote themselves." [identification]
- Hook 4: "Which job is still waiting on a quote from you?" [question]
- Hook 6: "The quote in drafts is not a blank page: it already holds the customer, the job and the price." [contrarian-or-myth]

**c04, the shop is not the content** (c04-e01 static-problem-card, ready; c04-e02 static-text-only-ugly, ready; lead c04-e01). Waits on the founders confirming the four marketplaces are current. Hook 3 (present-tense seller claim) stays out until they do.
- Hook 1: "The return, the restock and last night's customer message, all before the first new listing." [problem-naming]
- Hook 2: "Which one is still open: the return, the restock or the message from last night?" [question]
- Hook 4: "Product videos vs the shop's actual morning: messages, returns, restock." [comparison]
- Hook 5: "POV: the packing table, an open inbox, and nothing shipped yet." [pov]

**c07, use it on the business you already run** (c07-e01 static-us-vs-them, rendered; c07-e02 static-text-only-ugly, ready; lead c07-e01). Waits on the founders answering R3 and confirming the quoted line "Here, you learn from the AI processes we build and use in our businesses." is true today.
- Hook 1: "Two places to put AI: a stranger's pitch deck, or your own drafts folder." [comparison]
- Hook 2: "The first AI build does not need a client. It needs the invoice folder on your desk." [contrarian]
- Hook 3: "For the shop that already has customers, a phone that rings and a drafts folder." [identification]
- Hook 4: "Which business gets the AI first: a stranger's, or the one you open up every morning?" [question]
- Hook 5: "POV: the AI tab is open on your own job list, not on a client pitch." [pov]

**c09, bring the task you keep redoing** (c09-e01 carousel-tutorial-steps, ready; c09-e02 static-text-only-ugly, ready; lead c09-e01). Waits on the About-page edits only (status_hint names no further gate).
- Hook 1: "The same customer reply, typed by hand again, with the chat tab open beside it." [problem-naming]
- Hook 4: "Not a new tool: the first build is the email you keep rewriting, written out as steps." [contrarian]
- Hook 5: "POV: the chat tab is closed and a notepad holds the steps of the email you rewrite." [pov]

**c11, the list of what we do not do** (c11-e01 static-text-only-ugly, ready; c11-e02 static-faq-card, ready; lead c11-e02). Waits on the About-page edits (both the support lines and the rest), on the founders confirming the four items hold in practice, and on them confirming builds are posted as they happen today. Hook 6 stays out of every run field until the founders confirm it is theirs. Hooks are listed by number and family, not quoted, because their text states what the community does not do; read them in the entry.
- Hook 1 [pattern-interrupt], hook 2 [warning], hook 4 [callout]. Hook 5 is the lead ad's on-image hook, so it is not a candidate.
- Hook 3 [confession] stays out of batch one: it states a timing position the About page's support line currently contradicts, and it is safer to add after the page edit is confirmed.

**c08, ninety-seven dollars, and the reason.** Split in two, and the split matters.
- *Retargeting version*: c08-e01 static-offer-card (ready, Sign up) and c08-e02 static-text-only-ugly (ready). Hooks 1, 2, 3 and 5. This version needs a retargeting pool. No ads have run and the page has 5 members, so the pool does not exist and probably cannot reach the impression floor. It is **not** put in the cold broad ad set: mixing a warm pool into a cold set would contaminate both reads. It enters a separate retargeting ad set only when a pool exists, and that second ad set is a deliberate exception to "one broad ad set", for the founders to approve. Hook 4 (a failed build) waits on the founders confirming a failed build is posted; hook 6 (billing day) waits on the founders confirming the billing day.
- *Cold R4 test card A*: c08-e04 static-offer-card (rendered, Learn more). It runs only against card B, the bare "$97 a month, 7-day free trial, cancel anytime" card. **Card B is not in the bank yet**, so this arm cannot run until it is written, carrying the same kicker and hook as card A so the test reads only the reason line. One hook only (hook 1), read on CTR only. It waits on the founders confirming the reason line is true today.

Count: five concepts in the cold ad set (c01, c04, c07, c09, c11) with one lead-entry on-image hook ad each (5 ads), plus c08's cold arm when card B lands. The other hooks listed under each concept are candidates until built and tested (added after the release critic, 2026-10-23). Counting c08, **six concepts are in batch one**. All of it is conditional on the gates above.

### Concepts waiting

Not in batch one. Their entries are draft or held, and the plan does not pad the batch with them.

| Concept | Waits on |
|---|---|
| c02, the Tuesday screen | An asset: a real screen cataloged with its date, the AI's wrong line, the changed version, customer data hidden and consent (assets/catalog.md has 0 rows). Founders confirm the business is run today. |
| c03, AI ads are made for desks | Consent and owner decision: the named founder's OK to be named with their business type, Jared's approval of the note's words, founders confirm all three businesses are run today. Shop footage does not exist. |
| c05, the ad with no income number | Owner decision: blocked until "earn more" leaves the About page's first line. Jared has not approved the words or filmed the take. |
| c06, it did not stick the first time | An asset: the rejected-result demonstration is not cataloged. |
| c10, week one in three steps | Owner decision: the founders have not written week one as three steps true today (R1). R3 must also keep p5 in batch one. |
| Video entries of c01, c04, c07, c08, c09, c11 | Footage: nothing is shot or cataloged (assets/catalog.md is empty). Some also wait on a person's agreement (c04 on Julianna). |

## 5. Reading order of signals

Definitions from the signals glossary. Read in this order and stop at the first rule that fires, because each signal depends on the one before it.

1. **Hook rate** = 3-second video plays / impressions. Video only. Skipped in batch one.
2. **Hold rate** = ThruPlays / 3-second video plays. Video only. Skipped in batch one.
3. **CTR** = link clicks / impressions, the link version, not "CTR (all)". For statics and carousels this is the first real signal after CPM, and it is the one that carries batch one.
4. **Cost per trial start** = amount spent / results, where results must be trial starts and not an upstream event. Read only at volume. Below 20 conversions it is a direction.

CPM, CPC, landing conversion rate and frequency are context, not verdicts. A good CTR with a poor landing conversion points at the page or the offer, not the ad.

## 6. Decision rules (all starting points)

Thresholds are in `plan/thresholds.json`. Each rule prints the numbers that fired it. All are **starting point** values, not benchmarks.

- **Rule 0, not enough data (starting point).** If impressions < 2000 (impression_floor), then no judgment: print "insufficient impressions" and the days left to max_days. If days_running >= 7 (max_days, from the decision-rules file) and impressions < 2000, then the platform is not serving the ad: check bid, budget, audience size and policy status before judging the creative.
- **Rule 1, kill on a static (starting point).** If impressions >= 2000 and ctr < min_ctr, then kill the concept version and log it as a negative. **min_ctr is null.** The decision-rules file supplies no value and this plan invents none. Until the founders set min_ctr, the readout prints CTR and does not fire this rule. Suggested path: set it after the first readout, from the spread of the concepts' own CTRs, and write the reason down.
- **Rule 1 and 2, hook and hold (starting point), video only.** If hook_rate < min_hook_rate then kill or iterate the hook. If hook_rate >= min_hook_rate and hold_rate < min_hold_rate then iterate the body. Both minimums are null, and no batch-one entry is a video, so neither fires.
- **Rule 6, minimum volume (starting point).** If conversions < 20 then print "CPA not yet judged". Show the upstream signals, the conversions so far and the spend still needed. Given section 3, this is the rule every concept will meet in the first month at the placeholder budget. If spend >= 1625.53 and conversions < 20 then the budget assumption was wrong: say so, and apply the upstream rules.
- **Rule 4, offer or landing (starting point).** If CTR is at or above min_ctr and conversions >= 20 and cost per trial start > 81.28 then iterate the offer or the landing page, not the ad. If cost per trial start > 135.46 (the breakeven cost per trial; kill_cpa_multiple 1.67 x the target in thresholds.json) then the concept version is losing money per trial: stop spend on that version and iterate.
- **Rule 7, between target and breakeven (starting point).** If conversions >= 20 and 81.28 < cost per trial start <= 135.46 then iterate the landing page or the offer and do not scale (`tools/readout.py` prints "iterate landing or offer" in this range; aligned after the release critic, 2026-10-23).
- **Rule 5, scale (starting point).** If conversions >= 20 and cost per trial start <= 81.28 (target_cpa) and frequency <= max_frequency then raise budget in steps and re-read after each step. **max_frequency is null** in finance.md, so this rule does not fire. It says "set max_frequency before scaling" instead, matching the readout tool's change (added after the release critic, 2026-10-23).

The two cost figures are per trial start and both depend on the trial_to_paid placeholder. Rules 4, 5 and 7 cannot fire in month one at the placeholder budget (section 3).

No concept is called anything but "read", "iterate", "hold", "kill" or "not yet judged" until a readout says more.

## 7. Refresh cadence

Starting points, change after the first readout.

- **Read weekly.** The first readout is day 7 (max_days = 7), the same day the impression floor is checked.
- **Refresh creative every 4 weeks** at the earliest, or when a concept has been killed or iterated and its replacement is ready.
- **Early refresh triggers:**
  - a concept or entry still under the impression floor at day 7 (under-delivery, check before refreshing);
  - frequency passes the ceiling once the founders set one;
  - a gate stops being true: the founders stop sharing builds as they happen, a marketplace is no longer current, or the About page changes. The affected entries stop the same day;
  - an observed cohort replaces trial_to_paid or months_retained, which changes both cost figures and means thresholds.json is regenerated;
  - the founders raise the budget or lower judge_after_conversions.

## 8. What would make this plan wrong

The three inputs most likely to be off, all placeholders:

1. **trial_to_paid = 0.5.** It converts breakeven and target CPA per paid member into per-trial figures by direct multiplication. If the true rate is lower, both 135.46 and 81.28 fall in proportion and ads that read as "between" or "below" are actually dearer than they look. If higher, the reverse. The first cohort sets the baseline; until then both figures are hypotheses.
2. **months_retained = 4.** The contribution formula uses min(months_retained, payback_months). With payback at 3, any true value of 3 or more changes nothing in breakeven or target. A true value below 3 lowers contribution, breakeven and target together. So this input matters only if retention is shorter than the payback window, and nobody has a cohort to say.
3. **monthly_test_budget = 1500.** It decides the count of concepts to a CPA verdict, which is zero here. A larger budget raises that count and makes Rules 4, 5 and 7 live. A smaller one leaves the plan reading CTR only.

Also worth watching, not in the top three: gross_margin = 0.95 and refund_rate = 0.02 are placeholders. Margin excludes founder labor, so the true figure may be lower.

## 9. After the first week

Export the Ads Manager report (by ad, with impressions, link clicks, results, spend, frequency and, for any video, 3-second plays and ThruPlays) and run `/adlab:readout`. If a floor is still null, say so to the founders in one line and set it from that readout.

## Finished / doing now / next

- **Finished:** economics computed; thresholds written with three nulls where the library gives no value; batch one chosen from the 13 critic-passed entries across six concepts; waiting concepts listed with what each waits on.
- **Doing now:** nothing is running. Batch one is ready once the About-page gates clear and the founders confirm each concept's line is true today.
- **Next:** the founders decide the three About-page lines and confirm the per-concept lines (one decision list); Jared writes c08's card B; the founders choose between raising the budget, lowering judge_after_conversions, or reading direction only; then launch, and run `/adlab:readout` after week one.
