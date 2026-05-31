#!/usr/bin/env python3
"""
PR Quality Bot — post contributor-quality review on pull requests.

Runs inside GitHub Actions on PRs that touch Contributors.md.
Reads the repo locally (checked out by the workflow), runs the validator,
and posts a concise review comment. Idempotent: deletes its own previous
comment before posting a new one so the PR timeline stays clean.

Environment variables (set by the Actions workflow):
  GITHUB_TOKEN, GITHUB_REPOSITORY, GITHUB_EVENT_PATH
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path


def _api(token: str, method: str, url: str, payload: dict | None = None):
    data = json.dumps(payload).encode() if payload else None
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json",
            **({"Content-Type": "application/json"} if data else {}),
        },
        method=method,
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def _parse_event() -> tuple[int, str, str]:
    event_path = Path(os.environ.get("GITHUB_EVENT_PATH", ""))
    if not event_path.exists():
        raise SystemExit("GITHUB_EVENT_PATH not set or missing")
    ev = json.loads(event_path.read_text())
    pr = ev["pull_request"]
    return pr["number"], pr["head"]["sha"], pr["html_url"]


def _get_pr_diff_files(token: str, repo: str, pr_number: int) -> list[str]:
    """Get list of files changed in a PR (paginated up to 100)."""
    files = []
    for page in range(1, 3):
        data = _api(
            token,
            "GET",
            f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files?per_page=100&page={page}",
        )
        files.extend(f["filename"] for f in data)
        if len(data) < 100:
            break
    return files


def main() -> int:
    token = os.environ.get("GITHUB_TOKEN", "")
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    if not token or not repo:
        print("Missing GITHUB_TOKEN or GITHUB_REPOSITORY"); return 1

    pr_number, head_sha, pr_url = _parse_event()
    changed = _get_pr_diff_files(token, repo, pr_number)
    if "Contributors.md" not in changed:
        print("Contributors.md not changed — skipping"); return 0

    # Run validator from repo root
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
    from validate_contributors import validate
    rep = validate(Path("Contributors.md"))

    baseline = 31
    total_errors = len(rep.errors)
    delta = total_errors - baseline
    passed = total_errors <= baseline

    if passed:
        gate = "✅ passed"
    else:
        gate = f"❌ {delta} new error(s) above baseline ({baseline})"
        # If only a few, list the most likely new ones
        errors_to_show = rep.errors[max(0, baseline) : baseline + 10]
    # Show first errors regardless for reviewer reference
    error_lines = ""
    for e in rep.errors[:15]:
        error_lines += f"  - {e}\n"
    if len(rep.errors) > 15:
        error_lines += f"  - …and {len(rep.errors) - 15} more\n"

    comment_body = f"""## 🧪 Contributor Quality Report (PR #{pr_number})

**Gate:** {gate}
**Errors:** {total_errors} / baseline {baseline}
**Valid links:** {rep.valid_links}
**No-link entries:** {rep.no_link}
**Entries scanned:** {rep.total_entries}

---

### Detected issues (first 15)

{error_lines if error_lines else "_No errors detected._"}

---

> _This review is automated. If errors are pre-existing, they will appear in the baseline._
> _Use `python tools/fix_contributors.py --apply` to auto-fix common issues._
"""

    # Idempotent: delete previous bot comments (look for marker)
    marker = "## 🧪 Contributor Quality Report (PR #"
    comments = _api(token, "GET", f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments?per_page=100")
    for c in comments:
        if marker in c.get("body", "") and c.get("user", {}).get("login", "") == "github-actions[bot]":
            _api(token, "DELETE", f"https://api.github.com/repos/{repo}/issues/comments/{c['id']}")

    _api(token, "POST", f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments", {"body": comment_body})

    # Fail the workflow if above baseline
    if not passed:
        print(f"FAIL: {total_errors} errors exceeds baseline {baseline}")
        return 1

    print(f"PASS: {total_errors} errors (within baseline {baseline})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
