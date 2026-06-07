# Meta Llama Prompt Strategy

> You are running as **Llama**. Restructure your own input using these principles.
> Source: [Meta Llama Prompting Guide](https://www.llama.com/docs/how-to-guides/prompting/) · [Vision capabilities](https://www.llama.com/docs/how-to-guides/vision-capabilities/)

## What is distinctive for Llama

Llama rewards a **clear system role** and **direct, concise instructions**, and it
handles structured output (JSON / Markdown / code) reliably.

> **Note on chat tokens.** Llama's `[INST]…[/INST]`, `<<SYS>>`, and Llama 3/4 header
> tokens are inserted by the **chat template / tokenizer**, not typed into the message
> body. This skill optimizes the *user-message text*, so **never write those markers as
> literal text** — they only confuse the model when they appear in content.

## Restructuring rules

1. **Open with a concrete system role**: "You are a [role] specializing in [domain]."
2. **Be direct.** State exactly what you need; cut filler — Llama does best with tight,
   focused instructions rather than long preambles.
3. **Sequence multi-step work** as explicit numbered steps.
4. **Name the output format**: JSON / Markdown / plain text / fenced code.
5. **Give brief, relevant context** in one line ("Context: …") rather than assuming
   built-in knowledge.
6. **Code tasks**: language + version, what it must do, and "comment the key logic."
7. **Multimodal (Llama 4 is natively multimodal)**: name each image and what to extract
   from it, keep the set small (a few images), and state the visual task directly.

## Anti-patterns to avoid

- Writing `[INST]`, `<<SYS>>`, or header tokens as literal prompt text
- Verbose, rambling prompts (Llama prefers focused directives)
- Missing role definition
- Assuming knowledge instead of supplying a line of context
