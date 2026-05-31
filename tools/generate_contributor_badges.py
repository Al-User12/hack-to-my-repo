#!/usr/bin/env python3
"""
Generate contributor badge data from Contributors.md.

Outputs:
  - docs/contributor_badges.json
  - docs/contributor-badges.md

Badge rules (per entry):
  - clean-link: valid markdown link + valid URL
  - needs-fix: markdown/link/url issue detected
  - name-only: no link provided

This gives maintainers a transparent quality layer around each contribution.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]*)\)")
SPACE_LINK_RE = re.compile(r"\[[^\]]+\]\s+\([^)]*\)")


def url_error(url: str) -> str | None:
    u = url.strip()
    if not u:
        return "empty-url"
    if "https//:" in u or "http//:" in u or u.startswith("https//") or u.startswith("http//"):
        return "bad-scheme"
    if re.match(r"^https?:[^/]", u):
        return "missing-slashes"
    if u.startswith("github.com") or u.startswith("www.github.com"):
        return "missing-scheme"
    if "://" not in u and not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", u):
        return "no-scheme"
    return None


def parse_entries(path: Path):
    rows = []
    for n, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        s = raw.strip()
        if not s.startswith("-"):
            continue
        row = {
            "line": n,
            "raw": s,
            "name": None,
            "url": None,
            "badge": None,
            "reason": None,
        }
        if SPACE_LINK_RE.search(raw):
            row["badge"] = "needs-fix"
            row["reason"] = "space-before-paren"
            rows.append(row)
            continue

        m = LINK_RE.search(raw)
        if not m:
            row["badge"] = "name-only"
            row["reason"] = "no-markdown-link"
            rows.append(row)
            continue

        name, url = m.group(1).strip(), m.group(2).strip()
        row["name"] = name
        row["url"] = url
        err = url_error(url)
        if err:
            row["badge"] = "needs-fix"
            row["reason"] = err
        else:
            row["badge"] = "clean-link"
            row["reason"] = "ok"
        rows.append(row)
    return rows


def main() -> int:
    src = Path("Contributors.md")
    out_json = Path("docs/contributor_badges.json")
    out_md = Path("docs/contributor-badges.md")
    out_json.parent.mkdir(parents=True, exist_ok=True)

    rows = parse_entries(src)
    counts = Counter(r["badge"] for r in rows)

    payload = {
        "source": str(src),
        "total_entries": len(rows),
        "summary": counts,
        "entries": rows,
    }
    out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    md = [
        "# Contributor Badges",
        "",
        "This report classifies each contributor entry quality badge:",
        "",
        f"- clean-link: **{counts.get('clean-link',0)}**",
        f"- needs-fix: **{counts.get('needs-fix',0)}**",
        f"- name-only: **{counts.get('name-only',0)}**",
        "",
        "## Meaning",
        "",
        "- 🟢 clean-link: `[name](https://...)` valid.",
        "- 🟡 name-only: no link (allowed legacy format).",
        "- 🔴 needs-fix: malformed markdown or URL.",
        "",
        "## Sample needs-fix entries (first 30)",
        "",
        "| line | reason | raw |",
        "|---:|---|---|",
    ]
    shown = 0
    for r in rows:
        if r["badge"] != "needs-fix":
            continue
        raw = r["raw"].replace("|", "\\|")
        md.append(f"| {r['line']} | {r['reason']} | `{raw}` |")
        shown += 1
        if shown >= 30:
            break

    out_md.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"Wrote {out_json}")
    print(f"Wrote {out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
