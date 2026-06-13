#!/usr/bin/env python3
"""Generate games.json — a machine-readable manifest of the published catalog.

Built from rules/*.md frontmatter (the same source as the index), so an LLM
or app can resolve a game name to exact URLs without guessing slugs:

    {
      "generated": "2026-06-12",
      "site": "https://jonnyallred.github.io/boardgame-rules",
      "games": [
        {
          "title": "Catan",
          "slug": "catan",
          "bgg_id": 13,
          "player_count": "3-4",
          "play_time": "60-120 min",
          "verification": "verified",
          "summary_url": ".../rules/catan/",
          "rulebook_text_url": ".../extracted/catan-rules.txt"  # when available
        },
        ...
      ]
    }

Usage:
    python -m scripts.generate_manifest
    python -m scripts.generate_manifest --output games.json
"""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

from scripts.generate_index import load_games
from scripts.site import extracted_text_url, rules_page_url, site_base_url
from scripts.stamp_verification import has_extracted_source


def build_manifest(rules_dir: Path, extracted_dir: str = "extracted") -> dict:
    base = site_base_url()
    entries = []
    for game in load_games(rules_dir):
        slug = game["slug"]
        entry = {
            "title": game["title"],
            "slug": slug,
            "bgg_id": game.get("bgg_id"),
            "player_count": game.get("player_count", ""),
            "play_time": game.get("play_time", ""),
            "verification": game.get("verification", "unverified"),
            "summary_url": rules_page_url(slug, base),
        }
        if game.get("base_game_bgg_id"):
            entry["base_game_bgg_id"] = game["base_game_bgg_id"]
        if has_extracted_source(slug, extracted_dir):
            entry["rulebook_text_url"] = extracted_text_url(slug, base)
        entries.append(entry)
    entries.sort(key=lambda e: e["slug"])
    return {
        "generated": date.today().isoformat(),
        "site": base,
        "count": len(entries),
        "games": entries,
    }


def main():
    parser = argparse.ArgumentParser(description="Generate games.json manifest")
    parser.add_argument("--rules-dir", default="rules")
    parser.add_argument("--extracted-dir", default="extracted")
    parser.add_argument("--output", default="games.json")
    args = parser.parse_args()

    manifest = build_manifest(Path(args.rules_dir), args.extracted_dir)
    with open(args.output, "w") as f:
        json.dump(manifest, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"Wrote {args.output}: {manifest['count']} games")


if __name__ == "__main__":
    main()
