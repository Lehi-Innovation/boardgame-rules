# Product Vision

## What this product is and who it's for

A **board game rules database**: structured, precision-focused rules summaries for 1,600+ board games, produced by a semi-automated pipeline and published as a static site (`https://jonnyallred.github.io/boardgame-rules/`) designed to be **read by AI assistants at runtime**.

The landing page states the value proposition directly [code-backed, `index.md`]: *"AI-friendly rules summaries for board games. Use these with Claude, ChatGPT, or any AI assistant to get instant rules answers — including via voice."*

**Primary audiences** (from the design doc's consumer list and the shipped UX):
1. **Players at the table** — paste the provided prompt into Claude/ChatGPT (including voice mode on mobile), then ask rules questions hands-free mid-game. The site's predictable URL contract (`rules/{slug}/`) lets any web-fetching assistant pull exactly the right page.
2. **Claude (direct context)** — the repo's own skills: `/game <name>` loads a summary for conversational Q&A; `/rules <game>: <question>` runs a tiered deep lookup.
3. **RAG/embedding pipelines** — named as a primary consumer in `docs/plans/2026-03-02-boardgame-rules-db-design.md`. [INFERRED as future scope — no embedding code exists yet]
4. **Humans as standalone reference** — readable Markdown with a fixed section structure and a Player Reference quick-sheet per game.

## The core problem it solves

Mid-game rules questions are currently answered by: digging through a PDF rulebook, searching scattered BGG forum threads, or asking an LLM that **hallucinates rules from training data**. This product gives assistants **ground truth at answer time**:

- Summaries preserve *all* edge cases, exact numbers, thresholds, and scoring tables — the system prompt and project docs repeat the same principle: **"precision over brevity — AI can always summarize down; it can't recover lost detail."** [code-backed, `scripts/summarize.py:SYSTEM_PROMPT`]
- A fixed, machine-validated section structure (Overview → … → Player Reference) makes summaries scannable by humans and reliably parseable by machines. [code-backed, `scripts/validate.py`]
- When the summary itself can't answer, the `rules-lookup` skill escalates through the raw extracted rulebook, then BGG forums, then clearly-labeled intuition — and **feeds what it learned back into the summary via an auto-created PR**, so the database self-improves with use. [code-backed, `.claude/skills/rules-lookup/SKILL.md`]

## North star metric

[OPEN QUESTION: no metrics or analytics exist anywhere in the repo. The pipeline's implicit success measure is **validated catalog coverage** — games whose summaries passed the quality gate. Current funnel: 2,122 registered → 1,649 rules files → 1,616 `summarized` → only 6 `validated` (the quality stage has barely run). Candidate north stars: (a) count of validated summaries, (b) rules questions answered correctly from Tier 1 (the summary alone), (c) site fetches by AI assistants. NEEDS REVIEW: pick one.]

## What makes this different

1. **Built for AI consumption, not page views.** The recommended usage is literally a system prompt; URLs are computable from game names (`slugify(name)`); structure is enforced by validators rather than left to authors.
2. **Precision-first summaries.** Most rules-reference sites paraphrase; this pipeline's prompt forbids omitting edge cases and instructs "when in doubt, quote the original text."
3. **Pipeline scale with quality gates.** Four-stage batch pipeline (download → extract → summarize → quality-check) with atomic work-claiming, crash recovery, and an auto-accept/flag quality tier — designed to scale to thousands of games (already at 2,122 registered, grown from ~22 in March 2026).
4. **Self-healing content loop.** Q&A escalations automatically open PRs that improve the summaries, with provenance and confidence labels ("unverified" for intuition-sourced additions).
5. **Expansion-aware catalog.** Expansions are first-class records linked to their base game (`base_game_bgg_id`) with their own validated section template.

## What it explicitly is NOT

- **Not a marketplace.** No buying, selling, listings, or transactions — confirmed product scope. The product is reference content.
- **Not a PDF mirror.** Source rulebooks are deliberately gitignored and never redistributed; only derived summaries and extracted text are published. [code-backed, `.gitignore`, design doc decision]
- **Not a BGG replacement.** BGG remains the upstream authority for game identity (`bgg_id`) and metadata; the pipeline consumes its XML API2 and files pages.
- **Not a strategy/review site.** Content is rules only — no ratings, session reports, or buying advice.
- **Not an app.** There is no server or frontend application; the deliverable is files plus a static site. ("Flat files over SQLite… files are the product.")

## Risks visible from discovery

- **Licensing**: summaries derive from publisher PDFs with no recorded permission policy. [NEEDS REVIEW: document a takedown/permission stance]
- **Quality debt**: 1,610 summarized games have never been quality-checked; 19 flagged games have no review workflow. The product's accuracy promise rests on a gate that is currently almost entirely unexecuted.
- **Coverage ceiling**: 435 games are `not_found` (~20% of the registry) — PDF acquisition is the bottleneck stage.
- **Catalog integrity**: registry↔filesystem drift and the three-key identity model (name/bgg_id/slug) could silently break the URL contract that AI consumption depends on.
