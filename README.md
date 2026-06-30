# humanise

An open-source agent skill that makes AI-generated writing sound like a *specific human* wrote it rather than a generic one. Works with Claude Code, Cursor, Gemini CLI, Codex, Copilot, OpenCode, and Antigravity.

It does two things: it sweeps a draft for the tells that mark prose as AI-written, then it drafts from samples of your own writing so the result carries your voice. The detector is a Python checker you can run locally or in CI, with no model and no API key.

## See it

A model left to itself tends to write like this:

<!--sweep-ignore-->
> In today's fast-paced landscape, building a great product isn't just about writing code — it's about delighting your customers. We leveraged cutting-edge AI to deliver seamless, robust, and scalable solutions that move the needle. The result? A truly transformative experience that empowers teams to do their best work.

The checker flags the em dash, the slop words (`leverage`, `seamless`, `robust`, `scalable`), the `in today's fast-paced` opener, the binary contrast (`isn't just about X, it's about Y`), and the rule-of-three.
<!--/sweep-ignore-->



The same point, drafted in a specific person's voice:

> We shipped the new onboarding last Tuesday. Activation went from 41% to 58% in two weeks, mostly because we cut the signup form from nine fields to three. The engineering was the easy part. Talking ourselves into asking for less took longer.

Concrete numbers, an actual opinion, sentences of different lengths, no tells. The second version is what humanise produces once it has learned how you write.

## Body and soul

humanise keeps the universal part and the personal part separate.

- **The body (engine):** universal and shared, never personalised. The slop dictionary, the structural-tell detectors, the mechanical sweep, the eval suite: everyone runs the same body, because AI tells are model artefacts rather than personal taste.
- **The soul (profile):** entirely yours. `soul.md` (what you believe about writing and won't budge on), your voice fingerprint (how you actually write), your corpus (real samples), your dialect and absolute rules.

Fork the body. Keep your soul private. The fingerprint captures *how* you write; the soul captures *why*, and that point of view is the thing AI prose can't fake.

## Quick start (no setup, no API key)

The checker runs on its own, with no profile and no model. Clone the repo and point it at any file:

```
git clone https://github.com/Nisus74/humanise
cd humanise
node cli/bin/cli.js detect path/to/your-draft.md
```

It prints the tells it found and exits non-zero when a draft fails, so it drops straight into CI. You need Python 3 for the checker and Node 18+ for the CLI wrapper.

## Install into your agent

> The npm package and a Claude Code plugin are on the way. Until they land, install from a clone.

From the cloned repo:

```
npm run build                 # compile skill/ into dist/<provider>/
node cli/bin/cli.js install   # auto-detect your agent and copy the skill in
```

`install` detects your tool from its marker directory (`.claude`, `.cursor`, `.gemini`, `.agents`, `.github`, `.opencode`). Pass `--provider=<name>` to choose one explicitly (claude-code, cursor, gemini, codex, github for Copilot, opencode, universal), or `--global` to install into your home directory. Per-platform notes, including Gemini CLI and Antigravity, are in [docs/platforms.md](docs/platforms.md).

Then, inside your agent, run `/humanise init` for the guided voice setup.

## Set up your voice

Run `/humanise init` inside your agent. It helps you write your `soul.md` and collect 5 to 10 real samples of your writing, then builds your fingerprint from them. Budget about ten minutes. More samples sharpen the voice, and you can add them over time.

Your profile stays private. It lives in `profile/`, which is gitignored and never committed, and the checker runs fully on your machine with no network. Rewrite and guide mode use your own agent's model, the one you already run, so nothing goes anywhere new.

(The CLI's `humanise init` is a different, smaller thing: it only scaffolds the empty profile files. The guided walkthrough is the in-agent `/humanise init`.)

## Commands

One skill, a few verbs, run as `/humanise <command>` inside your agent:

- **init**: set up your voice profile (start here)
- **guide**: draft new content in your voice
- **rewrite**: rewrite existing AI text in your voice
- **check**: run the deterministic checker (no model)
- **fingerprint**: regenerate your voice fingerprint after adding samples

## CLI

```
node cli/bin/cli.js detect <file> [dialect] [medium]   # the checker; no model, no API key
node cli/bin/cli.js voiceprint <file>                  # score a draft's distance from your voice (advisory)
node cli/bin/cli.js voiceprint --build                 # build the voiceprint baseline from your samples
node cli/bin/cli.js init                               # scaffold the profile files
node cli/bin/cli.js build                              # rebuild dist/ from skill/
```

The voiceprint is the numeric companion to your fingerprint: the checker uses it to flag a draft that has drifted from how you usually write. It is advisory, never a target. Full walkthrough in [docs/SETUP.md](docs/SETUP.md).

## How it works

- `skill/SKILL.md` is the engine workflow: assess, draft from your corpus, two-pass sweep, self-critique, verify. It reads your `profile/` and `config.yml`.
- `skill/references/` is the universal knowledge: the slop dictionary, the structural tells, the channel playbooks, the dialect packs, plus tone and register.
- `skill/evals/` is the test suite: a Python assertion battery, a runnable `selftest.py`, the blind pairwise voice test, and the self-improvement loop.
- `skill/agents/` defines the subagents the workflow uses: an adversarial reviewer and a fact-and-brief checker for verification, plus a blind judge for the eval.
- `skill/profile/` is you.

## Repo layout

```
skill/                 the portable skill (drop into any agent)
  SKILL.md             engine workflow
  references/          universal engine knowledge (+ dialect-*.md)
  evals/               assertion battery, selftest, self-improvement loop
  agents/              adversarial-reviewer, fact-brief-checker, judge
  scripts/             voiceprint builder, fingerprint and corpus guides
  profile.template/    blank profile to copy
  profile.example/     a real, scrubbed profile to learn from
  config.example.yml   your settings
docs/                  setup, the body/soul explainer, per-platform install
scripts/               build and repo-check conveniences
.claude-plugin/        Claude Code plugin manifest
AGENTS.md / GEMINI.md  Codex and Gemini adapters
```

## Contributing

humanise improves through evidence-gated changes rather than opinion. An engine change is accepted only if it keeps `selftest.py` green and doesn't regress the held-out voice test; CI runs the suite on every PR. See [CONTRIBUTING.md](CONTRIBUTING.md) and `skill/evals/self-harness-loop.md`. Don't PR your personal voice into the engine; that's what your profile is for.

## License

[MIT](LICENSE)
