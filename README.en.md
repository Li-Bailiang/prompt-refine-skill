<div align="right"><b>English</b> | <a href="README.md">中文</a></div>

# 🎯 Prompt Refine

> Let the model rewrite your words the way **it** prefers — you just talk, it restructures.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Standard](https://img.shields.io/badge/Agent%20Skills-SKILL.md-blue)](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview)

## What is this?

**Prompt Refine** is a lightweight Agent Skill. On activation it first detects **which model is currently running it**, then **always uses that model's official prompting best practices** — silently restructuring each request into the shape that model handles best before answering. You never learn prompt engineering and never see the rewrite; you just notice the answers got better.

### Core idea

Different models prefer different prompt structures: Claude loves XML tags, OpenAI's reasoning models want you to **not** over-scaffold, Qwen wants you to **keep Chinese** instead of force-translating…

So Prompt Refine doesn't hop between vendors by topic — it **locks onto the model you're actually using** and applies that vendor's own official strategy. The 11 built-in strategies exist so it stays **optimal wherever you run it** — one skill, adapts everywhere.

## Quick Start

### Installation

Drop this repo into your tool's project-level skills directory. For Claude Code:

```bash
git clone https://github.com/Li-Bailiang/prompt-refine.git .claude/skills/prompt-refine
```

Project-level skills directory per tool (verified against official docs, 2026-06):

| Tool | Install path |
|------|---------|
| Claude Code | `.claude/skills/prompt-refine` |
| Cursor | `.cursor/skills/prompt-refine` (or `.agents/skills/`) |
| OpenAI Codex | `.agents/skills/prompt-refine` |
| Gemini CLI | `.gemini/skills/prompt-refine` (or `.agents/skills/`) |
| GitHub Copilot (VS Code) | `.github/skills/prompt-refine` (or `.agents/skills/`) |
| Windsurf | `.windsurf/skills/prompt-refine` |
| CodeBuddy | `.codebuddy/skills/prompt-refine` |

> Most tools also accept the shared **`.agents/skills/`** alias — place it once, use it everywhere. Global/user-level paths differ (e.g. `~/.gemini/skills/`, `~/.copilot/skills/`); see each platform's docs.
>
> Tip: to avoid bringing `.git` along, use `npx degit Li-Bailiang/prompt-refine <dir>` or a Release tarball.

### Usage

```text
/prompt-refine        # Activate (most tools: type / and pick prompt-refine)
```

Once active, control it with plain-text commands (interpreted by the active skill):

```text
/refine verbose       # Show a "before → after" diff for each prompt
/refine off           # Stop optimizing
/prompt-refine        # Re-activate any time (e.g. after context compaction)
```

> ⚠️ **About "session-level":** this is **conversation-scoped, best-effort** — it stays on while the activation remains in context, not a persistent runtime switch. If a long conversation is compacted and it lapses, just run `/prompt-refine` again. Claude Code users who want **hard enforcement** can enable the optional hook in [`hooks/`](hooks/).

## Built-in Strategies (auto-selected by host model)

| Host model | Series | Strategy source |
|--------|-------------|----------------|
| OpenAI | GPT-4o / 4.1 / o-series | [Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering) |
| Anthropic | Claude 4.x (Opus/Sonnet) | [Best Practices](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering) |
| Google | Gemini 2.5 / 3 | [Prompt Design Strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies) |
| Meta | Llama 3 / 4 | [Prompting Guide](https://www.llama.com/docs/how-to-guides/prompting/) |
| DeepSeek | V3 / R1 | [Prompt Library](https://api-docs.deepseek.com/prompt-library/) |
| Mistral | Large / Codestral | [Best Practices](https://docs.mistral.ai/models/best-practices/prompt-engineering) |
| Alibaba | Qwen 3 / 3.6 | [Model Studio Guide](https://help.aliyun.com/zh/model-studio/prompt-engineering-guide) |
| xAI | Grok 3 / 4 | [grok-prompts](https://github.com/xai-org/grok-prompts) |
| Cohere | Command R / R+ | [Docs](https://docs.cohere.com/) |
| Amazon | Nova | [Nova Prompt Guide](https://docs.aws.amazon.com/nova/latest/nova2-userguide/prompt-engineering-guide.html) |
| Microsoft | Phi-3 / 4 | [Phi Cookbook](https://github.com/microsoft/PhiCookBook) |
| Other / unknown | — | `strategies/universal.md` (fallback) |

## Before & After

Assume you're running on **Claude** (Anthropic strategy auto-selected):

### Before (your raw prompt)
> Help me analyze the competitive landscape of this market

### After (restructured internally)
```xml
<role>You are a senior market analyst specializing in competitive intelligence.</role>
<task>
Analyze the competitive landscape of this market, covering:
1. Key players and their market positions
2. Competitive dynamics and trends
3. Barriers to entry and switching costs
4. Strategic recommendations
</task>
<format>Present as a structured report with clear sections; include specific data where possible.</format>
```

> 💡 You typed one sentence; the model added the role, dimensions, and output format — and **kept your original language** — entirely transparently.
> The same prompt on **GPT** would instead use OpenAI's preferred delimiters + output-format spec, not XML.

## Why Prompt Refine?

| | Prompt Refine | Standalone optimizers |
|---|:---:|:---:|
| **Form** | Agent Skill (lightweight) | Web/Desktop app (heavy) |
| **Model fit** | **Locks onto your model, uses its official strategy** | Generic / manual model choice |
| **Output** | Silent, never interrupts the task | Explicit optimized prompt |
| **Activation** | Conversation-scoped (toggleable) | Single invocation |
| **Language** | Preserves original language & intent | Implementation-dependent |
| **Token cost** | Lightweight (meta-instructions + one strategy) | Medium–High |

## Compatible Platforms

Built on the SKILL.md open standard — usable in Claude Code, Cursor, OpenAI Codex, Gemini CLI, GitHub Copilot, Windsurf, Cline, and other tools that support Agent Skills. **The skills directory path is per each platform's official docs.**

## License

MIT License — free to use, modify, and distribute.

## Contributing

Issues and PRs welcome! For new or improved vendor strategies, read [CONTRIBUTING.md](CONTRIBUTING.md) first.

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Li-Bailiang/prompt-refine&type=Date)](https://star-history.com/#Li-Bailiang/prompt-refine&Date)
