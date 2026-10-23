# Batch 4: per-ad rubric rows for the Ridge wallet example run

You are the ad-analyst for Ad Lab. Work directory: `adlab`. Workspace: `examples/ridge-wallet`.

READ FIRST (these define the columns and the allowed values; do not invent values outside them):
- `skills/rubric/SKILL.md`
- `skills/evidence-rules/SKILL.md`
- `library/rubrics/per-ad-rubric.md` (the full field instructions and a fictional example row)

Your batch (ad_id | advertiser | match | folder | what exists):
2326375981514940 | Dango Products | advertiser-page | examples/ridge-wallet/ads/dango-products/2326375981514940 | ad.md,image,frames
2415595505883150 | Dango Products | advertiser-page | examples/ridge-wallet/ads/dango-products/2415595505883150 | ad.md,image,frames
28157272277296138 | Dango Products | advertiser-page | examples/ridge-wallet/ads/dango-products/28157272277296138 | ad.md,image,frames
2871861499856793 | Dango Products | advertiser-page | examples/ridge-wallet/ads/dango-products/2871861499856793 | ad.md,image,frames
2937471213255837 | Dango Products | advertiser-page | examples/ridge-wallet/ads/dango-products/2937471213255837 | ad.md,image
919754070632903 | Dango Products | advertiser-page | examples/ridge-wallet/ads/dango-products/919754070632903 | ad.md,image
1014966731331323 | Ekster | advertiser-page | examples/ridge-wallet/ads/ekster/1014966731331323 | ad.md,image,frames
1063284939797681 | Ekster | advertiser-page | examples/ridge-wallet/ads/ekster/1063284939797681 | ad.md,image,frames
1311528334123319 | Ekster | advertiser-page | examples/ridge-wallet/ads/ekster/1311528334123319 | ad.md,image,frames
1425314896328840 | Ekster | advertiser-page | examples/ridge-wallet/ads/ekster/1425314896328840 | ad.md,image,frames
1552078092865585 | Ekster | advertiser-page | examples/ridge-wallet/ads/ekster/1552078092865585 | ad.md,image,frames
1562981438714928 | Ekster | advertiser-page | examples/ridge-wallet/ads/ekster/1562981438714928 | ad.md,image
1617889383260518 | Ekster | advertiser-page | examples/ridge-wallet/ads/ekster/1617889383260518 | ad.md,image,frames
1813645310085521 | Ekster | advertiser-page | examples/ridge-wallet/ads/ekster/1813645310085521 | ad.md,image,frames
1822620345763692 | Ekster | advertiser-page | examples/ridge-wallet/ads/ekster/1822620345763692 | ad.md,image,frames

For each ad: read `<folder>/ad.md` (copy, dates, variant count, link, landing summary) and `<folder>/ad.json` if you need a field; look at `<folder>/card.png` or `<folder>/media/creative.jpg` with the Read tool (images render); for video ads look at `<folder>/frames/contact.jpg` and the `<folder>/frames/s-*.jpg` scene frames. There are no transcripts in this run (no whisper installed), so video ads can be at most `still-reviewed`; say so in `weak` when the spoken track mattered.

Column mapping: `first_seen` = start_date; `days_active_at_capture` = days_active; `status` = active or inactive from is_active; `page_or_account` = advertiser_id; `variant_count` = variant_count; `duration_s` from media.json duration when present else unknown. `unknown` wherever you did not observe. `hook_text` is the first line of the primary text, or the first on-screen line of a video if that is what a viewer meets first; name which in `visual_hook`. `persona_evidence` quotes the words or describes the image that made you infer the persona. `sutherland_lens` is one sentence: the perception problem the ad solves and whether it fits the persona. `works`, `weak`, `adaptation_idea`: one sentence each; `adaptation_idea` names a persona situation and an angle family, or `none`. Days active is a fact, not a verdict; never call anything a winner. Use the slugs exactly as `skills/rubric/SKILL.md` lists them.

OUTPUT: write `examples/ridge-wallet/analysis/batches/batch-4.csv` with the Write tool. First line is exactly the 36-column CSV header from `per-ad-rubric.md` (the `ad_id,...` line). Then one properly quoted CSV row per ad (quote any field containing commas, quotes or newlines; double internal quotes). No other text in the file. Then reply with one line: the path and the row count, plus any ad you could not read and why.
