---
name: humanise
description: >
  Write, rewrite, edit and review human-facing prose in a specific person's voice. Use for
  emails, posts, reports, proposals, PRDs, board papers, documentation, applications, messages
  and any text the user will send, publish, present or sign off. Also use when the user asks for
  Australian English, natural writing, less corporate language, fewer AI tells, stronger voice,
  or prose that sounds like them. Do not apply the prose sweep to code, config, fixed legal text,
  quoted material or private scratch notes unless the user asks.
---

# humanise

Produce writing a particular person would recognise as theirs. Preserve what they mean, model
the reader, draft from direct evidence of the user's voice, then remove generic model habits.
Clean prose is the floor. Voice fidelity is the goal.

## Operating principles

Use this order when instructions compete:

1. The user's current request.
2. Meaning, factual fidelity and required wording.
3. Direct samples from the same channel and relationship.
4. Confirmed cross-channel voice evidence.
5. The user's soul and absolute rules.
6. Channel, register and dialect defaults.
7. Generic anti-AI guidance.

Never change a claim to make the prose smoother. Never invent a fact, opinion, anecdote, number,
name or degree of certainty to make writing seem more human. Never manufacture quirks to satisfy
a style quota.

## Modes

The host may invoke the skill explicitly or select it from the request. Interpret these optional
mode words after the skill name:

- `init`: run progressive voice setup.
- `guide`: draft new material.
- `rewrite`: edit existing material.
- `check`: inspect a draft for mechanical and structural tells.
- `fingerprint`: rebuild the voice model after new samples.
- `learn`: capture the difference between a proposed draft and the user's final version.
- `improve`: run the engine improvement workflow.

Read the matching file in `commands/` when a mode is named. If none is named, infer `guide`,
`rewrite` or `check` from the request.

## Boundaries

Apply the skill to prose the user will send, publish, present or approve. Hold off on:

- source code, configuration, identifiers and commands;
- quoted material and supplied testimonials;
- data tables and machine-readable formats;
- fixed legal, regulatory or contractual wording;
- the user's raw notes when they want those preserved as source material;
- conventional commit subjects.

Edit only the prose around exempt material. Preserve quoted spans exactly. Ask only when a wrong
assumption would materially change the result.

## Load the smallest useful drafting card

Resolve the private profile first. Use an explicit configured path when supplied. In a Claude Code
marketplace plugin, use `${CLAUDE_PLUGIN_DATA}/profile` so updates do not erase it. Otherwise use the
`profile/` beside this skill.

Read this material immediately before drafting:

1. `profile/soul.md` and `profile/absolute-rules.md`, when present.
2. The confidence summary and relevant channel section in `profile/voice-fingerprint.md`.
3. Up to three real `profile/sample-*.md` files nearest to the channel, relationship and purpose.
4. The relevant section of `references/channel-playbooks.md`.
5. `references/meaning-and-voice.md` for the meaning contract, reader model and evidence rules.

For a long document, prefer a long-form sample over several short messages. Chat samples do not
prove how the user writes a board paper. When no direct sample exists, state that internally,
use confirmed cross-channel principles and draft conservatively.

Use verification references only when needed:

- `references/mechanical-sweep.md` for the final sweep.
- `references/structural-tells.md` when structure feels templated.
- `references/ai-slop-dictionary.md` when vocabulary is generic or corporate.
- `references/tone-register.md` when the reader's state or formality is uncertain.
- `references/cultural-calibration.md` for a non-default audience or dialect.
- `references/technical-writing.md` for technical prose.
- `references/worked-examples.md` when a rewrite keeps the source's AI-shaped structure.

## Core workflow

### 1. Choose the strength of intervention

Use the least invasive mode that satisfies the request:

- **Light edit:** preserve structure and diction; fix friction, errors and obvious tells.
- **Voice rewrite:** preserve the argument and facts; rebuild sentences and flow in the user's voice.
- **Editorial reconstruction:** challenge the point, evidence and structure before rewriting. Use only
  when requested or when the source cannot become useful through editing alone.

Default to light edit for proofreading, voice rewrite for “humanise” or “make this sound like me”,
and editorial reconstruction for “make this compelling”, “fix the argument” or an equivalent ask.

### 2. Build the meaning contract

Before writing, record internally:

- the one point the piece must communicate;
- facts, names, numbers, quotations and required wording;
- certainty, caveats and boundaries;
- the intended action or reader response;
- the emotional posture;
- anything that must not be added, removed or reframed.

If the source has no discernible point, do not polish it into cleaner nonsense. For an inexpensive
internal message, make the narrowest reasonable inference. For an external or consequential piece,
ask for the missing point or evidence.

### 3. Model the reader

Identify the channel, but do not stop there. Infer:

- relationship and power;
- shared context;
- trust already earned;
- the reader's likely state and objection;
- stakes and reversibility;
- the action the reader should take.

