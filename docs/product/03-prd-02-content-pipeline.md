# PRD-02 — Content Pipeline (Acquisition → Extraction → Summarization)

The pipeline is the production machinery of the product: it turns a game name into a published rules summary. All of this is code-backed.

## Pipeline shape

Four independently runnable stages orchestrated by `scripts/process_batch.py`, each gated on an input status:

| Stage | Input status | Transient (claimed) status | Output status | Implementation |
|---|---|---|---|---|
| download | `found` | `downloading` | `downloaded` | `scripts/download_pdf.py` |
| extract | `downloaded` | `extracting` | `extracted` | `scripts/extract_pdf.py` |
| summarize | `extracted` | `summarizing` | `summarized` | `scripts/summarize.py` |
| quality_check | `summarized` | `quality_checking` | `validated` or `flagged` | `scripts/quality_check.py` |

Upstream of the pipeline: **find** (agentic, no script — Claude Code + Playwright per `CLAUDE.md`'s "Batch PDF Finding") moves games `pending`/`queued` → `found` (+ `pdf_url`) or `not_found` (+ `notes`).

**Retryable states:** `pending`, `not_found`. **Terminal states:** `validated`, `flagged`. (Per `CLAUDE.md`.)

## Concurrency & crash recovery

- Every registry write goes through `locked_registry()` (`fcntl.flock` + atomic temp-file replace) — `scripts/registry.py`.
- Stages **claim work atomically** before running (`claim_games_by_status()`): status flips to the transient form and a `claimed_at` ISO timestamp is written, so concurrent workers never process the same game twice.
- If a worker crashes, the next run **reclaims stale claims after 1 hour** (`CLAIM_TIMEOUT_SECONDS = 60 * 60`). Claims with missing/unparseable timestamps are reclaimed immediately.
- On failure or missing inputs, games are **restored to the stage's input status** rather than left dangling.

## Stage details and thresholds

1. **Find (agentic):** search priority 1j1ju.com → publisher site → Google → BGG files page. BGG blocks automated PDF downloads, so manual download into `source_pdfs/<slug>-rules.pdf` is a documented fallback.
2. **Download:** HTTP fetch of `pdf_url`; a PDF is valid only if ≥ **10 KB** and starts with `%PDF` magic bytes.
3. **Extract:** PyMuPDF primary, `--method pdfplumber` fallback for table-heavy layouts; cleans headers/footers/page numbers; output to `extracted/<slug>-rules.txt`. For garbled output, `CLAUDE.md` documents rendering pages to PNG for visual reading by Claude.
4. **Summarize:** Anthropic API call (`claude-sonnet-4-20250514`, `max_tokens=8192`) with a system prompt enforcing precision ("include all exact numbers… do not invent rules… when in doubt, quote the original text"). Skips extracted text < **500 chars**. Output is the full rules file including frontmatter, written verbatim to `rules/<slug>.md`.
5. **Quality check:** see PRD-04.

## Bulk research mode (parallel subagents)

For adding many games at once, the `/research-games` skill bypasses the staged batch pipeline:
1. `scripts/import_games.py --dry-run --output candidates.txt` reconciles against the sibling `boardgame-database` (~3,880 games) and emits `Name (bgg_id)` lines.
2. `scripts/prepare_research.py` checks slug collisions, registers everything (`status: queued`), and emits batch JSON.
3. The skill dispatches parallel subagents (defaults per spec: batch-size 80, 3 concurrent) that each find/extract/summarize their batch.
4. `scripts/collect_results.py` parses `RESULTS_START/RESULTS_END` blocks from subagent output and applies status updates serially.
5. `scripts/rebuild_index.py` regenerates `index.md`.

This mode produced the bulk of the catalog (commits record 57, 156, 123, and 163 games added per run).

## Current funnel state (as of 2026-06-10)

```
2,122 registered ──► 435 not_found (20.5%)  ← acquisition is the bottleneck
                ──► 3 queued · 3 downloaded · 40 extracted (in-flight/stalled)
                ──► 1,616 summarized ──► 6 validated · 19 flagged
                                     └─► 1,610 never quality-checked  ← quality debt
```

Plus drift: 26 rules files with no registry entry; 20 summarized/validated entries with no rules file.

## Open questions & needs-review items

- [OPEN QUESTION: retry policy for the 435 `not_found` games — the docs say "query `not_found` to retry older misses," but there is no schedule, prioritization, or notes-driven triage.]
- [NEEDS REVIEW: run the quality_check stage across the 1,610-game backlog; the calibration phase (manual review of the first 20–30) was designed but apparently never completed — only 6 games are `validated`.]
- [OPEN QUESTION: the in-flight 3 downloaded / 40 extracted games appear stalled — resume or re-queue?]
- [NEEDS REVIEW: `searching` status is defined but never set by any code path — either wire it into the find stage or remove it.]
- [NEEDS REVIEW: re-extraction/re-summarization is undefined — there is no versioning story for when a better PDF or model becomes available; `extracted_date`/`summarized_date` exist in frontmatter but nothing compares them.]
- [OPEN QUESTION: cost controls — batch summarization calls the Anthropic API per game with no budget cap, token accounting, or dry-run estimate.]
