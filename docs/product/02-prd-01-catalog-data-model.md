# PRD-01 — Catalog & Data Model

The catalog layer is in production use by the pipeline; everything here is code-backed unless marked otherwise.

## The game hierarchy

The catalog uses a **single-layer `Game` entity with an expansion self-reference** — not a Works/Editions/Items hierarchy:

```
Game (games.yaml entry, keyed by bgg_id)
 └── Game with base_game_bgg_id → its base Game   (expansion)
```

- One registry entry per game in `games.yaml` (2,122 entries).
- Expansions are ordinary entries plus `base_game_bgg_id: <int>` pointing at the base game's `bgg_id`. Helpers exist: `find_expansions(path, base_bgg_id)` and `find_base_game(path, bgg_id)` in `scripts/registry.py:190-204`.
- Expansion records validate against a different section template (`EXPANSION_SECTIONS` in `scripts/validate.py:45-52`) and render indented under their base game with a `↳` prefix in `index.md`.

**Edition layer — absent but seeded.** The only edition-awareness is the free-text `rulebook_version` frontmatter field on rules files (e.g. `"PD-Verlag / Rio Grande Games Edition"` on Concordia). Nothing parses or indexes it. This matters when rulebooks differ across printings — a summary is faithful to *one specific rulebook*, and the model can't currently express which games have multiple circulating versions. [OPEN QUESTION: is one summary per game (latest printing) the policy, or should major editions get separate entries? BGG models versions as separate objects, but `scripts/bgg.py` requests only `type=boardgame` things and never fetches versions.]

**Game families** (e.g. the Catan family) are representable only transitively through `base_game_bgg_id`. BGG's `boardgamefamily` link type is not parsed by `parse_game_details()` — only `boardgamedesigner` links are read. [OPEN QUESTION: are families needed for browse/dedup, or is expansion-linkage sufficient?]

## How games are identified and sourced

Three identifiers coexist (a known integrity risk):

| Key | Role | Where enforced |
|---|---|---|
| `bgg_id` (int) | Canonical identity; dedup key | `add_game()` skips existing `bgg_id` (`scripts/registry.py:99-108`); verified 0 duplicates across 2,122 entries |
| `name` (str) | Write key for updates | `update_game()` / `update_status()` match case-insensitively on name |
| `slug` | Filesystem + URL key | `slugify()` (`re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")`) — duplicated in at least 6 scripts; collisions checked only in `prepare_research.py` |

[NEEDS REVIEW: converge writes on `bgg_id`, persist `slug` on the registry entry, and deduplicate the six `slugify()` copies into one module.]

**Sourcing is both BGG-driven and manual:**
- **BGG XML API2** (`scripts/bgg.py`): `/search` (name → candidates with id/name/year) and `/thing` (id → primary `name`, `player_count` as `"min-max"`, `play_time` as `"min-max min"`, `designer` comma-joined, `year`). Auth via `BGG_API_TOKEN` bearer header. Note: `year` is fetched but never written to the registry.
- **Bulk import** from the sibling `boardgame-database` project (`scripts/import_games.py`): matches on `bgg_id` first, case-insensitive name fallback; **entries without a bgg_id are skipped** — BGG identity is mandatory.
- **Manual entry**: the single-game flow in `CLAUDE.md` (`find_rulebook.py --bgg-id <ID>` to skip interactive search).
- **Rulebook PDFs** sourced in priority order: 1j1ju.com → publisher site → Google → BGG files page (scraped HTML via `scripts/bgg_files.py`, since the files page is JS-rendered; BGG also blocks automated downloads, so manual download is the documented fallback).

## Canonical data fields per layer

### Layer 1 — Game (registry, `games.yaml`)
`name`, `bgg_id`, `status` (14-value pipeline enum), `designer`, `player_count`, `play_time`, `pdf_url`, `notes`, `base_game_bgg_id`, `claimed_at` (transient), `review_notes`.

### Layer 2 — RulesSummary (`rules/<slug>.md`)
Frontmatter: `title`, `bgg_id` (required — `scripts/validate.py:19`), `player_count`, `play_time`, `designer`, `source_pdf`, `extracted_date`, `summarized_date`, `rulebook_version`, `base_game_bgg_id` (expansions only).
Body: 8 fixed `##` sections for base games (Overview, Components, Setup, Turn Structure, Actions, Scoring / Victory Conditions, Special Rules & Edge Cases, Player Reference); 6 for expansions (Overview, New Components, Setup Changes, Rule Changes, Special Rules & Edge Cases, Player Reference).

### Layer 3 — Provenance artifacts
- `extracted/<slug>-rules.txt` — raw cleaned text, tracked for diffability (1,015 files)
- `source_pdfs/<slug>-rules.pdf` — gitignored; validity = ≥ 10 KB + `%PDF` magic bytes
- `pdf_url` on the registry entry is the intended permanent provenance, but only 19 of 2,122 entries retain one — most provenance is currently discarded after download. [NEEDS REVIEW: always retain `pdf_url`]

## Expansions, promos, and game families

- **Expansions: modeled.** `base_game_bgg_id` + dedicated validation sections + indented index display. **Known inconsistency:** 8 rules files carry `base_game_bgg_id` in frontmatter but only 2 registry entries do — the two stores disagree. [NEEDS REVIEW: pick one authority; the registry is the natural choice since `find_expansions()` reads it.]
- **Promos/scenarios: not formally modeled.** Scenario-type rules files exist (`catan-scenario-crop-trust.md`, `catan-scenarios-frenemies.md`) and reuse the expansion frontmatter. [OPEN QUESTION: are promos/scenarios just expansions, or a distinct type? `import_games.py --type boardgame` shows the upstream CSV has a type column that could carry this.]
- **Families: not modeled** (see hierarchy section).

## Search/indexing considerations visible in the code

- **The slug-URL contract is load-bearing.** `index.md` instructs AI assistants to fetch `https://jonnyallred.github.io/boardgame-rules/rules/{slug}/` directly — slugs are a public API. Renaming a game breaks inbound links and saved AI prompts. Slugs must be treated as immutable once published.
- **Browse index is fully regenerated, never patched** — `generate_index.py` / `rebuild_index.py` rebuild from `rules/*.md` frontmatter. Two overlapping implementations exist. [NEEDS REVIEW: consolidate]
- **Lookup today is grep-based**: the `rules-lookup` skill Globs `rules/<slug>*.md` and Greps keywords. There is no inverted index or embeddings, although the original design doc names "RAG/embedding pipelines" as a primary consumer.
- **Faceted metadata exists** for player count, play time, and designer in both registry and frontmatter — but as display strings (`"2-5"`, `"45-90 min"`), not parsed numbers (see PRD-03).
