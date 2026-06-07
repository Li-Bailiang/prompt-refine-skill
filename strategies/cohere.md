# Cohere Command Prompt Strategy

> You are running as **Cohere Command** (Command A / A+, R / R+). Restructure your own input using these principles.
> Source: [Cohere — Crafting Effective Prompts](https://docs.cohere.com/docs/crafting-effective-prompts) · [Command A](https://docs.cohere.com/docs/command-a) · [Image inputs](https://docs.cohere.com/docs/image-inputs)

## What is distinctive for Cohere

The Command family is built for **RAG and document-grounded answering**, with first-class
**citation/grounding** behavior and strong **classification/extraction**. The current
flagships (**Command A / A+**) add reasoning, vision, and agentic tool use, but the
family's defining edge is still faithfulness to provided sources — so the structure should
make the source material and the grounding requirement unambiguous.

## Restructuring rules

1. **RAG**: put the documents first, clearly separated, then the question last:
   "Using only the documents above, answer: [question]. If the answer isn't there, say so."
2. **Grounding**: "Base every claim on the provided sources; do not fabricate."
3. **Citations**: "Cite the specific passage you used for each claim."
4. **Classification**: "Into exactly one of: [list]. Output only the label."
5. **Extraction**: "Extract [fields] as JSON."
6. **Multi-step**: chain explicitly — "First [step 1]; then, using that, [step 2]."
7. **Multimodal (Command A Vision)**: supports several images per request with a detail
   (low/high/auto) control; name each image's role, and for document images keep the
   grounding/citation requirement explicit.

## Anti-patterns to avoid

- Mixing grounded RAG and free generation without a boundary
- Asking a document question without supplying the document
- Open-ended categories for a classification task
- No citation/grounding instruction when faithfulness matters
