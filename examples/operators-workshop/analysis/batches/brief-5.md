# Batch 5: per-ad rubric rows for the Operators Workshop example run

You are the ad-analyst for Ad Lab. Work directory: `adlab`. Workspace: `examples/operators-workshop`.

READ FIRST (these define the columns and the allowed values; do not invent values outside them):
- `skills/rubric/SKILL.md`
- `skills/evidence-rules/SKILL.md`
- `library/rubrics/per-ad-rubric.md` (the full field instructions and a fictional example row)

Your batch (ad_id | advertiser | match | folder | what exists):
28771184185810174 | CTtheDisrupter | keyword-neighbor | examples/operators-workshop/ads/ctthedisrupter/28771184185810174 | ad.md,image
29146458868325004 | CTtheDisrupter | keyword-neighbor | examples/operators-workshop/ads/ctthedisrupter/29146458868325004 | ad.md,image
4895138667380500 | CTtheDisrupter | keyword-neighbor | examples/operators-workshop/ads/ctthedisrupter/4895138667380500 | ad.md,image
1012466708532658 | Cerirpurtflild Sintkucre | keyword-neighbor | examples/operators-workshop/ads/cerirpurtflild-sintkucre/1012466708532658 | ad.md,image
965834386589231 | Cerirpurtflild Sintkucre | keyword-neighbor | examples/operators-workshop/ads/cerirpurtflild-sintkucre/965834386589231 | ad.md,image
1470555241558217 | Chris Martin CEO | keyword-neighbor | examples/operators-workshop/ads/chris-martin-ceo/1470555241558217 | ad.md,image,frames
2342052149666159 | Chris Martin CEO | keyword-neighbor | examples/operators-workshop/ads/chris-martin-ceo/2342052149666159 | ad.md,image,frames
2405590020181280 | Chris Martin CEO | keyword-neighbor | examples/operators-workshop/ads/chris-martin-ceo/2405590020181280 | ad.md,image,frames
1906674503325314 | Clouddevopshub | keyword-neighbor | examples/operators-workshop/ads/clouddevopshub/1906674503325314 | ad.md,image,frames
940521275692490 | DAT Bootcamp | keyword-neighbor | examples/operators-workshop/ads/dat-bootcamp/940521275692490 | ad.md,image,frames
2524515458043699 | Essential Health Finds | keyword-neighbor | examples/operators-workshop/ads/essential-health-finds/2524515458043699 | ad.md,image
1120940773602615 | Grow with Rudy | keyword-neighbor | examples/operators-workshop/ads/grow-with-rudy/1120940773602615 | ad.md,image,frames
1651358503217361 | Grow with Rudy | keyword-neighbor | examples/operators-workshop/ads/grow-with-rudy/1651358503217361 | ad.md,image,frames
1107235645044624 | Hartamas Academy | keyword-neighbor | examples/operators-workshop/ads/hartamas-academy/1107235645044624 | ad.md,image
1089534664056623 | Hashtag NoCode | advertiser-page | examples/operators-workshop/ads/hashtag-nocode/1089534664056623 | ad.md,image,frames

For each ad: read `<folder>/ad.md` (copy, dates, variant count, link, landing summary) and `<folder>/ad.json` if you need a field; look at `<folder>/card.png` or `<folder>/media/creative.jpg` with the Read tool (images render); for video ads look at `<folder>/frames/contact.jpg` and the `<folder>/frames/s-*.jpg` scene frames. There are no transcripts in this run (no whisper installed), so video ads can be at most `still-reviewed`; say so in `weak` when the spoken track mattered.

Column mapping: `first_seen` = start_date; `days_active_at_capture` = days_active; `status` = active or inactive from is_active; `page_or_account` = advertiser_id; `variant_count` = variant_count; `duration_s` from media.json duration when present else unknown. `unknown` wherever you did not observe. `hook_text` is the first line of the primary text, or the first on-screen line of a video if that is what a viewer meets first; name which in `visual_hook`. `persona_evidence` quotes the words or describes the image that made you infer the persona. `sutherland_lens` is one sentence: the perception problem the ad solves and whether it fits the persona. `works`, `weak`, `adaptation_idea`: one sentence each; `adaptation_idea` names a persona situation and an angle family, or `none`. Days active is a fact, not a verdict; never call anything a winner.

OUTPUT: write `examples/operators-workshop/analysis/batches/batch-5.csv` with the Write tool. First line is exactly the CSV header printed by `library/rubrics/per-ad-rubric.md` (36 columns, the `ad_id,...` line). Then one properly quoted CSV row per ad (quote any field containing commas, quotes or newlines; double internal quotes). No other text in the file. Then reply with one line: the path and the row count, plus any ad you could not read and why.
