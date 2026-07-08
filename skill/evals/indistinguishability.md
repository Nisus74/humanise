# Pairwise indistinguishability test

The assertion battery measures rule compliance. This test measures the actual goal: whether skill output is distinguishable from the user's real writing. Run it after every corpus expansion and after any significant rule change.

## The voiceprint tripwire (when to spend the judge)

This test needs a model and human attention, so it's costly to run on every draft. The voiceprint distance (`humanise voiceprint <file>`, or the `voiceprint_distance` block when a baseline is passed to `writing_checks.py`) is the cheap, automatable early-warning that says *when* a draft is worth the judge. It scores a draft's distance from your corpus distribution as a mean per-feature z-score, advisory only. A draft sitting near your baseline is probably fine; a draft that drifts far is the one to put in front of the judge. The voiceprint is a tripwire, not a verdict: it flags candidates, the blind judge below decides. Never tune a draft to lower its distance; reporting a distance is not the same as naming a target, and tuning to it is the detector-gaming the loop forbids.

## Protocol

1. **Pick the channel.** Use a channel with at least two real `profile/sample-<channel>-*.md` samples. Hold one sample out; it must not appear in the drafting context.
2. **Generate the counterpart.** Give the skill a brief reconstructed from the held-out sample's frontmatter (`context` field): same topic territory, same audience, same approximate length. The skill must not see the held-out sample.
3. **Judge blind.** Present both texts, unlabelled and order-randomised, to a fresh judge (the `../agents/indistinguishability-judge.md` subagent, no access to this conversation or the corpus) with this prompt:

   > One of these two texts was written by a specific person; the other is an imitation. Identify which is the real one and explain the three strongest signals that decided it.

4. **Score.** Run at least 5 trials per channel (re-randomise order each time; vary the held-out sample if the corpus allows). The skill's score is the judge's error rate: 50% (chance) means indistinguishable, which is the target. Record the judge's stated signals regardless of whether it guessed right; the signals are the repair list.
5. **Log.** Append results to `evals/indistinguishability-log.md`: date, channel, trials, judge accuracy, top recurring signals, and what was changed in response.

## Automated path

`/humanise improve` runs this protocol end to end, with the deterministic parts scripted in `assertions/pairwise_trial.py`: `--prepare` selects the held-out sample per trial (seeded, replayable) and writes a frontmatter-only brief plus an allowed-context manifest; the `eval-generator` subagent writes the counterpart from that brief; `--pair` order-randomises each trial's pair with the blinding key kept out of the trial directories; one fresh judge subagent per trial returns a machine-readable verdict; `--score` unblinds, computes accuracy, feeds the judge's signals into the learning ledger, and prints the log row. The protocol above stays the authority; the script just makes it repeatable. Full trial artefacts land under `profile/learning/runs/` (never committed); only the aggregate row lands here in the log.

## Reading the results

- **Judge accuracy near 50%:** the voice transfers. Move to the next channel.
- **Judge accuracy high, signals are mechanical** (punctuation, slop, structure): the sweep is leaking; fix the rules or the sweep ordering.
- **Judge accuracy high, signals are voice-level** ("the real one has a stranger opinion", "the imitation is too even"): rules can't fix this. The repair is more corpus samples for that channel, or building drafts from the user's raw words (SKILL.md Step 1).
- **Judge picks the imitation as real:** flag it, but don't celebrate; it usually means the real sample was heavily edited or atypical. Check its `dogfood_status`.

## Long-form channel

Long-form is where the skill broke worst (the Intake pricing memo leaked every structural tell despite the rules banning them), so it needs its own test once the `long-form/` corpus has a real sample to hold out. The protocol is the same with three changes.

1. **Hold out a real long-form piece**, not a short one: a board memo, a PRD intro, a strategy doc. The reconstructed brief gives the skill the same document type, audience, and section outline, but not the text. The skill drafts in document mode (SKILL.md), section by section.

2. **Judge at two levels.** Run the blind pairwise judge as normal, and separately run the `structural_density` dashboard from `writing_checks.py` on both texts. A long imitation can pass a skim and still fail on density: the binary-contrast rate, the fragment-colon count, the academic-register count. Record both. If the judge can't tell them apart but the density numbers diverge sharply, the skill is leaking structurally even when it reads clean, and that gap widens on a document the judge reads less carefully than a test.

3. **Judge the back half.** Long-form tells cluster late, where attention decays. If the corpus sample is long enough, give the judge the second half of each document, not the first. The front of a generated memo is usually clean; the tell is whether the discipline held to the end. This is the specific failure document mode exists to fix, so it's the specific thing the eval should probe.

Target is the same: judge accuracy near 50%, and density numbers on the imitation within range of the real sample. Until a real long-form sample exists, this channel is blocked on corpus, not on protocol.

## Constraints

- Never run the judge in the same context that produced the draft; the writer shares the draft's blind spots.
- Don't iterate the draft against the judge more than once per trial; tuning to a single judge overfits to that judge's tells, not to the user.
- Chat-corpus samples are usable for the Slack/internal register only; don't use them to judge formal channels.
