"""Unit tests for tools.generate_contributor_badges."""
from __future__ import annotations

import unittest

from generate_contributor_badges import url_error


class UrlErrorTests(unittest.TestCase):
    def test_clean(self):
        self.assertIsNone(url_error("https://github.com/foo"))

    def test_http_ok(self):
        self.assertIsNone(url_error("http://github.com/foo"))

    def test_email_ok(self):
        self.assertIsNone(url_error("foo@example.com"))

    def test_bad_scheme(self):
        self.assertEqual(url_error("https//:github.com/foo"), "bad-scheme")

    def test_missing_slashes(self):
        self.assertEqual(url_error("https:github.com/foo"), "missing-slashes")

    def test_missing_scheme(self):
        self.assertEqual(url_error("github.com/foo"), "missing-scheme")

    def test_empty(self):
        self.assertEqual(url_error(""), "empty-url")

    def test_no_scheme(self):
        self.assertEqual(url_error("just-a-name"), "no-scheme")


if __name__ == "__main__":
    unittest.main()
