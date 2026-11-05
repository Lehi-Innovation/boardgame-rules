---
name: top-games-push
description: Use when asked to get the BGG Top 100 (or Top 200) games fully verified in the rules database. Fetches the current BGG rankings, diffs them against the registry, and drives every top-ranked game through the pipeline to independently-verified status. Invoke with /top-games-push [--top 100|200] [--batch-size 10].
---

# BGG Top-100/200 Priority Push

Game-night demand is extremely head-heavy: a small number of famous games
account for most real-world rules questions. This skill drives the **BGG
Top 100** (extended goal: Top 200) to fully trustworthy status. Coverage of
one top-100 game is worth more than ten long-tail games.

**Context (2026-08 snapshot):** the catalog had a popularity inversion —
obscure wargames fully verified while Catan/Splendor/7 Wonders sat at
`extracted`, Wingspan was `unverifiable`, and Carcassonne, Dominion,
Spirit Island, Everdell, and Love Letter were missing from the registry
entirely. This skill exists to fix that class of problem permanently.

## Definition of done (per game)

A top-ranked game is **done** only when ALL of these hold:

1. Registered in `games.yaml` with correct `bgg_id` and a `bgg_rank: <n>`
   field (so future runs can sort by priority).
2. Source rulebook obtained and extracted (`extracted/<slug>-rules.txt`
   exists and is genuinely the right game's rulebook — read the first 50
   lines to confirm).
3. Rules summary exists, passes `python -m scripts.validate`.
4. **Independently verified** — see "The verification bar" below.
5. Stamped (`python -m scripts.stamp_verification`) and reflected in a
   regenerated `index.md` + `games.json`.

