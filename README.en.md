<p align="center">
  <a href="README.md"><b>English</b></a> |
  <a href="README.zh.md">中文</a>
</p>

<h1 align="center">Prompt Refine</h1>

<p align="center">
  <b>A model-aware Agent Skill that silently refines your prompt for the model currently answering.</b>
</p>

<p align="center">
  You just ask. The active model reshapes the request for itself, preserves your language,
  and answers without showing the rewrite.
</p>

<p align="center">
  <a href="LICENSE">
    <img alt="MIT license" src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge">
  </a>
  <a href="SKILL.md">
    <img alt="Agent Skill" src="https://img.shields.io/badge/Agent%20Skill-SKILL.md-blue?style=for-the-badge">
  </a>
  <img alt="Zero dependencies" src="https://img.shields.io/badge/dependencies-zero-lightgrey?style=for-the-badge">
  <img alt="No optimizer call" src="https://img.shields.io/badge/optimizer%20call-none-brightgreen?style=for-the-badge">
</p>

<p align="center">
  <a href="#project-introduction">Project Introduction</a> |
  <a href="#quick-start">Quick Start</a> |
  <a href="#feature-demonstration">Feature Demonstration</a> |
  <a href="#built-in-strategies">Strategies</a> |
  <a href="#evaluation">Evaluation</a> |
  <a href="#compatible-platforms">Platforms</a> |
  <a href="examples/README.md">Examples</a>
</p>

---

## Project Introduction

**Prompt Refine** is a lightweight, cross-platform Agent Skill. After activation, it detects **which model is currently running the conversation** and applies that model family's prompting strategy before answering.

The core design is simple but important: **route by host model, not by task**. If Claude is answering, Prompt Refine uses the Anthropic strategy for the whole conversation. If GPT is answering, it uses the OpenAI strategy. A coding task never switches Claude into GPT-style prompting, and a writing task never switches GPT into Claude-style XML.

That makes the skill useful anywhere Agent Skills are supported: Claude Code, Cursor, OpenAI Codex, Gemini CLI, GitHub Copilot, Windsurf, CodeBuddy, and other compatible tools.

It is context-aware: follow-up requests can inherit the relevant goal, constraints, terminology, and preferences from the conversation, while the newest user instruction still wins.

It is intentionally lightweight: no runtime dependencies, no app server, no extra optimizer call, and only a short skill file plus one selected strategy file in context. The goal is better structure without spending a pile of extra tokens.

## Feature Demonstration

The same user request gets a different internal shape depending on the **host model**. These examples show the hidden rewrite style; in normal mode the user only sees the final answer.

### 1. Vague Request: Add The Missing Shape

User request:

```text
Help me analyze this market.
```

Anthropic Claude shape:

```xml
<role>You are a senior market analyst specializing in competitive intelligence.</role>
<context>
The user has not named the market, geography, customer segment, or timeframe.
Preserve uncertainty; make practical assumptions explicit instead of inventing facts.
</context>
<task>
Analyze the competitive landscape for the most likely intended market.
</task>
<constraints>
- Start by naming assumptions about market, audience, geography, and timeframe.
- Separate confident analysis from unknowns.
- Do not claim current market data unless it was provided or can be verified.
- Ask only the one or two follow-up questions that would most improve the analysis.
</constraints>
<format>
Use these sections: Assumptions, Competitive Map, Barriers And Switching Costs,
Strategic Implications, Unknowns, Next Questions.
</format>
<success_criteria>
The answer should be useful before the user clarifies the market, while making clear
which parts depend on assumptions.
</success_criteria>
```

OpenAI GPT shape:

```text
Goal: Turn an underspecified market-analysis request into a useful first-pass competitive landscape.

User request:
"""Help me analyze this market."""

Relevant context:
- Market, geography, audience, and timeframe are missing.
- Preserve uncertainty and make assumptions explicit.

Instructions:
1. State the assumed market scope first.
2. Identify likely player categories and competitive dynamics.
3. Compare barriers, switching costs, and strategic implications.
4. Flag unknowns instead of inventing facts.

Hard constraints:
- Do not claim current market data unless it was provided or can be verified.
- Ask only 1-2 follow-up questions.

Output format: Markdown headings for Assumptions, Competitive Map, Barriers,
Strategic Implications, Unknowns, and Next Questions.
```

### 2. Clear Request: Preserve The Constraints

User request:

```text
Write a 5-item npm release checklist. Keep each item under 8 words.
```

Anthropic Claude shape:

```xml
<context>
The user gave a tightly constrained formatting request. Do not expand the task.
</context>
<task>Write exactly five npm release checklist items.</task>
<constraints>
- Each item must be under 8 words.
- Cover package.json, README, LICENSE, version, and dry-run publishing.
- Return checklist items only; no intro or explanation.
</constraints>
<format>Use a numbered list with one short imperative phrase per item.</format>
<success_criteria>
Exactly 5 items, each under 8 words, with all requested topics covered.
</success_criteria>
```

OpenAI GPT shape:

```text
Task: Write exactly five npm release checklist items.

Context: The user already provided clear hard constraints, so preserve them and do not add scope.

Hard constraints:
- Under 8 words per item.
- Cover package.json, README, LICENSE, version, and dry-run publishing.
- Return only the checklist.

Output contract:
- Numbered list.
- Exactly 5 lines.
- No intro or outro.

Quality check before answering: each item is under 8 words and covers one requested release topic.
```

### What The User Sees

Only the final answer. The rewrite stays silent unless `/refine verbose` is enabled. For clear prompts, Prompt Refine should stay minimal and protect the user's exact constraints.

