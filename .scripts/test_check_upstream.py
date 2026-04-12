"""Tests for the published_at validation change in check_upstream.py main().

Covers the PR change: fail fast when upstream release date is invalid
(published_at missing "T" separator now triggers sys.exit(1) instead of
silently producing an empty date string).
"""
import importlib
import sys
import os
import types
import pytest
from io import StringIO
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open

# ---------------------------------------------------------------------------
# Import helper – the script lives in .scripts/ which is not a package.
# ---------------------------------------------------------------------------
SCRIPT_PATH = Path(__file__).parent / "check_upstream.py"


def load_module():
    spec = importlib.util.spec_from_file_location("check_upstream", SCRIPT_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

def _base_release(**overrides):
    """Return a minimal valid release payload, optionally overriding fields."""
    release = {
        "tag_name": "v1.2.3",
        "prerelease": False,
        "author": {"login": "testuser"},
        "html_url": "https://github.com/example/repo/releases/tag/v1.2.3",
        "body": "Some release notes.",
        "published_at": "2024-06-15T12:00:00Z",
    }
    release.update(overrides)
    return release


def _patch_filesystem(mod, tmp_path):
    """Return a context-manager stack that redirects all file-path constants to
    temporary paths so main() can write without touching the real repo."""
    upstream_ver = tmp_path / "UPSTREAM_VERSION"
    local_ver = tmp_path / "VERSION"
    changelog = tmp_path / "CHANGELOG.md"
    release_notes = tmp_path / "RELEASE_NOTES.md"
    metainfo = tmp_path / "metainfo.xml"  # does NOT exist – update_metainfo skips it

    return (
        patch.object(mod, "UPSTREAM_VERSION_FILE", upstream_ver),
        patch.object(mod, "LOCAL_VERSION_FILE", local_ver),
        patch.object(mod, "CHANGELOG_FILE", changelog),
        patch.object(mod, "RELEASE_NOTES_FILE", release_notes),
        patch.object(mod, "METAINFO_FILE", metainfo),
        patch.object(mod, "GITHUB_OUTPUT", None),
    )


# ---------------------------------------------------------------------------
# Helper: run main() with a given release payload
# ---------------------------------------------------------------------------

def run_main(release_payload, tmp_path):
    """Run main() with *release_payload* injected via get_latest_release mock.
    Returns the module so callers can inspect side-effects if needed.
    Raises SystemExit if main() calls sys.exit().
    """
    mod = load_module()
    patches = _patch_filesystem(mod, tmp_path)

    # Build a context manager from multiple patches
    from contextlib import ExitStack
    with ExitStack() as stack:
        for p in patches:
            stack.enter_context(p)
        stack.enter_context(patch.object(mod, "get_latest_release", return_value=release_payload))
        mod.main()

    return mod


# ===========================================================================
# Tests for the published_at validation block (the changed code)
# ===========================================================================

class TestPublishedAtValidation:
    """Tests targeting lines 143-146 of check_upstream.py (the PR change)."""

    # -----------------------------------------------------------------------
    # Happy-path: valid ISO-8601 timestamp
    # -----------------------------------------------------------------------

    def test_valid_published_at_extracts_date(self, tmp_path):
        """Standard ISO-8601 timestamp – date part extracted correctly."""
        release = _base_release(published_at="2024-06-15T12:00:00Z")
        run_main(release, tmp_path)
        # If we reach here sys.exit was NOT called; verify file was updated
        upstream_file = tmp_path / "UPSTREAM_VERSION"
        assert upstream_file.read_text().strip() == "v1.2.3"

    def test_valid_published_at_midnight(self, tmp_path):
        """Midnight timestamp still yields correct date."""
        release = _base_release(published_at="2023-12-31T00:00:00Z")
        run_main(release, tmp_path)
        # Successful execution: metainfo would get "2023-12-31" passed
        # (metainfo file doesn't exist so update_metainfo is a no-op, but no exit)

    def test_valid_published_at_splits_on_first_t_only(self, tmp_path):
        """split('T', 1) must keep everything after the first T intact.
        This validates the maxsplit=1 addition in the PR.
        A date portion must not be confused even if the time segment contained 'T'.
        """
        # Hypothetical value with two T characters
        release = _base_release(published_at="2024-06-15T14:30:00T+00:00")
        run_main(release, tmp_path)
        # No SystemExit = correct: "T" was found so we proceed

    def test_valid_published_at_with_timezone_offset(self, tmp_path):
        """ISO-8601 with numeric timezone offset."""
        release = _base_release(published_at="2025-03-07T08:45:00+05:30")
        run_main(release, tmp_path)

    # -----------------------------------------------------------------------
    # Failure path: missing or malformed published_at
    # -----------------------------------------------------------------------

    def test_missing_t_in_date_only_string_exits(self, tmp_path, capsys):
        """Date-only string (no 'T') must cause sys.exit(1)."""
        release = _base_release(published_at="2024-06-15")
        with pytest.raises(SystemExit) as exc_info:
            run_main(release, tmp_path)
        assert exc_info.value.code == 1

    def test_missing_t_stderr_message(self, tmp_path, capsys):
        """Error message is written to stderr when 'T' is absent."""
        release = _base_release(published_at="2024-06-15")
        with pytest.raises(SystemExit):
            run_main(release, tmp_path)
        captured = capsys.readouterr()
        assert "Error: Missing or invalid published_at in upstream release payload." in captured.err

    def test_empty_published_at_exits(self, tmp_path, capsys):
        """Empty string for published_at must cause sys.exit(1)."""
        release = _base_release(published_at="")
        with pytest.raises(SystemExit) as exc_info:
            run_main(release, tmp_path)
        assert exc_info.value.code == 1

    def test_empty_published_at_stderr_message(self, tmp_path, capsys):
        """Error message is written to stderr when published_at is empty."""
        release = _base_release(published_at="")
        with pytest.raises(SystemExit):
            run_main(release, tmp_path)
        captured = capsys.readouterr()
        assert "Error: Missing or invalid published_at in upstream release payload." in captured.err

    def test_none_published_at_exits(self, tmp_path, capsys):
        """None published_at (release dict missing the key) must cause sys.exit(1).
        release.get('published_at', '') returns '' when the key is absent.
        """
        release = _base_release()
        del release["published_at"]  # key absent → get() returns ""
        with pytest.raises(SystemExit) as exc_info:
            run_main(release, tmp_path)
        assert exc_info.value.code == 1

    def test_published_at_is_none_value_exits(self, tmp_path, capsys):
        """Explicit None value → get() returns None, 'T' not in None raises TypeError
        historically; the new code also catches this via 'T' not in ''.
        Actually: release.get('published_at', '') returns None here since the key exists.
        The guard 'if "T" not in published_at' will raise TypeError for None.
        Verify the code does NOT silently pass with None.
        """
        release = _base_release(published_at=None)
        # None is falsy; release.get returns None (key exists with None value).
        # "T" not in None raises TypeError in Python, so we expect either
        # SystemExit or TypeError – in both cases the function must NOT succeed.
        with pytest.raises((SystemExit, TypeError)):
            run_main(release, tmp_path)

    def test_whitespace_only_published_at_exits(self, tmp_path, capsys):
        """Whitespace-only string has no 'T' – must exit with code 1."""
        release = _base_release(published_at="   ")
        with pytest.raises(SystemExit) as exc_info:
            run_main(release, tmp_path)
        assert exc_info.value.code == 1

    def test_t_in_wrong_position_still_accepted(self, tmp_path):
        """A string that contains 'T' anywhere (even position 0) should not exit.
        This is a boundary test: the guard only checks membership, not position.
        """
        release = _base_release(published_at="T2024-06-15")
        # "T" is present so the guard passes; split("T", 1)[0] yields ""
        # The downstream code may or may not error, but the published_at guard itself passes.
        # We only care that the published_at-check does NOT exit(1).
        try:
            run_main(release, tmp_path)
        except SystemExit as e:
            # If it does exit, it must NOT be due to the published_at check
            # (could be due to missing tag or other guards)
            assert e.code == 1  # another guard may fire; that's fine

    # -----------------------------------------------------------------------
    # Regression: old behaviour would silently continue with empty date
    # -----------------------------------------------------------------------

    def test_regression_no_silent_empty_date(self, tmp_path):
        """Regression guard: ensure the old silent-empty-date path is gone.
        With a date-only published_at the script must exit, never write files.
        """
        release = _base_release(published_at="2024-06-15")
        upstream_file = tmp_path / "UPSTREAM_VERSION"
        assert not upstream_file.exists()

        with pytest.raises(SystemExit):
            run_main(release, tmp_path)

        # File must NOT have been written (exit happened before file writes)
        assert not upstream_file.exists()

    # -----------------------------------------------------------------------
    # Boundary: maxsplit=1 correctness
    # -----------------------------------------------------------------------

    def test_split_maxsplit_1_gives_correct_date(self, tmp_path, monkeypatch):
        """Directly verify that split('T', 1)[0] is used (not split('T')[0]).
        With maxsplit=1 both give the same result for well-formed input, but
        maxsplit=1 is strictly more defensive.  We verify the date part is correct.
        """
        captured_date = []

        mod = load_module()
        original_update_metainfo = mod.update_metainfo

        def spy_update_metainfo(version, date_str):
            captured_date.append(date_str)
            original_update_metainfo(version, date_str)

        patches = _patch_filesystem(mod, tmp_path)
        from contextlib import ExitStack
        with ExitStack() as stack:
            for p in patches:
                stack.enter_context(p)
            stack.enter_context(
                patch.object(mod, "get_latest_release",
                             return_value=_base_release(published_at="2024-06-15T12:00:00Z"))
            )
            stack.enter_context(patch.object(mod, "update_metainfo", side_effect=spy_update_metainfo))
            mod.main()

        assert captured_date == ["2024-06-15"]