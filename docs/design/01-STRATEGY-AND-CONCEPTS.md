# Ad Lab: strategy and concepts for the Scaling Skool hand-off artifact

Prepared October 22, 2026 for the Scaling Skool team. Working name **Ad Lab** (plugin slug `adlab`). Everything here is a design proposal for the thing Opus 5.5 will build; nothing has been built or tested yet. Where a claim rests on a vendor blog rather than a primary source, the research notes say so.

Companion files: [02-OPUS-5.5-BUILD-PROMPT.md](02-OPUS-5.5-BUILD-PROMPT.md) (paste into Opus), [03-FRAMEWORK-LIBRARY.md](03-FRAMEWORK-LIBRARY.md) (the knowledge seed), [04-RESEARCH-NOTES.md](04-RESEARCH-NOTES.md) (what is true about data access, packaging and models right now).

---

## 1. The one-sentence version

A member installs one Claude Code plugin, pastes their website, answers a short interrogation, and gets back a decoded market: who their competitors are, what every competitor ad is actually doing psychologically, which personas are being fought over and which are ignored, where the white space is, and a bank of their own ads built from that evidence, with the reasoning shown for every line, plus a finance-grounded test plan to find out whether any of it is true.

The product is not "a scraper" and not "an AI copywriter." It is a **research-to-production system with a visible chain of reasoning**. The reasoning chain is the moat: every output cites the competitor ad IDs, the persona, the awareness stage and the psychological lever it rests on, and labels what is observed versus inferred versus invented-as-hypothesis. That is the Operators Workshop house style already (the community's evidence-integrity rules and its ad-audit discipline), and it is what separates this from the fifty "AI ad generator" tools.

---

## 2. Why this is the right first artifact for the community

- **It is the foundation task.** Before a member builds anything (a landing page, a funnel, an offer, a content plan), they need to know who they are selling to, what the market already believes, and what the market is already being told. Every later artifact (offer builder, landing page builder, content engine) can read from the same `workspace/` this one creates. Position it as "Module 0: know your market before you build."
- **It fits the brief.** The standing brief says members do their own work and decide what to apply. This tool produces labeled hypotheses and a test plan. It does not launch ads, it does not touch Ads Manager, and it never invents proof. That is consistent with "Meta: never launch or edit" and with the no-guarantees rule.
- **It produces shareable community content.** Each member's market map and ad bank board are things they will want to post ("here is what my market looks like"). That feeds the discussion flywheel without founders doing work for members.
- **The hardest part already exists.** An earlier read-only scraper pulled 1,927 ads without login, captcha or block, by reading the JSON embedded in the Ad Library HTML plus intercepted GraphQL responses, and an earlier renderer turns HTML into PNG and MP4 without node. Those two scripts are the data and production layers of Ad Lab, generalized.

---

## 3. Who uses it (three member situations the tool must handle)

| Situation | Intake path | What changes |
|---|---|---|
| Existing business with a website | Paste URL; tool reads site, pricing, about, reviews | Full flow |
| Idea stage, no site | Describe the offer in the interrogation; tool builds the brief from answers | Competitor discovery leans on category search, not on the member's site |
| Service provider / agency member | `--client <name>` creates a separate workspace per client | Multi-workspace; the library is shared, the workspaces are not |

The audience in the brief includes beginners. So the install must be one command, the first run must produce something useful inside 20 minutes, and there must be a **Lite mode** that needs no Python: the member pastes 10 to 20 Ad Library links or screenshots and the analysis still runs.

---

## 4. The member journey (what it feels like)

1. **Install** (2 minutes): two slash commands, or "Add plugins" in the desktop app. Then `/adlab:setup` installs the Python tooling itself, checks it, and asks for optional keys (Higgsfield, Apify) only if the member wants them.
2. **Intake** (10 minutes): `/adlab:intake https://theirsite.com`. The tool reads the site and comes back not with a summary but with a Sutherland-style interrogation: eight to twelve pointed questions in two batches, each with a default so the member can skip. "Who is the customer trying to look like after buying this?" "What does the customer currently do instead, including nothing?" "Which claim on your site could a competitor also make word for word?" Output: `workspace/business/brief.md`, `offer.md`, `finance.md`.
3. **Competitors** (5 minutes plus confirmation): three rings of competitors with confidence and reason. The member crosses out and adds. Direct (same product), indirect (same job, different solution), and attention competitors (same persona, different category: the people buying this customer's attention).
4. **Pull** (20 to 60 minutes, unattended): ads from Meta, Google Transparency Center (which covers YouTube video ads), LinkedIn if B2B, TikTok where visible. Images, videos, card screenshots, start dates, variant counts, landing pages. Fast, because CDN URLs expire.
5. **Decode** (unattended, parallel subagents): every ad gets a rubric row (section 6). Then the market map: sophistication stage, table-stakes claims, uncontested claims, persona coverage heatmap, proof types in use, format mix, pricing signals, the longevity leaderboard with its caveats stated, and the list of category conventions worth inverting.
6. **Personas** (member reviews): three to seven, built from the brief, the competitor targeting evidence, mined customer language and the member's own customers. Member edits; Claude revises.
7. **Interrogation report**: the seven highest-leverage recommendations in the Sutherland register, each with mechanism, supporting evidence from the pull, the cheapest test, and what would prove it wrong.
8. **Angles and concepts**: a coverage matrix (persona x awareness x angle family x proof x format) with rejected cells explained, then eight to twelve genuinely distinct concepts.
9. **Ad bank**: copy, hooks, scripts, static layouts, carousel cards, UGC briefs, landing continuation notes. Each entry: stable ID, why it should work (framework citations), competitor reference IDs, the difference from the competitor, risk flags, and a critic's note.
10. **Assets**: member drops their photos, videos, screenshots, testimonials into `workspace/assets/`. The tool catalogs each item (what it shows, what it can prove, which persona and angle it fits, what edit it needs) in a three-column table: the member's note, Claude's read, the revised read. Per item, the member can go as deep as they like.
11. **Render**: statics from HTML templates to PNG in 1:1, 4:5 and 9:16; video storyboards with shot lists; optional generated b-roll through the Higgsfield API with the price shown before every run and a credit floor the member sets. Generated imagery is for mood and b-roll only, never for fake screenshots, results or testimonials.
12. **Test plan and readout**: breakeven and target CPA from `finance.md`, test budget per concept, the campaign structure (one ad set, broad, six to twelve concepts), the refresh cadence, decision rules, and `/adlab:readout` which reads an Ads Manager CSV export and says what to do next.
13. **Refresh**: rerun the roster; diff new ads, dead ads, ads crossing 30, 60 and 90 days; new advertisers using the category's language.

---

## 5. Product architecture (what Opus builds)

```
adlab/                                   <- plugin root (also the marketplace repo)
  .claude-plugin/plugin.json             <- name "adlab", version, author
  .claude-plugin/marketplace.json        <- single-plugin marketplace, source "./"
  skills/
    setup/SKILL.md                       /adlab:setup      install + doctor
    start/SKILL.md                       /adlab:start      guided tour, decides Lite vs Full
    intake/SKILL.md                      /adlab:intake <url|"description">
    competitors/SKILL.md                 /adlab:competitors
    pull/SKILL.md                        /adlab:pull [--mode scrape|apify|manual] [--max N]
    process/SKILL.md                     /adlab:process    frames, transcripts, OCR, landing pages
    analyze/SKILL.md                     /adlab:analyze    per-ad rubric + market map
    personas/SKILL.md                    /adlab:personas
    interrogate/SKILL.md                 /adlab:interrogate
    angles/SKILL.md                      /adlab:angles
    bank/SKILL.md                        /adlab:bank
    assets/SKILL.md                      /adlab:assets
    render/SKILL.md                      /adlab:render [static|storyboard|higgsfield]
    plan/SKILL.md                        /adlab:plan       finance + test structure
    readout/SKILL.md                     /adlab:readout <ads-manager.csv>
    refresh/SKILL.md                     /adlab:refresh
    doctor/SKILL.md                      /adlab:doctor     diagnose a broken step
  agents/
    researcher.md  ad-analyst.md  psychologist.md  persona-builder.md
    copywriter.md  creative-director.md  finance-analyst.md  critic.md  librarian.md
  library/                               <- the brain (seeded from 03-FRAMEWORK-LIBRARY.md)
    psychology/  strategy/  copy/  sales/  finance/  platform/  rubrics/  prompts/
  tools/                                 <- Python, run through the skills
    setup.py  meta_pull.py  google_pull.py  linkedin_pull.py  tiktok_assist.md
    media.py  transcribe.py  render.py  higgsfield.py  finance.py  export.py  doctor.py
  templates/                             <- HTML ad templates (static, carousel card, storyboard)
  examples/                              <- two complete sample runs members can read first
  START-HERE.md  INSTALL.md  FAQ.md  LEGAL-AND-ETHICS.md  CHANGELOG.md
```

The member's own data lives outside the plugin in `./adlab-workspace/` (or `./adlab-workspace/clients/<name>/`), so plugin updates never touch their work:

```
adlab-workspace/
  business/   brief.md  offer.md  finance.md  interrogation.md
  competitors/ roster.md  roster.json
  ads/        <advertiser>/<ad_id>/  card.png  media/  transcript.md  frames/  ad.md
  analysis/   ads.csv  market-map.md  competitor-<x>.md  conventions.md
  personas/   p1-<slug>.md ...  coverage.md
  concepts/   matrix.md  c01-<slug>.md ...
  bank/       ad-bank.html  ad-bank.csv  briefs/  renders/
  assets/     (member drops files)  catalog.md
  plan/       test-plan.md  readouts/
  changelog.md  PROGRESS.md
```

`PROGRESS.md` is the resumable state table (stable IDs, which steps ran, when, with what counts) so a member can stop and resume across sessions, which matters because a full run is hours of unattended work.

---

## 6. The analytical core (what makes the decode "extremely in depth")

### 6.1 Per-ad rubric (every ad gets this row)

Identity: ad ID, advertiser, platforms, first seen, days active at capture, status, variant count and variant type (same copy with different media = creative test; same media with different copy = message test), format, duration.

Message: hook text (first line and first three seconds), hook type, **angle** (the interpretive frame the ad asks you to adopt), awareness stage (Schwartz), sophistication move (claim, bigger claim, mechanism, better mechanism, identification), inferred persona with the evidence for the inference, emotional lever, biases and principles in play (Shotton, Cialdini, Kahneman), proof type, offer and price framing, CTA, landing page type and whether the landing page continues the ad's promise.

Craft: production style (polished, native, ugly, UGC, founder, screen recording), visual hook (what is in frame first), on-screen text density, distinctive brand assets (face, colour, sound, mnemonic), pacing.

Judgment: the Sutherland question ("what perception problem is this ad solving, and is it the right one?"), what works, what is weak, verdict (adapt, avoid, monitor), adaptation idea with persona and angle.

### 6.2 Market synthesis

- **Sophistication stage of the category** and what move is now required (Schwartz).
- **Table stakes**: claims everyone makes (the member must make them too, but cannot win on them).
- **Uncontested claims**: true things about the member's offer nobody in the set is saying.
- **Persona coverage heatmap**: who the ads talk to, who is ignored, who is overserved.
- **Proof arms race**: which proof types dominate; where a different proof type would be distinctive.
- **Price and positioning map**: who signals premium, who signals cheap, who signals nothing.
- **Format mix** and the gap (for example, nobody in the set uses founder-to-camera or static text ads).
- **Longevity leaderboard**, published with the caveats your own audit established: longevity is not profitability, the sample is active-only, variants are not independent evidence, a big advertiser's scale is not a reason to copy.
- **Conventions worth inverting**: the explicit "opposite of a good idea" pass.
- **Skool-specific**: creators' ads often run under the Skool Page as "X with Skool" co-branded ads. The pull must search `"<name> with Skool"` and the Skool Page, or a competitor community will show zero ads. Your October 21 run found 328 of these.

### 6.3 Personas as buying situations, not demographics

Each persona file: job to be done, trigger moment, the four forces (push of the situation, pull of the new solution, anxiety of the new, habit of the present), current workaround including "nothing," awareness distribution across the five stages, sophistication, objections in their words, emotional identity, the status game being played (Sutherland: who are they trying to look like, and to whom), language bank of verbatim phrases with sources, proof required, poor-fit signals, and preferred formats by stage (Levinger's trigger, exploration, evaluation, purchase).

### 6.4 The interrogation (your pasted prompt, operationalized)

The pasted Sutherland prompt becomes `library/prompts/interrogation.md` and the `/adlab:interrogate` skill. It is run **after** the decode, so the grilling is grounded in evidence rather than vibes: "You say you compete on quality. Nine of the twelve competitors say the same thing in their first line; here are the IDs. What would you have to be true about you that none of them can say?" The output format is fixed: diagnosis of which problem it really is (perception, trust, category, status, context, pricing signal, social proof, ritual, legibility), then seven recommendations, each with mechanism, evidence, cheapest test, and falsifier.

### 6.5 Concept generation discipline

The strategic unit is the angle. One working angle yields many hooks and several formats; one hook yields one ad. The coverage matrix forces breadth; the critic agent forces honesty. Concept diversity is also what the platform now rewards (the 2026 "Andromeda" guidance across agency sources is consistent on this even where their numbers conflict): distinct concepts beat twenty variants of one idea.

### 6.6 Finance that gates the creative

`finance.md` holds price, gross margin, refund rate, and for memberships the trial-to-paid rate and monthly retention guess. From that: breakeven CPA, target CPA at the member's payback window, test budget per concept, the minimum events before judging, and the contribution-after-acquisition view. The bank is not "done" until each concept has a CPA it must beat. For a Skool community this is where "$97/month" meets "what can I afford to pay for a trial start."

---

## 7. Differentiation, stated plainly

| Typical tool | Ad Lab |
|---|---|
| Shows competitor ads | Decodes why each one exists and who it is for |
| Generates copy from a prompt | Generates copy from evidence, with the chain shown |
| Hooks as the unit | Angles as the unit; hooks derived |
| Demographic personas | Buying-situation personas with four forces and language banks |
| "Winning ads" by longevity | Longevity leaderboard with the sampling caveats printed on it |
| Ignores money | Breakeven CPA gates every concept |
| Black box | Member's note, Claude's read, revised read, on every asset |
| SaaS subscription | A folder the member owns, versioned, updatable, extensible |

---

## 8. Tiers (ship Tier 1; design for all three)

- **Lite** (no Python): paste links or screenshots; analysis, personas, interrogation, bank. For Windows strugglers and the idea-stage member.
- **Full** (default): automated pulls on the member's machine, media processing, renders.
- **Pro** (keys): Apify pulls for reliability at volume, Higgsfield renders, scheduled refresh, multi-client workspaces. Costs are the member's and are displayed before each spend.

---

## 9. Distribution through Scaling Skool

- **Repo**: a public GitHub repo (`jayrad1222/adlab`) that is itself a single-plugin marketplace. Members run `/plugin marketplace add jayrad1222/adlab` then `/plugin install adlab@adlab`, or use the desktop app's Add plugins button. Updates: `claude plugin update adlab@adlab`. Zip fallback for `claude --plugin-dir`.
- **Public versus private**: a private repo means every member needs GitHub access granted; that is friction and support load. Recommend public. The moat is the community, the updates, the example runs and the discussion, not the files.
- **Classroom module "Ad Lab" (six short lessons)**: install and first run; reading your market map; personas to angles; bank to render; test plan and readout; the refresh loop. Each lesson ends with "post your X in the thread."
- **Example runs ship inside the plugin** so a member can read a finished output before installing anything. Suggest two: a Skool community (Operators Workshop itself is the honest choice) and a physical product brand.
- **Versioning as content**: each release gets a changelog post. Library additions (new frameworks, new hook families, new platform rules) are visible community value.

---

## 10. Risks and how the design absorbs them

| Risk | Design response |
|---|---|
| Meta terms on automated access to the Ad Library UI | Read-only, no login, gentle pacing, member runs it on their own machine for their own research; Apify and manual modes offered; competitor creatives stay in the member's private workspace and are never republished. `LEGAL-AND-ETHICS.md` states this plainly. |
| Scraper breaks when Meta changes markup | Data comes from embedded JSON and GraphQL interception, not CSS selectors; fallback is card screenshots read by Claude vision; `/adlab:doctor` diagnoses and the plugin updates. |
| Windows install pain | `/adlab:setup` does the install; Lite mode needs nothing. |
| Token cost of decoding 200 ads | Per-ad rubric on a cheaper model via subagents; Opus-class model for synthesis only; default caps (40 ads per competitor, 8 competitors) the member can raise. |
| Generic output | Library specificity; mandatory citations to ad IDs; the critic agent; the "can you visualize it, falsify it, could nobody else say it" copy test on every line. |
| Policy and truth | Risk flags on personal-attribute hooks, before/after, income claims; AI-generated media labeled; never fabricated proof. |
| Members expecting results | Everything labeled hypothesis; the test plan is the product's last step, not a promise. |

---

## 11. Naming

`adlab` reads well as a command prefix (`/adlab:intake`, `/adlab:pull`, `/adlab:bank`). Alternatives if you want something less generic for the Skool listing: Market Decoder, Angle Lab, Competitor Ad Decoder. Avoid anything leaning on "Alchemy" (Sutherland's book title). Decide the display name; keep the slug short.

---

## 12. What success looks like for the first release

- A new member on a clean Mac goes from zero to a finished market map and a twelve-concept bank for their own business in one evening, with the only manual steps being the interrogation answers, the competitor confirmation and the persona review.
- Every line in that bank traces to an ad ID, a persona and a framework.
- The finance sheet names the CPA each concept has to beat.
- Nothing in the output is a fabricated result, testimonial or guarantee.
- Three members post their market maps in the community in the first two weeks.

The build prompt that gets Opus there is in the next file.
