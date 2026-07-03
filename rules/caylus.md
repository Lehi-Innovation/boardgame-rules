---
title: "Caylus"
bgg_id: 18602
player_count: "2-5"
play_time: "60-150 min"
designer: "William Attia"
source_pdf: "caylus-rules.pdf"
extracted_date: "2026-03-18"
summarized_date: "2026-03-18"
verification: "verified"
verification_date: "2026-06-17"
---
<!-- verification:begin -->
> ✅ **Verified** — this summary was fact-checked against the rulebook text and no significant issues were found.
>
> 📄 [Full rulebook text](https://jonnyallred.github.io/boardgame-rules/extracted/caylus-rules.txt) · 🚩 [Report a rules error](https://github.com/Lehi-Innovation/boardgame-rules/issues/new?template=rule-error.yml&labels=rule-error&title=%5BRule%20error%5D%20Caylus&game=caylus)
<!-- verification:end -->


## Overview

Caylus is a worker-placement game set in 1289 France where players are master builders constructing a castle for King Philip the Fair. Players place workers on buildings along a road to gather resources, build new buildings, and contribute to the castle. A key mechanic is the provost, a corruptible official whose position determines which buildings activate each turn. The player with the most prestige points wins.

## Components

- 1 game board (road, castle, scoring track, favor table)
- 1 white bailiff cylinder, 1 white provost disc
- 30 one-denier coins, 10 five-denier coins
- 30 worker cylinders (6 per color: blue, red, green, orange, black)
- 100 houses (20 per color)
- 35 marker discs (7 per color)
- 140 resource cubes (30 each of food/pink, wood/brown, stone/gray, cloth/purple; 20 gold/yellow)
- 40 building tiles (6 neutral, 8 wooden, 9 stone, 8 residential, 9 prestige)
- Rulebook

## Setup

1. Place the board centrally. Sort building tiles by type and place near the board.
2. Place the 6 pink neutral tiles randomly on the first 6 road spaces.
3. Sort resources and coins as the stock.
4. Each player takes pieces of their color, places markers on the turn order scale, passing scale bridge, all four favor tracks, and score track (0).
5. Randomly determine turn order. Player 1 gets 5 deniers; players 2-3 get 6 deniers; players 4-5 get 7 deniers. Everyone also gets 1 wood + 2 food.
6. Place the bailiff and provost on the last neutral building tile.

## Turn Structure

Each turn has 7 phases:

### Phase 1: Collect Income
Each player receives 2 deniers plus 1 per residential building owned, +1 for Library, +2 for Hotel.

### Phase 2: Place Workers
In turn order, each player either:
- **Passes** (places marker on passing scale; first to pass gets 1 denier)
- **Places a worker** on a building or castle

**Placement costs:**
- Own building: 1 denier
- Other player's building: cost = smallest unoccupied number on passing scale (1-5 deniers). Owner gains 1 prestige point.
- Special/neutral/basic building: same as other player's building cost
- Castle: same cost as other player's building

Phase continues until all players have passed.

### Phase 3: Activate Special Buildings
Resolved in order: Gate, Trading Post, Merchants' Guild, Joust Field, Stables, Inn.

### Phase 4: Move the Provost
In passing order, each player may pay 1 denier per space to move the provost 1-3 spaces forward or backward. The provost cannot go before the bridge or beyond the last road space.

### Phase 5: Activate Buildings
Buildings activate in road order from first building after the bridge up to and including the provost's position. Buildings beyond the provost do NOT activate; workers there return without effect. A player may decline a building's effect (except production buildings).

### Phase 6: Build the Castle
Workers placed in the castle contribute batches of resources. A batch must be composed of exactly 3 different cubes, one of which must be a food cube. A player may contribute as many batches as they choose. For each batch contributed, the player places one of their houses in the current castle section and scores prestige points:

- Dungeon: **5 prestige points** per batch
- Walls: **4 prestige points** per batch
- Towers: **3 prestige points** per batch

If a section fills up mid-turn, the player may begin filling the next section. A player who placed a worker in the castle but cannot or will not give a batch loses 2 prestige points (cannot go below 0), except if the Towers section is full.

After all batches are given, the player who contributed the most batches (most houses placed) gains 1 royal favor. Ties are broken by castle order (position 1 wins). Players then retrieve their castle workers.

**Counts:** When the bailiff reaches or passes the designated count space for a section, or when a section is fully built, that section is counted. Each player consults the count table for the relevant section:

**Dungeon count:**
| Houses built | Result |
|---|---|
| 0 | −2 prestige points |
| 1 | 0 |
| 2 or more | 1 royal favor |

**Walls count:**
| Houses built | Result |
|---|---|
| 0 | −3 prestige points |
| 1 | 0 |
| 2 | 1 royal favor |
| 3 or 4 | 2 royal favors |
| 5 or more | 3 royal favors |

**Towers count:**
| Houses built | Result |
|---|---|
| 0 | −4 prestige points |
| 1 | 0 |
| 2 or 3 | 1 royal favor |
| 4 or 5 | 2 royal favors |
| 6 or more | 3 royal favors |

After a section is counted, players must move to the next section even if the previous section has empty spaces. When the Towers section is counted, the game ends.

The castle has 3 sections: Dungeon (6 parts), Walls (10 parts), Towers (14 parts).

### Phase 7: End of Turn
The bailiff advances along the road. Movement distance depends on the provost's position relative to the bailiff:
- Provost is ahead of the bailiff (farther from the castle): bailiff moves **2 spaces** forward.
- Provost is behind the bailiff or on the same space: bailiff moves **1 space** forward.

After the bailiff moves, place the provost on the bailiff's new space. Then check if a Count is triggered (if the bailiff reached or passed a Count space, or if a section was completed this turn). Then begin a new turn.

## Actions

### Building Types

**Production buildings:** Generate resource cubes. Stone buildings (gray) give the owner a bonus cube when activated by another player.

**Construction buildings:**
- Carpenter: build wooden buildings (brown tiles)
- Mason: build stone buildings (gray tiles)
- Architect: build prestige buildings (blue tiles, on residential sites only)

**The Lawyer:** Transform neutral or your own craft buildings into residential buildings (cost: 1 cloth + 1 denier; gain 2 prestige). Residential buildings produce 1 denier income per turn.

### Royal Favors
Gained from castle contributions (best builder each turn, Counts), the joust field, and certain prestige buildings (Church, Statue, Theater, University grant 1 favor each; Monument grants 2 favors). Multiple favors in the same phase must be spent on different lines. Maximum of 4 favors can be gained in a single phase.

The King's favor table has 4 lines, each with 5 columns of increasing power. The first 2 columns are available from the game's start. Columns 3–4 become available after the Dungeon Count. Column 5 becomes available after the Walls Count.

When earning a favor, advance the marker on the chosen line (if possible), then use any effect up to and including the current marker level. Once a marker reaches column 5, it stays there but can still be used.

| Line | Column 1 | Column 2 | Column 3 | Column 4 | Column 5 |
|------|----------|----------|----------|----------|----------|
| a) Prestige | 1 PP | 2 PP | 3 PP | 4 PP | 5 PP |
| b) Deniers | 3 deniers | 4 deniers | 5 deniers | 6 deniers | 7 deniers |
| c) Resources | 1 food | 1 wood or stone | 1 cloth | Exchange 1 cube for 2 cubes (no gold) | 1 gold cube |
| d) Buildings | (no effect) | Build wood building (−1 wood cost) | Build stone building (−1 stone cost) | Lawyer effect (pay only 1 cloth) | Build prestige building on your residential |

