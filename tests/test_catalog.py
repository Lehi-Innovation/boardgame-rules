from pathlib import Path

import pytest
import yaml

from scripts.catalog import validate_catalog
from tests.test_quality_check import GOOD_RULES


@pytest.fixture
def catalog(tmp_path):
    (tmp_path / "rules").mkdir()
    (tmp_path / "extracted").mkdir()
    (tmp_path / "rules/qe.md").write_text(GOOD_RULES.replace(
        'title: "QE"', 'title: "QE"\npermalink: /rules/qe/\nsource_pdf: qe-rules.pdf'
    ))
    (tmp_path / "extracted/qe-rules.txt").write_text("Auctions and company rules. " * 100)
    (tmp_path / "games.yaml").write_text(yaml.safe_dump({"games": [{
        "name": "QE", "bgg_id": 266830, "status": "validated",
        "player_count": "3-5", "play_time": "45 min", "designer": "Gavin Birnbaum",
    }]}))
    (tmp_path / "index.md").write_text(
        "| Game | Players | Time | Designer |\n|---|---|---|---|\n"
        "| [QE](rules/qe/) | 3-5 | 45 min | Gavin Birnbaum |\n"
    )
    return tmp_path


def test_consistent_catalog(catalog):
    assert validate_catalog(catalog) == []


def test_missing_validated_summary_and_broken_link(catalog):
    (catalog / "rules/qe.md").unlink()
    errors = validate_catalog(catalog)
    assert any("validated but rules file is missing" in error for error in errors)
    assert any("Catalog links to missing" in error for error in errors)


def test_wrong_metadata_and_missing_permalink(catalog):
    path = catalog / "rules/qe.md"
    path.write_text(path.read_text().replace("permalink: /rules/qe/\n", "").replace("45 min", "90 min"))
    errors = validate_catalog(catalog)
    assert any("permalink" in error for error in errors)
    assert any("play_time differs from registry" in error for error in errors)
    assert any("Catalog metadata differs" in error for error in errors)


def test_stale_status_and_missing_extraction(catalog):
    path = catalog / "games.yaml"
    path.write_text(path.read_text().replace("validated", "extracted"))
    (catalog / "extracted/qe-rules.txt").unlink()
    errors = validate_catalog(catalog)
    assert any("stale status extracted" in error for error in errors)
    assert any("missing extraction" in error for error in errors)


def test_duplicate_ids_and_catalog_entries(catalog):
    path = catalog / "games.yaml"
    data = yaml.safe_load(path.read_text())
    data["games"].append(data["games"][0].copy())
    path.write_text(yaml.safe_dump(data))
    index = catalog / "index.md"
    index.write_text(index.read_text() * 2)
    errors = validate_catalog(catalog)
    assert any("Duplicate registry BGG ID" in error for error in errors)
    assert any("Duplicate catalog link" in error for error in errors)


def test_validated_status_requires_passing_quality(catalog):
    (catalog / "extracted/qe-rules.txt").write_text("Incomplete extraction.")
    assert any("Extracted text too small" in error for error in validate_catalog(catalog))


def test_wrong_catalog_title(catalog):
    path = catalog / "index.md"
    path.write_text(path.read_text().replace("[QE]", "[Catan]"))
    assert any("Catalog title differs" in error for error in validate_catalog(catalog))


def test_orphan_summary_and_unlisted_summary(catalog):
    (catalog / "index.md").write_text("No games listed.\n")
    assert any("Summary missing from catalog" in error for error in validate_catalog(catalog))
    (catalog / "games.yaml").write_text("games: []\n")
    assert any("absent from registry" in error for error in validate_catalog(catalog))


def test_repository_catalog_is_consistent():
    assert validate_catalog(Path(__file__).resolve().parents[1]) == []
