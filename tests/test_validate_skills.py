"""Tests for Agent Workbench skill and source metadata validation."""
from pathlib import Path
import json
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "skills" / "babysit-pr" / "scripts"))
from validate_skills import (  # noqa: E402
    parse_skill_file,
    validate_role_cards,
    validate_skill_file,
    validate_skills_directory,
    validate_sources,
)


class ParseSkillFileTests(unittest.TestCase):
    def test_parses_valid_frontmatter_and_body(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "SKILL.md"
            path.write_text("---\nname: sample-skill\ndescription: A valid description.\n---\n\n" + "A workflow. " * 20, encoding="utf-8")
            fields, body = parse_skill_file(path)
        self.assertEqual(fields["name"], "sample-skill")
        self.assertTrue(body.startswith("A workflow."))

    def test_rejects_missing_frontmatter(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "SKILL.md"
            path.write_text("No metadata here.", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "frontmatter"):
                parse_skill_file(path)

    def test_rejects_duplicate_keys(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "SKILL.md"
            path.write_text("---\nname: one\nname: two\ndescription: test\n---\n" + "body " * 50, encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate"):
                parse_skill_file(path)


class RepositoryValidationTests(unittest.TestCase):
    def test_validates_all_repository_skills(self):
        errors, names = validate_skills_directory(ROOT / "skills")
        self.assertEqual(errors, [])
        self.assertGreaterEqual(len(names), 40)

    def test_detects_name_folder_mismatch(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "SKILL.md"
            path.write_text("---\nname: wrong-name\ndescription: Valid.\n---\n" + "body " * 50, encoding="utf-8")
            errors = validate_skill_file(path, expected_name="expected-name")
        self.assertTrue(any("does not match folder" in error for error in errors))

    def test_detects_short_workflow(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "SKILL.md"
            path.write_text("---\nname: small\ndescription: Too short.\n---\nTiny.\n", encoding="utf-8")
            errors = validate_skill_file(path)
        self.assertTrue(any("too short" in error for error in errors))

    def test_source_map_covers_each_skill(self):
        _, names = validate_skills_directory(ROOT / "skills")
        errors = validate_sources(ROOT / "sources.json", names)
        self.assertEqual(errors, [])

    def test_validates_role_cards(self):
        errors, count = validate_role_cards(ROOT / "agents")
        self.assertEqual(errors, [])
        self.assertGreaterEqual(count, 7)

    def test_detects_unknown_source_reference(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "sources.json"
            data = {"upstream_sources": {}, "skill_sources": {"sample": {"relationship": "workflow-inspired; instruction text independently written", "sources": ["missing"]}}}
            path.write_text(json.dumps(data), encoding="utf-8")
            errors = validate_sources(path, ["sample"])
        self.assertTrue(any("unknown source" in error for error in errors))

    def test_rejects_incomplete_source_registry_entry(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "sources.json"
            data = {
                "upstream_sources": {"demo": {"url": "http://example.com", "license": "", "role": ""}},
                "skill_sources": {"sample": {"relationship": "original", "sources": []}},
            }
            path.write_text(json.dumps(data), encoding="utf-8")
            errors = validate_sources(path, ["sample"])
        self.assertTrue(any("HTTPS URL" in error for error in errors))
        self.assertTrue(any("missing 'license'" in error for error in errors))
        self.assertTrue(any("missing 'role'" in error for error in errors))


class PullRequestWatcherTests(unittest.TestCase):
    def test_resolves_canonical_pull_request_url(self):
        from pr_wait import resolve_pr
        repo, number = resolve_pr("https://github.com/example/project/pull/42", None)
        self.assertEqual((repo, number), ("example/project", "42"))

    def test_rejects_invalid_pull_request_reference(self):
        from pr_wait import resolve_pr
        with self.assertRaisesRegex(ValueError, "number or a github.com"):
            resolve_pr("not-a-pr", "example/project")

    def test_rejects_invalid_repository_format(self):
        from pr_wait import resolve_pr
        with self.assertRaisesRegex(ValueError, "owner/name"):
            resolve_pr("42", "not a repository")

    def test_any_change_waits_for_a_change_after_initial_snapshot(self):
        import io
        from contextlib import redirect_stdout
        from unittest.mock import patch
        import pr_wait
        import subprocess
        snapshots = [
            '[{"name":"ci","bucket":"pending","link":"https://example.test/1"}]',
            '[{"name":"ci","bucket":"fail","link":"https://example.test/1"}]',
        ]
        completed = [subprocess.CompletedProcess([], 0, value, "") for value in snapshots]
        with patch("sys.argv", ["pr_wait.py", "1", "--repo", "example/project", "--until", "any-change", "--interval", "5"]), \
             patch.object(pr_wait, "run_gh", side_effect=completed) as run_gh, \
             patch.object(pr_wait.time, "sleep"):
            with redirect_stdout(io.StringIO()):
                result = pr_wait.main()
        self.assertEqual(result, 0)
        self.assertEqual(run_gh.call_count, 2)

    def test_green_mode_exits_on_success_bucket(self):
        import io
        from contextlib import redirect_stdout
        from unittest.mock import patch
        import pr_wait
        import subprocess
        completed = subprocess.CompletedProcess([], 0, '[{"name":"ci","bucket":"pass","link":""}]', "")
        with patch("sys.argv", ["pr_wait.py", "1", "--repo", "example/project", "--interval", "5"]), \
             patch.object(pr_wait, "run_gh", return_value=completed) as run_gh:
            with redirect_stdout(io.StringIO()):
                result = pr_wait.main()
        self.assertEqual(result, 0)
        run_gh.assert_called_once()

    def test_green_mode_returns_failure_for_failed_bucket(self):
        import io
        from contextlib import redirect_stdout
        from unittest.mock import patch
        import pr_wait
        import subprocess
        completed = subprocess.CompletedProcess([], 0, '[{"name":"ci","bucket":"fail","link":""}]', "")
        with patch("sys.argv", ["pr_wait.py", "1", "--repo", "example/project", "--interval", "5"]), \
             patch.object(pr_wait, "run_gh", return_value=completed) as run_gh:
            with redirect_stdout(io.StringIO()):
                result = pr_wait.main()
        self.assertEqual(result, 1)
        run_gh.assert_called_once()


if __name__ == "__main__":
    unittest.main()
