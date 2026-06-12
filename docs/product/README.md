# Product Document Suite (First Draft)

First-draft product and architecture documents for the **boardgame rules database** — the catalog of games and AI-friendly rules summaries this repository implements — produced from a full discovery pass on 2026-06-10.

The suite distinguishes code-backed findings from inferences ([INFERRED]), gaps ([OPEN QUESTION]), and reviewer to-dos ([NEEDS REVIEW]).

| Doc | Contents |
|---|---|
| [00 — Discovery Summary](00-discovery-summary.md) | Tech stack, entities, workflows, design decisions, integrity findings |
| [01 — Product Vision](01-product-vision.md) | What/who/why, differentiation, non-goals, risks |
| [02 — PRD-01 Catalog & Data Model](02-prd-01-catalog-data-model.md) | Game hierarchy, identity keys, sourcing, fields, expansions |
| [03 — PRD-02 Content Pipeline](03-prd-02-content-pipeline.md) | Acquisition → extraction → summarization stages, concurrency, funnel state |
| [04 — PRD-03 Search, Discovery & AI Consumption](04-prd-03-search-discovery.md) | Browse/lookup today, the slug-URL contract, tiered Q&A, facet taxonomy |
| [05 — PRD-04 Quality & Trust](05-prd-04-quality-trust.md) | Validation, quality tiers, provenance, licensing, integrity |
| [06 — Domain Model & ERD](06-domain-model-erd.md) | Entities, textual ERD, keys, implied-but-unmodeled entities |
| [07 — Document Generation Summary](07-document-generation-summary.md) | What was supported / inferred / missing |
