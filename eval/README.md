# Prompt Refine eval harness

Public tooling for checking whether Prompt Refine helps in the places it is supposed
to help, without hiding regressions behind one blended win-rate. This folder is tracked
so README claims can be inspected and rerun. It is intentionally excluded from the npm
package; using the skill does not require Python or the Anthropic SDK.

## Suites

| Suite | Prompt file | Rubric | Purpose |
|---|---|---|---|
| `vague` | `prompts.jsonl` | `rubric.vague.md` | Small smoke suite for underspecified prompts. |
| `guard` | `high_discrimination_prompts.jsonl` | `rubric.guard.md` | Measures non-regression on clear or constraint-heavy prompts. |

The published 120-prompt vague result uses the three chunk files
`prompts.all_c1.jsonl`, `prompts.all_c2.jsonl`, and `prompts.all_c3.jsonl`, with matching
result files in `results/final_c*.json`. Use `guard` as a quality gate: refine should
not damage JSON/config outputs, word limits, language fidelity, or direct-answer tasks.

## What it does

For each prompt, the same generation model produces two answers:

| Condition | System prompt |
|---|---|
| `control` | Minimal: "You are a helpful assistant." |
| `refine` | Simulates the skill by applying `strategies/<host>.md` before answering. |

A judge model can then score the pair blind and pairwise, with position swapping to
reduce order bias. The harness writes a summary plus every generated answer and
judgment to `results/<out>.json`.

## Run it

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...        # Windows: $env:ANTHROPIC_API_KEY="sk-ant-..."

# Free plumbing checks:
python run_eval.py --dry-run --suite vague
python run_eval.py --dry-run --suite guard

# Low-cost generation-only samples:
python run_eval.py --suite vague --limit 3 --generate-only --out vague-sample.json
python run_eval.py --suite guard --limit 3 --generate-only --out guard-sample.json

# Full judged runs:
python run_eval.py --suite vague --out vague-full.json
python run_eval.py --suite guard --out guard-full.json

# Reproduce the public 120-prompt vague run in three chunks:
python run_eval.py --suite vague --prompts-file prompts.all_c1.jsonl --out final_c1.json
python run_eval.py --suite vague --prompts-file prompts.all_c2.jsonl --out final_c2.json
python run_eval.py --suite vague --prompts-file prompts.all_c3.jsonl --out final_c3.json

# Summarize the checked-in public result files:
python analyze_public.py
```

Useful flags: `--host openai`, `--gen-model`, `--judge-model`, `--suite vague|guard`,
`--prompts-file`, `--rubric-file`, `--generate-only`, `--limit N`, and `--out`.
Defaults: suite `vague`, generation `claude-sonnet-4-6`, judge `claude-opus-4-8`.

## Interpreting results

- `vague` answers the uplift question: does refine help users move forward from vague
  prompts through better assumptions, structure, and actionability?
- `guard` answers the safety question: does refine avoid making clear tasks worse?
- Do not merge the two suites into one headline win-rate. A good result can be "vague
  improves, guard is neutral"; a bad result can be "vague improves, but guard regresses."
- `--generate-only` produces answer pairs only. Any manual or conversation-side judge
  must be labeled as not API-reproducible in the derived result file.

## Honest caveats

- Do not cite `--dry-run` numbers. Dry-run uses synthetic answers and judgments.
- One judge model has bias. For a public claim, use at least one second judge.
- A full judged run costs `N * (2 generations + 2 judgments)` calls. Judge calls usually
  dominate cost, so use `--generate-only` when budget is tight.
- Keep time-sensitive prompts out of the suite unless the evaluation explicitly controls
  browsing and current-knowledge assumptions.

## Public reporting rule

Only put a README headline in the public repo when all are true:

- `vague` win-rate is above 50% on a meaningful sample.
- `guard` shows no material non-regression failure.
- The judge setup is reproducible or clearly labeled as manual/non-reproducible.
- The sample size, suite, generation model, and judge model are named next to the number.

## Checked-in public results

| Suite | Result files | Sample | Headline |
|---|---|---:|---|
| `vague` | `results/final_c1.json`, `results/final_c2.json`, `results/final_c3.json` | 120 prompts / 240 judgments | 74.0% refine win-rate, 95% bootstrap CI [66.9%, 80.6%] |
| `guard` | `results/guard_live.json` | 6 prompts / 12 judgments | 66.7% preliminary non-regression win-rate |

The guard suite is intentionally reported as preliminary because it is small. It is a
quality gate, not a broad proof that all clear prompts are unaffected.
