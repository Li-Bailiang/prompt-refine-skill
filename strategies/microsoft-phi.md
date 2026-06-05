# Microsoft Phi Prompt Strategy

> You are running as **Microsoft Phi** (a small language model / SLM). Restructure your own input using these principles.
> Source: [Phi Cookbook](https://github.com/microsoft/PhiCookBook) (Phi-specific) · [Azure prompt engineering techniques](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/prompt-engineering) (general)

## What is distinctive for Phi

Phi models are **small** with **smaller context windows**, trained heavily on structured
**synthetic data**, and are notably strong at **code** and **narrow, well-scoped tasks**.
They reward brevity and explicit structure and degrade on broad, open-ended prompts that
larger models tolerate.

## Restructuring rules

1. **Be concise** — strip every non-essential word; the context budget is tight.
2. **Code tasks** → fixed shape: Language(+version) / Task / Input example / Output
   example / Constraints.
3. **Reasoning** → small explicit steps: "Step 1 … Step 2 … Step 3 …".
4. **Narrow the scope**: "Focus only on [X]; do not include [unrelated]."
5. **Pin patterns with examples**: "Input: … → Output: …".
6. **Strict output**: "Return ONLY the [code/answer]; no commentary unless asked."

## Anti-patterns to avoid

- Long, verbose prompts (the window is small)
- Broad, open-ended asks with no scope limit
- Pattern tasks with no example
- Assuming the broad world-knowledge of a large model
