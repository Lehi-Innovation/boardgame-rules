"""Cache and search the public 1jour-1jeu rulebook index for recovery candidates.

This discovers links only. Every download still needs identity, language, and
completeness review before being accepted as a usable source.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from pathlib import Path
import re
import time
import unicodedata
from urllib.parse import unquote, urlparse, urljoin

from bs4 import BeautifulSoup
import requests

from scripts.recover_sources import ROOT, TRACKER


def normalize(value):
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode().lower()
    value = value.replace("_", " ")
    value = re.sub(r"\b(rulebook|rules|multilingual|multilingue|regle|regles)\b", "", value)
    value = re.sub(r"\b(en|eng|english|uk)\s*$", "", value.strip(" -"))
    return re.sub("[^a-z0-9]", "", value)


def parse_page(html):
    soup = BeautifulSoup(html, "html.parser")
    result = []
    for block in soup.select(".col-center"):
        heading = block.select_one("h3")
        if not heading:
            continue
        for link in block.select("a[title='In English'][href]"):
            if link["href"].lower().endswith(".pdf"):
                result.append({"title": heading.get_text(" ", strip=True), "url": link["href"]})
    return result


def discover_capital(workers=4):
    """Follow matched game pages to actual PDF links; never guess download URLs."""
    cache = Path("/tmp/source-recovery/capital-index")
    cache.mkdir(parents=True, exist_ok=True)
    targets = json.loads(TRACKER.read_text())["games"]
    by_title = {}
    for game in targets:
        for key in {normalize(game["title"]), normalize(game["slug"])}:
            by_title.setdefault(key, set()).add(game["slug"])
    matches, failures = {}, []

    def read(url):
        path = cache / (Path(urlparse(url).path).name or "index.html")
        if not path.exists():
            response = requests.get(url, timeout=35)
            response.raise_for_status()
            path.write_text(response.text)
            time.sleep(0.25)
        return BeautifulSoup(path.read_text(), "html.parser")

    pages = {}
    for name in ["board-game-rules.htm", "party-game-rules.htm", "dice-card-game-rules.htm", "childrens-game-rules.htm"]:
        url = "https://www.boardgamecapital.com/" + name
        try:
            soup = read(url)
            for link in soup.select("a[href]"):
                slugs = by_title.get(normalize(link.get_text(" ", strip=True)), set())
                href = urljoin(url, link["href"])
                if slugs and href.endswith("-rules.htm"):
                    pages.setdefault(href, set()).update(slugs)
        except Exception as error:
            failures.append({"url": url, "error": str(error)})
    print(f"Matched {len(pages)} game pages in four archive indexes", flush=True)

    def fetch_page(url):
        soup = read(url)
        return [{"title": link.get_text(" ", strip=True), "url": urljoin(url, link["href"]),
                 "discovery_page": url} for link in soup.select("a[href]")
                if urlparse(link["href"]).path.lower().endswith(".pdf")]

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(fetch_page, url): url for url in pages}
        for future in as_completed(futures):
            url = futures[future]
            try:
                found = future.result()
                if found:
                    for slug in pages[url]:
                        matches.setdefault(slug, []).extend(found)
            except Exception as error:
                failures.append({"url": url, "error": str(error)})
    output = {"archive": "https://www.boardgamecapital.com/", "failures": failures, "candidates": matches}
    (ROOT / "docs/quality/source-recovery/capital-candidates.json").write_text(
        json.dumps(output, indent=2, ensure_ascii=False) + "\n")
    print(f"{len(matches)} games with PDF candidates; {len(failures)} failures", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pages", type=int, default=394)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--archive", choices=["1j1ju", "capital"], default="1j1ju")
    parser.add_argument("--cache", type=Path, default=Path("/tmp/source-recovery/1j1ju-index"))
    args = parser.parse_args()
    if args.archive == "capital":
        discover_capital(args.workers)
        return
    args.cache.mkdir(parents=True, exist_ok=True)
    targets = json.loads(TRACKER.read_text())["games"]
    by_title = {}
    for game in targets:
        for key in {normalize(game["title"]), normalize(game["slug"])}:
            by_title.setdefault(key, set()).add(game["slug"])
    records, failures, completed = {}, [], 0

    def fetch(page):
        dest = args.cache / f"{page:04d}.html"
        if not dest.exists():
            response = requests.get(f"https://en.1jour-1jeu.com/rules?page={page}", timeout=35)
            response.raise_for_status()
            if "All the rules of the game" not in response.text:
                raise ValueError("Unexpected index response")
            dest.write_text(response.text)
            time.sleep(0.3)
        return page, parse_page(dest.read_text())

    def persist():
        matches = {}
        for record in records.values():
            filename = Path(unquote(urlparse(record["url"]).path)).stem
            filename = re.sub(r"^[0-9a-f]{2}-", "", filename)
            slugs = by_title.get(normalize(record["title"]), set()) | by_title.get(normalize(filename), set())
            for slug in slugs:
                matches.setdefault(slug, []).append(record)
        output = {"archive": "https://en.1jour-1jeu.com/rules", "pages_completed": completed,
                  "pages_requested": args.pages, "english_documents": len(records),
                  "failures": failures, "candidates": matches}
        dest = ROOT / "docs/quality/source-recovery/archive-candidates.json"
        temp = dest.with_suffix(".tmp")
        temp.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n")
        temp.replace(dest)
        print(f"{completed}/{args.pages} pages; {len(records)} English documents; "
              f"{len(matches)} target games with exact-title candidates; {len(failures)} failures", flush=True)

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(fetch, page): page for page in range(1, args.pages + 1)}
        for future in as_completed(futures):
            try:
                page, found = future.result()
                for record in found:
                    record["discovery_page"] = f"https://en.1jour-1jeu.com/rules?page={page}"
                    records[record["url"]] = record
                completed += 1
            except Exception as error:
                failures.append({"page": futures[future], "error": str(error)})
            if (completed + len(failures)) % 25 == 0:
                persist()
    persist()


if __name__ == "__main__":
    main()
