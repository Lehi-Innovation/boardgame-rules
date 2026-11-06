"""Tests for scripts.stamp_verification."""

import os

import pytest
import yaml

from scripts.stamp_verification import (
    VERIFICATION_BEGIN,
    VERIFICATION_END,
    compute_state,
    has_extracted_source,
    build_block,
    promote_registry,
    stamp_file,
)

SAMPLE = """---
title: "Test Game"
bgg_id: 42
---

# Test Game

## Overview

A test game.
"""


def test_original_language_pdf_link_is_visible():
    block = build_block("example", "Example", "unverified", "", source_url="http://archive.test/download.php?id=12",
                        source_language="German")
    assert "Source PDF (German)" in block
    assert "http://archive.test/download.php?id=12" in block


def test_transcription_is_not_labelled_as_original_rulebook():
    block = build_block("example", "Example", "unverified", "", source_url="https://rules.test/example",
                        source_type="third_party_rules_transcription")
    assert "Rules source text" in block
    assert "Rules transcription (English)" in block
    assert "Full rulebook text" not in block


@pytest.mark.parametrize("source_type,label", [
    ("research_paper", "Research paper"),
    ("author_rules_html", "Author's rules"),
    ("author_rules_text", "Author's rules"),
    ("rules_reference_html", "Rules reference"),
    ("rules_reference_text", "Rules reference"),
    ("rules_reference_pdf", "Rules reference PDF"),
    ("rules_reference_images", "Rules reference images"),
    ("rulebook_images", "Rulebook images"),
    ("rulebook_archive", "Rulebook archive"),
])
@pytest.mark.parametrize("state", ["unverified", "inaccurate"])
def test_rules_references_have_accurate_source_labels(source_type, label, state):
    block = build_block("example", "Example", state, "Source-backed conflict.",
                        source_url="https://source.test/rules", source_type=source_type)
    assert f"{label} (English)" in block
    assert "full rulebook text" not in block.lower()
    assert "Source PDF" not in block
    assert "Source-backed conflict.." not in block


@pytest.fixture
def game_env(tmp_path, monkeypatch):
    """A rules file with a matching extracted source, cwd-independent."""
    rules = tmp_path / "rules"
    extracted = tmp_path / "extracted"
    rules.mkdir()
    extracted.mkdir()
    path = rules / "test-game.md"
    path.write_text(SAMPLE)
    (extracted / "test-game-rules.txt").write_text("source text " * 100)
    return path, str(extracted)


def test_compute_state_verdicts(game_env):
    _, extracted = game_env
    results = {"test-game": {"verdict": "PASS", "reason": ""}}
    assert compute_state("test-game", results, extracted)[0] == "verified"
    results["test-game"]["verdict"] = "MINOR"
    assert compute_state("test-game", results, extracted)[0] == "minor_issues"
    results["test-game"]["verdict"] = "MAJOR"
    results["test-game"]["reason"] = "wrong bid"
    assert compute_state("test-game", results, extracted) == ("inaccurate", "wrong bid")


def test_compute_state_no_audit(game_env):
    _, extracted = game_env
    assert compute_state("test-game", {}, extracted)[0] == "unverified"
    assert compute_state("missing-game", {}, extracted)[0] == "unverifiable"


@pytest.mark.parametrize("source_text", [None, "", " \n\t\f"])
@pytest.mark.parametrize("verdict", ["PASS", "MINOR", "MAJOR"])
def test_unusable_source_overrides_historical_verdict(game_env, source_text, verdict):
    path, extracted = game_env
    source = os.path.join(extracted, "test-game-rules.txt")
    if source_text is None:
        os.remove(source)
    else:
        with open(source, "w") as handle:
            handle.write(source_text)
    results = {"test-game": {"verdict": verdict, "reason": "old audit"}}
    assert compute_state("test-game", results, extracted) == ("unverifiable", "")
    stamp_file(str(path), results, extracted_dir=extracted)
    assert "Full rulebook text" not in path.read_text()
    assert "**Unverifiable**" in path.read_text()


def test_empty_canonical_source_allows_nonempty_legacy_source(game_env):
    _, extracted = game_env
    with open(os.path.join(extracted, "test-game-rules.txt"), "w") as handle:
        handle.write("")
    with open(os.path.join(extracted, "test-game_rules.txt"), "w") as handle:
        handle.write("A readable rulebook.")
    assert has_extracted_source("test-game", extracted)


def test_stamp_file_adds_frontmatter_and_block(game_env):
    path, extracted = game_env
    state = stamp_file(str(path), {}, extracted_dir=extracted, stamp_date="2026-06-12")
    assert state == "unverified"
    content = path.read_text()
    assert 'verification: "unverified"' in content
    assert 'verification_date: "2026-06-12"' in content
    assert VERIFICATION_BEGIN in content and VERIFICATION_END in content
    # block sits after the H1
    assert content.index("# Test Game") < content.index(VERIFICATION_BEGIN)
    assert "Report a rules error" in content
    assert "Full rulebook text" in content
    # frontmatter still parses and keeps original fields
    fm = yaml.safe_load(content.split("---")[1])
    assert fm["title"] == "Test Game" and fm["bgg_id"] == 42


def test_stamp_file_idempotent(game_env):
    path, extracted = game_env
    stamp_file(str(path), {}, extracted_dir=extracted, stamp_date="2026-06-12")
    first = path.read_text()
    stamp_file(str(path), {}, extracted_dir=extracted, stamp_date="2026-12-31")
    assert path.read_text() == first  # unchanged state -> no churn, date kept


def test_stamp_file_state_transition(game_env):
    path, extracted = game_env
    stamp_file(str(path), {}, extracted_dir=extracted, stamp_date="2026-06-12")
    results = {"test-game": {"verdict": "MAJOR", "reason": "minimum bid 1 vs 8"}}
    state = stamp_file(str(path), results, extracted_dir=extracted, stamp_date="2026-07-01")
    assert state == "inaccurate"
    content = path.read_text()
    assert 'verification: "inaccurate"' in content
    assert 'verification_date: "2026-07-01"' in content
    assert "minimum bid 1 vs 8" in content
    assert content.count(VERIFICATION_BEGIN) == 1  # replaced, not duplicated


def test_stamp_file_unverifiable_has_no_rulebook_link(tmp_path):
    rules = tmp_path / "rules"
    rules.mkdir()
    path = rules / "orphan.md"
    path.write_text(SAMPLE)
    state = stamp_file(str(path), {}, extracted_dir=str(tmp_path / "extracted"))
    assert state == "unverifiable"
    content = path.read_text()
    assert "Full rulebook text" not in content
    assert "Report a rules error" in content


def test_promote_registry(tmp_path):
    registry = tmp_path / "games.yaml"
    registry.write_text(yaml.dump({"games": [
        {"name": "Test Game", "bgg_id": 1, "status": "validated"},
        {"name": "Minor Game", "bgg_id": 2, "status": "validated"},
        {"name": "Other Game", "bgg_id": 3, "status": "summarized"},
    ]}))
    results = {
        "test-game": {"verdict": "PASS"},
        "minor-game": {"verdict": "MINOR"},
        "other-game": {"verdict": "PASS"},
    }
    promoted = promote_registry(str(registry), results)
    assert promoted == 1
    games = {g["name"]: g["status"] for g in yaml.safe_load(registry.read_text())["games"]}
    assert games["Test Game"] == "verified"
    assert games["Minor Game"] == "validated"  # MINOR not auto-promoted
    assert games["Other Game"] == "summarized"  # PASS but not yet validated
    os.remove(str(registry) + ".lock")
