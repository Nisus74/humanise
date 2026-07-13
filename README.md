# humanise

humanise helps AI write like a specific person, without changing what that person means.

It combines a shared writing engine with private evidence from your real writing. The engine removes
generic model habits. Your profile teaches it what you notice, how you make a case, how you handle a
reader and where you stop.

Works with Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot and OpenCode.

## See the difference

An untreated model might write:

<!--sweep-ignore-->
> In today's fast-paced landscape, onboarding isn't just about reducing friction, it's about creating
> a seamless and engaging journey that empowers users to unlock value.
<!--/sweep-ignore-->

humanise starts with the facts and the writer's judgement:

> We cut the signup form from nine fields to three last Tuesday. Activation moved from 41% to 58% in
> two weeks. The engineering was straightforward. Agreeing on what we could stop asking took longer.

The improvement is not a collection of fake quirks. The second version has a point, evidence and a
decision a person actually made.

## Install

The npm package is not published yet, so install from the repository today:

```sh
git clone https://github.com/Nisus74/humanise.git
cd humanise
npm run build
```

Choose your agent. User scope is the default and keeps your voice available across projects:

```sh
node cli/bin/cli.js install --provider=codex
node cli/bin/cli.js install --provider=claude-code
node cli/bin/cli.js install --provider=cursor
node cli/bin/cli.js install --provider=gemini
node cli/bin/cli.js install --provider=github
node cli/bin/cli.js install --provider=opencode
```

Use `--project` only when the skill should apply to one repository. The installer protects the private
profile through Git's local exclude file. Run the diagnostic after installation:

```sh
node cli/bin/cli.js doctor --provider=codex
```

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

After the package is published, `npx humanise <command>` will run the same interface.

## Contributing

Improve the shared engine with evidence that generalises. Keep personal samples and edit history out
of pull requests. Start with [CONTRIBUTING.md](CONTRIBUTING.md) and [Development](docs/DEVELOP.md).

## License

[MIT](LICENSE)
