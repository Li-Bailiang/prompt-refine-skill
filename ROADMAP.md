# Roadmap

Prompt Refine is young and intentionally small. This is a living document — see the open
[issues](https://github.com/Li-Bailiang/prompt-refine-skill/issues) for the active items.

## Now
- Keep the vendor strategies aligned with each vendor's **current official** guidance
  (ongoing accuracy passes as the docs change).
- Repository health: governance files, versioned releases, npm distribution, public eval
  artifacts, and CI quality gates. ✅

## Next
- **Evaluate more host-model strategies** beyond Anthropic — ideally with a cross-vendor
  judge to remove single-vendor bias. ([#1](https://github.com/Li-Bailiang/prompt-refine-skill/issues/1))
- **Bilingual governance files** — Chinese versions of `SECURITY.md` / `CODE_OF_CONDUCT.md`
  to match the bilingual READMEs. ([#2](https://github.com/Li-Bailiang/prompt-refine-skill/issues/2))
- **Broaden `examples/`** to cover more of the strategies. ([#3](https://github.com/Li-Bailiang/prompt-refine-skill/issues/3))
- A short **before → after demo** captured inside a real tool.

## Later / ideas
- Deeper, model-specific techniques in select strategies (beyond summarizing docs).
- Additional distribution channels — only if there is genuine demand.

## Non-goals
- No runtime dependencies and no app server.
- No task-based routing — route by **host model**, not by task (see CONTRIBUTING.md).
- No scaffold leakage, and never change the user's language or intent.
