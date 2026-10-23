# Batch 7: per-ad rubric rows for the Ridge wallet example run

You are the ad-analyst for Ad Lab. Work directory: `adlab`. Workspace: `examples/ridge-wallet`.

READ FIRST (these define the columns and the allowed values; do not invent values outside them):
- `skills/rubric/SKILL.md`
- `skills/evidence-rules/SKILL.md`
- `library/rubrics/per-ad-rubric.md` (the full field instructions and a fictional example row)

Your batch (ad_id | advertiser | match | folder | what exists):
2063475424239905 | Shopify1Percent | keyword-neighbor | examples/ridge-wallet/ads/shopify1percent/2063475424239905 | ad.md,image,frames
718837344646222 | SlashMode | keyword-neighbor | examples/ridge-wallet/ads/slashmode/718837344646222 | ad.md,image
1227762296142568 | The Estate Kit | keyword-neighbor | examples/ridge-wallet/ads/the-estate-kit/1227762296142568 | ad.md,image
888954367205632 | The Estate Kit | keyword-neighbor | examples/ridge-wallet/ads/the-estate-kit/888954367205632 | ad.md,image
1028460456846299 | The Ridge | advertiser-page | examples/ridge-wallet/ads/the-ridge/1028460456846299 | ad.md,image
1081840734441981 | The Ridge | advertiser-page | examples/ridge-wallet/ads/the-ridge/1081840734441981 | ad.md,image,frames
1110797578128915 | The Ridge | advertiser-page | examples/ridge-wallet/ads/the-ridge/1110797578128915 | ad.md,image
1382045620249355 | The Ridge | advertiser-page | examples/ridge-wallet/ads/the-ridge/1382045620249355 | ad.md,image
1402989268694829 | The Ridge | advertiser-page | examples/ridge-wallet/ads/the-ridge/1402989268694829 | ad.md,image,frames
1644214914045449 | The Ridge | advertiser-page | examples/ridge-wallet/ads/the-ridge/1644214914045449 | ad.md,image,frames
1668472461558360 | The Ridge | advertiser-page | examples/ridge-wallet/ads/the-ridge/1668472461558360 | ad.md,image
2211059562779279 | The Ridge | advertiser-page | examples/ridge-wallet/ads/the-ridge/2211059562779279 | ad.md,image,frames
3176541469344352 | The Ridge | advertiser-page | examples/ridge-wallet/ads/the-ridge/3176541469344352 | ad.md,image
38844454545168783 | The Ridge | advertiser-page | examples/ridge-wallet/ads/the-ridge/38844454545168783 | ad.md,image,frames
1041665274933050 | Thread Wallets | advertiser-page | examples/ridge-wallet/ads/thread-wallets/1041665274933050 | ad.md,image,frames

For each ad: read `<folder>/ad.md` (copy, dates, variant count, link, landing summary) and `<folder>/ad.json` if you need a field; look at `<folder>/card.png` or `<folder>/media/creative.jpg` with the Read tool (images render); for video ads look at `<folder>/frames/contact.jpg` and the `<folder>/frames/s-*.jpg` scene frames. There are no transcripts in this run (no whisper installed), so video ads can be at most `still-reviewed`; say so in `weak` when the spoken track mattered.

Column mapping: `first_seen` = start_date; `days_active_at_capture` = days_active; `status` = active or inactive from is_active; `page_or_account` = advertiser_id; `variant_count` = variant_count; `duration_s` from media.json duration when present else unknown. `unknown` wherever you did not observe. `hook_text` is the first line of the primary text, or the first on-screen line of a video if that is what a viewer meets first; name which in `visual_hook`. `persona_evidence` quotes the words or describes the image that made you infer the persona. `sutherland_lens` is one sentence: the perception problem the ad solves and whether it fits the persona. `works`, `weak`, `adaptation_idea`: one sentence each; `adaptation_idea` names a persona situation and an angle family, or `none`. Days active is a fact, not a verdict; never call anything a winner. Use the slugs exactly as `skills/rubric/SKILL.md` lists them.

OUTPUT: write `examples/ridge-wallet/analysis/batches/batch-7.csv` with the Write tool. First line is exactly the 36-column CSV header from `per-ad-rubric.md` (the `ad_id,...` line). Then one properly quoted CSV row per ad (quote any field containing commas, quotes or newlines; double internal quotes). No other text in the file. Then reply with one line: the path and the row count, plus any ad you could not read and why.
