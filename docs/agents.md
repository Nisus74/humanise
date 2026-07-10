# Subagents

humanise uses a handful of subagents: focused helpers the skill spawns in their own fresh context to do one job well. You rarely call these yourself. The skill spawns the two verification agents when a draft is about to ship, and `/humanise improve` orchestrates the three loop agents. This page is for understanding what runs under the hood, and why each one is walled off from the context that produced the work it judges.

The separation is deliberate. A reviewer who saw the drafting rationale would inherit the writer's blind spots. A judge who saw the corpus could not stay blind. So each agent gets only what it needs, and nothing that would let it cheat. The agent definitions live in `skill/agents/`.

Two families:

- **Verification** runs on a draft before it ships: `adversarial-reviewer`, `fact-brief-checker`.
- **The self-improvement loop** powers `/humanise improve`: `eval-generator`, `indistinguishability-judge`, `improvement-proposer`.

---

## Verification agents

These run on a finished draft as the last gate before it leaves your hands. Both run in a separate context from the drafting, so they read with fresh eyes.

### adversarial-reviewer

**Role.** Tries to fail a draft before it ships, by catching what makes it read as AI-generated.

**When it runs.** From the skill's Step 6 for external pieces, from Step D5 (mandatory for long-form), and from the acceptance gate for high-stakes (tier-3) engine changes. `/humanise guide`, `/humanise rewrite`, and `/humanise improve` all reach it.

**What it sees.** The draft alone. It does not receive the brief or the source, so it reads with no idea of what the piece was meant to do. It assumes the text is AI-generated until the prose proves otherwise.

**What it does.** Three passes: a mechanical pass that runs `writing_checks.py` and reads the structural-density block; a pass for the contrast shapes the regex misses; and a pass for the subtle tells (balanced clause pairs, uniform paragraph shape, an "assembled from parts" feel, the two tells the script under-fires on by design).

**Output.** The strongest tells, up to three, each with the exact offending sentence and a one-line fix, plus a verdict of ship or fix-first. It reports fewer on a clean draft, and none when it finds none. Inventing a tell to reach a quota is itself a failure, because it teaches you to distrust the reviewer.

### fact-brief-checker

**Role.** Checks that a draft is true to its brief: the specific claims are supported, and the piece still says what the brief asked.

**When it runs.** From Step 6 and Step D5, for external pieces that carry checkable claims, when a brief or source exists. The skill pushes drafts toward concrete numbers and names because specificity reads as human, and that same pressure can manufacture specifics that are confident and wrong. This agent is the guard against shipping one in your name.

**What it sees.** The brief or source material and the draft. Unlike the adversarial-reviewer, it does receive the source, so it can check claims against it. It runs in its own context, away from the drafting.

**What it does.** Two checks. It lists every checkable claim (figures, dates, proper nouns, quotes, and the causal claims a piece leans on) and marks each supported, unsupported, or contradicted. Then it states in one line what the brief asked the piece to say, and confirms the draft still carries that point.

**Output.** The unsupported or contradicted claims with their exact sentences, the point check, and a verdict of ship or fix-first. It writes "not checkable here" rather than guessing at anything the source cannot confirm.

---

## Self-improvement loop agents

These three power `/humanise improve`, and each is built so the loop cannot game itself. The generator never sees what it will be graded against. The judge stays blind, and the proposer works only from recorded evidence.

### eval-generator

**Role.** Generates one draft for the benchmark or the indistinguishability stage of a loop run.

**When it runs.** Spawned per fixture during `/humanise improve`, once per benchmark fixture and once per pairwise trial.

**What it sees.** A mode, a writing brief, and an output path. It never sees the eval's assertions. Drafting to the assertions is exactly the Goodhart failure this loop exists to catch, so the assertions are withheld and the agent is told to stop rather than read them if it stumbles on them.

**Modes.** In `mode: skill` it runs the full SKILL.md workflow (drafting card, both sweep passes, the checker) and writes a treated draft. In `mode: baseline` it receives only the brief, reads none of the skill, and writes the answer a capable assistant would give without humanise. The baseline exists to lose; it gives the benchmark an untreated comparison. On the indistinguishability path it reads only the files named in an allowed-context manifest, so a trial can stay honest.

**Output.** The finished draft, written to the given path. No commentary.

### indistinguishability-judge

**Role.** The blind pairwise judge. This is the only thing in humanise that gates on voice.

**When it runs.** Once per trial in the indistinguishability stage of `/humanise improve`. A fresh judge is spawned for every trial, never reused, never run in the context that generated the drafts.

**What it sees.** Two texts, unlabelled and order-randomised: one written by a real person, one an imitation. It reads only those two files. It has no access to the corpus, the conversation that produced either text, or the key that says which is which. Opening any of those would unblind the trial and void it.

**What it does.** Picks the real one, names the three strongest signals that decided it (each tied to a sentence or pattern), and states a calibrated confidence. On a close pair, medium is the correct answer, and an over-confident high is a calibration failure even when the pick is right.

**Output.** The verdict, the signals, the confidence, and a machine-readable JSON tail the loop parses. The signals matter more than the verdict: they are the repair list. Advisory checks and the voiceprint never gate; only this judge does.

### improvement-proposer

**Role.** Drafts bounded engine-change proposals from the mined weakness clusters.

**When it runs.** In the proposal stage of `/humanise improve`, once the mining step has written `candidates.json`.

**What it sees.** Only `candidates.json` and the named engine files. It runs in a fresh context on purpose, so it argues from the recorded evidence rather than the session that produced it. It never invents evidence beyond the file.

**What it does.** For each candidate it writes one proposal in a four-part schema: the target (the failure as behaviour, with count and sources), the surface (the exact file and section to edit, the smallest that fixes it), the evidence (the cluster itself), and the expected effect (what changes and what could regress). It states the gate tier, and for a voice-level cluster it will answer "no safe bounded edit; the repair is corpus" rather than force a mechanical rule onto a voice failure.

**Output.** Ranked proposals, highest count first. It proposes; it never applies. The orchestrator runs the gate and you decide what lands.

---

For how these agents fit the loop end to end, see [DEVELOP.md](DEVELOP.md) ("Run the loop") and `skill/evals/self-harness-loop.md`. For the commands that spawn them, see [commands.md](commands.md).
