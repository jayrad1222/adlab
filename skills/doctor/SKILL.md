---
name: doctor
description: Diagnose a broken Ad Lab step (install, browser, network, workspace) and print the fix in plain words.
argument-hint: "[--quick]"
allowed-tools: Bash(python3 -I ${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python3 -I "${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python -I ${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python -I "${CLAUDE_PLUGIN_ROOT}/tools/*), Read
---
# /adlab:doctor

Run `python3 -I "${CLAUDE_PLUGIN_ROOT}/tools/run.py" doctor $ARGUMENTS --workspace <ws>` and read the output.

For each `FIX` line, do the fix if it is something you can run (reinstall a package, install Chromium with the venv interpreter it names, create the workspace). If it is something only the member can do (network, disk, a login wall on Meta), say exactly what and why in one line.

Common cases:
- **Meta shows a login or checkpoint page.** Meta sometimes rate-limits an address. Wait an hour and retry, or continue in Lite mode with `/adlab:pull --mode manual`. Never try to log in.
- **Chromium missing.** `<venv python> -m playwright install chromium`.
- **No venv.** `/adlab:setup`.
- **A pull stopped early with "capped".** That is the per-advertiser or total cap, not an error; raise `--max-per-advertiser` or `--max-total` if the member wants more.
- **A tool fails with a traceback.** Read `<ws>/ads/run.log` or the tool's output; if the Ad Library markup changed, say so and fall back to card screenshots read by eye (`--no-media` still saves cards).

Report finished / doing now / next.
