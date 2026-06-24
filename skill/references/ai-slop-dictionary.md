# AI Slop Dictionary

A comprehensive reference of words, phrases, and patterns that signal AI-generated writing. Organised by category and severity.

This isn't about banning words from the English language. Many of these words are perfectly fine in the right context. The problem is frequency and clustering: AI reaches for these words far more often than humans do. "Delve" isn't inherently bad, but it appears 48x more often in AI text than human writing. When three or four of these cluster in a paragraph, the writing gets flagged.

The fix is almost always the same: say what you actually mean, in plainer language.

---

## Table of Contents

1. [Severity 1: Red flag words](#severity-1-red-flag-words)
2. [Severity 2: Overused vocabulary](#severity-2-overused-vocabulary)
3. [Severity 3: Corporate buzzwords](#severity-3-corporate-buzzwords)
4. [Severity 4: Verbose phrases](#severity-4-verbose-phrases)
5. [Severity 5: Filler openers](#severity-5-filler-openers)
6. [Severity 6: Hidden verbs (nominalisation)](#severity-6-hidden-verbs)
7. [Severity 7: Hedging and padding](#severity-7-hedging-and-padding)

---

## Severity 1: Red flag words

These words appear dramatically more often in AI text than human text. Even one of these in a short piece will get it flagged. Replace with plain alternatives or delete entirely.

The multipliers below are directional, not precise constants. They're drawn from published comparisons of AI-generated and human corpora (the "delve" spike is the most widely reported, tied to the rise of instruction-tuned models from 2023 on), but the exact ratio shifts with the study, the corpus, and the model generation. Read each as "heavily over-represented in AI text", not as a measured figure you could cite in a paper. The ranking matters more than the number.

| Word                      | Over-representation in AI text (approx.) | Instead                                         |
| ------------------------- | ---------------------------------------- | ----------------------------------------------- |
| delve                     | 48x                                      | explore, examine, look at, dig into             |
| tapestry                  | 35x                                      | mix, combination, range (or describe the thing) |
| multifaceted              | 28x                                      | complex, varied (or describe the facets)        |
| nuanced                   | 24x                                      | subtle, detailed (or describe the nuance)       |
| landscape                 | 20x (metaphorical)                       | market, field, space (or be specific)           |
| realm                     | 18x                                      | area, field, domain                             |
| embark                    | 15x                                      | start, begin                                    |
| endeavour                 | 14x                                      | effort, attempt, try                            |
| intricate / intricacies   | 13x                                      | complex, detailed (or describe what's complex)  |
| pivotal                   | 12x                                      | important, key, critical                        |
| meticulous / meticulously | 11x                                      | careful, thorough, detailed                     |
| testament                 | 10x                                      | proof, evidence, sign                           |
| interplay                 | 10x                                      | relationship, interaction, connection           |

Note on "endeavour": it's flagged in its "effort/attempt" sense, and it's also the AusE spelling of the same word. Being Australian doesn't rescue it; replace with "effort" or "attempt", and never count "endeavour" toward AusE visibility.

---

## Severity 2: Overused vocabulary

Words that aren't exclusively AI but appear far more often in AI output than human writing. One or two in a long piece is fine. Three or more in a paragraph is a tell.

### Adverbs that scream AI

If three or more of these appear in a paragraph, it reads as AI-generated.

| Word          | Instead                                          |
| ------------- | ------------------------------------------------ |
| literally     | (delete, or use only for actual literal meaning) |
| incredibly    | very, extremely (or quantify)                    |
| fundamentally | (delete, or say what's fundamental about it)     |
| genuinely     | (delete, or explain why it's genuine)            |
| essentially   | (delete — it rarely adds meaning)                |
| significantly | (quantify the significance)                      |
| arguably      | (state the argument instead)                     |
| undeniably    | (state the evidence instead)                     |
| remarkably    | (say what's remarkable)                          |
| interestingly | (say what's interesting)                         |
| notably       | (just state the notable thing)                   |
| particularly  | especially (or delete)                           |
| ultimately    | (delete, or say "in the end")                    |
| moreover      | also, and (or just start the next sentence)      |
| furthermore   | also, and (or delete)                            |
| consequently  | so, as a result                                  |

### Adjectives that mean nothing

Vague intensifiers that could describe anything. They add word count without adding meaning.

| Word             | Instead                            |
| ---------------- | ---------------------------------- |
| robust           | (describe what it handles)         |
| seamless         | (describe the integration)         |
| cutting-edge     | (describe the technology)          |
| state-of-the-art | (describe the technology)          |
| innovative       | (describe what's different)        |
| revolutionary    | (describe what changed)            |
| transformative   | (describe the transformation)      |
| world-class      | (delete or quantify)               |
| best-in-class    | (delete or quantify)               |
| comprehensive    | (describe the scope)               |
| holistic         | complete, full (or describe scope) |
| vibrant          | (describe what makes it vibrant)   |
| compelling       | (describe why it compels)          |
| crucial          | important, key (or explain why)    |
| enduring         | lasting (or describe duration)     |

### Verbs that sound smart but aren't

| Word                       | Instead                           |
| -------------------------- | --------------------------------- |
| leverage                   | use                               |
| utilise                    | use                               |
| facilitate                 | allow, enable, help               |
| optimise (without metrics) | improve (with specifics)          |
| harness                    | use, apply                        |
| navigate (metaphorical)    | handle, manage, work through      |
| garner                     | get, earn, attract                |
| bolster                    | strengthen, support               |
| underscore                 | highlight, show                   |
| foster                     | encourage, support, build         |
| spearhead                  | lead                              |
| catalyse                   | trigger, cause, start             |
| streamline                 | simplify (or describe the change) |
| empower                    | allow, enable                     |
| enhance                    | improve (with specifics)          |

### Copula avoidance verbs

AI avoids simple "is"/"are"/"has" and substitutes elaborate alternatives. These are a strong tell when clustered.

| Word                           | Instead |
| ------------------------------ | ------- |
| serves as                      | is      |
| stands as                      | is      |
| functions as                   | is      |
| represents (when meaning "is") | is      |
| marks (when meaning "is")      | is      |
| boasts                         | has     |
| features (when meaning "has")  | has     |
| offers (when meaning "has")    | has     |

---

## Severity 3: Corporate buzzwords

These aren't exclusively AI tells but they make writing sound corporate and generic. Replace with plain language.

| Banned                         | Instead                                     |
| ------------------------------ | ------------------------------------------- |
| synergy                        | (describe the actual benefit)               |
| paradigm                       | approach, method, model                     |
| scalable (without context)     | (describe the limits or capacity)           |
| value-add                      | benefit, advantage                          |
| thought leadership             | expertise, point of view                    |
| low-hanging fruit              | quick wins, easy fixes                      |
| bandwidth                      | time, capacity                              |
| circle back                    | follow up, revisit                          |
| touch base                     | check in, catch up                          |
| deep dive                      | detailed look, analysis                     |
| move the needle                | make a difference, improve (with specifics) |
| at the end of the day          | (delete)                                    |
| going forward                  | (delete, or say "from now on")              |
| best practices                 | what works, standards                       |
| learnings                      | lessons, what we learned                    |
| ideate                         | brainstorm, come up with ideas              |
| actionable insights            | (state the insight and the action)          |
| net-net                        | (state the conclusion)                      |
| on the same page               | aligned, agreed                             |
| take it offline                | discuss separately                          |
| double-click on                | look more closely at                        |
| unpack                         | explain, break down                         |
| at the intersection of X and Y | (describe the actual connection)            |

---

## Severity 4: Verbose phrases

Phrases that use more words than needed. The fix is almost always shorter.

| Verbose                                           | Fix                                  |
| ------------------------------------------------- | ------------------------------------ |
| "In order to..."                                  | "To..."                              |
| "It's important to note that..."                  | (just state it)                      |
| "It should be noted that..."                      | (just state it)                      |
| "It's worth noting that..."                       | (just state it)                      |
| "Please note that..."                             | (just state it)                      |
| "As mentioned earlier..."                         | (delete or link)                     |
| "In this document, we will..."                    | (just start)                         |
| "This allows users to..."                         | "Users can..."                       |
| "The system will..." / "The platform provides..." | (name the component)                 |
| "...and more!"                                    | (list what you mean or delete)       |
| "...etc." at end of a short list                  | (complete the list or use "such as") |
| "regarding"                                       | "about"                              |
| "commence"                                        | "start"                              |
| "prior to"                                        | "before"                             |
| "in the event of"                                 | "if"                                 |
| "in relation to"                                  | "about"                              |
| "with respect to"                                 | "about" / "for"                      |
| "given that"                                      | "because"                            |
| "as a result of"                                  | "because of"                         |
| "This function is responsible for..."             | (describe what it does)              |
| "in today's [adjective] [noun]..."                | (delete — say what you mean)         |
| "a wide range of"                                 | many, various                        |
| "in a timely manner"                              | quickly, on time                     |
| "at this point in time"                           | now                                  |
| "due to the fact that"                            | because                              |
| "for the purpose of"                              | to, for                              |
| "in the process of"                               | (delete — use the verb)              |

---

## Severity 5: Filler openers

Never start a response or paragraph with these. They delay the actual point.

### Chatbot openers (never use)

"Certainly!", "Great question!", "Of course!", "Absolutely!", "Sure!", "Happy to help!", "I'd be happy to...", "Definitely!", "Of course I can...", "That's a great point!"

### Throat-clearers (never use)

"Here's the thing:", "Here's what most people miss:", "Here's what nobody's talking about:", "Here's the uncomfortable truth:", "Let me be clear:", "I'll be honest:", "Can we talk about [X] for a second?", "Let's talk about [X].", "We need to talk about [X].", "Let's dive in.", "Gone are the days...", "Whether you're [X] or [Y]..." (audience-pander; pick one reader and write to them)

The formula "Here's + [dramatic noun]" is a stalling device. If you have something interesting to say, say it. If you don't, no opener will fix that.

### False exclusivity hooks (never use)

"What most people don't realise...", "The secret that top [X] know...", "Nobody is talking about this...", "Most people get this wrong...", "The hidden truth about..."

These promise insider knowledge and deliver generic observations.

### Manufactured urgency (never use)

"This changes everything.", "Drop everything.", "Buckle up.", "You need to see this.", "Read that again.", "Let that sink in.", "Full stop.", "The possibilities are endless.", "Act accordingly."

Creating artificial time pressure on information that has no expiration date.

---

## Severity 6: Hidden verbs

Nominalisation, turning verbs into nouns, is both a corporate and AI tell. It makes sentences longer and weaker. The fix is to find the verb hiding inside the noun.

| Bloated                    | Direct        |
| -------------------------- | ------------- |
| make a decision            | decide        |
| provide support            | help, support |
| conduct a review           | review        |
| give consideration to      | consider      |
| reach a conclusion         | conclude      |
| make an improvement        | improve       |
| provide assistance         | help          |
| carry out an investigation | investigate   |
| achieve a reduction        | reduce        |
| make an adjustment         | adjust        |
| perform an analysis        | analyse       |
| take into consideration    | consider      |
| have an impact on          | affect        |
| make a recommendation      | recommend     |
| give an indication         | indicate      |

Signal phrases: "make a", "provide a", "conduct a", "give a", "carry out a", "perform a", "take a" followed by a noun. There's almost always a simpler verb inside the noun.

---

## Severity 7: Hedging and padding

### Formal hedging

Cut entirely. State things as facts or qualify with specifics.

"This might potentially...", "It could arguably be said that...", "One might suggest that...", "It is perhaps worth considering...", "There is reason to believe that..."

If something is uncertain, say why it's uncertain. Don't hedge the hedge.

### Padding words

Words that add syllables but not meaning. Delete on sight unless they're genuinely needed for clarity.

"very", "really" (as intensifiers), "quite", "rather", "somewhat", "fairly", "actually" (when not contrasting), "basically", "just" (as filler), "simply" (as filler)

---

## Severity 2.5: Newer 2026 vocabulary

As the classic red-flag words became widely flagged, model output shifted toward a subtler register that's harder to catch because each word is individually defensible. Watch for clustering, same rule as the rest: one is fine, three in a paragraph is a tell.

| Word/phrase                                 | Why it flags                                 | Instead                                       |
| ------------------------------------------- | -------------------------------------------- | --------------------------------------------- |
| underpin / underpinned                      | over-used connective for "is the basis of"   | support, sit under (or name the relationship) |
| crucially / critically (as sentence adverb) | signals significance the content should show | (delete, or state why it's critical)          |
| stark (reminder, contrast, difference)      | stock intensifier                            | (describe the actual difference)              |
| telling (as in "a telling sign")            | editorialises without evidence               | (state what it tells you)                     |
| resonate / resonates                        | vague emotional claim                        | (say what connects and why)                   |
| speaks to / speaks volumes                  | evasive attribution                          | (state the point directly)                    |
| at its core / at the heart of               | filler throat-clearer                        | (just state the core thing)                   |
| compelling case / compelling reason         | tells the reader to be persuaded             | (make the case; let them judge)               |
| it's worth noting / worth highlighting      | stalling before a point                      | (just make the point)                         |
| double-edged sword                          | tired metaphor for a tradeoff                | (name both sides specifically)                |
| testament to (resurfacing)                  | see Severity 1; still appears                | proof, evidence, sign                         |
| increasingly (as scene-setter)              | fake trend signal                            | (cite the change, or cut)                     |

These pair with the structural patterns in `structural-tells.md`, especially "hedged confidence" and the "concessive pivot". Vocabulary and structure reinforce each other; a piece heavy in this register usually has the structural tells too.

---

## Severity 2.5b: Academic-register verbs

The fancier cousins of copula avoidance (serves as, functions as). They swap the crisp first person for a dissertation register, and they cluster in long documents where the draft has drifted formal. `writing_checks.py` (`academic_register`) counts them; pass is two or fewer. Same clustering rule: one is tolerable, three is a rewrite.

| Word/phrase                                     | Why it flags                                           | Instead                                |
| ----------------------------------------------- | ------------------------------------------------------ | -------------------------------------- |
| operationalise / operationalises                | register-paper verb for "turn into a measurable thing" | measure, make concrete, put numbers on |
| stems from / stemming from                      | over-used connective                                   | comes from, is caused by               |
| predicated on / upon                            | legalistic for "depends on"                            | depends on, rests on                   |
| constitutes / constituted                       | inflated "is"                                          | is, makes up                           |
| encompasses                                     | inflated "covers"                                      | covers, includes                       |
| indicative of / illustrative of / reflective of | hedged "shows"                                         | shows, points to                       |
| necessitates                                    | inflated "needs"                                       | needs, forces, means                   |
| contingent upon                                 | legalistic "depends on"                                | depends on                             |
| by virtue of                                    | throat-clearer for "because"                           | because                                |
| delineate / delineates                          | inflated "set out"                                     | set out, draw the line                 |

The fix is always the plain verb. If "operationalises a falsifier" is the sentence, the question is what it actually does: it turns a claim into something the pilot can measure. Write that.

---

## Severity 2: Self-narrated honesty

The writing captioning its own candour instead of just being candid: "Pipeline honesty:", "the honest version of", "an honest label", "to be honest", "the straightforward statement is", "candidly", "let me be clear". It's a trust-me reflex models reach for and people almost never use, because a person being straight doesn't announce it. `writing_checks.py` (`self_narrated_honesty`) flags every instance; the target is zero.

| Phrase                                                   | Why it flags                              | Instead                        |
| -------------------------------------------------------- | ----------------------------------------- | ------------------------------ |
| honestly / to be honest / in all honesty                 | captions candour the content should carry | (delete; just say the thing)   |
| the honest version / the honest answer / the honest read | signals the rest was dishonest            | (state it directly)            |
| an honest label / an honest assessment                   | self-congratulatory framing               | (give the label; let it stand) |
| "Pipeline honesty:" and any "<Noun> honesty:" label      | a heading that performs candour           | (use a plain heading, or none) |
| let's be clear / let me be clear                         | stalls before a point                     | (make the point)               |
| the truth is / truth be told / the real answer is        | melodramatic reveal                       | (just reveal it)               |
| candidly / frankly / plainly put                         | tells the reader how to read you          | (delete)                       |

The rewrite rule is one move: delete the caption, keep the claim. "Pipeline honesty: Intake has no live deals today" becomes "Intake has no live deals today." The fact does the work; the label only flagged that a model wrote it.

---

## Severity 2.6: Stolen-engineer and marketing diction (2025)

Engineering and product words that turned into AI flavour once they leaked into training data around late 2024. Each is individually defensible, which is why they slip through; the tell is the vague-impact claim they stand in for. From the impeccable.design STYLE.md denylist. `writing_checks.py` counts these with the severity 2-3 slop; pass is two or fewer.

| Word/phrase | Why it flags | Instead |
| --- | --- | --- |
| load-bearing | Vague claim of importance; the literal sense is rare in prose | Name the specific thing it does |
| highest-leverage | Vague impact claim | Say what specifically pays off |
| biggest unlock | Marketing-speak for "the change" | Describe the actual change |
| data-driven | Empty marketing adjective | Cite the data ("validated against 15 briefs") |
| elevate / elevates | Marketing verb | The specific verb: improve, raise, sharpen |
| underscore / underscores | Connective AI tell | "Show", "make clear" |

Two openers from the same source sit with the filler openers (Severity 5): "gone are the days" and "whether you're X or Y" (audience-pander). One structural move, the negation pivot "less about X, more about Y", is a binary-contrast variant the script flags as `negation_pivot`; see `structural-tells.md`.

## Using this dictionary

When generating or editing content:

1. Don't memorise every entry. Instead, develop a feel for the patterns: vague intensifiers, corporate nouns, stalling openers, smart-sounding verbs that say nothing.
2. The fix is almost always: be specific, be shorter, or delete.
3. Context matters. "Navigate" is fine when describing actual navigation. "Leverage" in a physics paper is correct. The problem is metaphorical overuse in business writing.
4. If you catch yourself reaching for a word on this list, ask: what am I actually trying to say? Say that instead.
