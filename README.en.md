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
<task>
Analyze the market and make the missing scope explicit:
1. Define the assumed market and audience.
2. Identify major players and their positions.
3. Compare competitive dynamics, barriers, and switching costs.
4. State assumptions and ask for the one or two details needed to refine the answer.
</task>
<format>Use a concise structured report with assumptions, analysis, and next questions.</format>
```

OpenAI GPT shape:

```text
Goal: Analyze the market despite missing scope.

User request: "Help me analyze this market."

Instructions:
- State the assumed market and audience.
- Identify major players and competitive dynamics.
- Flag uncertainty instead of inventing facts.
- Ask the few follow-up questions needed to refine the analysis.

Output format:
- Assumptions
- Competitive landscape
- Risks and unknowns
- Next questions
```

### 2. Clear Request: Preserve The Constraints

User request:

```text
Write a 5-item npm release checklist. Keep each item under 8 words.
```

Anthropic Claude shape:

```xml
<task>Write exactly five npm release checklist items.</task>
<constraints>
- Each item must be under 8 words.
- Cover package.json, README, LICENSE, version, and dry-run publishing.
- Do not add extra explanation.
</constraints>
```

OpenAI GPT shape:

```text
Task: Write exactly five npm release checklist items.

Hard constraints:
- Under 8 words per item.
- Cover package.json, README, LICENSE, version, and dry-run publishing.
- Return only the checklist.

Output format: numbered list.
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
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=Li-Bailiang/prompt-refine-skill&type=Date">
  </a>
</p>
