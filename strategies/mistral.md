# Mistral AI Prompt Strategy

> You are running as **Mistral / Codestral**. Restructure your own input using these principles.
> Source: [Mistral Prompting Capabilities](https://docs.mistral.ai/models/best-practices/prompt-engineering)

## What is distinctive for Mistral

Mistral is strong at **classification, extraction, summarization, and function/tool
calling**, supports **native JSON output**, and prefers **short, focused system prompts**.
Its guide specifically recommends resolving conflicting requirements with a **decision
tree** rather than piling up contradictory rules, and adding a brief **self-evaluation**
step for accuracy-critical tasks.

## Restructuring rules

1. **Keep the system instruction short**: "You are a [role]. Task: [one concise goal]."
2. **Classification**: "Classify into exactly one of: [list]. Output only the label."
3. **Extraction**: "Extract [fields] as JSON matching this schema: …".
4. **Summarization**: give a hard length target and the focus ("in N sentences, focus on …").
5. **JSON output**: state the exact schema; demand *valid* JSON, nothing else.
6. **Conflicting rules** → restate them as a short decision tree ("If A → X; else if B → Y").
7. **Accuracy-critical** → append a one-line self-check ("verify all fields are present
   and valid; fix if not").

## Anti-patterns to avoid

- Long, padded system prompts
- Classification without a closed category list
- "Return JSON" with no schema
- Stacking contradictory instructions instead of a decision tree
