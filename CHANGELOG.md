# Changelog

All notable changes to Prompt Refine are documented here.
This project adheres to [Semantic Versioning](https://semver.org/).

## [2.1.0] — 2026-06-06

Hardening release focused on output discipline and answer style. Routing and strategy
files are unchanged in design; what changed is how the skill behaves at output time.

Evaluated on 120 vague prompts (blind, position-swapped A/B; `claude-sonnet-4-6`
generator, `claude-opus-4-8` judge) the post-change skill reaches a **74.0% win-rate**
(95% CI [66.9%, 80.6%], sign-test p < 0.0001) over the raw baseline, and **64.7%** even
when answer lengths are matched — versus **50.5%** for the 2.0.0 version under the same
length control. See the **Evaluation** section in the README.

### Added
- **Output-language lock** in `SKILL.md`: the final answer is always in the user's
  language, even though the skill and strategy files are written in English. In
  technical answers, code and identifiers stay in their original form while prose,
  headings, and comments follow the user's language.
- **No-scaffold guard** in `SKILL.md`: `<role>` / `<task>` / `<constraints>` / rewritten
  prompts / internal checklists are private working notes and must not appear in the
  visible answer.
- **Intervention-level ladder** in `SKILL.md` — none / light / normal / strong — so the
  edit is matched to the prompt instead of always restructuring.
- **"Prefer delivering over interrogating"** rule in `SKILL.md`: when a reasonable
  interpretation exists, give a best-effort answer with assumptions stated, then ask
  1–2 focused follow-ups. A questions-only reply is the last resort, not the default.
- **Output-discipline block + new anti-patterns** in `strategies/anthropic.md` covering
  scaffold leakage and language drift.

### Fixed
- Scaffold-leak failure mode where `<role>` / `<task>` blocks were occasionally printed
  to the user instead of the answer (down to **0 / 120** on the eval set).
- Prose-language drift on Chinese technical prompts, where the English strategy could
  nudge the answer prose into English (down to **0 / 60** on the eval set, code stripped).

## [2.0.0] — 2026-06-06

Major redesign for correctness. The core routing model changed, so behavior differs
meaningfully from 1.x.

### Changed
- **Routing is now by host model, not by task.** The skill detects which model is
  actually executing it and uses that model's strategy for the whole conversation. Task
  type only modulates which rules within that strategy are emphasized. This makes
  "optimize for the current model" actually true. *(Breaking change vs 1.x, which routed
  each task to a different vendor — and thus formatted prompts for a model that wasn't
  running.)*
- **Activation entry point** documented as the real `/prompt-refine` (skills are invoked
  by name). `verbose` / `off` are interpreted as plain-text controls after activation,
  not as parsed flags.
- **"Session-level" reframed** as conversation-scoped best-effort (no persistent runtime
  state). Re-invoke `/prompt-refine` if a long conversation is compacted.
- **READMEs** rewritten; the flagship before/after example now follows the routing and
  **preserves the user's original language** instead of translating it.
- **Token claims** corrected to realistic figures (core ~500–650 tokens).

### Fixed
- `strategies/meta-llama.md`: removed the instruction to write `[INST]…[/INST]` into
  prompt bodies — those are chat-template tokens, not user-message content.
- `strategies/deepseek.md`: stopped instructing injection of `<think>` tags / forced
  chain-of-thought into DeepSeek-R1 input (R1 generates its own reasoning; the vendor
  advises against it).
- `strategies/xai-grok.md`: removed "MoE routing awareness" as a prompting principle
  (model-internal, not promptable).
- `strategies/microsoft-phi.md`: corrected source attribution to lead with the
  Phi-specific Cookbook; the Azure guide is marked as general.

### Added
- `strategies/universal.md` repurposed as the fallback for **unknown/uncovered host
  models**.
- `CONTRIBUTING.md`, `CHANGELOG.md`, `.gitignore`, language toggles between READMEs.
- `examples/` — before/after demonstrations across host models (English + 中文).
- `hooks/` — optional Claude Code hook for hard session enforcement, **gated by a
  `.refine-active` toggle flag** so `/refine off` genuinely stops it.
- `internal/` — design/plan docs + release checklist, excluded from the published skill.
- **Verified install paths** (2026-06) for Claude Code, Cursor, Codex, Gemini CLI,
  GitHub Copilot, Windsurf, and CodeBuddy; documented in both READMEs.

## [1.0.0] — 2026-06-05
- Initial design: task-based routing across 11 vendor strategies. *(Superseded by 2.0.)*
