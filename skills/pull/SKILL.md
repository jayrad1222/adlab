---
name: pull
description: Pull competitor ads from the public ad libraries for the confirmed roster (Meta, Google Transparency Center, LinkedIn for B2B, TikTok where visible). Read-only, no login, gentle pacing; runs in the background. Modes scrape (default), apify, manual.
argument-hint: "[--mode scrape|apify|manual] [--max 40] [--inactive] [--sources meta,google,linkedin,tiktok] [--urls ... | --screenshots DIR]"
disable-model-invocation: true
allowed-tools: Bash(python3 -I ${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python3 -I "${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python -I ${CLAUDE_PLUGIN_ROOT}/tools/*), Bash(python -I "${CLAUDE_PLUGIN_ROOT}/tools/*), Read, Write
---
# /adlab:pull

**Purpose.** Collect the ads with their copy, media, dates, variant counts and landing links. Takes 20 to 60 minutes unattended for 8 advertisers; say so, then run it in the background and keep working with the member. Manners are built in: one page at a time, 2 to 4 second pauses, no login, never likes or follows. Sources and their limits: `${CLAUDE_PLUGIN_ROOT}/library/platform/ad-library-sources.md`. Mark running with progress.py.

## Steps

1. Read `competitors/roster.json`. Refuse to pull if the roster is unconfirmed (no `confirmed: true` or no changelog line saying confirmed); run `/adlab:competitors` first.
2. **Build the Meta plan** `ads/plan.json`: for each roster entry a `name` item (keyword search plus typeahead-matched Pages), a `page` item for each known `page_names` id, and a `cobrand` item when `cobrand_pages` is set. Add 2 to 4 category `keyword` items from the brief as attention searches. Terms: the member's brand words and category words.
3. **Run Meta** in the background:
   `python3 -I "${CLAUDE_PLUGIN_ROOT}/tools/run.py" meta_pull --plan <ws>/ads/plan.json --out <ws>/ads --max-per-advertiser <max, default 40> --max-total 400 --terms <terms> --cobrand-pages <pages> [--include-inactive] [--eu-details 20]`
   Add `--include-inactive` when `--inactive` was given (useful for refresh and for seeing what died). Add `--eu-details 20` to capture EU reach blocks for ads that also ran in the EU.
4. **Run the other sources** (also background, after Meta or in parallel): Google (`run.py google_pull --advertisers <names> --domains <sites> --out <ws>/ads --max-per-advertiser 10`; one page load per creative, so ten take about four minutes; video ads come back as YouTube links, not files), LinkedIn only when the brief says B2B (`run.py linkedin_pull --advertisers <names> --out <ws>/ads`; dates and impressions show only for EU-delivered ads), TikTok CCL (`run.py tiktok_ccl_pull --advertisers <names> --out <ws>/ads --max-per-search 20`; EEA, Switzerland and UK ads only; the site throttles repeated loads, so keep it small and rerun later). For TikTok Creative Center, which needs a login for details, offer the assisted path in `${CLAUDE_PLUGIN_ROOT}/tools/tiktok_assist.md` (the member's own browser; you read what it shows) and do not scrape it.
5. **Mode apify** (needs a token and the member's `--yes`): write the actor input from the plan, show the price with `run.py apify_pull --actor <id> --price`, and only run after the member confirms the spend in chat.
6. **Mode manual (Lite)**: `run.py manual_pull --urls ... --out <ws>/ads` or `--screenshots DIR --advertiser "Name"`. For screenshot stubs, read each image yourself and fill `body_text`, `title`, `cta_text`, `format`, `advertiser` in the stub's `ad.json`, then set `inspection_coverage` to still-reviewed in analyze.
7. When the runs finish, read `<ws>/ads/SUMMARY.md` and `searches.csv`. Report honest counts: ads loaded versus Meta's reported totals, how many were capped, which roster names returned zero on their own Page (and whether co-branded ads covered them), and which searches errored. Mark done with the count.

## Outputs

`ads/ads.jsonl`, `ads/searches.csv`, `ads/run.log`, `ads/SUMMARY.md`, `ads/<advertiser>/<ad_id>/{ad.json, card.png, media/}`.

## Report

finished / doing now / next with the counts and caveats; suggest `/adlab:process`.