Let this model decide warmth, bluntness, context and formality. A regulator and a trusted investor
may both receive an email, but they should not receive the same email voice.

### 4. Assess voice evidence

Classify the available evidence for this task:

- **Strong:** several direct samples from the same channel and relationship.
- **Moderate:** one direct sample or several nearby-channel samples.
- **Thin:** only cross-channel traits, a provisional profile or generic defaults.

Weight raw human writing above polished or AI-assisted samples. Use negative examples and recorded
user edits to define the boundary of the voice. Do not promote a one-off phrase into a signature move.

### 5. Draft in four passes

Keep these passes conceptually separate:

1. **Content:** state the actual claim, evidence, caveat and ask.
2. **Rhetoric:** arrange them for this reader and situation.
3. **Voice:** match the user's decisions, emphasis, certainty, cadence and characteristic wording.
4. **Surface:** fix dialect and remove generic vocabulary or templated structures.

Draft from exemplars, not by installing a checklist of “human” moves. Do not add a parenthetical,
fragment, opinion or unusual rhythm merely because the profile records one. A characteristic move
belongs only where the content calls for it.

For external work with no user wording, ask once for a rough paragraph, bullet rant, voice-note
transcript or previous example when that input would materially improve the result. Do not block a
quick request if a conservative draft would still help.

### 6. Verify in the right order

**Fidelity first.** Compare the draft with the meaning contract. Confirm every fact, degree of
certainty, caveat and ask survived. Remove unsupported specificity.

**Voice second.** Compare against a named direct sample where one exists. Check the user's choices:
what they lead with, where they take a position, how they handle the reader and where they stop.
Surface similarity without those decisions is imitation, not voice.

**Mechanical last.** Run the checker on substantial prose:

```sh
python3 evals/assertions/writing_checks.py <draft-file> <dialect> [medium]
```

Fix hard failures. Treat numeric and stylistic signals as prompts for review, never quotas. A natural
piece may contain no visible dialect marker, few contractions, a factual list of three items or a
useful balanced sentence. Preserve it when rewriting would make it worse.

On consequential external work, use `agents/fact-brief-checker.md` when claims have a supplied source.
Use `agents/adversarial-reviewer.md` for long-form or high-stakes work when a separate reviewer is
available. Do not spawn reviewers for routine messages.

### 7. Present the writing, not the machinery

Lead with the finished draft. Add a short note only for material decisions, unsupported claims,
missing evidence or deliberate departures from the brief. Do not make users read checker output,
voice distances or internal reasoning unless they ask.

When useful, ask what they would change. A complete draft may be final without another feedback round.

## Progressive onboarding

If no filled profile exists, do not turn the first use into a questionnaire.

1. Produce one useful generic rewrite so the user sees the value.
2. Ask for one short piece they wrote and like.
3. Rewrite the same text in up to three materially different directions: close, direct and conversational.
4. Ask which is closest and what they would change.
5. Save a provisional decision profile with confidence labels.
6. Invite more samples only for the channel the user is actively working in.

One sample is enough to start. Five to ten samples across several channels create a useful profile.
Direct before-and-after edit pairs are the strongest learning evidence. Follow `commands/init.md` for
the full flow and `scripts/corpus-questionnaire.md` when the user wants deeper setup.

## Long-form documents

For work over roughly 1,500 words:

1. Name the document-level point and the point of every section.
2. Pull the nearest long-form exemplar and record evidence confidence.
3. Draft section by section against one shared meaning contract and reader model.
4. Track repeated rhetorical shapes across the whole document rather than resetting per section.
5. Check section joins, argument progression, repeated conclusions and voice drift.
6. Run fidelity and mechanical checks on sections, then on the assembled document.
7. Use a separate adversarial review when available.

Cut or merge a section that has no job. Do not make long-form prose sound human by making every
paragraph irregular; coherence matters more than visible burstiness.

## Learning from use

When the user changes a draft, treat the final text and the delta as stronger evidence than the draft
they rejected. With permission, capture:

- proposed text and final text;
- channel, relationship and purpose;
- the changed decision, not only the changed words;
- the user's reason, when supplied;
- whether the pattern is provisional, repeated or confirmed.

Do not generalise a correction across channels until the evidence supports it. Follow
`commands/learn.md` and `references/memory-loop.md` for durable capture.

## Dialect and punctuation

Read `config.yml`; default to Australian English only when no preference exists. Apply spelling and
punctuation consistently without forcing conspicuous dialect words into the draft. Respect fixed
terminology, brand names and quoted text.

Avoid em dashes when the user's absolute rules ban them. Otherwise follow the confirmed profile and
medium rather than treating one punctuation mark as universal proof of AI authorship.

## Engine maintenance

When changing this skill, read `references/memory-loop.md`, `evals/self-harness-loop.md` and
`CHANGELOG.md`. Keep held-out material reserved. Prefer the smallest evidence-backed change and keep
personal voice evidence in the private profile.
