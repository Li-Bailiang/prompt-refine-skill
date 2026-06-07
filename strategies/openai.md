# OpenAI GPT Prompt Strategy

> You are running as **an OpenAI GPT model** (GPT-5 family — 5.1 / 5.2 / 5.5). Restructure your own input using these principles.
> Source: [Prompt guidance](https://developers.openai.com/api/docs/guides/prompt-guidance) · [Using the latest model](https://developers.openai.com/api/docs/guides/latest-model) · [Reasoning best practices](https://developers.openai.com/api/docs/guides/reasoning-best-practices) · [Codex prompting](https://developers.openai.com/codex/prompting) · [Images and vision](https://developers.openai.com/api/docs/guides/images-vision)

## What is distinctive for OpenAI models

GPT-5-family models follow instructions precisely, call tools well, and reason internally.
The current official stance is **outcome-first**: describe the *destination* — goal, success
criteria, constraints, available context — and let the model choose the path. Heavy
step-by-step scaffolding that older models needed now **hurts**: it adds noise, narrows the
search space, and yields mechanical answers. Reasoning ("Thinking") variants reason on their
own, so "think step by step" is redundant — set **reasoning effort** to fit the task instead.

## Restructuring rules

1. **Lead with the outcome, not the procedure.** State the goal, what "done/correct" looks
   like (success criteria + required output fields), and the hard constraints — then stop.
   Don't transcribe every step.
2. **Reserve absolutes for true invariants.** Use `MUST` / `NEVER` only for real rules
   (safety, format contracts); for judgment calls, give the decision criteria instead.
3. **Separate instructions from content** with delimiters (` ``` `, `###`, or XML), and
   **specify the output contract** exactly ("Return JSON with keys …").
4. **Agentic / multi-step asks**: set a stopping rule ("stop when you can answer the core
   request") and allow persistence ("don't stop early if another tool call improves
   correctness"); ask for a short verification pass before high-impact output.
5. **Coding on Codex**: have it **verify its own work** — include repro steps, how to
   validate, and run lint/tests; split large work into smaller reviewable steps (ask it to
   propose a plan first if decomposition is unclear). Put durable, repo-wide rules in
   **`AGENTS.md`**, not in every prompt.
6. **Grounding**: never fabricate citations, URLs, or IDs; separate confident facts from
   uncertainty; don't turn missing evidence into a confident "no".
7. **Don't over-format.** Plain prose unless structure genuinely aids comprehension — avoid
   reflexive cards and nested bullets.
8. **Multimodal (vision)**: say exactly what to do with each image and keep the question with
   it; raise image detail for small or low-quality text. Don't rely on the model for
   **precise spatial layout or exact counts** (documented weak spots).

## Anti-patterns to avoid

- Carrying over a legacy prompt stack that **over-specifies the process** (now counter-productive)
- `ALWAYS` / `NEVER` / `must` on judgment calls instead of on true invariants
- Forcing "think step by step" onto a reasoning ("Thinking") model
- Loading durable, repo-wide rules into every Codex prompt instead of `AGENTS.md`
- No delimiter between instruction and pasted content; missing an output contract
- Reflexive heavy formatting where plain prose would read better
