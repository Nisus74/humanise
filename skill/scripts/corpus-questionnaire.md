# Corpus questionnaire: pull your samples fast

The corpus is the most valuable asset in your profile (see `profile/voice-corpus/README.md`), and also the most likely thing to stall onboarding: hunting for old writing and annotating it cold is slow. This questionnaire makes it fast. Run it with Claude (or any capable model); it pulls 5 to 10 real samples and fills the annotations by asking, instead of leaving you a blank template.

It pairs with `generate-fingerprint.md`: this collects the samples, that turns them into your fingerprint.

## How to run it

Work one channel at a time. For each, the model gives you a concrete fetch prompt, you paste what you have, and the model drafts the `SAMPLE_TEMPLATE.md` annotations for you to correct. Stop when you have 5 to 10 across at least three channels.

## The fetch prompts (concrete beats "share some writing")

Don't ask "share some writing". Ask for a specific, recent, real artefact:

- **LinkedIn / blog:** "Paste your last LinkedIn post, or the most recent thing you published." (Start here: the most AI-prone channels.)
- **Email:** "Paste the last substantial email you sent that wasn't logistics: a pitch, a piece of feedback, a follow-up after a meeting."
- **Slack / chat:** "Paste your bluntest internal message this week, the one where you said the real thing."
- **Investor update / board paper / status update:** "Paste your last update to investors or the board, or the last status update you wrote."
- **Long-form (memo, PRD, strategy):** "Paste a memo, PRD intro, or strategy doc. Even one section is enough, and long-form is where voice breaks worst, so it matters most."

Aim for spread across channels: a few covered beats ten LinkedIn posts. Rough is fine; this is ground truth, and polish isn't the point. An unedited sample is worth more than a polished one (record that in `dogfood_status`).

## Extract the annotations by asking (don't leave them blank)

The `what_worked` and `characteristic_of_you` fields are where most corpora go generic. Don't make the writer fill them cold. For each pasted sample, the model asks two or three targeted questions and drafts the annotation from the answers:

- "What were you trying to do here, in one line?" feeds `context`.
- "What about this one lands for you? What would you have hated to see written the bland way?" feeds `what_worked`.
- "Is there a move in here you make that others don't: how you open, where the opinion sits, how you stop?" feeds `characteristic_of_you`. If the answer is generic ("clear and direct"), push once: "Clear how? Point to the sentence."

The model then writes the sample to `profile/voice-corpus/<channel>/YYYY-MM-DD-short-description.md` using `SAMPLE_TEMPLATE.md`, annotations filled from the answers. You correct anything that doesn't ring true.

## When you're done

Run `scripts/generate-fingerprint.md` to synthesise `profile/voice-fingerprint.md` and build the voiceprint baseline. Refresh both after roughly every five new samples, or when a channel first gets real coverage.

## Discipline

- Real over representative. The sample you actually sent beats the one you'd write for show.
- Specific over generic. "Opens on the number, not the story" beats "data-driven". If an annotation would fit any sample, it's too vague.
- Spread over volume. Five channels lightly covered beats one channel ten times.
- Don't block on perfection. Five rough, well-annotated samples is a working profile; you add more over time.
