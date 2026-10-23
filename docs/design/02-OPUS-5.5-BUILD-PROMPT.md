# Ad Lab: build prompt for Claude Opus 5.5

This is the build prompt that produced Ad Lab, kept for reference. The design packet it reads is the rest of this folder.

---

# Build Ad Lab: a Claude Code plugin that decodes a market and builds an evidence-backed ad bank

You are building a distributable Claude Code plugin called **Ad Lab** (plugin name `adlab`) for members of a Skool community called Scaling Skool / Operators Workshop. Members will install it with two commands, paste their business website, and get back a decoded market (competitors, every competitor ad analyzed, personas, white space), a Sutherland-style interrogation of their business, a bank of their own ads with the reasoning shown for every line, optional rendered creatives, and a finance-grounded test plan. This is Module 0 of their curriculum: know the market before you build anything.

You are the lead engineer, the creative strategist and the librarian on this build. Work autonomously. Use parallel subagents for independent work. Ask me only when something materially blocks a dependent step; otherwise decide, record the decision in `DECISIONS.md`, and continue.

## 0. Operating rules for this build

1. **Read the design packet first**, in this order, before writing any code:
   - `docs/design/01-STRATEGY-AND-CONCEPTS.md` (what the product is and why)
   - `docs/design/03-FRAMEWORK-LIBRARY.md` (the knowledge seed you will expand into `library/`)
   - `docs/design/04-RESEARCH-NOTES.md` (what is true about data access, packaging and model settings in October 2026)
   - Then read the existing working code you will port: an earlier read-only Meta Ad Library scraper, `scrape.py`, that pulled 1,927 ads without login, captcha or block by reading the JSON embedded in the page plus intercepted `/api/graphql/` responses, with its plan file, summarizer, TikTok probes and the notes from its run (including the "with Skool" co-branded ad finding); then an HTML-to-PNG and MP4 renderer, `pw.py` (Python Playwright and imageio-ffmpeg, no node), and a board builder, `build_page.py`. These are proven on the build machine; generalize them, do not rewrite them from scratch.
   - Also read the community's evidence-integrity and house-style notes for the style you must preserve.
2. **Keep `BUILD-CHECKLIST.md` at the repo root** with every phase and acceptance criterion below as a checkbox. Update it as you go. A text summary at the end of a turn is a report, not proof; the checklist plus the files are the proof.
3. **Completion condition (the build is done when all of these are true):** `claude plugin validate --strict ./` passes; a clean user profile can install the plugin from the repo with the two documented commands and run `/adlab:start`; `/adlab:setup` installs the Python tooling on macOS and Windows without manual steps; two complete example runs exist under `examples/` with every artifact listed in section 5; every example artifact is free of fabricated results, testimonials or counts; `START-HERE.md`, `INSTALL.md`, `FAQ.md`, `LEGAL-AND-ETHICS.md`, `CHANGELOG.md` exist; the critic pass has run on both example banks and its notes are in the files; version `0.1.0` is tagged.
4. **Status lines go in the same message as your next tool call.** Do not end a turn with a summary that announces the next step; take the step. Do not write your reasoning into replies. Do not stop at a milestone because the session is long.
5. **Time matters.** Do not spend time that can be avoided; the earlier a correct result exists, the better. Pulls and renders run in the background while you keep building.
6. **Commit at the end of each phase** with a message that names the phase. Create the repo as a git repository at the start. Do not push until I say so.
7. **Subagent effort:** run library-writing subagents at `medium`, per-ad analysis subagents at `low`, and keep `xhigh` for your own synthesis and integration work.
8. **Truth rules are non-negotiable** in everything the plugin produces: observed, owner-provided, inferred and hypothetical are labeled separately; no invented results, testimonials, member counts, scarcity or urgency; longevity is not profitability; active-only samples cannot estimate survival; variants from one advertiser are not independent evidence; never claim a video was watched when only its poster or transcript was read; an editorial score is a priority, never a performance claim. These rules live in `library/rubrics/evidence-integrity.md` and the `critic` agent enforces them.
9. **The plugin never launches, edits or touches ad accounts.** It reads exports. It never republishes competitor creatives; they stay in the member's private workspace as research references.
10. **Every spend shows its price first.** Apify and Higgsfield calls print the estimated cost and respect a floor the member sets in `adlab-workspace/business/finance.md`. No key, no call; the skill falls back to the free path.

