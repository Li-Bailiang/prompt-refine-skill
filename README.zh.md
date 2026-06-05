<p align="center">
  <a href="README.md">English</a> |
  <a href="README.zh.md"><b>中文</b></a>
</p>

<h1 align="center">Prompt Refine</h1>

<p align="center">
  <b>一个按当前宿主模型自动优化提示词结构的 Agent Skill。</b>
</p>

<p align="center">
  你只需要正常提问。正在回答的模型会在内部把请求改写成自己更擅长处理的结构，
  保留原语言，然后直接给出答案。
</p>

<p align="center">
  <a href="https://github.com/Li-Bailiang/prompt-refine-skill/stargazers">
    <img alt="GitHub stars" src="https://img.shields.io/github/stars/Li-Bailiang/prompt-refine-skill?style=for-the-badge">
  </a>
  <a href="LICENSE">
    <img alt="MIT license" src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge">
  </a>
  <a href="SKILL.md">
    <img alt="Agent Skill" src="https://img.shields.io/badge/Agent%20Skill-SKILL.md-blue?style=for-the-badge">
  </a>
  <img alt="Zero dependencies" src="https://img.shields.io/badge/dependencies-zero-lightgrey?style=for-the-badge">
  <img alt="Low token overhead" src="https://img.shields.io/badge/token%20overhead-low-brightgreen?style=for-the-badge">
</p>

<p align="center">
  <a href="#项目介绍">项目介绍</a> |
  <a href="#快速开始">快速开始</a> |
  <a href="#功能演示">功能演示</a> |
  <a href="#内置策略">内置策略</a> |
  <a href="#兼容平台">兼容平台</a> |
  <a href="examples/README.zh.md">示例</a>
</p>

---

## 项目介绍

**Prompt Refine** 是一个轻量、跨平台的 Agent Skill。激活后，它会识别**当前正在运行并回答问题的模型**，然后在回答前应用该模型家族对应的提示词策略。

核心设计很简单，但很关键：**按宿主模型路由，而不是按任务路由**。如果当前是 Claude 在回答，就整段对话都使用 Anthropic 策略；如果当前是 GPT 在回答，就使用 OpenAI 策略。写代码任务不会让 Claude 切到 GPT 风格，写作任务也不会让 GPT 切到 Claude XML。

因此它可以用于支持 Agent Skills 的工具：Claude Code、Cursor、OpenAI Codex、Gemini CLI、GitHub Copilot、Windsurf、CodeBuddy 以及其他兼容 Agent。

它刻意保持轻量：无运行时依赖、无应用服务、不会额外调用一个“优化器模型”，上下文里只需要短小的 skill 文件和一个被选中的策略文件。目标是在不大量增加 token 成本的前提下，让请求结构更适合当前模型。

## 功能演示

假设当前宿主模型是 **Claude**，Prompt Refine 会在内部使用 Anthropic 策略。

### 1. 模糊需求：补出必要结构

```text
帮我分析一下这个市场的竞争格局
```

内部重构：

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

### 2. 清晰需求：保留硬约束

```text
请写一个 5 点 npm 发布检查清单，每点不超过 8 个字。
```

内部重构：

```xml
<task>写出恰好 5 点 npm 发布检查清单。</task>
<constraints>
- 每点不超过 8 个字。
- 覆盖 package.json、README、LICENSE、版本号和 dry-run 发布。
- 不添加额外解释。
</constraints>
```

### 用户看到什么

用户只看到最终答案。除非启用 `/refine verbose`，否则中间重构不会显示。对于已经很清楚的请求，Prompt Refine 应尽量轻量处理，重点保护用户的硬约束。

如果同样的请求由 GPT 回答，Prompt Refine 会改用 OpenAI 策略，而不是 XML。策略始终跟随**宿主模型**，不是跟随任务话题。

## 快速开始

把本仓库安装到工具的项目级 skills 目录。以 Claude Code 为例：

