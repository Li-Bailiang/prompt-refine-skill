# Alibaba Qwen Prompt Strategy

> You are running as **Qwen / 通义千问**. Restructure your own input using these principles.
> Source: [Alibaba Cloud Model Studio Prompt Engineering Guide](https://help.aliyun.com/zh/model-studio/prompt-engineering-guide) · [视觉理解](https://help.aliyun.com/zh/model-studio/vision)

## What is distinctive for Qwen

Qwen has **native-level Chinese** understanding and generation, keeps strong coherence
across **multi-turn** context, and processes **mixed 中/英** prompts well. Its biggest
edge is lost if you translate a natural Chinese request into stilted English.

## Restructuring rules

1. **Preserve the user's language.** A Chinese request stays Chinese; phrase the
   refined prompt in natural, idiomatic Chinese (not a literal English calque).
2. **Define the role in-language**: "你是一位[角色]，负责[领域/任务]。"
3. **Structure hierarchically**: 主目标 → 具体要求（编号）→ 约束 → 输出格式。
4. **Mixed-language tasks**: state the answer language explicitly ("请用中文回答" /
   "respond in English").
5. **Reasoning**: "请逐步分析：先理清核心要素，再逐一分析，最后给出结论。"
6. **Quality bar**: "确保回答准确、完整、条理清晰。"
7. **多模态（Qwen-VL）**：说明每张图要做什么；做文档、表格或网页解析时，直接指定
   输出结构（如 Markdown / HTML / JSON）。

## Anti-patterns to avoid

- Translating a Chinese prompt into English "to optimize it" (do the opposite)
- Missing role context
- Unspecified answer language in a mixed-language task
- Over-terse prompts for complex analytical work
