# Batch 1: per-ad rubric rows for the Ridge wallet example run

You are the ad-analyst for Ad Lab. Work directory: `adlab`. Workspace: `examples/ridge-wallet`.

READ FIRST (these define the columns and the allowed values; do not invent values outside them):
- `skills/rubric/SKILL.md`
- `skills/evidence-rules/SKILL.md`
- `library/rubrics/per-ad-rubric.md` (the full field instructions and a fictional example row)

Your batch (ad_id | advertiser | match | folder | what exists):
1131011726095206 | Andar | advertiser-page | examples/ridge-wallet/ads/andar/1131011726095206 | ad.md,image,frames
1315996623672010 | Andar | advertiser-page | examples/ridge-wallet/ads/andar/1315996623672010 | ad.md,image,frames
1428488879491057 | Andar | advertiser-page | examples/ridge-wallet/ads/andar/1428488879491057 | ad.md,image,frames
1439199331507895 | Andar | advertiser-page | examples/ridge-wallet/ads/andar/1439199331507895 | ad.md,image,frames
1497445808883066 | Andar | advertiser-page | examples/ridge-wallet/ads/andar/1497445808883066 | ad.md,image,frames
1520735273186403 | Andar | advertiser-page | examples/ridge-wallet/ads/andar/1520735273186403 | ad.md,image,frames
1586458106013811 | Andar | advertiser-page | examples/ridge-wallet/ads/andar/1586458106013811 | ad.md,image,frames
1803652474397216 | Andar | advertiser-page | examples/ridge-wallet/ads/andar/1803652474397216 | ad.md,image,frames
1916199539545345 | Andar | advertiser-page | examples/ridge-wallet/ads/andar/1916199539545345 | ad.md,image,frames
1988858838459438 | Andar | advertiser-page | examples/ridge-wallet/ads/andar/1988858838459438 | ad.md,image,frames
2162436151816342 | Andar | advertiser-page | examples/ridge-wallet/ads/andar/2162436151816342 | ad.md,image,frames
2323595761732589 | Andar | advertiser-page | examples/ridge-wallet/ads/andar/2323595761732589 | ad.md,image,frames
2551744741976028 | Andar | advertiser-page | examples/ridge-wallet/ads/andar/2551744741976028 | ad.md,image,frames
2635860816867558 | Andar | advertiser-page | examples/ridge-wallet/ads/andar/2635860816867558 | ad.md,image,frames
3633657103475043 | Andar | advertiser-page | examples/ridge-wallet/ads/andar/3633657103475043 | ad.md,image,frames

For each ad: read `<folder>/ad.md` (copy, dates, variant count, link, landing summary) and `<folder>/ad.json` if you need a field; look at `<folder>/card.png` or `<folder>/media/creative.jpg` with the Read tool (images render); for video ads look at `<folder>/frames/contact.jpg` and the `<folder>/frames/s-*.jpg` scene frames. There are no transcripts in this run (no whisper installed), so video ads can be at most `still-reviewed`; say so in `weak` when the spoken track mattered.

Column mapping: `first_seen` = start_date; `days_active_at_capture` = days_active; `status` = active or inactive from is_active; `page_or_account` = advertiser_id; `variant_count` = variant_count; `duration_s` from media.json duration when present else unknown. `unknown` wherever you did not observe. `hook_text` is the first line of the primary text, or the first on-screen line of a video if that is what a viewer meets first; name which in `visual_hook`. `persona_evidence` quotes the words or describes the image that made you infer the persona. `sutherland_lens` is one sentence: the perception problem the ad solves and whether it fits the persona. `works`, `weak`, `adaptation_idea`: one sentence each; `adaptation_idea` names a persona situation and an angle family, or `none`. Days active is a fact, not a verdict; never call anything a winner. Use the slugs exactly as `skills/rubric/SKILL.md` lists them.

OUTPUT: write `examples/ridge-wallet/analysis/batches/batch-1.csv` with the Write tool. First line is exactly the 36-column CSV header from `per-ad-rubric.md` (the `ad_id,...` line). Then one properly quoted CSV row per ad (quote any field containing commas, quotes or newlines; double internal quotes). No other text in the file. Then reply with one line: the path and the row count, plus any ad you could not read and why.
