"""Guard the source recovery review boundary and preserve existing sources."""
import json

import fitz
import pytest

from scripts import recover_sources as recovery
from scripts.discover_rulebook_sources import parse_page


@pytest.fixture
def recovery_env(tmp_path, monkeypatch):
    monkeypatch.setattr(recovery, "ROOT", tmp_path)
    monkeypatch.setattr(recovery, "TRACKER", tmp_path / "inventory.json")
    monkeypatch.setattr(recovery, "STAGING", tmp_path / "staged")
    (tmp_path / "extracted").mkdir()
    recovery.save({"games": [{"slug": "example", "status": "pending", "attempts": []}]})
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((30, 30), "Example Game: complete gameplay rules. " * 5)
    path = tmp_path / "download.pdf"
    doc.save(path)
    doc.close()
    return path


def test_download_does_not_install_without_review(recovery_env):
    recovery.fetch("example", "https://publisher.test/rules.pdf", cached_file=recovery_env)
    assert not (recovery.ROOT / "extracted/example-rules.txt").exists()
    data = json.loads(recovery.TRACKER.read_text())
    assert data["games"][0]["status"] == "downloaded_needs_review"


def test_explicit_html_selection_preserves_original_and_review_boundary(recovery_env):
    html = '<html><body><nav>Other games</nav><main><h1>Games</h1><p>Unrelated game.</p><h2>Example rules</h2><p>'
    html += 'Place your pieces, move them in turns and reach the goal. ' * 5
    html += '</p><h2>Other section</h2><p>Another game.</p></main></body></html>'
    source = recovery_env.with_suffix(".html")
    source.write_text(html)
    recovery.stage_html_selection(
        "example", "https://author.test/games", cached_file=source,
        selector="main", title="Example", source_type="author_rules_html",
        selection_note="Selected the author's Example rules section only.",
        start_text="Example rules", end_text="Other section")
    data = json.loads(recovery.TRACKER.read_text())
    attempt = data["games"][0]["attempts"][-1]
    assert (recovery.ROOT / attempt["file"]).read_text() == html
    selected = (recovery.ROOT / attempt["staged_text"]).read_text()
    assert "Place your pieces" in selected
    assert "Unrelated game" not in selected and "Another game" not in selected
    assert not (recovery.ROOT / "extracted/example-rules.txt").exists()


def test_review_rejects_changed_source(recovery_env):
    recovery.fetch("example", "https://publisher.test/rules.pdf", cached_file=recovery_env)
    (recovery.STAGING / "example.txt").write_text("different source")
    with pytest.raises(ValueError, match="changed"):
        recovery.accept("example", "reviewed the correct edition")
    assert not (recovery.ROOT / "extracted/example-rules.txt").exists()


def test_plaintext_rules_selection_excludes_unrelated_sections(recovery_env):
    source = recovery_env.with_suffix(".md")
    source.write_text("Implementation notes\nRules\n" + "Move a piece and reach the goal. " * 8 + "\nAuthor biography\n")
    recovery.stage_text_selection(
        "example", "https://source.test/README.md", cached_file=source,
        title="Example rules", selection_note="Rules section of implementation documentation.",
        start_text="Rules", end_text="Author biography")
    assert not (recovery.ROOT / "extracted/example-rules.txt").exists()
    selected = (recovery.STAGING / "example.txt").read_text()
    assert "Implementation notes" not in selected and "Author biography" not in selected
    recovery.accept("example", "Reviewed complete matching rules")
    game = json.loads(recovery.TRACKER.read_text())["games"][0]
    assert game["source_file"].endswith(".md")
    assert game["source_type"] == "rules_reference_text"


def test_review_preserves_existing_source(recovery_env):
    recovery.fetch("example", "https://publisher.test/rules.pdf", cached_file=recovery_env)
    dest = recovery.ROOT / "extracted/example-rules.txt"
    dest.write_text("existing authoritative source")
    with pytest.raises(ValueError, match="existing nonempty"):
        recovery.accept("example", "reviewed the correct edition")
    assert dest.read_text() == "existing authoritative source"


