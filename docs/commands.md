# Commands

humanise is one skill with a few verbs. Inside your agent you call them as `/humanise <command>`. Some also have a terminal equivalent through the CLI (`node cli/bin/cli.js <verb>`, or `npx humanise <verb>` once published). New here? Read [getting-started.md](getting-started.md) first, then come back for the detail.

The commands, grouped by job:

| Command | Job | Group |
| --- | --- | --- |
| `init` | Set up your voice profile | Setup |
| `guide` | Draft new content in your voice | Everyday |
| `rewrite` | Rewrite existing AI text in your voice | Everyday |
| `check` | Run the deterministic checker (no model) | Everyday |
| `fingerprint` | Rebuild your voice fingerprint | Setup |
| `learn` | Capture your edits as evidence | Self-improvement |
| `improve` | Run one cycle of the self-improvement loop | Self-improvement |

---

## `init`

**What it is.** One-time setup that writes your voice profile so every later command sounds like you.

**When to use it.** The first time you run humanise, or whenever you have no `profile/` yet.

**How to run it.** `/humanise init` inside your agent. This is the guided version: the agent asks the soul questions, helps you gather samples, and builds your fingerprint. There is also a smaller terminal command, `node cli/bin/cli.js init`, that only scaffolds the empty profile files from the template; it does not do the interview. For a real voice, use the in-agent version.

**Reads / writes.** Copies `profile.template/` to `profile/`, then writes `profile/soul.md`, `profile/identity.md`, `profile/absolute-rules.md`, your `sample-*.md` files, and `profile/voice-fingerprint.md`. Everything under `profile/` is gitignored and never committed.

**Example.** You say "set up humanise". The agent walks you through what you believe about writing, collects five to ten real samples with a fetch prompt per channel, and generates your fingerprint. Budget about ten minutes.

See also: [SETUP.md](SETUP.md) for the manual 15-minute walkthrough.

---

## `guide`

**What it is.** Draft mode. Writes new content in your voice from the first line.

**When to use it.** Before writing, when you want the draft to sound like you from the start rather than fixing a generic draft afterwards.

**How to run it.** `/humanise guide` inside your agent, with your brief.

**Reads / writes.** Reads `profile/soul.md`, `profile/voice-fingerprint.md`, the nearest `profile/sample-*.md` samples for the channel, and the channel playbook in `references/channel-playbooks.md`. Writes the draft into your session; nothing is saved to disk unless you ask.

**Example.** "Draft a LinkedIn post about the onboarding launch." The skill names the point, drafts from your closest samples, runs both sweep passes and the checker, self-critiques, and presents the result with the evidence so you can see what it changed.

