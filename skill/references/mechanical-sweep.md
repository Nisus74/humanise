# Mechanical sweep: full item detail

`SKILL.md` holds the two-pass sweep as a checklist. This file holds the detail behind each item: what the pattern looks like, why it flags, and how to fix it. The live workflow runs the script (`evals/assertions/writing_checks.py`), which automates most of both passes; consult this file when an item needs adjudication or when no shell is available and you're scanning by hand.

Read order: run the script first, read the `structural_density` block in its `_summary`, then open the items it flagged here.

---

## Pass one (character and vocabulary level)

The script covers items 1-5 and 8-9, plus slop openers and the spaced-hyphen dash. Items 6 and 7 still need a manual scan. If any check fails, fix it and rerun the whole pass from the top; fixes often introduce new issues.

1. **Em dashes.** Search the whole output (body, headings, notes) for U+2014 (—) and non-range U+2013 (–). If the user's confirmed rules ban them, rewrite with a comma, period, semicolon, or colon. Otherwise check for repetitive or model-like use and preserve a natural instance.
2. **Curly/smart quotes: match the medium.** Plain-text media (Slack, email, markdown): straight quotes; curly signals pasted-from-a-word-processor. A `.docx` or typeset deliverable: curly is the human default (autocorrect produces it), so straight is the tell. Never mix the two in one piece.
3. **Severity-1 slop words.** delve, tapestry, multifaceted, nuanced, landscape (metaphorical), realm, embark, endeavour, intricate, intricacies, pivotal, meticulous, testament, interplay. Replace with the plain alternative from `ai-slop-dictionary.md` or delete. Any one flags a short piece.
4. **Copula avoidance.** "serves as", "stands as", "functions as", "boasts", "features" (when "is"/"has" would work). Use "is" or "has".
5. **Severity 2-3 slop clustering.** leverage, utilise, facilitate, robust, seamless, foster, transformative, comprehensive, holistic, and the rest. One or two in a long piece is fine; three in a paragraph is a rewrite.
6. **-ing phrase chains** (manual). Sentences ending in participles added for fake depth: "...highlighting X", "...showcasing Y", "...contributing to Z". Delete the tail or fold it into a new sentence.
7. **Formatting tells** (manual). Excessive boldface, inline-header lists ("**Header:** content"), emoji, Title Case Headings, decorative dividers, over-bulleting. If it would read naturally as prose, write it as prose.
8. **Dialect consistency.** Use the configured spelling when a variant naturally appears. Never swap in a near-synonym merely to display the dialect. Full variant rules live in `cultural-calibration.md`.
9. **Contractions.** Check whether their presence or absence matches the user's evidence, channel and register. Zero contractions may signal an unintended formal drift; it is not a failure by itself.

---

## Pass two (structural level)

The script detects most of these; your job is adjudication, not detection. Start from the `structural_density` block, open every hit, and decide which stay and which get rewritten. The re-read still matters for the patterns no regex catches (a single balanced pair, paragraph shape, the "assembled from parts" feeling); the script now flags the balanced-pair *cluster* and the transition-opener *pileup*, but the single instances are still yours. Full taxonomy in `structural-tells.md`.

1. **Binary contrast, all forms.** Obvious ("It's not X, it's Y"), moderate ("Not just X, but Y"), inline ("X, not Y"), and negated-copula ("isn't X, it's Y"). Rewrite an empty contrast by stating the positive claim. Preserve a specific, load-bearing contrast when it is supported by the user's voice and does analytical work. Repetition across a piece is the stronger warning. The most common failure is diagnosing a contrast in the source and reproducing its shape with replacement vocabulary.
2. **Triples.** Three parallel items can be a model habit, but factual lists of three are ordinary writing. Rewrite when the cadence is ornamental, repeated or unsupported by the user's samples. Preserve a list when all three items are required.
3. **Balanced pairs.** Mirrored positive and negative clauses can sound templated when repeated. Rewrite a cluster or an empty rhetorical mirror. Preserve a single pair when the logic genuinely benefits from comparison.
4. **Dramatic fragmentation.** One-word sentences stacked for effect ("Ship. Learn. Repeat."). Fine for a LinkedIn post with the user's explicit sign-off; otherwise convert to prose.
5. **Transition slop.** "But here's where it gets interesting", "And here's the kicker". Delete and let the next sentence carry itself. The quieter cousin, a pileup of sentence-initial connectives (Moreover, Furthermore, Additionally), is a hard flag (`transition_pileup`) at two or more.
6. **Summary sentences.** The final "In other words..." or "The takeaway is..." that restates the point. Trust the reader. Delete.
7. **Sentence templates.** "The [role] don't [verb]. They [elevated verb]." Replace with a specific observation. The script catches this form and the cross-sentence reframe ("This isn't X. It's Y.") via `structural_tell_total`; the noun-dependent templates ("X is the new Y") stay manual.
8. **Sentence rhythm.** Similar sentence lengths may signal drift when the whole passage feels mechanical. Change the rhythm only when the read improves.
9. **Specificity check.** Important claims need support. Add only details supplied by the user or a source; never manufacture specificity.
10. **Paragraph shape.** Uniform paragraphs can feel assembled from a template. Vary them when the argument calls for it, not to manufacture irregularity.
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
| Binary contrast (all forms) + cross-sentence reframe | `binary_contrasts_per_1000`, `structural_tell_total` |
| Transition-opener pileup | `transition_openers` (hard at 2+) |
| Fragment-colon labels | `fragment_colon_labels` |
| Self-narrated honesty (incl. "real talk", "not gonna lie") | `self_narrated_honesty` |
| Academic register | `academic_register` |
| Approximation hedges | `approximation_hedges` (advisory) |
| Dead metaphor-verb cluster | `dead_verb_density` (advisory) |
| Balanced-pair cluster | `balanced_pairs` (advisory) |
| Sentence rhythm | `sentence_profile` (advisory) |
| Burstiness | `burstiness_cov` (advisory) |
| AusE visible / contractions | `ause_visible`, `contractions` (advisory tripwires) |

Items 6, 7 (pass one) and 9 (pass two: specificity) have no script field and need the manual re-read; item 3 (balanced pairs) and item 10 (paragraph shape) are now partly covered (the cluster, advisory) but the single instance is still manual.
