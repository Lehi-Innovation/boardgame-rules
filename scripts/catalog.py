"""Check the registry, available-games table, and rules files agree.

Run ``python -m scripts.catalog`` after adding or restoring rules. This is
read-only; it also checks saved extraction sources and published page URLs.
"""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
import re

import yaml

from scripts.quality_check import check_quality, slugify
from scripts.registry import load_registry
from scripts.validate import validate_rules_file


def validate_catalog(root: str | Path = ".") -> list[str]:
    root = Path(root)
    games = load_registry(str(root / "games.yaml"))
    errors = []
    ids = [game["bgg_id"] for game in games]
    for bgg_id, count in Counter(ids).items():
        if count > 1:
            errors.append(f"Duplicate registry BGG ID: {bgg_id}")
    registry = {game["bgg_id"]: game for game in games}
    summaries = {}
    expected_rows = {}
    expected_titles = {}

    for path in sorted((root / "rules").glob("*.md")):
        file_errors = validate_rules_file(str(path))
        errors.extend(file_errors)
        if file_errors:
            continue
        match = re.match(r"^---\n(.+?)\n---", path.read_text(), re.DOTALL)
        metadata = yaml.safe_load(match.group(1))
        bgg_id = metadata["bgg_id"]
        if bgg_id in summaries:
            errors.append(f"Duplicate summary BGG ID: {bgg_id}")
        summaries[bgg_id] = path
        game = registry.get(bgg_id)
        if game is None:
            errors.append(f"{path.name}: BGG ID {bgg_id} is absent from registry")
            continue
        slug = game.get("slug") or slugify(game["name"])
        if path.stem != slug:
            errors.append(f"{path.name}: registry resolves to {slug}.md")
        if metadata.get("permalink") != f"/rules/{path.stem}/":
            errors.append(f"{path.name}: missing or incorrect directory permalink")
        if metadata["title"] != game["name"]:
            errors.append(f"{path.name}: title differs from registry name")
        for field in ("player_count", "play_time", "designer", "base_game_bgg_id"):
            if metadata.get(field) != game.get(field):
                errors.append(f"{path.name}: {field} differs from registry")
        base_id = metadata.get("base_game_bgg_id")
        if base_id is not None and (base_id == bgg_id or base_id not in registry):
            errors.append(f"{path.name}: invalid base_game_bgg_id {base_id}")
        if game["status"] not in ("summarized", "validated", "flagged"):
            errors.append(f"{path.name}: existing summary has stale status {game['status']}")

        source_pdf = metadata.get("source_pdf")
        if not isinstance(source_pdf, str) or not source_pdf:
            errors.append(f"{path.name}: missing source_pdf")
        else:
            extraction = root / "extracted" / (Path(source_pdf).stem + ".txt")
            if not extraction.is_file():
                errors.append(f"{path.name}: missing extraction {extraction.name}")
            elif game["status"] == "validated":
                quality = check_quality(str(path), str(extraction))
                errors.extend(f"{path.name}: {issue}" for issue in quality.issues)

        expected_rows[path.stem] = [
            metadata.get(field, "") for field in ("player_count", "play_time", "designer")
        ]
        expected_titles[path.stem] = {metadata["title"]}
        if base_id is not None:
            expected_titles[path.stem].add(metadata["title"].split(": ", 1)[-1])

    for game in games:
        if game["status"] in ("summarized", "validated") and game["bgg_id"] not in summaries:
            errors.append(f"{game['name']}: {game['status']} but rules file is missing")

    index = (root / "index.md").read_text()
    links = re.findall(r"\]\(rules/([^/]+)/\)", index)
    for slug, count in Counter(links).items():
        if count > 1:
            errors.append(f"Duplicate catalog link: {slug}")
    for slug in sorted(set(links) - set(expected_rows)):
        errors.append(f"Catalog links to missing or invalid summary: {slug}")
    for slug in sorted(set(expected_rows) - set(links)):
        errors.append(f"Summary missing from catalog: {slug}")
    for line in index.splitlines():
        match = re.search(r"\]\(rules/([^/]+)/\)", line)
        if match and match[1] in expected_rows:
            title = re.search(r"\[([^\]]+)\]\(rules/", line)
            if title and title[1] not in expected_titles[match[1]]:
                errors.append(f"Catalog title differs from summary: {match[1]}")
            # The first cell is the title/link, followed by the three metadata cells.
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if cells[1:] != expected_rows[match[1]]:
                errors.append(f"Catalog metadata differs from summary: {match[1]}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Project root (default: current directory)")
    args = parser.parse_args()
    errors = validate_catalog(args.root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)
    count = len(list((Path(args.root) / "rules").glob("*.md")))
    print(f"Catalog consistent: {count} summaries; registry, links, metadata, sources, and permalinks checked.")


if __name__ == "__main__":
    main()
