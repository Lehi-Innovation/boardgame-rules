# Document Generation Summary

## What was well-supported by the codebase

- **PRD-01 (Catalog & Data Model)** — strongest document. The Game entity, `bgg_id`-canonical identity, slug/URL contract, expansion self-reference (`base_game_bgg_id`), BGG sourcing flows, frontmatter schema, and validation rules are all read directly from working code (`scripts/registry.py`, `scripts/bgg.py`, `scripts/validate.py`) and verified against live data (2,122 entries, 1,649 rules files).
- **Discovery Summary** — fully evidence-based, including registry integrity statistics computed during discovery (0 duplicate ids/names/slugs; 26 orphan rules files; 20 missing rules files; 8-vs-2 expansion-link disagreement).
- **PRD-03 (Search & Discovery), current-state half** — the alphabetical browse index, slug-URL contract, grep-based tiered lookup, and existing facet fields are all code-backed.
- **Tier 1 of the Domain Model & ERD** — every existing entity, field, join, and integrity caveat is verified.
- **Process patterns cited in PRD-02/PRD-04** (state machine with atomic claims and timeouts; tiered quality with human escalation; calibration-before-automation) — real, tested code, offered as transferable patterns only.

## What was inferred with low confidence

- **The entire marketplace premise.** The brief's framing ("board game marketplace") has no support anywhere in the code, docs, plans, commit history, or skills. The Product Vision is written as "marketplace layered on the existing catalog asset," which is the only coherent reading — but it is an inference about intent, not a finding.
- **Competitive positioning** (BGG Marketplace/GeekMarket weaknesses) — from general market knowledge, not the repo.
- **All proposed marketplace mechanics**: listing↔catalog binding via `bgg_id`, components-as-completeness-checklist, expansion bundles, the proposed Edition/Item/Listing/Transaction entities, and the listing/transaction lifecycle sketches. These are design proposals anchored to real catalog structures, marked [INFERRED] throughout.
- **North star metric candidates** — no metrics of any kind exist in the repo.

## What is genuinely missing and needs human input

1. **Scope confirmation** — is a marketplace actually planned for/around this repo? Everything downstream depends on this. (Discovery Summary, Open Question 1)
2. **All of PRD-02's core decisions**: seller model, condition grading scale, pricing model (fixed/offers/auction), single-copy vs inventory, bundles.
3. **All of PRD-04's core decisions**: payment provider and escrow model, fee structure, shipping ownership, dispute policy, minimum trust/KYC stack.
4. **Edition strategy** — whether/how to add an Edition layer (BGG "versions" fetch is the obvious source); currently only the free-text `rulebook_version` hint exists.
5. **Storage migration** — flat YAML + `fcntl` locks cannot support multi-user marketplace writes; choice of database/search engine is the first engineering decision.
6. **Licensing position** on publisher-derived rules content in a commercial context.
7. **Catalog hygiene before any dependent product**: reconcile registry↔filesystem drift, unify the expansion-link authority, consolidate `generate_index.py`/`rebuild_index.py`, converge writes on `bgg_id` keys, persist slugs and `pdf_url`.
8. **Whose analytics?** No traffic or usage data exists to validate the "content gravity converts to marketplace traffic" hypothesis in the Vision.
