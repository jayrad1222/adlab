# Ad Lab build checklist

Source of truth for build state. Update as work lands. Spec: `docs/design/02-OPUS-5.5-BUILD-PROMPT.md`.

## Completion condition
- [x] `claude plugin validate --strict ./` passes (marketplace manifest, and the plugin manifest with every agent and skill: `claude plugin validate --strict ./.claude-plugin/plugin.json`; fixed 2026-10-23, see DECISIONS)
- [x] Clean user profile installs the plugin from the repo with the two documented commands and runs `/adlab:start`
- [x] `/adlab:setup` installs the Python tooling on macOS without manual steps (Windows path written and reviewed; not run on Windows here)
- [x] Two complete example runs under `examples/` with every artifact listed in section 5 (brief, roster, ads.csv, market map, personas, interrogation, concepts, bank board and CSV, asset catalog, test plan, PROGRESS.md, changelog; checked 2026-10-23) of the spec
- [x] Every example artifact free of fabricated results, testimonials or counts (critic pass recorded: `examples/*/analysis/critic-report.md`, both overall pass after re-review; critic notes in every concept and bank entry)
- [x] `START-HERE.md`, `INSTALL.md`, `FAQ.md`, `LEGAL-AND-ETHICS.md`, `CHANGELOG.md` exist
- [x] Version `0.1.0` tagged (local tag on `main`; not pushed)

## Phase 0
- [x] `DECISIONS.md` opened
- [x] `BUILD-CHECKLIST.md` created
- [x] Repo initialized
- [x] Design packet copied to `docs/design/`

## Phase 1: scaffold
- [x] Layout exists; `plugin.json` and `marketplace.json` valid
- [x] `claude plugin validate --strict ./` passes on the skeleton
- [x] `claude --plugin-dir ./` lists the skills (16 visible to the model; setup, pull, render and refresh are member-only by design; checked 2026-10-23)

## Phase 2: library
- [x] Sixty-plus library files, each following the skeleton
- [x] Cross-links resolve
- [x] No invented statistics; contested claims marked
- [x] Two Shotton files carry the verification note
- [x] `prompts/interrogation.md` contains the member's original stance and the grounding schema

## Phase 3: tools
- [x] Every tool has `--help`, a fixture test that passes, and a dry run where it spends
- [x] `meta_pull.py` reproduces a 20-ad pull on a known advertiser with media downloaded
- [x] `render.py` produces the three sizes from a template
- [x] `finance.py` prints formulas and results for both worked examples
- [x] `higgsfield.py` dry-runs without a key

## Phase 4: skills
- [x] Every skill has frontmatter, inputs, outputs, asks and reporting
- [x] Internal skills hidden (`user-invocable: false`)
- [x] Scripts pre-approved via `allowed-tools`
- [x] `PROGRESS.md` updated by every skill

## Phase 5: agents
- [x] Nine agents with the specified fields
- [x] `ad-analyst` preloads the rubric
- [x] `critic` never edits silently

## Phase 6: templates and board
- [x] Templates render legibly at phone size
- [x] Board opens offline and filters

## Phase 7: example runs
- [x] Run A complete (brief, roster, ads.csv, market map, personas, interrogation, concepts, bank board and CSV, asset catalog, test plan, PROGRESS.md, changelog)
- [x] Run B complete (same)
- [x] Truth rules verified by the critic on both (interrogations, every concept and every bank entry reviewed, revised and re-reviewed; release reports in `analysis/critic-report.md`)

## Phase 8: docs
- [x] All docs present
- [x] Six lesson scripts present

## Phase 9: QA and release
- [x] Fresh-profile install succeeds on this Mac
- [x] Lite mode proven on a third business
- [x] Tag `v0.1.0`
