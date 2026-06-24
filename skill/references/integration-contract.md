# Integration contract

This file defines what other skills can assume about `humanise` and what `humanise` expects from them. It exists because other skills and agents can depend on these rules whenever they produce written output. The callers named below (a resume builder, a cover-letter writer, a PRD generator, an incident-postmortem tool) are illustrative integration patterns, not a fixed set.

If you are a calling skill, read this file. If you are editing `humanise`, keep this contract intact or deliberately break it with a plan to update callers.

---

## The two modes humanise runs in

### Mode A: standalone

the user says "write me a LinkedIn post" or "edit this email" and the skill runs end to end: assess, draft or diagnose, mechanical sweep pass one, mechanical sweep pass two, self-critique, self-score, present, ask for feedback.

In this mode the skill owns the whole workflow, including the verification gates and the final ask.

### Mode B: dependency

Another skill is the primary workflow owner and calls `humanise` for its style rules. Examples: `resume` is tailoring a CV, `cover-letter` is drafting a cover letter, `product-management` is producing a PRD, `cto-operating-system` is drafting an incident postmortem. The calling skill has its own structure, its own sections, its own acceptance criteria. What it borrows from `humanise` is the prose quality bar.

In dependency mode, `humanise` does NOT run its own workflow. It provides the rules; the caller applies them. The sections of the SKILL.md that matter in this mode are:

- Australian English (or the cultural variant the caller specifies)
- Punctuation: no em dashes
- Tone section
- AI detection avoidance (vocabulary + structure)
- Mechanical sweep pass one and pass two (callers should run these; the checklist is in SKILL.md, full item detail in `references/mechanical-sweep.md`)
- Positive patterns (callers should aim for two or three)

The sections that do NOT apply in dependency mode:

- Workflow: Generating new content (Steps 1, 2, 5, 6, 7)
- Workflow: Editing existing content (Steps 1, 2, 6, 7)
- The "present and ask for feedback" step at the end

The caller owns those pieces for its own output type.

---

## What callers must pass in

When a caller invokes `humanise` in dependency mode, the caller should tell `humanise` these things, either explicitly or via the surrounding conversation:

1. **Audience tag.** One of `aus-*`, `us-*`, `uk-*`, or `internal-team`. This drives cultural-calibration rules: AusE default, US spelling switch, or UK switch. Without a tag, assume `aus-*` and flag the assumption.

2. **Channel.** Which `references/channel-playbooks.md` entry applies. If the channel isn't in the playbook, use the nearest neighbour and flag it.

3. **Caller's own structural constraints.** For example, the `resume` skill specifies its own section headers and bullet format; `humanise` should not override those. The `product-management` PRD workflow specifies a "problem, solution, success criteria" structure; same deal. The contract here is: prose _inside_ the structure is governed by `humanise`; the structure itself is governed by the caller.

4. **Register target.** Formal / neutral / casual. The caller usually knows this better than `humanise` does because it knows the document type. If unspecified, `humanise` picks from the channel playbook.

---

## What callers can rely on

A caller invoking `humanise` in dependency mode can assume:

- No em dashes will appear in prose produced or edited through the skill.
- Severity 1 red-flag words (delve, tapestry, multifaceted, nuanced, realm, embark, intricate, pivotal, meticulous, testament, interplay) will not appear.
- Empty binary contrasts will be rewritten as direct statements. At most one load-bearing contrast (per the removal test in `structural-tells.md`) may remain per piece, and none in detector-bound copy such as sales material or formal submissions.
- Sentence rhythm will vary deliberately (no three consecutive sentences within 5 words of each other).
- At least three distinct contraction types will appear in any piece longer than a paragraph, unless the caller has explicitly asked for a no-contractions register.
- For `aus-*` tagged content, at least two distinct AusE spelling patterns will be visible.
- For `us-*` tagged content, zero AusE spelling leakage.

If the caller sees any of the above violated in the output, treat it as a skill bug and raise it rather than hand-patching it.

---

## Per-caller notes

### resume

