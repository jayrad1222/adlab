# Test plan: Ridge (minimalist wallets), 2026-10-23

This is a hypothesis-testing plan, not a forecast. Every number rests on `business/finance.md`, and every input there is a placeholder except the observed list price, which is itself a placeholder here: finance.md carries price 110 (placeholder), while the captured Aluminum Black product page showed $95 list and $76 on sale on 2026-10-23 (observed; `business/brief.md` addendum). Ridge is a stand-in member. Nothing below predicts revenue, ROAS, conversion rates or results.

## 1. The primary event and why

The primary event is a **purchase**. `plan/economics.md` names it: the model is a one-time product with one order inside a one-month payback window (placeholder), so the first order is the event that pays the ad back. Upstream signals (CTR) are read first, and cost per purchase is judged only at volume.

## 2. Breakeven and target cost per purchase, and the budget per concept

All numbers are placeholder, copied from `plan/economics.md` (computed 2026-10-23):

- Inputs: model=product price=110.0 (placeholder) gross_margin=0.60 (placeholder) refund_rate=0.06 (placeholder) payback_months=1.00 (placeholder) profit_fraction=0.30 (placeholder); aov 120 (placeholder).
- contribution per order = aov x gross_margin x (1 - refund_rate) = 120.0 x 0.60 x (1 - 0.06) = 67.68
- breakeven CPA = contribution over the payback window = **67.68** (placeholder)
- target CPA = breakeven x (1 - profit_fraction) = 67.68 x (1 - 0.30) = **47.38** (placeholder). This is the target cost per purchase.
- test budget per concept = target cost per primary event x conversions needed to judge = 47.38 x 25 = **1184.4** (placeholder)
- conversions needed to judge: 25 (finance.md `judge_after_conversions`, placeholder)

A purchase can be returned within 99 days of the order (Returns & Exchanges page, observed 2026-10-23). So a CPA at 25 purchases is **provisional** until returns are read, which is 99 days after the 25th purchase. A concept can look fine at 25 purchases and not be fine at day 99. The refund_rate of 0.06 is a placeholder hypothesis, and a 99-day window could push real returns above it.

## 3. How many concepts the monthly budget can carry to a CPA verdict

From economics: concepts the monthly test budget can judge = floor(monthly_test_budget / test budget per concept) = floor(6000.0 / 1184.4) = **5** (monthly_test_budget 6000 is a placeholder).

Arithmetic from the same lines: 5 x 1184.40 = 5922.00, which leaves 78.00 of the 6,000 (placeholder). The budget buys 25 purchases per concept only if each concept's CPA lands at the target. At breakeven, 25 purchases cost 25 x 67.68 = 1692.00, more than the budget per concept. A concept that converts above target will reach the spend cap before it reaches 25 purchases. Rule 6 below covers that case. The answer is not zero, so the plan does not fall back to reading signals alone, but the verdict is still provisional until day 99.

## 4. Structure

One campaign. One broad ad set. No interest stacking. Each ad is one hook cut as its own ad; the concept is the unit that is judged.

**Preconditions for every batch-one entry.** Each of these is a run condition carried in the bank (`status_hint`, `risk_flags`) or in the interrogation, and none is a Ridge term:

