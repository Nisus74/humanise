# humanise

An open-source agent skill that makes AI-generated writing sound like a *specific human* wrote it, not a generic one. Works with Claude Code, Cursor, Gemini CLI, Codex, Copilot, and OpenCode.

humanise runs a two-pass sweep for the tells of AI prose (em dashes, slop words, binary contrasts, triples, fragment-colon drumbeats, and the rest), then drafts from your own writing so the output carries your voice. It ships a Python checker you can run in CI.

## Body and soul

humanise separates the two things that matter:

- **The body (engine):** universal, shared, never personalised. The slop dictionary, the structural-tell detectors, the mechanical sweep, the eval suite. AI tells are model artefacts, not personal taste, so everyone runs the same body.
- **The soul (profile):** entirely yours. `soul.md` (what you believe about writing and won't budge on), your voice fingerprint (how you actually write), your corpus (real samples), your dialect and absolute rules.

Fork the body. Transplant your soul. The fingerprint captures *how* you write; the soul captures *why*, and that point of view is the thing AI prose can't fake.

## Two ways to use it

- **Rewrite mode**: paste AI-generated text; the agent strips the tells and rewrites it in your voice.
- **Guide mode**: invoke before writing; the agent drafts in your voice from the start.

## Install

You need Node (for the CLI) and Python 3 (for the checker and voiceprint). From your project root:

```
npx humanise install
```

This auto-detects your agent (Claude Code, Cursor, Gemini CLI, Codex, Copilot, OpenCode) and copies the skill to the right place. Then run `/humanise init` inside your tool to set up your voice profile. That guided setup is distinct from `npx humanise init`, which only scaffolds the profile files.

Claude Code users can also install the plugin: `/plugin marketplace add Nisus74/humanise`. For a specific agent, `npx humanise install --provider=<name>` (claude-code, cursor, gemini, codex, github for Copilot, opencode, universal). Per-platform detail, including Gemini CLI and Antigravity, in [docs/platforms.md](docs/platforms.md).

Setting up a profile from a local clone instead? See [docs/DEVELOP.md](docs/DEVELOP.md).

## Commands

One skill, a few verbs (`/humanise <command>`):

- **init**: set up your voice profile (start here)
- **guide**: draft new content in your voice
- **rewrite**: rewrite AI text in your voice
- **check**: run the deterministic checker (no LLM)
- **fingerprint**: regenerate your voice fingerprint

## CLI

```
npx humanise detect <file> [dialect]   # deterministic checker, no LLM, no API key
npx humanise voiceprint <file>         # score a draft's distance from your voice (advisory)
npx humanise voiceprint --build        # build the voiceprint baseline from your corpus
npx humanise init                      # scaffold your profile
npx humanise build                     # rebuild dist/ from skill/
```

Full setup walkthrough in [docs/SETUP.md](docs/SETUP.md).

## How it works

- `skill/SKILL.md` is the engine workflow: assess, draft from your corpus, two-pass sweep, self-critique, verify. It reads your `profile/` and `config.yml`.
- `skill/references/` is the universal knowledge: slop dictionary, structural tells, channel playbooks, dialect packs, tone and register.
- `skill/evals/` is the test suite: a Python assertion battery, a runnable `selftest.py`, the pairwise indistinguishability protocol, and the self-improvement loop.
- `skill/agents/` defines the two subagents the workflow uses: an adversarial reviewer and a blind judge.
- `skill/profile/` is you.

## Repo layout

```
skill/                 the portable skill (drop into any agent)
  SKILL.md             engine workflow
  references/          universal engine knowledge (+ dialects/)
  evals/               assertion battery, selftest, self-improvement loop
  agents/              adversarial-reviewer, indistinguishability-judge
  scripts/             the fingerprint generator
  profile.template/    blank profile to copy
  profile.example/     a real, scrubbed profile to learn from
  config.example.yml   your settings
docs/                  setup, the body/soul explainer, per-platform install
scripts/               repo conveniences (run the checks)
tests/                 how to run the suite (CI runs it on every PR)
.claude-plugin/        Claude Code plugin manifest
AGENTS.md / GEMINI.md  Codex and Gemini adapters
```

## Contributing

humanise improves through evidence-gated changes, not opinion. An engine change is accepted only if it keeps `selftest.py` green and doesn't regress the held-out voice test; CI runs the suite on every PR. See [CONTRIBUTING.md](CONTRIBUTING.md) and `skill/evals/self-harness-loop.md`. Don't PR your personal voice into the engine; that's what your profile is for.

## License

[MIT](LICENSE)
