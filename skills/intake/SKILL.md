---
name: intake
description: Read the member's website (or their description), draft the business brief from observed facts, run the two-batch interrogation with defaults, and write business/brief.md, offer.md, finance.md, brand.json and interrogation-answers.md.
argument-hint: "<url | \"two-sentence description\">"
allowed-tools: Bash(python3 -I ${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python3 -I "${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python -I ${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python -I "${CLAUDE_PLUGIN_ROOT}/tools/*), Read, Write, Edit, WebFetch, WebSearch
---
# /adlab:intake

**Purpose.** Build the brand reality (what the business can truthfully claim) before anyone looks at competitors. About ten minutes of the member's time. Questions: `${CLAUDE_PLUGIN_ROOT}/library/prompts/intake-questions.md`. Positioning order: `${CLAUDE_PLUGIN_ROOT}/library/strategy/dunford-positioning.md`. Finance keys: `${CLAUDE_PLUGIN_ROOT}/library/finance/inputs.md`.

Workspace: `./adlab-workspace` or the client folder named in `adlab-workspace/ACTIVE_CLIENT`. Mark the step running: `python3 -I "${CLAUDE_PLUGIN_ROOT}/tools/progress.py" --workspace <ws> set --step intake --status running`.

## Steps

1. **Read the site** (skip if the argument is a description). In Full mode capture it: `python3 -I "${CLAUDE_PLUGIN_ROOT}/tools/run.py" landing --site <url> --out <ws>/business/site` (home plus likely pricing, about, reviews, FAQ pages; text, phone-size screenshots, prices and buttons found). In Lite mode fetch the same pages with WebFetch. Read what came back. Note what the site shows: offer, price, promise, proof, tone, visual world, who it seems to be for, the CTA.
2. **Draft `business/brief.md`** with frontmatter (`name`, `url`, `category`, `model` (membership | product | service), `price_seen`, `captured`) and sections: what it is (observed), who it seems to be for (inferred, with the cue), the promise in their words (observed), proof on the site (observed), tone and visual world (observed), claims a competitor could also make word for word (inferred), what is missing (inferred). Label every line observed, owner-provided or inferred.
3. **Interrogation, batch 1** (six questions from intake-questions.md). Ask them in one message with the default answer under each so the member can reply "defaults" or answer any subset. Wait. Then **batch 2** the same way, then the five customers question. Write every answer, verbatim, to `business/interrogation-answers.md` under the question, marked owner-provided; write accepted defaults marked default.
4. **Write `business/offer.md`** in Dunford's order: competitive alternatives (including do nothing and the spreadsheet), unique attributes, the value they enable, the customers who care most, the category the member chooses to be judged in. Add the value-equation read (dream outcome, likelihood, time delay, effort) as inferred.
5. **Write `business/finance.md`** with the frontmatter template from inputs.md. Fill what the member gave; leave the rest as placeholders marked `# placeholder`. Ask only for price and gross margin if missing; everything else can stay placeholder for now. Run `python3 -I "${CLAUDE_PLUGIN_ROOT}/tools/finance.py" --workspace <ws>` once so `plan/economics.md` exists and the member sees the breakeven logic early.
6. **Write `business/brand.json`**: `primary`, `accent`, `bg`, `text` (hex, from the site or the member), `font_head`, `font_body`, `wordmark` (text), `logo_path` if they give a file later.
7. Mark done: `progress.py ... set --step intake --status done --note "<brief one-liner>"`.

## Asks (with defaults)

The two batches and the five customers. Nothing else. If the member says "defaults", proceed.

## Outputs

`business/brief.md`, `offer.md`, `finance.md`, `brand.json`, `interrogation-answers.md`, `site/` (Full mode), `plan/economics.md`.

## Report

finished / doing now / next; suggest `/adlab:competitors`.
