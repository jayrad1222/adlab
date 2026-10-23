# TikTok Creative Center: the assisted path

TikTok's Creative Center "Top Ads" is a curated gallery of advertiser-authorized high performers, not an archive, and brand-specific search and ad details need a TikTok login. Ad Lab does not scrape it and does not log in.

What the skill does instead, when the member wants TikTok coverage beyond the Commercial Content Library (which covers EEA, Switzerland and UK ads only, and is pulled by `tiktok_ccl_pull.py`):

1. Ask the member to open `https://ads.tiktok.com/business/creativecenter/inspiration/topads/pc/en` in their own browser, logged in if they want details, and filter by their industry and region.
2. With the member's browser tools available (Claude in Chrome or the built-in browser), read the visible cards: advertiser, the ad's text, duration, the metrics TikTok shows (these are TikTok's curated figures, label them so), and the video URL if exposed.
3. Save what was read as stub records with `manual_pull.py --urls <video or detail urls> --advertiser "<name>"`, and read the videos' first frames by eye for the rubric. Mark `inspection_coverage` honestly.
4. Never download from a logged-in session into the workspace; keep references and notes only.

Record in `searches.csv` that TikTok coverage was assisted and partial.
