# Cultural calibration

your company is an Australian company entering the US market. the user writes for different audiences on the same day. Spelling, idioms, units, and register shift depending on who's reading.

This file covers the three main variants: Australian English (default), US English (US-tagged content), and UK English (occasional, for certain European audiences). The goal is consistency within a piece, not AusE-with-leaked-Americanisms or US-with-leaked-Britishisms.

---

## When to switch

Switch based on the primary audience, not on the user's location. A board paper for the Australian board stays AusE even if the user is in California at the time. A deck for a US hospital stays US English even if written in Sydney.

If the audience is mixed (AU and US investors on the same cap table), default to AusE. Investors in the US tolerate AusE far better than AU audiences tolerate Americanisms.

Tag the content at the top of the brief so the skill knows which variant to use. Example tags:

- `[audience: aus-board]` → AusE
- `[audience: us-healthcare-buyer]` → US English
- `[audience: uk-regulator]` → UK English
- `[audience: mixed-au-us-investors]` → AusE (default)

If no tag is present, ask before drafting. Assuming wrong wastes a revision cycle.

---

## Australian English (default)

**Spelling:**

- -ise not -ize (organise, recognise, realise, prioritise, summarise)
- -our not -or (colour, behaviour, neighbour, honour, favour)
- -re not -er (centre, theatre, fibre, litre, metre)
- -ll- in inflected forms (travelling, modelling, cancelled, labelling)
- -ogue not -og (catalogue, dialogue, analogue)
- -ement not -ment (acknowledgement, judgement; exception: "judgment" in legal contexts)
- programme (general use), program (software only)
- practise (verb), practice (noun)
- licence (noun), license (verb)

**Vocabulary and idiom:**

- "fortnight" is normal; in US contexts use "two weeks"
- "heaps" as an informal intensifier is Australian; avoid in US-facing
- "bloody" as an informal emphatic is Australian; avoid in any professional AU-US document
- "different to" (AU) rather than "different than" (US)
- "in hospital" (AU) rather than "in the hospital" (US)
- "rubbish" is fine in Australian contexts where Americans would say "trash" or "garbage"

**Units and dates:**

- Metric by default (kilometres, metres, litres, celsius)
- Date format: DD/MM/YYYY in prose; ISO 8601 (YYYY-MM-DD) in technical and filename contexts
- Time: 24-hour format common in professional contexts; 12-hour AM/PM in informal

**Punctuation:**

- Single quotes for direct speech: 'like this'
- Punctuation outside quotes unless it's part of the quoted material: 'the proposal', not 'the proposal,'
- En dash for ranges: 2015–18
- No Oxford comma by default (Australian convention leans no-Oxford); add it where ambiguity demands it

**Register:**

- Australian professional register is less formal than US professional register
- "G'day" is a stereotype; the user doesn't open emails with it, and neither should the skill
- Mild self-deprecation is Australian and plays well; avoid in US contexts where it reads as weakness

---

## US English (for US-tagged content)

**Spelling:**

- -ize not -ise (organize, recognize, realize, prioritize)
- -or not -our (color, behavior, neighbor, honor, favor)
- -er not -re (center, theater, fiber, liter, meter)
- Single -l- in inflected forms (traveling, modeling, canceled, labeling)
- -og not -ogue (catalog, dialog, analog)
- judgment (no -e) in all contexts
- program (all contexts, not programme)
- practice (both noun and verb)
- license (both noun and verb)

**Vocabulary and idiom:**

- "two weeks" instead of "fortnight"
- "in the hospital" rather than "in hospital"
- "different than" or "different from" (both acceptable; "different from" is slightly more formal)
- "math" rather than "maths"
- "gotten" is acceptable past participle (UK/AU readers would say "got")
- Healthcare vocabulary: "lab" (AU "laboratory" both work); "ER" not "emergency department" in informal; "PCP" for primary care physician
- Dollar amounts default to USD: "$5,000" means USD unless context is clearly AU

**Units:**

- Imperial preferred in customer-facing US content (miles, pounds, Fahrenheit)
- Metric acceptable in scientific and technical content; state units explicitly where ambiguity matters
- Weight and height of a person in lbs/ft in US contexts

**Punctuation:**

- Double quotes for direct speech: "like this"
- Punctuation inside quotes: "the proposal," not "the proposal",
- Em dash with no spaces (US convention); however, the skill bans em dashes for all audiences, so this is moot
- Oxford comma used by default in US prose; include it

**Register:**

- US professional register leans more formal in written form
- US healthcare and enterprise sales contexts especially expect a slightly more formal tone
- Direct statements of capability work well; AU-style self-deprecation can read as lacking confidence
- "Cheers" as a sign-off is read as British or Australian; avoid in US emails

---

## UK English (for UK-tagged content)

**Spelling:** Matches AusE on almost everything. Exceptions:

- "organise" (AusE and UK both accept)
- "programme" (both AusE and UK)
- "practise" / "practice" distinction (both AusE and UK)

**Vocabulary:** UK-specific notes if relevant:

- "at university" not "in college"
- "lift" not "elevator"
- "flat" not "apartment"
- "CV" is standard (as in AU); "resume" is US

**Register:** UK professional register is closer to AU than to US. Moderate formality works.

---

## Cross-variant consistency check

Every piece should end up in one variant cleanly. Mixed-variant content signals either lazy editing or the model's training set leaking through. Common leakage patterns to check:

- "organization" / "organisation": pick one
- "behavior" / "behaviour": pick one
- "color" / "colour": pick one
- Single vs. double quotes: pick one per piece
- Oxford comma usage: consistent within a piece
- Date format: consistent within a piece

During the mechanical sweep, if the target variant is AusE, grep for `ize\b`, `ior\b`, `enter\b`, `olor\b` as signals of American leakage. For US-tagged pieces, grep for `ise\b`, `iour\b`, `entre\b`, `olour\b`.

---

## When the audience tag is unclear

Ask. "Is this piece for the AU board or the US pilot sites?" is a one-line question with a one-line answer. It saves a full revision.

Default to AusE if asking isn't possible and the work is urgent.

---

## Cross-cultural traps

Three patterns cause the most trouble for Australian writers addressing US audiences:

1. **Understatement.** Australian professional register often understates achievements ("We've built a pretty good system"). US audiences read this as "the system is okay at best". In US-facing content, the user states capabilities directly ("The system handles 200 samples per day at 99.5% accuracy").
2. **Self-deprecation.** Deflecting compliments or softening claims reads as polite in AU and as weak in US. Drop self-deprecation from US-facing content.
3. **Formality mismatch.** An Australian-register email can read as overly casual to a US healthcare procurement team. Lift the formality one notch for US enterprise contexts.

Three patterns cause trouble the other way:

1. **US hype language in AU contexts.** "Game-changing", "revolutionary", "best-in-class" reads as marketing spam to Australian professionals. Strip it.
2. **Over-formality.** Opening an email to an Australian collaborator with "Dear Dr Polland" when you're on first-name terms reads stiff. Match their register.
3. **American idiom in AU prose.** "Home run", "ballpark", "touch base", "circle back" stand out in AU writing. Use the AU equivalent or drop the metaphor.
