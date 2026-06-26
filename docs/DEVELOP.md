# Developing humanise

## Layout

- `skill/`: the source skill (SKILL.md, references, agents, evals, scripts, commands, profile.template, profile.example). This is what ships.
- `cli/`: the Node CLI (`bin/cli.js`) and the provider map (`providers.mjs`).
- `scripts/build.mjs`: compiles `skill/` into `dist/<provider>/<path>` for each target agent.
- `dist/`: generated build output (gitignored; built on demand and at publish).

## Build

```
npm run build        # or: node scripts/build.mjs
```

Emits `dist/<provider>/` for claude-code, cursor, gemini, codex, github, opencode, and universal. To add a provider: add a row to `cli/providers.mjs` (`PROVIDERS` path and a `DETECT` marker), then rebuild. The build is a copy with per-provider placement; the Python checker travels as-is, nothing is transpiled.

## Test

```
npm test             # runs the held-in selftest (Python)
```

The acceptance gate for engine changes is in `skill/evals/self-harness-loop.md`: the selftest stays green and the held-out voice test is not regressed. CI runs the selftest on every PR.

## CLI

```
npx humanise install [--provider=<name>] [--global]
npx humanise detect <file> [dialect] [medium]
npx humanise voiceprint <file>          # score a draft against your voice; --build builds the baseline
npx humanise init
npx humanise build
```

`install` auto-detects the agent from marker dirs (`.claude`, `.cursor`, `.gemini`, `.agents`, `.github`, `.opencode`); `--provider` overrides, `--global` installs into your home directory.

## Set up a profile from a clone

If you have cloned this repo and want to work on a profile in place (rather than installing the skill into another project via `npx humanise install`), build one under `skill/profile/`:

1. `cp -r skill/profile.template skill/profile` (or `skill/profile.example` to start from a real example).
2. Write `skill/profile/soul.md`: your convictions about writing. Concrete, first-person; `skill/profile.example/soul.md` shows the bar.
3. Drop 5 to 10 real writing samples into `skill/profile/voice-corpus/`, then run `skill/scripts/generate-fingerprint.md` to build your fingerprint (it also builds the voiceprint baseline).
4. `cp skill/config.example.yml skill/config.yml` and set your name, dialect, and channels.
5. Check the engine: `cd skill/evals/assertions && python3 selftest.py`.

`skill/profile/` is gitignored and never committed. Full walkthrough in [SETUP.md](SETUP.md).

## Release

- Bump `version` in `package.json`.
- `npm publish` (the `prepack` script rebuilds `dist/` into the published tarball).
- Tag the release once CI is green.
