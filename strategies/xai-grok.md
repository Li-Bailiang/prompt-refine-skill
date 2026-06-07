# xAI Grok Prompt Strategy

> You are running as **Grok**. Restructure your own input using these principles.
> Source: [xAI Docs](https://docs.x.ai) · [xAI grok-prompts repository](https://github.com/xai-org/grok-prompts) · [Image understanding](https://docs.x.ai/developers/model-capabilities/images/understanding)

## What is distinctive for Grok

Grok is oriented toward **truth-seeking, direct answers** and has access to **real-time
information**, so it benefits from explicit **temporal context** and from prompts that
invite **multiple perspectives** rather than a single canned line.

## Restructuring rules

1. **Frame for accuracy**: "Give an accurate, well-reasoned analysis of [topic]."
2. **Time-sensitive queries**: anchor the date — "As of [today's date], …" — and ask it
   to use current information where relevant.
3. **Multi-perspective**: "Examine this from these angles: [list]; distinguish facts
   from opinion."
4. **Push past the surface**: "Identify underlying patterns and second-order
   implications, not just the obvious points."
5. **Factual queries**: "Cite specific data/evidence where available; flag uncertainty."
6. **Scope it**: "Focus on [aspect]; brief background: [context]."
7. **Multimodal (vision)**: describe in plain language what to analyze in each image,
   raise detail for fine print, and ask for a structured result when extracting data.

## Anti-patterns to avoid

- Omitting temporal context for time-sensitive questions
- Yes/no framing when the value is in multiple perspectives
- Vague asks that expect deep insight without direction
- Over-restrictive prompts that suppress useful nuance
