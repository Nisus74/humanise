# Platforms

Humanise uses the same writing skill on every host. The install path and the way you invoke it differ.

## Path reference

| Host | Installer provider | Project install | Personal install | Invoke |
| --- | --- | --- | --- | --- |
| Codex | `codex` | `.agents/skills/humanise` | `~/.agents/skills/humanise` | `$humanise` |
| Claude Code | `claude-code` | `.claude/skills/humanise` | `~/.claude/skills/humanise` | `/humanise` |
| Cursor | `cursor` | `.cursor/skills/humanise` | `~/.cursor/skills/humanise` | `/humanise` |
| Gemini CLI | `gemini` | `.gemini/skills/humanise` | `~/.gemini/skills/humanise` | enable, then ask |
| GitHub Copilot | `github` | `.github/skills/humanise` | `~/.copilot/skills/humanise` | `/humanise` where supported |
| OpenCode | `opencode` | `.opencode/skills/humanise` | `~/.config/opencode/skills/humanise` | ask it to use humanise |
| Antigravity | `antigravity` (next npm release) | `.agents/skills/humanise` | `~/.gemini/config/skills/humanise` | mention humanise by name |
| Other Agent Skills hosts | `universal` | `humanise` | `~/.agents/skills/humanise` | ask the agent to use humanise |

The installer uses personal scope by default. Add `--project` to install for the current repository.
The commands below pin the released npm package so they produce the documented 1.0.0 setup.

## Codex

```sh
npx humanise@1.0.0 install --provider=codex
npx humanise@1.0.0 doctor --provider=codex
```

Start a new task if Humanise does not appear after installation. Invoke `$humanise rewrite`,
`$humanise guide` or `$humanise init`. Codex may also select the skill automatically for a matching
writing request. See the [official Codex skills guide](https://learn.chatgpt.com/docs/build-skills).

Opening this source repository in Codex is different from installing it. This repository's
`AGENTS.md` applies Humanise here, but does not install it for other work.

## Claude Code

For a direct personal skill:

```sh
npx humanise@1.0.0 install --provider=claude-code
npx humanise@1.0.0 doctor --provider=claude-code
```

Invoke `/humanise rewrite`, or let Claude select the skill from your request. See the
[official Claude Code skills guide](https://code.claude.com/docs/en/skills).

For the marketplace plugin:

```text
/plugin marketplace add Nisus74/humanise
/plugin install humanise@humanise
/reload-plugins
```

Invoke `/humanise:humanise rewrite`. The direct skill is the simpler personal installation. The
plugin provides managed updates and keeps its private profile in Claude's persistent
`${CLAUDE_PLUGIN_DATA}` directory.

## Cursor

```sh
npx humanise@1.0.0 install --provider=cursor
npx humanise@1.0.0 doctor --provider=cursor
```

Reload the workspace if Humanise does not appear. Invoke `/humanise rewrite`, or ask Cursor to use
Humanise. See the [official Cursor skills guide](https://cursor.com/docs/skills).

## Gemini CLI

Use the Humanise installer:

```sh
npx humanise@1.0.0 install --provider=gemini
npx humanise@1.0.0 doctor --provider=gemini
```

Gemini also has a native installer:

```sh
gemini skills install https://github.com/Nisus74/humanise
```

Run `/skills reload` if the session was already open. Enable Humanise if prompted, then ask Gemini to
use it for the writing task. See the
[official Gemini CLI skills guide](https://geminicli.com/docs/cli/using-agent-skills/).

## GitHub Copilot

Use the Humanise installer:

```sh
npx humanise@1.0.0 install --provider=github
npx humanise@1.0.0 doctor --provider=github
```

The Humanise installer uses `.github/skills` for project scope and `~/.copilot/skills` for personal
scope.

## OpenCode

```sh
npx humanise@1.0.0 install --provider=opencode
npx humanise@1.0.0 doctor --provider=opencode
```

The installer uses OpenCode's native paths. Ask OpenCode to use Humanise for your writing task. See the
[official OpenCode skills guide](https://opencode.ai/docs/skills).

## Antigravity

For npm 1.0.0, install the universal package that Antigravity can discover:

```sh
npx humanise@1.0.0 install --provider=universal
```

Antigravity discovers the resulting `~/.agents/skills/humanise` directory. To make the same installation
available to Antigravity CLI through its shared global directory, copy it once:

```sh
mkdir -p ~/.gemini/config/skills
cp -R ~/.agents/skills/humanise ~/.gemini/config/skills/humanise
```

The npm 1.0.0 package predates the explicit `antigravity` provider. This branch adds it for the next npm
release, using Antigravity's global `~/.gemini/config/skills/humanise` path. These locations follow
Google's [official Antigravity skills guide](https://codelabs.developers.google.com/getting-started-with-antigravity-skills).

## Universal install

For another host that supports Agent Skills:

```sh
npx humanise@1.0.0 install --provider=universal
npx humanise@1.0.0 doctor --provider=universal
```

This installs Humanise in the shared personal Agent Skills directory. If your host uses a different
directory, copy the installed `humanise/` folder there and confirm it discovers `SKILL.md`.

## Troubleshooting

Run the matching diagnostic:

```sh
npx humanise@1.0.0 doctor --provider=<name> [--project]
```

If several agent marker directories exist, the installer refuses to guess. Pass `--provider`
explicitly. If you installed during an open session, restart the task, reload plugins or refresh the
host's skill list.
