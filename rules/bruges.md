---
title: "Bruges"
bgg_id: 136888
player_count: "2-4"
play_time: "60 min"
designer: "Stefan Feld"
source_pdf: "bruges-rules.pdf"
extracted_date: "2026-03-18"
summarized_date: "2026-03-18"
verification: "verified"
verification_date: "2026-06-17"
---
<!-- verification:begin -->
> ✅ **Verified** — this summary was fact-checked against the rulebook text and no significant issues were found.
>
> 📄 [Full rulebook text](https://jonnyallred.github.io/boardgame-rules/extracted/bruges-rules.txt) · 🚩 [Report a rules error](https://github.com/Lehi-Innovation/boardgame-rules/issues/new?template=rule-error.yml&labels=rule-error&title=%5BRule%20error%5D%20Bruges&game=bruges)
<!-- verification:end -->


## Overview

In Bruges, players are 15th-century merchants in the Flemish city of Bruges, competing for power and influence. Each round, players draw cards and roll dice that determine threats and reputation costs. Players then play 4 cards per round, each enabling one of 6 possible actions: taking workers, earning money, removing threats, building canals, building houses, or recruiting influential persons. The game ends when the extra draw pile enters play, and the player with the most victory points wins.

## Components

- 1 game board (with reputation track, canal section, scoring track, guard houses, town hall)
- 165 cards (in 5 colors: blue, brown, red, purple, yellow)
- 50 workers (10 in each of 5 colors)
- 20 one-guilder pieces, 24 three-guilder pieces
- 45 Threat markers (in 5 colors)
- 40 Canal tokens
- 4 large Player emblems, 4 small Player emblems
- 8 player pawns (2 per player)
- 12 Majority markers (3 per player)
- 6 Statue tokens (values 2-7)
- 4 fifty/100 points tokens
- 9 Overview cards
- 1 Start player banner
- 5 dice (in 5 colors matching card colors)

## Setup

1. Place game board centrally. Stack Statue tokens sequentially (2 on bottom, 7 on top).
2. **Cards:** Shuffle all 165 cards, divide into 5 roughly equal stacks. Take 1 stack per player, shuffle together, then split into 2 draw piles. Remaining stacks form the extra draw pile.
3. Place workers, guilders, threat markers, and canal tokens in general supply.
4. Each player takes: large seal, small seal (on guard house), 2 pawns (one on space 5 of scoring track, one on town hall), 3 Majority markers (gray side up), 1 worker of each color, 5 guilders, 2 Overview cards.
5. First player: most recent Belgian chocolate eater. Gets Start player banner and 5 dice.

## Turn Structure

Each round has 4 phases:

### Phase 1: Draw Cards
Starting with the start player, each player draws cards (one at a time from either draw pile) until they have 5 cards in hand. Only look at cards once your hand is full.

**Extra draw pile trigger:** When one draw pile empties, immediately replace it with the extra draw pile. The round in which this happens is the **final round**. Exception: a pile usually runs out during Phase 1, but some person cards let you draw cards during Phase 3 — if a pile empties then, the extra draw pile enters play immediately, and the following round is the final round.

### Phase 2: Roll Dice
The start player rolls all 5 dice and places them on the board.

**Step 1 — Distribute Threats:** For each die showing **5 or 6**, every player receives 1 Threat marker of that die's color. A player's **3rd** Threat marker of a single color triggers a penalty.

**Step 2 — Advance Reputation:** The cost to advance 1 step on the reputation track equals the sum of all dice showing **1 or 2**. Each player may pay this cost (in guilders) to advance 1 step. Dice showing 3 or 4 have no effect this phase.

### Phase 3: Play Cards (4 times each)
Starting with the start player, each player plays 1 card and performs 1 of 6 actions. This continues clockwise until every player has played 4 cards (1 card remains in hand).

### Phase 4: Check Majorities
Check the 3 majority categories (people, canals, reputation). For each, the leading player flips their Majority marker to the colored side. Ties: no one leads. Then pass Start player banner clockwise.

## Actions

Any card can be used for any of the 6 actions. The **color** of the played card determines specifics for some actions.

### I. Take 2 Workers
Play 1 card. Take 2 workers of the played card's color from supply.

### II. Take Guilders
Play 1 card. Take guilders from the bank equal to the value shown on the matching-color die (1-6 guilders).

### III. Discard 1 Threat Marker
Play 1 card. Discard 1 Threat marker of the played card's color. Gain 1 point (advance scoring pawn 1 space) each time you discard a threat.

### IV. Build 1 Canal Token
Each player's guard house has 2 canal sections leading out from it (one heading left, one heading right), each with 5 spaces, for a total of 10 canal spaces per player. **A player's canal sections may only be built on by their owner** (the player whose seal is on that guard house) — you cannot build on another player's canals. A player's first built canal must be in one of her own 2 sections (adjacent to her seal). On each subsequent canal-building action, the player may continue building in the direction she started or switch to her other section — she always has 2 options for where to build, unless one of her sections is already completed.

To build, play 1 card matching the color of the canal space you wish to build on (among your own available spaces). Pay the number of guilders shown on that canal space. Place 1 canal token on that space. If a player reaches space 3 of a section, they score 3 points at game end. Completing a full canal section earns the topmost Statue token (max 2 statues per player).

### V. Build 1 House
Play 1 card. Pay 1 worker of the played card's color. Place the card face-down in your play area as a house of that color.

### VI. Recruit 1 Person
Play 1 card onto one of your empty houses (the person may be a different color than the house). Pay the guilder cost shown in the top-left corner of the person card. Each house accommodates exactly 1 person. Each person has a unique ability (immediate, ongoing, activated, or end-game) and is worth points at game end equal to one-third of their recruitment cost.

## Scoring / Victory Conditions

### Threat Penalties (3rd marker of a color)
Each color has its own penalty. The source text confirms only two color-to-penalty pairings explicitly (via worked examples): **Red = Fire** and **Yellow = Raid**. The extracted text never states which color corresponds to Flood, Plague, or Intrigue — those mappings below are unconfirmed and should be re-checked against the physical rulebook's color-coded icons before relying on them.

| Color | Threat Name | Penalty |
|-------|-------------|---------|
| Unconfirmed | Flood | Return ALL your workers to the supply |
| Unconfirmed | Plague | Discard 1 person of your choice from your play area (not from hand) |
| Red (confirmed) | Fire | Discard 1 built house OR 1 built canal token (if you have neither, no loss); if a house with a person is discarded, take that person back into hand |
| Unconfirmed | Intrigue | Lose 3 points (score cannot go below 0) |
| Yellow (confirmed) | Raid | Return ALL your guilders to the bank |

After resolving the penalty, return all 3 threat markers of that color to the supply (the next marker of that color received will count as the player's "first" again). Players do not score points when returning threat markers after suffering damage. A player may suffer multiple penalties in the same turn; if so, that player chooses the order in which they are applied.

### End-Game Scoring
Score in any order:
1. **Person points:** Each person in your play area scores points equal to one-third of their recruitment cost (shown on the card below the price).
2. **Houses:** 1 point per built house (occupied or not).
3. **Person end-game bonuses:** Each person with a "laurel" icon scores the VP indicated on that card.
4. **Majority markers:** Each Majority marker you flipped to its colored side is worth **4 points**.
5. **Canal milestones:** Each canal section space 3 you built scores **3 points**. Each Statue token you collected scores the points printed on it (2–7).
6. **Reputation track:** Score the number of points shown on the step your reputation pawn has reached.

**Highest VP total wins.** Tiebreaker: most guilders remaining. If still tied, those players share the victory.

## Special Rules & Edge Cases

- Players can make change at any time (3-guilder piece = 3 single guilders).
- The 5th unplayed card each round stays in hand but may not be used for actions.
- Multiple actions of the same type can be performed in a single round.
- A person may be placed in a house of any color — the person need not match the house color. You cannot recruit without an available empty house.
- Person types: Immediate (activates on recruitment), Ongoing (always active), Activated (use once per round), End-game (scores at game end).
- Guard houses: each has a round box for the player's small seal, marking the guard house from which that player's 2 personal canal sections extend (one left, one right).

## Player Reference

**Round structure:** Draw to 5 cards → Roll dice (threats + reputation) → Play 4 cards → Check majorities

**6 Actions:**
| # | Action | Cost | Effect |
|---|--------|------|--------|
| I | Take workers | Card | 2 workers of card color |
| II | Take guilders | Card | Guilders = value on matching-color die |
| III | Remove threat | Card | Discard 1 matching-color threat; gain 1 point |
| IV | Build canal | Card (matching canal space color) + guilders shown on that space | Place canal token on one of your own 2 available canal spaces (owner-only; first build adjacent to your seal, then continue that section or switch to the other) |
| V | Build house | Card + 1 matching worker | Place card face-down as house (scores 1 VP at end) |
| VI | Recruit person | Card onto empty house + guilders (person's printed cost) | Person may differ from house color; scores VP at end |

**Dice values:**
- 1-2: Determine reputation advance cost (sum of all dice showing 1 or 2)
- 3-4: No effect in Phase 2
- 5-6: Each player receives 1 threat marker of that die's color
