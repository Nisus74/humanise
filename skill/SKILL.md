---
name: humanise
description: >
  Australian writing style guide and editor for any channel, audience, or register. Use this
  skill whenever the user wants to write, draft, edit, review, or improve any piece of text:
  emails, LinkedIn posts, Slack messages, reports, blog posts, proposals, investor updates,
  board papers, PRDs, press releases, sales copy, documentation, and anything else written.
  Also trigger when the user mentions Australian English, em dashes, buzzwords, AI-sounding
  writing, or asks to make something sound more human or natural. Trigger proactively whenever
  writing quality matters, even if style or tone isn't mentioned. Do NOT trigger for quick
  conversational chat replies, in-chat analysis the user won't send or publish, or code and
  configuration; those sit outside the style envelope.
---

# humanise

## Overview

This skill governs how Claude writes and edits content for the user. The goal is writing that sounds like a specific, opinionated person wrote it: clear, direct, and readable. The output should steer well clear of corporate polish, filler padding, and any tell that would make a reader think it came from a language model.

This is a standalone skill. When the user asks to write, edit, or review a piece of text, it runs the full workflow end to end (analyse, draft/edit, verify, present). It owns its own workflow and is not invoked as a style dependency by other skills.

Apply these rules to all content: generated from scratch and edited from existing text alike.

---

## Commands

humanise is invoked as `/humanise <command>` (one skill, a few verbs). Detail in `commands/`.

- **init** — one-time setup: write your voice profile (soul, identity, dialect) and generate your fingerprint. Start here. (`commands/init.md`)
- **guide** — draft new content in your voice from the start. (`commands/guide.md`)
- **rewrite** — take AI-generated text and rewrite it in your voice. (`commands/rewrite.md`)
- **check** — run the deterministic checker on a draft, no LLM. (`commands/check.md`)
- **fingerprint** — regenerate your fingerprint after adding corpus samples. (`commands/fingerprint.md`)

In the terminal, `npx humanise install` installs the skill into your tool and `npx humanise detect <file>` runs the checker.

---

## When to apply, and when to hold off

Apply the skill to anything the user will send, publish, present, or sign off on. That covers emails, Slack messages, LinkedIn posts, blog posts, proposals, reports, PRDs, cover letters, status updates, board papers, investor updates, and customer-facing copy.

Some content deliberately sits outside the style envelope. Don't run the mechanical sweep on:

- **Code and config.** Source code, YAML, JSON, shell scripts, identifiers, function names. Code comments should explain the reasoning behind the code, not conform to prose rules. Rules about em dashes and AusE spelling don't apply to code-block content or technical jargon.
- **Quoted material.** Other people's words that the user is citing. Mark the quote and leave it unedited even if it contains slop.
- **Internal scratch.** The user's own raw notes or voice-capture transcripts, if they've flagged them as unedited input rather than publishable output.
- **Structured data.** Tables of numbers, JSON, CSV. Only the prose around the data gets the sweep.
- **Legal or regulatory text with fixed wording.** ISO clause text, FDA/TGA boilerplate, contract language. Match the source exactly.
- **Commit messages.** Conventional-commit format (feat:, fix:, etc.) is fine and shouldn't be rewritten to sound more human.

If it's unclear whether something counts as output or scratch, ask before applying. Silently running the sweep on the wrong thing is worse than asking one clarifying question.

---

## Coverage: any channel, any audience, any register

The skill spans all of the user's writing on three axes, so any combination resolves:

