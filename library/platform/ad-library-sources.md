# Ad library sources

This file describes the five public ad transparency sources Ad Lab draws on, what each shows and hides, and how to access it politely. Notes reflect what was verifiable in October 2026; items confirmed only from vendor sources are marked "vendor claim."

## Manners for automated access

These apply to every source below. Read only: no login, no likes, follows, saves, or messages. A normal desktop browser profile, one request at a time, pauses of a few seconds between searches. Stop at any captcha, login wall, or block. Platform terms may restrict automated access even to public pages; the plugin's legal and ethics note says so, and the member runs the research on their own machine for their own use. Apify actors and manual browsing are the alternatives. Media CDN links expire, so download creatives in the same session.

## Meta Ad Library

**What it shows.** Active ads across Meta surfaces, searchable by keyword or advertiser Page: creative, primary text, start date, platforms, Page, and link. Ads that also delivered in the EU show a transparency block with reach and a breakdown by age, gender, and location. This is the only free demographic signal available; the pull captures it when present (verify the layout on a live ad).

**What it does not show.** Spend, results, targeting outside the EU block, inactive commercial ads, or reliable per-Page totals headless (some Page views stopped at 30 ads while Meta reported hundreds; treat counts as samples).

**Login.** None needed in the October 21 run. No captcha or block appeared.

**Coverage.** Global for active commercial ads. Political and social-issue ads keep a seven-year archive; EU ads are archived one year after the last impression.

**API status (October 2026).** The official Ad Library API covers social-issue, electoral, and political ads plus ads delivered in the EU. It is not a route to general commercial ads elsewhere. A limit of roughly 200 calls per hour per token is a vendor claim. Meta's developer pages could not be fetched, so field lists and verification steps are unconfirmed.

**Retention caveat.** Commercial ads disappear when they stop running. Past campaigns are gone unless someone captured them.

**Best use in Ad Lab.** The primary source for the market map: keyword searches on the category's language, Page searches for named competitors, and the platform-Page check in the Skool co-branded file. Keyword results are noisy; "skool" also matches Vans Old Skool.

## Google Ads Transparency Center

**What it shows.** Ads by verified advertiser across Search, Display, and YouTube, with regions and date ranges, including the YouTube creative for video ads.

**What it does not show.** Spend, performance, or keyword search across all advertisers; you search by advertiser name.

**Login.** None for browsing.

**Coverage.** Global, with extra access for EEA ads under the DSA. Political ads are a public BigQuery dataset.

**API status.** No general public API. SerpApi, SearchAPI, and an Apify actor sell scraped endpoints (vendor routes).

**Retention caveat.** Vendor figures conflict (30 days to 13 months). Rely on none of them; capture what you need when you see it.

**Best use in Ad Lab.** The best free source for competitor video ads because it links the YouTube creative. Run it after the Meta pull.

## LinkedIn Ad Library

**What it shows.** Ads run on LinkedIn, searchable by company and keyword, with creative and dates.

**What it does not show.** Spend, results, or targeting detail.

**Login.** Public browse without login.

**Coverage.** Global.

**API status.** No public API. LinkedIn's Marketing API covers only the member's own account.

**Retention caveat.** Not confirmed from LinkedIn's own pages; treat the window as unknown.

**Best use in Ad Lab.** B2B members only. Skip it for consumer and creator categories.

## TikTok Commercial Content Library

**What it shows.** Ads shown in the EEA, Switzerland, and the UK, with advertiser, dates, and a targeting summary. Vendor sources say 33 markets; one adds Turkey.

**What it does not show.** Ads shown only outside those regions. In the October 2026 probe, "Skool" returned only Vans ads.

**Login.** None; confirmed by the probe.

**Coverage.** EEA, Switzerland, UK only.

**API status.** A research-credentialed Commercial Content API exists. A broader 2026 Research API expansion was reported but not confirmed.

**Retention caveat.** Not confirmed; assume ads leave when they stop delivering in the covered regions.

**Best use in Ad Lab.** EU coverage for members with European competitors. Expect thin results for US-only creators and say so rather than inferring from absence.

