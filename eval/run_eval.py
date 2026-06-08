#!/usr/bin/env python3
"""
Prompt Refine — A/B eval harness.

For each test prompt, generate two answers with the SAME generation model:
  • control: raw prompt, minimal system prompt.
  • refine:  raw prompt + a system prompt that applies the host model's
             strategy (the skill, simulated) before answering.

Then a judge model scores them BLIND and PAIRWISE, with position-swapping
(each pair judged twice with answers swapped) to cancel order bias.

Output: a JSON results file + a printed summary (refine win-rate and per-dimension
score deltas). Run with --dry-run first to validate the pipeline with no API calls.

Public evaluation tooling. The eval harness is tracked in the repository for
reproducibility, but it is not included in the npm package.
"""
from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys
from pathlib import Path

# repo root = .../prompt-refine ; this file is at eval/run_eval.py
REPO_ROOT = Path(__file__).resolve().parents[1]
EVAL_DIR = Path(__file__).resolve().parent

DIMENSIONS = [
    "clarification",      # surfaces missing info / states assumptions vs. blindly guessing
    "structure",         # organized, scannable, ready to act on
    "completeness",      # covers what a good answer needs
    "actionability",     # concrete, usable next steps/output
    "language_fidelity", # same language as the prompt; doesn't distort the ask
]

SUITES = {
    "vague": {
        "prompts_file": "prompts.jsonl",
        "rubric_file": "rubric.vague.md",
        "purpose": "uplift",
    },
    "guard": {
        "prompts_file": "high_discrimination_prompts.jsonl",
        "rubric_file": "rubric.guard.md",
        "purpose": "non_regression",
    },
}

# Structured-output schema for the judge. Note: numeric min/max isn't enforceable
# in json_schema here, so the 1-5 range is stated in the rubric and clamped in code.
_SCORE_OBJ = {
    "type": "object",
    "additionalProperties": False,
    "properties": {d: {"type": "integer"} for d in DIMENSIONS},
    "required": DIMENSIONS,
}
JUDGE_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "reasoning": {"type": "string"},
        "scores": {
            "type": "object",
            "additionalProperties": False,
            "properties": {"A": _SCORE_OBJ, "B": _SCORE_OBJ},
            "required": ["A", "B"],
        },
        "winner": {"type": "string", "enum": ["A", "B", "tie"]},
    },
    "required": ["reasoning", "scores", "winner"],
}

REFINE_TEMPLATE = """You are answering as the assistant. Before composing your answer,
silently restructure the user's request into the structure your model handles best,
applying the strategy below. Preserve the user's intent, requirements, and original
LANGUAGE — change only how the request is expressed, never what is asked. If the request
is already clear, answer directly. Do not show or mention the rewrite; output only the
final answer.

INTERVENTION LEVEL — match the edit to the prompt; prefer delivering over interrogating:
- If the request is vague but a reasonable interpretation exists, give a best-effort
  answer with your assumptions stated up front, THEN ask 1-2 focused follow-ups.
- Reply with clarifying questions ONLY when the missing info is genuinely blocking (the
  answer would be wrong, unsafe, or impossible without it) — and even then, sketch the
  likely shape of the answer. A questions-only reply is the last resort, not the default.

HARD GUARDS (apply to every answer):
- Output-language lock: your final answer MUST be in the user's language, even though
  these instructions and the strategy below are in English. In technical answers keep code
  and identifiers in their original form, but write prose/explanations in the user's language.
- No-scaffold guard: never emit <role>, <task>, <constraints>, XML tags, rewritten
  prompts, or internal checklists. Those are private working notes. The visible response
  must contain ONLY the final answer to the user.

<strategy>
{strategy}
</strategy>
"""
CONTROL_SYSTEM = "You are a helpful assistant."

# ---- live token/cost tracking (real runs only) -------------------------------
USAGE: dict[str, dict[str, int]] = {}


def _track(model: str, resp) -> None:
    u = getattr(resp, "usage", None)
    if not u:
        return
    rec = USAGE.setdefault(model, {"input": 0, "output": 0, "calls": 0})
    rec["input"] += (
        (getattr(u, "input_tokens", 0) or 0)
        + (getattr(u, "cache_read_input_tokens", 0) or 0)
        + (getattr(u, "cache_creation_input_tokens", 0) or 0)
    )
    rec["output"] += getattr(u, "output_tokens", 0) or 0
    rec["calls"] += 1


def _price(model: str, inp: int, outp: int) -> float:
    """Best-effort USD via Anthropic list prices; proxy pricing may differ."""
    m = model.lower()
    if "opus" in m:
        pi, po = 15.0, 75.0
    elif "sonnet" in m:
        pi, po = 3.0, 15.0
    elif "haiku" in m:
        pi, po = 1.0, 5.0
    else:
        pi, po = 3.0, 15.0
    return inp / 1e6 * pi + outp / 1e6 * po