### Special Buildings Summary

| Building | Effect |
|----------|--------|
| Gate | Move your worker to any unoccupied space at no cost |
| Trading Post | Take 3 deniers |
| Merchants' Guild | Move provost 1-3 spaces in either direction |
| Joust Field | Pay 1 denier + 1 cloth for 1 royal favor |
| Stables | Change turn order based on stable placement position |
| Inn | Pay only 1 denier for all worker placements until driven out |

## Scoring / Victory Conditions

The game ends immediately after the count of the Towers section (when the bailiff reaches the Towers count space or when all 14 parts of the Towers are built). The player with the most prestige points wins. In the case of a tie for first place, all tied players win.

Prestige is earned throughout the game by:
- Having others use your buildings (1 point per worker placed by an opponent)
- Building new buildings (prestige printed on tile)
- Contributing batches to the castle (5/4/3 PP per batch for Dungeon/Walls/Towers)
- Royal favor prestige line (1–5 PP per favor)
- Lawyer actions (2 PP per residential building built)

**End-game bonuses** (added after the Towers Count):
- 3 PP per gold cube remaining
- 1 PP per 3 non-gold resource cubes remaining
- 1 PP per 4 deniers remaining

## Special Rules & Edge Cases

- The provost can be moved to empty/unbuilt spaces.
- Workers on buildings beyond the provost are wasted (no compensation).
- Players can discuss provost moves but are not bound by promises.
- Production buildings MUST be activated when the building resolves.
- A player can only place 1 worker in the castle per turn.
- The castle can hold multiple workers from different players.
- Residential buildings can be replaced by prestige buildings (losing the income).
- Neutral buildings that are transformed are permanently removed.
- 2-player rules include some modifications to building setup.

## Player Reference

**Turn phases:** Income > Place Workers > Special Buildings > Move Provost > Activate Buildings > Castle > End of Turn

**Placement costs:**
| Where | Cost |
|-------|------|
| Own building | 1 denier |
| Other player's building | = smallest empty number on passing scale (1–5) |
| Neutral / special / basic / castle | = smallest empty number on passing scale (1–5) |

Note: The first player to pass receives 1 denier from the stock immediately.

**Resources:** Food (pink), Wood (brown), Stone (gray), Cloth (purple), Gold (yellow)

**Castle sections:** Dungeon (6 parts) > Walls (10 parts) > Towers (14 parts) — built in order; PP per batch: 5/4/3
