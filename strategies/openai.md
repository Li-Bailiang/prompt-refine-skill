# OpenAI GPT Prompt Strategy

> You are running as **GPT / an o-series model**. Restructure your own input using these principles.
> Source: [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)

## What is distinctive for OpenAI models

There are **two regimes**. **GPT-4o / 4.1-class** chat models reward explicit
instructions, delimiters, and an output-format spec. **Reasoning models (o-series)** are
the opposite: they reason internally, so *adding* "think step by step" or long scaffolding
**hurts** — give them a clean, complete problem and get out of the way.

## Restructuring rules

1. **Detect the regime first.** Reasoning/o-series → keep it short, state the goal and
   constraints, omit chain-of-thought instructions. GPT-4-class → continue below.
2. **Separate instruction from content** with delimiters (triple backticks, `###`,
   or XML) so the model never confuses the two.
3. **Specify the output contract** exactly: "Return JSON with keys …" / "a Markdown
   table with columns …".
4. **For GPT-4-class complex tasks**, request a short ordered breakdown before the
   final answer.
5. **Add the implied context** the user left out, and precision markers ("be specific,
   use concrete examples").
6. **Factual asks**: "only state what you're confident about; flag uncertainty."

## Anti-patterns to avoid

- Adding "let's think step by step" to an o-series reasoning model
- Mixing several unrelated asks in one prompt
- No delimiter between instruction and pasted content
- Missing an explicit output format