1. The terms are Ridge's return and warranty terms as captured on 2026-10-23. Ridge says they can change. Recheck the Returns & Exchanges and Warranty Policy pages before each flight and weekly while live. If a term changed, pause the ad that states it.
2. The ad lands on a standard finish only. Never a personalized or limited-edition wallet, which the terms exclude from returns.
3. U.S. audiences only wherever the ad mentions free return or exchange shipping. International customers pay for a tracked return label.
4. (Superseded by precondition 8, which covers c01, c03 and c05; kept so the numbering holds.)
5. c06 only: the $17.95 replacement fee applies to wallets under $150 and is "today's fee", dated; it fits the $95 product only.
6. Continuity: the captured landing carries a sitewide sale banner and the named product showed $76 against $95 list (observed). Entries carry no price, but the banner can pull toward waiting for a sale. Read it as a known mismatch (risk flag `landing-mismatch`), not a hidden one.
7. Added after the release critic, 2026-10-23. Every hook cut as its own ad keeps the dated small print the entry carries. For c01, c03 and c05 that is the dated return line ("Ridge return terms as of 23 October 2026; they can change.") and, on the hooks that say "within 99 days of the order", that phrase in the small print (bank `risk_flags`: c01 hooks 1, 2 and 6, c03 hooks 1 to 3 and day 99, c05 hooks 2, 4 and 6). For c06 the card also carries the review condition and the dated line: "Claims are reviewed and can be denied; Ridge may ask for proof of purchase and photos. Terms as of 23 October 2026; they can change." Any c06 ad that names a fee runs only with that condition, and only for the aluminum Ridge Wallet listed at $95. A hook cut without its small print does not run.
8. Added after the release critic, 2026-10-23. Before running, check that Royal Black (the finish on the landing) can be returned. Apply this to c01, c03 and c05, not only c05. The captured terms exclude personalized, warranty-claim and "certain limited edition items" from returns, and Royal Black returnability was not captured. If it cannot be confirmed, the ads do not run. Record the check and its date in the plan's changelog or the readout notes.

**Batch one: concepts with entries whose status is `ready` or `rendered` (five concepts, eleven entries).** Fewer than six concepts are ready, so the batch is five and is not padded with draft or held entries. All eleven entries are statics or carousels (no video entry is ready), so batch one has no hook rate or hold rate to read. The five concepts match the five the budget can carry.

| Concept | Entries (format, status) | Hooks that would be cut as separate ads |
|---|---|---|
| c01 the bifold that finally split | c01-e01 (static problem card, ready); c01-e02 (static text-only, ready) | problem-naming: "The bifold split at the fold. Next: a Ridge, and 99 days from the order to start a return."; question: "Split at the fold. Buy the same bifold again, or try plates and an elastic band?"; contrarian: "A split bifold does not need a twin. Try Ridge Wallet 2.0: plates and an elastic band."; specific-number: "99 days from the order to decide if the split bifold was the last bifold." |
| c02 twelve cards, then it stops | c02-e01 (static three reasons, ready); c02-e02 (static text-only, ready) | specific-number: "Ridge Wallet 2.0 holds 1 to 12 cards and IDs. Count yours."; question: "How many cards does a working day need? Ridge Wallet 2.0 stops at 12."; contrarian: "Do not ask how slim. Ask how many: Ridge Wallet 2.0 holds up to 12 cards and IDs."; confession: "Ridge Wallet 2.0 stops at 12 cards. Carry 13 and it is the wrong wallet." |
| c03 ninety-nine days told as the switch | c03-e01 (static three reasons, rendered); c03-e02 (carousel timeline, ready) | day-1-vs-30: "Day 1: the order, and the old bifold still in the back pocket. Day 99: the last day to start a Ridge return."; question: "What moves over from the bifold, and what stays behind until day 99?"; specific-number: "99 days, counted from the order, not from the day the box arrives."; callout: "Switching from a bifold to a Ridge: start a return within 99 days of the order if the switch does not take." |
| c05 the old wallet goes in a drawer | c05-e01 (static text-only, ready); c05-e02 (static problem card, rendered) | offer-led: "Keep the old wallet in a drawer. Reach for it, and start a Ridge return within 99 days of the order."; contrarian: "Do not throw out the old wallet. Put it in a drawer until day 99."; pattern-interrupt: "Old wallet. Top drawer. Miss it, and start a Ridge return within 99 days of the order."; specific-number: "99 days from the order. One drawer. The old wallet, kept." |
| c06 the warranty with the fees printed | c06-e01 (static three reasons, rendered); c06-e02 (static text-only, ready); c06-e03 (carousel swipe reveal, ready) | specific-number: "Lost or stolen? Today's fee for a replacement Ridge is $17.95. Up to two times."; confession: "Ridge's lifetime warranty does not cover scratches. A lost wallet is covered, for $17.95 today."; three-reasons: "Three answers from Ridge's wallet warranty: a defective part, free; a lost wallet, $17.95 today; scratches, not covered."; warning: "Before you buy a wallet 'for life', find the fee for a lost one. Ridge's is $17.95 today." |

