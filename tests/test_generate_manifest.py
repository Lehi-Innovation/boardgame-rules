"""Tests for scripts.generate_manifest."""

from pathlib import Path

from scripts.generate_manifest import build_manifest

SAMPLE = """---
title: "{title}"
bgg_id: {bgg_id}
player_count: "2-4"
play_time: "30 min"
verification: "{verification}"
---

# {title}
"""


def test_build_manifest(tmp_path):
    rules = tmp_path / "rules"
    extracted = tmp_path / "extracted"
    rules.mkdir()
    extracted.mkdir()
    (rules / "alpha.md").write_text(
        SAMPLE.format(title="Alpha", bgg_id=1, verification="verified"))
    (rules / "beta.md").write_text(
        SAMPLE.format(title="Beta", bgg_id=2, verification="unverifiable"))
    (extracted / "alpha-rules.txt").write_text("rulebook text")

    manifest = build_manifest(rules, str(extracted))

    assert manifest["count"] == 2
    by_slug = {g["slug"]: g for g in manifest["games"]}
    alpha, beta = by_slug["alpha"], by_slug["beta"]
    assert alpha["verification"] == "verified"
    assert alpha["summary_url"].endswith("/rules/alpha/")
    assert alpha["rulebook_text_url"].endswith("/extracted/alpha-rules.txt")
    assert "rulebook_text_url" not in beta  # no source on disk
    assert beta["verification"] == "unverifiable"
