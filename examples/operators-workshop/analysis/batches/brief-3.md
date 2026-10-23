# Batch 3: per-ad rubric rows for the Operators Workshop example run

You are the ad-analyst for Ad Lab. Work directory: `adlab`. Workspace: `examples/operators-workshop`.

READ FIRST (these define the columns and the allowed values; do not invent values outside them):
- `skills/rubric/SKILL.md`
- `skills/evidence-rules/SKILL.md`
- `library/rubrics/per-ad-rubric.md` (the full field instructions and a fictional example row)

Your batch (ad_id | advertiser | match | folder | what exists):
935595112679546 | Acti-V : Perte de Poids et Microbiome | keyword-neighbor | examples/operators-workshop/ads/acti-v-perte-de-poids-et-microbiome/935595112679546 | ad.md,image,frames
1417552993798822 | Apex Dental Marketing | keyword-neighbor | examples/operators-workshop/ads/apex-dental-marketing/1417552993798822 | ad.md,image,frames
1040148231921228 | Arcads AI | advertiser-page | examples/operators-workshop/ads/arcads-ai/1040148231921228 | ad.md,image
1231104560075127 | Arcads AI | advertiser-page | examples/operators-workshop/ads/arcads-ai/1231104560075127 | ad.md,image,frames
1523784102863150 | Arcads AI | advertiser-page | examples/operators-workshop/ads/arcads-ai/1523784102863150 | ad.md,image,frames
1540277927809358 | Arcads AI | advertiser-page | examples/operators-workshop/ads/arcads-ai/1540277927809358 | ad.md,image,frames
1685025776088110 | Arcads AI | advertiser-page | examples/operators-workshop/ads/arcads-ai/1685025776088110 | ad.md,image,frames
1734177540920708 | Arcads AI | advertiser-page | examples/operators-workshop/ads/arcads-ai/1734177540920708 | ad.md,image,frames
2126173977953160 | Arcads AI | advertiser-page | examples/operators-workshop/ads/arcads-ai/2126173977953160 | ad.md,image
2129005484694134 | Arcads AI | advertiser-page | examples/operators-workshop/ads/arcads-ai/2129005484694134 | ad.md,image,frames
2265069670962872 | Arcads AI | advertiser-page | examples/operators-workshop/ads/arcads-ai/2265069670962872 | ad.md,image,frames
2502491940222808 | Arcads AI | keyword-neighbor | examples/operators-workshop/ads/arcads-ai/2502491940222808 | ad.md,image,frames
2618868331892815 | Arcads AI | advertiser-page | examples/operators-workshop/ads/arcads-ai/2618868331892815 | ad.md,image
4405193209727676 | Arcads AI | advertiser-page | examples/operators-workshop/ads/arcads-ai/4405193209727676 | ad.md,image,frames
710487895220380 | Arcads AI | advertiser-page | examples/operators-workshop/ads/arcads-ai/710487895220380 | ad.md,image,frames

For each ad: read `<folder>/ad.md` (copy, dates, variant count, link, landing summary) and `<folder>/ad.json` if you need a field; look at `<folder>/card.png` or `<folder>/media/creative.jpg` with the Read tool (images render); for video ads look at `<folder>/frames/contact.jpg` and the `<folder>/frames/s-*.jpg` scene frames. There are no transcripts in this run (no whisper installed), so video ads can be at most `still-reviewed`; say so in `weak` when the spoken track mattered.

Column mapping: `first_seen` = start_date; `days_active_at_capture` = days_active; `status` = active or inactive from is_active; `page_or_account` = advertiser_id; `variant_count` = variant_count; `duration_s` from media.json duration when present else unknown. `unknown` wherever you did not observe. `hook_text` is the first line of the primary text, or the first on-screen line of a video if that is what a viewer meets first; name which in `visual_hook`. `persona_evidence` quotes the words or describes the image that made you infer the persona. `sutherland_lens` is one sentence: the perception problem the ad solves and whether it fits the persona. `works`, `weak`, `adaptation_idea`: one sentence each; `adaptation_idea` names a persona situation and an angle family, or `none`. Days active is a fact, not a verdict; never call anything a winner.

OUTPUT: write `examples/operators-workshop/analysis/batches/batch-3.csv` with the Write tool. First line is exactly the CSV header printed by `library/rubrics/per-ad-rubric.md` (36 columns, the `ad_id,...` line). Then one properly quoted CSV row per ad (quote any field containing commas, quotes or newlines; double internal quotes). No other text in the file. Then reply with one line: the path and the row count, plus any ad you could not read and why.
