"""Shared site/repo constants and URL helpers.

Reads the published site URL from _config.yml so scripts that emit links
(stamping, index, manifest, MCP server) stay consistent with the Jekyll config.
"""

from __future__ import annotations

import os
from urllib.parse import quote

import yaml

CONFIG_PATH = "_config.yml"
REPO_URL = "https://github.com/Lehi-Innovation/boardgame-rules"


def site_base_url(config_path: str = CONFIG_PATH) -> str:
    """Return the published site base URL (url + baseurl, no trailing slash)."""
    url = "https://jonnyallred.github.io"
    baseurl = "/boardgame-rules"
    if os.path.exists(config_path):
        with open(config_path) as f:
            cfg = yaml.safe_load(f) or {}
        url = (cfg.get("url") or url).rstrip("/")
        baseurl = cfg.get("baseurl") or baseurl
    return f"{url}{baseurl}".rstrip("/")


def rules_page_url(slug: str, base: str | None = None) -> str:
    """Published (Jekyll-rendered) page for a rules summary."""
    return f"{base or site_base_url()}/rules/{slug}/"


def extracted_text_url(slug: str, base: str | None = None) -> str:
    """Published raw extracted rulebook text."""
    return f"{base or site_base_url()}/extracted/{slug}-rules.txt"


def report_issue_url(title: str, slug: str) -> str:
    """Prefilled GitHub issue-form URL for reporting a rules error."""
    return (
        f"{REPO_URL}/issues/new"
        f"?template=rule-error.yml"
        f"&labels=rule-error"
        f"&title={quote(f'[Rule error] {title}')}"
        f"&game={quote(slug)}"
    )
