"""Regenerate selected completed-game catalog entries while preserving other work."""
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import argparse
import hashlib
import json
import os
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[5]))

from scripts.generate_index import generate
from scripts.generate_manifest import build_manifest

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("slugs", nargs="+")
args = parser.parse_args()
selected = set(args.slugs)
base = Path(__file__).parent
batch = json.loads((base / "manifest.json").read_text())
assignments = {game["slug"]: game for game in batch["games"]}
approvals = json.loads((base / "coordinator-approvals.json").read_text())
canonical_hashes = {}
for slug in selected:
    game = assignments[slug]
    assert game.get('coordinator_pending_scope_choice', {}).get('status') != 'awaiting-human-clarification', 'Resolve the pending human source-scope choice before publication'
    assert game["status"] in ("ready-for-publication", "complete", "awaiting-stamp-retest"), f"{slug}: coordinator evidence approval required"
    assert approvals[slug]['approved'] and not game.get('coordinator_pending_source_audit')
    assert game.get('coordinator_source_gap', {}).get('status') != 'open'
    stamp = game['publication']['stamp']
    assert approvals[slug]['summary_sha256'] == stamp['before_sha256']
    canonical_hashes[slug] = hashlib.sha256(Path(game['summary_path']).read_bytes()).hexdigest()
    assert canonical_hashes[slug] == stamp['after_sha256']

index_path = Path("index.md")
manifest_path = Path("games.json")
original_index = index_path.read_text()
original_json_bytes = manifest_path.read_bytes()
original_json = json.loads(original_json_bytes)
regenerated_index = generate(Path("rules"), index_path)
regenerated_json = build_manifest(Path("rules"))
output = base / "publication" / datetime.now(ZoneInfo("America/Phoenix")).strftime("%Y%m%d-%H%M%S")
output.mkdir(parents=True, exist_ok=False)
(output / "before-index.md").write_text(original_index)
(output / "before-games.json").write_bytes(original_json_bytes)
(output / "regenerated-index.md").write_text(regenerated_index)
(output / "regenerated-games.json").write_text(json.dumps(regenerated_json, indent=1, ensure_ascii=False) + "\n")

def row_slug(line):
    match = re.search(r"\]\(rules/([^/]+)/\)", line)
    return match[1] if match else None

generated_lines = regenerated_index.splitlines(keepends=True)
lines = original_index.splitlines(keepends=True)
for slug in args.slugs:
    row = next(line for line in generated_lines if row_slug(line) == slug)
    matches = [i for i, line in enumerate(lines) if row_slug(line) == slug]
    assert len(matches) <= 1, f"Duplicate existing row: {slug}"
    if matches:
        lines[matches[0]] = row
        continue
    generated_position = generated_lines.index(row)
    predecessors = [row_slug(line) for line in generated_lines[:generated_position] if row_slug(line)]
    existing_positions = {row_slug(line): i for i, line in enumerate(lines) if row_slug(line)}
    predecessor = next((candidate for candidate in reversed(predecessors) if candidate in existing_positions), None)
    assert predecessor is not None, f"Cannot safely place new row: {slug}"
    lines.insert(existing_positions[predecessor] + 1, row)
updated_index = "".join(lines)
assert "".join(line for line in lines if row_slug(line) not in selected) == "".join(line for line in original_index.splitlines(keepends=True) if row_slug(line) not in selected)

old_entries = {game["slug"]: game for game in original_json["games"]}
new_entries = {game["slug"]: game for game in regenerated_json["games"]}
merged = dict(old_entries)
for slug in selected:
    merged[slug] = new_entries[slug]
updated_json = dict(original_json)
updated_json["games"] = sorted(merged.values(), key=lambda game: game["slug"])
updated_json["count"] = len(merged)
updated_json["generated"] = datetime.now(ZoneInfo("America/Phoenix")).date().isoformat()
assert all(merged[slug] == entry for slug, entry in old_entries.items() if slug not in selected)
assert index_path.read_text() == original_index, "Index changed concurrently; regenerate from latest"
assert manifest_path.read_bytes() == original_json_bytes, "Manifest changed concurrently; regenerate from latest"
assert all(hashlib.sha256(Path(assignments[slug]['summary_path']).read_bytes()).hexdigest() == value for slug, value in canonical_hashes.items()), "Selected summary changed concurrently; recheck evidence before publication"

index_temp = output / "targeted-index.md"
json_temp = output / "targeted-games.json"
index_temp.write_text(updated_index)
json_temp.write_text(json.dumps(updated_json, indent=1, ensure_ascii=False) + "\n")
index_staging = index_path.with_suffix(".md.summary-qa-tmp")
json_staging = manifest_path.with_suffix(".json.summary-qa-tmp")
index_staging.write_text(updated_index)
json_staging.write_bytes(json_temp.read_bytes())
os.replace(index_staging, index_path)
os.replace(json_staging, manifest_path)
report = {
    "slugs": args.slugs,
    "non_selected_index_lines_preserved": True,
    "non_selected_manifest_entries_preserved": True,
    "selected_manifest_entries_match_regeneration": all(merged[slug] == new_entries[slug] for slug in selected),
    "selected_index_rows_match_regeneration": all(next(line for line in lines if row_slug(line) == slug) == next(line for line in generated_lines if row_slug(line) == slug) for slug in selected),
    "artifacts": str(output.resolve()),
}
(output / "validation.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
