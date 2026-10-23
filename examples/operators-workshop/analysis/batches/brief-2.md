# Batch 2: per-ad rubric rows for the Operators Workshop example run

You are the ad-analyst for Ad Lab. Work directory: `adlab`. Workspace: `examples/operators-workshop`.

READ FIRST (these define the columns and the allowed values; do not invent values outside them):
- `skills/rubric/SKILL.md`
- `skills/evidence-rules/SKILL.md`
- `library/rubrics/per-ad-rubric.md` (the full field instructions and a fictional example row)

Your batch (ad_id | advertiser | match | folder | what exists):
1065715359472023 | AI Video Bootcamp | advertiser-page | examples/operators-workshop/ads/ai-video-bootcamp/1065715359472023 | ad.md,image,frames
1403311474997024 | AI Video Bootcamp | advertiser-page | examples/operators-workshop/ads/ai-video-bootcamp/1403311474997024 | ad.md,image
1416360690414714 | AI Video Bootcamp | advertiser-page | examples/operators-workshop/ads/ai-video-bootcamp/1416360690414714 | ad.md,image,frames
1429775445162176 | AI Video Bootcamp | advertiser-page | examples/operators-workshop/ads/ai-video-bootcamp/1429775445162176 | ad.md,image,frames
1506202640947121 | AI Video Bootcamp | advertiser-page | examples/operators-workshop/ads/ai-video-bootcamp/1506202640947121 | ad.md,image,frames
1587585239519935 | AI Video Bootcamp | advertiser-page | examples/operators-workshop/ads/ai-video-bootcamp/1587585239519935 | ad.md,image,frames
1611195850348762 | AI Video Bootcamp | advertiser-page | examples/operators-workshop/ads/ai-video-bootcamp/1611195850348762 | ad.md,image,frames
1801930964690191 | AI Video Bootcamp | advertiser-page | examples/operators-workshop/ads/ai-video-bootcamp/1801930964690191 | ad.md,image,frames
1894923588153698 | AI Video Bootcamp | advertiser-page | examples/operators-workshop/ads/ai-video-bootcamp/1894923588153698 | ad.md,image,frames
1920683551935476 | AI Video Bootcamp | advertiser-page | examples/operators-workshop/ads/ai-video-bootcamp/1920683551935476 | ad.md,image
1994721787907520 | AI Video Bootcamp | advertiser-page | examples/operators-workshop/ads/ai-video-bootcamp/1994721787907520 | ad.md,image,frames
2294005904669622 | AI Video Bootcamp | advertiser-page | examples/operators-workshop/ads/ai-video-bootcamp/2294005904669622 | ad.md,image,frames
28188256047504517 | AI Video Bootcamp | advertiser-page | examples/operators-workshop/ads/ai-video-bootcamp/28188256047504517 | ad.md,image,frames
3366900353513536 | AI Video Bootcamp | advertiser-page | examples/operators-workshop/ads/ai-video-bootcamp/3366900353513536 | ad.md,image,frames
2341052899967522 | AI Video-Academy | advertiser-page | examples/operators-workshop/ads/ai-video-academy/2341052899967522 | ad.md,image,frames

For each ad: read `<folder>/ad.md` (copy, dates, variant count, link, landing summary) and `<folder>/ad.json` if you need a field; look at `<folder>/card.png` or `<folder>/media/creative.jpg` with the Read tool (images render); for video ads look at `<folder>/frames/contact.jpg` and the `<folder>/frames/s-*.jpg` scene frames. There are no transcripts in this run (no whisper installed), so video ads can be at most `still-reviewed`; say so in `weak` when the spoken track mattered.

Column mapping: `first_seen` = start_date; `days_active_at_capture` = days_active; `status` = active or inactive from is_active; `page_or_account` = advertiser_id; `variant_count` = variant_count; `duration_s` from media.json duration when present else unknown. `unknown` wherever you did not observe. `hook_text` is the first line of the primary text, or the first on-screen line of a video if that is what a viewer meets first; name which in `visual_hook`. `persona_evidence` quotes the words or describes the image that made you infer the persona. `sutherland_lens` is one sentence: the perception problem the ad solves and whether it fits the persona. `works`, `weak`, `adaptation_idea`: one sentence each; `adaptation_idea` names a persona situation and an angle family, or `none`. Days active is a fact, not a verdict; never call anything a winner.

OUTPUT: write `examples/operators-workshop/analysis/batches/batch-2.csv` with the Write tool. First line is exactly the CSV header printed by `library/rubrics/per-ad-rubric.md` (36 columns, the `ad_id,...` line). Then one properly quoted CSV row per ad (quote any field containing commas, quotes or newlines; double internal quotes). No other text in the file. Then reply with one line: the path and the row count, plus any ad you could not read and why.
