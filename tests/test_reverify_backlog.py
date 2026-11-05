"""Tests for scripts.reverify_backlog candidate selection (the pure part)."""

import os

from scripts.reverify_backlog import FATAL_ERROR_MARKERS, select_candidates


def test_credit_error_is_recognized_as_fatal():
    """The exact message that truncated the live run must be classified fatal."""
    msg = (
        "Error code: 400 - {'type': 'error', 'error': {'type': "
        "'invalid_request_error', 'message': 'Your credit balance is too low "
        "to access the Anthropic API.'}}"
    )
    assert any(s in msg.lower() for s in FATAL_ERROR_MARKERS)


def test_transient_error_is_not_fatal():
    msg = "Error code: 529 - overloaded_error: the service is temporarily overloaded"
    assert not any(s in msg.lower() for s in FATAL_ERROR_MARKERS)


def _make(tmp_path, slug, with_rules=True, with_source=True):
    if with_rules:
        (tmp_path / "rules").mkdir(exist_ok=True)
        (tmp_path / "rules" / f"{slug}.md").write_text("---\ntitle: x\n---\n# x")
    if with_source:
        (tmp_path / "extracted").mkdir(exist_ok=True)
        (tmp_path / "extracted" / f"{slug}-rules.txt").write_text("rulebook")


def test_select_candidates_filters(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    games = [
        {"name": "Major Game", "status": "flagged"},        # qualifies
        {"name": "Minor Game", "status": "flagged"},        # MINOR verdict -> no
        {"name": "Verified Game", "status": "verified"},    # not flagged -> no
        {"name": "No Source", "status": "flagged"},         # MAJOR but no source -> no
        {"name": "No Rules", "status": "flagged"},          # MAJOR but no rules file -> no
        {"name": "Other Flag", "status": "flagged"},        # no verdict at all -> no
    ]
    results = {
        "major-game": {"verdict": "MAJOR"},
        "minor-game": {"verdict": "MINOR"},
        "verified-game": {"verdict": "MAJOR"},
        "no-source": {"verdict": "MAJOR"},
        "no-rules": {"verdict": "MAJOR"},
    }
    _make(tmp_path, "major-game")
    _make(tmp_path, "minor-game")
    _make(tmp_path, "verified-game")
    _make(tmp_path, "no-source", with_source=False)
    _make(tmp_path, "no-rules", with_rules=False)
    _make(tmp_path, "other-flag")

    cands = select_candidates(games, results)
    assert cands == [("Major Game", "major-game")]


def test_select_candidates_sorted_by_slug(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    games = [
        {"name": "Zeta", "status": "flagged"},
        {"name": "Alpha", "status": "flagged"},
    ]
    results = {"zeta": {"verdict": "MAJOR"}, "alpha": {"verdict": "MAJOR"}}
    _make(tmp_path, "zeta")
    _make(tmp_path, "alpha")
    cands = select_candidates(games, results)
    assert [c[1] for c in cands] == ["alpha", "zeta"]