**Subagents.** For an external piece that carries checkable claims, `guide` spawns the [adversarial-reviewer](agents.md#adversarial-reviewer) and the [fact-brief-checker](agents.md#fact-brief-checker) before it hands the draft back.

---

## `rewrite`

**What it is.** Edit mode. Takes existing AI-generated text and rewrites it in your voice.

**When to use it.** When you paste text and want to de-slop it or make it sound like you.

**How to run it.** `/humanise rewrite` inside your agent, with the text to fix.

**Reads / writes.** Same profile inputs as `guide`. Preserves the original intent while stripping the tells; presents the rewrite with a diff of the anchor changes.

**Example.** You paste a paragraph a model wrote, full of <!--sweep-ignore-->"leverage" and "seamless"<!--/sweep-ignore--> and an em dash. The skill diagnoses the tells, rewrites preserving your point, runs the checker until it is clean, and shows the before and after.

**Subagents.** As with `guide`, external pieces get an [adversarial-reviewer](agents.md#adversarial-reviewer) read, and a [fact-brief-checker](agents.md#fact-brief-checker) pass where a brief or source exists.

---

## `check`

**What it is.** The deterministic checker on its own, with no model involved. Wraps `evals/assertions/writing_checks.py`.

**When to use it.** To gate a draft before you ship it, or in CI. It is the fastest way to catch the mechanical tells, and it runs anywhere Python 3 does.

**How to run it.**

- Terminal: `node cli/bin/cli.js detect <file> [dialect] [medium]` (dialect defaults to `aus`; also `us`, `uk`).
- In-agent: `/humanise check`. The agent writes the draft to a temp file, runs the checker, and reads back the summary (the `failed` list and the `structural_density` block).

**Reads / writes.** Reads the file you point at. Writes nothing; it prints a report and exits non-zero on failure.

**Example.** `node cli/bin/cli.js detect draft.md` prints the slop words, the em dashes, the template openers, and the structural density, then exits 1 if any hard check failed. Drop it into a pre-commit hook or a CI step.

The checker is the body; it never sees your soul, so a clean run is necessary but not sufficient. Pair it with the read-aloud test and, for external pieces, the [adversarial-reviewer](agents.md#adversarial-reviewer).

---

## `fingerprint`

**What it is.** Regenerates your voice fingerprint from your corpus, and rebuilds the numeric voiceprint baseline alongside it.

**When to use it.** After you add `profile/sample-*.md` samples: roughly every five new samples, or whenever a channel gets real coverage for the first time.

**How to run it.** `/humanise fingerprint` inside your agent. It follows `scripts/generate-fingerprint.md`: read every sample, extract the descriptors with evidence, measure the tripwires, and write `profile/voice-fingerprint.md`. The same step rebuilds the voiceprint baseline (`node cli/bin/cli.js voiceprint --build`).

**Reads / writes.** Reads every `profile/sample-*.md`. Writes `profile/voice-fingerprint.md` and `profile/voiceprint.json`, and notes the gaps (channels with no samples).

**Example.** You paste three new blog posts as samples, then run `/humanise fingerprint`. Your fingerprint now reflects how you open a blog post, and the voiceprint can flag a draft that drifts from it.

The fingerprint does more for your voice than any rule. More samples, better voice.

---

## `learn`

**What it is.** Captures what you changed in a draft the skill wrote, so the loop can learn from your edits. Every rewrite, cut, or addition becomes a record the improvement loop can mine.

**When to use it.** After you ship a piece the skill drafted, when your final version differs from what it handed you. The gap between draft and shipped is the signal.

**How to run it.** `/humanise learn` inside your agent. Give it the skill's draft and your shipped text. It runs `scripts/capture_edit.py`, which diffs the two sentence by sentence, classifies each changed span, and appends records to `profile/learning/ledger.jsonl`. For spans no automated check explains, the agent classifies the change against a fixed vocabulary (`too-even-rhythm`, `no-stance`, `too-generic`, `synonym-cycling`, `opener-template`, `register-miss`, `wrong-fact`, or `other:<slug>`).

**Reads / writes.** Reads the two texts. Appends to `profile/learning/ledger.jsonl` (the soul: your verbatim text, gitignored, never shipped). Mirrors durable corrections into session memory where the environment has a memory directory.

**Example.** The skill drafted an investor update; you cut "we are excited to share" and swapped a vague claim for a real number before sending. `/humanise learn` records both edits with their failure signature, then reports which signatures are approaching the promotion threshold (three occurrences makes a candidate).

See [memory-loop.md](../skill/references/memory-loop.md) for how the ledger feeds the loop.

---

## `improve`

**What it is.** Runs one full cycle of the self-improvement loop: benchmark the skill's output, run the blind voice test, mine the accumulated evidence for weaknesses, and gate any proposed engine change.

**When to use it.** Periodically, after `learn` has captured a batch of edits, or whenever you want to check whether the engine has a fixable weakness backed by evidence.

**How to run it.** `/humanise improve` inside your agent. Flags: `--baseline` also generates untreated comparison drafts; `--skip-benchmark` and `--skip-indist` run a partial cycle. The loop's rules live in `evals/self-harness-loop.md`; the command executes them.

**Reads / writes.** Reads `evals/evals.json`, your ledger, and your eligible corpus channels. Writes run artefacts to `profile/learning/runs/<timestamp>/` (gitignored), appends aggregate rows to `evals/indistinguishability-log.md`, and, for any change you accept, edits the named engine surface and adds a `CHANGELOG.md` entry.

**Example.** After a fortnight of `learn` captures, `/humanise improve` benchmarks every fixture, runs blind pairwise trials for each channel with two or more usable samples, clusters the evidence, and presents ranked proposals. You accept one; the command applies the smallest edit, runs the gate for its tier, and logs the change. An empty candidate set is a healthy result: the loop is running, evidence is still accumulating.

**Subagents.** `improve` orchestrates four of the five subagents: the [eval-generator](agents.md#eval-generator) drafts the benchmark and pairwise texts, the [indistinguishability-judge](agents.md#indistinguishability-judge) runs the blind voice test, the [improvement-proposer](agents.md#improvement-proposer) drafts bounded rule changes, and the [adversarial-reviewer](agents.md#adversarial-reviewer) reads any tier-3 change before it can land.
