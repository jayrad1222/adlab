# Batch 2: per-ad rubric rows for the Ridge wallet example run

You are the ad-analyst for Ad Lab. Work directory: `adlab`. Workspace: `examples/ridge-wallet`.

READ FIRST (these define the columns and the allowed values; do not invent values outside them):
- `skills/rubric/SKILL.md`
- `skills/evidence-rules/SKILL.md`
- `library/rubrics/per-ad-rubric.md` (the full field instructions and a fictional example row)

Your batch (ad_id | advertiser | match | folder | what exists):
2631280750656473 | Arthritis Support Community | keyword-neighbor | examples/ridge-wallet/ads/arthritis-support-community/2631280750656473 | ad.md,image
4459729837672055 | Arthritis Support Community | keyword-neighbor | examples/ridge-wallet/ads/arthritis-support-community/4459729837672055 | ad.md,image
1741809623402993 | Astrid Leather | keyword-neighbor | examples/ridge-wallet/ads/astrid-leather/1741809623402993 | ad.md,image
1046004753909784 | Bellroy | advertiser-page | examples/ridge-wallet/ads/bellroy/1046004753909784 | ad.md,image
1194881345055884 | Bellroy | advertiser-page | examples/ridge-wallet/ads/bellroy/1194881345055884 | ad.md,image,frames
1497017115093052 | Bellroy | advertiser-page | examples/ridge-wallet/ads/bellroy/1497017115093052 | ad.md,image
1714986336331015 | Bellroy | advertiser-page | examples/ridge-wallet/ads/bellroy/1714986336331015 | ad.md,image
2165783148149714 | Bellroy | advertiser-page | examples/ridge-wallet/ads/bellroy/2165783148149714 | ad.md,image,frames
412656131438903 | Bellroy | advertiser-page | examples/ridge-wallet/ads/bellroy/412656131438903 | ad.md,image,frames
4131865890367392 | Bellroy | advertiser-page | examples/ridge-wallet/ads/bellroy/4131865890367392 | ad.md,image
4170616893072944 | Bellroy | advertiser-page | examples/ridge-wallet/ads/bellroy/4170616893072944 | ad.md,image
513444261432452 | Bellroy | advertiser-page | examples/ridge-wallet/ads/bellroy/513444261432452 | ad.md,image
663640986473052 | Bellroy | advertiser-page | examples/ridge-wallet/ads/bellroy/663640986473052 | ad.md,image
861547736912965 | Bellroy | advertiser-page | examples/ridge-wallet/ads/bellroy/861547736912965 | ad.md,image
893004099363085 | Bellroy | advertiser-page | examples/ridge-wallet/ads/bellroy/893004099363085 | ad.md,image,frames

For each ad: read `<folder>/ad.md` (copy, dates, variant count, link, landing summary) and `<folder>/ad.json` if you need a field; look at `<folder>/card.png` or `<folder>/media/creative.jpg` with the Read tool (images render); for video ads look at `<folder>/frames/contact.jpg` and the `<folder>/frames/s-*.jpg` scene frames. There are no transcripts in this run (no whisper installed), so video ads can be at most `still-reviewed`; say so in `weak` when the spoken track mattered.

Column mapping: `first_seen` = start_date; `days_active_at_capture` = days_active; `status` = active or inactive from is_active; `page_or_account` = advertiser_id; `variant_count` = variant_count; `duration_s` from media.json duration when present else unknown. `unknown` wherever you did not observe. `hook_text` is the first line of the primary text, or the first on-screen line of a video if that is what a viewer meets first; name which in `visual_hook`. `persona_evidence` quotes the words or describes the image that made you infer the persona. `sutherland_lens` is one sentence: the perception problem the ad solves and whether it fits the persona. `works`, `weak`, `adaptation_idea`: one sentence each; `adaptation_idea` names a persona situation and an angle family, or `none`. Days active is a fact, not a verdict; never call anything a winner. Use the slugs exactly as `skills/rubric/SKILL.md` lists them.

OUTPUT: write `examples/ridge-wallet/analysis/batches/batch-2.csv` with the Write tool. First line is exactly the 36-column CSV header from `per-ad-rubric.md` (the `ad_id,...` line). Then one properly quoted CSV row per ad (quote any field containing commas, quotes or newlines; double internal quotes). No other text in the file. Then reply with one line: the path and the row count, plus any ad you could not read and why.
