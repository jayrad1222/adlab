---
name: assets
description: "Catalog everything the member drops into assets/ (photos, videos, screenshots, testimonials, logos): what each shows, what it can and cannot prove, persona and angle fit, needed edits, permissions; a three-column note per item (member's note, Claude's read, revised read) with per-item deep dives on request."
argument-hint: "[--item <file>] [--note <file> \"text\"]"
allowed-tools: Bash(python3 -I ${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python3 -I "${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python -I ${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python -I "${CLAUDE_PLUGIN_ROOT}/tools/*), Read, Write, Edit, Agent
---
# /adlab:assets

**Purpose.** Know what you have before you claim anything. Schema: `${CLAUDE_PLUGIN_ROOT}/library/rubrics/asset-catalog-schema.md`. Truth rules: the preloaded `evidence-rules`. Mark running.

## Steps

1. List `assets/` (recursively; ignore `catalog.md`). For videos run `run.py media --video <file> --out assets/.work/<slug>` and `run.py transcribe --video ...` so you can read frames and speech. Read images directly.
2. For each file write a row in `assets/catalog.md` with every schema field: file, type, what it shows (observed), what it can prove and cannot (a dated warehouse photo proves the warehouse exists on that date; it does not prove revenue), quality at phone size, persona and angle fit (ids), needed edit, the member's note (blank until they write one), Claude's read, the revised read (blank), permissions (who appears, consent status: granted / unknown / not needed), status.
3. Permissions block use: any file showing a person other than the member, or a customer's words, stays `consent: unknown` and cannot be referenced by a bank entry until the member marks it granted. Say this once.
4. **Member notes.** Invite the member to annotate: they can edit the "member's note" column directly or run `--note <file> "text"`. On each note, rewrite the revised read for that item and update persona and angle fit; keep the previous read in the row's history line.
5. `--item <file>`: a deep dive on one asset: a shot-by-shot or region-by-region read, every claim it could support with the exact wording allowed, every claim it cannot, and three bank entries it could carry.
6. Mark done with the item count and the number awaiting consent.

## Outputs

`assets/catalog.md`, `assets/.work/` (frames and transcripts, ignored by export).

## Report

finished / doing now / next; one-line ask: notes or consent marks. Suggest `/adlab:bank` (to attach proof) or `/adlab:render`.