```bash
git clone https://github.com/Li-Bailiang/prompt-refine-skill.git .claude/skills/prompt-refine
```

如果不想带入 `.git` 目录，可以使用 Release 包，或：

```bash
npx degit Li-Bailiang/prompt-refine-skill .claude/skills/prompt-refine
```

在对话中激活：

```text
/prompt-refine
```

可用的会话内控制命令：

```text
/refine verbose    # 每次回答前显示简短的 原始 -> 重构 对比
/refine off        # 在本轮对话中停止优化
/prompt-refine     # 上下文压缩或新会话后重新激活
```

## 安装路径

| 工具 | 项目级 skill 路径 |
|---|---|
| Claude Code | `.claude/skills/prompt-refine` |
| Cursor | `.cursor/skills/prompt-refine` 或 `.agents/skills/prompt-refine` |
| OpenAI Codex | `.agents/skills/prompt-refine` |
| Gemini CLI | `.gemini/skills/prompt-refine` 或 `.agents/skills/prompt-refine` |
| GitHub Copilot (VS Code) | `.github/skills/prompt-refine` 或 `.agents/skills/prompt-refine` |
| Windsurf | `.windsurf/skills/prompt-refine` |
| CodeBuddy | `.codebuddy/skills/prompt-refine` |

多数工具也支持通用的 `.agents/skills/` 约定。全局或用户级路径因平台而异，建议以各工具官方文档为准。

## 内置策略

| 宿主模型 | 策略文件 | 来源家族 |
|---|---|---|
| OpenAI GPT / o-series | `strategies/openai.md` | OpenAI 提示词指南 |
| Anthropic Claude | `strategies/anthropic.md` | Anthropic prompt engineering |
| Google Gemini | `strategies/google-gemini.md` | Gemini prompt design |
| Meta Llama | `strategies/meta-llama.md` | Llama prompting guidance |
| DeepSeek V3 / R1 | `strategies/deepseek.md` | DeepSeek prompt library |
| Mistral / Codestral | `strategies/mistral.md` | Mistral best practices |
| Qwen | `strategies/qwen.md` | 阿里云百炼 / Model Studio 指南 |
| xAI Grok | `strategies/xai-grok.md` | xAI Grok prompting references |
| Cohere Command | `strategies/cohere.md` | Cohere docs |
| Amazon Nova | `strategies/amazon-nova.md` | Nova prompt guide |
| Microsoft Phi | `strategies/microsoft-phi.md` | Phi Cookbook |
| 未知宿主 | `strategies/universal.md` | 保守通用兜底 |

## 为什么选择 Prompt Refine？

| | Prompt Refine | 独立提示词优化工具 |
|---|:---:|:---:|
| 形态 | Agent Skill | Web 或桌面应用 |
| 模型适配 | 使用当前运行模型的策略 | 通用策略或手动选择 |
| 输出 | 静默给出最终答案 | 展示优化后的 prompt |
| 激活 | 会话级、可关闭 | 通常单次调用 |
| 语言 | 保留原语言和意图 | 取决于实现 |
| Token 成本 | 低：短 skill + 单策略文件 | 往往需要额外完整优化轮次 |
| 依赖 | 无依赖 | 往往依赖具体应用 |

## 兼容平台

Prompt Refine 遵循 `SKILL.md` Agent Skill 约定，面向支持项目级 skills 的工具，包括 Claude Code、Cursor、OpenAI Codex、Gemini CLI、GitHub Copilot、Windsurf、CodeBuddy 以及其他兼容 Agent。

## 许可证

MIT License。可自由使用、修改和分发。

## 贡献

欢迎提交 Issue 和 Pull Request。新增或改进模型策略前，请先阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

## Star History

<p align="center">
  <a href="https://star-history.com/#Li-Bailiang/prompt-refine-skill&Date">
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=Li-Bailiang/prompt-refine-skill&type=Date">
  </a>
</p>
