# humanise

[![version](https://img.shields.io/badge/version-1.0.0-E9764A)](https://github.com/Nisus74/humanise/releases) <!-- x-release-please-version -->
[![license](https://img.shields.io/badge/license-MIT-68B42E)](LICENSE)
[![CI](https://github.com/Nisus74/humanise/actions/workflows/ci.yml/badge.svg)](https://github.com/Nisus74/humanise/actions/workflows/ci.yml)

## Your AI should write like you, not like AI.

An open-source Agent Skill that preserves what you mean and learns how you write from real examples.

Humanise is for people who use AI to draft or edit important writing and want the result to reflect
their judgement, evidence and voice. Your agent loads the skill when you ask it to write. Humanise
protects the point, facts and level of certainty before it changes the style.

### Install for Codex

You need Node.js 18 or later. Python 3 runs the local writing checker and voice tools.

```sh
npx humanise@1.0.0 install --provider=codex
npx humanise@1.0.0 doctor --provider=codex
```

Start a new Codex task and invoke `$humanise rewrite`. [See the illustrative example](#illustrative-example),
follow the [complete getting-started guide](https://github.com/Nisus74/humanise/blob/main/docs/getting-started.md),
or check the [compatibility evidence](https://github.com/Nisus74/humanise/blob/main/docs/compatibility.md).

## Illustrative example

The example below is illustrative. It was not produced from a recorded reproducible run, and the
figures are part of the example. In real use, every fact must come from the writer's brief or source.

An untreated model might write:

<!--sweep-ignore-->
> In today's fast-paced landscape, onboarding isn't just about reducing friction, it's about creating
> a seamless and engaging journey that empowers users to unlock value.
<!--/sweep-ignore-->

humanise starts with the facts and the writer's judgement:

> We cut the signup form from nine fields to three last Tuesday. Activation moved from 41% to 58% in
> two weeks. The engineering was straightforward. Agreeing on what we could stop asking took longer.

The intended difference is a specific point supported by supplied evidence. Humanise is instructed to
preserve the writer's meaning and never invent detail to make the prose feel more human.

## What makes Humanise different

- **Preserves meaning before changing style.** The point and facts come first, along with certainty,
  caveats and the ask.
- **Learns from real writing evidence.** Samples and draft-to-final edits show Humanise how your
  judgement and word choices work together.
- **Models the reader and relationship.** The same writer should sound different with a regulator, a
  colleague or a close collaborator.
- **Stores the profile locally.** Your samples, decisions and voice profile stay in the installed skill
  directory on your machine.

## Start with one result

A profile is optional for the first rewrite. Humanise uses conservative engine defaults and does not
pretend it already knows your voice. When you are ready to personalise it, initialise a local profile:

```sh
npx humanise@1.0.0 init --provider=codex
```

The [getting-started guide](https://github.com/Nisus74/humanise/blob/main/docs/getting-started.md)
covers configuration, one-sample calibration, expected output and troubleshooting without assuming
you already know how Agent Skills work.

### Claude Code marketplace plugin

Claude Code users can install the repository as a marketplace plugin instead:

```text
/plugin marketplace add Nisus74/humanise
/plugin install humanise@humanise
/reload-plugins
```

Invoke the plugin with `/humanise:humanise rewrite` or `/humanise:humanise init`.

## Privacy

Your profile is stored locally. Humanise itself does not upload it, although the AI host you use still has its own data policy.

Profiles may contain emails, drafts and edit history:

- User-scope installs keep the profile under your home directory.
- Project installs add the profile and configuration to Git's local exclude file.
- `humanise doctor` checks installation and warns when a project profile is tracked.
- The local checker uses no model and no API key.

Review and redact samples before saving them. Do not put secrets, credentials or material you are not
allowed to share into a profile. See [Security](https://github.com/Nisus74/humanise/blob/main/SECURITY.md)
for reporting problems.

## How it works

Every draft follows the same order:

1. Preserve the point and facts, the level of certainty, the caveats and the ask.
2. Model the relationship, reader state and stakes.
3. Prefer direct samples from the same channel and relationship.
4. Draft the content and argument before applying surface style.
5. Verify fidelity, voice and mechanical risks in that order.

The project keeps the shared engine and personal evidence separate:

- **Body:** `skill/SKILL.md`, commands and references. Shared and open source.
- **Soul:** `profile/`, including samples, decisions, negative examples and relationship overlays.
  Private to the writer.

Read [Body and soul](https://github.com/Nisus74/humanise/blob/main/docs/body-and-soul.md) for the design.

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

See [Commands and modes](https://github.com/Nisus74/humanise/blob/main/docs/commands.md) for examples.

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

Start with [Contributing](https://github.com/Nisus74/humanise/blob/main/CONTRIBUTING.md) and run
`npm run quality` before opening a PR.

## Languages

humanise supports English today, with Australian, British and American guidance. Adding another
language needs native writing evidence, language-specific model tells, cultural calibration, checker
behaviour and fluent review. Read [Adding a language](https://github.com/Nisus74/humanise/blob/main/docs/languages.md)
before proposing one.

## Support humanise

Stars help people discover the project. Contributions improve the shared engine. If humanise has
saved you real editing time, you can also [buy me a coffee](https://buymeacoffee.com/Nisus74).

## FAQ

### Is humanise an AI detector bypass?

No. The goal is faithful writing in a specific person's voice. Detector scores are unreliable and
are not the product target.

### Does my writing get uploaded?

Humanise itself does not upload your profile. The bundled checker is local and uses no model or API
key. The AI host you use still has its own data policy, so review that separately.

## License

[MIT](LICENSE)
