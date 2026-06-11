<div align="right"><a href="README.md">English</a> | <b>中文</b></div>

# 示例 —— 重构前 / 重构后

每个示例展示**同一类原始提问**在**不同宿主模型**下的重构方式。注意：结构随*正在运行 skill 的模型*变化，而非随话题变化——并且**始终保留用户的原始语言**。

---

## 1. 宿主模型：Claude —— XML 结构，保留中文

**重构前**
> 帮我分析一下这个市场的竞争格局

**重构后**（`strategies/anthropic.md`）
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

---

## 2. 宿主模型：GPT-5（Thinking）—— 精简，不添加思维链脚手架

**重构前**
> figure out the time complexity of this function and whether it can be improved

**重构后**（`strategies/openai.md`）
> Analyze the time complexity of the function below and state whether it can be
> improved; if so, give the improved complexity and the key idea. Be concise.
>
> ```
> [function]
> ```

> 为什么不加 "think step by step"？GPT-5 "Thinking" 类模型在内部自行推理，额外脚手架反而有害——
> 应改为设置 **reasoning effort**。若宿主是 GPT-5 "Instant" 类模型，同样的请求则会改为"先简要推演再作答" + 一行输出格式说明。

---

## 3. 宿主模型：Qwen —— 自然中文，不强行翻译

**重构前**
> 写个正则匹配中国大陆手机号

**重构后**（`strategies/qwen.md`）
> 你是一位正则表达式专家。请编写一个匹配中国大陆手机号的正则表达式。
> 要求：
> 1. 匹配 11 位、以 1 开头、第二位为 3–9 的号码
> 2. 给出 Python 和 JavaScript 两种写法
> 3. 附 2 个匹配示例与 2 个不匹配示例
> 输出：每种语言一个代码块，附简要说明。

---

## 4. 宿主模型：Phi（小模型）—— 精简到极致，严格输出

**重构前**
> can you help me write a function that checks if a string is a palindrome, with comments

**重构后**（`strategies/microsoft-phi.md`）
> Language: Python 3
> Task: function `is_palindrome(s: str) -> bool`, ignoring case and non-alphanumerics.
> Input example: "A man, a plan, a canal: Panama" → True
> Output: ONLY the function, with brief inline comments.

---

## 5. 宿主模型：Cohere Command —— RAG 接地 + 引用

**重构前**
> based on these release notes, what changed in the auth module?

**重构后**（`strategies/cohere.md`）
> [此处粘贴 release notes，清晰分隔]
>
> 仅基于上方 release notes，总结 auth 模块的变更。每条结论标注所依据的具体行；
> 若未覆盖某点，请明确说明。

## 6. 宿主模型：Codex 上的 GPT —— 目标导向 + 自我校验

**重构前**
> add rate limiting to the API

**重构后**（`strategies/openai.md`）
> Goal: add rate limiting to the public API endpoints.
> Done = requests over the limit return HTTP 429; existing tests still pass; new tests cover
> the limit, a burst, and the reset window.
> Approach: propose a short plan first, then implement in small steps. **Verify your work** —
> run the test suite and the linter before finishing. Put durable repo conventions in
> `AGENTS.md` rather than restating them here.

> 为什么是这个形态？Codex 在能**自我校验**、且大任务被**拆小**时产出更好；用"目标 + 成功标准"
> 胜过逐步指令，而长期规则应放进 `AGENTS.md`，而不是每次塞进 prompt。

---

## 7. 宿主模型：Grok —— 时间敏感、跨视角研判

**重构前**
> AI startup 的热潮像泡沫吗？这是真趋势还是过热？

**重构后**（`strategies/xai-grok.md`）
> 截至 2026-06-08，评估当前 AI startup 增长是否偏向“投机”信号。
>
> 将回答拆分为：事实依据、解读、未确定项。
>
> 从三种角度展开：
>
> 1. 业务动能（用户增长、留存、留存质量）
> 2. 产品护城河（护城河、转换成本、单位经济学信号）
> 3. 资金效率（消耗率、续航期、稀释和融资质量）
>
> 对每个角度分别给出：
> - 有明确事实支撑的结论
> - 推断得到的判断
> - 观点性判断
>
> 结尾包含：
> - 最可能情景
> - 泡沫风险情景
> - 未来 90 天的关键监测指标

---

## 8. 宿主模型：Kimi — 中文长上下文抽取

**重构前**
> 帮我看下这份合同哪里有风险

**重构后**（`strategies/kimi.md`）
> 你是一名合同审阅顾问。请仅基于下方合同文本，提取对我方不利或需要确认的条款。
>
> 重点关注：
> 1. 付款、交付、验收和违约责任
> 2. 单方解除、自动续约、排他或竞业限制
> 3. 模糊表述、缺失定义、缺失期限
>
> 输出为表格：`条款位置 | 风险点 | 为什么有风险 | 建议修改方向`。
> 如果合同文本没有覆盖某项，请写“未见明确约定”，不要补猜。
>
> ```text
> [合同全文]
> ```

---

> 以上仅为示意。在普通（非 verbose）模式下，用户**看不到**"重构后"——模型直接回答重构后的版本。
> 想看自己提问的对比，输入 `/refine verbose`。
