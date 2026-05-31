#!/usr/bin/env python3
"""
fix_contributors.py

Auto-fix common formatting issues in Contributors.md.
Safe transformations only (no deletions, no content changes).

Fixes applied:
  1. Remove space between ] and ( in markdown links.
  2. Insert missing // after scheme: "https:" -> "https://"
  3. Add missing scheme to github.com URLs.
  4. Strip trailing whitespace from all lines.

Dry-run by default. Pass --apply to write changes.

Usage:
    python tools/fix_contributors.py [--file Contributors.md] [--apply]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

SPACE_LINK_RE = re.compile(r"(\[[^\]]*\])\s+(\([^)]*\))")
MISSING_SLASHES_RE = re.compile(r"(https?):(?=[^/])")
BARE_GITHUB_RE = re.compile(r"(?<!\()(github\.com/\S+)")


def fix_line(line: str) -> tuple[str, list[str]]:
    changes: list[str] = []
    original = line

    # 1. Remove space between ] and (
    m = SPACE_LINK_RE.search(line)
    if m:
        old = m.group(0)
        new = f"{m.group(1)}{m.group(2)}"
        line = line.replace(old, new, 1)
        changes.append(f"removed space: {old!r} -> {new!r}")

    # 2. Fix "https:" missing "//" (but not "https://" already correct)
    for m in MISSING_SLASHES_RE.finditer(line):
        bad = m.group(0)
        good = f"{m.group(1)}://"
        if bad not in line.replace(good, "OK"):
            line = line.replace(bad, good, 1)
            changes.append(f"fixed scheme: {bad!r} -> {good!r}")

    # 3. Add scheme to bare github.com links
    def _add_scheme(m: re.Match) -> str:
        url = m.group(1)
        if "://" not in url and "(" not in url and ")" not in url:
            changes.append(f"added scheme to: {url!r}")
            return f"https://{url}"
        return m.group(0)

    line = BARE_GITHUB_RE.sub(_add_scheme, line)

    # 4. Strip trailing whitespace
    stripped = line.rstrip()
    if stripped != line.rstrip():
        changes.append("stripped trailing whitespace")
    line = stripped

    return line, changes


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(description="Auto-fix Contributors.md formatting")
    ap.add_argument("--file", default="Contributors.md")
    ap.add_argument("--apply", action="store_true", help="write changes (default: dry-run)")
    args = ap.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"ERROR: {path} not found", file=sys.stderr)
        return 2

    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    fixed_lines: list[str] = []
    total_changes = 0
    changed_lines = 0

    for n, raw in enumerate(lines, start=1):
        fixed, changes = fix_line(raw.rstrip("\n"))
        if changes:
            changed_lines += 1
            total_changes += len(changes)
            if not args.apply:
                for c in changes:
                    print(f"  line {n}: {c}")
        fixed_lines.append(fixed + "\n")

    print(f"\nSummary: {total_changes} fixes across {changed_lines} lines")

    if args.apply:
        # Backup
        backup = path.with_suffix(".md.bak")
        if not backup.exists():
            backup.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
            print(f"Backup saved: {backup}")
        path.write_text("".join(fixed_lines), encoding="utf-8")
        print(f"Applied fixes to {path}")
    else:
        print("Dry-run (pass --apply to write)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
