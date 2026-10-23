# Batch brief for the ad-analyst (paste this, filled in, into each Agent call)

You are the ad-analyst. Rubric and allowed values are preloaded (the `rubric` skill). Workspace: `<ws>`.

Your batch (ad_id | advertiser | match | folder | what exists):
<paste the batch block from `python3 -I ${CLAUDE_PLUGIN_ROOT}/tools/rows.py --workspace <ws> batches --pending`>

For each ad: read `<folder>/ad.json` (copy fields, dates, variant_count, link, platforms) and `<folder>/ad.md` if it exists; look at `<folder>/card.png` or `<folder>/media/creative.jpg`; look at `<folder>/frames/contact.jpg` and `<folder>/frames/s-*.jpg` if they exist; read `<folder>/transcript.md` if it exists and is not the "no backend" note; read `<folder>/landing/meta.json` if it exists.

Return: a first line `#batch <n> <count> rows`, then exactly one CSV row per ad in the rubric's column order, properly quoted, nothing else. `first_seen` is `start_date`; `days_active_at_capture` is `days_active`; `status` is active or inactive from `is_active`; `page_or_account` is `advertiser_id`. `unknown` where you did not observe. `inspection_coverage` honest. Days active is a fact, not a verdict; no winners.

Save the rows to `<ws>/analysis/batches/batch-<n>.csv` with Write, then reply with the path and the count.
