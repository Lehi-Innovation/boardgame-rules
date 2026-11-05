# Board game rules collection audit

Audit date: 2026-11-04.

Corrected gameplay rules in 21 summaries, fixed source availability labels for 154 empty extractions, and restored the Cytosis rulebook link. All 1,665 published summaries pass structural validation and the published catalog is consistent. The collection still has substantial verification gaps: 831 summaries lack usable source text, and the 21 repaired games require independent review before earning a verified badge.

## Audit scope

Every published summary was checked for required structure, catalog coverage, published metadata, source availability, and verification state. The optional strict registry audit also compared identities, registry metadata, pipeline states, and extraction coverage across the collection.

Gameplay review targeted 21 summaries with earlier MAJOR findings. Corrections were checked against the corresponding local rulebook extractions, including related claims in the body and reference sections. This was a collection-wide integrity audit with targeted gameplay review; it was not a sentence-by-sentence semantic verification of every game. No new full-game PASS verdicts were issued.

The [collection inventory](2026-11-04-collection-inventory.csv) has one row per summary, including source status, verification before and after, existing audit verdict, repair status, and source prefilter warnings. [Machine-readable totals](2026-11-04-collection-audit.json) accompany it.

## Gameplay corrections

The [correction evidence](audit-findings/2026-11-04-corrections.md) contains the final diff and supporting source passages for each game.

| Game | Corrections |
|---|---|
| A Feast for Odin | Ore and goods placement in houses; sheds require wood and stone. |
| Caverna | Count all grain, divide by two, then round up for scoring. |
| Dragonwood | A failed capture returns played Adventurer cards except the one-card wound. |
| Egizia | Joker crews must accompany another crew; two stones earn one point. Removed unsupported scoring claims and deferred the unreadable grave scoring table to the printed rulebook. |
| El Grande | Added the Home Bonus; Grandes can move through specified actions and do not count as Caballeros in the standard game. |
| Five Tribes | Corrected optional market actions, coin costs, visible-card selection, Djinn costs, Fakir uses, assassinations, merchandise sales, game-end timing, and shared ties. |
| Flamecraft | Six Artisan Dragons and seven Goods of each type; corrected final turns, Fancy Dragon timing, Coin scoring, and tiebreakers. |
| Forbidden Sky | Everyone must reach launch pad tiles before the final connection; abandonment is a loss. Wind-blocked pawns remain in place and lose rope. |
| Fort | Added all three game-end triggers; Macaroni Sculpture is worth four points. Corrected scoring categories, ties, recruitment, and card rewards. |
| My City | Campaign victory uses progress symbols rather than cumulative episode points; corrected passing costs. |
| Mysterium | Crows replace cards in the Ghost's hand. Corrected face-up visions, refills, failed guesses, the hourglass, and the final vote. |
| Oceans | Added population on surviving species to final scoring and documented the source's tiebreakers. |
| Olympos | Development costs seven AP before discounts; corrected Wonder requirements, final actions, scoring sources, discovery bonuses, and ties. |
| Ora et Labora | Buying land is an extra action; harvesting removes forest or moor cards. Corrected building placement restrictions. |
| Pandemic Legacy Season 0 | Removed Shuttle Flight; corrected Commercial and Unrecorded Flights, team actions, surveillance, and Mop Up. |
| Pandemic Legacy Season 2 | Added exposure; corrected sea travel, supply actions, free actions, production cards, plague placement, and Infection-deck exhaustion. |
| PARKS | Corrected Campfire relighting, Gear costs, First Hiker acquisition and scoring, and the visited-Parks tiebreaker. |
| Project L | Pieces return to personal supply. Added Finishing Touches, unfinished-puzzle penalties, correct tiebreakers, and the final Black-puzzle limit. |
| Quarriors | Restored the five-phase sequence, summoning costs, and the empty-Creature-card game end. |
| Raids | Only sold Goods score; added Mjöllnir scoring and shared victory on a tie. |
| Rajas of the Ganges | Complete the current stage after markers cross; compare the fame-point gap, then who crossed first. |

Original audit reasons are preserved as `previous_reason` in the audit tracker. Repair dates, evidence links, and `pending_independent_audit` status were added. All 21 games retain `flagged` registry status and their MAJOR verdict pending independent review.

## Source availability and verification labels

The stamper and manifest generator previously accepted an empty extraction file as available rulebook text. They now require non-whitespace text. Missing or empty sources also override historical audit verdicts, preventing an unavailable source from supporting a verified badge or a rulebook link. Regression tests cover missing, empty, whitespace-only, and legacy sources, as well as manifest links.

The source scan found 154 empty extractions. Their summaries now show **Unverifiable**, and their blank rulebook links are omitted. Schotten Totten also changed from **Known errors** to **Unverifiable** because its source is missing; its historical finding remains in the tracker.

Cytosis already had an extraction under the filename named in its frontmatter. A byte-identical copy at `extracted/cytosis-rules.txt` restores the canonical published link. Its state is now **Unverified**, since source availability alone does not establish accuracy.

Two historical source-only MAJOR verdicts, for The Quacks of Quedlinburg expansions The Alchemists and The Herb Witches, said their extractions were missing. Both sources are now present. Those stale verdicts were removed from the active tracker and preserved in [superseded source verdicts](2026-11-04-superseded-source-verdicts.yaml); the summaries remain **Unverified** awaiting semantic audit.

| Verification state | Before | After |
|---|---:|---:|
| Verified | 341 | 341 |
| Verified with minor gaps | 158 | 158 |
| Known errors or repairs awaiting review | 250 | 249 |
| Unverified | 239 | 86 |
| Unverifiable | 677 | 831 |
| Total | 1,665 | 1,665 |

`index.md` and `games.json` were regenerated from the updated summaries.

## Remaining findings

Of the 831 summaries without usable source text, 677 have no recognized extraction and 154 have empty extractions. Another 834 have nonempty text; availability does not establish that an extraction is complete or belongs to the correct edition. Prefilter warnings are included in the inventory for review, not treated as confirmed gameplay errors.

Of the 249 summaries still displaying Known errors, 21 received the targeted repairs above and 228 retain other historical findings. Those other findings were not substantively re-audited in this pass. Egizia's extracted grave scoring table lacks point values, so that detail still requires the printed table or a better extraction.

The [strict registry findings](2026-11-04-registry-findings.txt) contain 5,509 diagnostic messages: 4,721 metadata disagreements, 675 missing-extraction messages, 39 missing or stale artifact messages, four duplicate summary identities, and 70 structural or content-quality messages. These checks use different conditions from the source availability scan. Metadata disagreements can reflect missing registry fields or formatting differences; they are not 5,509 confirmed rules errors. Resolving ambiguous identities and conflicting metadata requires evidence before choosing which value to retain.

## Validation

- Full Python test suite: **129 passed**.
- `python -m scripts.validate`: **all 1,665 summaries valid**.
- `python -m scripts.catalog`: **consistent published catalog**.
- `git diff --check`: **passed**.
- Strict registry audit: findings retained in the linked diagnostic report; this optional check does not pass.

Changes are local. No commit, push, or deployment was performed.
