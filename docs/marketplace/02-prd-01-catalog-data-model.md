# PRD-01 — Catalog & Data Model

This is the best-supported document in the suite: the catalog layer exists and is in production use by the rules pipeline. Marketplace-specific extensions are marked [INFERRED].

## The game hierarchy

The codebase does **not** use a Works / Editions / Items hierarchy. It uses a **single-layer `Game` entity with an expansion self-reference**:

```
Game (games.yaml entry, keyed by bgg_id)
 └── Game with base_game_bgg_id → its base Game   (expansion)
```

- One registry entry per game in `games.yaml` (2,122 entries).
- Expansions are ordinary entries plus `base_game_bgg_id: <int>` pointing at the base game's `bgg_id`. Helpers exist: `find_expansions(path, base_bgg_id)` and `find_base_game(path, bgg_id)` in `scripts/registry.py:190-204`.
- Expansion records validate against a different section template (`EXPANSION_SECTIONS` in `scripts/validate.py:45-52`) and render indented under their base game with a `↳` prefix in `index.md`.

**Edition layer — absent but seeded.** The only edition-awareness in the system is the `rulebook_version` frontmatter field on rules files (free text, e.g. `"PD-Verlag / Rio Grande Games Edition"`). Nothing parses or indexes it. A marketplace needs an Edition/Printing layer (a used 1995 Mayfair Catan ≠ Catan 25th Anniversary) — this is the largest catalog gap. [OPEN QUESTION: introduce an Edition entity keyed how? BGG models versions as separate "version" objects under a thing — the current BGG client (`scripts/bgg.py`) requests only `type=boardgame` things and does not fetch versions.]

**Item layer — absent.** Physical copies do not exist in the model at all; they belong to the Listings domain (PRD-02). [INFERRED]

**Game families** (e.g. "Catan family", "Quacks of Quedlinburg + expansions") are representable only transitively through `base_game_bgg_id`. BGG's `boardgamefamily` link type is not parsed by `parse_game_details()`. [OPEN QUESTION: are families needed for browse/dedup, or is expansion-linkage sufficient?]

## How games are identified and sourced

Three identifiers coexist (a known integrity risk — surface in any schema migration):

| Key | Role | Where enforced |
|---|---|---|
| `bgg_id` (int) | Canonical identity; dedup key | `add_game()` skips existing `bgg_id` (`scripts/registry.py:99-108`); verified 0 duplicates across 2,122 entries |
| `name` (str) | Write key for updates | `update_game()` / `update_status()` match case-insensitively on name |
| `slug` | Filesystem + URL key | `slugify()` (`re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")`) — duplicated in at least 6 scripts; collisions checked only in `prepare_research.py` |

**Sourcing is both BGG-driven and manual:**
- **BGG XML API2** (`scripts/bgg.py`): `/search` (name → candidates) and `/thing` (id → `name`, `player_count` as `"min-max"`, `play_time` as `"min-max min"`, `designer` comma-joined, `year`). Auth via `BGG_API_TOKEN` bearer header.
- **Bulk import** from the sibling `boardgame-database` project (`scripts/import_games.py`): matches on `bgg_id` first, case-insensitive name fallback; **entries without a bgg_id are skipped** — BGG identity is mandatory.
- **Manual entry** is supported implicitly (CLAUDE.md's single-game flow; `--bgg-id` flag to skip interactive search).
- **Rulebook PDFs** sourced in priority order: 1j1ju.com → publisher site → Google → BGG files page (scraped HTML, since the files page is JS-rendered — `scripts/bgg_files.py`).

## Canonical data fields per layer

### Layer 1 — Game (registry, `games.yaml`)
`name`, `bgg_id`, `status` (14-value pipeline enum), `designer`, `player_count`, `play_time`, `pdf_url`, `notes`, `base_game_bgg_id`, `claimed_at` (transient), `review_notes`.

### Layer 2 — RulesSummary (`rules/<slug>.md`)
Frontmatter: `title`, `bgg_id` (required — `scripts/validate.py:19`), `player_count`, `play_time`, `designer`, `source_pdf`, `extracted_date`, `summarized_date`, `rulebook_version`, `base_game_bgg_id` (expansions only).
Body: 8 fixed `##` sections for base games (Overview, Components, Setup, Turn Structure, Actions, Scoring / Victory Conditions, Special Rules & Edge Cases, Player Reference); 6 for expansions (Overview, New Components, Setup Changes, Rule Changes, Special Rules & Edge Cases, Player Reference).

### Layer 3 — Provenance artifacts
- `extracted/<slug>-rules.txt` — raw text, tracked for diffability (1,015 files)
- `source_pdfs/<slug>-rules.pdf` — gitignored; provenance survives only as `pdf_url` (kept on just 19 of 2,122 entries — most provenance is currently discarded). [NEEDS REVIEW: retain `pdf_url` permanently rather than only until download]

### Proposed marketplace extension [INFERRED — no code basis]
A marketplace would add: `Edition` (publisher, year, language, `rulebook_version` linkage, component manifest derived from the Components section) and `Item` (a physical copy: edition ref, condition, completeness, photos). Neither exists; see PRD-02 and the Domain Model doc.

## Expansions, promos, and game families

- **Expansions: modeled.** `base_game_bgg_id` + dedicated validation sections + indented index display. **Known inconsistency:** 8 rules files carry `base_game_bgg_id` in frontmatter but only 2 registry entries do — the two stores disagree. [NEEDS REVIEW: pick one authority; registry is the natural choice since `find_expansions()` reads it]
- **Promos: not modeled.** No promo concept anywhere. Closest signal: scenario-type rules files exist (`catan-scenario-crop-trust.md`, `catan-scenarios-frenemies.md`) using the expansion frontmatter. [OPEN QUESTION: are promos/scenarios just expansions, or a distinct type? `import_games.py --type boardgame` suggests the upstream CSV has a type column that could carry this.]
- **Families: not modeled** (see hierarchy section above).

## Search/indexing considerations visible in the code

- **The slug-URL contract is load-bearing.** `index.md` instructs AI assistants to fetch `https://jonnyallred.github.io/boardgame-rules/rules/{slug}/` directly — slugs are a public API. Renaming a game breaks inbound links and AI prompts. Any future schema must treat slugs as immutable once published. 
- **Browse index is fully regenerated, never patched** — `generate_index.py` / `rebuild_index.py` rebuild from `rules/*.md` frontmatter (note: two overlapping implementations exist [NEEDS REVIEW: consolidate]).
- **Lookup today is grep-based**: the `rules-lookup` skill Globs `rules/<slug>*.md` and Greps keywords. There is no inverted index, embeddings, or search service, although the original design doc names "RAG/embedding pipelines" as a primary consumer.
- **Faceted metadata already exists** for player count, play time, and designer in both registry and frontmatter — the obvious first facets for marketplace search (PRD-03).
