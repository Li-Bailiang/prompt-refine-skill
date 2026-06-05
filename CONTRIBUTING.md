# Contributing to Prompt Refine

Thanks for helping improve Prompt Refine! This skill is plain Markdown — no build step,
no dependencies. Most contributions are edits to `SKILL.md` or a file in `strategies/`.

## The one rule that keeps the design coherent

**Route by host model, not by task.** Prompt Refine optimizes a prompt for *the model
that is actually executing it*. When the skill runs on Claude, it uses
`strategies/anthropic.md`; on GPT, `strategies/openai.md`; and so on. Task/topic only
decides *which rules inside the selected file* to emphasize — it must **never** switch to
another vendor's strategy.

> ❌ Do **not** reintroduce "code task → use Anthropic, math task → use DeepSeek" routing.
> That formats a prompt for a model that isn't running it. (It's the bug v2.0 fixed.)

## Project layout

```
SKILL.md            # Entry point: host-model → strategy routing + controls
strategies/         # One file per model family (+ universal.md fallback)
examples/           # Before/after demonstrations
hooks/              # Optional Claude Code hook for hard session enforcement
internal/           # Design notes — NOT shipped (see .gitignore)
```

## Editing or adding a strategy

Each `strategies/*.md` follows the same shape — keep it consistent and **short**
(~300–450 tokens; the whole file is loaded at runtime):

1. **Header line**: `> You are running as **<Model>**. Restructure your own input using these principles.`
2. **Source line**: link the vendor's **official** prompt-engineering doc.
3. **"What is distinctive for <Model>"**: 2–4 sentences on what *genuinely* differs for
   this model — not generic advice that applies everywhere.
4. **Restructuring rules**: concrete, model-specific moves.
5. **Anti-patterns to avoid**.

### Quality bar

- **Be model-specific.** If a rule reads identically to one in `universal.md`, it
  probably belongs only in `universal.md`. Differentiation is the point.
- **No internal-only mechanics as prompt content.** Chat-template tokens (`[INST]`,
  `<<SYS>>`, Llama-3 headers), a reasoning model's generated `<think>` tags, MoE routing,
  etc. are **not** things you type into a user prompt. Don't instruct the model to inject
  them.
- **Cite real, current official sources.** Verify the link resolves before submitting.
- **Preserve the user's language and intent** in every rule — restructure, never translate
  or change the ask.

### Adding a brand-new model family

1. Create `strategies/<vendor>.md` following the shape above.
2. Add one row to the **Host model → strategy** table in `SKILL.md`.
3. Add a row to the strategy table in `README.md` **and** `README.en.md`.
4. Add a before/after pair under `examples/` if the model has a distinctive format.

## Keep the two READMEs in sync

`README.md` (中文) and `README.en.md` (English) must stay equivalent. Any change to one
needs the matching change to the other.

## Submitting

1. Fork, branch, make your change.
2. Confirm `SKILL.md`, the strategy table in both READMEs, and the strategy files all
   agree.
3. Open a PR describing **which model** your change targets and **what is distinctive**
   about the strategy.

By contributing you agree your work is licensed under the project's [MIT License](LICENSE).
