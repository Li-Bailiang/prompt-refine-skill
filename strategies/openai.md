# OpenAI GPT Prompt Strategy

> You are running as **an OpenAI GPT model** (GPT-5 family). Restructure your own input using these principles.
> Source: [OpenAI Prompt Engineering Guide](https://developers.openai.com/api/docs/guides/prompt-engineering) · [Reasoning best practices](https://developers.openai.com/api/docs/guides/reasoning-best-practices)

## What is distinctive for OpenAI models

There are **two regimes**, and current models expose both. **Non-reasoning chat models**
(the GPT-5 "Instant"-class; earlier GPT-4.1 / 4o) reward explicit instructions, delimiters,
and an output-format spec. **Reasoning models** (the GPT-5 "Thinking"-class — the
standalone o-series has been folded into the GPT-5 family) are the opposite: they reason
internally, so *adding* "think step by step" or long scaffolding **hurts** — give them a
clean, complete problem and get out of the way.

## Restructuring rules

1. **Detect the regime first.** Reasoning ("Thinking") model → keep it short, state the
   goal and constraints, omit chain-of-thought instructions, and prefer zero-shot (add
   few-shot only if needed, keeping any examples aligned with the instructions).
   Non-reasoning chat model → continue below.
2. **Separate instruction from content** with delimiters (triple backticks, `###`,
   or XML) so the model never confuses the two.
3. **Specify the output contract** exactly: "Return JSON with keys …" / "a Markdown
   table with columns …".
4. **For non-reasoning chat models on complex tasks**, request a short ordered breakdown
   before the final answer.
5. **Add the implied context** the user left out, and precision markers ("be specific,
   use concrete examples").
6. **Factual asks**: "only state what you're confident about; flag uncertainty."

## Anti-patterns to avoid

- Adding "let's think step by step" to a reasoning ("Thinking") model
- Mixing several unrelated asks in one prompt
- No delimiter between instruction and pasted content
- Missing an explicit output format
