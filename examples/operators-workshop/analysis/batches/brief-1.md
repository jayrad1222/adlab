# Batch 1: per-ad rubric rows for the Operators Workshop example run

You are the ad-analyst for Ad Lab. Work directory: `adlab`. Workspace: `examples/operators-workshop`.

READ FIRST (these define the columns and the allowed values; do not invent values outside them):
- `skills/rubric/SKILL.md`
- `skills/evidence-rules/SKILL.md`
- `library/rubrics/per-ad-rubric.md` (the full field instructions and a fictional example row)

Your batch (ad_id | advertiser | match | folder | what exists):
2671836623213205 | 80,000 Hours | keyword-neighbor | examples/operators-workshop/ads/80-000-hours/2671836623213205 | ad.md,image
1534027074837411 | AI Automation Society | advertiser-page | examples/operators-workshop/ads/ai-automation-society/1534027074837411 | ad.md,image,frames
1750739099623552 | AI Automation Society | advertiser-page | examples/operators-workshop/ads/ai-automation-society/1750739099623552 | ad.md,image
4201948366761992 | AI Automation Society | advertiser-page | examples/operators-workshop/ads/ai-automation-society/4201948366761992 | ad.md,image
1054913050869810 | AI Operator CLUB | advertiser-page | examples/operators-workshop/ads/ai-operator-club/1054913050869810 | ad.md,image,frames
1123979320082708 | AI Operator CLUB | advertiser-page | examples/operators-workshop/ads/ai-operator-club/1123979320082708 | ad.md,image,frames
1125643543498156 | AI Operator CLUB | advertiser-page | examples/operators-workshop/ads/ai-operator-club/1125643543498156 | ad.md,image,frames
1129626886138176 | AI Operator CLUB | advertiser-page | examples/operators-workshop/ads/ai-operator-club/1129626886138176 | ad.md,image,frames
1384090043489432 | AI Operator CLUB | advertiser-page | examples/operators-workshop/ads/ai-operator-club/1384090043489432 | ad.md,image,frames
1617270070414246 | AI Operator CLUB | advertiser-page | examples/operators-workshop/ads/ai-operator-club/1617270070414246 | ad.md,image,frames
1623416949192396 | AI Operator CLUB | advertiser-page | examples/operators-workshop/ads/ai-operator-club/1623416949192396 | ad.md,image,frames
1641544464304869 | AI Operator CLUB | advertiser-page | examples/operators-workshop/ads/ai-operator-club/1641544464304869 | ad.md,image,frames
2218947982369421 | AI Operator CLUB | advertiser-page | examples/operators-workshop/ads/ai-operator-club/2218947982369421 | ad.md,image,frames
947774781312414 | AI Operator CLUB | advertiser-page | examples/operators-workshop/ads/ai-operator-club/947774781312414 | ad.md,image,frames
1013033575121449 | AI Video Bootcamp | advertiser-page | examples/operators-workshop/ads/ai-video-bootcamp/1013033575121449 | ad.md,image,frames

For each ad: read `<folder>/ad.md` (copy, dates, variant count, link, landing summary) and `<folder>/ad.json` if you need a field; look at `<folder>/card.png` or `<folder>/media/creative.jpg` with the Read tool (images render); for video ads look at `<folder>/frames/contact.jpg` and the `<folder>/frames/s-*.jpg` scene frames. There are no transcripts in this run (no whisper installed), so video ads can be at most `still-reviewed`; say so in `weak` when the spoken track mattered.

Column mapping: `first_seen` = start_date; `days_active_at_capture` = days_active; `status` = active or inactive from is_active; `page_or_account` = advertiser_id; `variant_count` = variant_count; `duration_s` from media.json duration when present else unknown. `unknown` wherever you did not observe. `hook_text` is the first line of the primary text, or the first on-screen line of a video if that is what a viewer meets first; name which in `visual_hook`. `persona_evidence` quotes the words or describes the image that made you infer the persona. `sutherland_lens` is one sentence: the perception problem the ad solves and whether it fits the persona. `works`, `weak`, `adaptation_idea`: one sentence each; `adaptation_idea` names a persona situation and an angle family, or `none`. Days active is a fact, not a verdict; never call anything a winner.

OUTPUT: write `examples/operators-workshop/analysis/batches/batch-1.csv` with the Write tool. First line is exactly the CSV header printed by `library/rubrics/per-ad-rubric.md` (36 columns, the `ad_id,...` line). Then one properly quoted CSV row per ad (quote any field containing commas, quotes or newlines; double internal quotes). No other text in the file. Then reply with one line: the path and the row count, plus any ad you could not read and why.
