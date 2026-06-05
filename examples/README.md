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

## 2. Host model: GPT o-series — minimal, no added chain-of-thought

**Before**
> figure out the time complexity of this function and whether it can be improved

**After** (`strategies/openai.md`)
> Analyze the time complexity of the function below and state whether it can be
> improved; if so, give the improved complexity and the key idea. Be concise.
>
> ```
> [function]
> ```

> Why no "think step by step"? o-series models reason internally — adding scaffolding
> hurts. For a **GPT-4o**-class host, the same request would instead get an explicit
> "work through it briefly, then answer" plus an output-format line.

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

---

> These are illustrative. In normal (non-verbose) mode the user never sees the "after" —
> the model answers the refined version directly. Run `/refine verbose` to see the diff
> for your own prompts.
