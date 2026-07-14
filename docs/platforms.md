# Platforms

humanise uses the same skill on every host. Installation paths and invocation syntax differ.

## Path reference

| Host | Project skill | Personal skill | Explicit invocation |
| --- | --- | --- | --- |
| Codex | `.agents/skills/humanise` | `~/.agents/skills/humanise` | `$humanise` |
| Claude Code | `.claude/skills/humanise` | `~/.claude/skills/humanise` | `/humanise` |
| Cursor | `.cursor/skills/humanise` | `~/.cursor/skills/humanise` | `/humanise` |
| Gemini CLI | `.gemini/skills/humanise` | `~/.gemini/skills/humanise` | enable, then ask normally |
| GitHub Copilot | `.github/skills/humanise` | `~/.copilot/skills/humanise` | `/humanise` where supported |
| OpenCode | `.opencode/skills/humanise` | `~/.config/opencode/skills/humanise` | load or ask normally |

The installer uses personal scope by default. Add `--project` for the project path.

## Codex

```sh
npx humanise install --provider=codex
npx humanise doctor --provider=codex
```

Start a new task if the skill list was already loaded. Invoke `$humanise rewrite`, `$humanise guide`
or `$humanise init`. Codex may also select the skill automatically for writing tasks.

Opening this source repository in Codex is different from installing it. The root `AGENTS.md` applies
humanise to work on this repository; it does not install the skill for unrelated projects.

## Claude Code

For a direct personal skill:

```sh
npx humanise install --provider=claude-code
```

Invoke `/humanise rewrite` or let Claude select it from the request.

For the marketplace plugin:

```text
/plugin marketplace add Nisus74/humanise
/plugin install humanise@humanise
/reload-plugins
```

Plugin skills are namespaced. Invoke `/humanise:humanise rewrite`. Use the direct skill when you want
the simplest personal installation. Use the plugin when you want managed updates and marketplace
distribution. The plugin keeps its private profile in Claude's persistent plugin-data directory so an
update does not replace it.

## Cursor

```sh
npx humanise install --provider=cursor
```

Restart or reload the workspace if the skill does not appear. Invoke `/humanise rewrite` or ask Cursor
to use humanise.

## Gemini CLI and Antigravity

Use Gemini's native installer:

```sh
gemini skills install https://github.com/Nisus74/humanise
```

Or use the bundled installer:

```sh
npx humanise install --provider=gemini
```

Enable the skill in the session if required, then ask normally. The root `GEMINI.md` configures work
inside this source repository only.

## GitHub Copilot

```sh
npx humanise install --provider=github
```

This uses `.github/skills` for project scope and `~/.copilot/skills` for personal scope. GitHub's
`gh skill` commands are another option once this repository is published in a layout the command can
discover directly.

## OpenCode

```sh
npx humanise install --provider=opencode
```

OpenCode also recognises the shared `.agents/skills` locations, but the installer uses its native
paths so ownership is clear.

## Universal copy

If a host can read Agent Skills but has no adapter here, copy `skill/` into a supported skill directory
as `humanise/`. Confirm that the host discovers `SKILL.md`, supports the referenced files and can access
the private profile location.

## Troubleshooting

Run:

```sh
npx humanise doctor --provider=<name> [--project]
```

If several agent marker directories exist, the installer refuses to guess. Pass `--provider`
explicitly. If a skill was installed during an open session, restart, reload plugins or start a new
task so the host refreshes discovery.
