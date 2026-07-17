# Beginner installation and onboarding design

## Purpose

Give someone who has never used an agent skill one reliable path from the repository homepage to a
working, private and personalised humanise installation.

The current documentation contains the necessary concepts, but the sequence is fragmented. The README
starts with commands before explaining the product model. The getting-started guide still assumes the
npm package is unpublished. Configuration, voice setup, invocation and vendor differences sit on
separate pages without a checklist that joins them together.

## Outcome

A first-time user should be able to answer these questions without understanding the Agent Skills
standard:

1. What is humanise, and what does installing a skill do?
2. Which command applies to my agent?
3. Where will the skill and my private profile live?
4. How do I confirm the installation worked?
5. How do I get a useful result before creating a profile?
6. How do I create and customise my voice profile?
7. How do I know the personalised result is working?
8. What should I do when the skill does not appear?

## Scope

This change covers:

- the primary README journey;
- the complete beginner walkthrough in `docs/getting-started.md`;
- accurate paths, native installers and invocation syntax in `docs/platforms.md`;
- the boundary between quick setup and advanced voice setup in `docs/SETUP.md`;
- explicit Antigravity support in the npm installer;
- provider-path and installation regression tests;
- live verification against the published `humanise@1.0.0` package.

The change does not redesign the writing engine, alter profile semantics, add a graphical installer or
publish another package version. Changes after `1.0.0` will require a later release before npm users
receive them.

## Recommended information architecture

### README: start here

The README remains the short entry point. Its installation section becomes a six-step quickstart:

1. Understand what will be installed.
2. Check Node.js and Python prerequisites.
3. Choose a host from a table.
4. Install and run `doctor`.
5. Open the host and get one generic rewrite.
6. Run the in-agent `init` flow with one real writing sample.

The README links to the full walkthrough before presenting advanced concepts. Claude's plugin option
remains visible, but it does not interrupt the default direct-install path.

### Getting started: one complete beginner journey

`docs/getting-started.md` becomes the canonical step-by-step guide. A user should not need to jump to
another page until the first personalised result is complete.

The guide follows this order:

1. Explain an agent skill in two plain-language paragraphs.
2. Explain what the installer copies and what it does not do.
3. Check `node --version` and `python3 --version`.
4. Choose a provider and scope.
5. Run the exact install and `doctor` commands.
6. Refresh or restart the host only when its discovery behaviour requires it.
7. Invoke humanise and complete a generic rewrite.
8. Create `profile/` and `config.yml` through `humanise init` or the host's `init` mode.
9. Set name, dialect, register and active channels in `config.yml`.
10. Add one redacted sample, its reader and its purpose.
11. Choose and correct a rewrite direction.
12. Run a personalised rewrite and compare it with the generic result.
13. Run the final privacy and health checks.

Every command block includes the expected success signal. Troubleshooting is symptom-led: command not
found, unsupported Node version, several agents detected, skill missing in the host, incomplete profile
and tracked private files.

### Platform guide: exact vendor reference

`docs/platforms.md` stays the reference for vendor-specific paths and alternative installers. It must
not repeat the full onboarding journey.

Each vendor section includes:

- npm provider name;
- project and personal paths;
- install and `doctor` commands;
- explicit invocation;
- refresh behaviour;
- a supported native installer when one exists.

Codex guidance states that skills are normally discovered automatically and recommends restarting only
when the skill is absent. Claude direct-skill and marketplace-plugin setup remain separate because they
use different invocation and profile locations. GitHub's current `gh skill` command replaces the stale
future-tense note and shows a `v1.0.0` pin.

### Voice setup: advanced depth

`docs/SETUP.md` starts after the first one-sample calibration. It keeps the multi-channel corpus,
relationships, negative examples, soul, fingerprint and learning-loop guidance. Beginner installation
and basic configuration stay in getting started rather than being repeated here.

## Provider behaviour

The npm CLI continues to support these provider names:

