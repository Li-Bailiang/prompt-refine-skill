# Anthropic Claude Prompt Strategy

> You are running as **Claude**. Restructure your own input using these principles.
> Source: [Anthropic Prompt Engineering](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering) + [Interactive Tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial)

## What is distinctive for Claude

Claude was explicitly trained to respect **XML-style tags** as structure, to follow an
**assigned role**, and to reason in an explicit **thinking** step before answering. It
handles very long context well when the **data comes first and the question last**.

## Restructuring rules

1. **Wrap the structure in tags** the task actually needs — typically `<role>`,
   `<task>`, `<context>`, `<constraints>`, `<format>`. Don't add empty tags.
2. **Assign a role**: `<role>You are a [specific expert].</role>`
3. **Long inputs first, question last.** Put documents/code inside `<document>` /
   `<context>` *above* the instruction; ask the question at the very end.
4. **Add explicit reasoning only for genuinely hard tasks**: instruct a brief
   `<thinking>` pass before the answer (Claude already reasons well on simple ones).
5. **Show, don't tell** with one or two `<example>` blocks when output shape matters.
6. **State hard rules** in `<constraints>` and the single must-not-miss requirement
   plainly — Claude follows positive, specific instructions best.

## Anti-patterns to avoid

- Unstructured walls of text for multi-part tasks (use tags)
- Burying a long document *after* the question
- Forcing a heavy `<thinking>` ritual onto a one-line request
- Vague role or missing output-shape when the format matters
