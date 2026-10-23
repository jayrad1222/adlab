# Persona schema (`personas/pN-<slug>.md`)

## Purpose

A persona in Ad Lab is a buying situation, not a demographic. It is written by the `persona-builder` agent from the brief, the interrogation answers, the `persona_inferred` and `persona_evidence` columns of `analysis/ads.csv`, review and comment text gathered by the `researcher`, and the member's five real customers. Three to seven personas per run. Every field below is required and appears in this order. A field with no evidence says `unknown` and what evidence would fill it.

Labels apply inside every field: **observed** (quoted from a source with a date), **owner-provided** (from intake), **inferred** (the builder's reading of an observed cue), **hypothetical** (no evidence yet).

Related: [`per-ad-rubric.md`](per-ad-rubric.md), [`../psychology/jtbd-four-forces.md`](../psychology/jtbd-four-forces.md), [`../psychology/barden-implicit-goals.md`](../psychology/barden-implicit-goals.md), [`../psychology/dont-design-for-average.md`](../psychology/dont-design-for-average.md), [`../psychology/status-and-identity.md`](../psychology/status-and-identity.md), [`../psychology/godin-people-like-us.md`](../psychology/godin-people-like-us.md), [`../strategy/levinger-three-realities-teep.md`](../strategy/levinger-three-realities-teep.md), [`../strategy/schwartz-awareness-stages.md`](../strategy/schwartz-awareness-stages.md), [`../sales/objection-taxonomy.md`](../sales/objection-taxonomy.md).

## The naming rule

The persona name is a situation, not a demographic. "Women 35 to 50" is not a persona; it is a targeting setting, and Meta treats targeting as a suggestion anyway. A situation names the moment and the pressure: what just happened, what they are doing instead, what it costs them. The test: could the member read the name aloud and picture one specific customer they have met?

Two example names in the required form:

- `p1-the-11pm-receipt-pile` (a solo trades owner doing their own books after the kids are asleep, after a year of saying they would hire someone)
- `p2-second-launch-after-a-quiet-first-one` (a creator whose first community launch got six members and who is deciding whether to try again or go back to one-to-one work)

Bad names, for contrast: `p1-small-business-owners`, `p2-millennial-creators`, `p3-budget-conscious-buyers`.

Copy everything below the line into `personas/pN-<slug>.md` and replace the italic instructions.

---

# pN: <name as a situation>

Version <n>, <YYYY-MM-DD>. Prior versions are kept below the line at the end of this file; a revision never deletes a prior version.

## Name as a situation

*One sentence expanding the file name: who is in this situation, what just happened, what they are doing about it today. No age, gender, income or location unless it is the situation itself (a move, a new baby, a new job). Label the sentence observed, owner-provided or inferred.*

## Job to be done

*What progress they are trying to make, in the form "when <situation>, I want to <action>, so I can <outcome>". One job per persona. If two jobs compete, that is two personas.*

## Trigger moment

*The specific event that moves them from living with the problem to looking for a solution. A date, a bill, a conversation, a failure, a comparison. Shotton's life-transition point applies: new job, new baby, new city, new year. Cite the source (a review, a comment, an interrogation answer, an ad that names it with its id).*

## Four forces

*All four must be filled; a persona with an empty force is not finished. See `../psychology/jtbd-four-forces.md`.*

- **Push** (what is wrong with the current situation, in their words):
- **Pull** (what the new solution promises them, in their words):
- **Anxiety** (what they fear about switching: looking foolish, wasting money, it not working for them, the first week):
- **Habit** (what keeps them in the current situation: the workaround, the sunk cost, the routine):

## Current workaround, including nothing

*What they do instead today. "Nothing" is a workaround and must be described: what not acting costs them, in their words, with a source. Include the spreadsheet, the cousin who helps, the cheaper tool, the manual process.*

## Awareness distribution

*How this persona is spread across Schwartz's five stages, as a rough split with the reasoning (for example "mostly problem-aware; some solution-aware who have tried a tool and dropped it"). Label as inferred unless survey or comment evidence exists. Do not give percentages without a source.*

## Sophistication

*How many promises like the member's they have already heard, and from whom. Which claims they are numb to. Which mechanism explanations they have already seen. Cite competitor ad ids from the market map.*

## Objections in their words

*Verbatim objections, each with its source and date, mapped to the objection taxonomy (price, trust, time, fit, priority, do-it-myself, tried-before, not-now). At least one quote per objection that applies. Paraphrases are labeled inferred.*

| Objection type | In their words | Source and date |
|---|---|---|
| | | |

## Emotional identity

*Who they believe they are and want to remain: the self-image the ad must not threaten (Levinger: the ad is a mirror). Written as "I am the kind of person who..." with the supporting quote.*

## Implicit goal (Barden)

*The one implicit goal that dominates: security, autonomy, excitement, adventure, discipline, enjoyment, or one of Barden's other goal territories. State the explicit goal (what the product does) alongside it. The visual world of the ad has to match the implicit goal. Label inferred.*

## Status game

*Who they want to look like after buying, and to whom (a partner, a peer group, a former boss, their customers, themselves). Which outcome would make them look foolish, and in front of whom. See `../psychology/status-and-identity.md`.*

## Language bank

*Verbatim phrases this persona uses, each with source and date. Minimum ten. These phrases are the raw material for hooks; the copywriter may quote them but may not present them as testimonials. Mark each as review, comment, forum, interrogation answer, competitor ad transcript (with id), or member's customer (with consent status).*

| Phrase (verbatim) | Source | Date |
|---|---|---|
| | | |

## Proof required

*What they would need to see before believing the promise: a demonstration, a named example, a number with a source, a person like them, a guarantee, a first week laid out. State which of these the member can supply today (from the asset catalog) and which are missing.*

## Preferred formats by T-E-E-P stage

*For each of trigger, exploration, evaluation and purchase: the formats most likely to reach this persona at that stage, with the reason. Cite competitor ads that already use the format for this persona (ids). See `../strategy/levinger-three-realities-teep.md`.*

| Stage | Formats | Reason | Competitor ids |
|---|---|---|---|
| Trigger | | | |
| Exploration | | | |
| Evaluation | | | |
| Purchase | | | |

## Poor-fit signals

*How to recognize someone who looks like this persona but is wrong for the member: the expectation the member cannot meet, the budget that will not work, the outcome they want that the member does not deliver. An ad can repel as well as attract; list what would repel the poor fit without insulting them.*

## Which competitor ads already talk to them

*Ad ids from `analysis/ads.csv` whose `persona_inferred` matches this situation, grouped by advertiser, with the angle family each uses. This is the crowd the member's ad has to stand apart from.*

## What nobody says to them yet

*Claims, mechanisms, proof or framings this persona would respond to that no captured ad uses. Each is hypothetical and says what evidence supports the gap (the heatmap cell, the language bank, the objection nobody answers). This section feeds the angles step directly.*

---

## Prior versions

*Appended, never overwritten. Each entry: version number, date, what changed and why, with the evidence that prompted the change.*
