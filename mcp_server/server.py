#!/usr/bin/env python3
"""MCP server exposing the boardgame rules corpus for mid-game Q&A.

Gives any MCP-capable client (Claude mobile/desktop, etc.) the same tiered
lookup the in-repo skills use: summary first, full extracted rulebook text
second, plus a feedback path back to the repo.

Tools:
    list_games(query)            — resolve a game name to slugs + metadata
    get_rules(game)              — the full rules summary + verification status
    search_rulebook(game, query) — keyword search over the extracted rulebook text
    report_rule_error(...)       — prefilled GitHub issue link for a bad rule

Run (stdio, from the repo root):
    pip install mcp
    python -m mcp_server.server

Claude Desktop config (claude_desktop_config.json):
    {"mcpServers": {"boardgame-rules": {
        "command": "python", "args": ["-m", "mcp_server.server"],
        "cwd": "/path/to/boardgame-rules"}}}
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from mcp.server.fastmcp import FastMCP

REPO_ROOT = Path(__file__).resolve().parent.parent
RULES_DIR = REPO_ROOT / "rules"
EXTRACTED_DIR = REPO_ROOT / "extracted"
MANIFEST_PATH = REPO_ROOT / "games.json"

mcp = FastMCP("boardgame-rules")


def _slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def _load_manifest() -> list[dict]:
    if MANIFEST_PATH.exists():
        return json.loads(MANIFEST_PATH.read_text())["games"]
    # Fallback: build a minimal catalog from the rules directory
    return [
        {"title": p.stem.replace("-", " ").title(), "slug": p.stem}
        for p in sorted(RULES_DIR.glob("*.md"))
    ]


def _resolve_slug(game: str) -> tuple[str | None, list[dict]]:
    """Resolve a user-supplied game name to a slug.

    Returns (slug, candidates). slug is None when no confident single match.
    """
    query_slug = _slugify(game)
    games = _load_manifest()
    exact = [g for g in games if g["slug"] == query_slug]
    if exact:
        return query_slug, exact
    partial = [
        g for g in games
        if query_slug in g["slug"] or query_slug.replace("-", "") in g["slug"].replace("-", "")
    ]
    if len(partial) == 1:
        return partial[0]["slug"], partial
    return None, partial[:10]


def _extracted_path(slug: str) -> Path | None:
    for pattern in (f"{slug}-rules.txt", f"{slug}_rules.txt", f"{slug}.txt"):
        path = EXTRACTED_DIR / pattern
        if path.exists():
            return path
    return None


@mcp.tool()
def list_games(query: str = "") -> str:
    """Search the catalog of available games. Returns matching games with their
    slug, player count, play time, and verification status. Call with an empty
    query to get the catalog size, or with a (partial) game name to resolve it."""
    games = _load_manifest()
    if query:
        q = _slugify(query)
        games = [g for g in games if q in g["slug"]]
    if not games:
        return f"No games matching {query!r}. Try a shorter or alternate name."
    lines = [f"{len(games)} game(s):"]
    for g in games[:50]:
        lines.append(
            f"- {g.get('title', g['slug'])} (slug: {g['slug']}, "
            f"players: {g.get('player_count', '?')}, "
            f"verification: {g.get('verification', 'unknown')})"
        )
    if len(games) > 50:
        lines.append(f"... and {len(games) - 50} more; refine the query.")
    return "\n".join(lines)


@mcp.tool()
def get_rules(game: str) -> str:
    """Get the full rules summary for a game (markdown, with a verification
    banner). Use this first for any rules question. If the summary does not
    answer the question, follow up with search_rulebook."""
    slug, candidates = _resolve_slug(game)
    if not slug:
        if candidates:
            names = ", ".join(g["slug"] for g in candidates)
            return f"Ambiguous game name {game!r}. Candidates: {names}"
        return f"No game matching {game!r} in the catalog. Use list_games to search."
    path = RULES_DIR / f"{slug}.md"
    if not path.exists():
        return f"Game {slug} is in the catalog but has no rules summary yet."
    return path.read_text()


@mcp.tool()
def search_rulebook(game: str, query: str, context_lines: int = 4) -> str:
    """Search the game's full extracted rulebook text (the authoritative source)
    for a keyword or phrase. Use when the summary doesn't answer the question,
    or to double-check a critical ruling — the rulebook text outranks the
    summary. Returns matching passages with surrounding context."""
    slug, candidates = _resolve_slug(game)
    if not slug:
        return f"No game matching {game!r}. Candidates: {[g['slug'] for g in candidates]}"
    path = _extracted_path(slug)
    if not path:
        return (
            f"No extracted rulebook text exists for {slug}; the summary is the only "
            "source available and cannot be double-checked."
        )
    lines = path.read_text(errors="replace").splitlines()
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    # Fall back to matching all words when the exact phrase misses (OCR text is messy)
    words = [re.escape(w) for w in query.split() if len(w) > 2]
    word_patterns = [re.compile(w, re.IGNORECASE) for w in words]

    def matches(line: str) -> bool:
        if pattern.search(line):
            return True
        return bool(word_patterns) and all(p.search(line) for p in word_patterns)

    hits = [i for i, line in enumerate(lines) if matches(line)]
    if not hits:
        return (
            f"No match for {query!r} in {slug}'s rulebook text "
            f"({len(lines)} lines). Try a different term — OCR text may use other wording."
        )
    blocks = []
    last_end = -1
    for i in hits[:8]:
        start = max(i - context_lines, last_end + 1, 0)
        end = min(i + context_lines + 1, len(lines))
        if start < end:
            blocks.append(f"[line {i + 1}]\n" + "\n".join(lines[start:end]))
            last_end = end - 1
    suffix = f"\n\n({len(hits)} total matches; showing first {min(len(hits), 8)})" if len(hits) > 8 else ""
    return "\n\n---\n\n".join(blocks) + suffix


@mcp.tool()
def report_rule_error(game: str, summary_claim: str, correction: str) -> str:
    """Report that the rules summary is wrong. Call this when the user says the
    summary contradicted the physical rulebook or an official ruling. Returns a
    link that files the report; the database is then fixed via an automated,
    source-verified pull request."""
    import sys

    sys.path.insert(0, str(REPO_ROOT))
    from scripts.site import report_issue_url

    slug, candidates = _resolve_slug(game)
    if not slug:
        return f"No game matching {game!r}. Candidates: {[g['slug'] for g in candidates]}"
    games = [g for g in _load_manifest() if g["slug"] == slug]
    title = games[0].get("title", slug) if games else slug
    url = report_issue_url(title, slug)
    return (
        f"Open this link to file the report (the form is prefilled):\n{url}\n\n"
        f"Include in the form:\n- What the summary says: {summary_claim}\n"
        f"- What the rule actually is: {correction}"
    )


if __name__ == "__main__":
    mcp.run()
