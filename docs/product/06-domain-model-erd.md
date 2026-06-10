# Domain Model & ERD Description

All entities below exist in the codebase today (file-backed, no database), except where explicitly marked as implied-but-unmodeled.

## Entities

### Game (registry entry)
The root catalog entity; one YAML dict per game in `games.yaml` (2,122 rows). Purpose: identity, BGG linkage, and pipeline state.
Key fields: `name` (unique case-insensitively), `bgg_id` (canonical id, unique, required — `add_game()` dedups on it), `status` (14-value pipeline enum), `designer`, `player_count` (string range `"2-5"`), `play_time` (string range `"45-90 min"`), `pdf_url` (19/2,122 retain it), `notes`, `base_game_bgg_id` (self-reference, expansions only), `claimed_at` (transient worker claim), `review_notes` (quality-check failures).

### RulesSummary
The product artifact: `rules/<slug>.md` (1,649 files), Markdown + YAML frontmatter, published as a page at `rules/{slug}/`.
Fields: `title`, `bgg_id` (required), `player_count`, `play_time`, `designer`, `source_pdf`, `extracted_date`, `summarized_date`, `rulebook_version` (free-text edition marker — the system's only edition awareness), `base_game_bgg_id` (8 files). Body: fixed validated sections (8 base / 6 expansion).

### ExtractedText
`extracted/<slug>-rules.txt` (1,015 files). Raw cleaned PDF text; tracked in git for diffability; the summarizer's input (must be ≥ 500 chars; quality gate requires ≥ 2,000 bytes).

### SourcePDF
`source_pdfs/<slug>-rules.pdf`. Gitignored; validity = ≥ 10 KB + `%PDF` magic bytes. Effectively ephemeral — provenance is meant to live in `pdf_url` but is usually dropped.

### IndexEntry
A generated row in `index.md` (name, players, time, designer, link). Not independently stored — fully derived from RulesSummary frontmatter on each regeneration.

### Candidate
A line `Name (bgg_id)` in `candidates*.txt`; staging records reconciled from the sibling `boardgame-database` project, consumed by `prepare_research.py`/`add_game()`.

## Textual ERD

```
  Game ───────────────┬──< Game (expansions)         via base_game_bgg_id → bgg_id  (self-ref, 1:N)
   │ bgg_id (PK)      │
   │ name (alt key)   └── helpers: find_expansions(), find_base_game()
   │ slug (derived, URL/file key — never stored)
   │
   ├── 1 : 0..1 ── RulesSummary      join: slugify(Game.name) == filename ; frontmatter.bgg_id
   ├── 1 : 0..1 ── ExtractedText     join: slugify(Game.name) + "-rules.txt"
   ├── 1 : 0..1 ── SourcePDF         join: slugify(Game.name) + "-rules.pdf"   (ephemeral)
   └── 1 : 0..1 ── IndexEntry        derived from RulesSummary frontmatter

  Candidate ── 1 : 0..1 ── Game      via add_game(name, bgg_id) during registration
```

Reading the chain: *a Game (registry entry) has at most one RulesSummary, produced from one ExtractedText, extracted from one SourcePDF* — a strictly linear provenance chain per game, joined throughout by the derived slug.

## Many-to-many relationships and how they are resolved

**There are none in the current model** — all relationships are 1:N or 1:0..1. Two places where reality is M:N but the model flattens it:

- **Game↔Designer is denormalized** — `designer` is a comma-joined string ("Bruno Cathala, Corentin Lebrat"), not a join to a Designer entity. Designer-based browse/filter would require splitting it. [NEEDS REVIEW if designer facets are wanted]
- **Expansion→base is N:1, not M:N** — an expansion points to exactly one base game. Cross-compatible expansions (usable with several base games) are inexpressible. [OPEN QUESTION: acceptable limitation?]

## Joins, keys, and integrity caveats

- All file joins go through the **derived slug**, recomputed from `name` by 6+ duplicated `slugify()` implementations. Slug is never stored; a rename silently orphans the game's files and breaks its published URL.
- Writes are keyed by case-insensitive `name` (`update_game`, `update_status`) while identity is `bgg_id` — two different keys for the same record.
- Verified current integrity: 0 duplicate `bgg_id`s, names, or slugs — but **26 rules files have no registry entry and 20 summarized/validated entries have no rules file**, and the expansion link disagrees between stores (8 frontmatter vs 2 registry). No referential integrity is enforced anywhere; a reconciliation/lint script is the cheapest near-term fix. [NEEDS REVIEW]

## Entities implied by the code but not formally modeled

- **Edition/Printing** — implied by `rulebook_version` and by `source_pdf`/`pdf_url` pointing at one specific printing's rulebook; needed if the catalog ever distinguishes versions (PRD-01 open question).
- **Designer** — implied by the comma-joined `designer` strings and BGG's `boardgamedesigner` links.
- **ComponentManifest** — implied by the validated Components section in every rules file (exact piece counts), currently prose rather than data.
- **PipelineJob / Claim** — implied by transient statuses + `claimed_at`; currently squashed into the Game record itself rather than modeled as a separate work-queue entity.
- **ReviewTask** — implied by `flagged` + `review_notes`; there is a backlog (19 flagged games) but no entity or tooling for working it.
- **Family/Category/Mechanic** — implied by BGG's link taxonomy, which the client deliberately ignores today.
