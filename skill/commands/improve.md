# /humanise improve

Run one full cycle of the self-improvement loop: benchmark the skill's output, run the blind voice test, mine the accumulated evidence for weaknesses, and gate any proposed engine change. The loop's rules live in `evals/self-harness-loop.md`; this command executes them. Every stage is skippable, but say which stage was skipped and why in the final report.

Artefacts for the run land in `profile/learning/runs/<UTC timestamp>/` (the soul; gitignored, never ships). Flags: `--baseline` also generates untreated comparison drafts; `--skip-benchmark`, `--skip-indist` to run a partial cycle.

## a. Preflight

1. Held-in must be green before anything: `python3 evals/assertions/selftest.py`. Red means fix the engine first; an improvement cycle on a broken engine mines noise.
2. `python3 scripts/build_voiceprint.py --status --json`. No profile: offer `/humanise init` and stop. Stale voiceprint: rebuild it (`humanise voiceprint --build`). Note which channels are eligible for the pairwise test.
3. Create the run directory: `profile/learning/runs/<timestamp>/`.

## b. Benchmark (rule compliance, with_skill vs baseline)

For each fixture in `evals/evals.json`, spawn an `agents/eval-generator.md` subagent in `mode: skill`, passing only the fixture's `prompt`, `channel`, `audience_tag`, and `medium` (never the assertions), with output path `<run>/with_skill/eval-<id>.md`. With `--baseline`, spawn a second generator per fixture in `mode: baseline` writing to `<run>/baseline/eval-<id>.md`.

Grade each directory: `python3 evals/assertions/run_all.py --outputs <dir>`. Read the exit codes correctly: baseline red is expected (the baseline exists to lose); with_skill hard failures are not a stop, they are mining signal for stage d. Summarise the delta (pass rates, which channels leak). Note in the report that an in-agent baseline is directional rather than a controlled experiment, and never gates anything.

## c. Indistinguishability (the real voice gate)

For each eligible channel from preflight (at least 2 usable samples):

1. `python3 evals/assertions/pairwise_trial.py --prepare --channel <ch> --profile profile --run-dir <run>/indist-<ch>` (default 5 trials, seeded; the seed prints for replay).
2. Per trial: spawn `eval-generator` (`mode: skill`) with ONLY that trial's `brief.md` and the files in `allowed-context.txt`; it writes the counterpart. Then `--pair --run-dir <dir> --trial <n> --generated <file>`.
3. Per trial: spawn a FRESH `agents/indistinguishability-judge.md` subagent whose prompt contains only the two file paths `trial-<n>/text-a.md` and `trial-<n>/text-b.md`. Never reuse a judge across trials, never run one in the context that generated the drafts. Collect the JSON verdict tails into `<dir>/verdicts.json`.
4. `--score --run-dir <dir> --verdicts <dir>/verdicts.json`. Append the printed row to `evals/indistinguishability-log.md` (aggregate row and signal slugs only; the full transcripts stay in the run directory).

Zero eligible channels: print the corpus priority list from the profile's `CORPUS.md`, note the stage as blocked on corpus, and continue. That result is itself the loop's finding: the highest-value change is samples rather than more rules.

## d. Weakness mining

```
python3 evals/assertions/mine_weaknesses.py \
  --benchmark with_skill=<run>/with_skill/benchmark.json \
  --dictionary-gaps --out <run>/candidates.json
```

(The judge signals are already in the ledger via `--score`; add `--indist` only for a results.json that was scored without a ledger.) Empty candidates is a healthy result: report "no signature at threshold; loop healthy, evidence accumulating" and stop cleanly after logging the run summary.

## e. Proposal and gate

Spawn `agents/improvement-proposer.md` with `<run>/candidates.json`. Present its proposals to the user, ranked. For each proposal the user accepts in principle:

1. Apply the edit to the named surface, smallest diff possible.
2. Run the gate for its tier (`evals/self-harness-loop.md` is the authority):
   - **Tier 1** (slop word, channel row): selftest green.
   - **Tier 2** (detector, threshold, structural rule): selftest green, plus the held-out surfaces not regressed: regenerate and grade `evals/holdout-evals.json` drafts, and re-run stage c where the change touches voice.
   - **Tier 3** (absolute rules, fingerprint): all of the above, plus an `agents/adversarial-reviewer.md` read, plus the user's explicit typed sign-off. Never edit `profile/absolute-rules.md` or the fingerprint's absolute-rules section without it.
3. On acceptance: write the `CHANGELOG.md` entry (target, surface, evidence, eval result). On rejection: append the rejected proposal to the ledger (`source: "memory"`, note why); a rejection is evidence.

Reminder for this repo: `npm run build` and git operations run on the user's machine; sandboxed mounts break them.

## Report

End with: benchmark delta, judge accuracy per channel (with trial counts, never a bare point score), candidates found, proposals accepted/rejected, and the single highest-value next action (usually a specific corpus sample).
