# Changelog

## 0.1.0 (2026-10-23)

First release.

- 17 commands: setup, start, doctor, intake, competitors, pull, process, analyze, personas, interrogate, angles, bank, assets, render, plan, readout, refresh.
- 9 agents: researcher, ad-analyst, psychologist, persona-builder, copywriter, creative-director, finance-analyst, critic, librarian.
- Library of 90 files: psychology, strategy, copy, sales, finance, platform, rubrics, prompts.
- Tools: Meta Ad Library pull (read-only, no login), Google Transparency Center, LinkedIn Ad Library and TikTok Commercial Content Library pulls, manual and Apify routes, media frames, transcription, landing capture, HTML template renderer, Higgsfield client with price display, finance calculator, Ads Manager readout, board exporter, progress tracker, doctor.
- Ten templates: nine statics (text-only ugly, us-versus-them, three reasons, review card, founder note, offer card, problem card, photo hook, carousel card) and a storyboard.
- Two complete example runs (Operators Workshop and a stand-in wallet brand) from intake to test plan, each with the critic's notes in the files and a critic report.

### Fixed before release

- Eight agents and skills (copywriter, finance-analyst; analyze, assets, bank, interrogate, plan, process) had an unquoted ": " in their frontmatter description, which made Claude Code load them with empty metadata. Quoted; `claude plugin validate --strict` now passes on the plugin manifest as well as the marketplace manifest, and `tools/tests/test_manifests.py` guards it.
- `tools/render.py` now runs the 9:16 overlay check its help text promised (top 250, bottom 400, right 120 px) and flags text that overflows the bottom of the frame; the 9:16 template padding now follows `library/platform/specs-and-safe-zones.md`, so the offer line and wordmark sit above the platform controls.
- The photo-hook template keeps its kicker legible when no photo is set (brand colour behind the image, a stronger top scrim, an empty image hidden).
- `tools/readout.py` reads the threshold keys `/adlab:plan` writes, accepts the spellings in `library/finance/decision-rules.md`, and skips a rule whose threshold the member has not set (null) instead of failing; it does not say "scale" until a frequency ceiling is set; `skills/plan/SKILL.md` names the keys.
- `library/rubrics/bank-entry-schema.md` now uses the `cNN-eNN` entry ids and `pN` persona ids that the bank and render skills use; `library/rubrics/concept-brief-schema.md` gives concept files the frontmatter `tools/export.py` reads.
