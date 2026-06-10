# PRD-02 — Listings & Inventory

> **Grounding note:** **No listings or inventory code exists in this repository.** There are no seller, buyer, price, or listing entities; the only "auction" references are game mechanics inside QE test fixtures (`tests/test_quality_check.py`). This PRD is therefore a structured set of decisions-to-make, anchored to the one thing that does exist: the catalog every listing must bind to. Everything below is [INFERRED] unless it cites a file.

## How sellers create and manage listings

[OPEN QUESTION: the entire seller experience is undefined — no user accounts, auth, or seller model exists anywhere in the codebase.]

What the codebase *does* contribute to listing creation [code-backed]:
- **Game selection can reuse the registration flow.** `scripts/bgg.py:search_game()` already implements name → BGG candidate list (id, name, year); the same interaction pattern (see `find_rulebook.py`'s interactive `--select`) maps directly to "which game are you selling?"
- **Structured metadata auto-fill.** Once a `bgg_id` is chosen, `get_game_details()` supplies `player_count`, `play_time`, `designer`, `year` — listing forms never need free-text game data.
- **Completeness checklists for free.** Every summarized game's rules file contains a Components section with exact piece counts (e.g. Concordia: "110 wooden pieces in 5 player colors… 72 cards total"). A listing flow could render this as a per-component completeness checklist. [INFERRED — promising but unbuilt; would require parsing the Components markdown]

## Condition grading system

[OPEN QUESTION: no condition grading exists. Industry conventions (BGG GeekMarket uses New / Like New / Very Good / Good / Acceptable) are a reasonable default, but nothing in this repo encodes one. Decision needed: scale granularity, whether component-level completeness is separate from box/cosmetic condition, and whether photos are required per grade.]

A precedent worth noting from the existing system [code-backed, analogous]: the pipeline already practices **tiered quality with human escalation** — automated checks (`scripts/quality_check.py`) auto-accept to `validated` or escalate to `flagged` with `review_notes`. The same auto-check + human-review pattern could govern listing quality (e.g., flag listings whose claimed components contradict the catalog's Components list).

## Pricing model

[OPEN QUESTION: nothing in the code implies fixed price, best-offer, or auction. The Product Vision tentatively excludes auctions pending a decision. Inputs that exist for price guidance: none — there is no price history, no BGG market data integration. The BGG XML API2 client could be extended, but GeekMarket pricing is not exposed via XML API2.]

## How a listing links to the catalog data model

This is the part the codebase genuinely answers [code-backed foundation, linkage itself INFERRED]:

- A Listing must reference a **`bgg_id`** — the proven canonical key (0 duplicates across 2,122 entries, dedup enforced in `scripts/registry.py:add_game()`).
- The listing's public page can deep-link the rules summary at `rules/{slug}/` — the slug contract is already public API for the AI-prompt use case.
- Expansion listings inherit the `base_game_bgg_id` link, enabling "frequently sold together" and bundle displays via `find_expansions()`.
- **Gap:** listings for *editions* can't be expressed — the catalog has no Edition entity (see PRD-01). Until one exists, listings can only say "Concordia," not "Concordia, PD-Verlag printing." The `rulebook_version` field shows the system already knows editions matter. [NEEDS REVIEW: sequence Edition entity before or with listings MVP]
- **Gap:** ~20% of the catalog (435 `not_found` games) has registry metadata but no rules summary; listings against these games lose the rules-attached differentiator but should still be allowed. [INFERRED]

## Listing lifecycle states

[OPEN QUESTION: no listing states exist.] The repository does, however, contain a directly reusable **state-machine pattern** [code-backed, analogous]: the pipeline's status flow with atomic claiming —

- Explicit enum of states including transient "claimed" states (`downloading`, `summarizing`…) with `claimed_at` timestamps
- Atomic claim-before-work (`claim_games_by_status()`), stale-claim reclamation after 1 hour, and restore-on-failure semantics
- Terminal vs retryable state classification (CLAUDE.md: retryable `pending`/`not_found`; terminal `validated`/`flagged`)

A listing lifecycle (e.g. `draft → active → reserved → sold / expired / withdrawn`, with `reserved` as the claimed-with-timeout analog of `downloading`) should adopt the same discipline: every transient state has an owner and a timeout, every failure restores to a retryable state. [INFERRED — pattern transfer, not existing behavior]

## Inventory

[OPEN QUESTION: single-copy listings vs multi-copy inventory for store-like sellers is undecided; nothing in the code hints either way. The flat-file storage decision ("can add SQLite later if scaling up") will not survive concurrent marketplace writes — `fcntl.flock` on one YAML file is single-host only. A real datastore is a prerequisite for listings.] [NEEDS REVIEW: storage migration is the first engineering decision of the marketplace track]
