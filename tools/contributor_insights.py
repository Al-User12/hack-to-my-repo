#!/usr/bin/env python3
"""
Generate contributor quality metrics for Contributors.md.

Outputs:
  - docs/contributor-quality-report.md

This gives maintainers a concrete health dashboard for a high-churn
beginner-contributor repository.
"""
from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone
import argparse

from validate_contributors import validate


def score(valid_links: int, total_entries: int, errors: int) -> float:
    if total_entries == 0:
        return 0.0
    link_quality = (valid_links / total_entries) * 100
    # Strong penalty on hard errors to keep incentives clear
    penalty = min(errors * 0.75, 35)
    return max(0.0, min(100.0, link_quality - penalty))


def make_report(path: Path, strict: bool = False) -> str:
    rep = validate(path, strict=strict)
    sc = score(rep.valid_links, rep.total_entries, len(rep.errors))
    grade = "A" if sc >= 90 else "B" if sc >= 80 else "C" if sc >= 70 else "D"

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    body = f"""# Contributor Quality Report

Generated: {generated_at}
Source: `{path}`

## Snapshot

- Total entries scanned: **{rep.total_entries}**
- Valid markdown links: **{rep.valid_links}**
- Entries without links: **{rep.no_link}**
- Hard errors: **{len(rep.errors)}**
- Contributor Quality Score (CQS): **{sc:.2f}/100 ({grade})**

## What this means

This repository intentionally welcomes first-time contributors. That creates a
high-volume, high-variance input stream in `Contributors.md`.

The quality toolchain keeps this beginner-friendly workflow scalable by:

1. detecting malformed links before merge,
2. documenting current debt transparently,
3. preventing regression in future pull requests.

## Top detected issues (sample)

"""
    if rep.errors:
        sample = rep.errors[:20]
        for e in sample:
            body += f"- {e}\n"
        if len(rep.errors) > 20:
            body += f"- ... and {len(rep.errors) - 20} more\n"
    else:
        body += "- No hard errors detected.\n"

    body += """
## Maintenance policy

- CI fails if hard errors exceed configured baseline.
- Baseline is intentionally lowered over time as old debt is cleaned.
- New PRs must not increase debt.
"""
    return body


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default="Contributors.md")
    ap.add_argument("--out", default="docs/contributor-quality-report.md")
    args = ap.parse_args()

    src = Path(args.file)
    if not src.exists():
        raise SystemExit(f"ERROR: {src} not found")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    report = make_report(src)
    out.write_text(report, encoding="utf-8")
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
