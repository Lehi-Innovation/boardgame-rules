#!/usr/bin/env python3
"""Rebuild index.md from all rules files.

Thin wrapper around scripts.generate_index (the canonical index generator,
which preserves the index.md preamble, nests expansions, and renders the
verification status column). Kept for backward compatibility with the bulk
research workflow documented in CLAUDE.md.

Usage:
    python -m scripts.rebuild_index
    python -m scripts.rebuild_index --rules-dir rules --index index.md
"""

from __future__ import annotations

import argparse
from pathlib import Path

from scripts.generate_index import generate


def main():
    parser = argparse.ArgumentParser(description="Rebuild index.md from rules files")
    parser.add_argument("--rules-dir", default="rules", help="Rules directory (default: rules)")
    parser.add_argument("--index", default="index.md", help="Output index file (default: index.md)")
    args = parser.parse_args()

    index_path = Path(args.index)
    content = generate(Path(args.rules_dir), index_path)
    index_path.write_text(content, encoding="utf-8")

    game_count = sum(
        1
        for line in content.splitlines()
        if line.startswith("| ") and "[" in line and "Game |" not in line
    )
    print(f"Rebuilt {args.index}: {game_count} games")


if __name__ == "__main__":
    main()
