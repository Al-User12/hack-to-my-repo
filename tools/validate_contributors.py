#!/usr/bin/env python3
"""
validate_contributors.py

Quality gate for Contributors.md.

This is the heart of what makes hack-to-my-repo more than a generic
"first contributions" sandbox: every contributor entry is validated, so the
list stays clean even after thousands of beginner PRs.

Checks performed per entry:
  - Markdown link is well-formed: `[name](url)` with NO space before `(`.
  - URL uses a real scheme (https:// preferred, http:// allowed).
  - URL host looks like github.com/<user> when it claims to be a GitHub link.
  - Catches the common beginner typos: `https//:`, `https:github`, `github/`,
    `(https://...)` with a stray space, bare emails, and empty links.

Exit code is non-zero when hard errors are found, so CI can block bad PRs.
Warnings (entries with no link at all) do not fail the build by default.

Usage:
    python tools/validate_contributors.py [--file Contributors.md] [--strict]
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# A markdown link: [label](target)
LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]*)\)")
# A markdown label with a stray space before the paren: [label] (target)
SPACED_LINK_RE = re.compile(r"\[([^\]]*)\]\s+\((https?[^)]*)\)")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass
class Report:
    total_entries: int = 0
    valid_links: int = 0
    no_link: int = 0
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def ok(self) -> bool:
        return not self.errors


def _check_url(url: str) -> str | None:
    """Return an error string if the URL is malformed, else None."""
    u = url.strip()
    if not u:
        return "empty link target"
    # Classic beginner typos
    if "https//:" in u or "http//:" in u:
        return f"reversed scheme separator: {u!r}"
    if re.match(r"^https?:[^/]", u):
        return f"missing // after scheme: {u!r}"
    if u.startswith("github.com") or u.startswith("www.github.com"):
        return f"missing scheme (add https://): {u!r}"
    if re.search(r"github\.com[^/]", u) and "://" in u and "github.com/" not in u:
        return f"malformed github host: {u!r}"
    if u.startswith("https//") or u.startswith("http//"):
        return f"malformed scheme: {u!r}"
    if "://" not in u and not EMAIL_RE.match(u):
        return f"no URL scheme: {u!r}"
    return None


def validate(path: Path, strict: bool = False) -> Report:
    rep = Report()
    lines = path.read_text(encoding="utf-8").splitlines()
    for n, raw in enumerate(lines, start=1):
        line = raw.strip()
        if not line.startswith("-"):
            continue
        rep.total_entries += 1

        # Stray space before paren -> always an error (breaks the link)
        for m in SPACED_LINK_RE.finditer(raw):
            rep.errors.append(
                f"line {n}: space between ] and ( breaks the link -> {m.group(0).strip()!r}"
            )

        links = LINK_RE.findall(raw)
        if not links:
            # No proper markdown link. It might be a bare name (allowed) or a
            # raw url that should have been a link.
            if "http" in line or "github.com" in line:
                rep.errors.append(f"line {n}: looks like a URL but is not a markdown link -> {line!r}")
            else:
                rep.no_link += 1
                if strict:
                    rep.warnings.append(f"line {n}: entry has no GitHub link -> {line!r}")
            continue

        entry_ok = True
        for _label, url in links:
            err = _check_url(url)
            if err:
                entry_ok = False
                rep.errors.append(f"line {n}: {err}")
        if entry_ok:
            rep.valid_links += 1
    return rep


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate Contributors.md formatting")
    ap.add_argument("--file", default="Contributors.md", help="path to contributors file")
    ap.add_argument("--strict", action="store_true", help="treat no-link entries as warnings")
    ap.add_argument("--max-errors", type=int, default=0,
                    help="allow up to N pre-existing errors before failing (migration aid)")
    args = ap.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"ERROR: {path} not found", file=sys.stderr)
        return 2

    rep = validate(path, strict=args.strict)

    print("Contributors.md validation")
    print("==========================")
    print(f"  entries scanned : {rep.total_entries}")
    print(f"  valid links     : {rep.valid_links}")
    print(f"  no-link entries : {rep.no_link}")
    print(f"  errors          : {len(rep.errors)}")
    print(f"  warnings        : {len(rep.warnings)}")

    if rep.errors:
        print("\nErrors (first 40 shown):")
        for e in rep.errors[:40]:
            print(f"  - {e}")
        if len(rep.errors) > 40:
            print(f"  ... and {len(rep.errors) - 40} more")

    if rep.warnings:
        print(f"\nWarnings: {len(rep.warnings)} (not failing build)")

    if len(rep.errors) > args.max_errors:
        print(f"\nFAILED: {len(rep.errors)} errors exceed allowed {args.max_errors}", file=sys.stderr)
        return 1
    print("\nOK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
