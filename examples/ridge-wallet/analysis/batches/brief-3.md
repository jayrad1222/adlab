# Batch 3: per-ad rubric rows for the Ridge wallet example run

You are the ad-analyst for Ad Lab. Work directory: `adlab`. Workspace: `examples/ridge-wallet`.

READ FIRST (these define the columns and the allowed values; do not invent values outside them):
- `skills/rubric/SKILL.md`
- `skills/evidence-rules/SKILL.md`
- `library/rubrics/per-ad-rubric.md` (the full field instructions and a fictional example row)

Your batch (ad_id | advertiser | match | folder | what exists):
912140034982191 | Bellroy | advertiser-page | examples/ridge-wallet/ads/bellroy/912140034982191 | ad.md,image
950853620698640 | Bellroy | advertiser-page | examples/ridge-wallet/ads/bellroy/950853620698640 | ad.md,image
958845403522598 | Bellroy | advertiser-page | examples/ridge-wallet/ads/bellroy/958845403522598 | ad.md,image
2133352764223673 | Bellroy - momo購物網  | advertiser-page | examples/ridge-wallet/ads/bellroy-momo/2133352764223673 | ad.md,image
1687936999471670 | Blessedeal | keyword-neighbor | examples/ridge-wallet/ads/blessedeal/1687936999471670 | ad.md,image,frames
2623694321383212 | Current Spaces | keyword-neighbor | examples/ridge-wallet/ads/current-spaces/2623694321383212 | ad.md,image,frames
1084569144031581 | Dango Products | advertiser-page | examples/ridge-wallet/ads/dango-products/1084569144031581 | ad.md,image,frames
1102071902279022 | Dango Products | advertiser-page | examples/ridge-wallet/ads/dango-products/1102071902279022 | ad.md,image
1396719148591918 | Dango Products | advertiser-page | examples/ridge-wallet/ads/dango-products/1396719148591918 | ad.md,image
1411342707530116 | Dango Products | advertiser-page | examples/ridge-wallet/ads/dango-products/1411342707530116 | ad.md,image
1457214629482883 | Dango Products | advertiser-page | examples/ridge-wallet/ads/dango-products/1457214629482883 | ad.md,image,frames
1736591054090233 | Dango Products | advertiser-page | examples/ridge-wallet/ads/dango-products/1736591054090233 | ad.md,image,frames
1771865427052597 | Dango Products | advertiser-page | examples/ridge-wallet/ads/dango-products/1771865427052597 | ad.md,image,frames
1822401658948250 | Dango Products | advertiser-page | examples/ridge-wallet/ads/dango-products/1822401658948250 | ad.md,image,frames
1985923242114280 | Dango Products | advertiser-page | examples/ridge-wallet/ads/dango-products/1985923242114280 | ad.md,image,frames

For each ad: read `<folder>/ad.md` (copy, dates, variant count, link, landing summary) and `<folder>/ad.json` if you need a field; look at `<folder>/card.png` or `<folder>/media/creative.jpg` with the Read tool (images render); for video ads look at `<folder>/frames/contact.jpg` and the `<folder>/frames/s-*.jpg` scene frames. There are no transcripts in this run (no whisper installed), so video ads can be at most `still-reviewed`; say so in `weak` when the spoken track mattered.

Column mapping: `first_seen` = start_date; `days_active_at_capture` = days_active; `status` = active or inactive from is_active; `page_or_account` = advertiser_id; `variant_count` = variant_count; `duration_s` from media.json duration when present else unknown. `unknown` wherever you did not observe. `hook_text` is the first line of the primary text, or the first on-screen line of a video if that is what a viewer meets first; name which in `visual_hook`. `persona_evidence` quotes the words or describes the image that made you infer the persona. `sutherland_lens` is one sentence: the perception problem the ad solves and whether it fits the persona. `works`, `weak`, `adaptation_idea`: one sentence each; `adaptation_idea` names a persona situation and an angle family, or `none`. Days active is a fact, not a verdict; never call anything a winner. Use the slugs exactly as `skills/rubric/SKILL.md` lists them.

OUTPUT: write `examples/ridge-wallet/analysis/batches/batch-3.csv` with the Write tool. First line is exactly the 36-column CSV header from `per-ad-rubric.md` (the `ad_id,...` line). Then one properly quoted CSV row per ad (quote any field containing commas, quotes or newlines; double internal quotes). No other text in the file. Then reply with one line: the path and the row count, plus any ad you could not read and why.
