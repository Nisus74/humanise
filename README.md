# humanise

[![version](https://img.shields.io/badge/version-1.0.0-E9764A)](https://github.com/Nisus74/humanise/releases) <!-- x-release-please-version -->
[![license](https://img.shields.io/badge/license-MIT-68B42E)](LICENSE)
[![CI](https://github.com/Nisus74/humanise/actions/workflows/ci.yml/badge.svg)](https://github.com/Nisus74/humanise/actions/workflows/ci.yml)

An open-source AI writing skill that preserves what you mean and learns how you write.

It combines a shared writing engine with private evidence from your real writing. The engine removes
generic model habits. Your profile teaches it what you notice, how you make a case, how you handle a
reader and where you stop.

Works with Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot and OpenCode.

If humanise improves something you would otherwise have sent, [star the repository](https://github.com/Nisus74/humanise).
Stars help other writers find it.

## See the difference

An untreated model might write:

<!--sweep-ignore-->
> In today's fast-paced landscape, onboarding isn't just about reducing friction, it's about creating
> a seamless and engaging journey that empowers users to unlock value.
<!--/sweep-ignore-->

humanise starts with the facts and the writer's judgement:

> We cut the signup form from nine fields to three last Tuesday. Activation moved from 41% to 58% in
> two weeks. The engineering was straightforward. Agreeing on what we could stop asking took longer.

The second version has a point, evidence and a decision a person actually made. It does not add fake
quirks or change the underlying claim.

## Install

Node 18 or later and Python 3 are required. Install humanise for your agent, then check the result:

```sh
npx humanise install --provider=codex
npx humanise doctor --provider=codex
```

Replace `codex` with `claude-code`, `cursor`, `gemini`, `github` or `opencode`. Personal scope is the
default, so your voice is available across projects. Add `--project` for one repository. The installer
refuses to guess when several supported agents are present, and `doctor` checks discovery and profile
privacy after installation.

Exact paths, native installers and invocation syntax are in [the platform guide](docs/platforms.md).

### Claude Code plugin

Claude Code users can install the repository as a marketplace plugin instead:

```text
/plugin marketplace add Nisus74/humanise
/plugin install humanise@humanise
/reload-plugins
```

Invoke the plugin skill with `/humanise:humanise` followed by a mode such as `rewrite` or `init`.

## Get your first result

Invoke the skill for your agent, then paste a paragraph and ask it to rewrite without changing the
meaning.

| Agent | Explicit invocation |
| --- | --- |
| Codex | `$humanise rewrite` |
| Claude Code, direct skill | `/humanise rewrite` |
| Claude Code, plugin | `/humanise:humanise rewrite` |
| Cursor | `/humanise rewrite` |
| Gemini CLI | Enable the skill, then ask normally |
| Copilot | `/humanise rewrite` where skills are supported |
| OpenCode | Ask normally or load the `humanise` skill |

No profile is required for the first rewrite. The generic engine will make the text cleaner without
pretending it already knows your voice.

## Make it sound like you

Ask humanise to set up your voice. The quick setup takes one real writing sample:

1. Paste something short you wrote and like.
2. Say what it was trying to do and who read it.
3. Choose between a close, direct and conversational rewrite.
4. Correct anything that does not feel like you.

That is enough for a provisional profile and a personalised result. Add more samples only for the
channels you use. Five to ten samples across several channels create a strong working profile.

Draft-to-final edit pairs are the best evidence. They teach humanise the difference between something
that could sound like you and something you would actually send.

Read [Getting started](docs/getting-started.md) for the walkthrough or [Voice setup](docs/SETUP.md) for
the deeper profile.

## Privacy

Your profile may contain emails, drafts and edit history. It is private by design:

- User-scope installs keep the profile under your home directory.
- Project installs add the profile and configuration to Git's local exclude file.
- `humanise doctor` checks installation and warns when a project profile is tracked.
- The local checker uses no model and no API key.

Review and redact samples before saving them. Do not put secrets, credentials or material you are not
allowed to share into a profile. See [Security](SECURITY.md) for reporting problems.

## How it works

Every draft follows the same order:

1. Preserve the point, facts, certainty, caveats and ask.
2. Model the relationship, reader state and stakes.
3. Prefer direct samples from the same channel and relationship.
4. Draft the content and argument before applying surface style.
5. Verify fidelity, voice and mechanical risks in that order.

The project keeps the shared engine and personal evidence separate:

- **Body:** `skill/SKILL.md`, commands and references. Shared and open source.
- **Soul:** `profile/`, including samples, decisions, negative examples and relationship overlays.
  Private to the writer.

Read [Body and soul](docs/body-and-soul.md) for the design.

## Modes

humanise is one skill with optional modes:

| Mode | Use it for |
| --- | --- |
| `init` | Start or deepen a private voice profile |
| `guide` | Draft new material |
| `rewrite` | Edit existing text at the right strength |
| `check` | Inspect mechanical and structural risks |
| `fingerprint` | Rebuild the evidence-backed voice model |
| `learn` | Capture the user's final edits |
| `improve` | Run the advanced engine improvement workflow |

See [Commands and modes](docs/commands.md) for examples.

## CLI

```text
humanise install --provider=<name> [--global|--project]
humanise doctor --provider=<name> [--global|--project]
humanise init [--provider=<name>] [--global|--project]
humanise detect <file> [dialect] [medium]
humanise voiceprint <file>
humanise voiceprint --build
humanise voiceprint --status
humanise build
```

Run any command as `npx humanise <command>`.

## Contributing

Good first contributions include a clearer installation step, a provider smoke test, a channel
playbook or a regional English pack. Engine changes need evidence and regression coverage. Personal
voice samples and edit history never belong in a pull request.

Start with [Contributing](CONTRIBUTING.md) and run `npm run quality` before opening a PR.

## Languages

humanise supports English today, with Australian, British and American guidance. Adding another
language needs native writing evidence, language-specific model tells, cultural calibration, checker
behaviour and fluent review. Read [Adding a language](docs/languages.md) before proposing one.

## Support humanise

Stars help people discover the project. Contributions improve the shared engine. If humanise has
saved you real editing time, you can also [buy me a coffee](https://buymeacoffee.com/Nisus74).

## FAQ

### Is humanise an AI detector bypass?

No. The goal is faithful writing in a specific person's voice. Detector scores are unreliable and
are not the product target.

### Does my writing get uploaded?

No. The bundled checker is local and uses no model or API key. The AI host you run humanise through
still has its own data policy, so review that separately.

## License

[MIT](LICENSE)