The `resume` skill reads `humanise` for prose rules (bullet text, summary paragraph, skills descriptions) but owns structure entirely. Resume bullets often run close to the specificity bar already (achievements with numbers); `humanise` should reinforce rather than rewrite.

Resume-specific overrides:

- Bullets typically drop the subject pronoun ("Led X", not "I led X"); this is fine.
- Past tense throughout for prior roles, present tense for current role.
- No contractions in resume prose (register override).
- "programme" / "program" distinction matters: "program" for software, "programme" for training, grants, schemes.

### cover-letter

The `cover-letter` skill reads `humanise` for voice and tone but has its own opening, middle, closing framework. Cover letters for US roles use US English; for AU/UK roles use the local variant.

Cover-letter-specific overrides:

- Opening sentence must not start with "I am writing to apply" (slop opener list applies).
- Signature block and formal sign-off are caller's domain, not humanise's.
- Slightly more formal register than a casual email, less formal than a board paper.
- Cover letters are a formal channel: pass `formal=true` to `writing_checks.py` (the 4th positional arg) so the "no I/This opener" rule is a hard check, not advisory. Eval 12 covers this path.

### product-management

The `product-management` skill produces many document types: PRDs, strategy memos, opportunity-solution trees, stakeholder updates, meeting prep docs. Each has its own structure, but the prose rules apply uniformly.

PM-specific overrides:

- Frameworks can be named when load-bearing (JTBD, OST, RICE, Kano) but should not be paraded for show.
- PRDs and strategy docs tolerate a slightly more formal register than investor updates.
- "Customers" vs "users" is a deliberate word choice in PM writing; humanise should not silently swap them.
- Metrics and numbers should be exact, not rounded, unless the caller signals otherwise.

### cto-operating-system

The `cto-operating-system` skill produces technical documents: ADRs, RFCs, incident postmortems, security reviews, vendor assessments. `references/technical-writing.md` applies directly.

CTO-OS specific overrides:

- Technical precision beats prose polish where they conflict (see `technical-writing.md`).
- Acronyms and jargon are fine once defined; no need to expand every occurrence.
- Code blocks, command examples, config snippets are outside the prose scope (pedagogy note applies).
- Commit messages follow conventional-commit format regardless of other prose rules.

---

## What humanise must not do

The following would break the contract:

- Rewrite section headers that the calling skill supplied. If the caller's template says "## Problem statement", humanise should not change that to "## The problem".
- Alter numerical or factual content in pursuit of style. If the caller put "99.2% accuracy" in the draft, humanise should not change it to "high accuracy" to make the prose flow.
- Apply prose rules to code blocks, commit messages, log excerpts, structured data, or quoted material. See the "When to apply, and when to hold off" section in SKILL.md.
- Inject signature blocks, sign-offs, or standard closings that the caller didn't request.
- Change the cultural variant implicit in the draft. If the draft is tagged `us-*`, humanise must not "correct" the spelling back to AusE.

---

## Failure modes and fallbacks

If a caller doesn't pass an audience tag or channel: default to `aus-*` and LinkedIn-neutral register, and leave a brief note in the output about the assumption. Don't silently guess.

If the prose rules and the caller's conventions conflict: the caller wins on structure; humanise wins on prose quality. A PRD that says "We must enhance our robust infrastructure" fails both the PM skill's (vague) and humanise's (slop) standards; it should be rewritten, and the rewrite preserves PM structure.

If humanise detects an em dash the caller's template includes deliberately (e.g., an ASCII divider line in a doc template): treat template content as structure, not prose. Em dashes in visible structural elements stay; em dashes in prose get rewritten.

---

## How to update this contract

When a new calling skill is added, add a per-caller notes section. When a caller's needs change, update the relevant section. When the prose rules change in a way that affects callers (e.g., a new red-flag word, a tightened assertion threshold), update the "what callers can rely on" section and mention it in `MEMORY.md` so future conversations don't miss it.

Any change to this contract is a high-stakes change under `evals/self-harness-loop.md`: it clears the held-in suite, an adversarial read, and the user's sign-off before promotion, because resume and cover-letter read this contract and a silent break ripples into their output.
