"""Regression tests for malformed inputs and GitHub CLI check-state handling."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "skills" / "babysit-pr" / "scripts"))

import audit_skill_overlap  # noqa: E402
import pr_wait  # noqa: E402
from validate_skills import validate_sources  # noqa: E402


class SourceRegistryRegressionTests(unittest.TestCase):
    def test_rejects_non_object_source_registry(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "sources.json"
            path.write_text("[]", encoding="utf-8")
            errors = validate_sources(path, [])
        self.assertTrue(any("top-level JSON value must be an object" in error for error in errors))

    def test_rejects_non_string_source_reference(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "sources.json"
            data = {
                "upstream_sources": {
                    "known": {"url": "https://example.com", "license": "MIT", "role": "test"}
                },
                "skill_sources": {
                    "sample": {
                        "relationship": "workflow-inspired; instruction text independently written",
                        "sources": [{"bad": "reference"}],
                    }
                },
            }
            path.write_text(json.dumps(data), encoding="utf-8")
            errors = validate_sources(path, ["sample"])
        self.assertTrue(any("must be strings" in error for error in errors))


class PullRequestWatcherRegressionTests(unittest.TestCase):
    def test_parses_pending_snapshot_when_gh_returns_exit_code_8(self) -> None:
        completed = subprocess.CompletedProcess(
            ["gh"],
            8,
            '[{"name":"ci","bucket":"pending","link":"https://example.test/1"}]',
            "",
        )
        with patch("pr_wait.subprocess.run", return_value=completed):
            state = pr_wait.get_check_snapshot("42", "example/project")
        self.assertEqual(state[0][1], "pending")

    def test_parses_failed_snapshot_when_gh_returns_exit_code_1(self) -> None:
        completed = subprocess.CompletedProcess(
            ["gh"],
            1,
            '[{"name":"ci","bucket":"fail","link":"https://example.test/1"}]',
            "",
        )
        with patch("pr_wait.subprocess.run", return_value=completed):
            state = pr_wait.get_check_snapshot("42", "example/project")
        self.assertEqual(state[0][1], "fail")

    def test_rejects_nonzero_gh_exit_without_json(self) -> None:
        completed = subprocess.CompletedProcess(["gh"], 8, "", "checks pending")
        with patch("pr_wait.subprocess.run", return_value=completed):
            with self.assertRaisesRegex(RuntimeError, "checks pending"):
                pr_wait.get_check_snapshot("42", "example/project")

    def test_rejects_malformed_check_rows(self) -> None:
        completed = subprocess.CompletedProcess(["gh"], 0, '["not-an-object"]', "")
        with patch("pr_wait.subprocess.run", return_value=completed):
            with self.assertRaisesRegex(RuntimeError, "index 0"):
                pr_wait.get_check_snapshot("42", "example/project")

    def test_rejects_conflicting_repository_and_pr_url(self) -> None:
        with self.assertRaisesRegex(ValueError, "must match"):
            pr_wait.resolve_pr(
                "https://github.com/example/project/pull/42", "other/project"
            )


class OverlapAuditRegressionTests(unittest.TestCase):
    def test_fails_when_no_skill_manifests_exist(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            with patch("sys.argv", ["audit_skill_overlap.py", temp]):
                with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
                    self.assertEqual(audit_skill_overlap.main(), 1)


if __name__ == "__main__":
    unittest.main()
