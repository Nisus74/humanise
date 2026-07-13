# Getting started

This guide takes you from a fresh clone to a personalised rewrite. You do not need to know how agent
skills work.

## 1. Install the skill

Until the npm package is published:

```sh
git clone https://github.com/Nisus74/humanise.git
cd humanise
npm run build
node cli/bin/cli.js install --provider=codex
```

Replace `codex` with `claude-code`, `cursor`, `gemini`, `github` or `opencode`. User scope is the safe
default. Add `--project` only when the skill belongs to one repository.

Verify the result:

```sh
node cli/bin/cli.js doctor --provider=codex
```

The diagnostic prints the installed skill, profile location and invocation. See [Platforms](platforms.md)
for native installation options and exact commands for every host.

## 2. Get a useful rewrite

Open your agent and invoke humanise. For Codex:

```text
$humanise rewrite
```

Paste a paragraph and say where it will be used. Humanise will preserve the point, facts and level of
certainty while removing generic model habits. With no profile, it writes cleanly and conservatively.
It will not claim the result already sounds like you.

## 3. Calibrate with one sample

Ask to set up your voice, then paste one short piece you wrote and like. A sent email, post, internal
message or document paragraph is enough. Remove sensitive details first.

Humanise will ask what the sample was trying to achieve and who read it. It will then show up to three
directions for the text you are working on:

- close to the source;
- more direct;
- more conversational.

Choose the closest one and correct it. Humanise records the decisions provisionally rather than
pretending one sample defines your whole voice.

## 4. Improve the channels you use

Add samples when there is an active reason:

- Add sent emails before an important email sequence.
- Add two posts before drafting public social content.
- Add a real memo before asking for a board paper.
- Save the AI draft and your final edit when the first version misses.

Five to ten samples spread across the channels you use create a useful working profile. Direct
draft-to-final pairs are stronger evidence than another polished sample.

For deeper setup, continue to [Voice setup](SETUP.md). For invocation syntax, read
[Commands and modes](commands.md).

## Privacy check

Profiles can contain private writing. User-scope installs live under your home directory. Project
installs are excluded locally from Git, but you should still run `humanise doctor` and inspect
`git status` before saving samples. Never store credentials or material you are not allowed to share.
