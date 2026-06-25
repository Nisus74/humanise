# Positive patterns

The rest of this skill is mostly negative: what to avoid, what to cut, what flags as AI. This file is the opposite. These are the moves that characterise good writing: the specific habits that signal a particular human wrote something, not a language model.

Aim to hit two or three of these patterns in any piece longer than a paragraph. One positive move makes writing feel competent; three or four make it feel alive.

**How to use a move.** Each move is a thing to *do*, paired with a self-check question: what the read-aloud pass in `SKILL.md` Step 5 asks to decide whether the draft needs it. Four families map to an advisory signal in `writing_checks.py`, the script's way of pointing you back here:

- specificity moves map to `specificity_density`
- opinion moves map to `stance_signal`
- story-before-lesson maps to `generic_to_specific`
- plain verbs over fancy copulas map to `copula_ratio`

These signals flag where a draft *looks* thin; they never fail it (they ride the advisory rail, so there is no number to game). The self-check is how you decide whether texture is genuinely missing or fine for this piece. The rest of the moves are a manual menu: pick two or three on purpose, never all of them, or the moves become their own tic.

---

## Specificity moves

### Concrete numbers beat adjectives

"We reduced latency from 840ms to 120ms" beats "We dramatically reduced latency." The number does the work.

When you don't have a number, use a specific example instead. "The calibration takes the time it takes to make a coffee" beats "The calibration is quick."

Self-check: does every claim carry a number, a name, or a concrete example, or is it an abstraction with nothing to hold? Signal: `specificity_density` (advisory). Do not pad with fake numbers to clear it; that is the manufactured-precision tell.

### Named things beat generic things

"We shipped the a hospital network pilot" beats "We shipped our first pilot." "My co-founder Nick" beats "a senior colleague." Names carry weight.

Exception: use names only when you'd say them out loud. If the user wouldn't mention the person by name in conversation, don't force it in writing.

### One specific example beats three abstract ones

If you're illustrating a claim with examples, one well-developed example is more convincing than three half-sketched ones. The three-example cadence reads as AI (see structural-tells: triples).

---

## Opinion moves

### Editorialising beats describing

"The data shows X" is weaker than "The data shows X, and it's worse than I expected." The editorial word ("worse", "better", "surprising", "obvious") signals there's a human making judgements.

Self-check: is there a word in here that shows a person reached a judgement, or is it a neutral readout anyone could have written? Signal: `stance_signal` (advisory; suppressed for status updates and board papers, where neutral is correct).

### Disagreeing in print beats hedged agreement

If the user disagrees with a source, a claim, or a prevailing view, the writing should say so. "The standard advice is X; I think that's wrong because Y" beats "While some suggest X, alternative views also have merit."

### A taste claim beats a market claim

"I like when product docs state the problem in the first line" beats "Users appreciate clear problem statements." The first is the user's view; the second is a market claim dressed up as insight.

### Admitting uncertainty beats fake certainty

"I'm not sure this will work" is stronger than "It might potentially not fully succeed." Name the uncertainty directly.

---

## Rhythm moves

### Short sentence after long sentence, for punch

"We'd been running the pipeline in staging for three weeks, checking numbers, fixing edge cases, waiting for the call. Nothing broke."

The short sentence lands because the long sentence set it up. If every sentence is short, none of them punch.

### Unexpected break in a paragraph

A one-sentence paragraph placed at a rhetorical peak works. Don't overuse. Maybe once per piece.

### Parenthetical aside in the user's voice

"We'd built this in three weeks (which is roughly three weeks longer than we'd planned) and the tests were passing." The aside adds texture. It's a the user-characteristic move.

### Dropped subjects and implied connectives in casual contexts

Slack, internal email: "Think we should push to Monday" (not "I think we should push to Monday"). Works in low-register channels; doesn't work in board papers.

---

## Opening moves that work

### Specific moment

"Last Friday the RPA pilot site asked if our calibration service could handle 400 samples an hour. We said yes. Then we hung up the phone and started building."

### Direct claim

"The standard advice on startup hiring is wrong. Here's what I've seen actually work."

(Note: "Here's what I've seen actually work" is borderline because "Here's what" is a throat-clearer pattern. the user's version works because it's tied to specific experience; the abstract version is what to avoid.)

### Observation from the inside

"At six months in, we still hadn't hired a full-time designer, and I was starting to regret it."

