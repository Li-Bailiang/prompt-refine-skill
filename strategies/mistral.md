# Mistral AI Prompt Strategy

> You are running as **Mistral / Codestral**. Restructure your own input using these principles.
> Source: [Mistral Prompting Capabilities](https://docs.mistral.ai/capabilities/completion/prompting_capabilities)

## What is distinctive for Mistral

Mistral is strong at **classification, extraction, summarization, and function/tool
calling**, and supports **native JSON output**. Its guide stresses **clear, complete,
well-structured prompts** and recommends marking up the sections with **Markdown and/or
XML-style tags** (readable, parsable, and familiar to the model). For conflicting
requirements it recommends a **decision tree** ("if A → X; else if B → Y") rather than
piling up contradictory rules.

## Restructuring rules

1. **Write a clear, complete instruction** and mark up its sections with Markdown or XML
   tags: "You are a [role]. Task: [one goal]." Favor structure and completeness over terseness.
2. **Classification**: "Classify into exactly one of: [list]. Output only the label."
3. **Extraction**: "Extract [fields] as JSON matching this schema: …".
4. **Summarization**: give a hard length target and the focus ("in N sentences, focus on …").
5. **JSON output**: state the exact schema; demand *valid* JSON, nothing else.
6. **Conflicting rules** → restate them as a short decision tree ("If A → X; else if B → Y").
7. **Few-shot** → when format compliance matters, include 1–3 input→output examples;
   the guide notes examples improve accuracy and consistency.

## Anti-patterns to avoid

- Vague or incomplete instructions (favor clarity and completeness)
- Classification without a closed category list
- "Return JSON" with no schema
- Stacking contradictory instructions instead of a decision tree
- Subjective qualifiers ("too long") or asking the model to count words/tokens
