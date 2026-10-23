# Batch 6: per-ad rubric rows for the Ridge wallet example run

You are the ad-analyst for Ad Lab. Work directory: `adlab`. Workspace: `examples/ridge-wallet`.

READ FIRST (these define the columns and the allowed values; do not invent values outside them):
- `skills/rubric/SKILL.md`
- `skills/evidence-rules/SKILL.md`
- `library/rubrics/per-ad-rubric.md` (the full field instructions and a fictional example row)

Your batch (ad_id | advertiser | match | folder | what exists):
1589827862670498 | Monos | keyword-neighbor | examples/ridge-wallet/ads/monos/1589827862670498 | ad.md,image
1604203081062483 | My Estate Kit | keyword-neighbor | examples/ridge-wallet/ads/my-estate-kit/1604203081062483 | ad.md,image
1773011874117399 | My Estate Kit | keyword-neighbor | examples/ridge-wallet/ads/my-estate-kit/1773011874117399 | ad.md,image
2190223528442324 | My Estate Kit | keyword-neighbor | examples/ridge-wallet/ads/my-estate-kit/2190223528442324 | ad.md,image
1417781337206546 | Nomad | keyword-neighbor | examples/ridge-wallet/ads/nomad/1417781337206546 | ad.md,image
1555225689001452 | Nomad | keyword-neighbor | examples/ridge-wallet/ads/nomad/1555225689001452 | ad.md,image
1781413329550236 | Nomad | keyword-neighbor | examples/ridge-wallet/ads/nomad/1781413329550236 | ad.md,image
1938402000163741 | Nomad | keyword-neighbor | examples/ridge-wallet/ads/nomad/1938402000163741 | ad.md,image
28022125120763124 | Nomad | keyword-neighbor | examples/ridge-wallet/ads/nomad/28022125120763124 | ad.md,image
4598955600339573 | Nomad | keyword-neighbor | examples/ridge-wallet/ads/nomad/4598955600339573 | ad.md,image
893141733556087 | Nomad | keyword-neighbor | examples/ridge-wallet/ads/nomad/893141733556087 | ad.md,image
1616785086769214 | Ridge EU | advertiser-page | examples/ridge-wallet/ads/ridge-eu/1616785086769214 | ad.md,image
4072538929716078 | Ridge UK | advertiser-page | examples/ridge-wallet/ads/ridge-uk/4072538929716078 | ad.md,image
1068638472734300 | Ryan Westbrook | keyword-neighbor | examples/ridge-wallet/ads/ryan-westbrook/1068638472734300 | ad.md,image,frames
1980082592608739 | Shopify1Percent | keyword-neighbor | examples/ridge-wallet/ads/shopify1percent/1980082592608739 | ad.md,image,frames

For each ad: read `<folder>/ad.md` (copy, dates, variant count, link, landing summary) and `<folder>/ad.json` if you need a field; look at `<folder>/card.png` or `<folder>/media/creative.jpg` with the Read tool (images render); for video ads look at `<folder>/frames/contact.jpg` and the `<folder>/frames/s-*.jpg` scene frames. There are no transcripts in this run (no whisper installed), so video ads can be at most `still-reviewed`; say so in `weak` when the spoken track mattered.

Column mapping: `first_seen` = start_date; `days_active_at_capture` = days_active; `status` = active or inactive from is_active; `page_or_account` = advertiser_id; `variant_count` = variant_count; `duration_s` from media.json duration when present else unknown. `unknown` wherever you did not observe. `hook_text` is the first line of the primary text, or the first on-screen line of a video if that is what a viewer meets first; name which in `visual_hook`. `persona_evidence` quotes the words or describes the image that made you infer the persona. `sutherland_lens` is one sentence: the perception problem the ad solves and whether it fits the persona. `works`, `weak`, `adaptation_idea`: one sentence each; `adaptation_idea` names a persona situation and an angle family, or `none`. Days active is a fact, not a verdict; never call anything a winner. Use the slugs exactly as `skills/rubric/SKILL.md` lists them.

OUTPUT: write `examples/ridge-wallet/analysis/batches/batch-6.csv` with the Write tool. First line is exactly the 36-column CSV header from `per-ad-rubric.md` (the `ad_id,...` line). Then one properly quoted CSV row per ad (quote any field containing commas, quotes or newlines; double internal quotes). No other text in the file. Then reply with one line: the path and the row count, plus any ad you could not read and why.
