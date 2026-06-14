<div align="right"><b>English</b> | <a href="README.zh.md">中文</a></div>

# Examples — before / after

Each example shows the **same kind of raw prompt** refined for a **different host model**.
Notice the structure changes with the *model running the skill*, not the topic — and the
user's **original language is always preserved**.

---

## 1. Host model: Claude — XML structure, Chinese kept

**Before**
> 帮我分析一下这个市场的竞争格局

**After** (`strategies/anthropic.md`)
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

## 2. Host model: GPT-5 (Thinking) — minimal, no added chain-of-thought

**Before**
> figure out the time complexity of this function and whether it can be improved

**After** (`strategies/openai.md`)
> Analyze the time complexity of the function below and state whether it can be
> improved; if so, give the improved complexity and the key idea. Be concise.
>
> ```
> [function]
> ```

> Why no "think step by step"? GPT-5 "Thinking"-class models reason internally — adding
> scaffolding hurts; set **reasoning effort** instead. For a GPT-5 "Instant"-class host,
> the same request would get an explicit "work through it briefly, then answer" plus an
> output-format line.

---

## 3. Host model: Qwen — natural Chinese, no force-translation

**Before**
> 写个正则匹配中国大陆手机号

**After** (`strategies/qwen.md`)
> 你是一位正则表达式专家。请编写一个匹配中国大陆手机号的正则表达式。
> 要求：
> 1. 匹配 11 位、以 1 开头、第二位为 3–9 的号码
> 2. 给出 Python 和 JavaScript 两种写法
> 3. 附 2 个匹配示例与 2 个不匹配示例
> 输出：每种语言一个代码块，附简要说明。

---

## 4. Host model: Phi (SLM) — stripped down, strict output

**Before**
> can you help me write a function that checks if a string is a palindrome, with comments

**After** (`strategies/microsoft-phi.md`)
> Language: Python 3
> Task: function `is_palindrome(s: str) -> bool`, ignoring case and non-alphanumerics.
> Input example: "A man, a plan, a canal: Panama" → True
> Output: ONLY the function, with brief inline comments.

---

## 5. Host model: Cohere Command — RAG grounding + citations

**Before**
> based on these release notes, what changed in the auth module?

**After** (`strategies/cohere.md`)
> [release notes pasted here, clearly delimited]
>
> Using only the release notes above, summarize what changed in the auth module.
> Cite the specific line(s) you used for each point. If something isn't covered, say so.

## 6. Host model: GPT on Codex — outcome + self-verification

**Before**
> add rate limiting to the API

**After** (`strategies/openai.md`)
> Goal: add rate limiting to the public API endpoints.
> Done = requests over the limit return HTTP 429; existing tests still pass; new tests cover
> the limit, a burst, and the reset window.
> Approach: propose a short plan first, then implement in small steps. **Verify your work** —
> run the test suite and the linter before finishing. Put durable repo conventions in
> `AGENTS.md` rather than restating them here.

> Why this shape? Codex produces better output when it can **verify its work** and when large
> tasks are **decomposed**; outcome + success criteria beat step-by-step dictation, and
> durable rules belong in `AGENTS.md`, not the prompt.

---

## 7. Host model: Grok — time-bound, multi-perspective analysis

**Before**
> AI startup growth feels like a bubble. Is this real or hype?

**After** (`strategies/xai-grok.md`)
> As of 2026-06-08, evaluate whether current AI startup momentum appears speculative.
>
> Separate your response into: evidence, interpretation, and uncertainty.
>
> Use 3 perspectives:
>
> 1. Business traction (user growth, retention, retention quality)
> 2. Product defensibility (moat, switching costs, unit economics signal)
> 3. Capital efficiency (burn, runway, dilution, and financing quality)
>
> For each perspective:
> - list what is clearly supported by observable facts
> - list what is inference
> - list what is opinion
>
> End with:
> - most-likely scenario
> - bubble-risk scenario
> - key indicators to watch in the next 90 days

---

## 8. Host model: Kimi — Chinese long-context extraction

**Before**
> 帮我看下这份合同哪里有风险

**After** (`strategies/kimi.md`)
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

## 9. Host model: Z.ai GLM — long-horizon coding agent boundaries

**Before**
> build a crawler and dashboard for these supplier pages

**After** (`strategies/zai-glm.md`)
> Goal: build a supplier-page crawler and a small dashboard from the URLs below.
>
> GLM surface: coding agent with tool use and thinking mode enabled.
>
> Done criteria:
> 1. crawler extracts supplier name, product category, price signal, and contact URL
> 2. dashboard groups suppliers by category and flags missing fields
> 3. tests cover one valid page, one missing-price page, and one unreachable page
>
> Tool boundaries: use only the provided URLs and local repo files. Do not invent supplier
> data; mark missing values as `null`.
>
> Stop after implementation and report: changed files, test command, and remaining risks.
>
> ```text
> [supplier URLs]
> ```

---

> These are illustrative. In normal (non-verbose) mode the user never sees the "after" —
> the model answers the refined version directly. Run `/refine verbose` to see the diff
> for your own prompts.
