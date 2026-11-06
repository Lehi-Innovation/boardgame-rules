"""Recover source files without automatically claiming a usable source or audit PASS.

Download: python -m scripts.recover_sources fetch SLUG URL [--ocr]
Review: inspect source_pdfs/<slug>-recovery.pdf and the staged text, then:
python -m scripts.recover_sources accept SLUG --evidence 'Identity and completeness checks'

The inventory retains all original targets, candidate URLs, failures, hashes,
and review evidence. Acceptance installs text only; summary auditing is separate.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

import fitz
import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
TRACKER = ROOT / "docs/quality/source-recovery/inventory.json"
STAGING = ROOT / "docs/quality/source-recovery/staged"


def timestamp():
    return datetime.now(timezone.utc).isoformat()


def save(data):
    temp = TRACKER.with_suffix(".tmp")
    temp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    temp.replace(TRACKER)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def extract_html_rules(html):
    """Extract the rules article only, rejecting navigation or challenge pages."""
    soup = BeautifulSoup(html, "html.parser")
    article = soup.select_one("#main")
    if article is None:
        # RulesPal exposes actual rulebooks in an article; missing-game URLs
        # redirect to a landing page without one. Require its explicit title.
        candidate = soup.find("article")
        if candidate is not None and any("rulebook" in h.get_text(" ", strip=True).lower()
                                         for h in candidate.find_all("h1")):
            article = candidate
    if article is None or article.find("h1") is None:
        raise ValueError("No identifiable rules article")
    heading = next((h for h in article.find_all("h1")
                    if any(word in h.get_text(" ", strip=True).lower()
                           for word in ["rules", "rulebook"])), None)
    if heading is None:
        raise ValueError("Page is not explicitly a rules article")
    title = heading.get_text(" ", strip=True)
    for element in article.select("script, style, noscript, iframe, #recommended_posts, [id^='ezoic-pub-ad'], .post-meta, .post-rating"):
        element.decompose()
    for link in article.select("a[href]"):
        if link.get_text(" ", strip=True) == "Continue Reading":
            link.decompose()
    text = article.get_text("\n", strip=True)
    # Game headers may include expansion/recommendation links before the
    # rulebook heading. Keep the explicitly titled rules content onward.
    text = text[text.index(title):]
    if len(text.split()) < 150:
        raise ValueError("Rules article is too short; manual review required")
    return title, text + "\n"


def fetch_html(slug, url, cached_file=None):
    """Stage a clearly labelled third-party rules transcription for review."""
    data = json.loads(TRACKER.read_text())
    game = next(g for g in data["games"] if g["slug"] == slug)
    attempt = {"url": url, "attempted_at": timestamp(), "source_type": "third_party_rules_transcription"}
    game["attempts"].append(attempt)
    try:
        final_url = url
        if cached_file:
            content = Path(cached_file).read_bytes()
        else:
            response = requests.get(url, timeout=(15, 60))
            response.raise_for_status()
            content = response.content
            final_url = response.url
        title, text = extract_html_rules(content.decode("utf-8", errors="replace"))
        text = ("SOURCE TRANSCRIPTION NOTE\nThis is a third-party rules transcription. "
                "It is not a publisher PDF extraction and may omit diagrams, revisions, or errata.\n"
                f"Source: {final_url}\n\n" + text)
        original = ROOT / "source_pdfs" / f"{slug}-recovery.html"
        original.parent.mkdir(exist_ok=True)
        if original.exists() and sha256(original.read_bytes()) != sha256(content):
            original = original.with_name(f"{slug}-recovery-{sha256(content)[:12]}.html")
        original.write_bytes(content)
        STAGING.mkdir(parents=True, exist_ok=True)
        staged = STAGING / f"{slug}.txt"
        staged.write_text(text)
        attempt.update(status="downloaded_needs_review", final_url=final_url,
                       file=str(original.relative_to(ROOT)), file_sha256=sha256(content),
                       bytes=len(content), title=title, characters=len(text),
                       staged_text=str(staged.relative_to(ROOT)), text_sha256=sha256(text.encode()),
                       pages=[{"page": 1, "method": "html_rules_article", "characters": len(text)}])
        game["status"] = "downloaded_needs_review"
        print(f"{slug}: staged third-party transcription, {len(text)} characters; review required")
    except Exception as error:
        attempt.update(status="failed", error=str(error))
        print(f"{slug}: {error}")
    save(data)


def stage_html_selection(slug, url, *, cached_file, selector, title, source_type,
                         selection_note, start_text=None, end_text=None):
    """Stage an explicitly selected rules section; acceptance remains separate.

    Older author and university sites do not necessarily have rulebook headings.
    Require an explicit selector and provenance note instead of guessing an article.
    The original HTML is retained unchanged, even when only one section is selected.
    """
    if source_type not in {"author_rules_html", "rules_reference_html"}:
        raise ValueError("Selected HTML must identify its author/reference source type")
    if not selector or not title or not selection_note:
        raise ValueError("Selector, title and selection note are required")
    content = Path(cached_file).read_bytes()
    soup = BeautifulSoup(content, "html.parser")
    section = soup.select_one(selector)
    if section is None:
        raise ValueError("Selected rules section is absent")
    for element in section.select("script, style, noscript, iframe, nav, footer"):
        element.decompose()
    selected = section.get_text("\n", strip=True)
    if start_text:
        selected = selected[selected.index(start_text):]
    if end_text:
        selected = selected[:selected.index(end_text)]
    _stage_selected_source(
        slug, url, content=content, selected=selected, title=title,
        source_type=source_type, selection_note=selection_note, suffix=".html",
        selection={"selector": selector, "start_text": start_text, "end_text": end_text},
        method="explicit_html_selection")


def stage_text_selection(slug, url, *, cached_file, title, selection_note,
                         start_text=None, end_text=None):
    """Stage a selected section of a public plain-text/Markdown rules reference."""
    source = Path(cached_file)
    if source.suffix.lower() not in {".txt", ".md"}:
        raise ValueError("Plain-text selection requires a .txt or .md source")
    if not title or not selection_note:
        raise ValueError("Title and selection note are required")
    content = source.read_bytes()
    selected = content.decode("utf-8")
    if start_text:
        selected = selected[selected.index(start_text):]
    if end_text:
        selected = selected[:selected.index(end_text)]
    _stage_selected_source(
        slug, url, content=content, selected=selected, title=title,
        source_type="rules_reference_text", selection_note=selection_note,
        suffix=source.suffix.lower(), selection={"start_text": start_text, "end_text": end_text},
        method="explicit_plaintext_selection")


def _stage_selected_source(slug, url, *, content, selected, title, source_type,
                           selection_note, suffix, selection, method):
    if len(selected.strip()) < 100:
        raise ValueError("Selected rules section is too short for review")
    text = (f"SOURCE SELECTION NOTE\n{selection_note}\nSource: {url}\n\n"
            f"{title}\n\n{selected.strip()}\n")
    data = json.loads(TRACKER.read_text())
    game = next(g for g in data["games"] if g["slug"] == slug)
    if game["status"] == "recovered":
        raise ValueError("Refusing to restage an already recovered source")
    original = ROOT / "source_pdfs" / f"{slug}-selection-{sha256(content)[:12]}{suffix}"
    original.parent.mkdir(exist_ok=True)
    original.write_bytes(content)
    STAGING.mkdir(parents=True, exist_ok=True)
    staged = STAGING / f"{slug}.txt"
    staged.write_text(text)
    game["attempts"].append({
        "url": url, "final_url": url, "attempted_at": timestamp(),
        "status": "downloaded_needs_review", "source_type": source_type,
        "file": str(original.relative_to(ROOT)), "file_sha256": sha256(content),
        "bytes": len(content), "title": title, "selection_note": selection_note,
        **selection,
        "characters": len(text), "staged_text": str(staged.relative_to(ROOT)),
        "text_sha256": sha256(text.encode()),
        "pages": [{"page": 1, "method": method, "characters": len(selected)}],
    })
    game["status"] = "downloaded_needs_review"
    save(data)
    print(f"{slug}: selected rules section staged; manual review required")


def extract_pdf(path, ocr=False, ocr_language="eng", force_ocr=False):
    pages = []
    methods = []
    with fitz.open(path) as doc:
        for number, page in enumerate(doc, 1):
            text = page.get_text().strip()
            method = "pdf_text"
            if force_ocr or (ocr and len(re.findall(r"[A-Za-z]{2,}", text)) < 20):
                with tempfile.TemporaryDirectory(prefix="rulebook-ocr-") as tmp:
                    image = Path(tmp) / "page.png"
                    # Some scans encode pixel dimensions as PDF points. Cap
                    # the raster size so those pages are not enlarged to tens
                    # of megapixels before recognition.
                    scale = min(3, 2600 / max(page.rect.width, page.rect.height))
                    page.get_pixmap(matrix=fitz.Matrix(scale, scale)).save(str(image))
                    result = subprocess.run(
                        ["tesseract", str(image), "stdout", "-l", ocr_language],
                        capture_output=True, text=True, check=True, timeout=180,
                        env={**os.environ, "OMP_THREAD_LIMIT": "1"},
                    )
                    text = result.stdout.strip()
                    method = f"tesseract_{ocr_language}_216dpi"
                    if len(text) < 100:
                        # Foldout sheets and colored shapes can look like blank
                        # pages to automatic layout detection. Sparse text mode
                        # is a fallback candidate, still requiring review.
                        sparse = subprocess.run(
                            ["tesseract", str(image), "stdout", "-l", ocr_language, "--psm", "11"],
                            capture_output=True, text=True, check=True, timeout=180,
                            env={**os.environ, "OMP_THREAD_LIMIT": "1"},
                        ).stdout.strip()
                        if len(sparse) > len(text):
                            text = sparse
                            method = f"tesseract_{ocr_language}_216dpi_psm11"
            text = "\n".join(line.rstrip() for line in text.splitlines()).strip()
            pages.append(f"--- Page {number} ---\n{text}")
            methods.append({"page": number, "method": method, "characters": len(text)})
    return "\n\n".join(pages) + "\n", methods


def fetch(slug, url, ocr=False, cached_file=None, force_ocr=False):
    data = json.loads(TRACKER.read_text())
    game = next(g for g in data["games"] if g["slug"] == slug)
    attempt = {"url": url, "attempted_at": timestamp()}
    game["attempts"].append(attempt)
    try:
        final_url = url
        if cached_file:
            content = Path(cached_file).read_bytes()
        else:
            response = requests.get(url, timeout=(15, 90))
            response.raise_for_status()
            content = response.content
            final_url = response.url
        if not content.startswith(b"%PDF-"):
            raise ValueError("Response is not a PDF; no source installed")
        path = ROOT / "source_pdfs" / f"{slug}-recovery.pdf"
        path.parent.mkdir(exist_ok=True)
        if path.exists() and sha256(path.read_bytes()) != sha256(content):
            path = path.with_name(f"{slug}-recovery-{sha256(content)[:12]}.pdf")
        path.write_bytes(content)
        text, pages = extract_pdf(path, ocr=ocr, force_ocr=force_ocr)
        STAGING.mkdir(parents=True, exist_ok=True)
        staged = STAGING / f"{slug}.txt"
        staged.write_text(text)
        attempt.update({
            "status": "downloaded_needs_review", "final_url": final_url,
            "file": str(path.relative_to(ROOT)), "file_sha256": sha256(content),
            "bytes": len(content), "pages": pages,
            "staged_text": str(staged.relative_to(ROOT)),
            "text_sha256": sha256(text.encode()), "characters": len(text),
        })
        game["status"] = "downloaded_needs_review"
        print(f"{slug}: {len(pages)} pages, {len(text)} characters; review {staged}")
    except Exception as error:
        attempt.update({"status": "failed", "error": str(error)})
        print(f"{slug}: {error}")
    save(data)


def accept(slug, evidence, language="English"):
    data = json.loads(TRACKER.read_text())
    game = next(g for g in data["games"] if g["slug"] == slug)
    attempt = next(a for a in reversed(game["attempts"]) if a["status"] == "downloaded_needs_review")
    staged = ROOT / attempt["staged_text"]
    content = staged.read_bytes()
    if sha256(content) != attempt["text_sha256"]:
        raise ValueError("Staged source changed since extraction; review its provenance")
    if not content.strip() or not any(p["characters"] > 100 for p in attempt["pages"]):
        raise ValueError("No usable extracted page text; retain file for OCR/review")
    dest = ROOT / "extracted" / f"{slug}-rules.txt"
    if dest.exists() and dest.read_text().strip():
        raise ValueError("Refusing to replace an existing nonempty source")
    dest.write_bytes(content)
    game.update({"status": "recovered", "source_url": attempt["final_url"],
                 "source_file": attempt["file"], "source_file_sha256": attempt["file_sha256"],
                 "text_path": str(dest.relative_to(ROOT)), "text_sha256": sha256(content),
                 "reviewed_at": timestamp(), "review_evidence": evidence,
                 "source_language": language,
                 "source_type": attempt.get("source_type", "rulebook_pdf"),
                 "summary_audit": "not performed by source recovery"})
    # The canonical extraction is the durable artifact; provenance retains its hash.
    staged.unlink()
    print(f"{slug}: source recovered; summary still requires a separate audit")
    save(data)


def finalize(stamp_date):
    """Refresh accepted-source provenance, conservative labels and local catalog."""
    from scripts.stamp_verification import load_audit_results, stamp_file
    import yaml

    data = json.loads(TRACKER.read_text())
    audits = load_audit_results(str(ROOT / "docs/quality/semantic-audit-results.yaml"))
    recovered = [g for g in data["games"] if g["status"] == "recovered"]
    for game in recovered:
        path = ROOT / game["text_path"]
        original = path.read_text()
        if sha256(path.read_bytes()) != game["text_sha256"]:
            raise ValueError(f"Accepted source changed without review: {game['slug']}")
        if sha256((ROOT / game["source_file"]).read_bytes()) != game["source_file_sha256"]:
            raise ValueError(f"Original source file changed: {game['slug']}")
        text = "\n".join(line.rstrip() for line in original.splitlines()).rstrip() + "\n"
        attempt = next(a for a in reversed(game["attempts"]) if a["status"] == "downloaded_needs_review")
        if any(p["method"].startswith("tesseract") for p in attempt["pages"]) and not text.startswith("SOURCE EXTRACTION NOTE"):
            text = ("SOURCE EXTRACTION NOTE\nThis is an OCR transcription and may contain recognition errors. "
                    "Consult the original PDF for exact wording, numbers, tables, symbols, and diagrams.\n"
                    f"Original PDF: {game['source_url']}\n\n" + text)
        if game.get("source_type") == "rulebook_images" and text.startswith("SOURCE EXTRACTION NOTE\n"):
            notice, separator, body = text.partition("\n\n")
            notice = notice.replace("original PDF", "original images").replace("Original PDF:", "Original images:")
            text = notice + separator + body
        game.setdefault("raw_extraction_text_sha256", game["text_sha256"])
        game.setdefault("source_language", "English")
        game.setdefault("source_type", "rulebook_pdf")
        game["text_normalization"] = "Trailing whitespace removed; OCR transcriptions have an extraction notice and original source URL."
        path.write_text(text)
        game["text_sha256"] = sha256(text.encode())
        rule = ROOT / "rules" / (game["slug"] + ".md")
        front, body = rule.read_text()[4:].split("\n---", 1)
        metadata = yaml.safe_load(front)
        source_key = {".html": "source_html", ".md": "source_text", ".txt": "source_text", ".rtf": "source_text"}.get(
            Path(game["source_file"]).suffix.lower(), "source_pdf")
        if source_key != "source_pdf":
            front = re.sub(r"(?m)^source_pdf:.*\n?", "", front)
        for key, value in {source_key: Path(game["source_file"]).name,
                           "source_url": game["source_url"], "source_type": game["source_type"], "source_language": game["source_language"],
                           "extracted_date": stamp_date}.items():
            line = key + ": " + json.dumps(value, ensure_ascii=False)
            if re.search(r"^" + key + r":.*$", front, re.M):
                front = re.sub(r"^" + key + r":.*$", lambda _: line, front, flags=re.M)
            else:
                front += "\n" + line
        rule.write_text("---\n" + front + "\n---" + body)
        # Finding a new source cannot substantiate an old PASS for unavailable
        # text. Preserve any verified status already earned by a later audit.
        if metadata.get("verification") not in {"verified", "minor_issues"}:
            applicable = audits if audits.get(game["slug"], {}).get("verdict") == "MAJOR" else {}
            stamp_file(str(rule), applicable, extracted_dir=str(ROOT / "extracted"), stamp_date=stamp_date)
    save(data)
    with (TRACKER.parent / "recovered.csv").open("w") as handle:
        fields = ["slug", "title", "bgg_id", "source_language", "source_url", "text_path", "review_evidence"]
        writer = csv.writer(handle)
        writer.writerow(fields)
        for game in recovered:
            writer.writerow([game.get(key, "") for key in fields])
    for module in ["scripts.generate_index", "scripts.generate_manifest"]:
        subprocess.run([sys.executable, "-m", module], cwd=ROOT, check=True)
    print(f"Recovered {len(recovered)}/{len(data['games'])}; remaining {len(data['games']) - len(recovered)}")


def batch(candidate_path, limit=0, workers=4):
    """Download concurrently but serialize inventory changes and source staging."""
    from concurrent.futures import ThreadPoolExecutor, as_completed

    candidates = json.loads(candidate_path.read_text())
    candidates = candidates.get("candidates", candidates)
    inventory = json.loads(TRACKER.read_text())
    games = {g["slug"]: g for g in inventory["games"]}
    todo = []
    for slug, items in candidates.items():
        game = games.get(slug)
        if not game or game["status"] == "recovered":
            continue
        available = [item for item in items
                     if not item.get("review_status", "").startswith("rejected")
                     and not any(a.get("status", "").startswith("rejected") and a["url"] == item["url"]
                                 for a in game["attempts"])]
        if not available:
            continue
        url = available[0]["url"]
        if any(a.get("status") == "downloaded_needs_review" and a["url"] == url
               for a in game["attempts"]):
            continue
        todo.append((slug, url))
    if limit:
        todo = todo[:limit]
    print(f"Downloading {len(todo)} candidates for review", flush=True)

    with tempfile.TemporaryDirectory(prefix="rulebook-downloads-") as tmp:
        def download(item):
            slug, url = item
            response = requests.get(url, timeout=(15, 90))
            response.raise_for_status()
            if not response.content.startswith(b"%PDF-"):
                raise ValueError("Response is not a PDF")
            dest = Path(tmp) / f"{slug}.pdf"
            dest.write_bytes(response.content)
            return dest, response.url

        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {executor.submit(download, item): item for item in todo}
            for future in as_completed(futures):
                slug, url = futures[future]
                try:
                    path, final_url = future.result()
                    fetch(slug, url, cached_file=path)
                    if final_url != url:
                        data = json.loads(TRACKER.read_text())
                        game = next(g for g in data["games"] if g["slug"] == slug)
                        game["attempts"][-1]["final_url"] = final_url
                        save(data)
                except Exception as error:
                    data = json.loads(TRACKER.read_text())
                    game = next(g for g in data["games"] if g["slug"] == slug)
                    game["attempts"].append({"url": url, "attempted_at": timestamp(),
                                             "status": "failed", "error": str(error)})
                    save(data)
                    print(f"{slug}: {error}", flush=True)


def needs_ocr(pages):
    # A native-text introduction must not hide scanned gameplay pages. Once
    # OCR has been attempted, a blank cover should not enqueue the book again.
    return any(p["method"] == "pdf_text" and p["characters"] < 100 for p in pages)


def ocr_staged(slugs=None, workers=4, ocr_language="eng"):
    """OCR downloaded scans, keeping every source pending human/agent review."""
    from concurrent.futures import ProcessPoolExecutor, as_completed

    data = json.loads(TRACKER.read_text())
    todo = []
    for game in data["games"]:
        if game["status"] != "downloaded_needs_review" or (slugs and game["slug"] not in slugs):
            continue
        attempt = next(a for a in reversed(game["attempts"]) if a["status"] == "downloaded_needs_review")
        # Front/back covers may have little text; do not skip an otherwise scanned book.
        if not needs_ocr(attempt["pages"]):
            continue
        todo.append((game, attempt))
    print(f"OCR queue: {len(todo)} books, {workers} processes; results require review", flush=True)
    # PyMuPDF is not thread safe. Isolate PDF rendering in worker processes;
    # only this parent writes source staging and inventory records.
    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(extract_pdf, ROOT / attempt["file"], True, ocr_language): (game, attempt)
                   for game, attempt in todo}
        for future in as_completed(futures):
            game, attempt = futures[future]
            try:
                text, pages = future.result()
                (ROOT / attempt["staged_text"]).write_text(text)
                attempt.update(pages=pages, text_sha256=sha256(text.encode()), characters=len(text))
                save(data)
                print(f"{game['slug']}: OCR {len(pages)} pages, {len(text)} characters; pending review", flush=True)
            except Exception as error:
                attempt["ocr_error"] = str(error)
                save(data)
                print(f"{game['slug']}: OCR failed: {error}", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    fetch_parser = sub.add_parser("fetch")
    fetch_parser.add_argument("slug")
    fetch_parser.add_argument("url")
    fetch_parser.add_argument("--ocr", action="store_true")
    fetch_parser.add_argument("--force-ocr", action="store_true",
                              help="Recognize every page, replacing an unusable existing PDF text layer")
    fetch_parser.add_argument("--cached-file", type=Path, help="Use an already downloaded copy of URL")
    html_parser = sub.add_parser("fetch-html")
    html_parser.add_argument("slug")
    html_parser.add_argument("url")
    html_parser.add_argument("--cached-file", type=Path)
    review_parser = sub.add_parser("accept")
    review_parser.add_argument("slug")
    review_parser.add_argument("--evidence", required=True)
    review_parser.add_argument("--language", default="English")
    finalize_parser = sub.add_parser("finalize")
    finalize_parser.add_argument("--date", required=True, help="Client-local date, YYYY-MM-DD")
    batch_parser = sub.add_parser("batch")
    batch_parser.add_argument("candidates", type=Path)
    batch_parser.add_argument("--limit", type=int, default=0)
    batch_parser.add_argument("--workers", type=int, default=4)
    ocr_parser = sub.add_parser("ocr-staged")
    ocr_parser.add_argument("slugs", nargs="*")
    ocr_parser.add_argument("--workers", type=int, default=4)
    ocr_parser.add_argument("--ocr-language", default="eng", help="Installed Tesseract language code, e.g. deu or fra")
    args = parser.parse_args()
    if args.command == "fetch":
        fetch(args.slug, args.url, args.ocr, args.cached_file, force_ocr=args.force_ocr)
    elif args.command == "fetch-html":
        fetch_html(args.slug, args.url, args.cached_file)
    elif args.command == "accept":
        accept(args.slug, args.evidence, args.language)
    elif args.command == "finalize":
        finalize(args.date)
    elif args.command == "batch":
        batch(args.candidates, args.limit, args.workers)
    else:
        ocr_staged(args.slugs, args.workers, args.ocr_language)


if __name__ == "__main__":
    main()
