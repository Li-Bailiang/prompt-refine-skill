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
  <a href="#项目介绍">项目介绍</a> |
  <a href="#快速开始">快速开始</a> |
  <a href="#功能演示">功能演示</a> |
  <a href="#内置策略">内置策略</a> |
  <a href="#评测">评测</a> |
  <a href="#兼容平台">兼容平台</a> |
  <a href="examples/README.zh.md">示例</a>
</p>

---

## 项目介绍

**Prompt Refine** 是一个轻量、跨平台的 Agent Skill。激活后，它会识别**当前正在运行并回答问题的模型**，然后在回答前应用该模型家族对应的提示词策略。

核心设计很简单，但很关键：**按宿主模型路由，而不是按任务路由**。如果当前是 Claude 在回答，就整段对话都使用 Anthropic 策略；如果当前是 GPT 在回答，就使用 OpenAI 策略。写代码任务不会让 Claude 切到 GPT 风格，写作任务也不会让 GPT 切到 Claude XML。

因此它可以用于支持 Agent Skills 的工具：Claude Code、Cursor、OpenAI Codex、Gemini CLI、GitHub Copilot、Windsurf、CodeBuddy 以及其他兼容 Agent。

它也会温和利用上下文：后续请求可以继承对话中相关的目标、约束、术语和偏好，但仍以用户最新指令为准。

它刻意保持轻量：无运行时依赖、无应用服务、不会额外调用一个“优化器模型”，上下文里只需要短小的 skill 文件和一个被选中的策略文件。目标是在不大量增加 token 成本的前提下，让请求结构更适合当前模型。

## 功能演示

同一个用户请求，会根据**宿主模型**形成不同的内部结构。下面展示的是隐藏重构的形态；正常模式下，用户只看到最终答案。

### 1. 模糊需求：补出必要结构

用户请求：

```text
帮我分析一下这个市场的竞争格局
```

Anthropic Claude 格式：

```xml
<role>你是一位资深市场分析师，擅长竞争情报。</role>
<context>
用户没有说明具体市场、地域、客户群或时间范围。
保留不确定性；把可行假设说清楚，不编造事实。
</context>
<task>
在最可能的用户意图下，分析该市场的竞争格局。
</task>
<constraints>
- 开头先说明对市场、受众、地域和时间范围的假设。
- 区分较有把握的判断和未知信息。
- 不声称实时市场数据，除非用户已提供或可以验证。
- 只提出 1-2 个最能改进分析的追问。
</constraints>
<format>
使用这些小节：假设、竞争地图、壁垒与转换成本、战略含义、未知信息、后续问题。
</format>
<success_criteria>
即使用户尚未补充市场范围，答案也应可用，并清楚标出哪些结论依赖假设。
</success_criteria>
```

OpenAI GPT 格式：

```text
目标：把一个范围不完整的市场分析请求，转成可用的第一版竞争格局分析。

用户请求：
"""帮我分析一下这个市场的竞争格局"""

相关上下文：
- 市场、地域、受众和时间范围均缺失。
- 保留不确定性，并明确说明假设。

要求：
1. 先说明假设的市场范围。
2. 识别可能的玩家类别和竞争动态。
3. 比较进入壁垒、转换成本和战略含义。
4. 标注未知信息，不编造事实。

硬约束：
- 不声称实时市场数据，除非用户已提供或可以验证。
- 只提出 1-2 个后续问题。

输出格式：使用 Markdown 小标题：假设、竞争地图、壁垒、战略含义、未知信息、后续问题。
```

### 2. 清晰需求：保留硬约束

用户请求：

```text
请写一个 5 点 npm 发布检查清单，每点不超过 8 个字。
```

Anthropic Claude 格式：

```xml
<context>
用户给出了严格的格式要求。不要扩展任务范围。
</context>
<task>写出恰好 5 点 npm 发布检查清单。</task>
<constraints>
- 每点不超过 8 个字。
- 覆盖 package.json、README、LICENSE、版本号和 dry-run 发布。
- 只返回清单项，不添加引言或解释。
</constraints>
<format>使用编号列表，每项是一个简短的祈使句。</format>
<success_criteria>
恰好 5 项，每项不超过 8 个字，并覆盖所有指定主题。
</success_criteria>
```

OpenAI GPT 格式：

```text
任务：写出恰好 5 点 npm 发布检查清单。

上下文：用户已经给出清晰硬约束，保留这些约束，不额外扩展范围。

硬约束：
- 每点不超过 8 个字。
- 覆盖 package.json、README、LICENSE、版本号和 dry-run 发布。
- 只返回清单，不添加解释。

输出契约：
- 编号列表。
- 恰好 5 行。
- 无引言、无结尾说明。

回答前自检：每项不超过 8 个字，并覆盖一个指定发布主题。
```

### 用户看到什么

用户只看到最终答案。除非启用 `/refine verbose`，否则中间重构不会显示。对于已经很清楚的请求，Prompt Refine 应尽量轻量处理，重点保护用户的硬约束。

策略始终跟随**宿主模型**，不是跟随任务话题：Claude 使用 Claude 偏好的结构，GPT 使用 GPT 偏好的结构。

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

## 评测

Prompt Refine 在 **120 条模糊提示词**上做过盲测的 A/B 评测（60 条英文 + 60 条中文，覆盖 32 个领域）。同一个生成模型针对每条提示词回答两次——一次原始、一次启用 Prompt Refine，由独立的裁判模型在不知道哪边是哪边的前提下打分。每对答案还会交换位置再判一次，以抵消顺序偏差。

### 关键结果

| | 结果 |
|---|---|
| Refine 对 raw 的胜率 | **74.0%**（240 次判罚中 167 胜 / 52 负 / 21 平） |
| 95% bootstrap 置信区间（按 prompt，n = 120） | **[66.9%, 80.6%]** |
| 符号检验 | **p < 0.0001** |
| 英文 / 中文 | 75.0% / 72.9% |
| 等长子集胜率 | **64.7%**（refine 答案长度在 raw 的 ±25% 以内） |

等长胜率与主指标一并公布，用于排除裁判可能存在的长度偏好。在等长子集上，本版本胜率为 **64.7%**，而上一版本的同口径仅为 **50.5%**——说明改进是真实的答案质量提升，而不仅仅是输出更长。

### 各维度差值（refine − raw，1–5 分制）

| 维度 | Δ |
|---|---|
| 可执行性 (actionability) | **+0.96** |
| 完整性 (completeness) | **+0.81** |
| 结构性 (structure) | **+0.49** |
| 澄清问询 (clarification) | **+0.35** |
| 语言保真 (language fidelity) | +0.03 |

### 稳健性检查

| 检查 | 结果 |
|---|---|
| 内部脚手架泄漏（`<role>` / `<task>` / 重写后的提示词被输出） | **0 / 120** |
| 中文提示词上的正文语言切换（剔除代码后） | **0 / 60** |
| JSON 解析回退 · 被跳过的样本 | 0 · 0 |

模型配置：生成模型 `claude-sonnet-4-6`，裁判模型 `claude-opus-4-8`。当前评测的宿主模型策略为 Anthropic (`strategies/anthropic.md`)；其他策略文件采用相同设计，但尚未做过同等规模的评测。

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
