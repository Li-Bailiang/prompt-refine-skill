# DeepSeek Prompt Strategy

> You are running as **DeepSeek (V3 or R1)**. Restructure your own input using these principles.
> Source: [DeepSeek Prompt Library](https://api-docs.deepseek.com/prompt-library/) · [DeepSeek-R1 usage recommendations](https://api-docs.deepseek.com/guides/reasoning_model)

## What is distinctive for DeepSeek

**R1 is a reasoning model.** It generates its own `<think>…</think>` chain in the
**output**; you do **not** put `<think>` in the input, and DeepSeek explicitly advises
**against** adding "think step by step" or a system prompt that dictates a reasoning
format — that fights the model's native reasoning. For R1, DeepSeek also recommends
putting **all instructions in the user message rather than a directive system prompt**,
and prompting **zero-shot** — adding few-shot examples consistently *degrades* R1, so
describe the task and desired output format instead. **V3** is a standard chat model
where an explicit chain-of-thought request is fine. Both are strongly bilingual (中/英).

## Restructuring rules

1. **R1 (reasoning)**: give a **complete, unambiguous problem statement** and the answer
   format you want — then stop. Do **not** inject `<think>`, "reason step by step," or a
   forced reasoning template; keep instructions in the **user message** (no directive
   system prompt) and stay **zero-shot** — describe the task instead of adding examples.
   Put any constraints plainly.
2. **V3 (chat)**: an explicit "work through it before answering" is acceptable; otherwise
   treat like a strong general model.
3. **Code**: language + version, functional requirements with an input/output example,
   constraints (perf/style/deps), and the expected output shape.
4. **Bilingual**: keep the user's language; if mixed, state the desired answer language.
5. **Role-play**: define persona traits and the target style explicitly.
6. **Analysis**: list the angles to cover and ask for specific evidence per angle.

## Anti-patterns to avoid

- Injecting `<think>` tags or "think step by step" into R1's input
- Adding few-shot examples to R1 (zero-shot is recommended; examples degrade it)
- Over-constraining R1's output structure so it can't reason freely
- Vague code requirements with no constraints or example
- Dropping the user's original language
