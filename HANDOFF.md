# Hand-off: finishing Ad Lab on Opus 5.5

Written 2026-10-23 by the session that built Phases 0 to 6, 8 and most of 7 and 9. Read this first, then `BUILD-CHECKLIST.md`, `DECISIONS.md`, and the two example workspaces' `PROGRESS.md`. The spec is `docs/design/02-OPUS-5.5-BUILD-PROMPT.md`; the completion condition is its section 0.3.

## State (updated 2026-10-23 by the Opus 5.5 session that finished the build)

- **Release:** v0.1.0 on `main`, published as `jayrad1222/adlab` from a single clean commit (see the redaction entry in DECISIONS.md). Both manifests validate strictly (`claude plugin validate --strict ./` and `claude plugin validate --strict ./.claude-plugin/plugin.json`); 51 tests pass (`python3 -I -m unittest discover -s tools/tests -p "test_*.py"`). 21 skills (17 model-visible; setup, pull, render and refresh are member-only), 9 agents, 90 library files, 23 Python files in `tools/`, 10 templates. Version 0.2.0 (tag `v0.2.0` on `main`) adds `/adlab:review` and `tools/scan.py`.
- **Example run A** (`examples/operators-workshop/`): every step from intake to plan is done in PROGRESS.md (setup, readout and refresh are skipped with the reason). Interrogation version 3, 11 concepts (version 2, c09 and c11 at version 3, critic notes and author replies in each), 32 bank entries with a critic note each (13 pass: 10 ready, 3 rendered at 1:1, 4:5 and 9:16; 19 held for assets, consent, the landing or week one), an empty asset catalog by design, a test plan and thresholds, and `analysis/critic-report.md` (no invented proof; the open items are founder decisions and assets).
- **Example run B** (`examples/ridge-wallet/`): the same chain. Four more Ridge pages were captured for the angles step (returns, warranty, a product page with five featured reviews, the wallets collection). Interrogation version 3, 10 concepts, 32 entries (11 pass: 8 ready, 3 rendered; 21 held), a test plan and `analysis/critic-report.md` (no invented proof).
- **Interpreter for live tools:** the builder's own venv with Playwright and Chromium installed (any venv made by `tools/setup.py` works). Tools that need no browser run as `python3 -I tools/<tool>.py`.

## What changed in the finishing session (see DECISIONS.md and CHANGELOG.md)

- Eight agents and skills had frontmatter that strict YAML rejected (an unquoted ": " in the description); they would have loaded with empty metadata. Fixed, and guarded by `tools/tests/test_manifests.py`. Validate the plugin manifest, not only the marketplace manifest.
- `tools/render.py` now checks the 9:16 overlay zones its help promised; the 9:16 template padding follows the specs file; the photo-hook kicker stays legible without a photo.
- `tools/readout.py` reads the threshold keys the plan writes, skips a rule the member has not set, and does not scale without a frequency ceiling.
- The bank-entry and concept-brief schemas now match what the skills and `export.py` use (`cNN-eNN` ids, `pN` personas, concept frontmatter).

## Remaining work

Nothing in the build. What is left is the member's: push the repo and choose the public owner name (Jared), the founders' decisions and assets that the run A critic report lists, and for Ridge the owner decisions that run B's report lists (a stand-in, so these stay open by design).

## Things learned that the spec did not say

- Subagents at `low` effort on the per-ad rubric produce good rows but slip on enum slugs; `tools/rows.py merge` normalizes common variants and rejects the rest. Keep using it rather than editing CSV by hand.
- Meta's typeahead matches homonyms (a pottery studio named Maker School; a Polish course for Claude Code Club). The pull keeps them; the synthesis excludes them and says so in the evidence limits. Keep that discipline.
- Keyword searches with very large result counts (50,001) rendered nothing in the 5-second window; not fixed. A longer settle or narrower terms is the workaround.
- The EU transparency block has not been observed on any ad yet; `eu` stays null and the docs say best effort.
- Standing rules for the Operators Workshop example: no guarantees, no done-for-you, no income promises; never launch or edit ads; Skool is read-only; nothing synthetic of a real person without written consent. Report in finished / doing now / next with one-line asks.
