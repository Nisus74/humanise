# Memory feedback loop

The humanise skill gets better over time if it remembers what the user accepts and what they rewrite. This file defines how that feedback accumulates into the session memory directory (wherever the current environment persists memories; in Cowork, the space's memory folder indexed by `MEMORY.md`) so future conversations can reuse it. Don't hard-code a path; resolve it from the environment at write time.

This is a lightweight convention, not a hard protocol. The goal is: when the user rejects a specific phrasing, or accepts something unusual, the pattern survives the session.

---

## Three memory types the skill writes

### 1. `feedback_writing_<topic>.md`: behavioural corrections

Trigger: the user corrects a specific phrasing or structural choice, OR accepts something non-obvious without pushback.

Store:

```
---
name: Writing feedback on <short topic>
description: What the user rewrote or accepted during a writing task, with the reason
type: feedback
---

<The rule itself, in one line>

**Why:** <the user's reason, or the inference from context>

**How to apply:** <when this guidance kicks in: channel, audience, register>
```

Examples of what to save:

- "the user cuts 'lean into' every time it appears, even though the slop dictionary has it as severity 2. Treat as severity 1 for their writing." (correction)
- "the user kept the opening 'Last Friday the pilot site asked', a specific-moment opener they accepted without revision on an investor update." (validated judgement call)
- "For Slack messages under 30 words, the user wants no sign-off at all, not even 'thanks'." (behavioural preference)

### 2. `user_voice_<facet>.md`: voice fingerprint updates

Trigger: something new about the user's voice that `profile/voice-fingerprint.md` should eventually absorb, but hasn't been corpus-verified yet. Treat as a candidate until confirmed.

Store:

```
---
name: Voice fingerprint candidate for <facet>
description: Observed the user-specific voice pattern pending corpus confirmation
type: user
---

<The observed pattern>

**Source:** <single observation, multiple observations, or explicit statement>

**Confidence:** <low/medium/high>

**How to apply:** <which channels this would affect>
```

When the voice corpus grows enough to confirm or reject the candidate, the relevant move in `profile/voice-fingerprint.md` should be updated and the candidate memory removed or merged.

### 3. `project_writing_<context>.md`: ephemeral writing project context

Trigger: the user is working on a sustained piece of writing (a series of investor updates, a board paper cycle, a blog series) and you learn context that should survive the current session but isn't a permanent voice fact.

Store per the standard `project` memory template. Include deadline, stakeholder, and why. These memories decay fast and should be pruned on the next consolidation pass.

---

## What NOT to write to memory

- Specific drafts or outputs. These belong in the conversation or the workspace, not memory.
- Generic prose rules already in the skill. If it's in `SKILL.md` or a references file, don't duplicate it.
- One-off corrections that don't generalise. If the user rewrote one sentence to be shorter, that's just editing; save it only if the pattern recurs or they explain the reasoning.
- Any content sensitive enough to fail the memory system's own guardrails.

---

## When to read from memory during writing tasks

At the start of any humanise task:

1. Scan `MEMORY.md` for entries matching `feedback_writing_*`, `user_voice_*`, and `project_writing_*`.
2. Load relevant ones into the working context. Relevance = matches the current channel, audience, or topic.
3. Apply them during drafting and the self-critique pass. A feedback memory that says "the user always cuts 'lean into'" means do not emit that phrase.

---

## Consolidation cadence

The `consolidate-memory` skill should be pointed at `feedback_writing_*` periodically. Specific things to look for on consolidation:

- Duplicates saying the same thing in different words. Merge.
- Contradictions (one memory says "prefer X", another says "avoid X"). Investigate context; the channel or audience is usually the distinguishing factor. Rewrite both memories to include the context.
- Stale project memories past their deadline. Prune.
- Voice candidates that have been corroborated by corpus samples or repeated observations. Promote these to `profile/voice-fingerprint.md` and remove the candidate memory.

---

## Worked example

**Scenario:** the user asks for a LinkedIn post. Draft emits "this pilot really moved the needle on our go-to-market clarity". the user replies: "cut 'moved the needle', I'd never say that out loud".

**Memory to write:**

File: `feedback_writing_moved_the_needle.md`

```
---
name: Writing feedback on "moved the needle"
description: Cut the phrase "moved the needle" from the user's writing; they have flagged it as a phrase they would not say
type: feedback
---

Never emit "moved the needle" in writing for the user.

**Why:** They explicitly said they would not say it out loud. Reads as corporate speak.

**How to apply:** Across all channels. If the output otherwise uses it, rewrite with a specific claim: name the metric or outcome that actually shifted.
```

MEMORY.md entry:

```
- [Writing feedback on "moved the needle"](feedback_writing_moved_the_needle.md): cut this phrase from all the user writing
```

Next LinkedIn post a week later: the skill sees the memory, does not emit "moved the needle", and uses a specific metric instead.

---

## How this feeds the self-improvement loop

Memory is stage one (weakness mining) of the skill's self-improvement loop in `evals/self-harness-loop.md`. A single correction is one observation; clustering several by failure signature (the tell, the channel, the mechanism) is what justifies a rule change. Promotion of a voice candidate into `profile/voice-fingerprint.md`, or a feedback rule into the skill, goes through that loop's acceptance gate: the change must keep the held-in suite (`evals/assertions/selftest.py`) green and not regress the held-out indistinguishability test. Three reinforcements make a candidate; the gate makes it a rule.

## The learning ledger (durable across tools)

Session memory depends on the host environment exposing a memory directory, which not every tool does, and entries decay with the session store. The durable record is `profile/learning/ledger.jsonl`: append-only JSON records written by `/humanise learn` (`scripts/capture_edit.py`), one per changed span, each carrying the failure signature `(check, channel, mechanism)` that `evals/assertions/mine_weaknesses.py` clusters into rule-change candidates. Memory entries mirror the ledger so a correction is active in the next session's drafting card; the ledger is what the improvement loop actually mines. It lives in `profile/` (the soul) because it holds the user's verbatim text: gitignored, never ships.

## Interaction with the voice corpus

The voice corpus (the `profile/sample-*.md` files) is the authoritative long-term record of the user's actual writing. Memory is the short-term buffer. The flow:

1. Skill learns something from a single interaction.
2. Writes a `feedback_writing_*` or `user_voice_*` memory.
3. Over multiple sessions, the pattern either repeats (confirming) or doesn't (weakening).
4. Periodically, confirmed patterns get synthesised into `profile/voice-fingerprint.md` by re-running the synthesis pass over the corpus plus the accumulated memories.
5. Once absorbed into the fingerprint, the candidate memory can be pruned.

This keeps the skill responsive to feedback in the short term without bloating the long-term voice record with one-offs.
