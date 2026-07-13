# Generate your voice fingerprint

Turns samples, negative examples and user edits into `profile/voice-fingerprint.md`, the distilled model
the skill reads selectively for the current task. Run it once several pieces of evidence exist.

This is a prompt and procedure, not a binary: run it with Claude (or any capable model) pointed at your corpus. The method is "extract structured descriptors from real samples, then write to those descriptors", which beats open-ended "write like me".

## Inputs

- Every `profile/sample-*.md` and its annotations.
- `profile/voice-decisions.md`, `profile/negative-examples.md` and available draft-to-final edit pairs.
- `profile/identity.md`, `profile/soul.md`, `profile/absolute-rules.md` and `profile/relationships.md`.

## Procedure

1. **Read every sample raw.** Downweight heavily edited or ghostwritten material.
2. **Extract decisions first.** Record what the writer selects, judges, foregrounds, leaves out and asks
   the reader to do. Then record structure, cadence and diction.
3. **Use contrastive evidence.** Treat a final user edit as stronger evidence than the rejected draft.
   Use negative examples to define boundaries.
4. **Label confidence.** Confirmed means three independent examples or explicit user confirmation;
   supported means two examples or one plus confirmation; provisional means one occurrence or an inference.
5. **Measure optional tripwires.** Use numeric features only as advisory distribution summaries. Never
   convert them into targets.
6. **Write `voice-fingerprint.md`** to the structure below.
7. **Name the gaps.** List channels and relationships with no direct evidence.

## Output structure (write to profile/voice-fingerprint.md)

Write each behavioural section as **moves**, not adjectives. A move names a concrete habit, shows a verbatim example from the corpus, and where it sharpens the picture, an anti-example: the bland version you would never write. "Opens investor updates on the quarter's biggest number, never on a pleasantry" is a move; "clear and direct" is an adjective. The stats table is one section, not the whole fingerprint; the moves are what make a draft sound like the writer rather than merely clean.

- **Status, confidence and evidence sources:** what it is built from and what cannot be re-verified.
- **The absolute rules:** pull from `absolute-rules.md`; the few that override everything.
- **Selection and judgement:** what the writer believes is worth saying and how they make calls.
- **Reader handling:** how trust, power, bad news, disagreement and asks change by relationship.
- **Opening moves** and **closing moves:** the shapes that recur, each with a verbatim example and, where it sharpens it, an anti-example.
- **Recurring phrasings** and **words that never appear.**
- **Sentence habits:** length variation (burstiness), word choice (perplexity), active voice, fragment discipline.
- **How disagreement is handled. Humour. Things never done.**
- **Channel-specific adjustments:** per channel with samples; mark the rest thin-signal.
- **Calibration examples:** verbatim sentences to anchor drafting.
- **Diagnostic profile:** optional measured ranges, explicitly advisory.

## Discipline

- Specific over generic. "Opens on the ask, not a pleasantry" beats "clear and direct".
- Evidence or it stays provisional. A fingerprint of guesses produces confident imitation.
- Tripwires, not quotas. The numbers flag a draft for another look; never pad prose to hit them.
- Scope every pattern to the channel and relationship the evidence supports.
- Regenerate, do not accumulate patches, when the evidence changes the picture.
