# Google Gemini Prompt Strategy

> You are running as **Gemini**. Restructure your own input using these principles.
> Source: [Gemini Prompt Design Strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies)

## What is distinctive for Gemini

Gemini weights **system-level instructions placed at the top** strongly, generalizes
well from **2–3 few-shot examples**, and has a **very large, natively multimodal context
window** — so it tolerates rich background and several worked examples that smaller
models couldn't fit.

## Restructuring rules

1. **Lead with the system framing**: role + goal in the first lines ("You are a […].
   Your goal is to […].").
2. **Use named sections**: `Context:` → `Task:` → `Constraints:` → `Format:`.
3. **Prefer examples over description.** When a pattern exists, include 1–3 concrete
   input→output examples; Gemini picks up the pattern faster than from prose rules.
4. **Spell out the constraints** Gemini honors well: word/length budget, audience,
   tone, and exact output format.
5. **For reasoning**, ask it to show its working before the final answer.
6. **Multimodal**: name each modality and what to do with it ("from the image, extract
   …; combine with the text to …").

## Anti-patterns to avoid

- Unstructured walls of text with no section breaks
- System/role framing placed *after* the main task
- Describing a format in prose when a single example would pin it down
- Omitting length/audience/format constraints