## TikTok Creative Center (Top Ads)

**What it shows.** A curated gallery of advertiser-authorized high performers, filterable by region, industry, and objective.

**What it does not show.** An archive. It is a showcase, so absence means nothing. Brand-specific search and ad details need login.

**Login.** The category dashboard loads without login; search and details require an account.

**Coverage.** Global, by region filter.

**API status.** No public API. Apify actors exist (vendor route).

**Retention caveat.** A roughly six-month window is a vendor claim.

**Best use in Ad Lab.** Format and pacing reference, not competitor evidence. Because of the login need, TikTok is an assisted flow in the member's own browser.

## Using them together

Meta first for the roster and the bank. Google second for video. LinkedIn only for B2B. TikTok for EU coverage and craft reference. Every ad carries its source, ID, and what was inspected, and the market map lists which sources and Pages were checked.

## Related

- [skool-cobranded-ads.md](skool-cobranded-ads.md)
- [tiktok-youtube-differences.md](tiktok-youtube-differences.md)
- [../rubrics/market-map-template.md](../rubrics/market-map-template.md)
- [../rubrics/per-ad-rubric.md](../rubrics/per-ad-rubric.md)
- [../rubrics/evidence-integrity.md](../rubrics/evidence-integrity.md)

## Sources

- Ad Lab research notes, section 1 (ad library data access), October 22, 2026, including its list of official and vendor pages.
- Notes from an earlier Ad Library research run, October 21, 2026.
- Meta Transparency Center ad library tools: https://transparency.meta.com/researchtools/ad-library-tools/
- Meta Ad Library: https://www.facebook.com/ads/library/
- Google Ads Transparency Center: https://adstransparency.google.com/
- LinkedIn Ad Library: https://www.linkedin.com/ad-library/
- TikTok Commercial Content Library: https://library.tiktok.com/
- TikTok Creative Center: named without a link; use the Top Ads section from TikTok for Business.

## Tool notes from the October 2026 live tests

Observed while building Ad Lab's pull tools on 2026-10-22 and 23; sources change, so re-check with `/adlab:doctor`.

- **Google Ads Transparency Center.** The site's internal RPC payloads are readable: search suggestions give the advertiser id and ad count; the creative list gives format (text, image, video), first and last shown dates, variant counts and region text; video ads expose a YouTube id, which the tool records as the video link and does not download. "Text" ads are served as rendered images, so their copy needs reading from the card; some responsive image ads yield only a card screenshot; the destination URL is rarely exposed. Each creative is one page load, so ten creatives take about four minutes; keep `--max-per-advertiser` low (10 is a sensible default) for this source.
- **LinkedIn Ad Library.** Browsable without login. Cards and detail pages give the body, headline, CTA, image or video with poster, the ad type label, the company and "paid for by". Run dates and impressions appear only for ads delivered in the EU; the destination link is not exposed. Name matching is loose (a company name also returns its regional pages); the tool filters by name and `--loose` turns that off.
- **TikTok Commercial Content Library.** Covers ads shown in the EEA, Switzerland and the UK only. The search API behind the page returns advertiser, ad id, first and last shown, the cover image, title and audience fields; the detail endpoint adds the advertiser's registry location, username, sponsor and targeting. The site slows and then throttles repeated automated loads (an HTTP 421 "system busy" after a few dozen requests); the tool notes empty details in `searches.csv`. Keep pulls small and rerun later; existing records are skipped.
- **Meta Ad Library.** No login wall, captcha or block in any run. The EU transparency block (reach and audience breakdown for ads delivered in the EU) is captured when the detail page carries it; in the October 2026 runs none of the probed ads did, so treat that field as best effort until a run shows one. Keyword searches are noisy (a church matched "club"); the tool labels each ad `advertiser-page`, `cobrand` or `keyword-neighbor` and caps neighbors per search. A creator's own Page can show zero while the platform's Page runs their ads; the two-term co-branded search (`<name> <platform>`) found them where the exact phrase did not.
