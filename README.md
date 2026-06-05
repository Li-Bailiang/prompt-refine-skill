<div align="right"><a href="README.en.md">English</a> | <b>中文</b></div>

# 🎯 Prompt Refine

> 让模型按**它自己**的偏好重写你的话 —— 你只管说，重构交给模型。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Standard](https://img.shields.io/badge/Agent%20Skills-SKILL.md-blue)](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview)

## 这是什么？

**Prompt Refine** 是一个轻量的 Agent Skill。激活后，它会先识别**当前正在运行的是哪个模型**，然后**始终用那个模型的官方提示词最佳实践**，在你提问后于内部把请求重组成它最擅长的结构，再作答。你不需要学提示词工程，也看不到中间过程——只感觉到"回答变好了"。

### 核心理念

不同模型偏好不同的提示词结构：Claude 吃 XML 标签，GPT 的推理模型反而要你**别**画蛇添足，Qwen 要你**保留中文**别硬翻译……

所以 Prompt Refine 不按话题在厂商间乱跳，而是**认准你正在用的那个模型**，套用它自家的官方策略。内置 11 家厂商策略，是为了让它**无论跑在哪个模型 / 平台上都最优**——一个 Skill，处处适配。

## 快速开始

### 安装

把本仓库放进你工具的项目级 skills 目录。以 Claude Code 为例：

```bash
git clone https://github.com/Li-Bailiang/prompt-refine.git .claude/skills/prompt-refine
```

各工具的项目级 skills 目录（已于 2026-06 对照官方文档核实）：

| 工具 | 安装目录 |
|------|---------|
| Claude Code | `.claude/skills/prompt-refine` |
| Cursor | `.cursor/skills/prompt-refine`（或 `.agents/skills/`） |
| OpenAI Codex | `.agents/skills/prompt-refine` |
| Gemini CLI | `.gemini/skills/prompt-refine`（或 `.agents/skills/`） |
| GitHub Copilot (VS Code) | `.github/skills/prompt-refine`（或 `.agents/skills/`） |
| Windsurf | `.windsurf/skills/prompt-refine` |
| CodeBuddy | `.codebuddy/skills/prompt-refine` |

> 多数工具同时支持通用别名 **`.agents/skills/`**，放一处即可多工具共用。全局/用户级路径各异（如 `~/.gemini/skills/`、`~/.copilot/skills/`），见各平台文档。
>
> 提示：若不想带入 `.git`，可改用 `npx degit Li-Bailiang/prompt-refine <目录>` 或下载 Release 包。

### 使用

```text
/prompt-refine        # 激活（多数工具：输入 / 选 prompt-refine）
```

激活后，用文本指令控制（由已激活的 skill 解释）：

```text
/refine verbose       # 显示每次「重构前 → 重构后」对比
/refine off           # 停止优化
/prompt-refine        # 上下文被压缩后可随时重新激活
```

> ⚠️ **关于"会话级"**：这是**对话级 best-effort**——只要激活指令还在上下文里就持续生效，并非持久化的运行时开关。若长对话被压缩导致失效，重新 `/prompt-refine` 即可。需要**硬强制**的 Claude Code 用户可启用 [`hooks/`](hooks/) 里的可选 hook。

## 内置策略（按宿主模型自动选用）

| 宿主模型 | 模型系列 | 策略来源 |
|------|---------|---------|
| OpenAI | GPT-4o / 4.1 / o-series | [Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering) |
| Anthropic | Claude 4.x (Opus/Sonnet) | [Best Practices](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering) |
| Google | Gemini 2.5 / 3 | [Prompt Design Strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies) |
| Meta | Llama 3 / 4 | [Prompting Guide](https://www.llama.com/docs/how-to-guides/prompting/) |
| DeepSeek | V3 / R1 | [Prompt Library](https://api-docs.deepseek.com/prompt-library/) |
| Mistral | Large / Codestral | [Best Practices](https://docs.mistral.ai/models/best-practices/prompt-engineering) |
| Alibaba | Qwen 3 / 3.6 | [百炼提示工程指南](https://help.aliyun.com/zh/model-studio/prompt-engineering-guide) |
| xAI | Grok 3 / 4 | [grok-prompts](https://github.com/xai-org/grok-prompts) |
| Cohere | Command R / R+ | [官方文档](https://docs.cohere.com/) |
| Amazon | Nova | [Nova Prompt Guide](https://docs.aws.amazon.com/nova/latest/nova2-userguide/prompt-engineering-guide.html) |
| Microsoft | Phi-3 / 4 | [Phi Cookbook](https://github.com/microsoft/PhiCookBook) |
| 其他/未知 | — | `strategies/universal.md`（通用兜底） |

## 效果对比

假设你正在 **Claude** 上运行（自动选用 Anthropic 策略）：

### 优化前（你的原话）
> 帮我分析一下这个市场的竞争格局

### 优化后（内部重组，**保留中文**）
```xml
<role>你是一位资深市场分析师，擅长竞争情报。</role>
<task>
分析该市场的竞争格局，覆盖：
1. 主要玩家及其市场地位
2. 竞争动态与趋势
3. 进入壁垒与转换成本
4. 战略建议
</task>
<format>以结构化报告呈现，分节清晰，尽量给出具体数据。</format>
```

> 💡 你只打了一句话，模型补全了角色、分析维度、输出格式——**且保留了你的中文**，全程对你透明。
> 若同样这句话跑在 **GPT** 上，它会改用 OpenAI 偏好的分隔符 + 输出格式规范，而不是 XML。

## 为什么选择 Prompt Refine？

| | Prompt Refine | 独立优化工具 |
|---|:---:|:---:|
| **形式** | Agent Skill（轻量） | Web/桌面应用（重） |
| **模型适配** | **认准当前模型，套用其官方策略** | 通用策略 / 手动选模型 |
| **输出** | 静默内化，不阻断任务 | 显式输出优化后 prompt |
| **激活** | 对话级持续（可关闭） | 单次调用 |
| **语言** | 保留原语言与意图 | 视实现而定 |
| **Token** | 轻量（元指令 + 单策略文件） | 中–高 |

## 兼容平台

基于 SKILL.md 开放标准，可用于 Claude Code、Cursor、OpenAI Codex、Gemini CLI、GitHub Copilot、Windsurf、Cline 等支持 Agent Skills 的工具。**各平台 skills 目录路径以其官方文档为准。**

## 许可证

MIT License — 自由使用、修改和分发。

## 贡献

欢迎 Issue 与 PR！新增厂商策略或改进现有策略，请先读 [CONTRIBUTING.md](CONTRIBUTING.md)。

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Li-Bailiang/prompt-refine&type=Date)](https://star-history.com/#Li-Bailiang/prompt-refine&Date)
