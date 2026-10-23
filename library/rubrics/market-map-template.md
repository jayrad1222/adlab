# Market map template (`analysis/market-map.md`)

## Purpose

The market map is the one document a member reads to understand the category they are entering. It is built from `analysis/ads.csv`, the per-advertiser files (`analysis/competitor-<x>.md`) and the roster. Every count in it must be reproducible from `ads.csv`; every claim about an ad must carry an ad id. Sections appear in the order below and none may be omitted; a section with nothing to report says so and why.

Related: [`per-ad-rubric.md`](per-ad-rubric.md), [`evidence-integrity.md`](evidence-integrity.md), [`../prompts/opposite-pass.md`](../prompts/opposite-pass.md), [`../strategy/schwartz-market-sophistication.md`](../strategy/schwartz-market-sophistication.md), [`../strategy/dunford-positioning.md`](../strategy/dunford-positioning.md), [`../strategy/andromeda-implications.md`](../strategy/andromeda-implications.md).

Copy everything below the line into `analysis/market-map.md` and replace the italic instructions.

---

# Market map: <category or member name>

Prepared <YYYY-MM-DD> from <N> ads across <M> advertisers. Capture dates: <earliest> to <latest>. Sources: <Meta Ad Library | Google Transparency Center | LinkedIn Ad Library | TikTok CCL | manual>.

Labels used in this document: **observed** (seen in an ad, a page or a library record, with an id), **owner-provided** (from the member's intake), **inferred** (the analyst's reading of an observed cue), **hypothetical** (a proposal to test; no evidence yet).

## 1. Roster and sample sizes

*One row per advertiser: ring (1 direct, 2 adjacent, 3 attention competitor), ads reported by the library, ads captured, ads inspected at each `inspection_coverage` level, capture date, active or all filter used. State the caps that were applied. The difference between "reported" and "captured" is the first evidence limit and must be visible here, not buried in section 12.*

| Advertiser | Ring | Reported by library | Captured | copy-only | still-reviewed | video-watched | Capture date | Filter |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |

## 2. Sophistication stage and required move

*State the Schwartz stage the category is at (1 to 5), the evidence for it (counts of `sophistication_move` values from `ads.csv`, with ids for the clearest examples), and the move the stage requires. If advertisers are split across stages, say so; a category where the leaders are at stage 4 and the newcomers at stage 2 is a different map from a uniform one. Label the stage call as inferred.*

## 3. Table-stakes claims

*The claims that most advertisers make. For each: the claim in a neutral paraphrase, the count of advertisers making it and the count of ads, the ad ids, and whether the member can also make it truthfully (owner-provided). A table-stakes claim is one the member must match or consciously decline; it is not a differentiator.*

| Claim | Advertisers (n of M) | Ads (n of N) | Ad ids | Member can say it (yes / no / unknown) |
|---|---|---|---|---|
| | | | | |

## 4. Uncontested claims about the member's offer

*Claims the member can truthfully make (from `business/offer.md` and the asset catalog) that no captured ad makes. For each: the claim, the evidence the member holds for it, and the search that was run to confirm nobody says it (which advertisers, how many ads). "Nobody says it" is a statement about this sample, not the market; say that.*

## 5. Persona coverage heatmap

*Rows are the personas inferred from `persona_inferred` (cluster similar situations; name each as a situation). Columns are awareness stages. Cells hold the count of ads and the ids of up to three examples. Empty cells are the white space; name them explicitly below the table. Cells are inferred, because `persona_inferred` is inferred.*

| Persona (situation) | unaware | problem | solution | product | most |
|---|---|---|---|---|---|
| | | | | | |

White space observed in this sample: *list the empty or thin cells.*

## 6. Proof arms race

*Count `proof_type` across the sample. Which proof types are everywhere, which are rare, which are absent. Note the unsupported numbers (a number with no source is a claim, not proof) with ids. Note any proof that looks fabricated or policy-risky with ids, labeled as a concern, not an accusation. State what proof the member actually holds (from the asset catalog) and where it would be rare in this market.*

## 7. Price and positioning map

*Which advertisers show a price in the ad, which show it on the landing page, which hide it. Price framing observed (charm, round, per-day, anchored, tiers, free). Positioning as the category each advertiser chooses to be judged in (Dunford): list the categories claimed and the reference prices they imply. Label the positioning read as inferred. Do not estimate revenue or spend from anything in this section.*

| Advertiser | Price shown in ad | Price on landing | Framing | Category claimed | Ids |
|---|---|---|---|---|---|
| | | | | | |

## 8. Format mix and gaps

*Count `format` across the sample and by advertiser. Which of the format taxonomy's groups (statics, video, carousel) and which specific formats are used, which are absent. Say whether at least two "ugly" or native formats appear. A gap here is a candidate for the bank, not a guarantee it will work.*

## 9. Longevity leaderboard

*The ads with the highest `days_active_at_capture`, with advertiser, format, hook type, angle family and id. Keep it to the top ten or fewer.*

The following caveats are printed here in full, every time, and may not be shortened:

- **Longevity is not profitability.** An ad that has run for a long time may be running because it works, because nobody turned it off, because it is a brand-awareness placement with no conversion goal, or because the advertiser has budget to waste. The leaderboard shows persistence, not results.
- **This is an active-only sample unless stated otherwise.** Ads that were launched and killed are not in it, so the leaderboard cannot estimate what fraction of ads survive, how long a typical ad lasts, or how this advertiser's hit rate compares with another's.
- **Variants from one advertiser are not independent evidence.** Five long-running variants of one concept from one advertiser count as one observation about that concept, not five.
- **`days_active_at_capture` depends on the library's `first_seen`**, which can reflect the ad set's start rather than the creative's, and which differs by platform.
- **Spend and reach are unknown** unless the library's transparency block reported them, in which case they are quoted with the id and the date.

| Rank | Ad id | Advertiser | Days active | Format | Hook type | Angle family | Coverage |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

## 10. Conventions worth inverting (the opposite pass)

*List the category's top five conventions found above (a claim, a format, a proof type, a price signal, a tone). For each, the inverse and whether the inverse is also a good idea, for which persona, under what mechanism, with the cheapest test. Use the table from `../prompts/opposite-pass.md`. Reject inversions that are only contrarian. Everything in this section is hypothetical until tested.*

## 11. Ten testable hypotheses

*Ten statements of the form "If we <do X> for <persona> at <awareness stage>, then <upstream signal> will <direction>, because <mechanism, with the framework file>." Each cites the ad ids that prompted it and names the result that would prove it wrong. Hypotheses are not recommendations; the interrogation and the angles step will rank them.*

1.
2.
3.
4.
5.
6.
7.
8.
9.
10.

## 12. Evidence limits

*Written in full, not summarized. Include at minimum: which advertisers were capped and at what cap; how many ads were `copy-only`, `still-reviewed` and `video-watched`; which videos were not watched and why; which landing pages were not fetched; whether the sample is active-only; which counts in this document are from samples rather than the library's full listing; which platforms were not searched; the date after which this map is stale; and anything the analyst was unsure about. A reader should be able to tell from this section alone how much weight each earlier section can bear.*
