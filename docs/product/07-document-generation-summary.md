# Document Generation Summary

## What was well-supported by the codebase

Nearly everything — this suite documents an existing, working product:

- **Discovery Summary** — fully evidence-based, including registry integrity statistics computed during discovery (0 duplicate ids/names/slugs; 26 orphan rules files; 20 missing rules files; 8-vs-2 expansion-link disagreement; full status distribution).
- **PRD-01 (Catalog & Data Model)** — entities, identity keys, sourcing flows, frontmatter schema, and validation rules read directly from `scripts/registry.py`, `scripts/bgg.py`, `scripts/validate.py` and verified against live data.
- **PRD-02 (Content Pipeline)** — stage map, statuses, claim/reclaim semantics, and every numeric threshold (10 KB PDF, 500-char summarize floor, 2,000-byte quality floor, 20-word section floor, 1-hour claim timeout) cited from code.
- **PRD-03 (Search & AI Consumption)** — the browse index, slug-URL contract, paste-a-prompt usage, and 4-tier lookup are all shipped behavior.
- **PRD-04 (Quality & Trust)** — both validation layers, the tier flow, and the Q&A confidence conventions are code-backed.
- **Domain Model & ERD** — every entity, field, join, and integrity caveat verified.

## What was inferred with low confidence

- **Audience framing** in the Vision (players at the table, RAG builders) — drawn from the design docs' consumer list and the shipped landing-page prompt, but no usage data exists to confirm who actually consumes the site.
- **North star metric candidates** — no metrics, analytics, or success criteria exist anywhere in the repo.
- **Future-facing suggestions** marked [INFERRED]: machine-readable `games.json` index, quality badges from `validated` status, BGG taxonomy facets, expansion cross-links as discovery.

## What is genuinely missing and needs human input

1. **North star metric** — pick one (validated coverage, Tier-1 answer rate, or AI fetch volume).
2. **Quality gate execution** — 1,610 summarized games never quality-checked; 19 flagged games with no review workflow. The calibration-then-auto-accept plan needs to actually run. (Largest design-vs-reality gap.)
3. **Edition policy** — one summary per game vs per major printing; whether to fetch BGG versions; what to do with `rulebook_version`.
4. **Retry/triage policy** for the 435 `not_found` games and the ~43 stalled in-flight games.
5. **Identity hardening** — converge writes on `bgg_id`, persist `slug` and `pdf_url`, unify the six `slugify()` copies, define a safe rename procedure.
6. **Reconciliation tooling + CI** — no referential-integrity checks and no CI exist; a registry↔filesystem lint run on PRs is the cheapest high-leverage fix.
7. **Licensing stance** — derived-work position, summary license, and takedown process are all unwritten.
8. **Consolidation decisions** — `generate_index.py` vs `rebuild_index.py`; doc-vs-code threshold drift (50 vs 20 words; unimplemented hallucination check); unused `searching` status.
