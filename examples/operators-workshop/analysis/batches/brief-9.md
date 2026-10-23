# Batch 9: per-ad rubric rows for the Operators Workshop example run

You are the ad-analyst for Ad Lab. Work directory: `adlab`. Workspace: `examples/operators-workshop`.

READ FIRST (these define the columns and the allowed values; do not invent values outside them):
- `skills/rubric/SKILL.md`
- `skills/evidence-rules/SKILL.md`
- `library/rubrics/per-ad-rubric.md` (the full field instructions and a fictional example row)

Your batch (ad_id | advertiser | match | folder | what exists):
834247362492467 | Mr. Paid Social | keyword-neighbor | examples/operators-workshop/ads/mr-paid-social/834247362492467 | ad.md,image,frames
1067363192787128 | NLM Consumer Goods Trading | keyword-neighbor | examples/operators-workshop/ads/nlm-consumer-goods-trading/1067363192787128 | ad.md,image
1063611693297007 | Nitin Andey | keyword-neighbor | examples/operators-workshop/ads/nitin-andey/1063611693297007 | ad.md,image
1980315969322824 | Nitin Andey | keyword-neighbor | examples/operators-workshop/ads/nitin-andey/1980315969322824 | ad.md,image
2122127781987303 | Nitin Andey | keyword-neighbor | examples/operators-workshop/ads/nitin-andey/2122127781987303 | ad.md,image
2437466690115961 | Nitin Andey | keyword-neighbor | examples/operators-workshop/ads/nitin-andey/2437466690115961 | ad.md,image
1439548628041867 | Orangutan.ia | keyword-neighbor | examples/operators-workshop/ads/orangutan-ia/1439548628041867 | ad.md,image,frames
1449771073866297 | Orangutan.ia | keyword-neighbor | examples/operators-workshop/ads/orangutan-ia/1449771073866297 | ad.md,image
27682986321375890 | Orangutan.ia | keyword-neighbor | examples/operators-workshop/ads/orangutan-ia/27682986321375890 | ad.md,image
1068918252179664 | Planet Smart City India | keyword-neighbor | examples/operators-workshop/ads/planet-smart-city-india/1068918252179664 | ad.md,image,frames
1421746219828247 | Planet Smart City India | keyword-neighbor | examples/operators-workshop/ads/planet-smart-city-india/1421746219828247 | ad.md,image,frames
1393995022127669 | Prismas Consultoria | keyword-neighbor | examples/operators-workshop/ads/prismas-consultoria/1393995022127669 | ad.md,image,frames
4206175853006205 | Shelby Sapp | keyword-neighbor | examples/operators-workshop/ads/shelby-sapp/4206175853006205 | ad.md,image,frames
1086075447748545 | Skool | cobrand | examples/operators-workshop/ads/skool/1086075447748545 | ad.md,image,frames
1087402847240240 | Skool | cobrand | examples/operators-workshop/ads/skool/1087402847240240 | ad.md,image,frames

For each ad: read `<folder>/ad.md` (copy, dates, variant count, link, landing summary) and `<folder>/ad.json` if you need a field; look at `<folder>/card.png` or `<folder>/media/creative.jpg` with the Read tool (images render); for video ads look at `<folder>/frames/contact.jpg` and the `<folder>/frames/s-*.jpg` scene frames. There are no transcripts in this run (no whisper installed), so video ads can be at most `still-reviewed`; say so in `weak` when the spoken track mattered.

Column mapping: `first_seen` = start_date; `days_active_at_capture` = days_active; `status` = active or inactive from is_active; `page_or_account` = advertiser_id; `variant_count` = variant_count; `duration_s` from media.json duration when present else unknown. `unknown` wherever you did not observe. `hook_text` is the first line of the primary text, or the first on-screen line of a video if that is what a viewer meets first; name which in `visual_hook`. `persona_evidence` quotes the words or describes the image that made you infer the persona. `sutherland_lens` is one sentence: the perception problem the ad solves and whether it fits the persona. `works`, `weak`, `adaptation_idea`: one sentence each; `adaptation_idea` names a persona situation and an angle family, or `none`. Days active is a fact, not a verdict; never call anything a winner.

OUTPUT: write `examples/operators-workshop/analysis/batches/batch-9.csv` with the Write tool. First line is exactly the CSV header printed by `library/rubrics/per-ad-rubric.md` (36 columns, the `ad_id,...` line). Then one properly quoted CSV row per ad (quote any field containing commas, quotes or newlines; double internal quotes). No other text in the file. Then reply with one line: the path and the row count, plus any ad you could not read and why.