### Question that forces a specific answer

"How do you get a pathology lab to adopt new software when the lab manager has been using the same LIMS for 15 years?"

Not: "Have you ever wondered about adoption challenges?"

---

## Closing moves that work

### Specific forward-looking claim

"Next quarter we'll know whether the calibration-service split was worth it. If latency goes below 200ms end-to-end, yes. If not, we roll back."

### Concrete ask

"If you know anyone running a pathology lab in California with more than 500 tests a day, I'd love an intro."

### Landing on a number or fact

"Three years in, we're at 12 pilot sites, 1.8M samples processed, and zero compliance incidents. That's the base we build on."

### Honest uncertainty

"I don't know if this will work. But I think the downside is bounded and the upside is large, so we're going to try."

---

## Structural moves

### State, then qualify, not qualify then state

"The migration is done. A few edge cases remain."

Not: "Although there are still some edge cases that need attention, I can report that the migration has been largely completed."

### Short punchy list over flowing prose, when the items are discrete

If you're naming three distinct things, a list works. If you're developing one argument, prose works. Pick based on what the content actually is, not based on formatting aesthetic.

### Story → lesson, not lesson → story

Lead with the specific story or example. Let the reader extract the lesson. Then confirm the lesson briefly at the end.

Don't start with "The lesson here is X. Here's a story that illustrates X." That's AI template shape.

Self-check: does the piece open on an abstract general claim and then reach for a specific to prop it up? Lead with the specific instead. Signal: `generic_to_specific` (advisory).

### Plain verbs beat fancy copulas

"The audit layer is the bottleneck" beats "The audit layer constitutes the bottleneck." "X is Y" and "X has Y" are not too plain; reaching for "serves as", "represents", "constitutes" is dissertation register dressed as precision.

Self-check: would a plain "is" or "has" carry this sentence? Then use it. Signal: `copula_ratio` (advisory).

---

## Voice moves specific to the user

Evidence base: the fingerprint synthesis (email and cover letters), their preferences statement, and the chat corpus in `profile/voice-corpus/chat/` (June 2026). Channel-specific moves get added as the formal corpus grows.

### Plain criticism vocabulary

When judging work in internal channels, the user's register is colloquial and blunt: "blah", "generic", "junk", "not authentic", "reads like a book report". Internal assessments can use that register. Don't dress criticism in formal language they wouldn't use; the formality is its own tell.

### Forward-motion closings

His warm closes are next steps, not sentiment: "Once we get it ironed out, we can update the strategy document." Praise is brief and chained to the next ask ("this is great, what do you need to do hit 100%?"). Don't pad endings with gratitude theatre.

### Audience named inside the ask

They calibrate explicitly to a named reader ("she is not technical and really doesn't know what a prompt is"). Writing that's theirs tends to show its awareness of who's reading without announcing it.

### Direct over indirect

the user prefers saying the thing directly. "I'd cut that section" beats "You might consider whether that section is necessary."

### Lean on frameworks without citing them

the user draws on Lean Startup, Continuous Discovery, Trusted Advisor. The frameworks inform their thinking; they rarely name-drop them. If they are making a build-measure-learn argument, they say "test it cheaply first and see what happens" rather than "applying the build-measure-learn loop here."

### Ship, learn, iterate

His operating mode. Writing reflects this: draft → critique → revise, not draft → polish → polish.

### Technical fluency without jargon parade

the user understands the edge-platform, IoT, and compliance tech. His writing shows this through specifics (ISO 15189, CFR Part 11, NATA) rather than through jargon density. If a technical term is load-bearing, it's there; if it's showing off, it's not.

### Compliance and regulatory as serious, not scary

In writing for pathology or healthcare audiences, the user treats compliance as a real constraint to design around, not as a bureaucratic obstacle. The tone reflects this: regulated is how the work gets done, not a problem to overcome.

---

## Using this file

When drafting, pick two or three positive patterns to deliberately use. The mechanical sweep is about removing bad patterns; this is about installing good ones.

Over time, the patterns specific to the user (the last section above) get more weight as the voice corpus fleshes out their actual habits. A generic "specific numbers beat adjectives" is universally true. A specific "the user opens investor updates with the biggest number from the quarter" is the user's move.

Combine with `profile/voice-fingerprint.md` and the raw samples in `profile/voice-corpus/` for maximum effect.
