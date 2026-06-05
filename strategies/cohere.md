# Cohere Command Prompt Strategy

> You are running as **Cohere Command R / R+**. Restructure your own input using these principles.
> Source: [Cohere Documentation](https://docs.cohere.com/)

## What is distinctive for Cohere

Command R/R+ are built for **RAG and document-grounded answering**, with first-class
**citation/grounding** behavior and strong **classification/extraction**. Their edge is
faithfulness to provided sources — so the structure should make the source material and
the grounding requirement unambiguous.

## Restructuring rules

1. **RAG**: put the documents first, clearly separated, then the question last:
   "Using only the documents above, answer: [question]. If the answer isn't there, say so."
2. **Grounding**: "Base every claim on the provided sources; do not fabricate."
3. **Citations**: "Cite the specific passage you used for each claim."
4. **Classification**: "Into exactly one of: [list]. Output only the label."
5. **Extraction**: "Extract [fields] as JSON."
6. **Multi-step**: chain explicitly — "First [step 1]; then, using that, [step 2]."

## Anti-patterns to avoid

- Mixing grounded RAG and free generation without a boundary
- Asking a document question without supplying the document
- Open-ended categories for a classification task
- No citation/grounding instruction when faithfulness matters
