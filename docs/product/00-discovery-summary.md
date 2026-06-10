# Discovery Summary

**Date:** 2026-06-10
**Scope:** Full inventory of the `boardgame-rules` repository, performed before drafting the product document suite.

> **What this product is:** a **board game rules database** — a catalog of 2,122 games with AI-friendly, precision-focused rules summaries, produced by a semi-automated pipeline (BGG metadata → PDF acquisition → text extraction → LLM summarization → quality gating) and published as a static site for consumption by AI assistants and humans. The documents in this suite describe that product as it exists, plus its open design questions.

## Tech Stack

- **Language:** Python 3.10+ (no web framework, no JS application — `package-lock.json` is an empty stub)
- **Data store:** Flat files only, by explicit design decision ("Flat files over SQLite", `docs/plans/2026-03-02-boardgame-rules-db-design.md`). No database, no server.
  - `games.yaml` — master registry (YAML list of game dicts)
  - `rules/*.md` — Markdown + YAML frontmatter (the product)
  - `extracted/*.txt` — raw PDF text (tracked in git)
  - `source_pdfs/*.pdf` — gitignored
- **Libraries:** PyMuPDF (fitz), pdfplumber, PyYAML, requests, beautifulsoup4, python-dotenv, anthropic SDK (`requirements.txt`)
- **External APIs:** BoardGameGeek XML API2 (bearer token, `scripts/bgg.py`); Anthropic API (`claude-sonnet-4-20250514`, `scripts/summarize.py`); BGG files-page HTML scraping (`scripts/bgg_files.py`)
- **Publishing:** Jekyll + GitHub Pages (`_config.yml`, theme `jekyll-theme-leap-day`, pretty permalinks), published at `https://jonnyallred.github.io/boardgame-rules/`
- **Concurrency:** `fcntl.flock` file locking + atomic temp-file writes in `scripts/registry.py`; atomic work-claiming with 1-hour stale-claim reclamation in `scripts/process_batch.py`
- **Agent tooling:** Claude Code skills in `.claude/skills/` (`game`, `rules-lookup`, `research-games`) and slash commands in `.claude/commands/`
- **Tests:** pytest suite in `tests/` (10 test modules covering registry, BGG client, download, extract, summarize, quality check, validate, import, batch)

## Implemented Entities (with fields)

### Game (registry entry in `games.yaml`) — 2,122 entries
| Field | Type | Presence |
|---|---|---|
| `name` | str | all entries; unique case-insensitively (verified: 0 duplicates) |
| `bgg_id` | int | all entries (verified: 0 missing, 0 duplicates) — dedup key in `add_game()` |
| `status` | enum | all entries; see status flow below |
| `designer` | str | 41 entries (comma-joined list from BGG) |
| `player_count` | str e.g. `"2-5"` | 44 entries |
| `play_time` | str e.g. `"45-90 min"` | 44 entries |
| `pdf_url` | str | 19 entries (provenance mostly discarded after download) |
| `notes` | str | 466 entries (mostly not-found reasons) |
| `base_game_bgg_id` | int | 2 entries (expansion → base-game link) |
| `claimed_at` | ISO timestamp | transient, written during claimed pipeline stages |
| `review_notes` | str | written when quality check flags a game (0 currently) |

**Status enum** (`scripts/process_batch.py:ALL_STATUSES`): `pending`, `queued`, `searching`, `found`, `not_found`, `downloading`, `downloaded`, `extracting`, `extracted`, `summarizing`, `summarized`, `quality_checking`, `validated`, `flagged`.
Current distribution: summarized 1,616 · not_found 435 · extracted 40 · flagged 19 · validated 6 · downloaded 3 · queued 3.

### RulesSummary (`rules/<slug>.md`) — 1,649 files
Frontmatter: `title`, `bgg_id` (both required by `scripts/validate.py`), `player_count`, `play_time`, `designer`, `source_pdf`, `extracted_date`, `summarized_date`, `rulebook_version`, optional `base_game_bgg_id` (8 files).
Body sections (base game): Overview, Components, Setup, Turn Structure, Actions, Scoring / Victory Conditions, Special Rules & Edge Cases, Player Reference.
Body sections (expansion, triggered by `base_game_bgg_id` in frontmatter): Overview, New Components, Setup Changes, Rule Changes, Special Rules & Edge Cases, Player Reference.

### Supporting artifacts
- **ExtractedText** (`extracted/<slug>-rules.txt`) — 1,015 files
- **SourcePDF** (`source_pdfs/<slug>-rules.pdf`) — gitignored, 0 in repo; validity = ≥10 KB + `%PDF` magic bytes (`scripts/download_pdf.py`)
- **IndexEntry** (`index.md`) — generated browse table: name, players, time, designer, link `rules/<slug>/`
- **Candidate** (`candidates*.txt`) — one `Name (bgg_id)` per line, import queue from the sibling `boardgame-database` project

## Implemented Workflows

