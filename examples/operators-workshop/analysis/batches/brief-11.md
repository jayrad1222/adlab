# Batch 11: per-ad rubric rows for the Operators Workshop example run

You are the ad-analyst for Ad Lab. Work directory: `adlab`. Workspace: `examples/operators-workshop`.

READ FIRST (these define the columns and the allowed values; do not invent values outside them):
- `skills/rubric/SKILL.md`
- `skills/evidence-rules/SKILL.md`
- `library/rubrics/per-ad-rubric.md` (the full field instructions and a fictional example row)

Your batch (ad_id | advertiser | match | folder | what exists):
989361853587159 | Solocreatorhub | keyword-neighbor | examples/operators-workshop/ads/solocreatorhub/989361853587159 | ad.md,image,frames
1101916785561103 | The Claude Club | advertiser-page | examples/operators-workshop/ads/the-claude-club/1101916785561103 | ad.md,image
28452428547771495 | The Claude Club | advertiser-page | examples/operators-workshop/ads/the-claude-club/28452428547771495 | ad.md,image
3519104148251249 | The Claude Club | advertiser-page | examples/operators-workshop/ads/the-claude-club/3519104148251249 | ad.md,image
1822693378724104 | Thrive OBM Academy | keyword-neighbor | examples/operators-workshop/ads/thrive-obm-academy/1822693378724104 | ad.md,image
1099623276106157 | Work Abroad by Schoters Nusa Tenggara | keyword-neighbor | examples/operators-workshop/ads/work-abroad-by-schoters-nusa-tenggara/1099623276106157 | ad.md,image

For each ad: read `<folder>/ad.md` (copy, dates, variant count, link, landing summary) and `<folder>/ad.json` if you need a field; look at `<folder>/card.png` or `<folder>/media/creative.jpg` with the Read tool (images render); for video ads look at `<folder>/frames/contact.jpg` and the `<folder>/frames/s-*.jpg` scene frames. There are no transcripts in this run (no whisper installed), so video ads can be at most `still-reviewed`; say so in `weak` when the spoken track mattered.

Column mapping: `first_seen` = start_date; `days_active_at_capture` = days_active; `status` = active or inactive from is_active; `page_or_account` = advertiser_id; `variant_count` = variant_count; `duration_s` from media.json duration when present else unknown. `unknown` wherever you did not observe. `hook_text` is the first line of the primary text, or the first on-screen line of a video if that is what a viewer meets first; name which in `visual_hook`. `persona_evidence` quotes the words or describes the image that made you infer the persona. `sutherland_lens` is one sentence: the perception problem the ad solves and whether it fits the persona. `works`, `weak`, `adaptation_idea`: one sentence each; `adaptation_idea` names a persona situation and an angle family, or `none`. Days active is a fact, not a verdict; never call anything a winner.

OUTPUT: write `examples/operators-workshop/analysis/batches/batch-11.csv` with the Write tool. First line is exactly the CSV header printed by `library/rubrics/per-ad-rubric.md` (36 columns, the `ad_id,...` line). Then one properly quoted CSV row per ad (quote any field containing commas, quotes or newlines; double internal quotes). No other text in the file. Then reply with one line: the path and the row count, plus any ad you could not read and why.
