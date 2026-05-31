"""Unit tests for tools.validate_contributors."""
from __future__ import annotations

import unittest
from pathlib import Path
import tempfile

from validate_contributors import validate, _check_url


class CheckUrlTests(unittest.TestCase):
    def test_good_https(self):
        self.assertIsNone(_check_url("https://github.com/foo"))

    def test_good_http(self):
        self.assertIsNone(_check_url("http://github.com/foo"))

    def test_reversed_scheme(self):
        msg = _check_url("https//:github.com/foo")
        self.assertIsNotNone(msg)
        self.assertIn("reversed", msg)  # type: ignore[arg-type]

    def test_missing_slashes(self):
        msg = _check_url("https:github.com/foo")
        self.assertIsNotNone(msg)
        self.assertIn("missing //", msg)  # type: ignore[arg-type]

    def test_missing_scheme(self):
        msg = _check_url("github.com/foo")
        self.assertIsNotNone(msg)
        self.assertIn("missing scheme", msg)  # type: ignore[arg-type]

    def test_empty(self):
        msg = _check_url("")
        self.assertIsNotNone(msg)
        self.assertIn("empty", msg)  # type: ignore[arg-type]

    def test_email_allowed(self):
        # Some old entries use an email instead of a URL — allowed.
        self.assertIsNone(_check_url("name@example.com"))


class ValidateFileTests(unittest.TestCase):
    def _write(self, content: str) -> Path:
        tmp = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8")
        tmp.write(content)
        tmp.close()
        return Path(tmp.name)

    def test_clean_file(self):
        p = self._write(
            "- [Alice](https://github.com/alice)\n"
            "- [Bob](https://github.com/bob)\n"
        )
        try:
            r = validate(p)
            self.assertEqual(r.total_entries, 2)
            self.assertEqual(r.valid_links, 2)
            self.assertEqual(len(r.errors), 0)
            self.assertTrue(r.ok())
        finally:
            p.unlink()

    def test_space_before_paren_caught(self):
        p = self._write("- [Alice] (https://github.com/alice)\n")
        try:
            r = validate(p)
            self.assertGreaterEqual(len(r.errors), 1)
            self.assertFalse(r.ok())
        finally:
            p.unlink()

    def test_reversed_scheme_caught(self):
        p = self._write("- [Alice](https//:github.com/alice)\n")
        try:
            r = validate(p)
            self.assertGreaterEqual(len(r.errors), 1)
        finally:
            p.unlink()

    def test_no_link_entry_not_error(self):
        # Some contributors list only their display name; allowed.
        p = self._write("- Alice in Wonderland\n")
        try:
            r = validate(p)
            self.assertEqual(r.no_link, 1)
            self.assertEqual(len(r.errors), 0)
        finally:
            p.unlink()


if __name__ == "__main__":
    unittest.main()
