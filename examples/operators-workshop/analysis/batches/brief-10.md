# Batch 10: per-ad rubric rows for the Operators Workshop example run

You are the ad-analyst for Ad Lab. Work directory: `adlab`. Workspace: `examples/operators-workshop`.

READ FIRST (these define the columns and the allowed values; do not invent values outside them):
- `skills/rubric/SKILL.md`
- `skills/evidence-rules/SKILL.md`
- `library/rubrics/per-ad-rubric.md` (the full field instructions and a fictional example row)

Your batch (ad_id | advertiser | match | folder | what exists):
1094023723542322 | Skool | cobrand | examples/operators-workshop/ads/skool/1094023723542322 | ad.md,image,frames
1094243879909487 | Skool | cobrand | examples/operators-workshop/ads/skool/1094243879909487 | ad.md,image,frames
1105898642086436 | Skool | cobrand | examples/operators-workshop/ads/skool/1105898642086436 | ad.md,image,frames
1446844843531566 | Skool | cobrand | examples/operators-workshop/ads/skool/1446844843531566 | ad.md,image,frames
1512670714026336 | Skool | cobrand | examples/operators-workshop/ads/skool/1512670714026336 | ad.md,image,frames
1662440802157193 | Skool | cobrand | examples/operators-workshop/ads/skool/1662440802157193 | ad.md,image,frames
1769820874579277 | Skool | cobrand | examples/operators-workshop/ads/skool/1769820874579277 | ad.md,image,frames
1807946097023857 | Skool | cobrand | examples/operators-workshop/ads/skool/1807946097023857 | ad.md,image,frames
2008806906449610 | Skool | cobrand | examples/operators-workshop/ads/skool/2008806906449610 | ad.md,image,frames
2032976233999151 | Skool | cobrand | examples/operators-workshop/ads/skool/2032976233999151 | ad.md,image
28791180740542576 | Skool | cobrand | examples/operators-workshop/ads/skool/28791180740542576 | ad.md,image,frames
39180737891574736 | Skool | cobrand | examples/operators-workshop/ads/skool/39180737891574736 | ad.md,image,frames
852511001188204 | Skool | cobrand | examples/operators-workshop/ads/skool/852511001188204 | ad.md,image
1431508675329812 | Solocreatorhub | keyword-neighbor | examples/operators-workshop/ads/solocreatorhub/1431508675329812 | ad.md,image,frames
943152218357153 | Solocreatorhub | keyword-neighbor | examples/operators-workshop/ads/solocreatorhub/943152218357153 | ad.md,image,frames

For each ad: read `<folder>/ad.md` (copy, dates, variant count, link, landing summary) and `<folder>/ad.json` if you need a field; look at `<folder>/card.png` or `<folder>/media/creative.jpg` with the Read tool (images render); for video ads look at `<folder>/frames/contact.jpg` and the `<folder>/frames/s-*.jpg` scene frames. There are no transcripts in this run (no whisper installed), so video ads can be at most `still-reviewed`; say so in `weak` when the spoken track mattered.

Column mapping: `first_seen` = start_date; `days_active_at_capture` = days_active; `status` = active or inactive from is_active; `page_or_account` = advertiser_id; `variant_count` = variant_count; `duration_s` from media.json duration when present else unknown. `unknown` wherever you did not observe. `hook_text` is the first line of the primary text, or the first on-screen line of a video if that is what a viewer meets first; name which in `visual_hook`. `persona_evidence` quotes the words or describes the image that made you infer the persona. `sutherland_lens` is one sentence: the perception problem the ad solves and whether it fits the persona. `works`, `weak`, `adaptation_idea`: one sentence each; `adaptation_idea` names a persona situation and an angle family, or `none`. Days active is a fact, not a verdict; never call anything a winner.

OUTPUT: write `examples/operators-workshop/analysis/batches/batch-10.csv` with the Write tool. First line is exactly the CSV header printed by `library/rubrics/per-ad-rubric.md` (36 columns, the `ad_id,...` line). Then one properly quoted CSV row per ad (quote any field containing commas, quotes or newlines; double internal quotes). No other text in the file. Then reply with one line: the path and the row count, plus any ad you could not read and why.