## 1. What the member experiences (build to this)

```
/adlab:setup                      installs tooling into ${CLAUDE_PLUGIN_DATA}, runs doctor, asks for optional keys
/adlab:start                      explains the flow, detects Lite vs Full, creates ./adlab-workspace/
/adlab:intake <url | "text">      reads the site, runs the interrogation in two batches, writes business/*
/adlab:competitors                three rings, confidence, reasons; member confirms
/adlab:pull [--mode scrape|apify|manual] [--max 40] [--inactive]
/adlab:process                    frames, transcripts, on-screen text, landing pages
/adlab:analyze                    per-ad rubric via subagents, then the market map
/adlab:personas                   3 to 7 buying-situation personas; member reviews
/adlab:interrogate                the Sutherland report, grounded in the decode
/adlab:angles                     coverage matrix, opposite pass, 8 to 12 concepts
/adlab:bank                       copy, hooks, scripts, layouts, briefs; the board and the CSV
/adlab:assets                     catalogs member files; three-column notes; per-item depth
/adlab:render [static|storyboard|higgsfield]
/adlab:plan                       breakeven and target CPA, test structure, decision rules
/adlab:readout <export.csv>       reads an Ads Manager export and applies the rules
/adlab:refresh                    re-pull, diff, changelog
/adlab:doctor                     diagnoses a broken step and prints the fix
```

Three member situations must work: an existing business with a site; an idea with no site (intake from text); a service provider with several clients (`--client <name>` gives `adlab-workspace/clients/<name>/`). A **Lite mode** must work with no Python at all: the member pastes Ad Library links or screenshots and everything from analyze onward still runs.

## 2. Repository and plugin layout (exact)

```
adlab/
  .claude-plugin/plugin.json        name "adlab", version "0.1.0", description, author, homepage, repository, license, keywords
  .claude-plugin/marketplace.json   single-plugin marketplace: { "name": "adlab", "owner": {...}, "plugins": [{ "name": "adlab", "source": "./", ... }] }
  skills/<skill>/SKILL.md           one folder per command above; supporting files beside it
  agents/*.md                       researcher, ad-analyst, psychologist, persona-builder, copywriter, creative-director, finance-analyst, critic, librarian
  library/                          psychology/ strategy/ copy/ sales/ finance/ platform/ rubrics/ prompts/ observed/
  tools/                            Python 3.9+; see section 4
  templates/                        HTML ad templates and the board template
  examples/<run-name>/              two complete runs
  docs/design/                      a copy of the three design-packet files
  START-HERE.md INSTALL.md FAQ.md LEGAL-AND-ETHICS.md CHANGELOG.md DECISIONS.md BUILD-CHECKLIST.md README.md
```

Conventions you must follow (they are from the current Claude Code docs; the research notes list the sources):

