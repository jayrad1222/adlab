# Batch 4: per-ad rubric rows for the Operators Workshop example run

You are the ad-analyst for Ad Lab. Work directory: `adlab`. Workspace: `examples/operators-workshop`.

READ FIRST (these define the columns and the allowed values; do not invent values outside them):
- `skills/rubric/SKILL.md`
- `skills/evidence-rules/SKILL.md`
- `library/rubrics/per-ad-rubric.md` (the full field instructions and a fictional example row)

Your batch (ad_id | advertiser | match | folder | what exists):
836000928775594 | Arcads AI | advertiser-page | examples/operators-workshop/ads/arcads-ai/836000928775594 | ad.md,image,frames
890665233928271 | Arcads AI | advertiser-page | examples/operators-workshop/ads/arcads-ai/890665233928271 | ad.md,image,frames
1012976541448133 | Arcads AI - Newsletter   | advertiser-page | examples/operators-workshop/ads/arcads-ai-newsletter/1012976541448133 | ad.md,image
1013196774518024 | Arcads AI - Newsletter   | advertiser-page | examples/operators-workshop/ads/arcads-ai-newsletter/1013196774518024 | ad.md,image
1290239729197064 | Arcads AI - Newsletter   | advertiser-page | examples/operators-workshop/ads/arcads-ai-newsletter/1290239729197064 | ad.md,image,frames
1475803497369859 | Arcads AI - Newsletter   | advertiser-page | examples/operators-workshop/ads/arcads-ai-newsletter/1475803497369859 | ad.md,image,frames
815941064905568 | Arcads AI - Newsletter   | advertiser-page | examples/operators-workshop/ads/arcads-ai-newsletter/815941064905568 | ad.md,image,frames
999181849530786 | Arcads AI - Newsletter   | advertiser-page | examples/operators-workshop/ads/arcads-ai-newsletter/999181849530786 | ad.md,image
1799856347755967 | Avora Code | keyword-neighbor | examples/operators-workshop/ads/avora-code/1799856347755967 | ad.md,image,frames
1019944280932044 | Braydon Carter | keyword-neighbor | examples/operators-workshop/ads/braydon-carter/1019944280932044 | ad.md,image,frames
1402781731986696 | CTtheDisrupter | keyword-neighbor | examples/operators-workshop/ads/ctthedisrupter/1402781731986696 | ad.md,image
1600873014871110 | CTtheDisrupter | keyword-neighbor | examples/operators-workshop/ads/ctthedisrupter/1600873014871110 | ad.md,image
1646241300194385 | CTtheDisrupter | keyword-neighbor | examples/operators-workshop/ads/ctthedisrupter/1646241300194385 | ad.md,image
1796405758057699 | CTtheDisrupter | keyword-neighbor | examples/operators-workshop/ads/ctthedisrupter/1796405758057699 | ad.md,image
2790059451394520 | CTtheDisrupter | keyword-neighbor | examples/operators-workshop/ads/ctthedisrupter/2790059451394520 | ad.md,image

For each ad: read `<folder>/ad.md` (copy, dates, variant count, link, landing summary) and `<folder>/ad.json` if you need a field; look at `<folder>/card.png` or `<folder>/media/creative.jpg` with the Read tool (images render); for video ads look at `<folder>/frames/contact.jpg` and the `<folder>/frames/s-*.jpg` scene frames. There are no transcripts in this run (no whisper installed), so video ads can be at most `still-reviewed`; say so in `weak` when the spoken track mattered.

Column mapping: `first_seen` = start_date; `days_active_at_capture` = days_active; `status` = active or inactive from is_active; `page_or_account` = advertiser_id; `variant_count` = variant_count; `duration_s` from media.json duration when present else unknown. `unknown` wherever you did not observe. `hook_text` is the first line of the primary text, or the first on-screen line of a video if that is what a viewer meets first; name which in `visual_hook`. `persona_evidence` quotes the words or describes the image that made you infer the persona. `sutherland_lens` is one sentence: the perception problem the ad solves and whether it fits the persona. `works`, `weak`, `adaptation_idea`: one sentence each; `adaptation_idea` names a persona situation and an angle family, or `none`. Days active is a fact, not a verdict; never call anything a winner.

OUTPUT: write `examples/operators-workshop/analysis/batches/batch-4.csv` with the Write tool. First line is exactly the CSV header printed by `library/rubrics/per-ad-rubric.md` (36 columns, the `ad_id,...` line). Then one properly quoted CSV row per ad (quote any field containing commas, quotes or newlines; double internal quotes). No other text in the file. Then reply with one line: the path and the row count, plus any ad you could not read and why.
