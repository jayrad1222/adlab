# House style

## Who follows this

Every agent, in every file the plugin writes for a member and in every message to the member. It is preloaded into the `psychologist` and applies to all of them. The critic flags breaches as `REVISE` under its cliché item.

Related: [`../rubrics/evidence-integrity.md`](../rubrics/evidence-integrity.md), [`../rubrics/critic-checklist.md`](../rubrics/critic-checklist.md), [`../copy/harry-dry-three-tests.md`](../copy/harry-dry-three-tests.md), [`../copy/canon-hopkins-ogilvy-caples.md`](../copy/canon-hopkins-ogilvy-caples.md).

## Plain language

- Write the way a careful person explains something to a friend who runs a small business. No jargon unless the member used it first; if a term from the library is needed, say what it means the first time.
- Prefer the concrete noun to the abstract one: "the invoice pile", not "administrative burden".
- Prefer the verb to the nominalization: "we tested", not "testing was conducted".
- One idea per paragraph. Headings say what the section contains, not what it is called.

## Short sentences

- Aim under twenty words. Split a sentence at "and", "which" or a semicolon when it runs long.
- No sentence needs a parenthetical that is itself a sentence.
- Lists for anything with three or more items.

## Labels

Every statement about a customer, a competitor, a result or a market carries one of four labels, in the text or in the field:

- **observed**: seen in an ad, a page, a library record or a file, with an id or a path and a date
- **owner-provided**: said by the member in intake or in a note; it is their word, not a verified fact
- **inferred**: the agent's reading of an observed cue; the cue is named alongside
- **hypothetical**: a proposal to test; no evidence yet

Unlabeled claims are treated as inferred by the critic and sent back. "Unknown" is a valid value and is better than a guess.

## No hype words

Twenty to avoid, with what to write instead. The critic flags any of them in member-facing copy, concepts or bank entries unless they are inside a quoted competitor line with its id.

| Avoid | Write instead |
|---|---|
| game-changing | say what changes, for whom |
| revolutionary | the specific difference |
| unlock | the thing they can now do |
| transform | the before and the after, concretely |
| supercharge | the measured or observed effect, or cut |
| effortless | what the first step actually takes |
| seamless | what connects to what |
| powerful | what it does |
| world-class | the proof, or cut |
| cutting-edge | the mechanism |
| skyrocket | the number with its source, or cut |
| 10x | the number with its source, or cut |
| crush | cut |
| dominate | cut |
| secret | the thing itself |
| hack | the method |
| guaranteed | the actual guarantee terms, or cut |
| proven | the proof, with its source |
| ultimate | cut |
| leverage (as a verb) | use |

Also avoid: exclamation marks in body copy; "simply" and "just" before a step that is not simple; "imagine" as a lead unless the concept is identity-led and the critic has passed it; rhetorical questions with no answer in the body.

## No em-dashes

Do not use em-dashes or en-dashes anywhere: not in prose, not in tables, not in copy. Use a comma, a colon, a full stop or parentheses. Ranges are written with "to" ("0 to 2", "10 to 12"). This applies to every file the plugin writes.

## Numbers only with a source

- A number appears only with its source beside it or in the labeled field it comes from: an ad id, a catalog row, a library record with a date, `finance.md`, a named study with author and year.
- Counts from the decode state their denominator ("nine of twelve advertisers", not "most advertisers").
- Placeholder numbers in worked examples are labeled placeholder every time they appear.
- No percentages without a denominator. No "studies show" without the study.
- Precise beats round when the precision is real (Shotton); fabricated precision is worse than honest vagueness.

## Reporting format

Every skill and every agent reports in the same shape at the end of a unit of work:

```
Finished: <what now exists, with paths>
Doing now: <the step in progress, or "nothing" if the turn is complete>
Next: <the next step and what it needs>
```

One status line per unit of work during the work ("analyzed 15 of 40 ads; 3 copy-only"), not a running narrative. Do not announce a step and then stop; take the step.

## One-line asks

When the member must do something or decide something, ask in one line, with the default stated, and keep going on everything that does not depend on the answer. Examples:

- "Confirm the roster (8 advertisers, 3 rings) or edit `competitors/roster.md`; default is to pull all 8."
- "Which of p1 or p3 should the first batch favour? Default: p1, the larger heatmap gap."

Never stack asks. Never ask for something the plugin can find out itself. Never ask for screenshots or lookups the member would have to do by hand when a tool can do it.

## Member-facing copy in particular

- The ad copy the plugin writes for the member follows this style and the copy canon: specifics, a reason-why, the headline carrying the promise, long only when interesting.
- Competitor wording is never reused. Mechanisms transfer; sentences do not.
- Every line passes Harry Dry's three tests before it is saved.
- The persona's own words from the language bank are the preferred vocabulary.
