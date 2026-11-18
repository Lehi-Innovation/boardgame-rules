"""Paths for rule summaries grouped by the first character of the title."""

from pathlib import Path


def title_folder(title: str) -> str:
    first = title.strip()[0].upper()
    return first if "A" <= first <= "Z" else "0-9"


def rule_path(rules_dir: str | Path, slug: str, title: str | None = None) -> Path:
    """Find an existing summary, or choose its folder when creating it."""
    root = Path(rules_dir)
    if title:
        path = root / title_folder(title) / f"{slug}.md"
        if path.exists():
            return path
    matches = list(root.glob(f"*/{slug}.md"))
    if len(matches) > 1:
        raise ValueError(f"Multiple rules summaries for {slug}")
    if matches:
        return matches[0]
    legacy = root / f"{slug}.md"
    if legacy.exists() or not title:
        return legacy
    return root / title_folder(title) / f"{slug}.md"
