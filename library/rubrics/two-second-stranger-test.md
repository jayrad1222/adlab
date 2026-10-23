# The two-second stranger test

## The test

Show the ad to someone who has never heard of the member's business for two seconds, then take it away and ask two questions:

1. Who is this for?
2. What is it about?

The ad passes if the stranger's answers match the persona and the one idea in the concept brief, in the stranger's own words. It fails if the stranger names a different audience, cannot name an audience, cannot say what it is about, or describes the format instead of the content ("some guy talking", "a text post").

Two seconds is the budget because feed placements are judged in that window and the platform's own hook metrics (3-second plays) start counting about there. Nothing in the test asks whether the stranger likes the ad, would buy, or finds it clever. Liking is not the question; legibility is.

Related: [`critic-checklist.md`](critic-checklist.md), [`editorial-score.md`](editorial-score.md), [`../copy/hook-taxonomy.md`](../copy/hook-taxonomy.md), [`../copy/hormozi-callout-value-cta.md`](../copy/hormozi-callout-value-cta.md), [`../platform/specs-and-safe-zones.md`](../platform/specs-and-safe-zones.md), [`../psychology/cialdini-pre-suasion.md`](../psychology/cialdini-pre-suasion.md).

## Who the stranger is

The critic agent plays the stranger by default, deliberately reading without the brief open. When the member can, a real person who does not know the business is better. The stranger must not be the member, the copywriter or anyone who has read the concept.

Record the stranger's answers verbatim. Paraphrasing them toward the brief defeats the test.

## How to run it on a static

1. Render the static at phone size (1080 wide, viewed on a phone or scaled to about 400 pixels wide on a screen). Do not run the test on the full-size design file.
2. Show it for two seconds. A timer, not a guess.
3. Hide it. Ask the two questions. Write the answers down.
4. Then check three things the stranger could not see for long:
   - Was the largest text the hook, and was it legible at that size (the `textstats` check in `render.py` is the floor, not the ceiling)?
   - Did the image or the first visual element show the persona's object, moment or situation, or something generic?
   - Did the hook or the visual contain a callout, explicit or implied ("if you run a...", a trade's tools in frame, a job's screen)? Most statics that fail do so because nothing in frame says who it is for.

## How to run it on a video's first three seconds

1. Play only the first three seconds, with sound on and with sound off (feed autoplay is often muted). Run both; a video that passes only with sound fails for muted placements unless the on-screen text carries the hook.
2. Hide it. Ask the two questions. Write the answers down for each condition.
3. Then check:
   - Was there a spoken or on-screen line inside the first second, or did the video open on a logo, a title card, a slow establishing shot or a greeting ("hey guys")? Any of those is a fail by itself.
   - Did the first frame show the persona's object, moment or face, or a generic setting?
   - Is the hook visible in the 9:16 safe zone, clear of the platform's UI overlays?
   - Does the hook on screen match the hook in the script and the bank entry's `hook` field? A mismatch is a continuity error to report to the author.

## Pass or fail criteria

| Result | Criterion |
|---|---|
| Pass | The stranger names the persona's situation (or a recognizable neighbour of it) and the one idea, in both sound conditions for video. |
| Partial | The stranger gets one of the two, or gets both only with sound on. Record as a fail with the reason; the item goes back for the first visual or the on-screen text. |
| Fail | The stranger names the wrong audience, no audience, no topic, or describes the format. |

A fail caps the editorial band at "revise" until fixed. The test is not re-run with the same stranger after they have seen the ad once; use a different stranger or a different first-frame.

## What the test does not do

It does not predict hook rate, hold rate or conversion. It does not reward cleverness. It does not care about brand polish. It catches the most common and cheapest failure in small-business ads: an ad that is clear to the owner and opaque to everyone else.
