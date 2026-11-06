"""Find rulebook candidates by the catalog's BGG IDs, without accepting files.

The public file listing is cached and paginated. File-page links are discovery
evidence, not proof of a usable download. Original rules are ranked ahead of
summaries, player aids, variants, maps and other secondary material.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from pathlib import Path
import re
import time
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
import requests

from scripts.recover_sources import ROOT, TRACKER

CACHE = Path("/tmp/source-recovery/bgg-index")
OUTPUT = ROOT / "docs/quality/source-recovery/bgg-candidates.json"


def source_candidates(data):
    candidates = []
    for record in data.get("files", []):
        title = record.get("title", "")
        filename = record.get("filename", "")
        description = record.get("description", {}).get("rendered", "")
        soup = BeautifulSoup(description, "html.parser")
        plain = soup.get_text(" ", strip=True)
        label = (title + " " + filename).lower()
        rule = bool(re.search(r"rule|instruction|manual|spielregel|spielanleitung|regolament|r[eè]gle", label))
        secondary = bool(re.search(r"summary|player.?aid|quick|reference|variant|errata|faq|clarification|scenario|map|counter|card", label))
        external = []
        for link in soup.select("a[href]"):
            url = link["href"]
            if urlparse(url).scheme in {"http", "https"} and urlparse(url).path.lower().endswith(".pdf"):
                external.append(url)
        # Keep off-site original-rule links even if the uploaded file is an aid.
        if not rule and not external:
            continue
        score = 20 * rule + 15 * ("official" in label) - 35 * secondary
        score += 10 * (record.get("language") == "English")
        score += 5 * filename.lower().endswith(".pdf")
        candidates.append({
            "title": title, "filename": filename, "fileid": record.get("fileid"),
            "filepageid": record.get("filepageid"), "language": record.get("language"),
            "bytes": int(record.get("size") or 0), "description": plain,
            "url": urljoin("https://boardgamegeek.com", record.get("href", "")),
            "normal_download_url": "https://boardgamegeek.com/file/download_redirect/" + str(record.get("fileid")),
            "external_pdf_urls": external, "secondary_material": secondary, "rank_score": score,
            "status": "candidate_not_downloaded_or_reviewed",
        })
    return sorted(candidates, key=lambda item: -item["rank_score"])


def discover_game(bgg_id):
    records, pages, next_page = [], [], 1
    while True:
        dest = CACHE / f"{bgg_id}-{next_page:04d}.json"
        url = (f"https://api.geekdo.com/api/files?objectid={bgg_id}"
               f"&objecttype=thing&pageid={next_page}&showcount=100")
        if dest.exists():
            data = json.loads(dest.read_text())
        else:
            response = requests.get(url, timeout=(15, 45))
            response.raise_for_status()
            data = response.json()
            if "files" not in data or "config" not in data:
                raise ValueError("Unexpected BGG file-list response")
            dest.write_text(json.dumps(data, ensure_ascii=False))
            time.sleep(1.0)
        records.extend(data["files"])
        pages.append(url)
        last_page = int(data["config"].get("endpage") or 1)
        if next_page >= last_page:
            break
        next_page += 1
    return {"bgg_id": bgg_id, "files_examined": len(records), "listing_pages": pages,
            "candidates": source_candidates({"files": records})}


def main():
    CACHE.mkdir(parents=True, exist_ok=True)
    targets = [g for g in json.loads(TRACKER.read_text())["games"] if g["status"] != "recovered"]
    by_id = {}
    for game in targets:
        if game.get("bgg_id"):
            by_id.setdefault(game["bgg_id"], []).append(game["slug"])
    output = {"provider": "BGG public files API", "target_games": len(targets),
              "unique_ids": len(by_id), "completed": {}, "failures": []}

    def persist():
        temp = OUTPUT.with_suffix(".tmp")
        temp.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n")
        temp.replace(OUTPUT)
        found = sum(bool(v["candidates"]) for v in output["completed"].values())
        print(f"BGG: {len(output['completed'])}/{len(by_id)} IDs checked; "
              f"{found} with rule-related candidates; {len(output['failures'])} failures", flush=True)

    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = {executor.submit(discover_game, bgg_id): bgg_id for bgg_id in by_id}
        for future in as_completed(futures):
            bgg_id = futures[future]
            try:
                result = future.result()
                result["slugs"] = by_id[bgg_id]
                output["completed"][str(bgg_id)] = result
            except Exception as error:
                output["failures"].append({"bgg_id": bgg_id, "slugs": by_id[bgg_id], "error": str(error)})
            if (len(output["completed"]) + len(output["failures"])) % 20 == 0:
                persist()
    persist()


if __name__ == "__main__":
    main()