1. **Single-game registration** — `scripts/find_rulebook.py`: BGG search → metadata fetch → registry entry (`status: pending`) → attempted PDF download from BGG files page.
2. **Bulk import** — `scripts/import_games.py`: reads sibling `boardgame-database` YAML + `master_list.csv`; matches by `bgg_id` (primary) then case-insensitive name; `--dry-run --output` produces candidates files; skips entries without a `bgg_id`.
3. **Batch pipeline** — `scripts/process_batch.py`: four independently runnable stages with atomic claiming and 1-hour stale-claim recovery:
   `found →(download)→ downloaded →(extract)→ extracted →(summarize)→ summarized →(quality_check)→ validated | flagged`
4. **PDF discovery (agentic)** — Claude Code + Playwright searches 1j1ju.com → publisher sites → Google → BGG files page (priority order per `docs/plans/2026-03-04-scalable-rules-pipeline-design.md`); writes `status: found, pdf_url:` or `status: not_found, notes:`.
5. **LLM summarization** — `scripts/summarize.py`: builds prompt with frontmatter template + 8 required sections; "precision over brevity" system prompt; skips extracted text < 500 chars.
6. **Validation & quality tiers** — `scripts/validate.py` (frontmatter + section presence) and `scripts/quality_check.py` (extracted text ≥ 2,000 bytes; every section ≥ 20 words; uncertainty-phrase scan, e.g. "unclear from the text") → `validated` or `flagged` + `review_notes`.
7. **Parallel bulk research** — `/research-games` skill + `scripts/prepare_research.py` (slug-collision check, batch JSON) + `scripts/collect_results.py` (parses `RESULTS_START/RESULTS_END` blocks from subagent output).
8. **Index generation** — `scripts/generate_index.py` *and* `scripts/rebuild_index.py` (overlapping implementations — see Conflicts).
9. **Rules Q&A** — `/game <name>` loads a summary into context; `/rules <game>: <question>` runs a 4-tier lookup (summary → extracted text → BGG forum search → labeled intuition) and auto-creates a PR when tiers 2–4 surface new information.

## Frontend Screens

There is no application frontend. The only user-facing surface is the static Jekyll site:
- **Landing page** (`index.md`): usage instructions (paste-a-prompt pattern for Claude/ChatGPT voice and text) + alphabetical game tables with a letter jump bar.
- **Game pages** (`rules/<slug>/`): rendered rules summaries at predictable URLs — the URL contract `rules/{slug}/` is explicitly part of the product (it is baked into the recommended AI prompt).
- Expansions are displayed indented under their base game with a `↳` prefix (per `CLAUDE.md`).

## Key Design Decisions Already Made (inferred from code/docs)

1. **Files are the product** — flat-file pipeline, version control as the database; explicit "can add SQLite later if scaling up."
2. **BGG ID is the canonical game identifier** — dedup key, expansion linkage, and external reference; slug (lowercase, hyphenated name) is the filesystem/URL key.
3. **Precision over brevity** — "AI can always summarize down; it can't recover lost detail."
4. **AI-first consumption** — the site is designed to be fetched by LLMs at runtime; structure (fixed section headings, frontmatter) matters more than visual design.
5. **Single-layer catalog with expansion self-reference** — one `Game` entity; expansions are games with a `base_game_bgg_id` pointer. No Work/Edition/Item layering.
6. **Human-in-the-loop quality** — auto-accept after a manual calibration phase; `flagged` is a terminal state requiring human attention.
7. **Concurrency-safe registry** — all writes through `locked_registry()`; claims are atomic; crashed workers' claims are reclaimed after 1 hour.
8. **PDFs gitignored, extracted text tracked** — reproducibility via `pdf_url`, diffability via tracked text.

## Apparent Intended Features (from stubs, TODOs, naming)

- **Edition awareness** — `rulebook_version` frontmatter (e.g. `"PD-Verlag / Rio Grande Games Edition"` in `rules/concordia.md`) records *which printing* a summary came from, but nothing consumes it.
- **Retry of misses** — `not_found` is documented as retryable ("To retry older misses, query `not_found`"); 435 games are waiting on this.
- **Quality tier rollout** — only 6 of 1,616 summarized games have passed `quality_check`; the calibration-then-auto-accept plan is designed but barely executed.
- **`searching` status** — defined in `ALL_STATUSES` and the design doc's status flow but never set by any script (the find stage is manual/agentic).
- **RAG/embedding consumption** — listed as a primary consumer in the design doc; no embedding or indexing code exists.

## Open Questions

1. **Identity model** — registry writes (`update_game`, `update_status`) are keyed by case-insensitive `name`, dedup by `bgg_id`, files by `slug`. Three keys, no enforced consistency. Which becomes canonical if this grows a database?
2. **Registry ↔ filesystem drift** — 26 rules files have no registry entry matching their slug; 20 summarized/validated entries have no rules file. No reconciliation tool exists.
3. **Expansion linkage inconsistency** — 8 rules files carry `base_game_bgg_id` but only 2 registry entries do. Which side is authoritative?
4. **Duplicate index generators** — `generate_index.py` vs `rebuild_index.py` implement the same job with different code paths. Which is canonical?
5. **Quality threshold drift** — design doc says flag sections "< 50 words"; code uses `MIN_SECTION_WORDS = 20`.
6. **Licensing of rulebook content** — summaries are derived from publisher PDFs; no license or permission policy is recorded anywhere.
7. **Quality backlog** — 1,610 summarized games have never been quality-checked, and 19 flagged games have no review tooling or workflow.
