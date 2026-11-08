#!/usr/bin/env python3
"""Wait for GitHub pull-request checks to change using the GitHub CLI.

Usage: pr_wait.py <PR number or URL> [--repo owner/name] [--until green|any-change] [--interval 20]
Requires an authenticated `gh` CLI. This checks CI status only; it does not inspect review threads
or certify that a PR is merge-ready.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from typing import Sequence

PR_URL = re.compile(r"https?://github\.com/([^/]+/[^/]+)/pull/(\d+)(?:[/?#].*)?")
REPO_NAME = re.compile(r"[\w.-]+/[\w.-]+")


def run_gh(args: Sequence[str]) -> subprocess.CompletedProcess[str]:
    """Run gh and return its captured result, surfacing actionable errors."""
    try:
        result = subprocess.run(
            ["gh", *args], text=True, capture_output=True, check=False
        )
    except FileNotFoundError as exc:
        raise RuntimeError("GitHub CLI `gh` is not installed or not on PATH") from exc
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(message or f"gh exited with status {result.returncode}")
    return result


def resolve_pr(pr: str, repo_arg: str | None) -> tuple[str, str]:
    """Resolve a PR number or canonical github.com PR URL to repo and number."""
    value = pr.strip()
    match = PR_URL.fullmatch(value)
    if match:
        repo = repo_arg or match.group(1)
        number = match.group(2)
    elif value.isdigit():
        repo = repo_arg
        number = value
    else:
        raise ValueError("PR must be a number or a github.com pull-request URL")

    if repo is None:
        repo = run_gh(
            ["repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner"]
        ).stdout.strip()
    if not REPO_NAME.fullmatch(repo):
        raise ValueError("repository must use owner/name format")
    return repo, number


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pr", help="pull-request number or URL")
    parser.add_argument("--repo", help="repository in owner/name format")
    parser.add_argument("--until", choices=("green", "any-change"), default="green")
    parser.add_argument("--interval", type=int, default=20)
    args = parser.parse_args()
    if args.interval < 5:
        parser.error("--interval must be at least 5 seconds")

    repo, number = resolve_pr(args.pr, args.repo)
    previous: tuple[tuple[str, str, str], ...] | None = None
    while True:
        payload = run_gh(
            ["pr", "checks", number, "--repo", repo, "--json", "name,bucket,link"]
        ).stdout
        try:
            rows = json.loads(payload or "[]")
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"gh returned invalid JSON: {exc}") from exc
        if not isinstance(rows, list):
            raise RuntimeError("gh returned an unexpected check payload")

        state = tuple(sorted(
            (str(row.get("name", "?")), str(row.get("bucket", "pending")).lower(), str(row.get("link", "")))
            for row in rows if isinstance(row, dict)
        ))
        if state != previous:
            changed_after_initial_snapshot = previous is not None
            summary = ", ".join(f"{name}={status}" for name, status, _ in state)
            print(f"{repo}#{number}: {summary or 'no checks reported'}", flush=True)
            previous = state
            if args.until == "any-change" and changed_after_initial_snapshot:
                return 0

        if args.until == "green":
            statuses = {status for _, status, _ in state}
            if state and statuses <= {"pass", "skipping"}:
                return 0
            if statuses & {"fail", "cancel"}:
                return 1
        time.sleep(args.interval)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        raise SystemExit(130)
    except (RuntimeError, ValueError) as exc:
        print(f"pr_wait: {exc}", file=sys.stderr)
        raise SystemExit(1)
