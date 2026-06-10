# Domain Model & ERD Description

Two clearly separated tiers: **entities that exist in the codebase today** (file-backed, no database) and **entities implied or required by the marketplace brief** (not modeled anywhere).

## Tier 1 — Existing entities (code-backed)

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
A line `Name (bgg_id)` in `candidates*.txt`; staging records from the sibling `boardgame-database` project, consumed by `prepare_research.py`/`add_game()`.

## Tier 2 — Marketplace entities [INFERRED — none exist in code]

**Edition** — a specific printing/version of a Game (publisher, year, language). Seeded only by the unparsed `rulebook_version` string. Required before listings can be edition-precise.
**Item** — a physical copy: Edition ref, condition grade, completeness vs the Components manifest, photos. [OPEN QUESTION: explicit Item entity vs folding into Listing for MVP]
**User / Seller / Buyer**, **Listing** (with lifecycle states), **Offer**, **Transaction/Order**, **Shipment**, **Review/Rating**, **Dispute** — all entirely unmodeled; see PRD-02/PRD-04 open questions before schema work.

## Textual ERD

```
EXISTING (file-backed)

  Game ───────────────┬──< Game (expansions)         via base_game_bgg_id → bgg_id  (self-ref, 1:N)
   │ bgg_id (PK)      │
   │ name (alt key)   └── helpers: find_expansions(), find_base_game()
   │ slug (derived, URL/file key)
   │
   ├── 1 : 0..1 ── RulesSummary      join: slugify(Game.name) == filename ; frontmatter.bgg_id
   ├── 1 : 0..1 ── ExtractedText     join: slugify(Game.name) + "-rules.txt"
   ├── 1 : 0..1 ── SourcePDF         join: slugify(Game.name) + "-rules.pdf"   (ephemeral)
   └──ND 1 : 0..1 ── IndexEntry      derived from RulesSummary frontmatter

PROPOSED (marketplace) [INFERRED]

  Game 1──N Edition 1──N Item 1──1 Listing N──1 Seller(User)
  Listing 1──N Offer N──1 Buyer(User)
  Listing 1──0..1 Transaction 1──0..1 Shipment
  Transaction 1──0..2 Review (buyer↔seller)
  Transaction 1──0..N Dispute
```

So in the proposed model: *a Listing sells one Item, which is a copy of one Edition, which is a printing of one Game* — the Works/Editions/Items pattern the brief anticipated, of which **only the top (Game) layer exists today**.

## Many-to-many relationships and how they are resolved

- **Existing model: there are none.** All relationships are 1:N or 1:0..1. Notably:
  - **Game↔Designer is stored denormalized** — `designer` is a comma-joined string ("Bruno Cathala, Corentin Lebrat"), not a join to a Designer entity. A real schema should split this into `Game N──M Designer`. [NEEDS REVIEW]
  - **Expansion→base is N:1, not M:N** — an expansion points to exactly one base game. Cross-compatible expansions (usable with several base games) are inexpressible. [OPEN QUESTION: acceptable limitation?]
- **Proposed M:N pairs** [INFERRED]: Game↔Designer (resolve via join table), Game↔Family/Category/Mechanic (if BGG taxonomy is adopted, PRD-03), Listing↔Item if bundle listings ("base + 2 expansions") are allowed — resolve via a ListingItem join entity. [OPEN QUESTION: are bundles in scope?]

## Joins, keys, and integrity caveats (code-backed)

- All file joins go through the **derived slug**, recomputed from `name` by 6+ duplicated `slugify()` implementations. Slug is not stored on the registry entry. A rename silently orphans files.
- Verified current integrity: 0 duplicate `bgg_id`s, names, or slugs — but **26 rules files have no registry entry and 20 summarized/validated entries have no rules file**, and the expansion link disagrees between stores (8 frontmatter vs 2 registry). No referential integrity is enforced anywhere; a reconciliation/linting script is the cheapest near-term fix. [NEEDS REVIEW]
- Writes are keyed by case-insensitive `name` while identity is `bgg_id` — converging on `bgg_id`-keyed writes (and persisting `slug`) is the first schema-hardening step for any database migration.

## Entities implied by the code but not formally modeled

- **Edition** — implied by `rulebook_version` and by `source_pdf`/`pdf_url` pointing at one specific printing's rulebook.
- **Designer** — implied by the comma-joined `designer` strings and BGG's `boardgamedesigner` links.
- **ComponentManifest** — implied by the validated Components section in every rules file (exact piece counts), currently prose rather than data.
- **PipelineJob / Claim** — implied by transient statuses + `claimed_at`; currently squashed into the Game record itself rather than a separate work-queue entity.
- **ReviewTask** — implied by `flagged` + `review_notes`; there is a backlog (19 flagged games) but no entity or tooling for working it.
