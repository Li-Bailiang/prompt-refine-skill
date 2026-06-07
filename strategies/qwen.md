# Alibaba Qwen Prompt Strategy

> You are running as **Qwen / 通义千问**. Restructure your own input using these principles.
> Source: [Model Studio Prompt Engineering Guide](https://help.aliyun.com/zh/model-studio/prompt-engineering-guide) · [视觉理解](https://help.aliyun.com/zh/model-studio/vision)

## What is distinctive for Qwen

Qwen has **native-level Chinese**, holds coherence across **multi-turn** context, and
handles **mixed 中/英** prompts well; the Qwen family also has a strong vision line
(**Qwen-VL**). Its biggest edge is lost the moment you translate a natural Chinese request
into stilted English — so keep the user's language.

## Restructuring rules

1. **Preserve the user's language.** A Chinese request stays Chinese — phrase the refined
   prompt in natural, idiomatic Chinese, never a literal English calque.
2. **Cover the official framing dimensions** — context, objective, style/tone, audience,
   and the desired response — supplying whichever the user left out.
3. **Role in-language + hierarchy**: "你是一位[角色]，负责[领域/任务]。" then
   主目标 → 具体要求（编号）→ 约束 → 输出格式。
4. **Mixed-language tasks**: state the answer language explicitly ("请用中文回答" /
   "respond in English").
5. **Complex tasks → explicit numbered steps**: "先理清核心要素，再逐一分析，最后给出结论"
   so the model reasons before concluding.
6. **Few-shot to stabilize output**: 1–3 input→output examples pin format, tone, and
   wording — the official guide notes examples make repeated outputs more consistent.
7. **Delimit with rare markers** — `###`, `===`, or `>>>` — to separate instructions from
   content and improve parsing.
8. **多模态（Qwen-VL）**：说明每张图要做什么；做文档、表格或网页解析时，直接指定输出结构
   （如 Markdown / HTML / JSON）。

## Anti-patterns to avoid

- Translating a Chinese prompt into English "to optimize it" (do the opposite)
- Missing role/context or the framing dimensions above
- Unspecified answer language in a mixed-language task
- Over-terse prompts for complex analytical work
- Using common words as delimiters, so instructions blur into content
