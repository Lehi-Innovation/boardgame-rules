# Product Vision

> **Grounding note:** The existing repository implements a board game **rules catalog and content pipeline** — not a marketplace. This vision document describes the marketplace as a **new product layered on top of that existing catalog asset**. Statements about the catalog and rules content are code-backed; statements about marketplace functionality are direction-setting and marked [INFERRED]. [NEEDS REVIEW: confirm a marketplace is actually the intended product before this vision is socialized.]

## What this product is and who it's for

A peer-to-peer marketplace for buying and selling physical board games, built on top of an existing structured catalog of 2,122+ games (keyed to BoardGameGeek IDs) and 1,649+ precision rules summaries published at `https://jonnyallred.github.io/boardgame-rules/`. [INFERRED — marketplace layer]

**Primary audiences** [INFERRED]:
- **Board game owners** with shelves of played-once games who want a low-friction way to sell or trade.
- **Budget-conscious buyers** hunting for out-of-print titles, specific editions, or used copies at fair prices.
- **The existing audience of the rules site**: players who already use the catalog as an AI-powered rules reference at the table.

## The core problem it solves

The dominant incumbent venues for second-hand board games are the **BGG Marketplace / GeekMarket**, eBay, and Facebook groups. Their well-known weaknesses [INFERRED — from market knowledge, not this codebase]:

- **Weak catalog binding.** eBay and Facebook listings are free text; buyers can't reliably tell *which edition or printing* they're buying. BGG binds to its catalog but with dated UX.
- **No edition/printing precision.** Reprints with different components or rules revisions are conflated. Notably, this repo's own data model has the seed of a fix: the `rulebook_version` frontmatter field already records which printing a rules summary describes (e.g. "PD-Verlag / Rio Grande Games Edition" on Concordia).
- **Thin trust mechanics.** Condition grading is inconsistent and disputes are handled ad hoc.
- **No content gravity.** Incumbent marketplaces are destinations only when you already intend to buy. This product's existing rules summaries are useful *every game night*, creating recurring traffic that a marketplace can convert. This is the one differentiator that already exists in code.

## North star metric

[OPEN QUESTION: no analytics, metrics, or success criteria exist anywhere in the codebase. Candidate north stars for discussion: (a) completed transactions per month, (b) GMV, (c) % of rules-page visitors who view a listing. The existing pipeline's implicit metric is **catalog coverage** — games with a validated rules summary — currently 1,616 summarized but only 6 validated.]

## What makes this different

1. **Catalog-first listings** [code-backed foundation]: every listing binds to a canonical game record with a stable `bgg_id`, slug-based URL (`rules/{slug}/`), and structured metadata (`player_count`, `play_time`, `designer`). No free-text ambiguity.
2. **Rules attached to every listing** [code-backed foundation]: a buyer evaluating a used copy can read the full, precision-focused rules summary — Components list included — before buying. The Components sections (exact piece counts, e.g. Concordia's "110 wooden pieces in 5 player colors") give a natural checklist for completeness claims. [INFERRED — the linkage is an idea; no listing code exists]
3. **Expansion-aware structure** [code-backed foundation]: expansions are first-class records linked via `base_game_bgg_id`, so a marketplace can express "base game + both Quacks expansions" bundles accurately. [INFERRED — bundling itself]
4. **AI-native surface** [code-backed foundation]: the catalog is already designed to be consumed by LLMs via predictable URLs; the same contract could let assistants answer "find me a used copy of Concordia under $40." [INFERRED]

## What it explicitly is NOT

- **Not a rules-content replacement for BGG** — BGG remains the upstream source of game identity (`bgg_id`) and metadata; the pipeline consumes its XML API2 and files pages. [code-backed]
- **Not a publisher/retail storefront for new games.** [INFERRED scope boundary; OPEN QUESTION: confirm]
- **Not an auction house.** [OPEN QUESTION: pricing model is entirely undecided — see PRD-02. The only "auctions" in this repo are game mechanics in QE test fixtures.]
- **Not a digital/print-and-play distribution channel** — rulebook PDFs are deliberately gitignored and never redistributed; only derived summaries are published. A marketplace must preserve this stance. [code-backed]
- **Not a logistics company** — no shipping, warehousing, or escrow infrastructure exists or is implied anywhere. [OPEN QUESTION: shipping model]

## Risks visible from discovery

- **Licensing**: rules summaries derive from publisher PDFs with no recorded permission policy. Acceptable risk for a free reference site; materially different for a commercial marketplace. [NEEDS REVIEW: legal position before any commercialization]
- **Catalog integrity**: registry↔filesystem drift (26 orphan rules files, 20 missing files) and the three-key identity model (name/bgg_id/slug) must be hardened before listings depend on them.
- **Coverage gaps**: 435 games are `not_found` (no rulebook sourced) — the catalog can still anchor listings for these, but without the rules-content differentiator.
