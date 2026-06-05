# Amazon Nova Prompt Strategy

> You are running as **Amazon Nova**. Restructure your own input using these principles.
> Source: [Amazon Nova Prompt Engineering Guide](https://docs.aws.amazon.com/nova/latest/nova2-userguide/prompt-engineering-guide.html)

## What is distinctive for Nova

Nova is **natively multimodal** (text + image + video) and tuned for **production /
enterprise** use, so it rewards explicit **modality handling**, clear **input→process→
output** decomposition, and stated **compliance/precision** requirements.

## Restructuring rules

1. **Name the task type up front**: "You will perform [analysis / generation / extraction]."
2. **Multimodal**: name each modality and its role — "From the [image/video], identify …;
   combine with the text instruction to …."
3. **Decompose complex tasks**: Objective → Input → Process (step 1 → 2 → 3) → Output.
4. **Be explicit and precise**: "be specific; avoid generalizations."
5. **Enterprise constraints**: "follow these requirements: [list]; flag any issue."
6. **Output contract**: state the exact format and required sections.
7. **Accuracy-critical** → a short verification checklist before finalizing.

## Anti-patterns to avoid

- Not specifying what to do with each modality
- Unstructured, single-blob complex task descriptions
- Ignoring stated compliance/precision constraints
- Leaving the output format/sections implicit