def _extract_json(text: str) -> dict:
    """Parse a JSON object even if the proxy wraps it in markdown fences / prose."""
    t = text.strip()
    if t.startswith("```"):
        t = re.sub(r"^```[a-zA-Z]*\n?", "", t)
        t = re.sub(r"\n?```\s*$", "", t).strip()
    try:
        return json.loads(t)
    except json.JSONDecodeError:
        start, end = t.find("{"), t.rfind("}")
        if 0 <= start < end:
            return json.loads(t[start : end + 1])
        raise


def load_text(path: Path) -> str:
    if not path.exists():
        sys.exit(f"ERROR: required file not found: {path}")
    return path.read_text(encoding="utf-8")


def resolve_eval_path(path: str | Path) -> Path:
    p = Path(path)
    return p if p.is_absolute() else EVAL_DIR / p


def normalize_suite(suite: str | None) -> str:
    name = (suite or "vague").lower()
    if name not in SUITES:
        sys.exit(f"ERROR: unknown suite {suite!r}; expected one of: {', '.join(SUITES)}")
    return name


def default_prompt_path(suite: str | None) -> Path:
    return resolve_eval_path(SUITES[normalize_suite(suite)]["prompts_file"])


def default_rubric_path(suite: str | None) -> Path:
    return resolve_eval_path(SUITES[normalize_suite(suite)]["rubric_file"])


def load_prompts(path: str | Path, limit: int = 0) -> list[dict]:
    prompts = [
        json.loads(line)
        for line in load_text(resolve_eval_path(path)).splitlines()
        if line.strip()
    ]
    return prompts[:limit] if limit else prompts


def load_suite_prompts(suite: str | None, limit: int = 0) -> list[dict]:
    return load_prompts(default_prompt_path(suite), limit)


def build_refine_system(host: str) -> str:
    strategy = load_text(REPO_ROOT / "strategies" / f"{host}.md")
    return REFINE_TEMPLATE.format(strategy=strategy.strip())


def cached_system(text: str) -> list:
    # cache_control is harmless here; it only actually caches when the block exceeds
    # the model's minimum cacheable prefix (~2-4K tokens). Strategy/rubric blocks are
    # usually smaller, so this is a no-op until they grow. See README.
    return [{"type": "text", "text": text, "cache_control": {"type": "ephemeral"}}]


def generate(client, model: str, system_text: str, user_prompt: str, dry: bool) -> str:
    if dry:
        return f"[DRY-RUN answer — system={system_text[:24]!r} prompt={user_prompt[:40]!r}]"
    resp = client.messages.create(
        model=model,
        max_tokens=2000,
        system=cached_system(system_text),
        messages=[{"role": "user", "content": user_prompt}],
    )
    _track(model, resp)
    return "".join(b.text for b in resp.content if b.type == "text").strip()


def judge(client, model: str, rubric: str, prompt: str, ans_a: str, ans_b: str, dry: bool) -> dict:
    if dry:
        return {
            "reasoning": "SYNTHETIC dry-run judgment (no API call).",
            "scores": {
                "A": {d: 3 for d in DIMENSIONS},
                "B": {d: 4 for d in DIMENSIONS},
            },
            "winner": "B",
        }
    dims = ", ".join(f'"{d}"' for d in DIMENSIONS)
    user = (
        f"<user_prompt>\n{prompt}\n</user_prompt>\n\n"
        f"<answer id=\"A\">\n{ans_a}\n</answer>\n\n"
        f"<answer id=\"B\">\n{ans_b}\n</answer>\n\n"
        "Score answer A and answer B on each rubric dimension (integer 1-5), then pick the winner.\n"
        "Return ONLY a raw JSON object (no markdown fences, no prose) with keys: "
        '"reasoning" (string), "scores" (object with "A" and "B", each an object whose '
        f"integer keys are exactly {dims}), and \"winner\" (one of \"A\", \"B\", \"tie\")."
    )
    resp = client.messages.create(
        model=model,
        max_tokens=2000,
        system=cached_system(rubric),
        messages=[{"role": "user", "content": user}],
        output_config={"format": {"type": "json_schema", "schema": JUDGE_SCHEMA}},
    )
    _track(model, resp)
    text = next(b.text for b in resp.content if b.type == "text")
    try:
        return _extract_json(text)
    except Exception as e:  # never let one bad parse kill a paid run or fake a win
        return {
            "reasoning": f"PARSE_FALLBACK {type(e).__name__}: {str(e)[:120]} | raw={text[:160]!r}",
            "scores": {"A": {d: 3 for d in DIMENSIONS}, "B": {d: 3 for d in DIMENSIONS}},
            "winner": "tie",
        }


