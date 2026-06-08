from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

import run_eval


class EvalHarnessFlagsTest(unittest.TestCase):
    def make_prompt_file(self, rows: list[dict]) -> Path:
        handle = tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".jsonl", delete=False)
        with handle:
            for row in rows:
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
        return Path(handle.name)

    def test_load_prompts_uses_custom_path_and_limit(self) -> None:
        prompt_file = self.make_prompt_file(
            [
                {"id": "x1", "lang": "en", "domain": "debugging", "prompt": "my app is slow"},
                {"id": "x2", "lang": "zh", "domain": "writing", "prompt": "帮我写一封邮件"},
            ]
        )
        self.addCleanup(lambda: prompt_file.unlink(missing_ok=True))

        prompts = run_eval.load_prompts(prompt_file, limit=1)

        self.assertEqual([p["id"] for p in prompts], ["x1"])

    def test_generate_only_skips_judge_calls_and_writes_answer_pairs(self) -> None:
        prompt_file = self.make_prompt_file(
            [{"id": "x1", "lang": "en", "domain": "debugging", "prompt": "my app is slow"}]
        )
        self.addCleanup(lambda: prompt_file.unlink(missing_ok=True))

        out_name = "test-generate-only.json"
        out_path = run_eval.EVAL_DIR / "results" / out_name
        out_path.unlink(missing_ok=True)
        self.addCleanup(lambda: out_path.unlink(missing_ok=True))

        args = SimpleNamespace(
            host="anthropic",
            gen_model="claude-opus-4-8",
            judge_model="claude-opus-4-8",
            prompts_file=prompt_file,
            generate_only=True,
            limit=0,
            dry_run=True,
            seed=7,
            out=out_name,
        )

        run_eval.run(args)
        payload = json.loads(out_path.read_text(encoding="utf-8"))

        self.assertTrue(payload["summary"]["config"]["generate_only"])
        self.assertEqual(payload["summary"]["config"]["judgments"], 0)
        self.assertEqual(set(payload["results"][0]["answers"]), {"control", "refine"})
        self.assertNotIn("judgments", payload["results"][0])

    def test_suite_defaults_load_vague_and_guard_prompt_sets(self) -> None:
        vague = run_eval.load_suite_prompts("vague", limit=0)
        guard = run_eval.load_suite_prompts("guard", limit=0)

        self.assertEqual(len(vague), 18)
        self.assertEqual(len(guard), 6)
        self.assertEqual(vague[0]["id"], "p01")
        self.assertEqual(guard[0]["id"], "hd01_zh_ambiguous_launch")

    def test_suite_defaults_pick_matching_rubric_files(self) -> None:
        self.assertEqual(run_eval.default_rubric_path("vague").name, "rubric.vague.md")
        self.assertEqual(run_eval.default_rubric_path("guard").name, "rubric.guard.md")

    def test_rubric_file_override_is_recorded_in_summary(self) -> None:
        prompt_file = self.make_prompt_file(
            [{"id": "x1", "lang": "en", "domain": "debugging", "prompt": "my app is slow"}]
        )
        rubric_file = tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False)
        with rubric_file:
            rubric_file.write("Custom rubric for a narrow smoke test.")
        rubric_path = Path(rubric_file.name)
        self.addCleanup(lambda: prompt_file.unlink(missing_ok=True))
        self.addCleanup(lambda: rubric_path.unlink(missing_ok=True))

        out_name = "test-rubric-override.json"
        out_path = run_eval.EVAL_DIR / "results" / out_name
        out_path.unlink(missing_ok=True)
        self.addCleanup(lambda: out_path.unlink(missing_ok=True))

        args = SimpleNamespace(
            host="anthropic",
            suite="guard",
            gen_model="claude-opus-4-8",
            judge_model="claude-opus-4-8",
            prompts_file=prompt_file,
            rubric_file=rubric_path,
            generate_only=True,
            limit=0,
            dry_run=True,
            seed=7,
            out=out_name,
        )

        run_eval.run(args)
        payload = json.loads(out_path.read_text(encoding="utf-8"))

        config = payload["summary"]["config"]
        self.assertEqual(config["suite"], "guard")
        self.assertEqual(config["rubric_file"], str(rubric_path))
        self.assertIsNone(config["api_reproducible_judge"])

    def test_dry_run_judged_summary_marks_synthetic_judge(self) -> None:
        prompt_file = self.make_prompt_file(
            [{"id": "x1", "lang": "en", "domain": "debugging", "prompt": "my app is slow"}]
        )
        self.addCleanup(lambda: prompt_file.unlink(missing_ok=True))

        out_name = "test-synthetic-judge.json"
        out_path = run_eval.EVAL_DIR / "results" / out_name
        out_path.unlink(missing_ok=True)
        self.addCleanup(lambda: out_path.unlink(missing_ok=True))

        args = SimpleNamespace(
            host="anthropic",
            suite="vague",
            gen_model="claude-opus-4-8",
            judge_model="claude-opus-4-8",
            prompts_file=prompt_file,
            rubric_file=None,
            generate_only=False,
            limit=0,
            dry_run=True,
            seed=7,
            out=out_name,
        )

        run_eval.run(args)
        payload = json.loads(out_path.read_text(encoding="utf-8"))

        config = payload["summary"]["config"]
        self.assertEqual(config["judge"], "synthetic_dry_run")
        self.assertFalse(config["api_reproducible_judge"])
        self.assertEqual(config["judgments"], 2)


if __name__ == "__main__":
    unittest.main()
