#!/usr/bin/env python3
"""
Housekeeping script to validate translation links and missing files.

Checks:
- translation links listed in translations/Translations.md
- missing translation files referenced in the index
- obvious broken local markdown links within translation files

Exits non-zero on failures, zero on success.
"""
import re
import sys
from pathlib import Path

TRANSLATIONS_DIR = Path("translations")
TRANSLATIONS_INDEX = TRANSLATIONS_DIR / "Translations.md"


def extract_local_links(file_path: Path) -> list[str]:
    """Extract relative/local markdown links from a file."""
    links = []
    content = file_path.read_text(encoding="utf-8")
    pattern = re.compile(r"\]\(([^)]+)\)")
    for match in pattern.finditer(content):
        link = match.group(1).strip()
        if not link.startswith("http") and not link.startswith("#") and not link.startswith("mailto:"):
            links.append(link)
    return links


def check_files() -> list[str]:
    """Validate translation index links and local links in translation files."""
    errors = []

    if not TRANSLATIONS_DIR.exists():
        print("Warning: translations/ directory not found. Skipping validation.")
        return errors

    # Check links in Translations.md index
    if TRANSLATIONS_INDEX.exists():
        links = extract_local_links(TRANSLATIONS_INDEX)
        for link in links:
            target = (TRANSLATIONS_INDEX.parent / link).resolve()
            # Only flag missing files that are expected to be in the translations directory
            try:
                target.relative_to(TRANSLATIONS_DIR)
                if not target.exists():
                    errors.append(f"Missing file referenced in index: {link}")
            except ValueError:
                pass  # Skip links pointing outside translations/

    # Check local links within each translation file
    for md_file in TRANSLATIONS_DIR.rglob("*.md"):
        if md_file.name == "Translations.md":
            continue
        links = extract_local_links(md_file)
        for link in links:
            target = (md_file.parent / link).resolve()
            if not target.exists():
                errors.append(f"Broken local link in {md_file.name}: {link}")

    return errors


def main() -> int:
    errors = check_files()
    if errors:
        print("Translation validation failed:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("All translation links and files are valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
