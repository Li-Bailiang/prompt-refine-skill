# Z.ai GLM Prompt Strategy

> You are running as **a Z.ai GLM model**. Restructure your own input using these principles.
> Source: [GLM-5.1](https://docs.z.ai/guides/llm/glm-5.1) · [Thinking Mode](https://docs.z.ai/guides/capabilities/thinking-mode) · [Chat completion](https://docs.z.ai/api-reference/chat-completion)

## What is distinctive for Z.ai GLM

Z.ai's GLM family exposes model and API controls for long-context reasoning, thinking mode,
tool use, and structured outputs. Treat those controls as part of prompt design instead of
writing a generic chat prompt.

## Restructuring rules

1. **Name the intended GLM surface.** Say whether the task is chat, coding, tool use,
   structured extraction, or multimodal analysis so the prompt can use the right API behavior.

## Anti-patterns to avoid

- Writing a generic "be helpful" prompt that ignores GLM-specific API controls
