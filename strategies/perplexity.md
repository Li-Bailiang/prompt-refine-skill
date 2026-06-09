# Perplexity / Sonar Prompt Strategy

> You are running as **Perplexity Sonar or Perplexity's Agent API**. Restructure your own input using these principles.
> Source: [Prompt Guide](https://docs.perplexity.ai/guides/prompt-guide)

## What is distinctive for Perplexity

Perplexity is optimized for source-grounded search and answer synthesis. Its Agent API can
iterate through search, analysis, and answer generation, but the user prompt still needs to
make the research target, freshness needs, source boundaries, and answer contract explicit.
The prompt guide separates stable `instructions` from per-request `input`; use that split
when refining prompts for repeated research workflows.

## Restructuring rules

1. **State the research question first.** Turn vague asks into one precise query plus the
   decision the answer should support.
2. **Separate standing behavior from the task.** Put role, citation discipline, and output
   rules in instructions; put the one-off question, entities, dates, and constraints in input.
3. **Make source boundaries explicit.** Name required or excluded source types, acceptable
   domains, geography, date ranges, and whether current web evidence is required.
4. **Use API parameters for hard retrieval constraints when available.** Do not bury filters
   such as domain, recency, or location only in prose if the host surface exposes dedicated
   controls.
5. **Ask for source-grounded synthesis, not generic explanation.** Require the answer to
   connect claims to cited evidence, separate direct evidence from inference, and flag
   unresolved conflicts.
6. **Plan for sparse or conflicting results.** Tell the model what to do when sources are
   weak: say what was not found, list near-misses, and avoid filling gaps with guesses.
7. **Constrain breadth.** Give a maximum number of sources, comparisons, or bullets when the
   task could sprawl; prefer ranked findings with short rationales.
8. **Preserve temporal wording.** Convert "latest", "today", or "recent" into an explicit
   date window when possible, especially for news, products, regulations, and pricing.

## Anti-patterns to avoid

- Asking for an uncited answer when the task depends on current or source-specific evidence
- Mixing permanent assistant behavior and one-off research details in one paragraph
- Treating source filters as soft preferences when dedicated parameters are available
- Requesting a broad web summary without a decision, timeframe, or source boundary
- Hiding uncertainty, source conflicts, or missing evidence behind confident prose
