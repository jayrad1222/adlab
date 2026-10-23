# Batch 8: per-ad rubric rows for the Operators Workshop example run

You are the ad-analyst for Ad Lab. Work directory: `adlab`. Workspace: `examples/operators-workshop`.

READ FIRST (these define the columns and the allowed values; do not invent values outside them):
- `skills/rubric/SKILL.md`
- `skills/evidence-rules/SKILL.md`
- `library/rubrics/per-ad-rubric.md` (the full field instructions and a fictional example row)

Your batch (ad_id | advertiser | match | folder | what exists):
1085463157290005 | Maker School: AI Automation | advertiser-page | examples/operators-workshop/ads/maker-school-ai-automation/1085463157290005 | ad.md,image,frames
1384073453905007 | Maker School: AI Automation | advertiser-page | examples/operators-workshop/ads/maker-school-ai-automation/1384073453905007 | ad.md,image,frames
1633617958211625 | Maker School: AI Automation | advertiser-page | examples/operators-workshop/ads/maker-school-ai-automation/1633617958211625 | ad.md,image,frames
1660385472178283 | Maker School: AI Automation | advertiser-page | examples/operators-workshop/ads/maker-school-ai-automation/1660385472178283 | ad.md,image,frames
1761940881625624 | Maker School: AI Automation | advertiser-page | examples/operators-workshop/ads/maker-school-ai-automation/1761940881625624 | ad.md,image,frames
1836279407805960 | Maker School: AI Automation | advertiser-page | examples/operators-workshop/ads/maker-school-ai-automation/1836279407805960 | ad.md,image,frames
1836652044438432 | Maker School: AI Automation | advertiser-page | examples/operators-workshop/ads/maker-school-ai-automation/1836652044438432 | ad.md,image,frames
2856093574749410 | Maker School: AI Automation | advertiser-page | examples/operators-workshop/ads/maker-school-ai-automation/2856093574749410 | ad.md,image,frames
4518007081778935 | Maker School: AI Automation | advertiser-page | examples/operators-workshop/ads/maker-school-ai-automation/4518007081778935 | ad.md,image,frames
960956262925605 | Maker School: AI Automation | advertiser-page | examples/operators-workshop/ads/maker-school-ai-automation/960956262925605 | ad.md,image,frames
1940708906902849 | Miva Open University | keyword-neighbor | examples/operators-workshop/ads/miva-open-university/1940708906902849 | ad.md,image
2060144201373911 | Miva Open University | keyword-neighbor | examples/operators-workshop/ads/miva-open-university/2060144201373911 | ad.md,image
4538457029767464 | Miva Open University | keyword-neighbor | examples/operators-workshop/ads/miva-open-university/4538457029767464 | ad.md,image
1015443054328277 | Mr. Paid Social | keyword-neighbor | examples/operators-workshop/ads/mr-paid-social/1015443054328277 | ad.md,image,frames
25880119681682478 | Mr. Paid Social | keyword-neighbor | examples/operators-workshop/ads/mr-paid-social/25880119681682478 | ad.md,image,frames

For each ad: read `<folder>/ad.md` (copy, dates, variant count, link, landing summary) and `<folder>/ad.json` if you need a field; look at `<folder>/card.png` or `<folder>/media/creative.jpg` with the Read tool (images render); for video ads look at `<folder>/frames/contact.jpg` and the `<folder>/frames/s-*.jpg` scene frames. There are no transcripts in this run (no whisper installed), so video ads can be at most `still-reviewed`; say so in `weak` when the spoken track mattered.

Column mapping: `first_seen` = start_date; `days_active_at_capture` = days_active; `status` = active or inactive from is_active; `page_or_account` = advertiser_id; `variant_count` = variant_count; `duration_s` from media.json duration when present else unknown. `unknown` wherever you did not observe. `hook_text` is the first line of the primary text, or the first on-screen line of a video if that is what a viewer meets first; name which in `visual_hook`. `persona_evidence` quotes the words or describes the image that made you infer the persona. `sutherland_lens` is one sentence: the perception problem the ad solves and whether it fits the persona. `works`, `weak`, `adaptation_idea`: one sentence each; `adaptation_idea` names a persona situation and an angle family, or `none`. Days active is a fact, not a verdict; never call anything a winner.

OUTPUT: write `examples/operators-workshop/analysis/batches/batch-8.csv` with the Write tool. First line is exactly the CSV header printed by `library/rubrics/per-ad-rubric.md` (36 columns, the `ad_id,...` line). Then one properly quoted CSV row per ad (quote any field containing commas, quotes or newlines; double internal quotes). No other text in the file. Then reply with one line: the path and the row count, plus any ad you could not read and why.
