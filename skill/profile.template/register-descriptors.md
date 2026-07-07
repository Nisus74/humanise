# Register descriptors: <your name>

Long-form documents (memos, board papers, PRDs, strategy docs, investor updates) have structural habits that short chat samples can't teach: how you open a memo, how you build the argument, where the opinion sits, how you handle risk and caveats, how you close. The fingerprint and the chat corpus capture sentence-level voice; this file captures document-level shape.

**When the skill reads it.** Document mode (see `SKILL.md`, the long-form workflow) reads your nearest long-form `sample-*.md` first. When you have no long-form sample for a document type, it leans on these descriptors instead. So fill in the registers you write before you have samples for them: it's the difference between the skill inferring your document shape and guessing it.

Write each line as a **move**, not an adjective, and where it sharpens the picture, add the bland version you'd never write. "Opens a board paper on the decision being asked for, not a recap" beats "clear and structured".

## One block per long-form register you write

Copy the block below for each register you actually use (memo, board-paper, prd, investor-update, strategy). Delete the ones you don't write; an empty block is worse than an absent one, because it tells the skill to imitate a shape you don't have.

### <register, e.g. board-paper>

- **Opening move:** how the first paragraph works. (e.g. "States the decision and my recommendation in the first two sentences; context comes after.")
- **Argument structure:** the order you build the case in. (e.g. "Problem, options, recommendation, risks. The recommendation is never buried in the middle.")
- **Where the opinion sits:** (e.g. "One clear recommendation up front; I don't lay out three options evenly and make the reader choose.")
- **Caveats and risk:** how you handle them. (e.g. "One honest risk, stated plainly, with the mitigation. Not a wall of reflexive hedges.")
- **Closing move:** (e.g. "Closes on the specific ask and the date, then stops. No summary paragraph, no thanks.")
- **Formatting habits:** headings, tables, bullets vs prose. (e.g. "Headings for navigation, prose for the argument. Numbers live in a table, never narrated in a sentence.")
- **Never here:** (e.g. "No executive-summary throat-clearing, no 'in conclusion'.")

## Keep it honest

Describe how you actually write these, not how you think a memo should read. If you've never written a board paper, leave that block out and the skill will tell the reader it's inferring rather than pretend it knows. Regenerate or revise this when you add a real long-form sample for a register; the sample is ground truth and supersedes the descriptor.
