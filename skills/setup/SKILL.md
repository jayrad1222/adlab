---
name: setup
description: Install Ad Lab's Python tooling (venv, Playwright, Chromium; optional whisper and API keys) into the plugin data folder, then run the doctor. Run once per machine.
argument-hint: "[--with-transcription] [--keys] [--skip-browser]"
disable-model-invocation: true
allowed-tools: Bash(python3 -I ${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python3 -I "${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python -I ${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python -I "${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(${CLAUDE_PLUGIN_DATA}/venv/bin/python *), Read
---
# /adlab:setup

**Purpose.** One-time install of the tools behind Full mode. Takes 3 to 8 minutes, mostly the Chromium download (about 150 MB). Nothing is installed system-wide; everything goes under `${CLAUDE_PLUGIN_DATA}` (or `~/.adlab` when that variable is unset).

**Before running, tell the member in one line:** what will be installed, where, and how long it takes. Then run it.

## Steps

1. Run the installer with the member's flags (`$ARGUMENTS`), using the system Python:
   `python3 -I "${CLAUDE_PLUGIN_ROOT}/tools/setup.py" $ARGUMENTS`
   On Windows use `python` instead of `python3`. If the member passed `--keys`, the installer prompts in the terminal and never echoes values; do not ask them to paste keys into chat.
2. The installer ends by running the doctor in quick mode. If anything shows `FIX`, read the fix line and do it (for example rerun Chromium install with the venv interpreter it names). Then run the full doctor once:
   `python3 -I "${CLAUDE_PLUGIN_ROOT}/tools/run.py" doctor`
3. If the full doctor's "meta ad library loads" check fails because of a login or checkpoint page, say so plainly: wait and retry later, or use Lite mode (`/adlab:pull --mode manual`). Do not retry in a loop.
4. If the member wants transcription later: `python3 -I "${CLAUDE_PLUGIN_ROOT}/tools/setup.py" --with-transcription --skip-browser`.

## Outputs

`${CLAUDE_PLUGIN_DATA}/venv/`, `config.json` (chmod 600), `setup.log`.

## Report

finished / doing now / next. State whether Full mode is ready, and that Lite mode works regardless. Suggest `/adlab:start` next.
