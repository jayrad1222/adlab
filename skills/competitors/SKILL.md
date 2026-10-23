---
name: competitors
description: Find the member's competitors in three rings (direct, indirect, attention) with a confidence and a reason for each, write competitors/roster.md and roster.json, and get the member's yes before any pull.
argument-hint: "[--max 8] [--add \"Name\"] [--remove \"Name\"]"
allowed-tools: Bash(python3 -I ${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python3 -I "${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python -I ${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python -I "${CLAUDE_PLUGIN_ROOT}/tools/*), Read, Write, Edit, WebFetch, WebSearch, Agent
---
# /adlab:competitors

**Purpose.** A roster worth pulling. Five minutes of searching, then the member's confirmation. Reads `business/brief.md`, `offer.md` and `interrogation-answers.md`. Mark running with progress.py.

## The three rings

- **Direct**: same product or offer for the same customer.
- **Indirect**: same job to be done, a different solution (the spreadsheet, the agency, the course that teaches it, the bigger platform).
- **Attention**: a different product aimed at the same persona in the same feed; they compete for the same two seconds. Use `library/copy/angle-families.md` and the persona cues in the brief to spot them.

## Steps (delegate the searching to the `researcher` agent; keep the judgment)

1. Start from the member's own answer to "who else does the customer consider" in interrogation-answers.md.
2. Search engines: `"<category> alternatives"`, `"<competitor> vs"`, `"best <category> for <persona>"`, `"<category> reviews"`. Category directories and review sites where they exist (G2, Capterra, Trustpilot, Product Hunt, Etsy or Amazon category pages, app stores).
3. **Ad Library keyword searches on the category's language.** In Full mode: `python3 -I "${CLAUDE_PLUGIN_ROOT}/tools/run.py" meta_pull --plan <tmp plan of 3 to 6 keyword items> --out <ws>/ads/_discovery --max-per-search 30 --max-per-advertiser 3 --no-media --no-cards --terms <category words>`. Advertisers who use the member's words are competitors for attention even when the product differs. Read `<ws>/ads/_discovery/SUMMARY.md`. In Lite mode, ask the member for 3 to 5 names and search the web.
4. **Co-branded check.** If the category is creator, community, course or marketplace, note that competitor ads may run under a platform's Page (Skool runs "X with Skool" ads). The pull handles this; list the platform in roster.json `cobrand_pages`.
5. Write `competitors/roster.md`: a table (name, ring, confidence high/medium/low, why it qualifies with the observed cue, website, ad library page names if known, notes) and `competitors/roster.json` (`[{"name","ring","confidence","why","site","page_names":[],"cobrand_pages":["Skool"]}]`). Default cap 8; rank by relevance to the persona, not by size.
6. **Ask for the yes.** Show the table and ask: "Cross out any, add any, then say go." Apply `--add`/`--remove` edits. Only then mark done.

## Outputs

`competitors/roster.md`, `competitors/roster.json`, `ads/_discovery/` (Full mode).

## Report

finished / doing now / next; one-line ask: confirm the roster.
