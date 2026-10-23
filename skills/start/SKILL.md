---
name: start
description: Begin Ad Lab. Explains the flow in one screen, detects Full mode (tooling installed) or Lite mode, creates ./adlab-workspace/ (or a client workspace), and offers to run intake.
argument-hint: "[--client <name>]"
allowed-tools: Bash(python3 -I ${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python3 -I "${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python -I ${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python -I "${CLAUDE_PLUGIN_ROOT}/tools/*), Read, Write
---
# /adlab:start

**Purpose.** Orient the member and create the workspace. Two minutes.

## Steps

1. Decide the workspace. Default `./adlab-workspace`. With `--client <name>`: `./adlab-workspace/clients/<slug>`, and write the slug to `./adlab-workspace/ACTIVE_CLIENT` so later skills use it. Every later skill reads `ACTIVE_CLIENT` and passes `--workspace` accordingly; tell the member this.
2. Create it: `python3 -I "${CLAUDE_PLUGIN_ROOT}/tools/progress.py" --workspace <ws> init`
3. Detect mode: `python3 -I "${CLAUDE_PLUGIN_ROOT}/tools/run.py" doctor --quick`. Exit 0 means Full mode. Otherwise Lite mode: pulls are replaced by pasted links or screenshots, everything from analyze onward still works. Offer `/adlab:setup` if they want Full mode.
4. Show the flow, one line each, with rough times:
   intake (10 min with you) · competitors (5 min plus your yes) · pull (20 to 60 min unattended) · process (10 to 30 min unattended) · analyze (unattended, longest step) · personas (your review) · interrogate · angles · bank · assets (your files) · render (optional) · plan · readout (after you run ads) · refresh (later).
5. Say what the tool does not do: it never launches or edits ads, never republishes competitor creatives, never invents proof. Everything it writes is a hypothesis until a readout says otherwise.
6. Ask one question: "Paste your website URL, or describe the offer in two sentences if there is no site yet." Then run `/adlab:intake` with the answer.

## Outputs

`<ws>/PROGRESS.md`, `<ws>/changelog.md`, the folder tree.

## Report

finished / doing now / next, one-line ask (the URL or description).
