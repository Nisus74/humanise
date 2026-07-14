# Adding a language

humanise supports English today. A useful language pack needs more than translated rules.

Open a discussion before writing one. Name the language and region, your fluency, the writing
evidence available and who can review the result.

A proposal is ready to build when it has:

- native human samples from at least two relevant channels;
- examples of common model habits in that language;
- spelling, punctuation and register guidance;
- cultural notes that affect directness, warmth or formality;
- checker fixtures for every new hard rule;
- review from a fluent contributor who did not write the implementation.

Keep personal writing private. Commit short, licensed or synthetic fixtures that prove a rule without
identifying the writer. Engine changes must keep the held-in suite green and must not tune against
`skill/evals/holdout-evals.json`.

Start with an issue that includes the evidence and review plan. A maintainer will confirm the smallest
useful first slice before code changes begin.