def clamp(v: int) -> int:
    try:
        return max(1, min(5, int(v)))
    except (TypeError, ValueError):
        return 3


def judge_metadata(dry_run: bool, generate_only: bool) -> tuple[str, bool | None]:
    if generate_only:
        return "skipped", None
    if dry_run:
        return "synthetic_dry_run", False
    return "api_pairwise_position_swap", True


def run(args) -> None:
    suite = normalize_suite(getattr(args, "suite", "vague"))
    prompts_file = getattr(args, "prompts_file", None) or default_prompt_path(suite)
    rubric_file = getattr(args, "rubric_file", None) or default_rubric_path(suite)
    generate_only = bool(getattr(args, "generate_only", False))
    prompts = load_prompts(prompts_file, args.limit)
    rubric_path = resolve_eval_path(rubric_file)
    rubric = load_text(rubric_path)
    refine_system = build_refine_system(args.host)

    # --rejudge: hold generations fixed, re-score saved answers with a new judge.
    rejudge_path = getattr(args, "rejudge", None)
    saved_answers = None
    if rejudge_path:
        rej = json.loads(load_text(resolve_eval_path(rejudge_path)))
        prompts = [r["item"] for r in rej["results"]]
        saved_answers = [r["answers"] for r in rej["results"]]
        if args.limit:
            prompts, saved_answers = prompts[: args.limit], saved_answers[: args.limit]
        generate_only = False  # rejudge always judges

    # --control-from: reuse saved CONTROL answers (by id), regenerate only refine.
    # Isolates a refine/skill change against an unchanged control baseline.
    control_from = getattr(args, "control_from", None)
    saved_control = None
    if control_from:
        cf = json.loads(load_text(resolve_eval_path(control_from)))
        saved_control = {r["item"]["id"]: r["answers"]["control"] for r in cf["results"]}

    client = None
    if not args.dry_run:
        try:
            import anthropic
        except ImportError:
            sys.exit("ERROR: `pip install -r requirements.txt` (anthropic SDK missing).")
        if not (os.getenv("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_AUTH_TOKEN")):
            sys.exit("ERROR: set ANTHROPIC_API_KEY before a real run (or use --dry-run).")
        client = anthropic.Anthropic(max_retries=5)

    rng = random.Random(args.seed)
    results = []
    skipped = []
    judgments_total = 0
    win = {"refine": 0, "control": 0, "tie": 0}
    dim_sum = {"refine": {d: 0 for d in DIMENSIONS}, "control": {d: 0 for d in DIMENSIONS}}
    dim_n = {"refine": 0, "control": 0}

    for i, item in enumerate(prompts, 1):
        prompt = item["prompt"]
        print(f"[{i}/{len(prompts)}] {item.get('id','?')} ({item.get('lang','?')}/{item.get('domain','?')})")
        # Fallible API work first; commit to counters only if it all succeeds, so one
        # bad call can't corrupt aggregates or kill a long (expensive) run.
        try:
            if saved_answers is not None:
                ans = saved_answers[i - 1]
            elif saved_control is not None and item.get("id") in saved_control:
                ans = {
                    "control": saved_control[item["id"]],
                    "refine": generate(client, args.gen_model, refine_system, prompt, args.dry_run),
                }
            else:
                ans = {
                    "control": generate(client, args.gen_model, CONTROL_SYSTEM, prompt, args.dry_run),
                    "refine": generate(client, args.gen_model, refine_system, prompt, args.dry_run),
                }
            if generate_only:
                results.append({"item": item, "answers": ans})
                continue
            # Position-swap: judge twice, control/refine in each slot once.
            local = []
            for pos in ({"A": "control", "B": "refine"}, {"A": "refine", "B": "control"}):
                j = judge(client, args.judge_model, rubric, prompt, ans[pos["A"]], ans[pos["B"]], args.dry_run)
                local.append((pos, j))
        except Exception as e:  # noqa: BLE001 - skip this prompt, keep the run alive
            print(f"   !! skipped {item.get('id','?')}: {type(e).__name__}: {str(e)[:120]}")
            skipped.append(item.get("id", "?"))
            continue

        pair_judgments = []
        for pos, j in local:
            judgments_total += 1
            w = j.get("winner", "tie")
            won = pos.get(w, "tie") if w in ("A", "B") else "tie"
            win[won] += 1
            for letter in ("A", "B"):
                cond = pos[letter]
                for d in DIMENSIONS:
                    dim_sum[cond][d] += clamp(j.get("scores", {}).get(letter, {}).get(d, 3))
                dim_n[cond] += 1
            pair_judgments.append({"positions": pos, "winner": w, "scores": j.get("scores", {}), "reasoning": j.get("reasoning", "")})

        results.append({"item": item, "answers": ans, "judgments": pair_judgments})

    # ---- aggregate ----
    total = judgments_total or 1
    refine_winrate = (win["refine"] + 0.5 * win["tie"]) / total
    dim_delta = {
        d: (dim_sum["refine"][d] / max(1, dim_n["refine"]))
        - (dim_sum["control"][d] / max(1, dim_n["control"]))
        for d in DIMENSIONS
    }
    judge_label, api_reproducible_judge = judge_metadata(args.dry_run, generate_only)
    summary = {
        "config": {
            "suite": suite,
            "suite_purpose": SUITES[suite]["purpose"],
            "host_strategy": args.host,
            "gen_model": args.gen_model,
            "judge_model": args.judge_model,
            "prompts_file": str(resolve_eval_path(prompts_file)),
            "rubric_file": str(rubric_path),
            "n_prompts": len(prompts),
            "n_skipped": len(skipped),
            "skipped_ids": skipped,
            "judgments": judgments_total,
            "dry_run": args.dry_run,
            "generate_only": generate_only,
            "judge": judge_label,
            "api_reproducible_judge": api_reproducible_judge,
            "rejudge_source": str(resolve_eval_path(rejudge_path)) if getattr(args, "rejudge", None) else None,
        },
        "refine_win_rate": None if generate_only else round(refine_winrate, 3),
        "win_counts": win,
        "per_dimension_mean_delta_refine_minus_control": {d: round(v, 2) for d, v in dim_delta.items()},
    }

    out = EVAL_DIR / "results" / args.out
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps({"summary": summary, "results": results}, ensure_ascii=False, indent=2), encoding="utf-8")

    print("\n" + "=" * 60)
    tag = "  [DRY-RUN - synthetic, do NOT cite]" if args.dry_run else ""
    mode = "  [GENERATE-ONLY]" if generate_only else ""
    print(f"SUMMARY{mode}{tag}")
    print("=" * 60)
    print(f"host strategy : {args.host}")
    print(f"suite         : {suite} ({SUITES[suite]['purpose']})")
    print(f"gen / judge   : {args.gen_model}  /  {args.judge_model}")
    print(f"prompts       : {len(prompts)}   judgments: {judgments_total}")
    if generate_only:
        print("judge skipped : true")
    else:
        print(f"refine wins   : {win['refine']}   control wins: {win['control']}   ties: {win['tie']}")
        print(f"REFINE WIN-RATE: {refine_winrate:.1%}")
        print("per-dimension mean delta (refine minus control, range -4..+4):")
        for d in DIMENSIONS:
            print(f"   {d:18s} {dim_delta[d]:+.2f}")
    if USAGE:
        total_cost = 0.0
        print("token usage (input incl. cache / output):")
        for m, r in USAGE.items():
            c = _price(m, r["input"], r["output"])
            total_cost += c
            print(f"   {m:18s} calls={r['calls']:>3d}  in={r['input']:>8d}  out={r['output']:>7d}  ~${c:.3f}")
        print(f"   est. list-price cost: ~${total_cost:.2f}  (proxy pricing may differ)")
    print(f"\nfull results -> {out}")


