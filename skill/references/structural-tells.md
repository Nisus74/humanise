# Structural AI Tells

Individual word choices are the most obvious AI tells, but structural patterns are harder to catch and often more damaging. A piece of writing can avoid every word on the slop list and still read as AI-generated because of how it's built.

These patterns aren't bad writing per se. Each one works because it mimics effective human rhetoric. The problem is that AI reaches for them constantly, so they've become signatures.

---

## Table of Contents

1. [The binary contrast](#the-binary-contrast)
2. [The triple](#the-triple)
3. [The balanced pair / mirror](#the-balanced-pair)
4. [Dramatic fragmentation](#dramatic-fragmentation)
5. [The fragment-colon drumbeat](#the-fragment-colon-drumbeat)
6. [The ladder of escalation](#the-ladder-of-escalation)
7. [False agency](#false-agency)
8. [Generic-to-specific](#generic-to-specific)
9. [Transition slop](#transition-slop)
10. [The qualifier sandwich](#the-qualifier-sandwich)
11. [Closer slop](#closer-slop)
12. [Sentence templates](#sentence-templates)
13. [The summary sentence](#the-summary-sentence)
14. [Question restating](#question-restating)

---

## The binary contrast

One of the most overused AI writing structures. Set up what something ISN'T, then reveal what it IS. Creates the illusion of insight through contrast.

The pattern is a detection tell at the syntactic level. Detection tools flag the shape regardless of substance. Most instances need rewriting. The carve-out below covers the narrow case where the contrast is doing real analytical work.

### Two forms

**Empty form (rewrite every time).** Both halves are abstract. The "not X" could be any plausible claim and the "but Y" restates the main point. The contrast is rhetorical balance, not argument. Examples:

- "It's not about the product, it's about the customer."
- "The problem isn't technology, it's people."
- "This isn't just a feature, it's a platform."
- "Not just X, but Y." / "Not only X, but also Y."
- Inline: "decisions based on evidence, not opinion"

For empty contrasts, state the positive claim and drop the negation. "Put the customer first" does the same work as "It's not about the product, it's about the customer."

**Load-bearing form (allow, but budget: one per piece).** The contrast names what actually mattered by rejecting a plausible-but-wrong alternative a reader would reasonably assume. The "not X" is a specific candidate, not an abstraction; the "but Y" is the specific thing that was true instead. Examples of the move working:

- "That's what convinced seven organisations across four sectors, not the accuracy figure." (The reader would reasonably assume accuracy was the sell. Naming what actually closed the deal is the whole point of the sentence.)
- "That governance challenge, not the model itself, is what attracted me to Provation's Mira iPro Insights." (Reframes the candidate's apparent interest away from the obvious technical hook toward the harder, more specific problem.)
- "The harder problem was audit traceability. That governance layer took longer to get right than the models did." (Two-sentence form doing the same reframe work.)

### Surface variants the script catches

The same negate-then-reveal move wears several surfaces: classic ("it's not X, it's Y"), inline ("X, not Y"), not-just ("not just X, but Y"), negated-copula ("isn't X, it's Y"), and the **negation pivot** ("less about X, more about Y"). `writing_checks.py` flags all of these (the last as `negation_pivot`). A close relative is the **audience-pander opener** ("whether you're X or Y..."), which performs balance while addressing no one; pick one reader and write to them. (Variants surfaced via the impeccable.design STYLE.md denylist.)

### How to judge

If you remove the negation, does the remaining sentence still say the same thing? If yes, the contrast was empty and the rewrite was already there in the positive half. If removing the negation collapses a real reframe, the contrast was load-bearing and naming the plausible-wrong alternative is the argument.

### Budget

At most one load-bearing contrast per piece. More than one starts to read as template, and the reader stops experiencing the reframes as discoveries and starts seeing them as a rhetorical move the writer is leaning on.

On a long document the budget is a density, not a flat count. A 30-page memo with one load-bearing contrast per section has sixteen of them, and that reads as a tic no matter how good each one is in isolation. Hold it to roughly one per 600 words across the whole document, measured globally, not reset per section. `writing_checks.py` (`binary_contrast_density`) reports the contrasts-per-1000-words rate so you can see when a long piece has drifted over the line. The per-section feeling of "this is my one allowed contrast" is exactly the trap: each section gets its one, and the document accumulates fifty.

### Why this matters

The skill's purpose is to strip AI tells, not to strip moves that happen to share a shape with AI writing. The load-bearing carve-out protects a specific, opinionated analytical move used in well-written cover letters, investor updates, and board papers. Blanket ban flattens the prose into something correct but tonally neutered.

### Detection-tool risk

Even a load-bearing contrast can trigger syntactic detectors. If the piece is going somewhere that will be scanned (sales copy going through a buyer's AI detection workflow, academic or regulatory submission, published journalism), drop the load-bearing form too. The carve-out applies to ordinary professional writing where the reader is a human making a judgement about voice and argument, not a machine matching patterns.

---

## The triple

Three items in a row with identical grammatical structure. Often formatted as a list or a comma-separated series.

**Patterns:**

- "Ship things that matter, cut the ones that don't, stay close to users throughout."
- "We need speed, quality, and reliability."
- "Build faster. Ship smarter. Scale bigger."
- Any three-part list where each item has the same verb-noun-modifier rhythm.

**Why it's a tell:** The "rule of three" is a real rhetorical device, but AI applies it mechanically. When every list has exactly three items with parallel grammar, it reads like a template. Real people sometimes list two things, sometimes four, and don't maintain perfect parallel structure.

**Fix:** Break the parallelism. Make one item longer than the others. Use two items instead of three. Or collapse the list into a sentence: "We need to ship things that matter and stay close to users while we do it."

---

## The balanced pair

Two clauses with perfectly mirrored structure, one positive and one negative (or one showing success and one failure).

**Patterns:**

- "When these elements align, teams ship great products. When they don't, teams build features no one uses."
- "If A, then B. If not A, then C."
- "The companies that do X will thrive. The companies that don't will be left behind."
- "Where there's clarity, there's progress. Where there's confusion, there's waste."

**Why it's a tell:** Humans rarely write with this much symmetry. The perfectly balanced "When X / When not-X" or "If A / If not A" structure is mechanical. Real people give more weight to one side or break the pattern.

**Fix:** Give the two halves different weight or rhythm. Make one longer than the other. Or just state the positive case and let the reader infer the negative: "Teams ship great products when these elements align." The failure case is obvious; you don't need to spell it out.

---

## Dramatic fragmentation

Short. Sentences. For. Effect. Using sentence fragments to create artificial gravitas or emphasis.

**Patterns:**

- "One word. Execution."
- "The result? Silence."
- "Full stop."
- Starting paragraphs with sentence fragments for drama.
- One-word paragraphs.

**Why it's a tell:** Humans use fragments occasionally and naturally. AI uses them rhythmically, often in sequences, and always to manufacture drama. The pattern is especially common in LinkedIn-style content.

**Fix:** If you need emphasis, use a short full sentence. "Execution was the only thing that mattered" is stronger than "One word. Execution." because it doesn't perform its own importance.

---

## The fragment-colon drumbeat

A close cousin of dramatic fragmentation, specific to documents. A short label-fragment opens a section, then the real sentence follows: "The recommendation. Adopt Price Book." / "The ask. The cash inputs come first." / "The key finding:" / "The constraint is cash." One is a clean, punchy beat. The tell is the repetition: the same shape opening section after section, which turns a stylistic choice into a template.

**Patterns:**

- "The recommendation." / "The ask." / "The upshot." opening consecutive sections
- "The X:" label-then-colon used as a recurring section header
- A noun-phrase fragment standing in for a topic sentence, three or more times in a document

**Why it's a tell:** A model writing a long document reaches for the same emphatic opener every time it starts a new section, because the shape feels authoritative. A person varies it: some sections open with the fragment, most just start with the sentence. `writing_checks.py` (`fragment_colon_headers`) flags a cluster of three or more; below that it stays quiet, because the single deliberate beat is fine.

**Fix:** Keep at most one or two across a document. For the rest, fold the label into the first sentence ("Adopt Price Book as the standard offer") or just start with the sentence. The information survives; only the drumbeat goes.

---

## The ladder of escalation

Each line slightly bigger than the last, building manufactured momentum toward a conclusion.

**Patterns:**

- "First, we improved our process. Then, we transformed our approach. Finally, we revolutionised the industry."
- "It started as a project. It became a movement. It changed everything."
- Any sequence where each step uses a grander verb or claim than the previous one.

**Why it's a tell:** This is narrative structure as a formula. The escalation is predictable after the first line. Real narrative tension comes from specificity and surprise, not from ratcheting up the adjectives.

**Fix:** State the most important thing first. If there was a progression, describe it with specifics rather than escalating abstractions.

---

## False agency

Giving inanimate things human powers to avoid naming who actually did something.

**Patterns:**

- "The data tells us..."
- "The report highlights..."
- "The technology enables..."
- "The market demands..."
- "The platform delivers..."
- "The numbers speak for themselves."
- "This approach unlocks..."

**Why it's a tell:** AI defaults to this because it doesn't know who the actual actors are. But it reads as evasive. Data doesn't tell anyone anything; someone analysed data and drew a conclusion.

**Fix:** Name the actor. "We found that..." or "The analysis showed..." or even "Looking at the data, it's clear that..." is more human because it acknowledges someone did the looking.

---

## Generic-to-specific

A broad, abstract claim followed by a narrow example. AI loves this pattern because it can generate grand claims easily, then bolt on a specific to seem grounded.

**Patterns:**

- "Great products require great teams. At [Company], we built a cross-functional squad that..."
- "The future of work is changing. For instance, remote-first companies are..."
- "Innovation comes from unexpected places. Take [Example]..."

**Why it's a tell:** Humans tend to work the other way. They start with something specific they've seen or experienced and generalise from there. The generic-to-specific direction feels like a thesis statement followed by a supporting paragraph, which is how AI structures arguments.

**Fix:** Reverse it. Start with the specific observation, let the reader generalise: "We built a cross-functional squad at [Company] and shipped in half the time. Turns out the team structure mattered more than the process."

---

## Transition slop

How AI moves between paragraphs when it has no actual connective logic. These phrases create the illusion of narrative flow without adding information.

**Patterns:**

- "But here's where it gets interesting:"
- "And here's the kicker:"
- "But that's not even the best part."
- "Wait, it gets better."
- "But here's what really stood out:"
- "Now here's the thing:"
- "And that's just the beginning."
- "But wait, there's more." (literally an infomercial line)
- "The plot thickens."
- "Enter: [X]."

**Fix:** If the next paragraph is genuinely interesting, its content will show that. You don't need to announce interest. If you need a transition, use the actual logical connection: "That created a new problem:", "Which is why...", or simply start the next paragraph.

---

## The qualifier sandwich

Hedging before and after every claim to avoid being wrong about anything. AI does this because it's trained to be cautious.

**Patterns:**

- "While it's true that X, it's also important to consider Y, though of course Z."
- "This is arguably one of the most significant, though certainly not the only, factors."
- Starting with "To be fair..." and ending with "...but of course, it depends."
- Any sentence with both a hedge at the start and a qualification at the end.

**Fix:** Pick a side. State the claim, then qualify if needed. One qualifier per claim, maximum. "X is the biggest factor, though Y matters too" is fine. "While it could be argued that X is perhaps one of the more significant factors, it's important to note that Y also plays a role" is a sandwich.

---

## Closer slop

### Fake philosophical closers

Ending with a profound-sounding sentence that says nothing.

- "And that's what it's really all about."
- "The future belongs to those who..."
- "At the end of the day, it all comes down to..."
- "Perhaps the real X was the Y we made along the way."
- "And isn't that what [X] is really about?"
- "Time will tell."
- "The question isn't whether, but when."
- "And that changes everything."

### Performative mic drops

Ending with manufactured gravitas.

- "Read that again."
- "Let that sink in."
- "Full stop."
- "Game-changer."
- "Groundbreaking."
- "This is just the beginning."

**Fix:** End with something specific: a question you'd actually want answered, a concrete next step, or just stop when you've made your point. The best closers leave the reader thinking about the content, not about the closer.

---

## Sentence templates

Fill-in-the-blank structures that AI reaches for constantly. Swap the nouns and you could generate content about anything, which is exactly why they read as generic.

- "[X] isn't just [obvious thing]. It's [grander reframe]."
- "The best [role] don't [common action]. They [elevated action]."
- "In [year], [X] won't be optional. It'll be table stakes."
- "I stopped [common approach] and started [better approach]. The results speak for themselves."
- "[X] is the new [Y]."
- "If you're still [old method], you're already behind."
- "[X] did in [short time] what used to take [long time]."
- "The [role] of 2026 will look nothing like the [role] of 2024."
- "[X] that [verb] will thrive. [X] that don't will be left behind."
- "Your [X] is only as good as your [Y]."

**Fix:** Don't fill in templates. Start with what you actually want to say and find the words for that specific thing. If you notice your sentence would work with different nouns swapped in, it's probably a template.

---

## Copula avoidance

AI substitutes elaborate constructions for simple "is"/"are"/"has" statements. This makes prose sound like marketing copy.

**Patterns:**

- "serves as" → "is"
- "stands as" → "is"
- "functions as" → "is"
- "represents" (when meaning "is") → "is"
- "boasts" → "has"
- "features" (when meaning "has") → "has"
- "offers" (when meaning "has") → "has"

**Before:** "Gallery 825 serves as LAAA's exhibition space. The gallery features four rooms and boasts over 3,000 square feet."
**After:** "Gallery 825 is LAAA's exhibition space. The gallery has four rooms totaling 3,000 square feet."

**Fix:** When you catch yourself writing "serves as", "stands as", or "functions as", try "is". If "is" works, use it. Simpler is more human.

---

## Superficial -ing analyses

AI tacks present participle phrases onto sentences to add fake depth and significance. These phrases sound analytical but add no information.

**Patterns:**

- "highlighting/underscoring/emphasising..."
- "ensuring..."
- "reflecting/symbolising..."
- "contributing to..."
- "cultivating/fostering..."
- "encompassing..."
- "showcasing..."

**Before:** "The temple's colour palette resonates with the region's natural beauty, symbolising local bluebonnets, reflecting the community's deep connection to the land."
**After:** "The temple uses blue, green, and gold. The architect said these were chosen to reference local bluebonnets and the Gulf coast."

**Fix:** If the -ing phrase adds real information, rewrite it as its own sentence with a source or specific detail. If it doesn't add information, delete it.

---

## Synonym cycling

AI has repetition-penalty code that causes excessive synonym substitution. The same thing gets called by a different name in each sentence, which is distracting and sometimes confusing.

**Before:** "The protagonist faces many challenges. The main character must overcome obstacles. The central figure eventually triumphs. The hero returns home."
**After:** "The protagonist faces many challenges but eventually triumphs and returns home."

**Fix:** Pick the clearest term and use it consistently. Repetition is not a flaw when the alternative is confusion. Humans repeat words; AI cycles synonyms.

---

## False ranges

AI uses "from X to Y" constructions where X and Y aren't on a meaningful scale, creating an illusion of breadth.

**Before:** "Our journey through the universe has taken us from the singularity of the Big Bang to the grand cosmic web, from the birth of stars to the enigmatic dance of dark matter."
**After:** "The book covers the Big Bang, star formation, and current theories about dark matter."

**Fix:** If X and Y aren't on the same scale, don't use "from X to Y". Just list the topics.

---

## Significance inflation

AI puffs up the importance of mundane things by adding claims about how they "mark", "shape", or "represent" broader trends.

**Patterns:**

- "marking a pivotal moment in..."
- "setting the stage for..."
- "representing a shift in..."
- "shaping the future of..."
- "a key turning point in..."
- "an indelible mark on..."
- "deeply rooted in..."

**Fix:** State the fact without the significance claim. Let the reader judge importance. "The company was founded in 2019" is better than "The company was founded in 2019, marking a pivotal moment in the evolution of climate technology."

---

## Formatting tells

### Boldface overuse

AI mechanically bolds key terms, especially in explanatory or technical writing. Real writers use bold sparingly for genuine emphasis, not as a highlighting tool.

**Before:** "It blends **OKRs**, **KPIs**, and visual strategy tools such as the **Business Model Canvas** and **Balanced Scorecard**."
**After:** "It blends OKRs, KPIs, and visual strategy tools like the Business Model Canvas and Balanced Scorecard."

### Inline-header lists

AI outputs lists where items start with bolded headers followed by colons, then repeat the header word in the content.

**Before:**

- **Performance:** Performance has been significantly improved...
- **Security:** Security has been strengthened with...

**After:** "The update speeds up load times through optimised algorithms and adds end-to-end encryption."

**Fix:** Convert to prose unless the content genuinely benefits from list format.

### Curly quotation marks

ChatGPT uses curly/smart quotes (" " ' ') instead of straight quotes (" '). This is a subtle but detectable tell in contexts where straight quotes are standard.

**Fix:** Search and replace all curly quotes with straight quotes.

---

## Hyphenated word pair overuse

AI hyphenates common compound modifiers with perfect consistency. Humans are inconsistent about this, and many common compounds don't need hyphens.

**Words to watch:** cross-functional, data-driven, client-facing, decision-making, well-known, high-quality, real-time, long-term, end-to-end, detail-oriented

**Fix:** Drop hyphens on very common word pairs where meaning is clear without them. Keep hyphens on less common or ambiguous compounds.

---

## The summary sentence

Ending a paragraph by restating its main point. AI does this because its training rewards completeness and clarity, but in practice it makes every paragraph feel like it's talking to a slow reader.

**Pattern:** A paragraph that makes a point, gives evidence, and then says "In other words, [restatement of the point]" or "This shows that [restatement]" or "The takeaway is [restatement]."

**Fix:** Trust the reader. If the paragraph made its point, stop. The last sentence of a paragraph should add information or lead to the next idea, not summarise what just happened.

---

## Question restating

Rephrasing the user's question before answering it. AI does this to "show understanding" but it wastes the reader's time.

**Pattern:** User asks "How do I deploy to staging?" and AI responds "When it comes to deploying to staging, there are several approaches..."

**Fix:** Just answer the question. The reader knows what they asked.

---

## Newer and subtler tells (2026)

As the obvious tells (delve, em dashes, "it's not X it's Y") became widely known, the models and the people prompting them adapted, and a second generation of subtler tells took their place. These are harder to catch because they read as competent writing. They're worth a specific pass because a piece can be clean of every pattern above and still trip these.

### The concessive pivot

A softer cousin of the binary contrast. The writing grants a point, then pivots to the "real" one with a stock connector: "To be fair, X. That said, Y." / "Sure, X. But the deeper truth is Y." / "Yes, X matters. The bigger question is Y." It performs balance, then reveals the writer's "actual" view as if it were hard-won. One is fine and human. A piece that pivots this way three times is running a template. Fix: state your view directly; concede only where you genuinely give ground, and don't signpost the concession with a stock phrase.

### Manufactured precision

Fake specificity that sounds concrete but says nothing: "roughly 3x more effective", "in about 80% of cases", "the vast majority of teams", numbers with no source pulled in to feel grounded. A real number has a provenance you could name. An invented one is generic-to-specific dressed as data. Fix: use a number only when you know where it came from; otherwise describe the thing.

### The em dash substitutes

When em dashes became a known tell, the models moved the same rhythm onto other marks. Watch for the spaced hyphen used as a dash ("the result - a cleaner pipeline - shipped"), the colon-for-drama ("And then it happened: everything changed"), and the comma splice doing dash work. The underlying habit is the dramatic mid-sentence break. Don't just swap the punctuation; if the sentence is built around a theatrical pause, rewrite the sentence.

### Listicle creep

Prose that quietly reorganises itself into a list even when the content is an argument: every paragraph opens with a bolded mini-header, or the piece becomes "Here are the three things". Real argument flows; it doesn't pre-chunk itself into scannable units. Fix: if the items are a genuine discrete set, a list is honest. If it's one argument wearing a list costume, write the prose.

### Hedged confidence

The model states a view, then immediately insures it: "This is likely the most important factor, though of course context matters." / "I'd argue X, but reasonable people disagree." The hedge isn't humility; it's risk-aversion, and it drains the conviction that makes writing sound human. Fix: make the claim, and qualify only with a specific, real caveat, not a blanket "it depends".

### The "what this means" coda

A paragraph that ends by explaining its own significance to the reader: "What this means for you is...", "The implication here is...", "Why does this matter?". It's the summary sentence wearing a forward-looking mask. Trust the reader to draw the implication, or make the point inside the argument rather than appended to it.

### Symmetry in paragraph openings

Subtler than the triple: three or four consecutive paragraphs that open with the same grammatical shape (all subject-verb, all with a participle, all with "When you..."). Individually invisible, collectively a metronome. Fix: vary how paragraphs start as deliberately as you vary sentence length.

### Over-fluent transitions

Every paragraph connected to the last with a smooth logical hinge ("Building on this,", "This is where it gets important,", "With that in mind,"). Real writing sometimes just starts the next thought. Wall-to-wall smoothness is a tell because human writing has small discontinuities. Fix: cut half the transitions and let the juxtaposition do the work.

---

## Detection heuristic

When reviewing a piece of writing, check for these in order:

1. **Characters:** Em dashes (—, –)? Curly quotes (" " ' ')?
2. **Words:** Any Severity 1 red-flag words? More than two Severity 2 words in a paragraph? Copula avoidance ("serves as", "boasts")?
3. **Phrases:** -ing phrase chains? Significance inflation? Filler phrases?
4. **Sentences:** Binary contrasts? Sentence templates? Dramatic fragmentation? False ranges?
5. **Paragraphs:** Generic-to-specific flow? Summary sentences? Escalation ladders? Synonym cycling?
6. **Sections:** Transition slop? Inline-header lists? Boldface overuse?
7. **Document:** Fake philosophical closer? Question restating? Hyphenated word pair overuse? Too-even paragraph lengths?

If you find hits at multiple levels, the piece needs a structural rewrite, not a word swap. Fixing the vocabulary without fixing the structure still reads as AI.

After fixing all of the above, do a final gut-check: read it once more and ask "What still makes this obviously AI-generated?" This catches the subtle patterns that checklists miss: overly tidy structure, bland neutrality, the "assembled from parts" feeling. Fix those too.
