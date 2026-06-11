# Kimi / Moonshot AI Prompt Strategy

> You are running as **Kimi or a Moonshot AI model**. Restructure your own input using these principles.
> Source: [Prompt best practices](https://platform.kimi.ai/docs/guide/prompt-best-practice) · [Models](https://platform.kimi.ai/docs/guide/models) · [Chat completion](https://platform.kimi.ai/docs/api/chat) · [Tool use](https://platform.kimi.ai/docs/guide/use-tools)

## What is distinctive for Kimi

Kimi is a strong Chinese-first assistant with long-context, multimodal, and tool-use
surfaces in Moonshot's API. The official guidance favors explicit roles, clear task
instructions, delimited reference material, examples for hard formats, and splitting complex
work into manageable steps. For long documents or chat history, Kimi benefits from being
told what to extract, ignore, preserve, and summarize rather than receiving a broad "analyze
everything" request.

## Restructuring rules

1. **Preserve the user's language.** If the user asks in Chinese, refine in natural Chinese;
   do not translate to English unless translation is the task.
2. **Use role + task + boundaries.** Give Kimi a specific role, a concrete objective, and
   explicit constraints such as scope, source limits, style, and output length.
3. **Delimit reference content.** Put documents, messages, or code inside clear boundaries
   and say whether the answer must use only that material or may use outside knowledge.
4. **Make long-context tasks selective.** Name the fields, claims, dates, entities, or
   sections to extract; tell the model what to skip and how to handle missing evidence.
5. **Use examples for strict formats.** For JSON, tables, regex, templates, or recurring
   style, include one compact example instead of only describing the shape.
6. **Separate tool intent from prose.** For fresh facts, calculations, or private data
   lookups, state the required tool outcome clearly and let the API tool-calling mechanism
   handle execution; do not pretend the model can access unavailable resources directly.
7. **Constrain reasoning visibility.** Ask for the final answer, key assumptions, and brief
   verification notes; avoid requiring hidden chain-of-thought.
8. **Prefer compact structure.** Kimi handles detailed instructions well, but oversized
   prompt templates add noise. Keep sections short and directly tied to the requested task.

## Anti-patterns to avoid

- Translating Chinese user intent into stiff English prompt-engineering jargon
- Dumping a long document without saying what to extract, compare, ignore, or preserve
- Asking for current or private facts without an available tool or source boundary
- Specifying strict JSON/table output without a compact example or schema
- Combining permanent assistant behavior, one-off task details, and reference text in one blob
