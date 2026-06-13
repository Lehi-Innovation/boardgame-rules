---
title: "Arkadia"
bgg_id: 25643
player_count: "2-4"
play_time: "60 min"
designer: "Rüdiger Dorn"
source_pdf: "arkadia-rules.pdf"
extracted_date: "2026-03-18"
summarized_date: "2026-03-18"
verification: "minor_issues"
verification_date: "2026-06-13"
---
<!-- verification:begin -->
> ✅ **Verified (minor gaps)** — fact-checked against the rulebook text; only small omissions were found, nothing that changes how the game is played or scored.
>
> 📄 [Full rulebook text](https://jonnyallred.github.io/boardgame-rules/extracted/arkadia-rules.txt) · 🚩 [Report a rules error](https://github.com/Lehi-Innovation/boardgame-rules/issues/new?template=rule-error.yml&labels=rule-error&title=%5BRule%20error%5D%20Arkadia&game=arkadia)
<!-- verification:end -->


## Overview

Arkadia is a tile-placement and worker-management game where players build a town including a central castle. Players place buildings, deploy workers, and collect seals from four noble families. The value of each family's seals fluctuates based on their contribution to the castle. Players choose when to convert their seals to gold, and the player with the most gold wins.

## Components

- 1 game board
- 1 building lot for the castle (10 squares)
- 4 player screens (yellow, orange, green, violet)
- 16 architect banners (4 per player)
- 40 building cards
- 40 buildings in 7 forms (residential, farm, tavern, mill, smithy, trade centre, monastery)
- 88 seals of 4 families (red=cloth, olive=spice, black=carpenter, silver=silversmith; 8 with value 5)
- 44 workers (11 per player color)
- 24 neutral workers (beige)
- 28 castle pieces (with seal tiles)
- Gold coins (values 1, 5, 10)

## Setup

1. Place game board centrally. Position castle building lot so no tent camp squares are covered.
2. Each player takes a screen, 4 architect banners, and 3 workers of their color. Place remaining workers and neutral workers in the general pool.
3. Distribute 12 castle pieces on first floor pool, 12 on second floor pool (stacking same colors), 4 on third floor colored squares.
4. Sort buildings by form. Place seals and gold beside the board.
5. Shuffle building cards; deal 4 to each player face down. Place 3 face up next to board. Stack the rest face down.

## Turn Structure

The youngest player starts; play proceeds clockwise. Each turn:

1. **MUST** do one of:
   - A) Play a building card and place the corresponding building, OR
   - B) Deploy one or more workers
2. **CAN** optionally use one architect banner.

## Actions

**A) Place a Building:**
- Choose a card from hand, take the matching building tile.
- Place it on the board, horizontally/vertically adjacent to an existing building or the castle lot.
- Cannot be placed on squares already occupied by other buildings or workers.
- After placing, check if any buildings are now completely surrounded (all adjacent squares occupied). Surrounded buildings are "completed."

**Completing a Building:** When a building is surrounded by other buildings, workers, or the board edge:
- Each of the active player's own workers and each other player's own (colored) workers adjacent to the completed building earns its owner 1 seal matching the family color shown on the building. **Neutral workers never earn seals for anyone.**
- The active player (who triggered the completion) also receives the seal tile lying on the completed building itself, in addition to any seals earned for adjacent workers.
- Workers are **never removed** from the board after a building is completed; they remain permanently on their squares.
- Then place 1 castle piece on the castle lot (continuing castle construction). The family color on the castle piece affects seal values.

**B) Deploy Workers:**
- Place any number of your own and/or neutral workers from behind your screen onto empty squares adjacent to a single chosen building. All workers introduced in one turn must be adjacent to the same building.

**Architect Banner:**
- After your mandatory action, you may play 1 architect banner (it is then out of the game).
- When played, you immediately receive 2 workers of your color from the general pool.
- In addition, you may then execute a personal evaluation: convert any number of your collected seals to gold at their current exchange rate.
- The exchange rate = number of castle pieces of that family's color currently visible on the castle from a bird's-eye view.
- Each banner can only be used once (4 total per player, so a maximum of 4 personal evaluations per game).

## Scoring / Victory Conditions

- When converting seals to gold, each seal is worth gold equal to the number of castle pieces of that seal's color currently visible on the castle.
- The end of the game begins as soon as a player places the last castle piece on the **second floor** of the castle. Each remaining player (including the triggering player, who goes last) takes one final turn.
- Final scoring: all players convert their remaining seals at end-game exchange rates.
- The player with the most gold wins. If two or more players tie, they share the victory.

## Special Rules & Edge Cases

- Workers behind your screen are hidden; opponents don't know how many you have.
- The castle has 3 floors; higher floors cover lower ones, changing visible colors and thus seal values.
- Timing of seal conversion is critical — seal values change as new castle pieces are placed.
- Each architect banner may be used only once per game.
- Neutral workers can be deployed alongside your own workers in any number, but they never earn seals.
- Buildings come in 7 different shapes/sizes, affecting board coverage.

## Player Reference

| Action Type | Description |
|------------|-------------|
| Place building | Must be adjacent to existing building/castle; squares must be free of buildings and workers |
| Deploy workers | Place any number of own and/or neutral workers, all adjacent to the same building |
| Architect banner | Gain 2 workers of your color; optionally convert seals to gold at current rate (once each) |

| Seal Family | Color |
|------------|-------|
| Cloth merchants | Red |
| Spice merchants | Olive |
| Carpenters | Black |
| Silversmiths | Silver |

| Seal Value | = Number of visible castle pieces of that color |