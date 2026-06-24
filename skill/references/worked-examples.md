# Worked Examples

Before/after examples showing how to fix common AI writing patterns. Each example shows the problem, why it's a problem, and the rewrite.

These are organised by the type of fix, not the type of problem, because the same piece of text often has multiple issues.

---

## Table of Contents

1. [Em dash rewrites](#em-dash-rewrites)
2. [Vocabulary fixes](#vocabulary-fixes)
3. [Structural rewrites](#structural-rewrites)
4. [Tone and voice adjustments](#tone-and-voice-adjustments)
5. [Full paragraph rewrites](#full-paragraph-rewrites)

---

## Em dash rewrites

The em dash (—) and the spaced en dash ( – ) are the most commonly flagged AI punctuation tells. Every em dash can be replaced by a comma, period, semicolon, or colon. The choice depends on the relationship between the clauses.

### Use a comma for parenthetical asides

**Before:** "The report — which took three weeks — is ready."
**After:** "The report, which took three weeks, is now ready."

**Before:** "At a startup — a 0-to-1 startup — I shipped the ML pipeline."
**After:** "At a startup, a 0-to-1 startup, I shipped the ML pipeline."

### Use a period to split into two sentences

**Before:** "The challenge wasn't the AI itself — it was sequencing."
**After:** "The challenge wasn't the AI itself. It was sequencing."

**Before:** "Fintech moves fast, and the stakes are real — regulatory constraints, user trust, and integration complexity all compound."
**After:** "Fintech moves fast, and the stakes are real. Regulatory constraints, user trust, and integration complexity all compound."

### Use a semicolon for closely related clauses

**Before:** "I rebuilt the pipeline — reducing cycle time from three days to one."
**After:** "I rebuilt the pipeline; cycle time dropped from three days to one."

**Before:** "The founder wanted customisation — every enterprise client did."
**After:** "The founder wanted customisation; every enterprise client did."

### Use a colon to introduce an explanation or list

**Before:** "The fix was obvious in hindsight — we'd been watching the wrong dashboard."
**After:** "The fix was obvious in hindsight: we'd been watching the wrong dashboard."

(Avoid the tempting "Three things mattered: X, Y, and Z" shape here; it fixes the dash and introduces a triple.)

**Before:** "One thing made the difference — sequencing."
**After:** "One thing made the difference: sequencing."

---

## Vocabulary fixes

### Red-flag word replacements

**Before:** "We need to delve into the nuanced landscape of enterprise compliance."
**After:** "We need to look closely at how enterprise compliance actually works."

**Before:** "The intricate interplay between data quality and model performance is pivotal."
**After:** "Data quality directly affects model performance."

**Before:** "This multifaceted endeavour requires meticulous attention to the evolving regulatory realm."
**After:** "This requires careful attention to changing regulations."

### Corporate buzzword replacements

**Before:** "We leveraged our robust platform to facilitate seamless integration."
**After:** "We used the platform to connect the two systems."

**Before:** "The initiative was designed to streamline workflows and empower cross-functional teams."
**After:** "We simplified the workflow so teams across the business could move faster."

**Before:** "Our comprehensive, holistic approach enables scalable, best-in-class solutions."
**After:** "Our approach handles [specific scope] and works at [specific scale]." (If you can't fill in the specifics, the sentence has no content.)

### Adverb cleanup

**Before:** "This is fundamentally a remarkably significant shift that will undeniably transform how we essentially approach the problem."
**After:** "This changes how we approach the problem." (Four adverbs removed. The sentence lost nothing.)

**Before:** "Interestingly, the results were notably different from what we arguably expected."
**After:** "The results surprised us." (Three adverbs removed. Meaning preserved.)

---

## Structural rewrites

### Binary contrast → direct statement

**Before:** "It's not about the technology. It's about the people."
**After:** "The people matter more than the technology." (One sentence instead of two. Same point.)

**Before:** "The problem isn't a lack of data. It's a lack of clarity about what to do with it."
**After:** "We have plenty of data. We don't know what to do with it."

### Inline binary contrast → positive claim only

The subtle form. A ", not Y" tucked inside a sentence. The model generates these constantly because they feel concise and punchy, but they're the same AI contrast pattern.

**Before:** "Make decisions based on evidence, not opinion."
**After:** "Make decisions based on evidence." (The "not opinion" adds nothing. If you're basing decisions on evidence, the absence of opinion is implied.)

**Before:** "We ship features users need, not features we think are clever."
**After:** "We ship features users actually need." (Same idea without the rhetorical contrast.)

**Before:** "Focus on outcomes, not outputs."
**After:** "Focus on outcomes." (Or better: "We measure what changed for users, not how many tickets we closed." If you must contrast, make it specific and asymmetric rather than a neat X/not-Y pair.)

### Triple → varied structure

**Before:** "Ship things that matter, cut the ones that don't, stay close to users throughout."
**After:** "Ship what matters and stay close to users. Cut the rest."

**Before:** "We focused on speed, quality, and reliability."
**After:** "Speed and reliability were the priorities. Quality was non-negotiable but we couldn't gold-plate it."

### Balanced pair → asymmetric

**Before:** "When these elements align, teams ship great products. When they don't, teams build features no one uses."
**After:** "Teams ship great products when these elements align. Without them, you end up building features nobody asked for."

### Generic-to-specific → specific-to-general

**Before:** "Great products require great teams. At a former employer, we built a cross-functional squad that shipped the MVP in eight weeks."
**After:** "At a former employer, we shipped the MVP in eight weeks with a four-person squad. The team structure mattered more than the process."

### Transition slop → real transitions

**Before:** "We launched the product. But here's where it gets interesting: the adoption numbers exceeded every forecast."
**After:** "We launched the product. Adoption exceeded every forecast."

**Before:** "The data was clean. And here's the kicker: it had been clean all along."
**After:** "The data was clean. It had been clean all along; we'd been looking at the wrong dashboard."

### Summary sentence → just stop

**Before:** "We reduced churn by 15% in Q3 by fixing the onboarding flow. Three small changes to the first-run experience cut drop-off in half. In other words, the onboarding improvements had a measurable impact on retention."
**After:** "We reduced churn by 15% in Q3 by fixing the onboarding flow. Three small changes to the first-run experience cut drop-off in half." (The last sentence added nothing. Delete it.)

---

## The near-miss: rewrites that still carry the tell

The most common failure isn't missing a tell. It's "fixing" one while keeping its structure. The rewrite looks clean (different words, no banned vocabulary) but the shape a detector flags is still there. Each example below shows the source, a naive rewrite that still fails, and why, then the actual fix.

### Binary contrast, resequenced but intact

**Source:** "It's not about the technology, it's about the people."

**Naive rewrite (still fails):** "The win wasn't the technology. It was the people."

Why it still fails: same two-beat negate-then-reveal shape, just split across two sentences. The detector flags the structure, not the words. "Wasn't X. It was Y" is the same move as "not X, it's Y".

**Fixed:** "Our four engineers decided this, more than the stack did." One positive claim, a specific number, no negation scaffolding.

### Triple reworded into another triple

**Source:** "We need speed, quality, and reliability."

**Naive rewrite (still fails):** "It came down to moving fast, building well, and staying reliable."

Why it still fails: still three parallel items in the same rhythm. Swapping nouns for gerunds doesn't break the cadence that reads as AI.

**Fixed:** "Speed was the constraint. Quality and reliability we treated as non-negotiable and moved on." Two unequal halves, different weight, no parallel triple.

### Vocabulary scrubbed, skeleton intact

**Source:** "Our robust platform leverages cutting-edge AI to seamlessly streamline compliance."

**Naive rewrite (still fails):** "Our strong platform uses advanced AI to smoothly simplify compliance."

Why it still fails: every slop word got a plainer synonym, but it's still an empty copula-marketing sentence with zero specifics. It would describe any product. The vocabulary was never the real problem.

**Fixed:** "The platform flags ISO 15189 breaches in the sensor stream within about 90 seconds, which is the part labs actually pay for." A real claim, a number, a named standard, a reason it matters.

### How to catch yourself

After any structural rewrite, put the source and the rewrite side by side and ask: does the rewrite have the same _shape_ as the source, or a different one? If you diagnosed a binary contrast and your fix still has two beats, you reproduced it. If you diagnosed a triple and your fix still has three matched items, you reproduced it. The test is structural, not lexical.

---

## Tone and voice adjustments

### Stiff → conversational

**Before:** "I possess extensive experience in product management within regulated industries."
**After:** "I've spent most of my career building products where getting it wrong has real consequences."

**Before:** "It would be beneficial to establish a regular cadence of communication with key stakeholders."
**After:** "We should talk to stakeholders regularly." (Or better: "I'd set up a weekly sync with [specific person].")

### Generic wisdom → specific observation

**Before:** "Eight years in product has taught me that the difference between a good product and a great one usually comes down to how well you understand the problem before you start building."
**After:** "I've spent most of the last eight years arguing for what not to build as much as what to build. That instinct is what I'd bring to this role."

**Before:** "In today's rapidly evolving digital landscape, organisations must adapt or risk being left behind."
**After:** (Delete the entire sentence. Start with something specific.)

### Over-polished → natural

**Before:** "We've got an efficiency problem, and I want us to sort that out before we hit the end of this phase."
**After:** "We've got an efficiency problem. The numbers make it pretty clear. I'd rather deal with it now than scramble at the end."

---

## Full paragraph rewrites

### Example 1: LinkedIn post

**Before:**
"Here's what nobody's talking about: The future of product management isn't about building features. It's about building understanding. In today's rapidly evolving landscape, the best PMs don't just ship products. They cultivate deep, nuanced relationships with their users, leveraging cutting-edge research methods to facilitate transformative outcomes. And that changes everything."

**After:**
"Most product teams I've worked with ship too much and learn too little. The ones that slow down to run proper discovery end up shipping less but hitting the mark more often. We cut our feature backlog in half at a former employer and user satisfaction went up."

**What changed:** Removed the throat-clearer opener ("Here's what nobody's talking about"), the binary contrast ("isn't about X, it's about Y"), the sentence template ("The best [role] don't [action]. They [elevated action]."), five slop words (landscape, nuanced, leveraging, cutting-edge, facilitate, transformative), and the fake philosophical closer ("And that changes everything"). Replaced generic wisdom with a specific observation and a concrete example.

### Example 2: Email

**Before:**
"I hope this email finds you well. I wanted to reach out to discuss the incredibly exciting opportunity to collaborate on the upcoming initiative. I believe that by leveraging our respective strengths, we can facilitate a truly seamless and robust partnership that will undeniably yield significant results for all stakeholders involved."

**After:**
"Quick question about the [project name] collaboration. I think our teams could work well together on this, especially on [specific area]. Are you free for a 20-minute call this week to talk through the details?"

**What changed:** Removed the dead opener ("I hope this email finds you well"), the vague purpose ("reach out to discuss"), seven slop words (incredibly, leveraging, facilitate, seamless, robust, undeniably, significant), and the nominalisation ("yield results for stakeholders"). Replaced with a specific ask and a concrete next step.

### Example 3: Report introduction

**Before:**
"This comprehensive report delves into the multifaceted challenges facing our organisation in the current regulatory landscape. Through meticulous analysis of the intricate interplay between compliance requirements and operational efficiency, we endeavour to provide actionable insights that will empower leadership to navigate these pivotal challenges and drive transformative outcomes."

**After:**
"This report covers the three compliance problems most likely to cost us money in the next 12 months, and what we can do about each one."

**What changed:** Removed eight Severity 1/2 slop words (comprehensive, delves, multifaceted, landscape, meticulous, intricate, interplay, endeavour, actionable, empower, navigate, pivotal, transformative). Replaced the vague promise with a specific scope and purpose. One sentence instead of two.
