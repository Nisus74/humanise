# Getting started

New to agent skills? Start here. This gets you from a fresh clone to your first humanised draft, with no prior skill experience assumed.

## What humanise is

humanise strips the tells that mark writing as AI-generated, then drafts from samples of your own writing so the result carries your voice.

It ships as an **agent skill**: a folder of instructions your AI coding agent loads and follows. If you use Claude Code, Cursor, Gemini CLI, Codex, GitHub Copilot, OpenCode, or Antigravity, you already have a tool that reads skills. You install humanise once. After that you write with your agent the way you normally do, and it applies humanise whenever you draft or edit prose.

You need two things on your machine:

- **Python 3** for the checker (standard library only, nothing to install).
- **Node 18 or newer** for the CLI wrapper and the installer.

## Try it in 30 seconds (no install, no profile, no model)

The checker runs on its own. It needs no agent, no profile, and no API key. Clone the repo and point it at any file:

```
git clone https://github.com/Nisus74/humanise
cd humanise
node cli/bin/cli.js detect path/to/your-draft.md
```

It prints the tells it found (slop words, em dashes, template openers, the structural patterns) and exits non-zero when a draft fails, so it drops straight into CI. That is the whole checker: deterministic, local, and yours to run in a script. Everything below is about getting your voice into the drafting.

## Install it into your agent

From the cloned repo, build the skill and install it:

```
npm run build                 # compile skill/ into dist/<provider>/
node cli/bin/cli.js install   # detect your agent and copy the skill in
```

`install` looks for your tool's marker directory (`.claude`, `.cursor`, `.gemini`, `.agents`, `.github`, `.opencode`) and copies the matching build into place. To choose a tool yourself, pass `--provider=<name>`, where `<name>` is one of `claude-code`, `cursor`, `gemini`, `codex`, `github` (for Copilot), `opencode`, or `universal`. Add `--global` to install into your home directory instead of the current project.

A couple of tools have their own entry point:

- **Claude Code** can also load humanise as a plugin. The repo ships `.claude-plugin/plugin.json`; add the repo as a plugin (or through a marketplace) and the skill becomes available without the copy step.
- **Codex** reads `AGENTS.md` at the repo root, and **Gemini CLI / Antigravity** read `GEMINI.md`. Open the repo in one of those and it picks up the skill.

The full per-tool table, including where the skill lands for each, is in [platforms.md](platforms.md).

## Run your first command

Inside your agent, humanise is a set of verbs you call as `/humanise <command>`. Two get you writing straight away:

- `/humanise rewrite` takes AI text you paste in and rewrites it clean.
- `/humanise guide` drafts something new from a brief.

Try the rewrite. Paste a paragraph a model wrote and ask your agent to run `/humanise rewrite` on it. The skill runs the checker, cuts the slop and the template shapes, and hands back prose that reads like a person wrote it. Before you set up a profile the result is clean and competent; it does not yet sound like *you*. That is the next step.

## Make it sound like you

The voice comes from your **profile**: `soul.md` (what you believe about writing) plus real samples of your own writing. Run `/humanise init` inside your agent for the guided setup. It walks you through the soul questions and helps you collect five to ten samples, then builds your voice fingerprint from them. Budget about ten minutes. More samples sharpen the voice, and you can add them over time.

Your profile stays private. It lives in `profile/`, which is gitignored and never committed, and the checker runs fully on your machine with no network.

From here:

- [SETUP.md](SETUP.md) is the 15-minute profile walkthrough (soul, samples, fingerprint).
- [commands.md](commands.md) documents every command in full.
- [body-and-soul.md](body-and-soul.md) explains why the engine and your profile stay separate.
