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
