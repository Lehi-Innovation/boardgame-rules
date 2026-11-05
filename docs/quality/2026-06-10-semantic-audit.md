# Semantic Accuracy Audit — 2026-06-10

> **Follow-up (2026-06-13):** all four MAJOR games below were subsequently
> re-summarized (`fix: rewrite three summaries…` + the critter-kitchen fix) and
> then re-verified against source by `scripts/verify_summary.py`. Current
> verdicts: critter-kitchen, colosseum, a-game-of-thrones-catan → PASS;
> pacific-typhoon → MINOR. battlecars and die-dracheninsel (MINOR here) were
> corrected via the verify+repair loop and are now MINOR/verified. This file is
> retained as the historical record of the original audit.


A calibration sample for the quality pipeline: 6 games were drawn at random from summaries that **pass** the automated quality gate (`scripts/quality_check.py`), and each summary was fact-checked line-by-line against its source text in `extracted/` by an independent review agent. This is the "hallucination risk" check that the pipeline design (`docs/plans/2026-03-04-scalable-rules-pipeline-design.md`) specified but never implemented.

## Headline result

| Game | Verdict | Numbers checked → supported |
|---|---|---|
| die-dracheninsel | MINOR_ISSUES | 11 → 11 |
| battlecars | MINOR_ISSUES | 20 → 19 |
| critter-kitchen | **MAJOR_ISSUES** | 24 → 23 |
| a-game-of-thrones-catan-brotherhood-of-the-watch | **MAJOR_ISSUES** | 18 → 16 |
| pacific-typhoon | **MAJOR_ISSUES** | 7 → 3 |
| colosseum | **MAJOR_ISSUES** | 16 → 11 |

**4 of 6 randomly sampled gate-passing summaries contain errors that would mislead players at the table.** The automated gate measures structure and depth, not accuracy — `validated` status should be read as "structurally complete," not "correct." The four MAJOR games have been set to `flagged` with `review_notes` in `games.yaml`.

## Error taxonomy observed

1. **Base-game contamination** (agot-catan): the model imported standard-Catan assumptions (desert hex, 4:1 trade, 2-VP Longest Road, win-on-reaching-10-VP) that the variant's rulebook explicitly overrides, and omitted the variant's signature systems (wildlings, guards, heroes).
2. **Invented mechanics** (pacific-typhoon, colosseum): a "Pass" action the rules explicitly forbid; VP tokens that don't exist; an "Emperor's Loge token shop"; "reduced-value substitution"; "program tiers."
3. **Wrong numbers** (colosseum): minimum bid 1 vs the rulebook's 8; 5 nobles vs 6.
4. **Fabricated metadata** (critter-kitchen): designers credited as "Nathan Meunier, Jack Caesar" — names that appear in the rulebook only as *example players*; real designers are Alex Cutler and Peter C. Hayward.
5. **Material omissions** (all four): entire scoring steps (critter-kitchen's Final Score track), phases (colosseum's Closing Ceremonies), and economies (colosseum's event income; pacific-typhoon's fate/hand-size rules).
6. **Direction-reversal** (battlecars, minor): tank "takes no damage *performing* a ram" summarized as "immune to *being* rammed."

## Implications for the quality process

- The automated gate (`quality_check.py`) is **necessary but not sufficient**: it caught thin/under-sourced summaries (234 flagged in the 2026-06-10 batch run) but passes semantically wrong ones.
- A semantic cross-check against `extracted/` text catches what the gate misses, and can be run by agents in batches — no human reading required for the first pass.
- Humans are best reserved for: triaging `flagged` games, adjudicating audit findings, and games where no extracted source exists to check against (668 summaries currently have no `extracted/` file — they are *unverifiable* without re-sourcing the PDF).
- Expansion/variant games appear to be a high-risk class (base-game contamination); prioritize them in any systematic audit.

## Full agent findings

The complete per-game findings (every claim checked, with quotes) are preserved below.

