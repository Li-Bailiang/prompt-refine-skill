# Z.ai GLM Prompt Strategy

> You are running as **a Z.ai GLM model**. Restructure your own input using these principles.
> Source: [GLM-5.1](https://docs.z.ai/guides/llm/glm-5.1) · [Core parameters](https://docs.z.ai/guides/overview/concept-param) · [Chat completion](https://docs.z.ai/api-reference/llm/chat-completion) · [Thinking Mode](https://docs.z.ai/guides/capabilities/thinking-mode) · [Function Calling](https://docs.z.ai/guides/capabilities/function-calling) · [Structured Output](https://docs.z.ai/guides/capabilities/struct-output) · [Context Caching](https://docs.z.ai/guides/capabilities/cache) · [GLM-5V](https://docs.z.ai/guides/vlm/glm-5v-turbo)

## What is distinctive for Z.ai GLM

Z.ai's GLM family exposes model and API controls for long-horizon reasoning, thinking mode,
tool use, structured outputs, context caching, and multimodal input. GLM-5.1 is positioned
for agentic coding, complex reasoning, and long tasks, so prompt quality depends on matching
the task to the right capability rather than writing a generic chat prompt.

## Restructuring rules

1. **Name the intended GLM surface.** Say whether the task is chat, coding, tool use,
   structured extraction, or multimodal analysis so the prompt can use the right API behavior.
2. **Set thinking intent explicitly.** Use thinking mode for hard planning, coding,
   tool-heavy diagnosis, and multi-step reasoning; avoid forcing it for simple rewriting,
   classification, or low-latency extraction.
3. **Frame long-horizon work with checkpoints.** For coding or research agents, provide the
   goal, done criteria, state to preserve, allowed files/tools, and when to stop or ask.
4. **Make tool calls concrete.** State the real-world outcome each tool should achieve, the
   required parameters, permission boundaries, and how to validate returned data.
5. **Use structured-output contracts for strict formats.** For JSON or tabular extraction,
   define required fields, null/missing behavior, and whether extra keys are forbidden.
6. **Keep streaming output separable.** For interactive agents, separate progress notes,
   tool arguments, tool results, and the final user-facing answer so partial output is safe.
7. **Separate stable context from per-turn input.** Put reusable instructions, corpora, or
   specs in stable context/cache; keep the user turn focused on the current delta.
8. **Bind each visual input to a task.** For GLM-5V-style prompts, say what to inspect in
   each image/video/file and whether to extract text, compare layout, or reason about state.
9. **Preserve the user's working language.** Keep Chinese prompts natural, keep code/API
   names unchanged, and ask for compact sections rather than decorative formatting.

## Anti-patterns to avoid

- Writing a generic "be helpful" prompt that ignores GLM-specific API controls
- Replacing thinking-mode selection with blanket "think step by step" instructions
