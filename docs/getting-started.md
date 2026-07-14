# Getting started

This guide assumes you have never installed an Agent Skill. By the end, humanise will be visible in
your agent, your private profile will exist, and you will have compared a generic rewrite with one
calibrated from your own writing.

## What you are installing

An Agent Skill is a folder your AI agent reads when a task matches its description. humanise contains
the writing workflow, reference material and local tools. The installer copies those files into your
agent's skill directory. Your agent still provides the model and follows its own data policy.

humanise stores your writing profile separately from the shared engine. Personal installs keep it under
your home directory. Project installs keep it inside one repository and add local Git exclusions.
humanise itself does not upload the profile.

## Step 1: check Node.js and Python

Open a terminal and run:

```sh
node --version
python3 --version
```

Continue when Node reports `v18` or later and Python reports version 3. The installer needs Node.
Python runs `detect`, `fingerprint` and the deterministic writing checks.

## Step 2: choose your host and scope

| Agent | Provider name | Invoke after installation |
| --- | --- | --- |
| Codex | `codex` | `$humanise rewrite` |
| Claude Code, direct skill | `claude-code` | `/humanise rewrite` |
| Cursor | `cursor` | `/humanise rewrite` |
| Gemini CLI | `gemini` | Enable the skill, then ask normally |
| GitHub Copilot | `github` | `/humanise rewrite` where supported |
| OpenCode | `opencode` | Ask it to use humanise |
| Antigravity | Native GitHub CLI install | Mention humanise by name |
| Another Agent Skills host | `universal` | Ask it to use humanise |

Personal scope is the default. Choose it when you want one profile across projects. Project scope uses
`--project`; choose it for a repository-specific installation. Start with personal scope unless you
have a reason to keep the skill in one repository.

## Step 3: install humanise

This example uses Codex. Replace `codex` with `claude-code`, `cursor`, `gemini`, `github`, `opencode` or
`universal` for another host.

```sh
npx humanise@1.0.0 install --provider=codex
```

Success looks like:

```text
Installed humanise for codex (global) -> /your/home/.agents/skills/humanise
Next in codex: $humanise. Ask it to set up humanise.
```

Antigravity uses GitHub CLI 2.90.0 or later with the released `v1.0.0` skill:

```sh
gh skill install Nisus74/humanise skill/SKILL.md --agent antigravity --scope user --pin v1.0.0
```

## Step 4: check the installation

Use the same provider and scope you used for installation:

```sh
npx humanise@1.0.0 doctor --provider=codex
```

`OK` should appear beside the skill, profile template and configuration template. `NOT SET UP` beside
the private profile is expected before Step 6.

For the native Antigravity installation, verify discovery with:

```sh
gh skill list --agent antigravity --scope user
```

The output should include `humanise`, pinned to `v1.0.0`.

## Step 5: get a useful rewrite before setup

| Agent | First command or request |
| --- | --- |
| Codex | `$humanise rewrite` |
| Claude direct skill | `/humanise rewrite` |
| Claude marketplace plugin | `/humanise:humanise rewrite` |
| Cursor | `/humanise rewrite` |
| Gemini CLI | `/skills enable humanise`, then ask it to use humanise |
| GitHub Copilot | `/humanise rewrite` where supported |
| OpenCode, Antigravity and other hosts | Ask the agent to use humanise in rewrite mode |

Give the agent a real paragraph and a little context:

```text
Rewrite this without changing the point, facts or level of certainty. It is an email to a customer who
already knows the project context:

<paste your paragraph>
```

Save the result temporarily. It is the generic baseline you will compare after calibration.

## Step 6: create the profile and configuration

For an npm installation, run:

```sh
npx humanise@1.0.0 init --provider=codex
```

Success looks like:

```text
Created /your/home/.agents/skills/humanise/profile from profile.template.
Created /your/home/.agents/skills/humanise/config.yml.
```

The terminal command creates files. It does not interview you or infer your voice. If you installed
with a native vendor command, ask the agent to use Humanise in `init` mode so it can create the profile
and configuration from the included templates. For a Claude marketplace plugin, invoke
`/humanise:humanise init`; Claude creates the profile in its persistent plugin data directory.

## Step 7: set the basic configuration

Open the `config.yml` path printed by `init` and set only what you know:

```yaml
name: "Your Name"
dialect: en-AU
default_register: 3
profile_dir: profile
channels:
  - email
  - slack
custom_slop: []
```

Use `en-AU`, `en-GB` or `en-US`. Register `1` is raw and casual; `5` is ceremonial. Start at `3` when
you are unsure. List only channels you regularly use. Leave `custom_slop` empty until you can name a
phrase you personally reject.

## Step 8: teach humanise with one sample

Invoke humanise in `init` mode inside the agent. Paste one short piece you wrote and like after removing
sensitive details. Explain who read it, your relationship and what the writing needed to achieve.

humanise offers close, direct and conversational directions. Choose the closest version and correct
anything that feels wrong. Your choice and corrections become provisional voice evidence. One sample is
enough to start; it does not define your whole voice.

## Step 9: run the personalised comparison

Give humanise the same paragraph and brief from Step 5. Check that the point, facts, certainty and ask
remain unchanged. The improvement should come from decisions such as what leads, what gets cut, how the
reader is handled and where the piece stops.

If the result misses, say what you would change. A direct correction teaches humanise more than another
list of style adjectives.

## Step 10: run the final health and privacy check

```sh
npx humanise@1.0.0 doctor --provider=codex
```

The private profile should now report `OK`. For project scope, also run `git status` and confirm neither
`profile/` nor `config.yml` appears. Never add credentials or writing you are not allowed to share with
your chosen AI host.

For a native Antigravity installation, repeat the `gh skill list` check and ask Antigravity to confirm
the profile and `config.yml` paths it created.

## Troubleshooting

### `npx` or `node` is not found

Install Node.js 18 or later, reopen the terminal and run `node --version` again. Continue only when the
command prints `v18` or a newer major version.

### More than one supported agent was detected

Pass the provider explicitly, for example `--provider=codex`. Do not delete another agent's
configuration to make auto-detection choose one host.

### The skill does not appear

Codex normally discovers skills automatically; restart only when it remains absent. Restart Claude Code
when its top-level skills directory was created after the session began, or run `/reload-plugins` for a
marketplace plugin. Reload Cursor's window, use `/skills reload` in Gemini CLI, use `/skills reload` in
Copilot CLI where available, or restart OpenCode.

### `doctor` reports `MISSING`

Rerun `install` with the same provider and scope passed to `doctor`. A personal install and a project
check point at different directories.

### The profile is `NOT SET UP`

Run the terminal `init` command with the same provider and scope. Afterwards, invoke humanise in `init`
mode inside the agent to perform the voice calibration.

### A project profile appears in Git

Stop before committing. Run `doctor`, inspect `.git/info/exclude` and remove already tracked profile
files from Git's index without deleting the local copies.

## Next steps

Continue to [Voice setup](SETUP.md) when one sample is useful and you want coverage across more channels.
Read [Commands and modes](commands.md) for normal use or [Platforms](platforms.md) for native vendor
installers and exact host paths.
