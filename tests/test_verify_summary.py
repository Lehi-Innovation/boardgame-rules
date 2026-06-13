"""Tests for scripts.verify_summary (verifier logic mocked, no API calls)."""

import json
import os

import pytest
import yaml

import scripts.verify_summary as vs

SAMPLE_RULES = """---
title: "Test Game"
bgg_id: 42
---

# Test Game

## Overview

A test game where the minimum bid is 1 coin.
"""

REPAIRED_RULES = SAMPLE_RULES.replace("1 coin", "8 coins")


def test_parse_verifier_response_plain():
    raw = json.dumps({"verdict": "PASS", "reason": "", "findings": []})
    assert vs.parse_verifier_response(raw)["verdict"] == "PASS"


def test_parse_verifier_response_fenced_with_prose():
    raw = 'Here is my audit:\n```json\n{"verdict": "MINOR", "reason": "x", "findings": []}\n```'
    result = vs.parse_verifier_response(raw)
    assert result["verdict"] == "MINOR"
    assert result["findings"] == []


def test_parse_verifier_response_rejects_garbage():
    with pytest.raises(ValueError):
        vs.parse_verifier_response("I could not audit this game.")
    with pytest.raises(ValueError):
        vs.parse_verifier_response('{"verdict": "MAYBE"}')


@pytest.fixture
def pipeline_env(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "rules").mkdir()
    (tmp_path / "extracted").mkdir()
    (tmp_path / "rules" / "test-game.md").write_text(SAMPLE_RULES)
    (tmp_path / "extracted" / "test-game-rules.txt").write_text(
        "The opening bid must be 8 coins or more. " * 50
    )
    registry = tmp_path / "games.yaml"
    registry.write_text(yaml.dump({"games": [
        {"name": "Test Game", "bgg_id": 42, "status": "verifying"},
    ]}))
    return tmp_path, str(registry)


def _registry_entry(registry_path):
    return yaml.safe_load(open(registry_path))["games"][0]


def test_verify_game_pass(pipeline_env, monkeypatch):
    tmp_path, registry = pipeline_env
    monkeypatch.setattr(vs, "verify_text", lambda s, src: {
        "verdict": "PASS", "reason": "", "findings": []})
    game = {"name": "Test Game", "bgg_id": 42}
    assert vs.verify_game(game, registry) is True
    entry = _registry_entry(registry)
    assert entry["status"] == "verified"
    assert entry["verified_date"]
    content = (tmp_path / "rules" / "test-game.md").read_text()
    assert 'verification: "verified"' in content


def test_verify_game_repair_then_pass(pipeline_env, monkeypatch):
    tmp_path, registry = pipeline_env
    verdicts = iter([
        {"verdict": "MAJOR", "reason": "bid wrong", "findings": [
            {"severity": "major", "summary_quote": "minimum bid is 1 coin",
             "source_evidence": "opening bid must be 8 coins or more",
             "fix": "minimum bid is 8 coins"}]},
        {"verdict": "PASS", "reason": "", "findings": []},
    ])
    monkeypatch.setattr(vs, "verify_text", lambda s, src: next(verdicts))
    monkeypatch.setattr(vs, "repair_text", lambda s, src, f: REPAIRED_RULES)

    game = {"name": "Test Game", "bgg_id": 42}
    assert vs.verify_game(game, registry) is True
    content = (tmp_path / "rules" / "test-game.md").read_text()
    assert "8 coins" in content and "1 coin" not in content
    assert _registry_entry(registry)["status"] == "verified"


def test_verify_game_keeps_best_version_on_oscillation(pipeline_env, monkeypatch):
    """MAJOR -> MINOR -> MAJOR must end MINOR/verified with the round-1 content,
    not flagged with the drifted final round (the live battlecars/die-dracheninsel
    case: a good repair followed by verifier severity drift)."""
    tmp_path, registry = pipeline_env
    r1 = SAMPLE_RULES.replace("# Test Game", "# Test Game\n\n<!-- round1 -->")
    r2 = SAMPLE_RULES.replace("# Test Game", "# Test Game\n\n<!-- round2 -->")
    verdicts = iter([
        {"verdict": "MAJOR", "reason": "v0", "findings": [{"x": 1}]},
        {"verdict": "MINOR", "reason": "small gap", "findings": [{"x": 1}]},
        {"verdict": "MAJOR", "reason": "drift", "findings": [{"x": 1}]},
    ])
    repairs = iter([r1, r2])
    monkeypatch.setattr(vs, "verify_text", lambda s, src: next(verdicts))
    monkeypatch.setattr(vs, "repair_text", lambda s, src, f: next(repairs))

    game = {"name": "Test Game", "bgg_id": 42}
    assert vs.verify_game(game, registry, max_repair_rounds=2) is True
    content = (tmp_path / "rules" / "test-game.md").read_text()
    assert "<!-- round1 -->" in content  # best (MINOR) round kept
    assert "<!-- round2 -->" not in content  # drifted final round discarded
    assert _registry_entry(registry)["status"] == "verified"
    assert 'verification: "minor_issues"' in content


def test_verify_game_major_keeps_original_content(pipeline_env, monkeypatch):
    """When no repair beats the original, the original content is preserved
    (never left holding a failed rewrite) and the game is flagged."""
    tmp_path, registry = pipeline_env
    monkeypatch.setattr(vs, "verify_text", lambda s, src: {
        "verdict": "MAJOR", "reason": "unfixable", "findings": [{"x": 1}]})
    monkeypatch.setattr(vs, "repair_text", lambda s, src, f: REPAIRED_RULES)
    game = {"name": "Test Game", "bgg_id": 42}
    assert vs.verify_game(game, registry, max_repair_rounds=2) is False
    content = (tmp_path / "rules" / "test-game.md").read_text()
    assert "1 coin" in content and "8 coins" not in content  # original, not repaired
    assert _registry_entry(registry)["status"] == "flagged"


def test_verify_game_major_flags(pipeline_env, monkeypatch):
    tmp_path, registry = pipeline_env
    monkeypatch.setattr(vs, "verify_text", lambda s, src: {
        "verdict": "MAJOR", "reason": "unfixable", "findings": [
            {"severity": "major", "summary_quote": "x", "source_evidence": "y", "fix": "z"}]})
    monkeypatch.setattr(vs, "repair_text", lambda s, src, f: REPAIRED_RULES)

    game = {"name": "Test Game", "bgg_id": 42}
    assert vs.verify_game(game, registry, max_repair_rounds=1) is False
    entry = _registry_entry(registry)
    assert entry["status"] == "flagged"
    assert "unfixable" in entry["review_notes"]
    content = (tmp_path / "rules" / "test-game.md").read_text()
    assert 'verification: "inaccurate"' in content


def test_verify_game_no_source_flags_unverifiable(pipeline_env, monkeypatch):
    tmp_path, registry = pipeline_env
    os.remove(tmp_path / "extracted" / "test-game-rules.txt")
    game = {"name": "Test Game", "bgg_id": 42}
    assert vs.verify_game(game, registry) is False
    entry = _registry_entry(registry)
    assert entry["status"] == "flagged"
    assert "Unverifiable" in entry["review_notes"]


def test_verify_game_api_error_restores_status(pipeline_env, monkeypatch):
    tmp_path, registry = pipeline_env

    def boom(s, src):
        raise RuntimeError("API down")

    monkeypatch.setattr(vs, "verify_text", boom)
    game = {"name": "Test Game", "bgg_id": 42}
    assert vs.verify_game(game, registry, restore_status="validated") is False
    assert _registry_entry(registry)["status"] == "validated"
