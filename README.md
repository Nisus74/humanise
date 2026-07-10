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

## Getting started

New to agent skills? The full walkthrough is in [docs/getting-started.md](docs/getting-started.md). The short version is three steps.

**1. Try the checker (no install, no profile, no model).**

```
git clone https://github.com/Nisus74/humanise
cd humanise
node cli/bin/cli.js detect path/to/your-draft.md
```

It prints the tells it found and exits non-zero when a draft fails, so it drops straight into CI. You need Python 3 for the checker and Node 18+ for the CLI wrapper.

**2. Install it into your agent.**

```
npm run build                 # compile skill/ into dist/<provider>/
node cli/bin/cli.js install   # auto-detect your agent and copy the skill in
```

`install` detects your tool from its marker directory (`.claude`, `.cursor`, `.gemini`, `.agents`, `.github`, `.opencode`). Pass `--provider=<name>` to choose one explicitly (claude-code, cursor, gemini, codex, github for Copilot, opencode, universal), or `--global` to install into your home directory. Per-platform notes, including the Claude Code plugin and Antigravity, are in [docs/platforms.md](docs/platforms.md).

**3. Set up your voice, then write.** Inside your agent, run `/humanise init` for the guided setup: your `soul.md` plus five to ten real samples, then your fingerprint, in about ten minutes. Then `/humanise guide` to draft something new or `/humanise rewrite` to fix existing text.

Your profile stays private. It lives in `profile/`, which is gitignored and never committed, and the checker runs fully on your machine with no network.

> The npm package and a Claude Code plugin are on the way. Until they land, install from a clone as above.

## Body and soul

humanise keeps the universal part and the personal part separate.

- **The body (engine):** universal and shared, never personalised. The slop dictionary, the structural-tell detectors, the mechanical sweep, the eval suite: everyone runs the same body, because AI tells are model artefacts rather than personal taste.
- **The soul (profile):** entirely yours. `soul.md` (what you believe about writing and won't budge on), your voice fingerprint (how you actually write), your corpus (real samples), your dialect and absolute rules.

Fork the body. Keep your soul private. The fingerprint captures *how* you write; the soul captures *why*, and that point of view is the thing AI prose can't fake. More in [docs/body-and-soul.md](docs/body-and-soul.md).

## Commands

Run these as `/humanise <command>` inside your agent. Full detail and worked examples are in [docs/commands.md](docs/commands.md).

| Command | What it does | Group |
| --- | --- | --- |
| `init` | Set up your voice profile (start here) | Setup |
| `fingerprint` | Rebuild your voice fingerprint after adding samples | Setup |
| `guide` | Draft new content in your voice | Everyday |
| `rewrite` | Rewrite existing AI text in your voice | Everyday |
| `check` | Run the deterministic checker (no model) | Everyday |
| `learn` | Capture what you changed in a shipped draft | Self-improvement |
| `improve` | Run one cycle of the self-improvement loop | Self-improvement |

## CLI

```
node cli/bin/cli.js install [--provider=<name>] [--global]   install the skill into your agent
node cli/bin/cli.js detect <file> [dialect] [medium]         the checker; no model, no API key
node cli/bin/cli.js voiceprint <file>                        score a draft's distance from your voice (advisory)
node cli/bin/cli.js voiceprint --build                       build the voiceprint baseline from your samples
node cli/bin/cli.js voiceprint --status                      corpus counts and voiceprint state per channel
node cli/bin/cli.js init                                     scaffold the profile files
node cli/bin/cli.js build                                    rebuild dist/ from skill/
```

Once published, `npx humanise <verb>` runs the same commands. The voiceprint is the numeric companion to your fingerprint: the checker uses it to flag a draft that has drifted from how you usually write. It is advisory, never a target. Full walkthrough in [docs/SETUP.md](docs/SETUP.md).

## How it works

- `skill/SKILL.md` is the engine workflow: assess, draft from your corpus, two-pass sweep, self-critique, verify. It reads your `profile/` and `config.yml`.
- `skill/commands/` holds the `/humanise` verbs. `skill/references/` is the universal knowledge: the slop dictionary, the structural tells, the channel playbooks, the dialect packs, plus tone and register.
- `skill/evals/` is the test suite: a Python assertion battery, a runnable `selftest.py`, the blind pairwise voice test, the reserved holdout set, and the self-improvement loop.
- `skill/agents/` are the subagents the workflow spawns: an adversarial reviewer and a fact-and-brief checker that gate a draft before it ships, plus the three that run the loop (an eval generator, a blind voice judge, and a rule-change proposer). Reference in [docs/agents.md](docs/agents.md).
- The loop is code you can run. `/humanise learn` captures your real edits into a ledger; `/humanise improve` runs a full cycle (benchmark, blind voice test, mine, propose) behind a regression gate. See [docs/DEVELOP.md](docs/DEVELOP.md).
- `skill/profile/` is you.

## Repo layout

```
skill/                 the portable skill (drop into any agent)
  SKILL.md             engine workflow
  commands/            the /humanise verbs (init, guide, rewrite, check, fingerprint, learn, improve)
  references/          universal engine knowledge (+ dialect-*.md)
  evals/               assertion battery, selftest, holdout set, self-improvement loop
  agents/              verification agents (reviewer, fact-checker) + loop agents (generator, judge, proposer)
  scripts/             voiceprint builder, edit capture, fingerprint and corpus guides
  profile.template/    blank profile to copy
  profile.example/     a real, scrubbed profile to learn from
  config.example.yml   your settings
docs/                  getting started, setup, commands, subagents, body/soul, platforms, develop
scripts/               build and repo-check conveniences
.claude-plugin/        Claude Code plugin manifest
AGENTS.md / GEMINI.md  Codex and Gemini adapters
```

## Contributing

humanise improves through evidence-gated changes rather than opinion. An engine change is accepted only if it keeps `selftest.py` green and doesn't regress the held-out voice test; CI runs the suite on every PR. See [CONTRIBUTING.md](CONTRIBUTING.md) and `skill/evals/self-harness-loop.md`. Don't PR your personal voice into the engine; that's what your profile is for.

## License

[MIT](LICENSE)
