# Ad Lab framework library: the seed

Prepared October 22, 2026. This is the knowledge seed Opus expands into `adlab/library/`. It is written for a model to work from, so it is dense. Attributions are to the author or book; nothing here quotes protected text at length. Where I am confident a list is complete I say so; where it should be checked against the primary source before shipping, I say that too.

## 0. How Opus should turn this into `library/`

One file per framework, same skeleton every time, so the agents can read any of them the same way:

```
# <Framework name> (<author, work, year>)
## The idea in three sentences
## Spot it in a competitor ad (detection cues, with an example of what the cue looks like in copy or visuals)
## Use it in ours (concrete moves, per format: hook, body, static, video, landing)
## How it backfires (abuse, policy risk, when the mechanism reverses)
## Questions it adds to the interrogation
## Related: [[other-framework]]
## Sources (author/book/talk; link if public)
```

Rules for the library: no invented statistics; no "studies show" without a named study; mark contested claims as contested; every detection cue must be something an ad-analyst agent can actually look for in copy, transcript or frames. The `librarian` agent appends observed patterns from member runs to `library/observed/` with the ad IDs, never into the canonical files.

---

## 1. Rory Sutherland (the spine of the interrogation)

Rory Sutherland is Vice Chairman of Ogilvy UK, co-founder of its behavioural science practice, author of *Alchemy: The Surprising Power of Ideas That Don't Make Sense* (2019), and in 2025 and 2026 the most-heard voice on marketing podcasts (Diary of a CEO, Modern Wisdom, Rogan, plus his own Ogilvy work). His frame is the one the pasted interrogation prompt is written in.

### 1.1 The rules from Alchemy (his own list, paraphrased; this list is complete as far as I know, verify ordering against the book)

1. The opposite of a good idea can also be a good idea.
2. Don't design for average.
3. It doesn't pay to be logical if everyone else is being logical.
4. The nature of our attention affects the nature of our experience.
5. A flower is simply a weed with an advertising budget.
6. The problem with logic is that it kills off magic.
7. A good guess which stands up to observation is still science. So is a lucky accident.
8. Test counterintuitive things, only because no one else will.
9. Solving problems using rationality is like playing golf with only one club.
10. Dare to be trivial.
11. If there were a logical answer, we would have found it already.

### 1.2 The working concepts (each becomes a library file)