The strategy always follows the **host model**, not the topic: Claude gets Claude-shaped structure, GPT gets GPT-shaped structure.

## Quick Start

Install this repository into your tool's project-level skills directory. For Claude Code:

```bash
git clone https://github.com/Li-Bailiang/prompt-refine-skill.git .claude/skills/prompt-refine
```

To avoid copying the `.git` folder, use a release archive or:

```bash
npx degit Li-Bailiang/prompt-refine-skill .claude/skills/prompt-refine
```

Activate it in a conversation:

```text
/prompt-refine
```

Available in-session controls:

```text
/refine verbose    # Show a compact original -> refined diff before each answer
/refine off        # Stop refining for the rest of the conversation
/prompt-refine     # Re-activate after context compaction or a new session
```

## Install Paths

| Tool | Project-level skill path |
|---|---|
| Claude Code | `.claude/skills/prompt-refine` |
| Cursor | `.cursor/skills/prompt-refine` or `.agents/skills/prompt-refine` |
| OpenAI Codex | `.agents/skills/prompt-refine` |
| Gemini CLI | `.gemini/skills/prompt-refine` or `.agents/skills/prompt-refine` |
| GitHub Copilot (VS Code) | `.github/skills/prompt-refine` or `.agents/skills/prompt-refine` |
| Windsurf | `.windsurf/skills/prompt-refine` |
| CodeBuddy | `.codebuddy/skills/prompt-refine` |

Most tools also accept the shared `.agents/skills/` convention. User-level paths differ by platform, so use each tool's official docs when installing globally.

## Built-in Strategies

| Host model | Strategy file | Source family |
|---|---|---|
| OpenAI GPT / o-series | `strategies/openai.md` | OpenAI prompting guidance |
| Anthropic Claude | `strategies/anthropic.md` | Anthropic prompt engineering |
| Google Gemini | `strategies/google-gemini.md` | Gemini prompt design |
| Meta Llama | `strategies/meta-llama.md` | Llama prompting guidance |
| DeepSeek V3 / R1 | `strategies/deepseek.md` | DeepSeek prompt library |
| Mistral / Codestral | `strategies/mistral.md` | Mistral best practices |
| Qwen | `strategies/qwen.md` | Alibaba Model Studio guidance |
| xAI Grok | `strategies/xai-grok.md` | xAI Grok prompting references |
| Cohere Command | `strategies/cohere.md` | Cohere docs |
| Amazon Nova | `strategies/amazon-nova.md` | Nova prompt guide |
| Microsoft Phi | `strategies/microsoft-phi.md` | Phi Cookbook |
| Unknown host | `strategies/universal.md` | Conservative fallback |

## Evaluation

Prompt Refine was evaluated in a blind, position-swapped A/B test on **120 vague prompts** (60 English, 60 Chinese, 32 domains). The same generator model answered each prompt twice — once raw, once with Prompt Refine active — and an independent judge scored the two answers without knowing which was which. Each pair was judged twice with the answers swapped to cancel order bias.

### Headline results

| | Result |
|---|---|
| Refine vs raw win-rate | **74.0%** (167 wins / 52 losses / 21 ties of 240 judgments) |
| 95% bootstrap CI (per prompt, n = 120) | **[66.9%, 80.6%]** |
| Sign test | **p < 0.0001** |
| English / Chinese split | 75.0% / 72.9% |
| Length-matched win-rate | **64.7%** (refine answer within ±25% of raw length) |

The length-matched figure is reported alongside the headline to rule out a length preference in the judge. On length-matched pairs the current release wins **64.7%**, versus **50.5%** for the previous version of the skill — evidence of a genuine quality gain, not just longer answers.

### Per-dimension delta (refine − raw, 1–5 scale)

| Dimension | Δ |
|---|---|
| actionability | **+0.96** |
| completeness | **+0.81** |
| structure | **+0.49** |
| clarification | **+0.35** |
| language fidelity | +0.03 |

### Robustness

| Check | Result |
|---|---|
| scaffold leakage (`<role>` / `<task>` / rewritten prompt in output) | **0 / 120** |
| prose-language switches on Chinese prompts (code stripped) | **0 / 60** |
| parse fallbacks · skipped prompts | 0 · 0 |

Models: generator `claude-sonnet-4-6`, judge `claude-opus-4-8`. The host-model strategy under test is Anthropic (`strategies/anthropic.md`); other strategy files ship with the same design but have not yet been evaluated at this scale.

## Why Prompt Refine?

| | Prompt Refine | Standalone prompt optimizers |
|---|:---:|:---:|
| Form | Agent Skill | Web or desktop app |
| Model fit | Uses the currently running model's strategy | Generic or manually selected |
| Output | Silent final answer | Shows optimized prompt |
| Activation | Conversation-scoped and toggleable | Usually one-off |
| Language | Preserves original language and intent | Depends on implementation |
| Token cost | Low: short skill + one strategy | Often another full prompt pass |
| Dependencies | None | Often app-specific |

## Compatible Platforms

Prompt Refine follows the `SKILL.md` Agent Skill convention and is designed for tools that can load project-level skills, including Claude Code, Cursor, OpenAI Codex, Gemini CLI, GitHub Copilot, Windsurf, CodeBuddy, and compatible agents.

## License

MIT License. Free to use, modify, and distribute.

## Contributing

Issues and pull requests are welcome. For new or improved model strategies, read [CONTRIBUTING.md](CONTRIBUTING.md) first.

## Star History

<p align="center">
  <a href="https://star-history.com/#Li-Bailiang/prompt-refine-skill&Date">
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=Li-Bailiang/prompt-refine-skill&type=Date&size=desktop">
  </a>
</p>