def main() -> None:
    p = argparse.ArgumentParser(description="Prompt Refine A/B eval.")
    p.add_argument("--host", default="anthropic", help="strategy file under strategies/ (default: anthropic)")
    p.add_argument("--suite", choices=sorted(SUITES), default="vague", help="eval suite: vague uplift or guard non-regression")
    p.add_argument("--gen-model", default="claude-sonnet-4-6", help="model under test")
    p.add_argument("--judge-model", default="claude-opus-4-8", help="judge model")
    p.add_argument("--prompts-file", default=None, help="JSONL prompt file override, relative to eval dir unless absolute")
    p.add_argument("--rubric-file", default=None, help="rubric markdown override, relative to eval dir unless absolute")
    p.add_argument("--generate-only", action="store_true", help="generate control/refine answers and skip judge calls")
    p.add_argument("--rejudge", default=None, help="path to a prior results JSON; skip generation, re-judge its saved answers with --judge-model")
    p.add_argument("--control-from", default=None, help="path to prior results JSON; reuse its saved CONTROL answers (by id), regenerate only refine")
    p.add_argument("--limit", type=int, default=0, help="only the first N prompts")
    p.add_argument("--dry-run", action="store_true", help="no API calls; validate the pipeline")
    p.add_argument("--seed", type=int, default=7)
    p.add_argument("--out", default="latest.json", help="results filename under results/")
    run(p.parse_args())


if __name__ == "__main__":
    main()