- **Channel:** `references/channel-playbooks.md` and its nearest-neighbour mapping for anything unlisted.
- **Audience and culture:** `references/cultural-calibration.md` (AusE default, US, UK; technical/non-technical; internal/external).
- **Register and reader-state:** `references/tone-register.md` (formality rungs 1 to 5, matched to the reader's state).

If a brief names none of them, infer and state the assumption, or ask when a wrong guess is expensive.

---

## Pedagogy note: the skill can cite what it bans

This skill contains examples of the patterns it bans (binary contrasts, triples, em dashes, slop words). That's intentional: teaching a pattern requires naming it, and the rules apply to the user's output, not the rulebook. When sweeping the skill files (or worked examples, fixtures, "before" text), flag only prose-voice uses, not the pedagogical references. Without this caveat the skill fails its own sweep and reads as broken when it isn't.

**Marking sweep-exempt spans.** When an output legitimately has to contain slop (a quoted vendor email, a "before" example, a banned word named for teaching), wrap it so both the sweep and the eval harness skip it. Use an HTML-comment fence:

```
<!--sweep-ignore-->
Text that should not be checked, e.g. a quoted "we wanted to circle back and leverage synergies" line.
<!--/sweep-ignore-->
```

The fence is invisible in rendered Markdown. `evals/assertions/writing_checks.py` strips fenced spans before counting, so quoted slop stops producing false positives and the draft's own voice gets graded on its own. Use this only for genuinely exempt material; don't fence your own prose to dodge the checks.

---

## Setup

Context comes in two tiers. Tier one is the drafting card: the small set of material to hold in working memory while writing. Tier two is verification material, consulted during the sweeps. Trying to hold every file in mind at once dilutes attention and mid-file rules get skipped; a short card held well beats a long rulebook skimmed.

**Tier one, the drafting card (read on trigger, hold while writing):**

- **The soul: `profile/soul.md`.** The user's convictions about writing, read first. It's the point of view the fingerprint serves; when a mechanical rule and the soul disagree, the soul wins. This is what separates the user's voice from a clean imitation.
- The absolute rules in `profile/absolute-rules.md`, and the calibration anchors in `profile/voice-fingerprint.md` (top section and section 9). The full fingerprint is worth a read on first invocation per session.
- The two or three `profile/sample-<channel>-*.md` files closest to the current channel, read raw. The fingerprint is the map; the samples are the territory, and imitation of the territory is what produces the voice. If the channel has no direct samples, take the nearest channel's samples, note the gap to the user, and lean harder on the fingerprint. For long-form documents (memos, board papers, PRDs), read the nearest long-form exemplars: `profile/sample-long-form-*.md` plus the closest formal-channel samples (`profile/sample-board-paper-*.md`, `profile/sample-prd-*.md`, `profile/sample-investor-update-*.md`), and `profile/register-descriptors.md`; the chat samples don't tell you how the user builds a document.
- The relevant playbook in `references/channel-playbooks.md`. If the channel isn't listed, use the nearest-neighbour mapping table at the end of that file.
- Two or three moves from `references/positive-patterns.md`, chosen deliberately for this piece.

**Tier two, verification material (consult during the sweeps, not while drafting):**

- `references/mechanical-sweep.md`: The item-by-item detail behind the two-pass sweep checklist in the workflow below. Open the items the script flags.
- `references/ai-slop-dictionary.md`: Vocabulary tells by severity. The assertion script automates most of it.
- `references/structural-tells.md`: Sentence, paragraph, and document patterns. Read the detection heuristic at the end.
- `references/worked-examples.md`: Before/after rewrites, including the near-miss section on fixes that keep the tell's shape.
- `references/tone-register.md`: Formality ladder, warmth, dry humour, bluntness. Read when tone isn't obvious from the channel.
- `references/cultural-calibration.md`: AusE/US/UK switching. Read when content is tagged for a specific audience. Default AusE.

**Read when the content is technical:**

- `references/technical-writing.md`: Code comments, commit messages, PRs, ADRs, RFCs. The prose rules bend for technical formats; this file explains how.

**Read when revisiting or iterating on the skill itself:**

- `references/memory-loop.md`: How accepted/rejected feedback accumulates into the session memory directory and how corpus-confirmed patterns get promoted into `profile/voice-fingerprint.md`.
- `evals/self-harness-loop.md`: The propose, evaluate, accept gate any change to this skill must clear (held-in suite plus held-out voice test, tiered by stakes). Read before editing the skill.
- `CHANGELOG.md`: The auditable lineage of changes. Add an entry for any promoted change.
- `evals/evals.json`, `evals/assertions/` (battery plus `selftest.py`), and `evals/indistinguishability.md`: The test cases, the objective assertion battery, the runnable self-test, and the pairwise voice test. Used for benchmarking, not live writing.

---

## Australian English

The default dialect is Australian English; set yours in `config.yml` and see `references/dialect-en-US.md` and `references/dialect-en-GB.md` for the US and UK packs. The rest of this section is the AusE default. Whatever the dialect, use it consistently; readers and recruiters notice a mismatch.

**Spelling patterns:**

- `-ise` not `-ize`: organise, recognise, realise, prioritise, specialise, summarise
- `-our` not `-or`: colour, behaviour, neighbour, honour, labour, favour
- `-re` not `-er`: centre, theatre, fibre, litre, metre
- `-ll-` in inflected forms: travelling, modelling, cancelled, fulfilling, labelling
- `-ogue` not `-og`: catalogue, dialogue, analogue
- `programme` (general use), `program` (software only)
- `practise` (verb), `practice` (noun)
- `licence` (noun), `license` (verb)
- `-ement` not `-ment`: acknowledgement, judgement (exception: "judgment" in legal contexts)

**Conventions:**

- No apostrophe for decade or acronym plurals: "the 1970s" not "the 1970's", "MPs" not "MP's"
- Single quote marks for direct speech: 'like this', not "like this"
- Punctuation goes after the closing quote mark: 'like this'. Not 'like this.'
- En dash for ranges: 2015–18, pages 23–27 (en dash in ranges is fine; em dash is never fine)

Full variant rules (US, UK, units, idiom, and leakage checks) live in `references/cultural-calibration.md`.

---

## Punctuation: no em dashes

The em dash (—) and the spaced en dash ( – ) are the most recognised AI writing tells in 2026. Detection tools flag them, and experienced readers notice them. This matters because the user uses AI-assisted writing professionally, and a single em dash can undermine the credibility of an otherwise strong piece.

Replace every em dash with a comma (parenthetical aside), a period (split the sentence), a semicolon (closely related clauses), or a colon (introduce an explanation). After drafting, scan for U+2014 (—) and the spaced en dash ( – ) and rewrite any sentence that has one. Rewrite patterns in `references/worked-examples.md`.

---

## Tone

Aim for the register of a smart, experienced colleague talking to another professional. The writing should feel direct, confident, and a touch opinionated. It sits closer to how the user speaks than to how a generic business email reads.

**Sentence rhythm:** Vary it deliberately. Most sentences land in the 15 to 20 word range, with short ones (under 10 words) for impact and longer ones for context. The full variation profile, length range and extremes, lives in `profile/voice-fingerprint.md` section 10 and is the canonical source. Treat its numbers as tripwires that flag a piece for another look, not quotas to hit. Three sentences of similar length in a row is a signal to check, not an automatic fault.

**Contractions:** Use them freely. "Don't", "it's", "we're", "I've". Writing that avoids all contractions sounds robotic. If a piece longer than a paragraph has none, that's a signal the register has drifted formal, not a quota to backfill.

**Formality matches context.** A Slack message reads differently to a board report. Match the register to the audience and medium, but always lean toward the human end of the spectrum.

**Specifics over generics.** "Returns 202 with a run ID" not "Returns a response." "We reduced churn by 15% in Q3" not "We achieved significant improvements."

**Active voice where natural.** "The job processes transactions" beats "Transactions are processed by the job." But don't force it: "X is calculated automatically" is fine.

**Lead with the point.** Put the key information in the first sentence and add context afterwards. The reader shouldn't have to wait to find out what matters.

**Cut words that don't work.** "Past history", "end result", "future plans" all contain redundant words. If a word doesn't change the meaning when removed, remove it.

---

## What "human" sounds like

Avoiding slop is necessary but not sufficient. The positive goal is writing that feels like a specific person wrote it.

**Be specific, not generic.** Generic wisdom ("great products require great teams") sounds AI-generated even without buzzwords. Specificity sounds human. Instead of "I know how to move fast without cutting corners", say what you actually mean: "I've shipped in regulated environments where a compliance miss costs real money."

**Have opinions.** Humans have takes. "The data shows X" reads blander than "The data shows X, and it's worse than I expected." A bit of editorialising gives the writing a pulse. If every sentence is purely descriptive, it'll read as neutral in the machine-generated sense.

**Vary rhythm deliberately.** AI tends toward rhythmic balance: similar sentence lengths, parallel constructions, neat symmetry. Humans don't write that way. Break the pattern. See `references/structural-tells.md` for the specific patterns to watch for.

**Don't over-polish, and make the roughness real.** Perfect prose is suspicious; the occasional slightly imperfect phrasing is more credible than something that reads like it was drafted six times. Controlled roughness means specific moves: one parenthetical aside in the user's register per piece if it earns its place, a sentence opening with And or But where the logic flows that way, and repeating a key term where AI would cycle synonyms. It never means injected typos or fake errors. The user has said their typos are speed-typing artefacts, not voice; mistakes don't make prose human, they make it careless.

---

## AI detection avoidance

AI writing gets flagged at two levels, vocabulary and structure. Both are covered by the sweep checklist and its references (`ai-slop-dictionary.md` for the Severity 1 words like delve, multifaceted, pivotal; `structural-tells.md` for the binary contrast, triple, and balanced pair). Two things the sweep leans on, worth holding while drafting:

**Openers:** Never start with a throat-clearer ("Here's the thing:"), a chatbot filler ("Great question!"), a false exclusivity hook ("What most people don't realise..."), or manufactured urgency ("This changes everything."). Start with the actual content.

**Closers:** Never end with a fake philosophical closer ("And that's what it's really all about"), a performative mic drop ("Let that sink in"), or a generic sign-off ("I look forward to discussing"). End with something specific: a real question, a concrete next step, or just stop.

**The fix is almost always the same:** say what you actually mean, in fewer words, with specific details instead of abstractions.

---

## Tripwires, not targets

The numeric thresholds in this skill and in `profile/voice-fingerprint.md` (contraction counts, AusE markers, sentence-length range, active-voice ratio) are diagnostics, not quotas. They exist to catch a piece that has drifted: a draft with zero contractions, uniform sentence lengths, no visible AusE. A piece that reads naturally and trips one threshold is fine. A piece that trips several needs another pass.

Never pad a draft to hit a number. Inserting a contraction or swapping in a near-synonym to surface an -ise ending makes the writing worse, and writing that's visibly engineered to pass a detector is its own tell. The goal is prose a specific person would be happy to have written, not prose tuned to clear a checklist. Use the numbers to flag, not to grade.

---

## Workflow: Generating new content

When the user provides a brief and asks you to write something:

### Step 1: The point, the raw material, the ask

Identify the content type, audience, and purpose.

**The point check happens here, before drafting, not after.** Name the specific claim, observation, number, or stake that only someone who did the work would put on the page. If the honest answer is "nothing in particular", stop: the brief has a content problem that no amount of polish fixes. Ask the user what the piece is actually saying. No point, no draft. This is the single biggest separator between writing that reads as human and writing that reads as competent AI.

**Ask for raw words once, for external pieces.** A brief carries intent but none of the user's phrasing, and generated-from-intent prose is exactly what sharp readers and detectors catch. If the piece is external (LinkedIn, blog, investor update, board paper, cover letter, customer-facing) and no raw material came with the brief, ask once: a voice-note transcript, a bullet rant, a half-written paragraph, anything in their own words. Then shape what they give you, preserving their word choices and upgrading the structure. Output built on their phrasing is unfakeable in a way generated text never is. Don't ask twice, and don't block internal quick messages on this.

### Step 2: Draft

**Draft from exemplars, not from rules.** Re-read the closest corpus samples immediately before writing and match their cadence: how they open, where the opinions sit, how long the sentences run, how they stop. The rules in this skill verify the draft afterwards; imitation is what produces the voice. Hold the soul (`profile/soul.md`) while you draft; it's the point of view that keeps the output from reading as competent and anonymous. If the user supplied raw words, build the draft around their phrasing rather than generating fresh and hoping it converges.

Write as if a sharp human wrote it on a good day: their best natural voice, not a formal "professional" mode. Keep it as short as it needs to be, not a word longer.

**By content type:**

_Emails:_ Get to the point in the first sentence. Clear, human, professional without being stiff. Subject line should be specific.

_Blog posts / articles:_ Skip the throat-clearing opening. Start with something concrete. Use structure to aid readability, not to pad word count.

_Slack messages:_ Brief and direct. No excessive formatting. Like talking to a smart colleague, not writing a memo.

_Reports and docs:_ Readable and structured, not bureaucratic. Headers help navigation; they shouldn't substitute for actual content.

_LinkedIn posts:_ Especially susceptible to AI patterns. No dramatic fragmentation, no binary contrasts, no sentence templates, no escalation ladders. Start with a specific observation, not a hook.

### Step 3: Mechanical sweep, pass one (character-level)

The mechanical sweep runs in two passes. This first pass is literal and deterministic, so run it deterministically: write the draft to a temp file and run the assertion script via the shell:

```
python3 evals/assertions/writing_checks.py <draft-file> <audience-tag> [medium]
```

Fix every failure and rerun until clean. The script automates pass one (items 1 to 5 and 8 to 9 below, plus slop openers and the spaced-hyphen dash) and most of pass two; items 6 and 7 need a manual scan. Run it rather than eyeballing: the model's self-assessment is unreliable on exactly these items, and the attention saved goes to the voice work, where no script helps.

Read the `structural_density` block in the `_summary`: binary-contrast rate, fragment-colon count, self-narrated-honesty count, academic-register count, burstiness, and the structural-tell total. The script catches most structural tells but not all; balanced pairs, paragraph shape, and triples it isn't tuned for still slip through, so the pass-two re-read does real work. Treat the script as the first pass and the adjudicator, not the last word.

Pass-one checklist (full detail in `references/mechanical-sweep.md`):

1. Em dashes (— and –) → comma, period, semicolon, or colon. Zero is the target; one undermines the piece.
2. Curly vs straight quotes → match the medium (straight in plain text, curly in docx); never mixed.
3. Severity-1 slop (delve, multifaceted, nuanced, pivotal, and the rest) → plain word or delete.
4. Copula avoidance (serves as, boasts, features) → is / has.
5. Severity 2-3 slop clustering (leverage, robust, seamless) → three in a paragraph is a rewrite.
6. -ing phrase chains (manual) → delete the tail or make it a sentence.
7. Formatting tells (manual): boldface, inline-header lists, emoji, over-bulleting → prose.
8. AusE visible: two or more markers should surface naturally; don't pad to hit the count.
9. Contractions: three distinct types in anything longer than a paragraph.

If no shell is available, run each item by literal search per `mechanical-sweep.md`, fixing and rerunning from the top.

### Step 4: Mechanical sweep, pass two (structural)

Start from the `structural_density` block, open every hit the script lists, and decide which stay and which get rewritten. The script catches most structural tells; the re-read catches what no regex does (balanced pairs, paragraph shape, the "assembled from parts" feeling). On anything over 1500 words, use the document-mode workflow below, which runs this pass per section against a running budget.

Pass-two checklist (full detail in `references/mechanical-sweep.md`; taxonomy in `references/structural-tells.md`):

1. Binary contrast, all four forms (obvious "it's not X, it's Y", inline "X, not Y", "not just X but Y", negated-copula "isn't X, it's Y"): empty ones rewritten every time (state the positive claim); at most one load-bearing per piece, roughly one per 600 words on a long doc measured globally. Apply the removal test. The common failure is reproducing the source's contrast shape in the rewrite with new words.
2. Triples, with or without "and" → break the parallelism.
3. Balanced pairs → make asymmetric.
4. Dramatic fragmentation → prose, unless a signed-off LinkedIn stylistic.
5. Transition slop ("but here's where it gets interesting") → delete.
6. Summary sentences ("in other words...") → delete; trust the reader.
7. Sentence templates ("the [role] don't X, they Y") → the specific observation.
8. Sentence rhythm (advisory): three consecutive similar-length sentences → vary one.
9. Specificity: every claim carries a concrete detail, or it's cut.
10. Paragraph shape (advisory): vary length and shape.
11. Fragment-colon labels (script flags a cluster of 3+) → fold in or vary.
12. Self-narrated honesty ("Pipeline honesty:", "to be honest") → delete the caption, keep the claim.
13. Academic-register verbs (operationalise, stems from, predicated on) → the plain verb.

### Step 5: Self-critique pass (the voice check)

**Re-check the point.** Step 1 named the claim only someone who did the work could make. Confirm it's still on the page and hasn't been polished into mush during the sweeps. If it's gone, that's the first fix; clean vocabulary and varied rhythm on top of a draft with no actual point still reads as machine-made.

**The read-aloud test.** Read the draft as the user speaking, sentence by sentence. Any sentence they wouldn't say out loud survives or dies on that test, not on a checklist. The corpus samples and the section 9 anchors in the fingerprint are the reference for what they sound like; their own test for bad output is "doesn't sound or read like me", so apply exactly that test before they have to.

Then re-read the draft with fresh eyes and ask yourself: **"What still makes this obviously AI-generated, and does this actually sound like the user?"**

**Use the advisory signals as prompts, not verdicts.** The script's `_summary.advisory_flagged` list names where the draft may be thin: `specificity_density` (no numbers or names to hold), `stance_signal` (no opinion where one belongs), `generic_to_specific` (an abstract opener propped up by a borrowed example), `copula_ratio` (dissertation register). These never fail the piece, by design; they point the read-aloud test at the likely soft spots. For each flag, ask the matching self-check question in `references/positive-patterns.md` and fix only if the draft is genuinely anonymous, not merely short or neutral by design. Removing AI tells makes a draft clean; installing these makes it sound like a person.

Write a brief internal list of remaining tells. Common things that survive the mechanical sweep:

- Binary contrasts you diagnosed in the source and reproduced in your rewrite with different words (compare your diagnosis against your rewrite line by line)
- Overly tidy paragraph structure (each paragraph same length, same shape)
- Bland neutrality where an opinion would be more human
- Too-clean prose that reads like it was drafted six times
- The "assembled from parts" feeling where sentences don't flow naturally from one to the next
- Voice that could belong to any competent writer: no personality, no specificity, no characteristic moves

Then revise to fix those remaining tells. This second pass separates decent output from output that actually sounds human. The mechanical sweep catches the obvious patterns; this pass catches the subtle ones.

**Final character check:** Do one last literal search of the output for U+2014 (—) and U+2013 (–). The model has a strong tendency to reintroduce em dashes during revision, even after removing them in the first sweep. If any appear, fix them. Confirm at least two Australian English spelling variants are visible.

### Step 6: Verification evidence

Don't self-score on a 1–5 scale; model self-ratings cluster at 4 and tell the user nothing. Assemble the evidence instead:

1. **Script results.** The final `writing_checks.py` run, clean on the non-negotiables: em dashes, quote style matched to the medium, severity-1 slop, slop openers.
2. **A named anchor diff.** Name the corpus sample or section 9 anchor closest to this piece and state, in a line or two, where the draft diverges from it and why that's deliberate. A voice claim with no named comparison is a guess, and the model grading its own voice on feel is exactly the self-assessment this skill says not to trust. When a `profile/voiceprint.json` baseline exists, add the voiceprint distance (`humanise voiceprint <file>`) as the quantified companion: a low distance corroborates the anchor diff, a high one says re-read before presenting. It's advisory, so it informs the judgement and never replaces it.
3. **The adversarial read, for external pieces** (board paper, investor update, LinkedIn, blog, cover letter, customer-facing): one pass whose only job is to fail the draft. Assume it's AI-generated and find what gives it away (up to three things); fix them before presenting. A clean draft is a valid result: the reviewer reports that it's hard to tell apart and ships it, rather than inventing tells to hit a count. Where the stakes warrant it, run this as a separate reviewer (the `agents/adversarial-reviewer.md` subagent) rather than the persona that wrote the draft, since the writer shares the draft's blind spots.
4. **The fidelity check, for external pieces that carry claims** (numbers, names, dates, causal assertions) when a brief or source exists: confirm every specific claim is supported and the point still matches the brief. The skill pushes for specifics, and unsupported specifics are the cost; this catches a confident fabrication before it ships in the user's name. Where the stakes warrant it, run the `agents/fact-brief-checker.md` subagent over the brief plus the draft (unlike the adversarial reviewer, it receives the brief).

If any of these turns up a problem, revise and re-verify. For internal quick messages (Slack, short emails), the script run alone is enough, but the point still has to be there: a quick message with no actual point shouldn't be sent.

### Step 7: Present

Present the revised draft with the evidence in compact form: one line of script summary, the anchor diff, and anything the adversarial and fidelity passes caught and fixed. If you made non-obvious choices (chose a particular angle, cut something from the brief, went against a direction), note them briefly. Then ask: "What would you change?"

Don't finalise without feedback.

---

## Workflow: Editing existing content

When the user provides text to review or improve:

### Step 1: Assess

Check if the source is specific enough to edit. If it's so vague that cleaning up the words would produce cleaner-sounding nonsense, say so. Ask what it's actually trying to say before rewriting. Editing slop into polished slop isn't useful.

### Step 2: Diagnose

Identify what's wrong: spelling, tone, slop vocabulary, structural tells, em dashes, buzzwords, formality mismatch, padding, nominalisation.

### Step 3: Rewrite

Produce a clean rewrite. Showing is more useful than telling. Preserve the user's voice and intent while fixing the issues.

### Step 4: Mechanical sweep (both passes)

Run the same two-pass sweep from the generation workflow: pass one (character-level, items 1–9) and pass two (structural, items 1–10). Every item. Editing slop into polished slop is the trap here; the structural tells are often what's making the original feel AI-generated, not the vocabulary.

### Step 5: Self-critique pass

Run the point check from the generation workflow Step 1 first: what does this say that a generic model wouldn't? An edit can scrub every tell and still leave a piece that says nothing. Then run the read-aloud test and re-read asking: "What still makes this obviously AI-generated, and does this sound like the user?" Read the `advisory_flagged` presence-of-human signals (`specificity_density`, `stance_signal`, `generic_to_specific`, `copula_ratio`) as prompts for where the edit may have left the piece anonymous, and fix remaining tells. This pass matters as much for editing as for generation; it's easy to clean up obvious slop and leave the structural patterns intact.

### Step 6: Verification evidence

Same as the generation workflow: script results, a named anchor diff, and the adversarial read for external pieces. No self-scores.

### Step 7: Present

If the user asked for a rewrite, present it with the compact evidence. If they asked for feedback, point to specific problems with specific fixes.

Keep commentary brief. Default to producing a clean rewrite with a short note on the key changes, not a long explanation of everything you did.

---

## Workflow: Long-form documents (document mode)

Trigger this for anything over ~1500 words: pricing memos, board papers, PRDs, strategy docs, long reports. The standard workflow is built for a LinkedIn post or an email, and it breaks on long-form in three specific ways. Its budgets are per-piece ("one load-bearing contrast"), which is meaningless across sixteen sections. Its structural pass asks you to "re-read, don't search" the whole thing, and attention decays, so the misses cluster in the back half. And the corpus has fewer long-form samples to imitate, so the draft drifts toward AI document-voice exactly where the stakes are highest. Document mode exists to counter all three.

The principle: don't draft or sweep 30 pages in one pass. Chunk it, check each chunk, and check the joins. A model's attention dilutes over a long generation the same way a human's does on a long re-read; the fix is the same for both, which is to work in sections and verify the seams.

### Step D1: Outline and point-per-section

Before drafting, lay out the section structure and name the point for each section (the generation workflow's Step 1 point check, run once per section). A section with no point that only someone who did the work would make is a section to cut or merge, not to polish. Do this first; it's cheaper to fix a hollow section in the outline than after it's written.

### Step D2: Pull a long-form exemplar

Re-read the closest long-form exemplar before drafting (`profile/sample-long-form-*.md`, or the nearest `profile/sample-board-paper-*.md`, `profile/sample-prd-*.md`, or `profile/sample-investor-update-*.md`), not just the chat samples. The chat corpus nails the Slack register and tells you almost nothing about how the user builds a memo. If there's no long-form sample for this document type, say so to the user and lean on the register descriptors in `profile/register-descriptors.md`, which capture the structural habits (how they open a memo, how they handle caveats, where the opinions sit) that the chat samples can't.

### Step D3: Draft section by section

Write one section at a time against its named point and the exemplar's cadence. Don't generate the whole document in a single pass and sweep afterward; by page 20 the voice has drifted and the tells have compounded. Carry a running voice budget across sections as you go: total binary contrasts, total fragment-colon labels, total triples, measured as density over everything written so far, not reset at each section boundary. This is the single most important habit in document mode. It's what stops fifty contrasts hiding behind a per-section budget of one.

### Step D4: Per-section sweep, then a whole-document sweep

Run `writing_checks.py` on each section as you finish it (pass one and the now-automated pass two), fixing as you go. Then run it once on the assembled whole. The whole-document run catches what per-section runs cannot: the same triad surfacing in four sections, the binary-contrast density creeping over threshold across the full length, a fragment-colon label opening every section. Read the `structural_density` block in the summary; it's the document-level dashboard. This is map-reduce on the sweep, local checks per chunk and global checks on the join.

### Step D5: Mandatory adversarial reviewer (separate context)

For long-form this is not optional. Spin up the `agents/adversarial-reviewer.md` subagent (no access to the drafting context) whose only job is to fail the document. The writer shares the draft's blind spots, which is exactly why the persona that wrote fifty contrasts won't see them on re-read. Give the reviewer the `structural_density` dashboard plus the full text and this brief: assume it's AI-generated, find the tells, and specifically check for any residual binary-contrast shape in the draft itself, including ones re-clothed in fresh vocabulary that the regex misses. Fix what it finds before presenting. Where the document carries specific claims and a brief or source exists, also run the `agents/fact-brief-checker.md` subagent (which, unlike the adversarial reviewer, receives the brief) to confirm the claims are supported and the point held.

### Step D6: Present with the document-level evidence

Present the cleaned document with the compact evidence: the whole-document `structural_density` numbers, the named long-form anchor diff, and what the adversarial reviewer and fact-brief checker caught and fixed. Note any section you cut or merged for having no point. Then ask what they'd change.

---

## Quick reference

| Problem                                     | Fix                                                               |
| ------------------------------------------- | ----------------------------------------------------------------- |
| Em dash (— or –)                            | Comma, period, semicolon, or colon                                |
| Curly vs straight quotes                    | Straight in plain-text media; curly in .docx; never mixed         |
| Empty binary contrast                       | Direct statement; load-bearing form budgeted at one per piece     |
| -ize suffix                                 | Change to -ise                                                    |
| -or suffix                                  | Change to -our (colour, behaviour)                                |
| -er suffix                                  | Change to -re (centre, theatre)                                   |
| Filler opener                               | Delete. Start with content.                                       |
| Red-flag word (delve, tapestry, etc.)       | Replace with plain alternative or delete                          |
| Corporate buzzword                          | Replace with specific, plain language                             |
| Nominalisation                              | Find the verb inside the noun                                     |
| Formal hedging                              | Cut it. State the thing.                                          |
| Triple / parallel structure                 | Break the parallelism, vary length                                |
| Balanced pair                               | Make asymmetric                                                   |
| Transition slop                             | Delete or use actual logical connection                           |
| Summary sentence                            | Delete. Trust the reader.                                         |
| Excessive bullets                           | Convert to prose                                                  |
| Passive voice                               | Active where it reads better                                      |
| Sentence template                           | Say the specific thing, not the template                          |
| Fragment-colon label drumbeat               | Fold the label into the sentence; vary openers                    |
| Self-narrated honesty ("Pipeline honesty:") | Delete the caption, keep the claim                                |
| Academic verb (operationalise, stems from)  | Use the plain verb (is, has, comes from)                          |
| Long document (>1500 words)                 | Switch to document mode: chunk, per-section sweep, running budget |
