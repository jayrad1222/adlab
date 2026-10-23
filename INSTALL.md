# Install

## Requirements

- Claude Code (desktop app, CLI, or an IDE extension), version 2.1 or newer.
- For Full mode: Python 3.9 or newer on your machine. macOS ships one; on Windows install it from python.org and tick "Add to PATH". Lite mode needs nothing.

## Route 1: from the marketplace (recommended)

In Claude Code:

```
/plugin marketplace add jayrad1222/adlab
/plugin install adlab@adlab
```

Or in the desktop app: the **+** button, then **Add plugins**, and search for Ad Lab once the marketplace is added.

Then, in the project folder where you want your workspace:

```
/adlab:setup
/adlab:start
```

## Route 2: from a zip

Unzip the plugin folder somewhere permanent, then start Claude Code with it loaded:

```
claude --plugin-dir /path/to/adlab
```

Everything else is the same.

## Updating

```
claude plugin update adlab@adlab
```

Your workspace lives outside the plugin (`./adlab-workspace/`), so updates never touch your work. Tooling lives in the plugin data folder and survives updates too.

## Optional extras

- Transcription of competitor videos: `/adlab:setup --with-transcription` (installs whisper; a model download of a few hundred MB on first use).
- Paid pulls through Apify or renders through the Higgsfield API: `/adlab:setup --keys`. Keys are typed in the terminal, stored in `config.json` with owner-only permissions, and never printed back. Every paid call shows its price first and needs your yes.

## Windows notes

- Use `python` where the docs say `python3`.
- The venv interpreter is `%USERPROFILE%\.adlab\venv\Scripts\python.exe` (or under the plugin data folder when Claude Code sets one).
- If PowerShell blocks scripts, you do not need to run any; Ad Lab calls Python directly.
- The Windows path has been written and reviewed but not run on a Windows machine in this release. If anything fails, `/adlab:doctor` prints the fix, and Lite mode works regardless.

## Uninstall

`/plugin uninstall adlab@adlab`, then delete `~/.adlab` (or the plugin data folder) if you want the tooling gone. Your workspace is yours; delete it or keep it.
