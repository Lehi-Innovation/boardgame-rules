# PRD-04 — Quality & Trust

The product's promise is *accurate* rules at answer time, so quality machinery is a first-class subsystem. It exists in code today, in two layers: structural validation and content quality gating, plus provenance/confidence conventions in the Q&A loop.

## Layer 1 — Structural validation (`scripts/validate.py`)

- Frontmatter must parse as YAML and contain non-empty `title` and `bgg_id` (`REQUIRED_FRONTMATTER`).
- Body must contain every expected `##` section: 8 for base games, 6 for expansions (template chosen by presence of `base_game_bgg_id` in frontmatter).
- Runnable per-file or across all of `rules/`; exit code 1 on any failure (CI-friendly, though **no CI is configured** [NEEDS REVIEW: add a GitHub Action running `validate.py` + pytest on PRs]).

## Layer 2 — Content quality gate (`scripts/quality_check.py`)

Run as the pipeline's final stage (`summarized → validated | flagged`):

| Check | Flag condition (code) |
|---|---|
| Structural validation | any `validate_rules_file()` error |
| Source sufficiency | extracted text < **2,000 bytes** (`MIN_EXTRACTED_SIZE`) |
| Section depth | any section < **20 words** (`MIN_SECTION_WORDS`) |
| Hedging | any of 5 `UNCERTAINTY_PHRASES` (e.g. "unclear from the text", "not specified in the rules") |

- Pass → `status: validated`. Fail → `status: flagged` + machine-readable `review_notes` (semicolon-joined issues) on the registry entry.
- **Drift:** the design doc (`docs/plans/2026-03-04-scalable-rules-pipeline-design.md`) specifies a 50-word section threshold and a "hallucination risk" check (mechanics mentioned that aren't in the extracted text); the code implements 20 words and no hallucination check. [NEEDS REVIEW: reconcile doc vs code; the hallucination check is designed but unimplemented]

## Quality tiers and the calibration plan

Per the design doc: **auto-accept with calibration** — manually review the first 20–30 summaries, then let the gate auto-accept the rest.

**Current reality** [code-backed counts]: 1,616 games sit at `summarized`, only **6** are `validated`, **19** are `flagged` — the gate has barely been run, and flagged games have no review tooling or documented workflow. The product's quality promise currently rests on the summarization prompt alone. [NEEDS REVIEW: this is the single largest gap between design and reality — run the backlog, then build a minimal flagged-review loop (list flagged + `review_notes`, fix or re-summarize, re-check).]

## Trust conventions in the Q&A loop (`rules-lookup` skill)

- **Source-tier citation**: every answer states whether it came from the summary, the extracted rulebook, BGG forums, or intuition.
- **Confidence labels**: high / medium / low on every answer.
- **"Unverified" marking**: intuition-sourced summary additions are explicitly labeled unverified in the auto-created PR description.
- **Human merge as final gate**: auto-updates land as PRs, never direct commits to the summaries — the maintainer reviews diffs before they reach the published site.

## Provenance

What exists: `source_pdf`, `extracted_date`, `summarized_date`, `rulebook_version` in frontmatter; tracked `extracted/` text enabling diffs against re-extractions; `pdf_url` in the registry.

Gaps:
- `pdf_url` survives on only 19 of 2,122 entries — provenance is usually discarded once the PDF is downloaded (and PDFs themselves are gitignored). Reproducing or auditing a summary's source is often impossible. [NEEDS REVIEW: persist `pdf_url` permanently]
- `rulebook_version` is rarely populated and never consumed (see PRD-01's edition question).
- The summarizing model is not recorded in frontmatter — summaries produced by different models/prompts are indistinguishable. [OPEN QUESTION: add a `summarizer` or `model` frontmatter field?]

## Content licensing & takedown

Summaries are derived works of publisher rulebooks. The repo records no permission policy, license file for the content, or takedown procedure; the site states no terms. The deliberate choices already made (never republish PDFs; summaries in original wording; link identity to BGG) reduce exposure but are undocumented as policy. [NEEDS REVIEW: write down the licensing stance and a publisher-request/takedown process; decide a license for the summaries themselves]

## Integrity (trust in the catalog itself)

Verified current state: 0 duplicate `bgg_id`s/names/slugs — but 26 orphan rules files, 20 summarized/validated entries with missing files, and an 8-vs-2 expansion-link disagreement between frontmatter and registry. No referential-integrity check exists. [NEEDS REVIEW: add a `scripts/lint_registry.py`-style reconciliation that cross-checks registry ↔ rules/ ↔ extracted/ and fails CI on drift — the cheapest high-leverage quality investment available.]