**Added after the release critic, 2026-10-23.** Only one hook per entry has been built and reviewed (the hook on that entry's rendered layout and critic note). Any extra hook the plan runs as a separate ad needs its own render and critic pass first. Until then, the other hooks listed above are candidates, not ready ads, and batch one runs the eleven reviewed entries as built.

Each concept's bank entries carry six hooks; four per concept are named above (the other two stay in the bank as spares). Hooks within a concept share one angle, so they are iterations of a concept, not independent concepts. Cut them as separate ads, but count and judge the concept.

**Concepts waiting** (all have status draft; none is in batch one):

- c04 the one-take shake: waits on an asset. One uncut phone take (loaded wallet shaken upside down, cards pushed out) must be filmed, cataloged with its raw file and cleared. Nothing in it can run before then.
- c07 the same wallet years apart: waits on consent and an asset. Needs a dated, owner-carried aluminum Ridge (three years or more), its order record, the owner's written consent for paid ads cataloged in `assets/catalog.md`, and Ridge's substantiation of typical wear.
- c08 for the man who says he needs nothing: waits on an owner decision. Ridge must build the landing that shows the three finishes and the exchange line on the first screen, and confirm stock of Royal Black, Alpine Navy and Matte Olive for the flight. The video also needs a cast creator with written consent.
- c09 one price, no code: waits on an owner decision. Ridge must decide to run wallet ads with no sale and no code for the flight. While the landing shows $76 and a sale banner, a $95 card breaks continuity.
- c10 the bulge is the wallet, not the suit: waits on an asset. The same-jacket photo pair (bifold then Ridge, unretouched, dated) must be shot and cataloged. The pairing is a claim only the photographs can make.

Video and photo entries inside the five ready concepts (c01-e03, c01-e04, c02-e03, c03-e03, c05-e03, c06-e04) are draft and wait on footage or a photograph that does not exist. They join a later batch when cataloged.

One gap to name: the interrogation's tests (R1, R4) compare a concept to a catalogue-tile control. No control entry is in the bank. Until one is added, the first week compares the five concepts to each other and to the thresholds below, not to a control.

## 5. Reading order of signals

Definitions from `library/finance/signals-glossary.md`:

1. **Hook rate**: 3-second video plays / impressions. Video only. Batch one has no video, so this is skipped in week one.
2. **Hold rate**: ThruPlays / 3-second video plays. Video only. Skipped in week one.
3. **CTR**: link clicks / impressions. Use link clicks, not "CTR (all)". For these statics and carousels, CTR is the first signal after CPM.
4. **Cost per purchase (CPA)**: amount spent / results, where results is the purchase. Judged only after 25 purchases.

Each signal depends on the one before it, so a failure upstream explains the numbers downstream. Do not read CPA from a concept that has not met the impression floor.

## 6. Decision rules (all thresholds are starting points)

Thresholds are in `plan/thresholds.json`, labeled starting points, not benchmarks, to be changed after the first readout. `library/finance/decision-rules.md` supplies variable names and a template value only for the impression floor and the conversions to judge. It gives 0.00 for hook rate, hold rate and CTR, and 0.0 for frequency, which is no value. Those four are written as `null`, and `tools/readout.py` skips any rule whose threshold is null and says so. The member sets them before the first readout, from the account's own history, not from this plan.

- Impression floor: 2000 (starting point; the template value in decision-rules.md). It is a floor for reading a signal, not a verdict.
- Target CPA 47.38 and breakeven CPA 67.68 (both placeholder). Judge after 25 purchases (placeholder).
- Kill CPA multiple: 1.43 = breakeven / target = 67.68 / 47.38, rounded to 2 places. A CPA above target x 1.43 is a CPA above breakeven.

If-then lines, each a starting point:

- **Rule 0.** If impressions < 2000, then no judgment: report "insufficient impressions" and days remaining. If a concept has run 7 days (decision-rules.md template value for `max_days`, a starting point) and impressions are still < 2000, then report "under-delivery" and check bid, budget, audience and policy status before judging the creative.
- **Rule 1 (statics).** If impressions >= 2000 and CTR < min_ctr and no other rule applies, then kill the concept. Min CTR is null, so this rule is skipped until the member sets it, and the readout says so. Log the concept and hook family as a negative.
- **Rule 4.** If CTR >= min_ctr and purchases >= 25 and CPA > 47.38, then iterate the offer or the landing page. If CPA > 67.68 as well, say plainly that the concept is losing money per purchase in the placeholder economics, not only missing target.
- **Rule 5.** If purchases >= 25 and CPA <= 47.38 and frequency <= max_frequency, then scale in steps and re-read after each. Max frequency is null, so the frequency check is skipped until set. A CPA at or under target at 25 purchases is provisional until day 99 returns are read. Do not scale on it alone.
- **Rule 6.** If purchases < 25, then do not judge CPA. Say "CPA not yet judged" and report the upstream signals, purchases so far and spend. If a concept's spend >= 1184.40 and purchases < 25, then it is converting below the rate the budget assumed: say the budget assumption was wrong, and decide continue or stop from the upstream signals.
- **Rule 7.** If purchases >= 25 and 47.38 < CPA <= 67.68, then hold at current spend. Not losing money in the placeholder economics, not making the profit the member asked for. Do not scale.
- **Terms rule (ours).** If Ridge's return or warranty page changed since 2026-10-23, then pause every ad that states the changed term until the copy is revised and rechecked.

Hook-rate and hold-rate rules (decision-rules.md Rules 1 to 3 for video) are not in force in week one, because no video entry is ready.

## 7. Refresh cadence

- **Weekly:** recheck Ridge's Returns & Exchanges and Warranty Policy pages while any ad is live (a run condition on every entry). Export the Ads Manager report once a week.
- **After week 1:** run the first readout and revise the null thresholds.
- **Every 4 weeks:** rerun `tools/finance.py` and refresh this plan, and refresh the creative if a readout says to.
- **Day 99 after the 25th purchase of any concept:** read returns and recompute that concept's CPA against refund_rate.
- **Early refresh triggers:** a change in a captured term; Ridge names the hero product or confirms its real price, margin or return rate; a sale starts or ends on the landing; a held concept's asset or decision arrives; spend reaches 1184.40 on a concept below 25 purchases.

## 8. What would make this plan wrong

The three inputs most likely to be off (all placeholders):

1. **Price and AOV (110 and 120).** The captured product page showed $95 list and $76 on sale. If real order value is lower, contribution falls, and so do breakeven CPA, target CPA, budget per concept and the number of concepts affordable. Rerun `tools/finance.py` once the member names the hero product and its selling price.
2. **Gross margin (0.60).** It is a typical-DTC guess, not Ridge's number. A sale price makes a percentage margin overstate contribution. A lower real margin lowers breakeven and target CPA together.
3. **Refund rate (0.06).** A 99-day window may raise returns above it. A higher rate lowers contribution, and a CPA judged at 25 purchases can move after day 99. This is why that CPA is provisional.

Also unchanged: the 6,000 monthly budget (placeholder) sets the 5-concept limit. A smaller budget cuts it. No input here is Ridge's own except the observed terms and list price.

## 9. After the first week

Export the Ads Manager report (ad-level, with impressions, link clicks, spend, purchases, frequency) and run `/adlab:readout`. The readout applies the rules above, prints which fired, and skips and names any rule whose threshold is still null.

## Finished / doing now / next

- **Finished:** test plan and thresholds for Ridge. Target cost per purchase 47.38, breakeven 67.68, budget per concept 1184.40, five concepts affordable (all placeholder). Batch one is five ready concepts (11 entries); five are held.
- **Doing now:** nothing; this step is done.
- **Next:** the member sets min CTR, min hook and hold rates, and max frequency from the account's history, and confirms the hero product's real price, margin and return rate. Add a catalogue-tile control to the bank. Run the batch, then `/adlab:readout` after week one.
