# Decision rules

Purpose: the explicit if-then rules the readout skill applies to an Ads Manager export, with every threshold left as a member-set variable. The skill names which rule fired and prints the numbers that fired it. Nothing here supplies a threshold; the seed gives none and this library invents none.

## Member-set variables

These live in `business/finance.md` beside the inputs in [inputs.md](inputs.md). The member sets them before the first readout and revises them after each round.

```yaml
impression_floor: 2000        # impressions before any signal is read
hook_rate_floor: 0.00         # share of impressions that became 3-second plays
hold_rate_floor: 0.00         # share of 3-second plays that became ThruPlays
ctr_floor: 0.00               # link CTR
min_conversions: 30           # conversions before CPA is judged; same as conversions_to_judge
frequency_ceiling: 0.0        # frequency above which scaling stops
max_days: 7                   # days a concept may run without reaching impression_floor
```

`target_cpa` and `breakeven_cpa` come from [formulas.md](formulas.md). For trial memberships substitute the per-trial-start versions.

## Reading order

Read in this order and stop at the first rule that fires: hook rate, hold rate, CTR, CPA. For statics, skip hook and hold. Each signal depends on the one before it, so a failure upstream explains everything downstream and the downstream numbers are not evidence of anything.

## Rule 0: not enough data

If `impressions < impression_floor`, then no judgment. Report "insufficient impressions" and the days remaining to `max_days`.

If `days_running >= max_days` and `impressions < impression_floor`, then the platform is not serving the ad. Report "under-delivery" and check the bid, budget, audience size and policy status before judging the creative.

## Rule 1: kill

If `impressions >= impression_floor` and `hook_rate < hook_rate_floor`, then kill the concept. The angle selected nobody. Do not iterate the hook on this concept; a fair impression floor was met and the premise did not stop people. Log the concept, the hook family and the result to the bank as a negative.

For statics: if `impressions >= impression_floor` and `ctr < ctr_floor` and no other rule applies, then kill.

## Rule 2: iterate hook

If `hook_rate < hook_rate_floor` and `hold_rate >= hold_rate_floor` and the concept has run fewer than the member's iteration count, then iterate the hook. The body held the few people who got in; the first seconds are the problem. Produce new openers from a different hook family against the same body and offer. Do not touch the body or the landing page.

Note the order of operations with Rule 1: Rule 1 fires when hook fails and there is no hold evidence. Rule 2 fires when hook fails but hold is good, which means the concept has a body worth saving. The skill reports both numbers so the member can see why one fired and not the other.

## Rule 3: iterate body

If `hook_rate >= hook_rate_floor` and `hold_rate < hold_rate_floor`, then iterate the body. The opener worked and the promise of the first seconds was not kept. Keep the hook, rework the middle, re-cut.

## Rule 4: iterate offer or landing

If `hook_rate >= hook_rate_floor` and `hold_rate >= hold_rate_floor` and `ctr >= ctr_floor` and `conversions >= min_conversions` and `cpa > target_cpa`, then iterate the offer or the landing page. The ad did its job: people stopped, stayed and clicked. The page or the offer did not close them. Check landing conversion rate against the member's other ads to decide which.

If in the same case `cpa > breakeven_cpa`, say so plainly: the concept is losing money per conversion, not only missing target.

## Rule 5: scale

If `conversions >= min_conversions` and `cpa <= target_cpa` and `frequency <= frequency_ceiling`, then scale. Raise budget in steps and re-read after each step; the rule re-applies on the new volume.

If `cpa <= target_cpa` and `frequency > frequency_ceiling`, then do not scale. The creative is wearing out. Produce iterations and broaden the audience before adding spend.

## Rule 6: minimum volume

If `conversions < min_conversions`, then refuse to judge CPA. Report the upstream signals, the conversions so far, and the spend needed to reach `min_conversions` at the current CPA. The skill says "CPA not yet judged" in those words. A concept with five conversions at a good CPA is not a winner, and a concept with five at a bad CPA is not a loser.

If `spend >= test_budget_per_concept` and `conversions < min_conversions`, then the concept is converting below the rate the budget assumed. Apply Rules 1 to 4 on the upstream signals to decide whether to continue, and say the budget assumption was wrong.

## Rule 7: between target and breakeven

If `conversions >= min_conversions` and `target_cpa < cpa <= breakeven_cpa`, then hold. The concept is not losing money and is not making the profit the member asked for. Keep it running at current spend while Rule 4 iterations are tested against it. Do not scale.

## What the skill prints

For every concept: the rule that fired, the signal values that fired it, the thresholds they were compared to, and the next action in one line. Where no rule fires because the data is between floors, print "no rule fired; continue to `max_days`."

## Related

- [Signals glossary](signals-glossary.md)
- [Formulas](formulas.md)
- [Inputs](inputs.md)
- [Denney concept versus iteration](../strategy/denney-concept-vs-iteration.md)
- [Hook taxonomy](../copy/hook-taxonomy.md)
- [Bank entry schema](../rubrics/bank-entry-schema.md)
- [Evidence integrity](../rubrics/evidence-integrity.md)