def test_selected_source_cannot_downgrade_an_accepted_record(recovery_env):
    source = recovery_env.with_suffix(".md")
    source.write_text("Move a piece and reach the goal. " * 8)
    arguments = dict(cached_file=source, title="Example", selection_note="Reviewed reference.")
    recovery.stage_text_selection("example", "https://source.test/rules.md", **arguments)
    recovery.accept("example", "Reviewed complete matching rules")
    before = recovery.TRACKER.read_bytes()
    canonical = recovery.ROOT / "extracted/example-rules.txt"
    text_before = canonical.read_bytes()
    with pytest.raises(ValueError, match="already recovered"):
        recovery.stage_text_selection("example", "https://source.test/rules.md", **arguments)
    assert recovery.TRACKER.read_bytes() == before
    assert canonical.read_bytes() == text_before


def test_scan_without_ocr_cannot_be_accepted_as_text(recovery_env):
    doc = fitz.open()
    doc.new_page()
    path = recovery_env.with_name("scan.pdf")
    doc.save(path)
    doc.close()
    recovery.fetch("example", "https://publisher.test/scan.pdf", cached_file=path)
    with pytest.raises(ValueError, match="No usable extracted page text"):
        recovery.accept("example", "a PDF download alone is insufficient")
    assert not (recovery.ROOT / "extracted/example-rules.txt").exists()


def test_native_intro_does_not_hide_scanned_gameplay_pages():
    pages = [{"method": "pdf_text", "characters": 1400},
             {"method": "pdf_text", "characters": 0}]
    assert recovery.needs_ocr(pages)
    pages[1]["method"] = "tesseract_deu_216dpi"
    assert not recovery.needs_ocr(pages)


def test_force_ocr_replaces_an_existing_but_unusable_pdf_text_layer(recovery_env, monkeypatch):
    from types import SimpleNamespace
    monkeypatch.setattr(recovery.subprocess, "run", lambda *a, **kw:
                        SimpleNamespace(stdout="Readable rules recognized from the scanned page. " * 5))
    text, pages = recovery.extract_pdf(recovery_env, force_ocr=True)
    assert "Readable rules recognized" in text
    assert "Example Game: complete gameplay rules" not in text
    assert pages[0]["method"].startswith("tesseract")


@pytest.mark.parametrize("status", ["rejected_identity_mismatch", "rejected_quality", "rejected_edition_mismatch"])
def test_batch_does_not_retry_rejected_source(recovery_env, monkeypatch, status):
    url = "https://publisher.test/wrong-game.pdf"
    data = json.loads(recovery.TRACKER.read_text())
    data["games"][0]["attempts"].append({"url": url, "status": status})
    recovery.save(data)
    candidates = recovery.ROOT / "candidates.json"
    candidates.write_text(json.dumps({"example": [{"url": url}]}))
    monkeypatch.setattr(recovery.requests, "get", lambda *a, **kw: pytest.fail("Rejected URL requested"))
    recovery.batch(candidates, workers=1)
    assert json.loads(recovery.TRACKER.read_text()) == data


def test_archive_discovery_only_returns_english_documents():
    html = '''<div class="col-center"><h3>Example Rulebook</h3>
    <a title="In French" href="https://archive.test/fr.pdf">French</a>
    <a title="In English" href="https://archive.test/en.pdf">English</a></div>'''
    assert parse_page(html) == [{"title": "Example Rulebook", "url": "https://archive.test/en.pdf"}]


def test_html_challenge_page_is_not_a_rules_source():
    with pytest.raises(ValueError, match="No identifiable rules article"):
        recovery.extract_html_rules("<html><h1>Just a moment...</h1><p>Checking your browser</p></html>")


def test_rulebook_article_with_game_heading_excludes_surrounding_navigation():
    html = '<nav>Other games</nav><article><h1>Example</h1><h1>Example Rulebook</h1><p>'
    html += 'Place a piece and complete the goal. ' * 30 + '</p></article><footer>About us</footer>'
    title, text = recovery.extract_html_rules(html)
    assert title == "Example Rulebook"
    assert "Place a piece" in text
    assert "Other games" not in text and "About us" not in text


def test_html_rules_extraction_excludes_scripts_and_recommendations():
    html = '<div id="main"><h1>Example Game Rules</h1><p>' + 'Place a piece and complete the goal. ' * 30
    html += '</p><script>trackingData()</script><div id="recommended_posts">Other game instructions</div></div>'
    title, text = recovery.extract_html_rules(html)
    assert title == "Example Game Rules"
    assert "Place a piece" in text
    assert "trackingData" not in text
    assert "Other game" not in text