- A skill is `skills/<name>/SKILL.md` with YAML frontmatter starting on line 1. Useful fields: `name`, `description` (when Claude should use it; keep it specific), `argument-hint`, `allowed-tools` (pre-approve the plugin's own scripts: `Bash(${CLAUDE_PLUGIN_ROOT}/tools/*)`), `disable-model-invocation: true` for commands only the member should trigger (setup, pull, render, refresh), `user-invocable: false` for internal skills that only agents preload (the rubric, the evidence rules), `context: fork` with `agent:` for long isolated steps where that is cleaner, `effort`. Keep each `SKILL.md` under 500 lines; put long reference text in sibling files and link to them. Use `$ARGUMENTS` and named `arguments:` for inputs. Use `${CLAUDE_PLUGIN_ROOT}` for plugin files, `${CLAUDE_PLUGIN_DATA}` for the venv and browser binaries (so plugin updates do not wipe them), and `${CLAUDE_PROJECT_DIR}/adlab-workspace` for member data. Plugin skills are invoked as `/adlab:<name>`.
- A subagent is `agents/<name>.md` with required `name` and `description`, optional `tools`, `model`, `skills` (preloaded skills: this is how the ad-analyst gets the rubric), `effort`, `maxTurns`. Plugin subagents cannot carry `hooks`, `mcpServers` or `permissionMode`.
- `plugin.json` needs only `name`; set `version` and bump it on every release because hosted users get a cached copy until the version changes. Components are namespaced under the plugin name.
- Validate with `claude plugin validate --strict ./` and test with `claude --plugin-dir ./`. The install commands members use are `/plugin marketplace add jayrad1222/adlab` then `/plugin install adlab@adlab`, and the desktop app's Add plugins button. Put both in `INSTALL.md` with a zip fallback (`claude --plugin-dir`).
- A root `CLAUDE.md` is not loaded by plugins; do not rely on one.

## 3. The library (Phase 2): expand the seed into sixty-plus files

Expand `03-FRAMEWORK-LIBRARY.md` into `library/` using the file skeleton in its section 0 (idea; spot it in a competitor ad; use it in ours; how it backfires; questions it adds; related; sources). One file per framework or concept. Use parallel subagents at `medium`, one per library folder, each given the seed section and the skeleton; then you integrate, deduplicate, cross-link and run a consistency pass. Required folders and minimum contents:

- `psychology/`: every Sutherland concept in seed section 1.2 as its own file; Shotton (two files, with the "verify against the table of contents" note kept until verified); Cialdini; Kahneman-Tversky-Thaler-Ariely (one file per bias that has a distinct detection cue); Barden; Berger; Heath; Moesta JTBD forces; Godin.
- `strategy/`: Schwartz awareness; Schwartz sophistication; Sharp; Binet and Field; Ritson's order; Dunford positioning; Hormozi value equation; Hormozi offer stack; Levinger three realities and T-E-E-P; Denney concept versus iteration; Hott ugly ads; Andromeda implications (marked as agency consensus, not Meta documentation).
- `copy/`: the canon (Hopkins, Ogilvy, Caples, Halbert, Sugarman, Bencivenga, Collier); formulas; hook taxonomy; angle families; format taxonomy (statics, video, carousel); CTA patterns; UGC brief structure; Harry Dry's three tests; Hormozi callout-value-CTA.
- `sales/`: SPIN; Challenger; Gap; Sandler; Voss toolkit mapped to copy; Klaff frames; the objection taxonomy with the copy move per objection.
- `finance/`: inputs; formulas; the two worked examples with every number labeled placeholder; the signals glossary; decision rules.
- `platform/`: Meta policy pitfalls; FTC endorsement rules; creator-category truth rules; specs and safe zones; TikTok and YouTube creative differences; the Skool co-branded ad finding.
- `rubrics/`: per-ad rubric (field list verbatim from seed 9.1); market map template; persona schema; concept brief schema; bank entry schema; asset catalog schema; editorial score; evidence integrity; the critic checklist; the two-second stranger test.
- `prompts/`: `interrogation.md` (the member's original prompt text is in Appendix A of this document; keep its stance and wording, add the grounding and schema from seed 1.3 and 10.1); `opposite-pass.md`; `intake-questions.md`.
- `observed/`: empty with a README explaining that the librarian agent appends patterns here with ad IDs and never edits canonical files.

Library quality bar: no invented statistics; "studies show" only with a named study; contested claims marked contested; every detection cue is something the ad-analyst can look for in copy, transcript or frames.

## 4. Tools (Phase 3): port, generalize, contract

All tools are Python 3.9+ (the reference Mac runs 3.9.6), live in `tools/`, are run by skills through `Bash(${CLAUDE_PLUGIN_ROOT}/tools/...)`, take explicit paths as arguments, write JSONL or CSV plus a short Markdown summary, and print one line of progress per unit of work. Each tool has a `--help`, a `--dry-run` where it spends anything, and a fixture-based test under `tools/tests/`. Run all Python with `-I`.

- `setup.py`: creates a venv in `${CLAUDE_PLUGIN_DATA}/venv`; installs `playwright`, `imageio-ffmpeg`, `pillow`, `pyyaml`, `requests`; runs `playwright install chromium`; installs `mlx-whisper` on Apple Silicon and `faster-whisper` elsewhere, with a flag to skip transcription; handles macOS and Windows (PowerShell paths, no symlinks); writes `${CLAUDE_PLUGIN_DATA}/config.json` with optional keys the member pastes (Higgsfield key id and secret, Apify token, SerpApi key); never prints a key back. Ends by running `doctor.py`.
- `doctor.py`: checks Python, venv, Playwright, Chromium, network, that a Meta Ad Library keyword search page loads and yields at least one ad, that Google Transparency Center loads, disk space, and the workspace structure; prints the fix for each failure in plain words.
- `meta_pull.py`: the port of `scrape.py`. Inputs: a plan JSON (keyword searches, exact-phrase searches, page searches via typeahead and `view_all_page_id`, country, active or all, media type), caps per advertiser and total, output dir. Behaviour: headless Chromium, desktop UA, one search at a time with 2 to 4 second pauses, no login, no likes or follows, data from embedded JSON plus intercepted GraphQL, scroll until the cap or until two scrolls add nothing, dedupe on `ad_archive_id`. Captures per ad: ids, page name and id, start date, status, platforms, body text, title, caption, CTA, link url and domain, media urls, card element screenshot, poster frame. **Downloads media immediately** because the CDN URLs expire. Captures the EU transparency block (reach, age and gender and location breakdown) when the detail page shows one. Adds the "co-branded" search: for a competitor name N, also search `"N with Skool"` and open the Skool Page's ads filtered by N, and generalize this as a configurable list of known "platform pages that run ads for creators". Writes `ads.jsonl`, `ads_flat.csv`, `searches.csv`, `run.log`. Keep the fallback: if the embedded JSON is absent, take card screenshots and let Claude read them.
- `google_pull.py`: Google Ads Transparency Center by advertiser name and domain; formats (text, image, video), regions, date ranges; YouTube links for video ads; Playwright with the same manners; optional SerpApi path if a key exists (print the price first).
- `linkedin_pull.py`: LinkedIn Ad Library by company; mark in `INSTALL.md` that this source is for B2B members and that coverage must be verified at run time.
- `tiktok_assist.md` plus `tiktok_ccl_pull.py`: the Commercial Content Library (EU/EEA/UK ads only) is pulled by script; Creative Center Top Ads is an assisted flow where the skill drives the member's browser through Claude's browser tools and saves what it sees; document both honestly.
- `apify_pull.py`: optional; runs a configurable actor id with the member's token, prints the estimated cost from the actor's listed price before running, normalizes the output to the same `ads.jsonl` schema.
- `manual_pull.py`: Lite mode; takes a list of Ad Library URLs or ad ids and fetches each detail page; or takes a folder of screenshots and builds `ads.jsonl` stubs for Claude to fill from vision.
- `media.py`: frames at 1 to 2 second intervals plus scene changes via imageio-ffmpeg; poster; duration; a contact sheet per video.
- `transcribe.py`: whisper transcripts with timestamps; graceful "no transcript available" when the model is not installed.
- `landing.py`: fetches each landing page, saves text, a full-page screenshot and the above-the-fold screenshot, and records the offer, price and CTA found.
- `render.py`: the port of `pw.py`: HTML template plus a JSON of fields to PNG at 1080x1080, 1080x1350, 1080x1920, and layered MP4 for simple motion; brand variables (colors, fonts, wordmark) from `business/brand.json`; a `textstats` check for legibility at phone size.
- `higgsfield.py`: wraps `higgsfield-client`; model ids as path strings (for example `higgsfield-ai/soul/v2/standard` for stills; read the docs for the current image-to-video endpoints before hard-coding any); submits with an idempotency key; polls status; downloads outputs within the retention window; prints the estimated price from `tools/higgsfield_prices.json` before every run; refuses below the member's credit floor; logs every run to `bank/renders/HIGGSFIELD.md`. Generated media is for mood and b-roll; the skill refuses prompts that would fabricate screenshots, results, people presented as customers, or anything the asset catalog cannot support.
- `finance.py`: reads `business/finance.md` (YAML frontmatter), prints every formula with its result, writes `plan/economics.md`.
- `readout.py`: parses an Ads Manager export (detect columns; tolerate renames), computes hook rate, hold rate, CTR, CPC, CVR, CPA, frequency per ad, applies the decision rules from `library/finance/decision-rules.md`, writes `plan/readouts/<date>.md`.
- `export.py`: builds `bank/ad-bank.html` (the board) and `bank/ad-bank.csv`; the board is static HTML with no external dependencies, filterable by persona, concept, format and status, and shows for each entry the hook, the why, the competitor references and the critic note.
- `progress.py`: maintains `PROGRESS.md` and `changelog.md` with stable ids, counts and timestamps so a member can resume.

## 5. Skills (Phase 4): contracts

For each skill write the frontmatter, a one-paragraph purpose, inputs, what it reads, what it writes, when it asks the member something (rarely, with defaults), how it reports (one status line per unit of work; a finished / doing now / next summary at the end), and how it updates `PROGRESS.md`. Specific requirements:

- `setup`: `disable-model-invocation: true`; runs `setup.py` then `doctor.py`; explains Lite mode if setup fails.
- `start`: detects whether tooling is present; creates `adlab-workspace/`; prints the flow; offers to run intake.
- `intake`: fetches the site and its pricing, about, reviews and FAQ pages; drafts `brief.md` as observed facts only; then asks the two interrogation batches from `library/prompts/intake-questions.md` with defaults; writes `offer.md` (positioning components in Dunford's order), `finance.md` with a frontmatter template, `brand.json` (colors, fonts, wordmark path if found); for the no-site member, builds the same from text. Ends with the five customers question (three to five real customers or situations).
- `competitors`: three rings with confidence and the reason each qualifies; search methods in this order: the member's own answer, search engines ("alternatives to", "vs", "best X for Y"), category directories and review sites, Ad Library keyword searches on the category's language (advertisers who use the same words are competitors for attention even when the product differs), community threads; writes `roster.md` and `roster.json`; the member confirms and edits before pull.
- `pull`: builds the plan from the roster; runs the pull tools in the background; default caps 40 ads per advertiser, 8 advertisers; honest counts (Meta's reported totals versus what loaded); `--mode manual` for Lite.
- `process`: runs media, transcribe and landing; writes `ads/<advertiser>/<id>/ad.md` with transcript, shot list, on-screen text and the landing summary; records `inspection_coverage` per ad.
- `analyze`: fans out to `ad-analyst` subagents at `low` effort in batches of about 15 ads each, with the rubric preloaded; collects `analysis/ads.csv`; then you (at full effort) write `competitor-<x>.md` per advertiser and `market-map.md` with every section from the rubric file, including the evidence limits section.
- `personas`: `persona-builder` agent; sources: brief, interrogation answers, the persona evidence column of `ads.csv`, review and comment text gathered by `researcher`, the five customers; three to seven files plus `coverage.md`; member reviews; revisions preserve prior versions.
- `interrogate`: `psychologist` agent with `library/prompts/interrogation.md`; the fixed schema; every challenge cites ad ids and persona files.
- `angles`: coverage matrix persona x awareness x angle family x proof x format with rejected cells explained; the opposite pass; eight to twelve concept briefs with the CPA they must beat left blank until `plan` fills it; `critic` note on each.
- `bank`: `copywriter` and `creative-director` produce per concept: three primary-text lengths, five headlines, two descriptions, six hooks, a 15, 30 and 60 second script with shot list and on-screen text, a static layout choice from `templates/`, carousel cards where the concept suits, a UGC brief, and landing continuation notes; `critic` runs the three tests and the policy checks; `export.py` builds the board and CSV; every entry carries why-it-should-work, competitor refs and risk flags.
- `assets`: catalogs everything in `assets/`; videos get frames and transcripts; the three-column table (member note, Claude's read, revised read); per-item deep dives on request; a permissions column (who appears, consent status) that blocks use when unknown.
- `render`: `static` renders the chosen layouts at three sizes; `storyboard` renders frame boards for video concepts; `higgsfield` only with a key, with price and floor checks; AI-generated media is labeled in the bank entry.
- `plan`: `finance-analyst`; fills the CPA on every concept; writes `test-plan.md`: one broad ad set, six to twelve concepts, three to six hooks each, budget per concept from the formulas, the reading order of signals, the decision rules, the refresh cadence; says plainly that this is a hypothesis-testing plan, not a forecast.
- `readout`: runs `readout.py`; explains which rule fired per concept and what to do next; appends to `changelog.md`.
- `refresh`: re-pulls the roster; diffs new, dead, and ads crossing 30, 60 and 90 days; flags new advertisers using the category's language; appends to `changelog.md`.
- `doctor`: runs `doctor.py` and interprets.
- Internal, `user-invocable: false`: `rubric` (the per-ad rubric and allowed values), `evidence-rules`, `house-style` (plain language, labels, no hype), preloaded into agents through `skills:`.

## 6. Agents (Phase 5)

Write `agents/*.md` with `name`, `description` (specific enough that automatic delegation picks the right one), `tools`, `model`, `skills`, `effort`, `maxTurns`:

- `researcher` (web search, fetch, Bash for the pull tools; `medium`): competitor discovery, review and comment mining, landing pages.
- `ad-analyst` (`sonnet`, `low`; preloads `rubric` and `evidence-rules`): one rubric row per ad from `ad.md`, frames and transcript; must fill `inspection_coverage` honestly.
- `psychologist` (`inherit`, `high`; preloads `house-style`): the interrogation; the Sutherland lens on the market map; the opposite pass.
- `persona-builder` (`inherit`, `medium`).
- `copywriter` (`inherit`, `medium`; preloads `rubric`): direct response in plain language; every line passes the three tests.
- `creative-director` (`inherit`, `medium`): formats, layouts, scripts, shot lists, storyboards.
- `finance-analyst` (`sonnet`, `medium`): economics and the test plan.
- `critic` (`inherit`, `high`; preloads `evidence-rules`): truth, policy, cliché and the two-second stranger test; writes notes, never silently edits.
- `librarian` (`sonnet`, `low`): appends observed patterns to `library/observed/` with ad ids.

## 7. Templates and the board (Phase 6)

HTML templates for the static formats in the library's format taxonomy (at least: text-only ugly ad, us-versus-them, three reasons, review card, founder note, offer card, problem card, carousel card, storyboard frame). CSS variables for brand colors and fonts; one real moment or one real result fills the frame; words on the image are the hook, an optional kicker, the offer line and the wordmark. The board (`ad-bank.html`) is a single static file. Styles to avoid in the board and the templates: cream or off-white page backgrounds, italic accent words in headlines, numbered "01/02/03" section labels, pill-shaped buttons, purple-to-blue gradients, emoji in headings, drop shadows on every card, centered hero paragraphs. Check the first render and extend this list in `DECISIONS.md`.

## 8. Example runs (Phase 7)

Run the full flow twice with real pulls, default caps, and no keys: one Skool community (ask me which; the default is Operators Workshop, for which a roster and Meta data from an earlier pull already exist) and one physical-product brand (ask me which; if I do not answer, choose a public DTC brand with an active Meta presence and say so in `DECISIONS.md`). Store the complete `adlab-workspace/` of each under `examples/<run-name>/` with media kept to poster frames and contact sheets so the repo stays small; keep the full media out of git. These runs are what a member reads before installing. They must honor every truth rule; the critic pass runs on both.

## 9. Docs and lessons (Phase 8)

`START-HERE.md` (what it does, what it does not do, the twenty-minute first run); `INSTALL.md` (both install routes, the zip fallback, Windows notes, updating); `FAQ.md`; `LEGAL-AND-ETHICS.md` (read-only research on the member's own machine, no login, gentle pacing, competitor creatives never republished, platform terms may restrict automated access so the Apify and manual routes exist, generated media is labeled, no fabricated proof); `CHANGELOG.md`; and `docs/lessons/` with six short lesson scripts for the Skool classroom (install and first run; reading your market map; personas to angles; bank to render; test plan and readout; the refresh loop), each ending with a "post your X in the thread" prompt.

## 10. QA and release (Phase 9)

Create a fresh user profile directory, install from the repo with the documented commands, run `/adlab:setup` and `/adlab:start`, then run intake on a third business in Lite mode to prove the no-Python path. Fix what breaks. Run `claude plugin validate --strict ./`. Run the critic over both example banks. Bump nothing; tag `v0.1.0`. Finish with the checklist fully checked and a final report in this format: finished / doing now / next, with one-line asks only.

## 11. Acceptance criteria per phase (put these in `BUILD-CHECKLIST.md`)

- Phase 0: `DECISIONS.md` opened; `BUILD-CHECKLIST.md` created from this document; repo initialized; the design packet copied to `docs/design/`.
- Phase 1: layout exists; `plugin.json` and `marketplace.json` valid; `claude plugin validate --strict ./` passes on the skeleton; `claude --plugin-dir ./` lists the skills.
- Phase 2: sixty-plus library files; each follows the skeleton; cross-links resolve; no invented statistics; the two Shotton files carry the verification note; `prompts/interrogation.md` contains the member's original stance and the grounding schema.
- Phase 3: every tool has `--help`, a fixture test that passes, and a dry run where it spends; `meta_pull.py` reproduces a 20-ad pull on a known advertiser with media downloaded; `render.py` produces the three sizes from a template; `finance.py` prints formulas and results for both worked examples; `higgsfield.py` dry-runs without a key.
- Phase 4: every skill has frontmatter, inputs, outputs, asks and reporting; internal skills are hidden; scripts are pre-approved via `allowed-tools`; `PROGRESS.md` updates from every skill.
- Phase 5: nine agents with the specified fields; `ad-analyst` preloads the rubric; the critic never edits silently.
- Phase 6: templates render at phone size legibly; the board opens offline and filters.
- Phase 7: two example runs complete with brief, roster, ads.csv, market map, personas, interrogation, concepts, bank board and CSV, asset catalog (may be empty with the template), test plan, PROGRESS.md and changelog; truth rules verified by the critic.
- Phase 8: all docs and six lesson scripts present.
- Phase 9: fresh-profile install succeeds on this Mac; Lite mode proven; tag `v0.1.0`.

## 12. What to report to me at the end

Finished / doing now / next, one-line asks only, the checklist state, the two install commands, and the three things you are least sure about. Do not ask me for screenshots or lookups; where only I can do something (for example pushing the repo, choosing the public owner name, adding the Skool lesson), hand me a paste-ready instruction.

---

## Appendix A: the member's original interrogation prompt (keep this stance verbatim in `library/prompts/interrogation.md`)

# Rory Sutherland-Style Marketing Interrogation Prompt

You are a ruthless, deeply creative marketing strategist using the principles of Rory Sutherland, Ogilvy-style behavioral science, behavioral economics, consumer psychology, positioning, brand strategy, and startup growth.

Your job is not to give generic marketing advice.

Your job is to grill, interrogate, rip apart, reframe, and psychologically decode the business idea below, then produce the 7 highest-leverage marketing recommendations possible.

Think like this:

Most businesses do not have a marketing problem. They have a perception problem, a trust problem, a category problem, a status problem, a context problem, a pricing signal problem, a social proof problem, a ritual problem, or a "people do not know how to emotionally understand this" problem.

Do not treat the customer as a rational calculator. Treat them as a status-aware, story-driven, ambiguity-averse, emotionally interpretive human being who makes decisions through cues, habits, shortcuts, social meaning, fear, aspiration, trust, identity, and post-rationalization.

## Appendix B: the member's product idea in their own words (context, not spec)

An ads-library "deep researcher": the member downloads the artifact, briefly describes their business or inserts their website, and it does deep research on the business, finds competitors, looks through the ad libraries, builds a full list of competitors with samples of their videos and ad copy and the personas they target, then cross-references the member's business against the competitors and generates the member's own versions for their own brand (possibly through Higgsfield, possibly through Claude Code generating images). Members can create multiple personas, connect all their assets so the tool can see what each asset is for, and go as deep as they want per item and per video, with the member's explanation and Claude's explanation side by side and revised together. It needs to analyze marketing, sales and finance, look into sales tactics and sales psychology, and showcase ad copy that works, built on Rory Sutherland's principles and the tips of people of his caliber.
