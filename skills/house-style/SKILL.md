---
name: house-style
description: Internal. Ad Lab's writing and reporting style for every member-facing output. Preloaded into agents; not a command.
user-invocable: false
---
# House style (internal)

Full reference: `${CLAUDE_PLUGIN_ROOT}/library/prompts/house-style.md`.

- Plain language. Short sentences. One idea per sentence. No hype words (game-changing, unlock, skyrocket, secret, hack, crush, explode, 10x, effortless, revolutionary, ultimate, insane, guaranteed, proven, world-class, next-level, seamless, supercharge, dominate, massive).
- No em-dashes. No emoji in headings. No numbers without a source or a label (observed, owner-provided, inferred, hypothetical, placeholder).
- Every recommendation carries its mechanism (which framework) and its evidence (which ad ids, which persona file, which answer).
- Reports end with **finished / doing now / next** and one-line asks only. Say how long a step takes and why before starting it.
- Never ask the member for screenshots or lookups you can do yourself. When only the member can do something (keys, a decision, consent), hand them one paste-ready instruction.
- Write to files; chat is for the summary. Every skill updates `PROGRESS.md` through `tools/progress.py`.
