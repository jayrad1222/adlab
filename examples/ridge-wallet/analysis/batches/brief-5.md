# Batch 5: per-ad rubric rows for the Ridge wallet example run

You are the ad-analyst for Ad Lab. Work directory: `adlab`. Workspace: `examples/ridge-wallet`.

READ FIRST (these define the columns and the allowed values; do not invent values outside them):
- `skills/rubric/SKILL.md`
- `skills/evidence-rules/SKILL.md`
- `library/rubrics/per-ad-rubric.md` (the full field instructions and a fictional example row)

Your batch (ad_id | advertiser | match | folder | what exists):
1850535302597312 | Ekster | advertiser-page | examples/ridge-wallet/ads/ekster/1850535302597312 | ad.md,image,frames
2117113273022536 | Ekster | advertiser-page | examples/ridge-wallet/ads/ekster/2117113273022536 | ad.md,image,frames
2199495037650591 | Ekster | advertiser-page | examples/ridge-wallet/ads/ekster/2199495037650591 | ad.md,image,frames
2460029297812083 | Ekster | advertiser-page | examples/ridge-wallet/ads/ekster/2460029297812083 | ad.md,image,frames
2594876510944721 | Ekster | advertiser-page | examples/ridge-wallet/ads/ekster/2594876510944721 | ad.md,image,frames
819475624524650 | Ekster | advertiser-page | examples/ridge-wallet/ads/ekster/819475624524650 | ad.md,image,frames
1955265108477113 | Embrosh | keyword-neighbor | examples/ridge-wallet/ads/embrosh/1955265108477113 | ad.md,image,frames
2386860001845657 | Healthy lifestyle | keyword-neighbor | examples/ridge-wallet/ads/healthy-lifestyle/2386860001845657 | ad.md,image,frames
1624052195780903 | Kitchen & Home Hub | keyword-neighbor | examples/ridge-wallet/ads/kitchen-home-hub/1624052195780903 | ad.md,image,frames
1669817068036369 | Kruz Wallets | keyword-neighbor | examples/ridge-wallet/ads/kruz-wallets/1669817068036369 | ad.md,image,frames
29008724368734831 | Kruz Wallets | keyword-neighbor | examples/ridge-wallet/ads/kruz-wallets/29008724368734831 | ad.md,image,frames
3645027328978840 | Kruz Wallets | keyword-neighbor | examples/ridge-wallet/ads/kruz-wallets/3645027328978840 | ad.md,image,frames
921439164088469 | Kruz Wallets | keyword-neighbor | examples/ridge-wallet/ads/kruz-wallets/921439164088469 | ad.md,image,frames
4169847356647263 | Les astuces de Jérôme | keyword-neighbor | examples/ridge-wallet/ads/les-astuces-de-jerome/4169847356647263 | ad.md,image,frames
1030406983143162 | Monos | keyword-neighbor | examples/ridge-wallet/ads/monos/1030406983143162 | ad.md,image,frames

For each ad: read `<folder>/ad.md` (copy, dates, variant count, link, landing summary) and `<folder>/ad.json` if you need a field; look at `<folder>/card.png` or `<folder>/media/creative.jpg` with the Read tool (images render); for video ads look at `<folder>/frames/contact.jpg` and the `<folder>/frames/s-*.jpg` scene frames. There are no transcripts in this run (no whisper installed), so video ads can be at most `still-reviewed`; say so in `weak` when the spoken track mattered.

Column mapping: `first_seen` = start_date; `days_active_at_capture` = days_active; `status` = active or inactive from is_active; `page_or_account` = advertiser_id; `variant_count` = variant_count; `duration_s` from media.json duration when present else unknown. `unknown` wherever you did not observe. `hook_text` is the first line of the primary text, or the first on-screen line of a video if that is what a viewer meets first; name which in `visual_hook`. `persona_evidence` quotes the words or describes the image that made you infer the persona. `sutherland_lens` is one sentence: the perception problem the ad solves and whether it fits the persona. `works`, `weak`, `adaptation_idea`: one sentence each; `adaptation_idea` names a persona situation and an angle family, or `none`. Days active is a fact, not a verdict; never call anything a winner. Use the slugs exactly as `skills/rubric/SKILL.md` lists them.

OUTPUT: write `examples/ridge-wallet/analysis/batches/batch-5.csv` with the Write tool. First line is exactly the 36-column CSV header from `per-ad-rubric.md` (the `ad_id,...` line). Then one properly quoted CSV row per ad (quote any field containing commas, quotes or newlines; double internal quotes). No other text in the file. Then reply with one line: the path and the row count, plus any ad you could not read and why.