| Provider | Personal path | Project path | Invocation |
| --- | --- | --- | --- |
| `codex` | `~/.agents/skills/humanise` | `.agents/skills/humanise` | `$humanise` |
| `claude-code` | `~/.claude/skills/humanise` | `.claude/skills/humanise` | `/humanise` |
| `cursor` | `~/.cursor/skills/humanise` | `.cursor/skills/humanise` | `/humanise` |
| `gemini` | `~/.gemini/skills/humanise` | `.gemini/skills/humanise` | enable, then ask normally |
| `github` | `~/.copilot/skills/humanise` | `.github/skills/humanise` | `/humanise` where supported |
| `opencode` | `~/.config/opencode/skills/humanise` | `.opencode/skills/humanise` | ask normally or load the skill |
| `antigravity` | `~/.gemini/config/skills/humanise` | `.agents/skills/humanise` | mention humanise by name |

Antigravity becomes an explicit provider. Its detection must fail closed because `.agents` is shared
with Codex and its `.gemini` marker can overlap Gemini CLI. Users pass `--provider=antigravity`; the CLI
does not guess between those hosts.

The provider table remains the single source of truth for CLI paths and invocation text. Documentation
examples must match it.

## Installation and configuration model

Personal scope remains the default because it works across projects and keeps private writing under the
user's home directory. Project scope remains opt-in through `--project` and continues to add profile and
configuration entries to Git's local exclude file.

The guide distinguishes two setup operations:

- `npx humanise init --provider=<name>` creates the profile and configuration files.
- The in-agent `init` mode interviews the user, interprets a sample and records provisional voice
  decisions.

Users should not be told that the terminal command performs the interview. The recommended beginner
sequence is terminal scaffolding first, then the in-agent calibration.

Configuration instructions cover only the fields a new user can decide immediately: name, dialect,
default register, profile directory and active channels. Advanced evidence and confidence concepts stay
in the voice-setup guide.

## Privacy and safety

The walkthrough warns users before requesting a writing sample. Samples should be real, redacted and
something the user is allowed to provide to their chosen AI host.

The guide states clearly:

- humanise itself does not upload profile files;
- the selected AI host has its own data policy;
- user-scope profiles live under the home directory;
- project profiles must not appear in `git status` or `git ls-files`;
- credentials and regulated material do not belong in the profile;
- the local deterministic checker makes no model or API call.

## Error handling

The user journey treats `doctor` as the source of truth after installation. Each troubleshooting entry
starts from an observable symptom and gives one next action.

Provider auto-detection remains strict. Zero matches require `--provider`; several matches list the
candidates and require an explicit choice. Antigravity is never inferred automatically.

Host refresh advice follows current vendor behaviour rather than applying one restart instruction to
every tool.

## Verification

The implementation must prove both documentation accuracy and installer behaviour:

1. Unit tests assert every provider's personal path, project path and invocation text.
2. CLI tests install each provider into isolated personal and project fixtures.
3. `doctor` passes for every installed fixture.
4. Antigravity tests confirm explicit installation and no optimistic auto-detection.
5. Claude's marketplace manifest passes `claude plugin validate .`.
6. The published `humanise@1.0.0` tarball is downloaded and its six released providers are smoke-tested.
7. Repository quality, package privacy and version checks pass.
8. Substantial documentation runs through the humanise writing checker.
9. Documentation links and command examples are checked for stale unpublished-package language.

The published tarball cannot contain the new Antigravity provider until a later release. Documentation
must distinguish the behaviour available in `1.0.0` from unreleased repository changes, or defer the
new provider instructions until the next version is published.

## Acceptance criteria

The work is complete when:

- the README exposes an obvious beginner starting point above advanced product detail;
- a user can follow `docs/getting-started.md` from zero knowledge to one personalised rewrite;
- no user-facing page claims the npm package is unpublished;
- every documented provider command matches the CLI and current vendor documentation;
- Gemini CLI and Antigravity have separate, accurate instructions;
- the guide explains both terminal scaffolding and in-agent calibration;
- configuration and privacy checks are explicit;
- all provider tests, package checks and writing checks pass;
- the worktree contains no private profile changes.
