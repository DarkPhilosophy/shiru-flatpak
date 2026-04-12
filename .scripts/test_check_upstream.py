#!/usr/bin/env python3
"""Regression tests for check_upstream.py published_at validation."""

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent))
import check_upstream  # noqa: E402


def _release(published_at="2024-01-01T12:00:00Z"):
    return {
        "tag_name": "v1.0.0",
        "prerelease": False,
        "author": {"login": "testuser"},
        "html_url": "https://github.com/example/releases/tag/v1.0.0",
        "body": "test body",
        "published_at": published_at,
    }


class TestPublishedAtValidation(unittest.TestCase):
    def _assert_exit_1(self, release):
        with patch.object(check_upstream, "get_latest_release", return_value=release):
            with self.assertRaises(SystemExit) as ctx:
                check_upstream.main()
        self.assertEqual(ctx.exception.code, 1)

    def test_empty_string_exits(self):
        self._assert_exit_1(_release(""))

    def test_missing_key_exits(self):
        release = _release("placeholder")
        del release["published_at"]
        self._assert_exit_1(release)

    def test_date_only_exits(self):
        self._assert_exit_1(_release("2024-01-01"))

    def test_none_value_exits(self):
        self._assert_exit_1(_release(None))

    def test_missing_date_before_t_exits(self):
        self._assert_exit_1(_release("T2024-01-01"))


if __name__ == "__main__":
    unittest.main()
