# DeepSeek Prompt Strategy

> You are running as **DeepSeek**. Restructure your own input using these principles.
> Source: [DeepSeek-V4 release notes](https://api-docs.deepseek.com/news/news260424) · [Reasoning model guide](https://api-docs.deepseek.com/guides/reasoning_model) · [Prompt library](https://api-docs.deepseek.com/prompt-library/) · [DeepSeek-R1 model card](https://huggingface.co/deepseek-ai/DeepSeek-R1)

## What is distinctive for DeepSeek

The current main line is **DeepSeek-V4** (`deepseek-v4-pro` / `deepseek-v4-flash`), with a
**1M-token default context** and **two modes — Thinking and Non-Thinking**. The older
`deepseek-chat` (non-thinking) and `deepseek-reasoner` (thinking) names now route to
V4-Flash and are scheduled to retire on **2026-07-24**. **DeepSeek-R1** is the earlier
dedicated reasoner, kept here as a legacy, R1-specific case. All DeepSeek models are
strongly bilingual (中/英).

> **Official V4 prompting guidance is limited.** The release notes confirm model behavior
> (dual modes, 1M context, the chat/reasoner mapping) but ship no dedicated V4 prompting
> guide. The rules below reflect *verified* API/model behavior; the stronger R1
> recommendations are kept explicitly scoped to R1.

## Restructuring rules

1. **Non-Thinking mode (default chat)** — treat as a strong general model: give explicit
   instructions, the structure you want, and the output shape. An explicit "work through
   it before answering" is acceptable here.
2. **Thinking mode** — the model emits its own chain of thought, so **do not inject
   `<think>`, "reason step by step," or a forced reasoning template**. Behaviour in this
   mode is steered by the **prompt**, not by sampling parameters (`temperature` / `top_p`
   / penalties have no effect). State the problem and the desired answer format, then stop.
3. **R1 (legacy reasoner)** — R1's model card additionally recommends keeping **all
   instructions in the user message (no system prompt)** and prompting **zero-shot**
   (few-shot examples *degrade* R1). Apply this **only** when the host is R1.
4. **Code**: language + version, functional requirements with an input/output example,
   constraints (perf/style/deps), and the expected output shape.
5. **Bilingual**: keep the user's language; if mixed, state the desired answer language.
6. **Role-play**: define persona traits and the target style explicitly.
7. **Analysis**: list the angles to cover and ask for specific evidence per angle.

## Anti-patterns to avoid

- Injecting `<think>` tags or "think step by step" into Thinking-mode / reasoner input
- Applying R1's "no system prompt / zero-shot" rule to V4 by default (it is R1-specific)
- Treating `deepseek-chat` / `deepseek-reasoner` as permanent names (they retire 2026-07-24)
- Vague code requirements with no constraints or example
- Dropping the user's original language
