#!/usr/bin/env python3
"""
Generate country/language onboarding coverage heatmap from README flag links.

Outputs:
  - docs/country-onboarding-heatmap.json
  - docs/country-onboarding-heatmap.html

The README already maps many country flags to translation files.
This script turns that into a maintainable quality map:
  - does linked file exist?
  - is file non-empty?
  - basic readiness score
"""
from __future__ import annotations

import json
import re
from pathlib import Path

README = Path("README.md")

# Matches one badge block line piece:
# <kbd>[<img .../svg/id.svg" ...>](translations/README.id.md)</kbd>
BADGE_RE = re.compile(
    r"svg/([a-z\-]+)\.svg[^\]]*\]\((translations/[^)]+)\)", re.IGNORECASE
)


def status_for_file(path: Path) -> tuple[str, int, str]:
    if not path.exists():
        return "missing", 0, "translation file does not exist"
    text = path.read_text(encoding="utf-8", errors="replace")
    ln = len(text.strip())
    if ln == 0:
        return "empty", 20, "file exists but empty"
    if ln < 200:
        return "thin", 55, "very short translation"
    return "ready", 100, "translation present"


def main() -> int:
    if not README.exists():
        raise SystemExit("README.md not found")

    rows = []
    for line in README.read_text(encoding="utf-8", errors="replace").splitlines():
        for m in BADGE_RE.finditer(line):
            cc = m.group(1).lower()
            rel = m.group(2)
            f = Path(rel)
            st, score, note = status_for_file(f)
            rows.append(
                {
                    "country_code": cc,
                    "translation_file": rel,
                    "status": st,
                    "score": score,
                    "note": note,
                }
            )

    # de-duplicate exact pairs while preserving order
    seen = set()
    uniq = []
    for r in rows:
        key = (r["country_code"], r["translation_file"])
        if key in seen:
            continue
        seen.add(key)
        uniq.append(r)

    # summary
    summary = {"ready": 0, "thin": 0, "empty": 0, "missing": 0, "total": len(uniq)}
    for r in uniq:
        summary[r["status"]] += 1

    out_json = Path("docs/country-onboarding-heatmap.json")
    out_html = Path("docs/country-onboarding-heatmap.html")
    out_json.parent.mkdir(parents=True, exist_ok=True)

    payload = {"summary": summary, "entries": uniq}
    out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def color(status: str) -> str:
        return {
            "ready": "#22c55e",
            "thin": "#eab308",
            "empty": "#f97316",
            "missing": "#ef4444",
        }[status]

    cards = []
    for r in uniq:
        cards.append(
            f"""
            <div class='card' style='border-color:{color(r['status'])}'>
              <div class='cc'>{r['country_code'].upper()}</div>
              <div class='status'>{r['status']} ({r['score']})</div>
              <div class='file'>{r['translation_file']}</div>
            </div>
            """.strip()
        )

    html = f"""<!doctype html>
<html>
<head>
  <meta charset='utf-8' />
  <meta name='viewport' content='width=device-width,initial-scale=1' />
  <title>Country Onboarding Heatmap</title>
  <style>
    body {{ font-family: Inter, Arial, sans-serif; margin: 24px; background:#0b1020; color:#e5e7eb; }}
    h1 {{ margin: 0 0 8px; }}
    .meta {{ color:#93a4c3; margin-bottom:16px; }}
    .legend span {{ display:inline-block; margin-right:12px; }}
    .dot {{ width:10px; height:10px; border-radius:50%; display:inline-block; margin-right:6px; }}
    .grid {{ display:grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap:10px; margin-top:16px; }}
    .card {{ background:#111827; border:2px solid #374151; border-radius:10px; padding:10px; }}
    .cc {{ font-weight:700; font-size:18px; }}
    .status {{ font-size:13px; margin-top:4px; }}
    .file {{ font-size:11px; opacity:.85; margin-top:6px; word-break:break-word; }}
  </style>
</head>
<body>
  <h1>Country/Lang Onboarding Heatmap</h1>
  <div class='meta'>Total: {summary['total']} | ready: {summary['ready']} | thin: {summary['thin']} | empty: {summary['empty']} | missing: {summary['missing']}</div>
  <div class='legend'>
    <span><i class='dot' style='background:#22c55e'></i>ready</span>
    <span><i class='dot' style='background:#eab308'></i>thin</span>
    <span><i class='dot' style='background:#f97316'></i>empty</span>
    <span><i class='dot' style='background:#ef4444'></i>missing</span>
  </div>
  <div class='grid'>
    {''.join(cards)}
  </div>
</body>
</html>
"""
    out_html.write_text(html, encoding="utf-8")

    print(f"Wrote {out_json}")
    print(f"Wrote {out_html}")
    print(json.dumps(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
