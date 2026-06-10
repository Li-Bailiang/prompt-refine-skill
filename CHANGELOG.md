# Changelog

All notable changes to Prompt Refine are documented here.
This project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- **Perplexity / Sonar strategy** grounded in the official Perplexity Prompt Guide, focused
  on source-bounded research, retrieval constraints, citation discipline, and uncertainty
  handling.

## [2.3.0] — 2026-06-08

Distribution, automation, and a deeper OpenAI strategy. Routing and runtime behavior are
unchanged; this release adds npm distribution, CI, and refreshes the OpenAI strategy.

### Added
- **Published to npm** as [`prompt-refine-skill`](https://www.npmjs.com/package/prompt-refine-skill),
  with a `files` whitelist (skill content only) and `publishConfig` pinned to the official
  registry.
- **CI** — a dependency-free validator for strategy-file structure and source links
  (`.github/workflows/validate.yml`), plus tag-triggered npm publish with provenance
  (`.github/workflows/publish.yml`).
- **ROADMAP.md**; a **Limitations** section in the READMEs; npm version/downloads badges;
  a star call-to-action.

### Changed
- **OpenAI strategy deepened for the GPT-5 family (5.1 / 5.2 / 5.5).** Reframed around
  OpenAI's current **outcome-first** guidance (describe the destination; set success
  criteria and constraints; avoid over-specifying the process), reasoning-effort control,
  agentic stopping/persistence/verification, and a **Codex** section (verify-your-work,
  decompose, durable rules in `AGENTS.md`). Source links updated to current pages.
- New **Codex** before/after example; example #2 modernized from "o-series" to GPT-5
  (Thinking).
- Routing labels in `SKILL.md` made consistent with the READMEs (OpenAI → GPT-5;
  DeepSeek → V4 (+ R1)).

## [2.2.0] — 2026-06-08

Accuracy and repository-health release. The strategy **design** and routing are unchanged;
this release refreshes strategy *content* against each vendor's current official guidance,
adds a multimodal (vision) framing rule where the host model supports images, and adds
standard project governance files.

> The **Evaluation** numbers in the README describe the 2.1.0 behavior and were **not**
> re-run for this release. The changes here are documentation/accuracy and governance —
> not a behavioral redesign.

### Changed
- **Vendor strategies aligned with official guidance.** Corrected source links and claims
  across `strategies/*.md` to match each vendor's current official prompt-engineering docs
  (e.g. OpenAI `developers.openai.com`, Anthropic `platform.claude.com`); removed claims a
  current official guide no longer supports.
- **Refreshed for current model lines.** OpenAI reframed around the **GPT-5 family**;
  DeepSeek updated to the **V4** main line (V4-Pro / V4-Flash, dual Thinking / Non-Thinking
  modes, 1M context) with **R1** kept explicitly as a legacy, R1-scoped case; Cohere
  updated to the **Command A** family. README strategy tables updated to match.

### Added
- **Multimodal (vision) framing rule** in the strategies that lacked one — Anthropic,
  OpenAI, Meta Llama, DeepSeek, Mistral, Cohere, xAI Grok, Qwen, Microsoft Phi — plus
  `universal.md`. (Google Gemini and Amazon Nova already covered vision.) Each rule is
  short and grounded in the vendor's official vision documentation.
- **Repository governance files**: `SECURITY.md`, `CODE_OF_CONDUCT.md`, issue templates,
  and a pull-request template. Private Vulnerability Reporting enabled on the repository.

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
