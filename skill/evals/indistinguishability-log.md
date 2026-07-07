# Indistinguishability log

The audit trail for the pairwise voice test (`indistinguishability.md`). The protocol's step 5
appends here after every run, so the held-out voice gate has a memory: what was tested, how the
blind judge did, and what changed in response. Without this log the test is run-and-forget; with
it, recurring judge signals become the repair list that drives engine and corpus changes.

## How to use it

After each run (step 5 of `indistinguishability.md`), add a row to the table for the channel,
then a short note under it for the recurring signals and any change made. Keep the newest entries
at the top.

- **judge accuracy** is the judge's error rate framed as how often it picked the real text.
  50% (chance) is the target: indistinguishable. Higher means the imitation is detectable.
- **top signals** are the judge's stated reasons, recorded whether or not it guessed right; these
  are the repair list.
- **change made** links the result to the action: a rule edit, a sweep-ordering fix, more corpus,
  or "none (already at chance)".

## Results

| date | channel | trials | judge accuracy | top recurring signals | change made |
| ---- | ------- | ------ | -------------- | --------------------- | ----------- |
| _(none yet)_ | | | | | |

## Notes

<!-- One short paragraph per noteworthy run: what the signals were, and what you did about them.
     Mechanical signals (punctuation, slop, structure) mean the sweep is leaking; voice-level
     signals ("the imitation is too even", "the real one has a stranger opinion") mean the repair
     is more corpus or building from the user's raw words, not more rules. -->