- **Psycho-logic.** People make decisions through a parallel logic that handles meaning, risk, status and context, and then post-rationalize. The ad's job is to satisfy psycho-logic first. Detection cue: an ad that "makes no sense" on a feature comparison but has run for 200 days is usually satisfying psycho-logic. Use: ask what the customer needs to *feel* is true before the rational case can land.
- **Costly signaling.** Advertising works partly because it is expensive and visible; the effort itself signals confidence and commitment. Detection cue: production value, celebrity, big-media placements, long-running campaigns, physical-world gestures. Use: a visible, effortful gesture (a hand-written note, a founder who shows up every day, a guarantee with teeth) can carry more trust than a claim. Backfire: cheap-looking signals of expense read as fake.
- **Satisficing, not maximizing.** Buyers try to avoid a catastrophe, not to pick the optimum. "Nobody got fired for buying IBM." Detection cue: safety language, "trusted by," guarantees, brand-name reassurance. Use: remove the fear of looking stupid before adding the dream.
- **Context changes value.** The same product is worth different amounts in different contexts (the Eurostar example: instead of making the train faster, make the journey better; Uber's map lowers anxiety, not wait time). Detection cue: ads that change *when* or *where* the product is imagined. Use: move the product into a new context in the hook.
- **Perception is a legitimate lever.** Psychological value is real value. The waiting display at the bus stop does not shorten the wait; it removes the uncertainty, which was the real cost. Use: find the uncertainty in the customer's situation and remove it visibly.
- **The doorman fallacy.** Efficiency drives strip out the thing that carried meaning (replace the doorman with an automatic door, lose the security, the status and the welcome). Interrogation question: what inefficiency in your offer is actually the point?
- **Don't design for the average.** The average customer does not exist; extremes reveal the real jobs. Use: personas are situations, and the best hooks speak to an edge case so specifically that the middle recognizes itself.
- **The opposite pass.** For every convention in the category, write its inverse and ask whether it is also a good idea (Red Bull: a small can, a strange taste, a high price; all signals of potency). This is a mandatory step in `/adlab:angles`.
- **Ask the question nobody asks.** Not "how do we sell more" but "why would anyone not buy this, and what would make the not-buying feel risky?"
- **Price is information.** A higher price can raise perceived efficacy (placebo effects scale with price). Charm pricing signals "deal," round pricing signals "quality." Interrogation question: what does your price say about you before anyone reads your copy?
- **Status and identity.** Most purchases are partly about who the buyer gets to be, and to whom. Interrogation question: after buying, who does the customer get to look like, and in front of whom?
- **Rituals and ownership.** Products with rituals (the way you make the drink, the unboxing, the weekly check-in) are stickier. Interrogation question: what is the ritual of using your product, and does the ad show it?
- **Test counterintuitive things.** Because competitors will not, the counterintuitive test is the cheapest uncontested experiment. The library should keep a list of "counterintuitive tests worth running" per category.
- **Make the invisible visible.** Trust is built by showing the work (the glass-walled kitchen). Use: process, behind-the-scenes, the founder's hands.
- **Psychological moonshots.** Small changes in framing that produce large changes in behaviour (naming, defaults, the order of information). The interrogation asks for three per business.
- **Chief Psychology Officer.** His 2026 line: every company needs one, because the finance and engineering views have one each and the human view has none. Ad Lab's `psychologist` agent is that role.

### 1.3 The interrogation (the pasted prompt, operationalized)

The pasted prompt's stance is kept verbatim in spirit: treat the customer as status-aware, story-driven, ambiguity-averse, emotionally interpretive, deciding through cues, habits, shortcuts, social meaning, fear, aspiration, trust, identity and post-rationalization; assume the business does not have a marketing problem but a perception, trust, category, status, context, pricing-signal, social-proof, ritual or legibility problem.

Ad Lab adds three things:

1. **Grounding.** The interrogation runs after the decode, so each challenge cites ad IDs and persona files. "Nine of twelve competitors open with the same claim; here they are."
2. **A fixed output schema.** (a) Diagnosis: which of the nine problems it really is, in order, with evidence. (b) The seven highest-leverage recommendations, each with: the mechanism (named framework), the evidence (ad IDs, persona, interrogation answers), the cheapest test, the falsifier (what result would prove it wrong), the risk (policy or truth). (c) Three psychological moonshots. (d) The opposite pass on the category's top five conventions.
3. **A tone rule.** Ruthless is fine; invented is not. Every reframe must be testable, and every "people do X" claim must either name its source or be labeled a hypothesis.

Suggested interrogation questions for the intake (two batches, defaults allowed):

- Who is the customer trying to look like after buying, and to whom?
- What does the customer do instead today, including nothing? What does "nothing" cost them, in their words?
- Which claim on your site could a competitor make word for word?
- What is the worst thing a buyer fears will happen if this goes wrong? What would make them look foolish?
- What is the one thing you do that is inefficient on purpose, and why?
- What is the ritual of using it? What does the first week look like?
- What does your price say about you?
- Which customers are wrong for you, and how would an ad repel them?
- When someone decides to buy, what just happened in their life?
- What would you have to be true about you that none of your competitors can say?
- If you had to make the product more expensive and better, what would you add?
- Which proof do you have that you are not using because it feels too small or too odd?

---

## 2. The behavioural science bench (Sutherland's peers)

### 2.1 Richard Shotton (Ogilvy lineage; *The Choice Factory*, 2018; *The Illusion of Choice*, 2023)

Shotton's value is that each bias comes with an applied experiment. *The Choice Factory* covers 25 biases chosen for commercial relevance; *The Illusion of Choice* covers sixteen and a half more. The lists below are the ones I am confident appear; check the tables of contents before publishing the library as complete.

From *The Choice Factory* (selected): the fundamental attribution error (context beats personality; target moments, not people); social proof and its dangerous inverse, negative social proof ("most people don't…" normalizes the bad behaviour); habit (hard to break except at life transitions, which is why "new job, new baby, new city" moments are targeting gold); the pain of payment; the danger of claimed data (people misreport why they buy; watch behaviour); mood and media context (the same ad performs differently next to different content); price relativity and anchoring; the primacy effect; expectancy (branding changes taste); confirmation bias; overconfidence; the wisdom of crowds; the pratfall effect (admitting a flaw raises trust; "it's expensive, and here is why"); the winner's curse; scarcity; the Goldilocks effect (three options, the middle sells); the power of "because" (Langer: a reason, even a weak one, raises compliance); charm pricing (99 endings read as cheaper and as "deal"); the curse of knowledge (experts write for experts); distinctiveness (Von Restorff: the odd one out is remembered); the replication caveat (not every bias replicates; prefer the robust ones).

From *The Illusion of Choice* (selected): make it easy (friction is the biggest lever and the most ignored); make it precise (precise numbers are more believable than round ones: 1,214 not 1,200); keep it concrete (concrete words are remembered, abstractions are not); the peak-end rule (design the best moment and the last moment); the generation effect (let the audience complete the thought; they remember what they generate); the red sneakers effect (deliberate nonconformity signals status if the person could clearly conform); the Keats heuristic (rhymes feel truer); extremeness aversion; denominator neglect; the power of free; bad is stronger than good (loss frames carry more weight, use with care under policy); choice overload; humour as a trust and recall device.

Detection cues for the ad-analyst: precise numbers, admitted flaws, "because," three-tier offers, 99 endings, rhyming lines, "most people" lines, odd-one-out visuals, free-shipping emphasis, a single clear next step.

### 2.2 Robert Cialdini (*Influence*, 1984/2021; *Pre-Suasion*, 2016)

Seven principles (the 2021 edition adds unity): reciprocity, commitment and consistency, social proof, liking, authority, scarcity, unity (shared identity: "people like us"). *Pre-Suasion* adds the privileged moment: what you draw attention to just before the message becomes important, and attention equals importance. Use: the frame before the hook (the first visual sets what the viewer thinks the ad is about). Backfire: fake scarcity and fake authority are now detected by audiences and by platform policy.

### 2.3 Kahneman, Tversky, Thaler, Ariely

System 1 and System 2; prospect theory (losses weigh roughly twice gains; reference points matter more than absolutes); anchoring; framing (90% lean versus 10% fat); the endowment effect (trials and "yours already" language); status quo bias and defaults (the default option wins; make the desired path the default); availability (vivid, recent, concrete examples feel more probable); hyperbolic discounting (today beats later: why "start today" and immediate bonuses work); mental accounting (which budget does this come from; reframe the budget); the peak-end rule; the IKEA effect (effort invested raises valuation; onboarding that asks for a small effort increases retention); the power of free (zero price is a category, not a discount); the decoy effect (a third option that makes the target look best); pain of paying (bundle, prepay, subscription smooths it).

### 2.4 Phil Barden (*Decoded*, 2013)

Explicit goals (what the product does) versus implicit goals (what it means: security, autonomy, excitement, adventure, discipline, enjoyment). The strongest ads hit an implicit goal through a concrete signal. Detection cue: what does the visual world of the ad promise beyond the product? Use: pick the implicit goal per persona and make the visual world match it.

### 2.5 Jonah Berger (*Contagious*, 2013) and Chip and Dan Heath (*Made to Stick*, 2007)

STEPPS: social currency, triggers, emotion (high-arousal emotions travel: awe, anger, anxiety, amusement; sadness does not), public (visible use), practical value, stories. SUCCESs: simple, unexpected, concrete, credible, emotional, stories. Use both as checklists for the critic agent.

### 2.6 Bob Moesta and Clayton Christensen (Jobs to be Done)

The four forces of progress: the push of the current situation, the pull of the new solution, the anxiety about the new, the habit of the present. A sale happens when push plus pull exceeds anxiety plus habit. Persona files must fill all four. Hooks that name the push ("still doing X by hand at 11pm") and bodies that lower anxiety ("here is exactly what the first week looks like") map directly to this.

### 2.7 Seth Godin

The smallest viable audience; "people like us do things like this" (identity as the engine of adoption, which is Sutherland's status point in different words); permission; the purple cow (remarkable means worth remarking on). Use: a persona is a "people like us" group; the ad names the "things like this."

### 2.8 Byron Sharp (*How Brands Grow*), Les Binet and Peter Field (*The Long and the Short of It*), Mark Ritson

Sharp: growth comes from reach among light and non-buyers, mental availability (being thought of in the buying situation) and physical availability (being easy to buy), and distinctive brand assets (face, colour, sound, shape) that make the ad attributable. Binet and Field: brand building (emotional, broad, slow, compounding) and activation (rational, targeted, fast, decaying) need each other; the 60/40 split is a guide for large brands, not a law for a small one. Ritson: diagnosis first (research), then strategy (who, what position, what objectives), then tactics (ads); most small businesses start at tactics. Ad Lab's order (intake, competitors, decode, personas, interrogation, angles, bank, plan) is Ritson's order. Detection cue: does the competitor have any distinctive asset at all, or are they a stock-photo brand?

### 2.9 April Dunford (*Obviously Awesome*, 2019)

Positioning components in order: competitive alternatives (including "do nothing" and spreadsheets), unique attributes, the value those attributes enable, the customers who care most, the market category you choose to be judged in. The category choice is a Sutherland lever (the same product in a different category has a different reference price). Interrogation question: what category are you letting the customer judge you in, and is there a better one?

---

## 3. The direct-response canon

### 3.1 Eugene Schwartz (*Breakthrough Advertising*, 1966)

The five stages of awareness: unaware; problem-aware; solution-aware; product-aware; most aware. Each needs a different opening: the most aware get the offer and the price; the product-aware get the proof and the difference; the solution-aware get the mechanism; the problem-aware get the problem named better than they can name it; the unaware get a story or an identity.

The five stages of market sophistication and the required move: (1) a new market: a simple direct claim works; (2) competitors copy the claim: make the claim bigger; (3) claims stop working: introduce a mechanism ("how it works"); (4) mechanisms get copied: a better or easier mechanism, or a bigger promise for the mechanism; (5) the market is exhausted: identification (the ad is about who the buyer is) and experience (the ad shows the feeling of the product). Ad Lab's market map states the stage and the move. Most categories members will enter are stage 3 to 5.

Also from Schwartz: you cannot create desire, only channel existing mass desire onto a product; the headline's job is to select the reader and promise the payoff of reading.

### 3.2 Claude Hopkins (*Scientific Advertising*, 1923), David Ogilvy, John Caples

Hopkins: specifics beat generalities; a reason-why; test everything; the ad is a salesperson, judge it by sales. Ogilvy: research before writing; the big idea; the headline carries most of the value; long copy works when it is interesting; never write an ad you would not want your family to read. Caples: headlines with self-interest, news, curiosity, in that order of reliability; "they laughed when I sat down at the piano" as the identification headline.

### 3.3 Gary Halbert, Joe Sugarman, Gary Bencivenga, Robert Collier

Halbert: the starving crowd (the market matters more than the copy); A-pile mail versus B-pile mail (the personal-looking envelope gets opened; today, the native-looking ad gets watched). Sugarman: the slippery slide; the only job of the first sentence is to get the second read; seeds of curiosity ("but there's more"). Bencivenga's persuasion equation: urgent problem plus unique promise plus unquestionable proof plus user-friendly proposition. Collier: enter the conversation already going on in the prospect's mind.

### 3.4 Copy formulas (for the copywriter agent)

AIDA; PAS (problem, agitate, solve); BAB (before, after, bridge); the 4 Ps (picture, promise, prove, push); Star-Story-Solution; the "open loop" lead; the "you've probably tried" lead (an accusation audit, see section 5); the "mechanism reveal" lead; the "confession" lead (pratfall); the "specific number" lead; the "identification" lead ("if you run a two-person shop…").

### 3.5 Harry Dry's three tests (Marketing Examples)

For every line: can you visualize it? Can you falsify it? Could nobody else say it? A line that fails all three is deleted. The critic agent runs this on every hook and headline.

### 3.6 Alex Hormozi (*$100M Offers*, 2021; *$100M Leads*, 2023)

The value equation: dream outcome times perceived likelihood of achievement, divided by time delay times effort and sacrifice. Ads raise the numerator with specificity and proof and lower the denominator by showing the first step is small. The Grand Slam Offer stack: the core, bonuses, scarcity, urgency, guarantee, naming. His working ad structure: a callout (who this is for, said so the right person stops), value (hook them, keep them, reward them), a call to action. His scaling heuristic in his content: more (more ads, more placements), better (improve what works), new (new platforms, new formats). His own first winning ad was ugly; the offer and the hook did the work. Keep his frameworks; do not import his promises or delivery model; members do not sell guaranteed outcomes.

---

## 4. 2026 paid-social craft

### 4.1 Sarah Levinger (consumer psychology for creative strategy; Motion bootcamp June 2026)

Three realities to research: customer reality (what they actually feel and say), brand reality (what the brand can truthfully claim), presentation reality (what the ad shows). Ads as mirrors: the viewer must see themselves, so emotional identity beats demographics. T-E-E-P: trigger, exploration, evaluation, purchase; each stage prefers different formats (trigger wants pattern interrupts and identity; exploration wants education and mechanism; evaluation wants proof and comparison; purchase wants offer and friction removal). Her method mines review text for emotional language; Ad Lab's `/adlab:personas` does the same on reviews, comments and community threads.

### 4.2 Dara Denney (Motion) and Barry Hott

Denney: concept variation (a different idea) is not creative iteration (a different hook on the same idea); the hook is a science with named categories; the creative strategist's job is to build the concept library and read the data. Hott: ugly ads and native-looking ads often beat polished ones because they do not look like ads; authenticity is a signal the platform's ranking also rewards. Ad Lab's format taxonomy keeps "ugly" as a first-class format, and the bank must include at least two.

### 4.3 Meta's 2026 ranking shift ("Andromeda") and what it means for the bank

Every agency source in October 2026 agrees on the direction even where their numbers disagree: creative diversity does the targeting work audiences used to do; detailed targeting is treated as a suggestion; consolidated structures (fewer ad sets, more distinct concepts) outperform fragmented ones; fatigue arrives faster (refresh in weeks, not months); distinct concepts beat twenty variants of one. Treat the specific percentages in those blogs as vendor claims. Design consequence: the bank ships eight to twelve genuinely different concepts per round, each with three to six hooks, and the test plan uses one broad ad set.

### 4.4 Format taxonomy (every bank must cover at least six)

Statics: text-only "ugly" ad; us-versus-them table; three-reasons list; review or press card; founder note (typed letter); meme or tweet screenshot; "what's inside" flat lay; FAQ card; comparison chart; "I was skeptical" quote; DM or email screenshot (real only); before-and-after (policy caution); offer card; problem-named card.

Video: founder-to-camera; product demo; screen recording with picture-in-picture; podcast clip; street interview; day-in-the-life; mini-documentary; whiteboard explainer; listicle; skit or humour; POV; reaction or duet; real testimonial; "how it's made"; mistakes and lessons; objection handling; myth correction; comparison with doing it alone.

Carousel: tutorial steps; persona cards; timeline; "swipe to see" reveal; before-during-after process (with fair context).

### 4.5 Hook taxonomy (the ad-analyst tags one of these per ad; the copywriter uses them as a menu)

Callout ("if you run a…"); question; bold claim; specific number; curiosity gap; pattern interrupt; contrarian or myth ("stop doing X"); negative or warning; confession or pratfall; story opener; POV; "three reasons"; "I was today years old"; "nobody talks about"; comparison ("X vs Y"); news or "new"; social proof ("why 1,214 people…"); authority ("as a…"); demonstration ("watch this"); problem-naming ("the 11pm invoice pile"); identification ("for the two-person shop"); offer-led ("free until Friday"); "what I wish I knew"; "the real reason"; "unpopular opinion"; "day 1 vs day 30".

Angle families (the strategic unit): problem-led; desire-led; mechanism-led; identity-led; proof-led; offer-led; contrarian; news or trend; comparison; story or origin; education or insight (Challenger); cost-of-inaction (policy caution).

### 4.6 UGC and creator brief structure

Persona and situation; the single angle; three hook options; the body beats (problem, mechanism, proof, first step); the on-screen text plan; the CTA; what not to say (policy, claims without proof); the "ugly is fine" note; shot list; deliverables and aspect ratios.

---

## 5. Sales psychology translated into ads, pages and DMs

Ad Lab is not a sales trainer; it borrows the mechanisms because an ad is a sales conversation compressed into seconds.

- **SPIN (Neil Rackham).** Situation, problem, implication, need-payoff. In an ad: name the situation in the callout, the problem in the hook, the implication in one line (what it costs), and the need-payoff as the promise.
- **The Challenger Sale (Dixon and Adamson).** Teach, tailor, take control; the commercial insight reframes how the buyer sees their own problem. The "insight ad" format: "the reason your X isn't working isn't Y, it's Z."
- **Gap Selling (Keenan).** Current state versus future state; the gap is the value. Ads that make the current state vivid and the future state concrete, without fabricated results.
- **Sandler pain funnel.** Questions that go from surface to cost to feeling. Use as a hook-writing exercise per persona: "tell me more… how long… what have you tried… what did that cost… how do you feel about that."
- **Chris Voss (*Never Split the Difference*).** Tactical empathy; labeling ("it seems like you've been burned by this before"); the accusation audit (name the objections before they do: "you're thinking this is another course"); mirroring; calibrated "how" questions; no-oriented questions ("would it be ridiculous to…"); the "that's right" moment (the viewer feels understood). Labels and accusation audits are the best objection-handling hooks in the library.
- **Oren Klaff (*Pitch Anything*).** Frame control; status; prizing (the seller as the prize: selective offers, "not for everyone"); intrigue; time constraint. Use carefully; false exclusivity is a trust killer.
- **Objection taxonomy and the copy move for each.** Price (reframe the unit: per day, versus the cost of the workaround); trust (proof, pratfall, guarantee, show the work); time (the first step is small; what the first week looks like); fit ("this is for… this is not for…"); priority (cost of inaction, stated fairly); "I can do it myself" (acknowledge, then show the hidden cost of doing it yourself); "tried before and it didn't work" (accusation audit plus mechanism difference); "not now" (a reason-why for now, never fake urgency).

---

## 6. Finance (the gate on the bank)

### 6.1 Inputs (`finance.md`)

Price; gross margin per sale (or per first period); refund or chargeback rate; average order value and units per order if relevant; for subscriptions or memberships: trial-to-paid rate, expected months retained (or monthly churn), price per period; the member's payback window (how many months they are willing to wait to recover acquisition cost); the monthly test budget.

### 6.2 Formulas

- Contribution per customer over the payback window = sum over the window of (price x gross margin x survival rate) minus refunds.
- Breakeven CPA = contribution over the payback window.
- Target CPA = breakeven CPA x (1 minus the profit fraction the member wants to keep).
- Subscription LTV (simple) = price x gross margin x (1 / monthly churn); treat this as a ceiling, not a target.
- For a trial-based membership: breakeven cost per trial start = breakeven CPA x trial-to-paid rate.
- MER (marketing efficiency ratio) = total revenue / total ad spend; nCAC = ad spend / new customers; payback months = CPA / monthly contribution.
- Test budget per concept = target CPA x the number of conversions needed to judge (a practical floor is in the tens of conversions, not single digits; below that, judge on upstream signals only).

### 6.3 Worked example (memberships, illustrative numbers only)

A $97 per month community with a seven-day trial, 60% trial-to-paid (hypothesis), 4 months average retention (hypothesis), 95% margin after processing: contribution per paid member over 4 months is about $369; breakeven CPA per paid member about $369; breakeven cost per trial start about $221; a target leaving 40% margin is about $133 per trial start. Every number here is a placeholder to be replaced by the member's real inputs; the tool must print the formula with the result.

### 6.4 Signals glossary and decision rules

CPM; hook rate (3-second plays / impressions); hold rate (ThruPlays or 15-second plays / 3-second plays); CTR (link); CPC; landing conversion rate; CPA; ROAS; MER; nCAC; frequency. Reading order for a new concept: hook rate first (did the angle select anyone), hold rate second (did the body keep them), CTR third (did the offer pull), CPA last and only at sufficient volume. Decision rules: kill a concept that fails hook rate after a fair impression floor; iterate hooks on a concept with good hold and poor hook; iterate offer or landing on good CTR and poor CPA; scale a concept only on CPA inside target with stable frequency. The readout skill applies these to an Ads Manager export and says which rule fired.

---

## 7. Pricing psychology and offer construction

Anchoring (show the reference price first); the decoy; Goldilocks tiers (three, the middle is the target); charm versus round pricing (charm for value positioning, round for premium); price as a signal of efficacy (Sutherland); the per-day or per-use reframe; "free" as its own category; pain-of-paying smoothing (annual, bundles); guarantees (unconditional, conditional, performance-based, "keep the bonuses"); bonuses that remove an objection each; scarcity and urgency only when true; offer naming (Hormozi's elements: the magnet reason, the avatar, the goal, the time interval, the container); the value equation as the editing tool for the offer line.

---

## 8. Platform and policy rules the critic enforces

- Meta: no implied personal attributes in the second person ("are you depressed," "struggling with your weight"); no before-and-after in health and body categories; no misleading income or results claims; no sensational imagery; AI-generated content disclosure where required; branded content rules if creators post it.
- FTC and equivalents: endorsements must be real, typical or disclaimed, and material connections disclosed; "results not typical" is not a shield for a fabricated result.
- Creator and community categories: no earnings guarantees; a scripted founder is not a customer testimonial; a demonstration is not a deployed system; deposits are not profit; business spend is not ad spend. (These are the Operators Workshop house rules and they generalize.)
- Specs: 1:1, 4:5 and 9:16; safe zones for 9:16 UI overlays; the first three seconds carry the hook; captions on by default; text legibility at phone size.

---

## 9. Rubrics and schemas (verbatim field lists for the agents)

### 9.1 Per-ad rubric (`analysis/ads.csv` columns)

`ad_id, advertiser, page_or_account, platforms, first_seen, days_active_at_capture, status, variant_count, variant_type (copy-test|creative-test|placement|none), format, duration_s, hook_text, hook_type, angle_family, awareness_stage (unaware|problem|solution|product|most), sophistication_move (claim|bigger-claim|mechanism|better-mechanism|identification), persona_inferred, persona_evidence, emotional_lever, biases_used, proof_type (demo|testimonial|data|authority|social-proof|press|ugc|none), offer_elements, price_framing, cta, landing_type, landing_continuity (strong|weak|broken|unknown), production_style (polished|native|ugly|ugc|founder|screen-rec), visual_hook, on_screen_text_density (none|low|medium|high), distinctive_assets, sutherland_lens, works, weak, verdict (adapt|avoid|monitor), adaptation_idea, inspection_coverage (copy-only|still-reviewed|video-watched)`

### 9.2 Market map (`analysis/market-map.md` sections)

Roster and sample sizes with capture dates; sophistication stage and required move; table-stakes claims (with counts and IDs); uncontested claims about the member's offer; persona coverage heatmap; proof arms race; price and positioning map; format mix and gaps; longevity leaderboard with caveats printed; conventions worth inverting (the opposite pass); ten testable hypotheses; evidence limits (what was not inspected, which videos were not watched, which counts are samples).

### 9.3 Persona (`personas/pN-<slug>.md`)

Name as a situation, not a demographic; job to be done; trigger moment; four forces (push, pull, anxiety, habit); current workaround including nothing; awareness distribution; sophistication; objections in their words; emotional identity; implicit goal (Barden); status game (who they want to look like, to whom); language bank (verbatim phrases with sources and dates); proof required; preferred formats by T-E-E-P stage; poor-fit signals; which competitor ads already talk to them (IDs); what nobody says to them yet.

### 9.4 Concept brief (`concepts/cNN-<slug>.md`)

Persona; awareness stage; angle family; the one idea; the mechanism (framework citations); competitor evidence (IDs) and the difference; proof available (from the asset catalog, with the claim-to-evidence ledger); formats planned; six hooks; the CTA; landing continuation; policy and truth risk flags; the critic's note; the CPA it must beat; status (draft, ready, testing, retired).

### 9.5 Bank entry (`bank/ad-bank.csv`)

`entry_id, concept_id, persona, format, aspect_ratio, hook, primary_text_short, primary_text_long, headline, description, cta, script_or_layout_ref, asset_refs, why_it_should_work, competitor_refs, risk_flags, critic_note, editorial_score, status, version, changelog`

### 9.6 Asset catalog (`assets/catalog.md` row)

File; type; what it shows (observed); what it can prove and what it cannot; quality at phone size; persona and angle fit; needed edit; the member's note; Claude's read; the revised read; permissions (who is in it, consent status); status.

### 9.7 Editorial score (adapted from the Operators Workshop improvement system)

Six dimensions, zero to two each: recognizable situation; specificity; curiosity with a payoff; visual fit; credibility; fit with the offer. Ten to twelve shortlist; seven to nine revise; six or under rebuild. Plus the two-second stranger test (would a stranger know who it is for and what it is about in two seconds) and Harry Dry's three tests. An editorial score is a recording priority, never a performance claim.

### 9.8 Evidence integrity rules (the critic's checklist)

Observed, owner-provided, inferred and hypothetical are labeled separately; no invented results, testimonials, member counts, scarcity or urgency; longevity is not profitability; active-only samples cannot estimate survival; variants from one advertiser are not independent evidence; never say a video was watched if only the poster or transcript was read; a demonstration is not a deployment; correlation is not causation; every borrowed pattern has a source and an observation distinct from the interpretation.

---

## 10. The two core prompts (seed text for `library/prompts/`)

### 10.1 `interrogation.md`

Role: a ruthless, deeply creative marketing strategist working in the register of Rory Sutherland and Ogilvy-style behavioural science, with behavioural economics, consumer psychology, positioning, brand strategy and startup growth as the toolkit. Job: not generic advice; grill, interrogate, rip apart, reframe and psychologically decode the business, then produce the seven highest-leverage recommendations. Stance: most businesses do not have a marketing problem; they have a perception, trust, category, status, context, pricing-signal, social-proof, ritual or legibility problem. Treat the customer as status-aware, story-driven, ambiguity-averse and emotionally interpretive, deciding through cues, habits, shortcuts, social meaning, fear, aspiration, trust, identity and post-rationalization, never as a rational calculator.

Inputs: `business/brief.md`, `business/offer.md`, `business/finance.md`, the interrogation answers, `analysis/market-map.md`, the persona files. Rules: cite ad IDs and persona files for every challenge; label hypotheses; every recommendation has a mechanism, evidence, cheapest test and falsifier; no invented facts; no guaranteed outcomes. Output: the fixed schema in section 1.3.

### 10.2 `opposite-pass.md`

For each of the category's top five conventions found in the market map (claims, formats, proof types, price signals, tones), write the inverse, then answer: is the inverse also a good idea, for which persona, under what mechanism, and what is the cheapest test. Reject inversions that are merely contrarian with no mechanism.

---

## 11. Sources to cite in the library (public)

Sutherland: *Alchemy* (2019); Ogilvy; 2025 and 2026 podcast appearances. Shotton: *The Choice Factory* (2018), *The Illusion of Choice* (2023). Cialdini: *Influence* (new and expanded 2021), *Pre-Suasion* (2016). Kahneman: *Thinking, Fast and Slow* (2011). Thaler and Sunstein: *Nudge* (2008). Ariely: *Predictably Irrational* (2008). Barden: *Decoded* (2013). Berger: *Contagious* (2013). Heath: *Made to Stick* (2007). Christensen, Moesta: *Competing Against Luck* (2016). Godin: *This Is Marketing* (2018). Sharp: *How Brands Grow* (2010). Binet and Field: *The Long and the Short of It* (2013). Ritson: Marketing Week columns and the Mini MBA. Dunford: *Obviously Awesome* (2019). Schwartz: *Breakthrough Advertising* (1966). Hopkins: *Scientific Advertising* (1923). Ogilvy: *Ogilvy on Advertising* (1983). Caples: *Tested Advertising Methods*. Halbert: the Boron Letters. Sugarman: *The Adweek Copywriting Handbook*. Bencivenga: the Bencivenga Bullets. Collier: *The Robert Collier Letter Book*. Hormozi: *$100M Offers* (2021), *$100M Leads* (2023). Rackham: *SPIN Selling*. Dixon and Adamson: *The Challenger Sale*. Keenan: *Gap Selling*. Voss: *Never Split the Difference* (2016). Klaff: *Pitch Anything* (2011). Levinger: Motion Creative Strategy Bootcamp talk (June 2026) and her articles. Denney: Motion library and bootcamp. Hott: public talks and posts. Harry Dry: Marketing Examples copywriting guide. Meta, TikTok, Google and LinkedIn: current ad policy and transparency pages (link the live pages; they change).
