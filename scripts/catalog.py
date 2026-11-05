"""Check that the published catalog and manifest match rules files.

Run ``python -m scripts.catalog`` to check published artifacts. Add
``--strict-registry`` to audit registry IDs, metadata, statuses, and sources
as well; this reports ingestion and verification backlog without changing it.
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re

import yaml

from scripts.quality_check import check_quality, slugify
from scripts.registry import load_registry
from scripts.validate import validate_rules_file


def validate_catalog(root: str | Path = ".", *, strict_registry: bool = False) -> list[str]:
    root = Path(root)
    games = load_registry(str(root / "games.yaml"))
    errors = []
    if strict_registry:
        for bgg_id, count in Counter(game["bgg_id"] for game in games).items():
            if count > 1:
                errors.append(f"Duplicate registry BGG ID: {bgg_id}")
    registry = {game["bgg_id"]: game for game in games}
    summaries = {}
    metadata_by_slug = {}
    config_path = root / "_config.yml"
    config = yaml.safe_load(config_path.read_text()) if config_path.exists() else {}
    base_url = str(config.get("url", "")).rstrip("/") + config.get("baseurl", "")

    for path in sorted((root / "rules").glob("*.md")):
        file_errors = validate_rules_file(str(path))
        errors.extend(file_errors)
        if file_errors:
            continue
        match = re.match(r"^---\n(.+?)\n---", path.read_text(), re.DOTALL)
        metadata = yaml.safe_load(match.group(1))
        bgg_id = metadata["bgg_id"]
        if strict_registry and bgg_id in summaries:
            errors.append(f"Duplicate summary BGG ID: {bgg_id}")
        summaries[bgg_id] = path
        metadata_by_slug[path.stem] = metadata
        permalink = metadata.get("permalink")
        if permalink is not None:
            if permalink != f"/rules/{path.stem}/":
                errors.append(f"{path.name}: incorrect directory permalink")
        elif config.get("permalink") != "pretty":
            errors.append(f"{path.name}: directory permalink requires explicit frontmatter or pretty site URLs")

        if not strict_registry:
            continue
        game = registry.get(bgg_id)
        if game is None:
            errors.append(f"{path.name}: BGG ID {bgg_id} is absent from registry")
            continue
        slug = game.get("slug") or slugify(game["name"])
        if path.stem != slug:
            errors.append(f"{path.name}: registry resolves to {slug}.md")
        if metadata["title"] != game["name"]:
            errors.append(f"{path.name}: title differs from registry name")
        for field in ("player_count", "play_time", "designer", "base_game_bgg_id"):
            if metadata.get(field) != game.get(field):
                errors.append(f"{path.name}: {field} differs from registry")
        base_id = metadata.get("base_game_bgg_id")
        if base_id is not None and (base_id == bgg_id or base_id not in registry):
            errors.append(f"{path.name}: invalid base_game_bgg_id {base_id}")
        if game["status"] not in ("summarized", "validated", "verified", "flagged"):
            errors.append(f"{path.name}: existing summary has stale status {game['status']}")
        source_pdf = metadata.get("source_pdf")
        candidates = [root / "extracted" / f"{path.stem}-rules.txt"]
        if isinstance(source_pdf, str) and source_pdf:
            candidates.append(root / "extracted" / (Path(source_pdf).stem + ".txt"))
        candidates.extend(root / "extracted" / name for name in (f"{path.stem}_rules.txt", f"{path.stem}.txt"))
        extraction = next((candidate for candidate in candidates if candidate.is_file()), None)
        if extraction is None:
            errors.append(f"{path.name}: missing extraction")
        elif game["status"] in ("validated", "verified"):
            errors.extend(f"{path.name}: {issue}" for issue in check_quality(str(path), str(extraction)).issues)

    if strict_registry:
        for game in games:
            if game["status"] in ("summarized", "validated", "verified") and game["bgg_id"] not in summaries:
                errors.append(f"{game['name']}: {game['status']} but rules file is missing")

    index = (root / "index.md").read_text()
    links = re.findall(r"\]\(rules/([^/]+)/\)", index)
    for slug, count in Counter(links).items():
        if count > 1:
            errors.append(f"Duplicate catalog link: {slug}")
    for slug in sorted(set(links) - set(metadata_by_slug)):
        errors.append(f"Catalog links to missing or invalid summary: {slug}")
    for slug in sorted(set(metadata_by_slug) - set(links)):
        errors.append(f"Summary missing from catalog: {slug}")
    for line in index.splitlines():
        match = re.search(r"\[([^\]]+)\]\(rules/([^/]+)/\)", line)
        if not match or match[2] not in metadata_by_slug:
            continue
        metadata = metadata_by_slug[match[2]]
        titles = {metadata["title"]}
        if metadata.get("base_game_bgg_id") is not None:
            titles.add(metadata["title"].split(": ", 1)[-1])
        if match[1] not in titles:
            errors.append(f"Catalog title differs from summary: {match[2]}")
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        expected = [str(metadata.get(field, "")) for field in ("player_count", "play_time", "designer")]
        if cells[1:4] != expected:
            errors.append(f"Catalog metadata differs from summary: {match[2]}")

    manifest_path = root / "games.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
        entries = manifest.get("games", [])
        manifest_slugs = [entry["slug"] for entry in entries]
        if len(manifest_slugs) != len(set(manifest_slugs)):
            errors.append("Duplicate manifest slugs")
        if set(manifest_slugs) != set(metadata_by_slug) or manifest.get("count") != len(metadata_by_slug):
            errors.append("Manifest game coverage differs from rules files")
        if manifest.get("site") != base_url:
            errors.append("Manifest site differs from Jekyll configuration")
        for entry in entries:
            slug = entry["slug"]
            if slug not in metadata_by_slug:
                continue
            metadata = metadata_by_slug[slug]
            for field in ("title", "bgg_id", "player_count", "play_time", "base_game_bgg_id"):
                if entry.get(field, "") != metadata.get(field, ""):
                    errors.append(f"Manifest {field} differs from summary: {slug}")
            if entry.get("verification", "unverified") != metadata.get("verification", "unverified"):
                errors.append(f"Manifest verification differs from summary: {slug}")
            if entry.get("summary_url") != f"{base_url}/rules/{slug}/":
                errors.append(f"Manifest summary URL differs from page path: {slug}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Project root (default: current directory)")
    parser.add_argument("--strict-registry", action="store_true", help="Also report registry and source backlog")
    args = parser.parse_args()
    errors = validate_catalog(args.root, strict_registry=args.strict_registry)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)
    count = len(list((Path(args.root) / "rules").glob("*.md")))
    print(f"Catalog consistent: {count} summaries; published links, metadata, manifest, and URL paths checked.")


if __name__ == "__main__":
    main()
