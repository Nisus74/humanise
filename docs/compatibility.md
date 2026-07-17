# Compatibility and installation evidence

This page records checks completed on 14 July 2026. A successful installer smoke test proves that
Humanise reached the expected directory with its required files. It does not prove that a host selected
the skill or completed a writing request. The status column keeps that distinction explicit.

The package checks used a local `humanise-1.0.0.tgz` produced from this working tree. They did not
download the published npm release. The skills CLI check fetched the repository's default branch from
GitHub. See [Platforms](platforms.md) for the normal installation instructions.

| Host | Installation method | Invocation | Last tested date | Operating system | Host or CLI version | Status | Known limitations | Evidence or test command |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Codex | npm CLI; skills CLI | `$humanise` | 2026-07-14 | macOS 26.5.2, arm64 | Codex CLI 0.144.3; skills 1.5.17 | Package install, `doctor`, skill name and supporting files verified. Host invocation was not run. | The Codex host did not select the skill or perform a rewrite. The skills CLI fetched GitHub rather than the npm artefact. | `npm run test:package`; isolated `npx skills add Nisus74/humanise --global --agent codex --skill humanise --yes --copy` |
| Claude Code | npm CLI; Claude marketplace manifest | `/humanise`; plugin: `/humanise:humanise` | 2026-07-14 | macOS 26.5.2, arm64 | Claude Code 2.1.209 | Package install and `doctor` passed. The plugin manifest validated. Host invocation was not run. | Marketplace installation, plugin reload and a writing request were not run. Manifest validation alone does not prove runtime discovery. | `npm run test:package`; `claude plugin validate .` |
| Cursor | npm CLI | `/humanise` | 2026-07-14 | macOS 26.5.2, arm64 | Cursor 3.8.23 | Repository installer smoke test passed at personal and project scope. Host invocation was not run. | The packaged artefact and Cursor discovery were not tested separately for this host. | `node --test --test-name-pattern=cursor tests/cli-install.test.mjs` |
| Gemini CLI | npm CLI; native installer documented | Enable Humanise, then ask normally | 2026-07-14 | macOS 26.5.2, arm64 | Not installed | Repository installer smoke test passed at personal and project scope. Host invocation was not run. | Gemini CLI and its native installer were unavailable, so discovery and invocation were not tested. | `node --test --test-name-pattern=gemini tests/cli-install.test.mjs` |
| GitHub Copilot | npm CLI | `/humanise` where supported | 2026-07-14 | macOS 26.5.2, arm64 | gh 2.95.0; Copilot host not run | Repository installer smoke test passed at personal and project scope. Host invocation was not run. | The native installer remains unsuitable for this release: the prior authenticated v1.0.0 smoke test installs the skill as `skill`, not `humanise`. That native check was not rerun here. | `node --test --test-name-pattern=github tests/cli-install.test.mjs`; prior command: `gh skill install Nisus74/humanise skill/SKILL.md --pin v1.0.0 --force` |
| OpenCode | npm CLI | Ask OpenCode to use Humanise | 2026-07-14 | macOS 26.5.2, arm64 | Not installed | Repository installer smoke test passed at personal and project scope. Host invocation was not run. | OpenCode discovery and invocation were not tested. | `node --test --test-name-pattern=opencode tests/cli-install.test.mjs` |
| Antigravity | npm 1.0.0: `universal`; unreleased branch: `antigravity` | Mention Humanise by name | 2026-07-14 | macOS 26.5.2, arm64 | Not installed | Repository provider smoke test passed. The released fallback and host invocation were not run in this change. | npm 1.0.0 uses `universal`. The unreleased branch adds `antigravity`; do not treat that provider as released until a later package is published. | `node --test --test-name-pattern=antigravity tests/cli-install.test.mjs` |
| Universal Agent Skills hosts | npm CLI with `universal` | Ask the host to use Humanise | 2026-07-14 | macOS 26.5.2, arm64 | No host selected | Repository installer smoke test passed at personal and project scope. Host invocation was not run. | Hosts choose their own discovery paths and invocation behaviour. A generic directory copy cannot verify every compatible host. | `node --test --test-name-pattern=universal tests/cli-install.test.mjs` |

## What the package test checks

`npm run test:package` creates a tarball and installs it into a temporary consumer project. Codex and
Claude Code installations then run inside separate temporary home directories. The test confirms:

- the package and skill are both named `humanise`;
- `SKILL.md` is discoverable at each documented personal path;
- the rewrite command, meaning rules, profile template and configuration template are present;
- `humanise doctor` passes for both priority hosts;
- no filled `profile/`, private `config.yml`, Python cache or bytecode is packaged.

The test removes its temporary directory afterwards. It never writes to the user's real skill
directories.

## Live checks and skips

The following live commands ran successfully on 14 July 2026:

```sh
claude plugin validate .
npx skills --help
npx skills add Nisus74/humanise --global --agent codex --skill humanise --yes --copy
```

The skills CLI commands used an isolated temporary home. The installed skill reported
`name: humanise`, included its commands, references and templates, and contained no filled private
profile.

No writing request was run inside Codex, Claude Code, Cursor or another host. Gemini CLI, OpenCode and
Antigravity were not installed. Those checks remain unverified rather than being inferred from file
placement.
