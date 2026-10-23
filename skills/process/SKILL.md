---
name: process
description: "Prepare every pulled ad for analysis: video frames and contact sheets, transcripts when whisper is installed, on-screen text read from frames, and landing-page captures. Writes ads/<advertiser>/<ad_id>/ad.md per ad."
argument-hint: "[--max-landing 60] [--no-transcripts]"
allowed-tools: Bash(python3 -I ${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python3 -I "${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python -I ${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python -I "${CLAUDE_PLUGIN_ROOT}/tools/*), Read, Write, Agent
---
# /adlab:process

**Purpose.** Turn media into things an analyst can read. 10 to 30 minutes unattended depending on video count. Mark running.

## Steps

1. Frames: `python3 -I "${CLAUDE_PLUGIN_ROOT}/tools/run.py" media --all <ws>/ads` (every video gets frames every 2 s, scene-change frames, a poster and a contact sheet).
2. Transcripts: `run.py transcribe --all <ws>/ads` unless `--no-transcripts`. If no backend is installed it writes a note and continues; say so once, not per ad.
3. Landing pages: `run.py landing --all <ws>/ads --max <n>` (phone-size fold and full-page screenshots, text, prices and buttons; read-only).
4. **Write `ad.md` per ad**: run `python3 -I "${CLAUDE_PLUGIN_ROOT}/tools/admd.py" --workspace <ws>` to write the reading sheet (copy fields, dates, variant count, frame list, transcript, landing summary, honest coverage ceiling) for every ad; then, for video ads, use subagents at low effort in batches of about 15 to append a shot list read from the contact sheet and scene frames (what is in frame, in order, with the on-screen text). The sheet holds the ad.s copy fields from `ad.json`, the transcript (or "no transcript"), a shot list from the contact sheet and scene frames (what is in frame, in order, with the on-screen text you can read), the landing summary (title, h1, prices, buttons, does it continue the ad's promise), and a `coverage` line: `copy-only`, `still-reviewed` or `video-watched` (transcript AND frames read). Keep each ad.md under 120 lines.
5. Mark done with the ad count. Note how many had video, how many got transcripts, how many landing captures failed.

## Outputs

`ads/<advertiser>/<ad_id>/{frames/, media.json, transcript.md, landing/, ad.md}`.

## Report

finished / doing now / next; suggest `/adlab:analyze`.
