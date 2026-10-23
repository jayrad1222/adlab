# Skool co-branded ads

This file records a finding from the October 21, 2026 Meta Ad Library pull: Skool's own Page runs ads on behalf of individual communities, so a creator's ads can be invisible on the creator's Page. It changes how every competitor roster in the creator and community category has to be built.

## What was found

During the October 21 run (headless browser, no login, 1,927 unique active ads collected), the Skool Page (the official one, around 155k likes at the time) was running ads titled in the form "<Creator> with Skool". Each one linked to the community's about page at `skool.com/<slug>/about`. 328 of these co-branded ads were collected.

Several named communities had every one of their collected ads under Skool's Page and none under their own. In the sample: Meta Ads Mastery (62), Wholesailors (60), Matt Ryder (43), Ben Heath (24), Maker School (14), Origins (10), Evelyn (8), AI Operator Academy (5), Viral You (4), Claude Code Club (3), Rank Expand Academy (3). A further 46 linked to `/facebook`.

Two cautions. Meta reported about 3,260 active ads for the Skool Page and the run captured a few hundred, because lazy loading did not always fire headless; the counts are a sample. And the run was one day; the mix changes.

## What it means for competitor research

- **A zero on a creator's Page is not evidence of no ads.** The ad-analyst must not write "this competitor is not advertising" after checking only the creator's Page. The market map should mark the creator's own Page as checked and the platform Page as checked separately, with the counts from each.
- **Attribution has to be by destination, not by advertiser.** The pull records `skool_group` (the community slug from the link) and `points_to_skool`, and the brand attribution table counts active ads per named group across both the group's own Pages and the ads Skool runs for them. Use that table, not the Page name, when building a roster.
- **Creative style differs.** The co-branded ads use a shared template with the creator's name and face inside Skool's format. When decoding them, separate what the creator chose (the hook, the face, the promise) from what the template imposed (the layout, the "with Skool" line, the about-page destination). Tag the production style accordingly.
- **Variants from one advertiser are not independent evidence.** Dozens of co-branded ads under one Page are one advertiser's test, not dozens of businesses agreeing on a hook. The evidence rules already say this; it matters more here.

## The exact searches to run

Run these in the Meta Ad Library web UI (or the pull script) for any creator or community competitor:

1. **The creator's own Page.** Search the creator or community name, read the Page suggestions in the typeahead and the filter sidebar, open up to three matching Pages, and record active ads per Page. Beware of lookalike names; the October run hit unrelated Pages with the same words.
2. **The Skool Page, filtered by the creator.** Open the Skool Page's ads and search within them for the creator's name or the community slug. Record the "<Creator> with Skool" ads and their about-page links.
3. **A keyword search on the slug.** Search `skool.com/<slug>` and the slug alone. This catches ads from affiliates, partners, or alternate Pages that link to the same community.
4. **A keyword search on the category language.** The words the community uses to describe itself ("AI automation," "Meta ads coaching"). Advertisers who use your words compete for your attention, whatever their Page is called.
5. **Pages that run under another name.** Several people in the October run advertised under a different Page name (a business name, a program name, a partner's name). Search the person, the program, and the business separately and note the mapping in the roster.

Filter noisy results on the pull's `skool_signal` and `points_to_skool` fields; "skool" alone matches Vans Old Skool.

## The generalization: platforms that advertise for their sellers

Skool is not unusual. Many platforms and marketplaces run paid ads that feature or link to an individual seller, creator, listing, or storefront, under the platform's own ad account. When that happens, the seller's own Page or account shows nothing, and a roster built from seller accounts alone is wrong.

Treat this as a pattern to check for every category, not as a claim about any named platform:

- Does the competitor sell through a platform or marketplace (a course host, a community host, a booking site, a delivery app, a marketplace, an app store, a listing site)?
- Does that platform have its own advertiser Page or account in the ad library?
- Does a search for the competitor's name, product, or URL inside that platform's ads return results?
- Do the ads link to a page on the platform's domain that identifies the competitor?

If yes to the first two, run the last two before concluding anything about the competitor's ad activity. Record which platform Pages were checked in the market map so the next run can repeat them.

## What this does not tell you

Who paid for the co-branded ads, how they were targeted, or whether they worked. Longevity is not profitability.

## Related

- [ad-library-sources.md](ad-library-sources.md)
- [../rubrics/market-map-template.md](../rubrics/market-map-template.md)
- [../rubrics/per-ad-rubric.md](../rubrics/per-ad-rubric.md)
- [../rubrics/evidence-integrity.md](../rubrics/evidence-integrity.md)
- [../strategy/sharp-mental-physical-availability.md](../strategy/sharp-mental-physical-availability.md)

## Sources

- Notes from an earlier Ad Library research run, October 21, 2026 (the co-branded finding, counts, and the Page-name mappings).
- Ad Lab research notes, section 1 (Meta Ad Library web UI pull and the co-branded finding), October 22, 2026.
- Meta Ad Library: https://www.facebook.com/ads/library/
