# Batch 6: per-ad rubric rows for the Operators Workshop example run

You are the ad-analyst for Ad Lab. Work directory: `adlab`. Workspace: `examples/operators-workshop`.

READ FIRST (these define the columns and the allowed values; do not invent values outside them):
- `skills/rubric/SKILL.md`
- `skills/evidence-rules/SKILL.md`
- `library/rubrics/per-ad-rubric.md` (the full field instructions and a fictional example row)

Your batch (ad_id | advertiser | match | folder | what exists):
1377610441202909 | Hashtag NoCode | advertiser-page | examples/operators-workshop/ads/hashtag-nocode/1377610441202909 | ad.md,image,frames
1467334001994239 | Hashtag NoCode | advertiser-page | examples/operators-workshop/ads/hashtag-nocode/1467334001994239 | ad.md,image
1532055512061124 | Hashtag NoCode | advertiser-page | examples/operators-workshop/ads/hashtag-nocode/1532055512061124 | ad.md,image,frames
1553453959885361 | Hashtag NoCode | advertiser-page | examples/operators-workshop/ads/hashtag-nocode/1553453959885361 | ad.md,image
1567323282101407 | Hashtag NoCode | advertiser-page | examples/operators-workshop/ads/hashtag-nocode/1567323282101407 | ad.md,image
1567476751374389 | Hashtag NoCode | advertiser-page | examples/operators-workshop/ads/hashtag-nocode/1567476751374389 | ad.md,image,frames
1613353846922990 | Hashtag NoCode | advertiser-page | examples/operators-workshop/ads/hashtag-nocode/1613353846922990 | ad.md,image
1617703866668196 | Hashtag NoCode | advertiser-page | examples/operators-workshop/ads/hashtag-nocode/1617703866668196 | ad.md,image,frames
1673198080806670 | Hashtag NoCode | advertiser-page | examples/operators-workshop/ads/hashtag-nocode/1673198080806670 | ad.md,image,frames
2219084038830459 | Hashtag NoCode | advertiser-page | examples/operators-workshop/ads/hashtag-nocode/2219084038830459 | ad.md,image,frames
2224429541749390 | Hashtag NoCode | advertiser-page | examples/operators-workshop/ads/hashtag-nocode/2224429541749390 | ad.md,image
2391436374631797 | Hashtag NoCode | advertiser-page | examples/operators-workshop/ads/hashtag-nocode/2391436374631797 | ad.md,image,frames
2533465053802504 | Hashtag NoCode | advertiser-page | examples/operators-workshop/ads/hashtag-nocode/2533465053802504 | ad.md,image,frames
1353490406100848 | Ith_marriage_intl | keyword-neighbor | examples/operators-workshop/ads/ith-marriage-intl/1353490406100848 | ad.md,image
1106125972107418 | Kurs Claude Code PRO | advertiser-page | examples/operators-workshop/ads/kurs-claude-code-pro/1106125972107418 | ad.md,image,frames

For each ad: read `<folder>/ad.md` (copy, dates, variant count, link, landing summary) and `<folder>/ad.json` if you need a field; look at `<folder>/card.png` or `<folder>/media/creative.jpg` with the Read tool (images render); for video ads look at `<folder>/frames/contact.jpg` and the `<folder>/frames/s-*.jpg` scene frames. There are no transcripts in this run (no whisper installed), so video ads can be at most `still-reviewed`; say so in `weak` when the spoken track mattered.

Column mapping: `first_seen` = start_date; `days_active_at_capture` = days_active; `status` = active or inactive from is_active; `page_or_account` = advertiser_id; `variant_count` = variant_count; `duration_s` from media.json duration when present else unknown. `unknown` wherever you did not observe. `hook_text` is the first line of the primary text, or the first on-screen line of a video if that is what a viewer meets first; name which in `visual_hook`. `persona_evidence` quotes the words or describes the image that made you infer the persona. `sutherland_lens` is one sentence: the perception problem the ad solves and whether it fits the persona. `works`, `weak`, `adaptation_idea`: one sentence each; `adaptation_idea` names a persona situation and an angle family, or `none`. Days active is a fact, not a verdict; never call anything a winner.

OUTPUT: write `examples/operators-workshop/analysis/batches/batch-6.csv` with the Write tool. First line is exactly the CSV header printed by `library/rubrics/per-ad-rubric.md` (36 columns, the `ad_id,...` line). Then one properly quoted CSV row per ad (quote any field containing commas, quotes or newlines; double internal quotes). No other text in the file. Then reply with one line: the path and the row count, plus any ad you could not read and why.
