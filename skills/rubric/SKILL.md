---
name: rubric
description: Internal. The per-ad rubric, allowed values and the inspection-coverage honesty rule. Preloaded into the ad-analyst and copywriter agents; not a command.
user-invocable: false
---
# Per-ad rubric (internal)

Full reference: `${CLAUDE_PLUGIN_ROOT}/library/rubrics/per-ad-rubric.md`. Hook types: `${CLAUDE_PLUGIN_ROOT}/library/copy/hook-taxonomy.md`. Angle families: `${CLAUDE_PLUGIN_ROOT}/library/copy/angle-families.md`. Formats: `${CLAUDE_PLUGIN_ROOT}/library/copy/format-taxonomy.md`.

One row per ad. Write what you observed; write `unknown` when you did not observe it. Never infer a field and present it as observed.

## CSV header (verbatim, this order)

```
ad_id,advertiser,page_or_account,platforms,first_seen,days_active_at_capture,status,variant_count,variant_type,format,duration_s,hook_text,hook_type,angle_family,awareness_stage,sophistication_move,persona_inferred,persona_evidence,emotional_lever,biases_used,proof_type,offer_elements,price_framing,cta,landing_type,landing_continuity,production_style,visual_hook,on_screen_text_density,distinctive_assets,sutherland_lens,works,weak,verdict,adaptation_idea,inspection_coverage
```

## Allowed values

- `variant_type`: copy-test | creative-test | placement | none
- `format`: a slug from the format taxonomy (static-text-only-ugly, static-us-vs-them, static-three-reasons, static-review-card, static-founder-note, static-meme-tweet, static-whats-inside, static-faq, static-comparison, static-skeptic-quote, static-dm-screenshot, static-before-after, static-offer-card, static-problem-card, video-founder-to-camera, video-demo, video-screen-pip, video-podcast-clip, video-street-interview, video-day-in-life, video-mini-doc, video-whiteboard, video-listicle, video-skit, video-pov, video-reaction, video-testimonial, video-how-its-made, video-mistakes, video-objection, video-myth, video-vs-alone, carousel-tutorial, carousel-personas, carousel-timeline, carousel-reveal, carousel-process) or `unknown`
- `hook_type`: one of the 26 in the hook taxonomy (callout, question, bold-claim, specific-number, curiosity-gap, pattern-interrupt, contrarian, warning, confession, story, pov, three-reasons, today-years-old, nobody-talks-about, comparison, news, social-proof, authority, demonstration, problem-naming, identification, offer-led, wish-i-knew, real-reason, unpopular-opinion, day-1-vs-30)
- `angle_family`: problem | desire | mechanism | identity | proof | offer | contrarian | news | comparison | story | education | cost-of-inaction
- `awareness_stage`: unaware | problem | solution | product | most
- `sophistication_move`: claim | bigger-claim | mechanism | better-mechanism | identification
- `emotional_lever`: fear | hope | pride | belonging | relief | curiosity | status | guilt | anger | greed | humor | trust
- `proof_type`: demo | testimonial | data | authority | social-proof | press | ugc | none
- `landing_continuity`: strong | weak | broken | unknown
- `production_style`: polished | native | ugly | ugc | founder | screen-rec
- `on_screen_text_density`: none | low | medium | high
- `verdict`: adapt | avoid | monitor
- `inspection_coverage`: copy-only | still-reviewed | video-watched

## Inspection coverage rule

`video-watched` only when you read the transcript AND the frames (or watched the video). `still-reviewed` when you looked at the card or creative image. `copy-only` when you only had text. A transcript alone is not `video-watched`; say `still-reviewed` plus a note in `weak` if the frames were missing.

## The Sutherland column

`sutherland_lens` answers: what perception problem is this ad solving (trust, status, category, context, price signal, social proof, ritual, legibility), and is it the right one for the persona it targets?
