# Mechanical sweep: full item detail

`SKILL.md` holds the two-pass sweep as a checklist. This file holds the detail behind each item: what the pattern looks like, why it flags, and how to fix it. The live workflow runs the script (`evals/assertions/writing_checks.py`), which automates most of both passes; consult this file when an item needs adjudication or when no shell is available and you're scanning by hand.

Read order: run the script first, read the `structural_density` block in its `_summary`, then open the items it flagged here.

---

## Pass one (character and vocabulary level)

The script covers items 1-5 and 8-9, plus slop openers and the spaced-hyphen dash. Items 6 and 7 still need a manual scan. If any check fails, fix it and rerun the whole pass from the top; fixes often introduce new issues.

1. **Em dashes.** Search the whole output (body, headings, notes) for U+2014 (—) and U+2013 (–). Rewrite the sentence with a comma, period, semicolon, or colon. The single most recognised AI tell; zero is the target, one undermines the piece.
2. **Curly/smart quotes: match the medium.** Plain-text media (Slack, email, markdown): straight quotes; curly signals pasted-from-a-word-processor. A `.docx` or typeset deliverable: curly is the human default (autocorrect produces it), so straight is the tell. Never mix the two in one piece.
3. **Severity-1 slop words.** delve, tapestry, multifaceted, nuanced, landscape (metaphorical), realm, embark, endeavour, intricate, intricacies, pivotal, meticulous, testament, interplay. Replace with the plain alternative from `ai-slop-dictionary.md` or delete. Any one flags a short piece.
4. **Copula avoidance.** "serves as", "stands as", "functions as", "boasts", "features" (when "is"/"has" would work). Use "is" or "has".
5. **Severity 2-3 slop clustering.** leverage, utilise, facilitate, robust, seamless, foster, transformative, comprehensive, holistic, and the rest. One or two in a long piece is fine; three in a paragraph is a rewrite.
6. **-ing phrase chains** (manual). Sentences ending in participles added for fake depth: "...highlighting X", "...showcasing Y", "...contributing to Z". Delete the tail or fold it into a new sentence.
7. **Formatting tells** (manual). Excessive boldface, inline-header lists ("**Header:** content"), emoji, Title Case Headings, decorative dividers, over-bulleting. If it would read naturally as prose, write it as prose.
8. **Australian English visible.** Any word with an AusE form takes it: -ise, -our, -re, -ement, -ll-. In a piece longer than a sentence, two or more usually surface on their own. Don't swap in near-synonyms to hit the count; that makes the prose worse. Avoid "optimised" as a default substitute (flagged as slop without concrete metrics). Full variant rules in `cultural-calibration.md`.
9. **Contractions.** At least three distinct types in anything longer than a paragraph (don't, it's, we're, I've, can't). Zero contractions reads as stilted. A tripwire, not a quota.

---

## Pass two (structural level)

The script detects most of these; your job is adjudication, not detection. Start from the `structural_density` block, open every hit, and decide which stay and which get rewritten. The re-read still matters for the patterns no regex catches (balanced pairs, paragraph shape, the "assembled from parts" feeling). Full taxonomy in `structural-tells.md`.

1. **Binary contrast, all forms.** Obvious ("It's not X, it's Y"), moderate ("Not just X, but Y"), inline ("X, not Y"), and negated-copula ("isn't X, it's Y"). Empty contrasts get rewritten every time: state the positive claim only. Load-bearing contrasts are budgeted by density: one on a short piece, roughly one per 600 words across a long document, measured globally. Apply the removal test in `structural-tells.md`. For detector-bound copy (sales, formal submissions), drop even the load-bearing form. The most common failure is diagnosing a contrast in the source and reproducing its shape in the rewrite with different words.
2. **Triples.** Three parallel items, with or without "and" ("fast, reliable, and secure"; "Ship fast, learn deeply, repeat endlessly"). Break the parallelism: cut one, fold two together, or vary the lengths. Two reads as a pair; three scans as AI cadence.
3. **Balanced pairs.** Mirrored positive/negative clauses ("When X, we succeed. When not-X, we fail."). Rewrite asymmetrically so the clauses differ in shape and length.
4. **Dramatic fragmentation.** One-word sentences stacked for effect ("Ship. Learn. Repeat."). Fine for a LinkedIn post with the user's explicit sign-off; otherwise convert to prose.
5. **Transition slop.** "But here's where it gets interesting", "And here's the kicker". Delete and let the next sentence carry itself.
6. **Summary sentences.** The final "In other words..." or "The takeaway is..." that restates the point. Trust the reader. Delete.
7. **Sentence templates.** "The [role] don't [verb]. They [elevated verb]." Replace with a specific observation.
8. **Sentence rhythm.** Three consecutive sentences within five words of each other in length. Break the pattern. (Tripwire, advisory in the script.)
9. **Specificity check.** Every claim needs a concrete detail. If a sentence would work with different nouns swapped in, add a number, a name, an example, or delete.
10. **Paragraph shape.** All paragraphs the same length and shape is itself a tell. Vary deliberately. (Advisory.)
11. **Fragment-colon labels.** "The recommendation." / "The ask." / "The key finding:" opening section after section. The script flags a cluster of three or more; vary them or fold the label into the first sentence.
12. **Self-narrated honesty.** "Pipeline honesty:", "the honest version of", "to be honest". The writing captioning its own candour. Delete the caption, keep the claim.
13. **Academic-register verbs.** "operationalises", "underpins", "stems from", "predicated on", "constitutes", "indicative of". Map each back to the plain verb (see `ai-slop-dictionary.md`).

---

## How this maps to the script output

| Checklist item | Script field (`_summary.structural_density` or check name) |
| --- | --- |
| Em dashes | `em_dash`, `en_dash_non_range`, `spaced_hyphen_dash` |
| Curly quotes | `curly_quotes` (medium-aware) |
| Severity-1 slop | `severity_1_slop` |
| Severity 2-3 slop | `severity_2_3_slop` |
| Binary contrast (all four forms) | `binary_contrasts_per_1000`, `structural_tell_total` |
| Fragment-colon labels | `fragment_colon_labels` |
| Self-narrated honesty | `self_narrated_honesty` |
| Academic register | `academic_register` |
| Sentence rhythm | `sentence_profile` (advisory) |
| Burstiness | `burstiness_cov` (advisory) |
| AusE visible / contractions | `ause_visible`, `contractions` (advisory tripwires) |

Items 6, 7 (pass one) and 3, 9, 10 (pass two) have no script field and need the manual re-read.
