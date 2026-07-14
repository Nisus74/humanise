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

## Start here

humanise is an Agent Skill: a folder of instructions and supporting files that your AI coding agent can
load when you ask it to write or edit. Installing it copies that folder into a directory your agent
already checks. It does not create another account, run a background service or upload your writing.

### 1. Check the requirements

You need Node.js 18 or later. Python 3 runs the local writing checker and voice tools.

```sh
node --version
python3 --version
```

### 2. Choose your agent

| Agent | Provider name | Invoke after installation |
| --- | --- | --- |
| Codex | `codex` | `$humanise rewrite` |
| Claude Code, direct skill | `claude-code` | `/humanise rewrite` |
| Cursor | `cursor` | `/humanise rewrite` |
| Gemini CLI | `gemini` | Enable the skill, then ask normally |
| GitHub Copilot | `github` | `/humanise rewrite` where supported |
| OpenCode | `opencode` | Ask it to use humanise |
| Antigravity | Native GitHub CLI install | Mention humanise by name |
| Another Agent Skills host | `universal` | Ask it to use humanise |

### 3. Install and check it

This example installs humanise for Codex in your personal skill directory. Replace `codex` with the
provider name from the table.

```sh
npx humanise@1.0.0 install --provider=codex
npx humanise@1.0.0 doctor --provider=codex
```

Personal scope is the default and works across projects. Add `--project` to both commands when the
skill belongs to one repository.

### 4. Get one result before configuring anything

Open or refresh your agent, invoke humanise in `rewrite` mode and paste a paragraph. Ask it to preserve
the point and facts. A profile is optional for this first pass. Humanise uses conservative engine
defaults and does not pretend the result already sounds like you.

### 5. Create your private profile

```sh
npx humanise@1.0.0 init --provider=codex
```

Then invoke humanise in `init` mode. Paste one short, redacted piece you wrote and like. Tell it who read
the piece and what you wanted it to achieve. Choose the closest rewrite and correct anything that feels
wrong.

### 6. Confirm the personalised result

Run the same rewrite again. The second result should preserve the same meaning while reflecting the
decisions in your sample. Run `doctor` once more to confirm the profile path and privacy state.

Follow the complete [Getting started guide](https://github.com/Nisus74/humanise/blob/main/docs/getting-started.md)
for every provider, configuration fields, expected output and troubleshooting. Exact host paths and
native installers are in the [platform guide](https://github.com/Nisus74/humanise/blob/main/docs/platforms.md).

### Claude Code marketplace plugin

Claude Code users can install the repository as a marketplace plugin instead:

```text
/plugin marketplace add Nisus74/humanise
/plugin install humanise@humanise
/reload-plugins
```

Invoke the plugin with `/humanise:humanise rewrite` or `/humanise:humanise init`.

## Privacy

Your profile may contain emails, drafts and edit history. It is private by design:

- User-scope installs keep the profile under your home directory.
- Project installs add the profile and configuration to Git's local exclude file.
- `humanise doctor` checks installation and warns when a project profile is tracked.
- The local checker uses no model and no API key.

Review and redact samples before saving them. Do not put secrets, credentials or material you are not
allowed to share into a profile. See [Security](https://github.com/Nisus74/humanise/blob/main/SECURITY.md)
for reporting problems.

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

No. The bundled checker is local and uses no model or API key. The AI host you run humanise through
still has its own data policy, so review that separately.

## License

[MIT](LICENSE)
