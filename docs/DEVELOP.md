# Developing humanise

## Layout

- `skill/`: the source skill. This is what ships. The folder is named `skill/` in the repo but builds and installs as `humanise/` (matching the `name` in SKILL.md), so the shipped skill satisfies the spec's name-matches-directory rule. Validate the built artifact rather than the source.
- `cli/`: the Node CLI (`bin/cli.js`) and the provider map (`providers.mjs`).
- `scripts/build.mjs`: compiles `skill/` into `dist/<provider>/<path>` for each target agent.
- `dist/`: generated build output (gitignored; built on demand and at publish).

## Build

```
npm run build        # or: node scripts/build.mjs
```

Emits a `dist/<provider>/` for every supported agent (claude-code, cursor, gemini, codex, github, opencode, universal). To add a provider: add a row to `cli/providers.mjs` (`PROVIDERS` path and a `DETECT` marker), then rebuild. The build is a copy with per-provider placement; the Python checker travels as-is, nothing is transpiled.

## Validate

```
npm run validate     # check the built dist/ against the Agent Skills spec
```

Run after `npm run build`. For each built `humanise/` it enforces the spec's hard rules:

- the SKILL.md frontmatter is present and parses,
- the `name` is lowercase-hyphenated and matches its directory,
- the `description` stays within 1024 characters.

Advisory warnings (which never fail the run) fire when SKILL.md goes over the ~5,000-token or 500-line progressive-disclosure budget, or when a folder sits more than one level deep. It checks the built artifact under `dist/`; running `skills-ref validate ./skill` on the source would flag that the folder is `skill/` rather than `humanise/`. `prepack` runs build then validate, so a publish can't ship a spec regression. Zero dependencies (Node built-ins), like `check:deps`.

## Test

```
npm test             # runs the held-in selftest (Python)
```

The acceptance gate for engine changes is in `skill/evals/self-harness-loop.md`: the selftest stays green and the held-out voice test is not regressed. CI runs the selftest on every PR.

## Run the loop

The self-improvement loop is runnable, not just documented. `/humanise learn` (inside your agent) diffs a shipped text against the skill's draft with `skill/scripts/capture_edit.py` and appends failure-signature records to `skill/profile/learning/ledger.jsonl`. `/humanise improve` runs a full cycle: generator subagents draft every `evals.json` fixture (optionally an untreated baseline too), `run_all.py` grades them, `pairwise_trial.py` runs the blind indistinguishability trials for any channel with two or more usable samples, `mine_weaknesses.py` clusters everything at or past three occurrences into `candidates.json`, and a proposer subagent drafts bounded edits that still clear the tiered gate before anything ships.

Two hard rules. `skill/evals/holdout-evals.json` is reserved held-out: never tune a change against it, never draft to its assertions. And everything under `skill/profile/learning/` is soul: it holds your verbatim text and run transcripts, stays gitignored, and never appears in `dist/`; only aggregate rows land in the committed `evals/indistinguishability-log.md`.

## CLI

```
npx humanise install [--provider=<name>] [--global]
npx humanise detect <file> [dialect] [medium]
npx humanise voiceprint <file>          # score a draft against your voice; --build builds the baseline
npx humanise voiceprint --status        # per-channel corpus counts, pairwise-test eligibility, baseline freshness
npx humanise init
npx humanise build
```

`install` auto-detects the agent from marker dirs (`.claude`, `.cursor`, `.gemini`, `.agents`, `.github`, `.opencode`); `--provider` overrides, `--global` installs into your home directory.

## Set up a profile from a clone

If you have cloned this repo and want to work on a profile in place (rather than installing the skill into another project via `npx humanise install`), build one under `skill/profile/`:

1. `cp -r skill/profile.template skill/profile` (or `skill/profile.example` to start from a real example).
2. Write `skill/profile/soul.md`: your convictions about writing. Concrete, first-person; `skill/profile.example/soul.md` shows the bar.
3. Drop 5 to 10 real writing samples into `skill/profile/` as flat `sample-<channel>-<slug>.md` files, then run `skill/scripts/generate-fingerprint.md` to build your fingerprint (it also builds the voiceprint baseline).
4. `cp skill/config.example.yml skill/config.yml` and set your name, dialect and channels.
5. Check the engine: `cd skill/evals/assertions && python3 selftest.py`.

`skill/profile/` is gitignored and never committed. Full walkthrough in [SETUP.md](SETUP.md).

## Release

- Bump `version` in `package.json`.
- `npm run validate` passes (also runs automatically in `prepack`).
- `npm publish` (the `prepack` script rebuilds `dist/` and validates it before packing the tarball).
- Tag the release once CI is green.
