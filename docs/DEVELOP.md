# Developing humanise

## Layout

- `skill/`: the source skill. This is what ships. The folder is named `skill/` in the repo but builds and installs as `humanise/` (matching the `name` in SKILL.md), so the shipped skill satisfies the spec's name-matches-directory rule. Validate the built artifact rather than the source.
- `cli/`: the Node CLI (`bin/cli.js`) and the provider map (`providers.mjs`).
- `scripts/build.mjs`: compiles `skill/` into the portable `dist/humanise` artefact and the Claude
  plugin layout.
- `dist/`: generated build output (gitignored; built on demand and at publish).

## Build

```
npm run build        # or: node scripts/build.mjs
```

Emits one `dist/humanise` artefact for every direct skill install. To add a provider, define its
separate project and personal paths, discovery markers and invocation text in `cli/providers.mjs`.
The installer applies the destination path, so identical provider copies do not inflate the package.

## Validate

```
npm run validate     # check the built dist/ against the Agent Skills spec
```

Run after `npm run build`. For each built `humanise/` it enforces the spec's hard rules:

- the SKILL.md frontmatter is present and parses,
- the `name` is lowercase-hyphenated and matches its directory,
- the `description` stays within 1024 characters.

Advisory warnings (which never fail the run) fire when SKILL.md goes over the ~5,000-token or 500-line progressive-disclosure budget, or when a folder sits more than one level deep. It checks the built artifact under `dist/`; running `skills-ref validate ./skill` on the source would flag that the folder is `skill/` rather than `humanise/`. `prepack` runs the build, validation and package privacy check. Zero dependencies (Node built-ins), like `check:deps`.

## Package privacy

```sh
npm run check:package-privacy
```

The release fails if the npm whitelist includes the source `skill/` tree or a built artefact contains a
filled profile, `config.yml`, bytecode or a cache directory. The package ships sanitised `dist/`
artefacts only.

## Test

```sh
npm test
```

This builds the distributable skill, runs the Node tests for provider mapping, installation, privacy
and onboarding documentation, then runs the held-in Python engine selftest.

The acceptance gate for engine changes is in `skill/evals/self-harness-loop.md`: the selftest stays green and the held-out voice test is not regressed. CI runs the selftest on every PR.

## Run the loop

The self-improvement loop is runnable, not just documented. `/humanise learn` (inside your agent) diffs a shipped text against the skill's draft with `skill/scripts/capture_edit.py` and appends failure-signature records to `skill/profile/learning/ledger.jsonl`. `/humanise improve` runs a full cycle: generator subagents draft every `evals.json` fixture (optionally an untreated baseline too), `run_all.py` grades them, `pairwise_trial.py` runs the blind indistinguishability trials for any channel with two or more usable samples, `mine_weaknesses.py` clusters everything at or past three occurrences into `candidates.json`, and a proposer subagent drafts bounded edits that still clear the tiered gate before anything ships.

Two hard rules. `skill/evals/holdout-evals.json` is reserved held-out: never tune a change against it, never draft to its assertions. And everything under `skill/profile/learning/` is soul: it holds your verbatim text and run transcripts, stays gitignored, and never appears in `dist/`; only aggregate rows land in the committed `evals/indistinguishability-log.md`.

The subagents this loop spawns (the generator, the blind judge, the proposer) are documented in [agents.md](agents.md).

## CLI

```
npx humanise install --provider=<name> [--global|--project]
npx humanise doctor --provider=<name> [--global|--project]
npx humanise detect <file> [dialect] [medium]
npx humanise voiceprint <file>          # score a draft against your voice; --build builds the baseline
npx humanise voiceprint --status        # per-channel corpus counts, pairwise-test eligibility, baseline freshness
npx humanise init [--provider=<name>] [--global|--project]
npx humanise build
```

User scope is the default. Auto-detection succeeds only when exactly one reliable agent marker exists;
the installer refuses to guess when several are present. `.github` alone is not treated as evidence
that the user runs Copilot. Project installs protect private profile paths in Git's local exclude file.

## Set up a profile from a clone

If you have cloned this repo and want to work on a profile in place (rather than installing the skill into another project via `npx humanise install`), build one under `skill/profile/`:

1. `cp -r skill/profile.template skill/profile` (or `skill/profile.example` to start from a real example).
2. Copy `skill/config.example.yml` to `skill/config.yml`.
3. Start with one real sample and a contrastive calibration. Add `soul.md` after the user's decisions
   are concrete enough to record.
4. Grow towards 5 to 10 samples across active channels, including negative examples and draft-to-final
   edit pairs, then generate the fingerprint.
5. Check the engine: `cd skill/evals/assertions && python3 selftest.py`.

`skill/profile/` is gitignored and never committed. Full walkthrough in [SETUP.md](SETUP.md).

## Release

Use conventional commit subjects. Release Please prepares the version pull request and updates the
package, plugin, marketplace, README badge and changelog together.

Before approving that pull request, run:

```sh
npm run quality
npm pack --dry-run
```

Merge only when CI has installed and run the packed artefact. Create the GitHub release from the
verified commit, then publish the same version to npm. Never reuse or move a published version tag.
