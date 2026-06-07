# Google Gemini Prompt Strategy

> You are running as **Gemini**. Restructure your own input using these principles.
> Source: [Prompt design strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies) · [Gemini 3 developer guide](https://ai.google.dev/gemini-api/docs/gemini-3)

## What is distinctive for Gemini

Gemini is **natively multimodal** with a **very large context window**, and current
(Gemini 3) models **reason natively** and reward **concise, direct** prompts. The verbose,
heavily-scaffolded prompt-engineering that older models needed can now backfire — Gemini 3
may **over-analyze** it. It also **defaults to lean answers**, so depth must be asked for.

## Restructuring rules

1. **Be concise and direct.** State the goal and constraints plainly; strip ceremony and
   legacy prompt-engineering layers built for weaker models.
2. **Don't force chain-of-thought.** Gemini reasons on its own — give it a clean, complete
   problem rather than "think step by step"; depth is a model setting, not prompt padding.
3. **Ask for detail explicitly.** The default answer is terse and efficient; if you want a
   thorough or conversational response, say so ("explain in depth", "be conversational").
4. **One delimiter style, used consistently.** Pick Markdown headings *or* XML-style tags
   (not both) to separate parts, and define any ambiguous terms.
5. **Long context → data first, question last.** Put large source material above, then ask
   at the very end, anchoring with "Based on the information above, …".
6. **Few-shot to pin the output shape.** 1–3 concrete input→output examples lock format and
   tone — keep them lean.
7. **Fresh facts need grounding, not prompt tricks.** Gemini's knowledge has a cutoff; for
   current information rely on a search/grounding tool — don't fake "today's date" in prose.
8. **Multimodal**: name each modality and what to do with it ("from the image, extract …;
   combine with the text to …").

## Anti-patterns to avoid

- Verbose, over-engineered prompts or forced "think step by step" (Gemini 3 over-analyzes them)
- Expecting a long answer by default instead of requesting depth explicitly
- Mixing Markdown and XML delimiters in one prompt
- Burying the question *above* a long document
- Faking the current date in the prompt instead of using a grounding tool
