# /humanise learn

Capture what the user changed in a draft the skill wrote, so the loop can learn from it. Every rewrite, cut, or addition is evidence; this command turns it into ledger records that `/humanise improve` mines for rule-change candidates.

## Inputs

Two texts:

1. **The skill's draft.** From this session if it's still in context, or a file the user points at.
2. **The shipped text.** What the user actually sent or published: pasted into chat, or a file path.

Write each to a temp file if it isn't one already. Ask for the channel and audience tag if the session doesn't already know them; `unknown` is allowed but clusters worse.

## Steps

1. Run the capture script:

   ```
   python3 scripts/capture_edit.py --draft <draft> --final <final> --channel <channel> --audience <tag>
   ```

   It diffs the texts sentence by sentence, classifies each changed span against the deterministic checks, and appends records to `profile/learning/ledger.jsonl` (the soul; gitignored, never ships). The script prints every record it wrote.

2. **Classify the unexplained spans.** Any record printed as `voice (unclassified)` is an edit no deterministic check explains. Read the draft span next to the final span and pick the mechanism from this vocabulary (a fixed menu is what keeps the ledger clusterable):

   - `too-even-rhythm`: the user broke up same-length sentences or added a fragment.
   - `no-stance`: the user inserted an opinion or a call the draft ducked.
   - `too-generic`: the user swapped an abstraction for a number, a name, or a date.
   - `synonym-cycling`: the user collapsed elegant variation back to one repeated word.
   - `opener-template`: the user rewrote a stock opening or closing move.
   - `register-miss`: the user shifted formality up or down (see `references/tone-register.md`).
   - `wrong-fact`: the correction is about content rather than voice; usually not a rule candidate.
   - `other:<slug>`: nothing fits; coin a short slug and say why in `note`.

   Append one superseding record per classified span: same `span_id`, `source: "memory"`, the chosen `mechanism`, and a one-line `note`. Append with the same JSON shape the script wrote; never edit existing lines. Mining takes the latest record per span, so the classification wins without rewriting history.

3. **Mirror durable corrections into session memory** where the environment has a memory directory, following `references/memory-loop.md` (a `feedback_writing_*` entry for a behavioural correction, `user_voice_*` for a fingerprint candidate). The ledger is the durable record that survives across tools; memory entries make the correction active in the next session's drafting card.

4. **Report the running counts.** Run `python3 evals/assertions/mine_weaknesses.py --summary` and tell the user which signatures are approaching the promotion threshold (three occurrences makes a candidate; see `evals/self-harness-loop.md`). If the mining script isn't present yet, `grep -c` the mechanism in the ledger and say so plainly.

## What not to capture

Content corrections (facts, names, numbers the user fixed) are `wrong-fact` and rarely become rules. Edits to quoted material or code aren't voice signal at all; skip them. When the user rewrote a span merely because the brief changed, that's a fresh brief rather than feedback; skip it too.
