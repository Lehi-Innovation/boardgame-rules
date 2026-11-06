#!/usr/bin/env python3
"""Validate rules markdown files for completeness.

Usage:
    python -m scripts.validate
    python -m scripts.validate rules/catan.md
"""

import argparse
import os
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

import yaml

RULES_DIR = "rules"

REQUIRED_FRONTMATTER = ["title", "bgg_id"]


def _has_required_value(frontmatter: dict, field: str) -> bool:
    """Return True when a required frontmatter field is present and usable."""
    if field == "bgg_id" and frontmatter.get(field) is None:
        # A known wrong ID may be withdrawn while the matching named game has
        # no confirmed replacement. Require an explicit, traceable decision.
        original = frontmatter.get("original_bgg_id")
        evidence = frontmatter.get("identity_evidence_url", "")
        try:
            parsed = urlsplit(evidence) if isinstance(evidence, str) else None
        except ValueError:
            parsed = None
        return (field in frontmatter
                and frontmatter.get("bgg_id_status") == "unresolved"
                and type(original) is int and original > 0
                and parsed is not None and parsed.scheme in {"http", "https"}
                and bool(parsed.netloc))
    if field not in frontmatter:
        return False

    value = frontmatter[field]
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    return True

EXPECTED_SECTIONS = [
    "Overview",
    "Components",
    "Setup",
    "Turn Structure",
    "Actions",
    "Scoring / Victory Conditions",
    "Special Rules & Edge Cases",
    "Player Reference",
]

EXPANSION_SECTIONS = [
    "Overview",
    "New Components",
    "Setup Changes",
    "Rule Changes",
    "Special Rules & Edge Cases",
    "Player Reference",
]


class _FrontmatterLoader(yaml.SafeLoader):
    """Reject duplicate keys instead of silently accepting the last value."""

    def construct_mapping(self, node, deep=False):
        keys = set()
        for key_node, _ in node.value:
            key = self.construct_object(key_node, deep=deep)
            if not isinstance(key, str):
                raise yaml.constructor.ConstructorError(
                    None, None, "frontmatter keys must be strings", key_node.start_mark
                )
            if key in keys:
                raise yaml.constructor.ConstructorError(
                    None, None, f"duplicate frontmatter key: {key}", key_node.start_mark
                )
            keys.add(key)
        return super().construct_mapping(node, deep=deep)


def validate_rules_file(path: str) -> list[str]:
    """Validate a rules markdown file. Returns list of error messages."""
    errors = []
    content = Path(path).read_text()
    filename = os.path.basename(path)

    # Check frontmatter
    fm_match = re.match(r"^---\n(.+?)\n---", content, re.DOTALL)
    if not fm_match:
        errors.append(f"{filename}: No YAML frontmatter found")
        return errors

    try:
        frontmatter = yaml.load(fm_match.group(1), Loader=_FrontmatterLoader)
    except yaml.YAMLError as e:
        errors.append(f"{filename}: Invalid YAML frontmatter: {e}")
        return errors

    if not isinstance(frontmatter, dict):
        return [f"{filename}: YAML frontmatter must be a mapping"]

    # Check required fields
    for field in REQUIRED_FRONTMATTER:
        if not _has_required_value(frontmatter, field):
            errors.append(f"{filename}: Missing required frontmatter field: {field}")

    # Choose section list based on whether this is an expansion
    is_expansion = "base_game_bgg_id" in frontmatter
    sections = EXPANSION_SECTIONS if is_expansion else EXPECTED_SECTIONS

    # Check sections
    body = content[fm_match.end():]
    for section in sections:
        pattern = rf"^## {re.escape(section)}(?:[ \t].*)?$"
        if not re.search(pattern, body, re.MULTILINE):
            errors.append(f"{filename}: Missing section: {section}")

    return errors


def validate_all(rules_dir: str = RULES_DIR) -> dict[str, list[str]]:
    """Validate all .md files in the rules directory."""
    results = {}
    rules_path = Path(rules_dir)

    if not rules_path.exists():
        return {}

    for md_file in sorted(rules_path.glob("*.md")):
        errors = validate_rules_file(str(md_file))
        results[md_file.name] = errors

    return results


def main():
    parser = argparse.ArgumentParser(description="Validate rules markdown files")
    parser.add_argument("files", nargs="*", help="Specific files to validate (default: all in rules/)")
    parser.add_argument("--rules-dir", default=RULES_DIR, help="Rules directory")
    args = parser.parse_args()

    if args.files:
        all_errors = {}
        for f in args.files:
            all_errors[f] = validate_rules_file(f)
    else:
        all_errors = validate_all(args.rules_dir)

    if not all_errors:
        print("No rules files found.")
        sys.exit(0)

    has_errors = False
    for filename, errors in all_errors.items():
        if errors:
            has_errors = True
            print(f"\n{filename}:")
            for e in errors:
                print(f"  - {e}")
        else:
            print(f"{filename}: OK")

    if has_errors:
        sys.exit(1)
    else:
        print(f"\nAll {len(all_errors)} file(s) valid.")


if __name__ == "__main__":
    main()