### pacific-typhoon — MAJOR_ISSUES
- Summary action "**Pass:** Choose not to play any more cards this round" contradicts rule 7.7: "You may not 'pass' your turn... if you don't play, you must choose one of the two discard options."
- Summary component "Victory point tokens" — no support; VPs come only from spoil cards.
- "The battle type [Day/Night] determines which values are most relevant" contradicts 7.4: the round leader declares a **suit** (Air/Surface/Sub/Combined); the suit mechanic is absent from the summary.
- "Round leader reveals a Battle card" — text 7.2: leader draws two, selects one, discards the other.
- "The winning side's highest contributor claims the Battle card's VP" understates 11.1–11.2: winner must **divide** spoils among every winning player with combat value 1+.
- Spoils include captured force cards (0–6 VP), not just battle cards.
- Play time claims ("about 1 hour", "60 minutes") have no support in the text.
- "Surigao Strait" example battle: not in the text. "Special weapons" card category: not in the text (categories are regular/bonus/event).
- Omitted: hand-size rules (base 6, +1 per full resource, max 9), the fate/victim mechanic, year-of-battle restriction, tied-battle continuation, "?" die-roll values, 110 force cards, tiebreakers, Renewed Battle card.

### battlecars — MINOR_ISSUES
- Tank ram immunity reversed: text grants immunity when the tank *performs* a side/shunt ram; summary says it is immune to *being* rammed.
- Ram table omits "If you perform the ram, you take no damage" qualifier.
- "Last vehicle operational wins" — unsupported inference; text only says driver death eliminates you.
- Destruction condition misstated; the text's damage-cap rule ("damage stops at one destroyed internal unit") is omitted.
- Crash/ram facing-change rule (roll 1 die, change direction) omitted.
- Post-apocalyptic framing and frontmatter player count/play time/designers absent from source (source is the 2020 fan-made Print N Play V2.0 by Chris Morse, not the 1983 original — not noted in frontmatter).

### a-game-of-thrones-catan-brotherhood-of-the-watch — MAJOR_ISSUES
- "Desert hex" terrain: the variant has Ice Fields, no desert; Tormund's start location is unspecified in the text.
- "Supply trade: Default 4:1" contradicts the variant's "standard rate... is 3:1 (instead of 4:1)."
- "Longest Road (2 VP)" contradicts "Longest Road and Largest Patrol are only worth 1 VP each."
- "First player to reach 10 VP on their turn wins" contradicts win-only-at-END-of-turn, plus two omitted immediate end conditions (3 wall breaches; 8+ wildlings in the Gift).
- Invented "Wall defense" turn phase; guard *pieces* miscalled cards.
- Omitted: guard build cost (1 Brick, 1 Wool, 1 Lumber), guard VP tokens, hero cards (entire system), wildling types/migration/breach track, Largest Patrol card, 3-round setup with guard placement.

### die-dracheninsel — MINOR_ISSUES
- Omitted: "Treasure bearers may not enter the treasure site"; Sweet Slumber cannot stop forced departure; Foolhardy Flight landing/partner-jump details.
- All 11 numbers checked were supported; all action cards and core mechanics match.

### critter-kitchen — MAJOR_ISSUES
- Fabricated designer credit ("Nathan Meunier, Jack Caesar" are example-player names; real designers Alex Cutler, Peter C. Hayward).
- "All ties are friendly" applied to *winning* contradicts the score-track/priority-track tiebreaker.
- Critic-meal "Final Score" step (a major star source) entirely absent.
- Meal-preparation step structure misattributed (text places it in Step 5: End of Round).
- 23 of 24 numbers supported; body text otherwise faithful.

### colosseum — MAJOR_ISSUES
- "Minimum bid: 1 coin" vs text "opening bid... must be 8 coins or more."
- "5 nobles (… 2 Senators)" vs text 6 nobles (3 Senators).
- "4 phases" vs 5 (Closing Ceremonies omitted: Podium, mandatory clean-up, asset donation).
- Podium rule wrong (highest score since game start, not per-round most spectators).
- Invented: Emperor's Loge token shop; reduced-value asset substitution; "3 tiers" of programs; program-designated star performers.
- Omitted: Emperor Medals, event income, +5 bonuses (produced programs, Season Tickets), auction-winner exclusion, 2-programs-at-setup, starting asset deals, second tiebreaker.