A game may instead be **blocked**: `status: not_found` with a `notes` field
explaining what was tried (e.g. "no public English PDF; publisher does not
release rules"). Blocked is an acceptable terminal state for the push ONLY
if the notes show a real search was done (all sources in priority order).

## The verification bar (do not lower it)

Self-graded verification over-claims: a 2026-07-03 measurement found
**~27–35% of "verified" summaries still contained a MAJOR error** on
independent re-audit (see `docs/quality/2026-07-03-independent-reaudit.md`).
For top-100 games the bar is therefore:

- The `verify` pipeline stage (or `scripts.verify_summary`) is **necessary
  but not sufficient**.
- After a game reaches `verified`, run an **independent re-audit with a
  fresh agent** following `.claude/skills/audit-rules/SKILL.md` (use an
  ad-hoc batch id like `top-001`, `top-002`, …). Record verdicts with
  `python -m scripts.audit record` (see that module's docstring for exact
  usage) — it auto-flags MAJOR games.
- Only PASS/MINOR from the independent audit counts as done. MAJOR →
  re-summarize from the extracted text and re-audit. Never let the agent
  that wrote or repaired a summary grade it.

## Procedure

### Step 1 — Fetch the current BGG rankings

Ranks drift; always fetch fresh rather than reusing an old tracker.

**Primary method — scrape the BGG browse pages** (100 games per page,
sorted by rank; page 1 = ranks 1–100, page 2 = 101–200):

```
https://boardgamegeek.com/browse/boardgame/page/1
https://boardgamegeek.com/browse/boardgame/page/2
```

- Use Playwright browser tools if plain `requests` gets a 403/redirect —
  BGG blocks obvious scrapers. Send a real browser User-Agent, wait ~2s
  between pages, and fetch only the pages you need.
- Each row links to `/boardgame/<bgg_id>/<slug>` and shows the rank.
  **Sanity-check the parse before trusting it:** print the first 5 rows —
  rank 1 should be a famous heavyweight (Brass: Birmingham held #1 for
  years). If ranks or IDs look wrong, the markup changed; adjust.
- The `boardgame` browse ranks base games; if an entry is an expansion
  (check the BGG page type), register it per the Expansions section of
  CLAUDE.md with `base_game_bgg_id`.

**Fallback / spot-check — BGG XML API2** (token in `.env` as used by
`scripts/bgg.py`, `Authorization: Bearer` header):

```
GET https://boardgamegeek.com/xmlapi2/thing?id=<id1>,<id2>,...&stats=1
```

`item/statistics/ratings/ranks/rank[@name="boardgame"]/@value` is the
overall rank. Batch ≤20 ids per request, sleep 2s between requests. The
API cannot list "top N" directly — use it to verify scraped ranks or fetch
metadata (`scripts.bgg.get_game_details`).

### Step 2 — Build the tracker

Write `docs/quality/top200.yaml` (regenerate fully on every run):

```yaml
updated: "YYYY-MM-DD"
source: "BGG browse pages 1-2, fetched YYYY-MM-DD"
games:
  - rank: 1
    bgg_id: 224517
    name: "Brass: Birmingham"
    slug: brass-birmingham        # null until registered
    registry_status: verified     # or: missing / pending / found / ... / flagged
    verification: verified        # from rules file frontmatter, if any
    action: done                  # register|find_pdf|download|extract|summarize|verify|reaudit|stamp|done|blocked
    notes: ""
```

Diff against the registry **by `bgg_id`** (names drift across editions):

```python
from scripts.registry import load_registry
by_id = {g.get("bgg_id"): g for g in load_registry("games.yaml")}
```

For every ranked game already registered, set
`bgg_rank` on its registry entry via
`update_game("games.yaml", name, bgg_rank=rank)`. Report the headline
numbers (X of top 100 done, Y in pipeline, Z missing/blocked) before
starting work.

### Step 3 — Work the queue in batches

Work **top rank first**, 5–10 games per session (a full game through
summarize + verify is context-heavy; don't overfill). For each game,
`action` follows from `registry_status`:

| Current state | Action |
|---|---|
| missing | `python -m scripts.find_rulebook "<Name>" --bgg-id <ID>`, then PDF hunt |
| pending / not_found | PDF hunt (retry `not_found` — old misses often succeed) |
| found | `python -m scripts.process_batch --stage download --limit N` |
| downloaded | `python -m scripts.extract_pdf source_pdfs/<slug>-rules.pdf` (use `--method pdfplumber` for tables); review output quality |
| extracted | Summarize **interactively** (below), then `scripts.validate` |
| summarized / validated | `python -m scripts.verify_summary rules/<slug>.md`; fix MAJOR findings |
| verified (self-graded) | Independent re-audit (fresh agent, audit-rules skill) |
| flagged | Read `review_notes`, re-summarize from extracted text, re-verify, re-audit |

**PDF hunt, in priority order:** (1) 1j1ju.com, (2) the publisher's own
site — top-100 publishers almost always host rules (catan.com, Stonemaier,
Days of Wonder, Rio Grande, Z-Man, Fantasy Flight/Asmodee support, Cephalofair,
Leder Games, Czech Games Edition, Capstone, GMT's living rules pages),
(3) BGG's files page for the game. Save to `source_pdfs/<slug>-rules.pdf`
(`touch` the empty file first so a manual "Save As" lands with the right
name). BGG blocks automated downloads; publisher sites usually don't.

**Summarize interactively, not via the batch stage.** Top-100 games get
the careful treatment: read the full extracted text, follow the template
in CLAUDE.md, keep exact numbers and edge cases, and when the extraction
has garbled tables, render the PDF pages to images and read those (command
in CLAUDE.md's pipeline section). If a game has well-known official FAQ
errata available, add a `## FAQ & Rulings` section with sourced rulings
only — top games are exactly where FAQ content pays off.

**Editions:** match on `bgg_id`, record `rulebook_version` in frontmatter,
and make sure the PDF matches the edition the BGG entry describes (e.g.
Catan 5th ed vs older "Settlers of Catan"). Family contamination (base-game
rules leaking into a variant's summary) is the #1 audit failure for famous
families — flag it to the auditor in the batch notes.

### Step 4 — Verify, stamp, publish

After each batch:

1. Independent re-audit the batch's games (fresh agent, ad-hoc batch id).
2. `python -m scripts.stamp_verification --update-registry` (or list the
   files) to stamp banners and promote audit-PASS games.
3. `python -m scripts.generate_index && python -m scripts.generate_manifest`
4. Update `docs/quality/top200.yaml` statuses.
5. Commit: extracted text, rules files, `games.yaml`, `index.md`,
   `games.json`, tracker. Message convention:
   `Top-100 push: <slugs or count> (<done>/<target> done)`.
6. If a remote MCP worker deploy workflow exists (`worker/`), pushing to
   main redeploys the corpus automatically — no extra step.

### Step 5 — Report and repeat

End each session by reporting: done count vs target, games blocked (with
reasons), and the next batch. Re-run Step 1 quarterly or when resuming
after a gap — ranks drift, and newly ranked games enter the target set.

## Edge cases

- **Expansions in the top 200** (rare in the boardgame browse but possible):
  register with `base_game_bgg_id`, use the expansion section template.
- **Monster rulebooks** (Gloomhaven, Twilight Imperium): summarize the core
  loop and scenario-agnostic rules precisely rather than compressing
  everything; the extracted text + `search_rulebook` covers the long tail.
- **No public PDF** after all three sources → `status: not_found`, notes
  say exactly what was searched; tracker `action: blocked`.
- **Slug collisions** with existing entries: `scripts.prepare_research`
  contains the collision check; never silently overwrite another game's
  files.
- **Copyright**: per the project posture in CLAUDE.md, publishing summaries
  and extracted text is accepted practice here — do not skip or unpublish a
  game out of caution. If a takedown notice arrives, surface it to the
  repository owner; do not action it autonomously.
