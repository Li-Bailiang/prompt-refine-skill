#!/usr/bin/env python3
"""Summarize the public Prompt Refine evaluation artifacts."""
from __future__ import annotations

import json
import random
import statistics as st
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIMS = [
    "clarification",
    "structure",
    "completeness",
    "actionability",
    "language_fidelity",
]


def load(name: str) -> dict:
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def prompt_pref(result: dict) -> float:
    wins = ties = total = 0
    for judgment in result.get("judgments", []):
        total += 1
        winner = judgment.get("winner", "tie")
        if winner == "tie":
            ties += 1
        elif judgment["positions"].get(winner) == "refine":
            wins += 1
    return (wins + 0.5 * ties) / total if total else 0.0


def binom_two_sided(k: int, n: int) -> float:
    if n == 0:
        return 1.0
    tail = sum(comb(n, i) for i in range(min(k, n - k) + 1)) / (2**n)
    return min(1.0, 2 * tail)


def summarize_vague() -> None:
    runs = [
        load("results/final_c1.json"),
        load("results/final_c2.json"),
        load("results/final_c3.json"),
    ]
    results = [result for run in runs for result in run["results"]]
    prefs = [prompt_pref(result) for result in results]
    rng = random.Random(7)
    n = len(prefs)
    boot = sorted(sum(prefs[rng.randrange(n)] for _ in range(n)) / n for _ in range(50000))

    wins = ties = judgments = 0
    for result in results:
        for judgment in result.get("judgments", []):
            judgments += 1
            winner = judgment.get("winner", "tie")
            if winner == "tie":
                ties += 1
            elif judgment["positions"].get(winner) == "refine":
                wins += 1
    control = judgments - wins - ties
    win_rate = (wins + 0.5 * ties) / judgments

    ref = sum(pref > 0.5 for pref in prefs)
    ctl = sum(pref < 0.5 for pref in prefs)
    tie = sum(pref == 0.5 for pref in prefs)
    p_two = binom_two_sided(min(ref, ctl), ref + ctl)

    print("VAGUE")
    print(f"  prompts / judgments : {len(results)} / {judgments}")
    print(f"  wins / losses / ties: {wins} / {control} / {ties}")
    print(f"  win-rate            : {win_rate:.1%}")
    print(f"  prompt mean pref    : {st.mean(prefs):.1%}")
    print(
        "  95% bootstrap CI    : "
        f"[{boot[int(.025 * len(boot))]:.1%}, {boot[int(.975 * len(boot))]:.1%}]"
    )
    print(f"  sign test           : two-sided p={p_two:.4g}; prompt directions {ref}/{ctl}/{tie}")
    print("  per-dimension delta :")
    for dim in DIMS:
        vals = []
        for result in results:
            for judgment in result.get("judgments", []):
                scores = judgment.get("scores", {})
                refine_letter = next(k for k, v in judgment["positions"].items() if v == "refine")
                control_letter = next(k for k, v in judgment["positions"].items() if v == "control")
                vals.append(scores[refine_letter][dim] - scores[control_letter][dim])
        print(f"    {dim:18s} {st.mean(vals):+.2f}")


def summarize_guard() -> None:
    run = load("results/guard_live.json")
    summary = run["summary"]
    print("\nGUARD")
    print(f"  prompts / judgments : {summary['config']['n_prompts']} / {summary['config']['judgments']}")
    print(
        "  wins / losses / ties: "
        f"{summary['win_counts']['refine']} / "
        f"{summary['win_counts']['control']} / "
        f"{summary['win_counts']['tie']}"
    )
    print(f"  win-rate            : {summary['refine_win_rate']:.1%}")
    print("  note                : preliminary small-sample non-regression gate")


if __name__ == "__main__":
    summarize_vague()
    summarize_guard()
