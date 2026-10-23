---
name: render
description: Render static entries from the HTML templates at 1:1, 4:5 and 9:16, render storyboards for video entries, and optionally generate mood or b-roll media through the Higgsfield API with the price shown first and the member's floor respected. AI media is labeled; never used as proof.
argument-hint: "static|storyboard|higgsfield [--only c01-e01] [--yes]"
disable-model-invocation: true
allowed-tools: Bash(python3 -I ${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python3 -I "${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python -I ${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python -I "${CLAUDE_PLUGIN_ROOT}/tools/*), Read, Write, Edit
---
# /adlab:render

**Purpose.** Files you can upload or hand to an editor. Specs: `${CLAUDE_PLUGIN_ROOT}/library/platform/specs-and-safe-zones.md`. Templates: `${CLAUDE_PLUGIN_ROOT}/templates/` (one real moment or one real result fills the frame; words on the image are the hook, an optional kicker, the offer line and the wordmark). Mark running.

## static

For each `bank/entries.jsonl` entry with `layout_template` (or `--only`): write its `layout_fields` to `bank/renders/<entry_id>/fields.json` (image fields are file paths from `assets/`), then
`python3 -I "${CLAUDE_PLUGIN_ROOT}/tools/run.py" render still --template "${CLAUDE_PLUGIN_ROOT}/templates/<layout_template>" --data <fields.json> --brand <ws>/business/brand.json --out <ws>/bank/renders/<entry_id> --name <entry_id>`.
Read the report it prints: fix any legibility warning (text under 11 px at phone width, clipped text) by shortening the hook or picking another template, then re-render. Look at one PNG per entry yourself at phone size. Add the PNG paths to the entry's `renders` list and set `status: rendered` if it was `ready`.

## storyboard

For each video entry: write the shot list into the storyboard template fields (six frames: hook frame, three body beats, proof beat, CTA frame; each with the on-screen text and a one-line visual) and render it with the same tool and `templates/storyboard.html`. The storyboard is a brief for a shoot or an editor, not an ad.

## higgsfield

Only with a key configured. For a mood or b-roll need named in a brief: run `run.py higgsfield price --model <model> [--seconds N]`, show the estimate and the floor from finance.md, and only after the member says yes in chat run `run.py higgsfield generate ... --yes`. The tool refuses prompts that would fabricate proof; do not reword a refused prompt to get around it. Every run is logged to `bank/renders/HIGGSFIELD.md`; mark the entry `ai_media: true` and add the label the platform requires.

Mark done with counts. Re-export the board: `python3 -I "${CLAUDE_PLUGIN_ROOT}/tools/export.py" --workspace <ws>`.

## Report

finished / doing now / next; name any entries that failed legibility. Suggest `/adlab:plan`.
