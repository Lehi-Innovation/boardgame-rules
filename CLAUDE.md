# Boardgame Rules Database

## Project Structure
- `games.yaml` — master game registry (name, bgg_id, status)
- `games.json` — published machine-readable catalog manifest (regenerate with `python -m scripts.generate_manifest`)
- `source_pdfs/` — downloaded PDFs (gitignored)
- `extracted/` — raw extracted text from PDFs (published on the site as the authoritative fallback source)
- `rules/` — final structured markdown files with YAML frontmatter
- `scripts/` — Python pipeline tools
- `mcp_server/` — MCP server exposing the corpus to MCP clients (list_games, get_rules, search_rulebook, report_rule_error)
- `index.md` — GitHub Pages landing page (game list + usage instructions)
- `_config.yml` — Jekyll config for GitHub Pages
- `.github/` — rule-error issue form + automated triage workflow

## Pipeline

### Adding a Single Game (Manual)

- [ ] Run `python -m scripts.find_rulebook "Game Name" --bgg-id <ID>` to fetch metadata from BGG and register the game. Use `--bgg-id` to skip interactive search (find the ID on the game's BGG page URL). The script will attempt to download the PDF, but BGG blocks automated scraping — you'll likely need to download manually.
- [ ] Download the rulebook PDF manually. Check these sources in order: 1j1ju.com (good coverage of manuals), BGG's files page, or the publisher's site. Save it to `source_pdfs/<slug>-rules.pdf`. Tip: create the empty file first with `touch source_pdfs/<slug>-rules.pdf` so the user can "Save As" directly over it with the correct name.
- [ ] Run `python -m scripts.extract_pdf source_pdfs/<slug>-rules.pdf` to extract text. Use `--method pdfplumber` if tables are mangled. Review `extracted/<slug>-rules.txt` for quality.
- [ ] If extracted text has gaps or garbled tables, render the PDF pages to images for visual inspection: `python -c "import fitz; doc=fitz.open('source_pdfs/<slug>-rules.pdf'); [doc[i].get_pixmap(matrix=fitz.Matrix(2,2)).save(f'/tmp/<slug>-p{i+1}.png') for i in range(len(doc))]"` then use the Read tool on the resulting PNGs to read tables and diagrams directly.
- [ ] Summarize interactively with Claude Code: read the extracted text, produce `rules/<slug>.md` following the template format. Precision over brevity — keep all edge cases and exact numbers.
- [ ] Run `python -m scripts.validate` to check the rules file has all required frontmatter and sections.
- [ ] Run `python -m scripts.verify_summary rules/<slug>.md` to semantically fact-check the summary against the extracted text (requires ANTHROPIC_API_KEY). Fix MAJOR findings before publishing, or run the batch form with repair: `python -m scripts.verify_summary --batch`.
- [ ] Run `python -m scripts.stamp_verification rules/<slug>.md` to stamp the verification banner and feedback links into the page.
- [ ] Run `python -m scripts.generate_index` to rebuild `index.md` and `python -m scripts.generate_manifest` to rebuild `games.json`.
- [ ] Commit the extracted text, rules file, updated `games.yaml`, `index.md`, and `games.json`.

### Batch Processing (Scalable Pipeline)

**Import games from boardgame-database:**
```bash
python -m scripts.import_games /path/to/boardgame-database/games/ \
  --master-csv /path/to/boardgame-database/master_list.csv \
  --limit 100
```

**Find PDFs (interactive with Claude Code + Playwright):**
See "Batch PDF Finding" section below.

**Process pipeline stages:**
```bash
# Download all found PDFs
python -m scripts.process_batch --stage download --limit 50

# Extract text from downloaded PDFs
python -m scripts.process_batch --stage extract --limit 50

# Summarize extracted text via Claude API
python -m scripts.process_batch --stage summarize --limit 20

# Quality check summarized rules (structural gate)
python -m scripts.process_batch --stage quality_check --limit 20

# Semantically verify against extracted sources (accuracy gate, Claude API,
# auto-repairs fixable findings; PASS/MINOR -> verified, MAJOR -> flagged)
python -m scripts.process_batch --stage verify --limit 20

# Check overall pipeline status
python -m scripts.process_batch --status
```

**Status flow:** `pending → found → downloaded → extracted → summarized → validated → verified`

`validated` means **structurally complete only** (sections present, not thin).
`verified` means the summary was fact-checked against its extracted source.
Only `verified` should be treated as trustworthy.

**Retryable states:** `pending`, `not_found`

**Terminal states:** `verified`, `flagged`

**Transient claimed states:** `downloading`, `extracting`, `summarizing`, `quality_checking`, `verifying`

`process_batch` claims work atomically before running a stage so concurrent workers do not process the same game twice. Claimed jobs carry a `claimed_at` timestamp in `games.yaml`. If a worker crashes, the next batch run will automatically reclaim stale claimed jobs after 1 hour.

### Bulk Research (Parallel Subagents)

Generate a candidates file from boardgame-database, then bulk-research with parallel subagents:

1. Generate candidates: `python -m scripts.import_games ~/projects/boardgame-database/games/ --master-csv ~/projects/boardgame-database/master_list.csv --dry-run --type boardgame --limit 100 --output candidates.txt`
2. Run the skill: `/research-games candidates.txt --batch-size 20 --parallel 3`
3. Review results — check flagged games for issues

The skill registers all games upfront, dispatches subagents to find PDFs / extract / summarize, then consolidates results into `games.yaml` and `index.md`.

**Helper scripts for the bulk research workflow:**

```bash
# Step 1: Generate candidates (already exists)
python -m scripts.import_games ~/projects/boardgame-database/games/ \
  --master-csv ~/projects/boardgame-database/master_list.csv \
  --dry-run --type boardgame --limit 200 --output candidates.txt

# Step 2: Register games, check slug collisions, output batch JSON
# Prints BATCH1:{json} BATCH2:{json} etc. to stdout (status to stderr)
python -m scripts.prepare_research candidates.txt --batch-size 50 --batches 4

# Step 3: Dispatch subagents (done by /research-games skill or manually)

# Step 4: Collect subagent results and update games.yaml
# Parses RESULTS_START/RESULTS_END blocks from subagent output files
python -m scripts.collect_results batch1_output.txt batch2_output.txt

# Step 5: Rebuild index.md from all rules/ files
python -m scripts.rebuild_index
```

### Batch PDF Finding (Interactive)

To find rulebook PDFs for pending or retryable games using Playwright browser tools:

1. Check queue: `python -m scripts.process_batch --status`
2. Ask Claude Code: "Find rulebook PDFs for the next 20 pending games"
3. Claude searches (in priority order): 1j1ju.com, Google, BGG files page
4. For each game found, update registry: `status: found`, `pdf_url: "..."`
5. For games not found: `status: not_found`, `notes: "reason"`
6. Then run: `python -m scripts.process_batch --stage download`

Queue management helpers:
```python
from scripts.registry import get_games_by_status, update_game

# Get next batch
games = get_games_by_status("games.yaml", "pending", limit=20)

# Record a found PDF
update_game("games.yaml", "Agricola", status="found",
            pdf_url="https://1j1ju.com/rules/agricola-en.pdf")

# Record not found (can be retried later)
update_game("games.yaml", "Obscure Game", status="not_found",
            notes="No English rulebook found")
```

To retry older misses, query `not_found` instead of `pending`.

### Reclaim Testing

To test stale-claim recovery on a scratch registry:

1. Copy the registry: `cp games.yaml /tmp/games-test.yaml`
2. Edit one record into a transient state such as:
   - `status: summarizing`
   - `claimed_at: "2026-04-01T00:00:00+00:00"`
3. Run the matching stage:
   - `python -m scripts.process_batch --registry /tmp/games-test.yaml --stage summarize --limit 1`
4. The stale claimed record should be reclaimed and processed.

## Semantic Audit

The automated `quality_check` gate verifies structure only; a separate **semantic
audit** fact-checks each summary against its extracted source text (~half of
gate-passing summaries contain table-misleading errors). Workflow:

- Queue/state: `docs/quality/semantic-audit-manifest.json` (batches) and
  `docs/quality/semantic-audit-results.yaml` (verdicts); evidence in
  `docs/quality/audit-findings/<batch>.md`.
- Toolkit: `python -m scripts.audit status|next|prefilter|record` (see module
  docstring). `record` auto-flags MAJOR games in `games.yaml`.
- Run waves with `/audit-rules [--waves N] [--model haiku|sonnet]` — dispatches
  one low-cost subagent per batch following
  `.claude/skills/audit-rules/SKILL.md`, then records, commits, and pushes.
- Verdicts: PASS / MINOR / MAJOR. MAJOR = would mislead players at the table;
  those games need re-summarization from the extracted text (see
  `docs/quality/2026-06-10-semantic-audit.md` for the error taxonomy).
- For NEW summaries, the same checklist runs inside the pipeline as the
  `verify` stage (`scripts/verify_summary.py`) with an automatic repair loop —
  the retroactive audit waves are for the pre-existing backlog.

### Independent Re-Audit (the second gate)

**A repairer cannot grade its own work.** The `verify` stage and the manual
repair passes have one agent both find an error and fix it, then call it
`verified` — with no independent check. A 2026-07-03 measurement (random
sample, then a full pass) found this over-claims: **~27–35% of "verified"
summaries still contained a MAJOR error** on independent re-audit. Treat any
self-graded `verified` as provisional — necessary but not sufficient.

The remedy is a three-stage pipeline run by **separate** agents —
**audit → repair (only if MAJOR) → re-verify (fresh auditor)** — so a repair
that didn't actually work is re-flagged instead of stamped `verified`. Only
games that pass the independent re-verify keep `verified`; the rest stay
`flagged` with the specific finding in `review_notes`. Re-run it over any set
of `verified` games as a standing second gate. See
`docs/quality/2026-07-03-independent-reaudit.md` for the method, the measured
residual rates, and why ~1/3 of the hardest games (OCR-degraded sources,
omitted subsystems, invented mechanics) resist automated fixing.

## Verification & Trust Stamping

Every rules file carries `verification` / `verification_date` frontmatter and
a visible banner block (between `<!-- verification:begin/end -->` markers)
with a rulebook-text link and a report-an-error link. States:

| State | Meaning | Index badge |
|---|---|---|
| `verified` | audit/verify PASS | ✅ |
| `minor_issues` | audit MINOR — small omissions, play unaffected | ✅ |
| `inaccurate` | audit MAJOR — known table-misleading errors | ❗ |
| `unverified` | not yet fact-checked; source text exists | ⚠️ |
| `unverifiable` | no extracted source text to check against | ⚠️ |

- Stamp after any audit recording or rules edit:
  `python -m scripts.stamp_verification [files...] [--update-registry]`
  (idempotent; `--update-registry` promotes audit-PASS games `validated → verified`).
- The stamper derives state from `docs/quality/semantic-audit-results.yaml` +
  presence of `extracted/<slug>-rules.txt`. The `verify` pipeline stage stamps
  automatically.
- After stamping, regenerate `index.md` (`python -m scripts.generate_index`)
  and `games.json` (`python -m scripts.generate_manifest`).

## Feedback Loop

- End users report wrong rules via the **Report a rules error** link on every
  page (prefilled `rule-error` issue form in `.github/ISSUE_TEMPLATE/`).
- The `rule-error-triage` workflow (`.github/workflows/rule-error-triage.yml`,
  requires `ANTHROPIC_API_KEY` repo secret) dispatches Claude with
  `.claude/skills/triage-rule-error/SKILL.md`: verify the report against the
  extracted text, fix-via-PR if confirmed, reply with evidence if not.
- Canonical rules sections may only contain claims verified against the
  extracted rulebook text. Forum/designer rulings go in a labeled
  `## FAQ & Rulings` section; pure inference is never written to any file
  (see `.claude/skills/rules-lookup/SKILL.md` tier rules).
- The corpus is also consumable via `mcp_server/` (see README) so mid-game
  Q&A clients get tiered lookup plus the `report_rule_error` tool.

## Rules File Format
YAML frontmatter (title, bgg_id, player_count, play_time, designer, source_pdf, extracted_date, summarized_date, rulebook_version, verification, verification_date) + Markdown body with sections: Overview, Components, Setup, Turn Structure, Actions, Scoring / Victory Conditions, Special Rules & Edge Cases, Player Reference. Optional: FAQ & Rulings (sourced rulings only). The verification banner block is machine-managed — edit via `scripts.stamp_verification`, not by hand.

## Expansions

Expansions are tracked as separate entries linked to their base game. The pipeline is the same as for base games, with two differences:

1. **Registry:** Add `base_game_bgg_id: <int>` to the expansion's `games.yaml` entry, pointing to the base game's BGG ID.
2. **Rules file:** Use expansion sections instead of base game sections:
   - Overview (what the expansion adds/changes)
   - New Components (new pieces, cards, boards)
   - Setup Changes (how setup differs from base game)
   - Rule Changes (modified or new mechanics)
   - Special Rules & Edge Cases
   - Player Reference

Frontmatter must include `base_game_bgg_id` to trigger expansion validation.

**Helper functions:**
```python
from scripts.registry import find_expansions, find_base_game

# Get all expansions for Catan (bgg_id=13)
find_expansions("games.yaml", 13)

# Find the base game for an expansion
find_base_game("games.yaml", 325)  # returns Catan entry
```

**Display:** In `index.md`, list expansions indented under their base game with `↳` prefix.

## Testing
```bash
source .venv/bin/activate
python -m pytest tests/ -v
```

## GitHub Pages Site
The rules are published at `https://jonnyallred.github.io/boardgame-rules/`. GitHub Pages builds automatically from the `main` branch using Jekyll. The `_config.yml` excludes non-site directories (scripts, source_pdfs, extracted, tests, etc.). When adding a new game, update `index.md` with the new entry in alphabetical order.

## Requirements
- Python 3.10+
- BGG API token in `.env` (register at https://boardgamegeek.com/applications)
- Anthropic API key in `.env` (for batch summarization)
- Virtualenv at `.venv/` — activate with `source .venv/bin/activate`
