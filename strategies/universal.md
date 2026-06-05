# Universal Prompt Strategy

> Fallback when the host model is unknown or not one of the 11 covered families.
> These practices help across essentially all modern LLMs.

## Core principles

1. **Clarity over cleverness** — say exactly what you want.
2. **Structure over stream-of-consciousness** — organize the ask logically.
3. **Context over assumption** — supply the background the model needs.
4. **Constraints over ambiguity** — specify format, length, tone, audience.
5. **Examples over descriptions** — show one, don't only tell.

## Restructuring rules

1. **State the objective**: "Your task is to [specific goal]."
2. **Give context**: "Background: [what the model needs to know]."
3. **Specify format**: "Respond as [format] with [structure]."
4. **Set quality + boundaries**: "[accurate/thorough/concise]; focus on [scope], exclude
   [out-of-scope]."
5. **Decompose complex tasks**: "First [step], then [step], finally [step]."
6. **Name the audience and tone** when they affect the answer.
7. **Preserve the user's language and intent** — restructure, don't translate or rewrite the ask.

## Anti-patterns to avoid

- Ambiguous requests with no clear objective
- Missing format specification
- No context where context is clearly needed
- Changing the language or meaning of the original request
