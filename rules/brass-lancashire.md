---
title: "Brass: Lancashire"
bgg_id: 28720
player_count: "2-4"
play_time: "60-120 min"
designer: "Martin Wallace"
source_pdf: "brass-lancashire-rules.pdf"
extracted_date: "2026-03-18"
summarized_date: "2026-03-18"
verification: "minor_issues"
verification_date: "2026-07-03"
---
<!-- verification:begin -->
> ✅ **Verified (minor gaps)** — fact-checked against the rulebook text; only small omissions were found, nothing that changes how the game is played or scored.
>
> 📄 [Full rulebook text](https://jonnyallred.github.io/boardgame-rules/extracted/brass-lancashire-rules.txt) · 🚩 [Report a rules error](https://github.com/Lehi-Innovation/boardgame-rules/issues/new?template=rule-error.yml&labels=rule-error&title=%5BRule%20error%5D%20Brass%3A%20Lancashire&game=brass-lancashire)
<!-- verification:end -->


## Overview

Brass: Lancashire is an economic strategy game set during the Industrial Revolution in Lancashire, England (1770-1870). Players build and develop industries (Cotton Mills, Coal Mines, Iron Works, Shipyards, Ports), establish canal and rail networks, and sell cotton to earn victory points. The game plays over two eras (Canal and Rail), with scoring at the end of each. The player with the most VPs after the Rail Era wins.

## Components

- 1 Game Board
- 4 Player Mats
- 4 Character tiles
- 4 Income Markers, 4 VP Markers
- 66 Location and Industry cards
- 12 Distant Cotton Market tiles
- 1 Distant Cotton Market Marker
- 1 Deck tile
- 4 Player Aids
- 148 Industry tiles (37 per color)
- 56 Link tiles (14 per color)
- 24 Coal cubes, 16 Iron cubes
- 67 Money tokens

## Setup

1. Place board. Set up Coal and Iron Markets. Place Distant Cotton Market tiles.
2. Each player takes: Player Mat, 30 pounds, Character tile, Link tiles, Industry tiles (stacked by type on mat), VP marker on 0, Income marker on 10.
3. Deal 8 cards to each player.
4. Shuffle Character tiles randomly on Turn Order Track.
5. Remove Location cards by player count: 2P remove blue + teal; 3P remove teal; 4P use all.
6. Set up Deck tile during Canal Era setup (cards beneath it are reserved for Rail Era).

## Turn Structure

### Eras and Rounds
- **Canal Era** then **Rail Era**, each played in rounds.
- Rounds per era: 4P = 8 rounds, 3P = 9 rounds, 2P = 10 rounds.
- **First round of Canal Era:** each player performs only 1 action.

### Player Turn
1. Perform 2 actions (discarding 1 card per action).
2. Place all money spent on Character tile (for turn order).
3. Refill hand to 8 cards from Draw Deck.

### End of Round
- Rearrange turn order: least money spent goes first.
- Return spent money to Bank.
- Collect income (positive or negative).
- Exception: No income after final round of the game.

## Actions

### Build
Place an Industry tile from your Player Mat onto a board location. Discard one card:
- **Location card:** build at named location (even outside network).
- **Industry card:** build matching industry at a location in your network.
- **Double Action Build:** Discard any 2 cards instead of the normal 1, using both of your turn's actions. Treat them as any 1 Location card — build any industry tile in any location with a space for that industry. Still refill your hand with 2 cards.
- Pay money cost. Consume required coal and/or iron.
- Coal Mines/Iron Works: place resource cubes on the tile when built. Shipyards: flip immediately when built.

### Network
Place a Link tile for canal (Canal Era) or rail (Rail Era).
- Canal: costs 3 pounds. 1 Link per route.
- Rail: 1 Link costs 5 pounds; a maximum of 2 Links may be built in one Network action for 15 pounds total. 1 coal must be consumed per Link built.

### Develop
Remove 1 or 2 Industry tiles from Player Mat (consuming iron), to access higher-level tiles.

### Sell (Cotton)
Flip Cotton Mill tiles by selling to the Distant Cotton Market or through connected Ports. The Cotton Mill must be connected to the market trade icon (shown on all Port tiles and some board edges).
- **Distant Cotton Market:** The Cotton Mill must be connected to the market trade icon. Flip the topmost Distant Cotton Market tile; move the Distant Cotton Market Marker along its track by the number of spaces shown on the tile. Advance your Income Marker by the number of spaces shown next to the marker's new position. If the marker reaches the "X" space, cotton cannot be sold to the Distant Market and the Sell action ends immediately (the Cotton Mill is not flipped). Otherwise flip your Cotton Mill and advance your Income Marker by its flip bonus.
- **Port:** Flip a connected unflipped Port tile (any player's); that Port's owner advances their Income Marker. Then flip your Cotton Mill and advance your Income Marker.

### Loan
Take 10, 20, or 30 pounds. Move Income Marker back 1, 2, or 3 income levels respectively.

### Pass
Skip an action but must still discard a card.

## Scoring / Victory Conditions

**Scoring at end of each era:**

1. **Score Links:** Each Link tile scores 1 VP per merchant/trade icon displayed in adjacent locations. Remove Links after scoring.
2. **Score Flipped Industry Tiles:** Score VPs from bottom-left of flipped tiles.

**End of Canal Era additional steps:**
- Remove all level 1 Industry tiles from board.
- Reset Distant Cotton Market. Shuffle deck (including cards under Deck tile) into new Draw Deck with Deck tile inserted near bottom.

**End of Rail Era additional scoring:**
- Score 1 VP per 10 pounds remaining.

**Winner:** Most VPs. Tiebreaker: highest income, then most money.

### How Tiles Flip
| Industry | How it Flips |
|----------|-------------|
| Cotton Mill | Sell action (Distant Market or Port) |
| Port | Sell action (used to sell cotton) |
| Coal Mine | Last coal cube removed |
| Iron Works | Last iron cube removed |
| Shipyard | Immediately when built |

When flipped, advance Income Marker by spaces shown on tile.

## Special Rules & Edge Cases

### Connected Locations
Traced through Link tiles (any player's). Required for Industry card builds, coal consumption, and Port-based selling.

### Coal Consumption
- From closest connected unflipped Coal Mine (free).
- If no connected mine, purchase from Coal Market (requires connection to market trade icon on Ports or board edges).

### Iron Consumption
- From any Iron Works on board (no connection needed, free).
- If none available, purchase from Iron Market.

### Distant Cotton Market
- When selling cotton to the Distant Market, flip the topmost Distant Cotton Market tile.
- Move the Distant Cotton Market Marker along the track by the number of spaces shown on the bottom centre of the tile.
- Advance your Income Marker by the number of spaces shown next to the marker's current position.
- If the marker reaches the "X" space, the Sell action ends immediately and cotton is not sold to the Distant Market.
- You may repeat the process for each of your remaining unflipped Cotton Mills in the same Sell action.

### Overbuilding
Replacing an already-placed Industry tile with a higher-level tile of the same industry type (still paying the build cost) is Overbuilding.
- **Your own tile:** You may Overbuild any Industry tile. Any iron/coal cubes on the replaced tile are removed from it.
- **Opponent's tile:** You may Overbuild only a Coal Mine or an Iron Works, and only if there are no resource cubes anywhere on the entire board (including in its Market) of the same type as the Industry tile being replaced.
- Overbuilt Industry tiles are removed from the game and returned to the box (they do not score VPs). Players do not lose income or VPs when their tiles are overbuilt.

### Negative Income
Pay the negative amount to the Bank. If unable, remove Industry tiles from board at half cost. If still short, lose 1 VP per pound.

### Deck Tile
During Rail Era, the Deck tile is inserted near the bottom of the Draw Deck (2 cards per player beneath it). When reached, it signals the final rounds.

### Canal Era Restrictions
- Only 1 Industry tile per location during Canal Era.
- Rail Era allows multiple tiles per location.

### Market Mechanics
When you build a Coal Mine that is connected to the market trade icon, or an Iron Works (regardless of whether it is connected to the market trade icon), immediately move as many cubes as possible from the Industry tile to available spaces in its associated Market (filling the most expensive spaces first). For each cube moved, collect the money shown on that Market space. If the last cube is moved from the tile, flip it and advance your Income Marker by the amount shown on the tile.

## Player Reference

**Turn Summary:**
1. Perform 2 actions (1 card discarded per action)
2. Place spent money on Character tile
3. Refill hand to 8 cards

**Starting Resources:** 30 pounds, Income level 10, 0 VP

**Action Quick Reference:**

| Action | Cost | Card Required |
|--------|------|--------------|
| Build | Tile cost + resources | Location or Industry card |
| Network (Canal) | 3 pounds | Any card |
| Network (Rail) | 5 pounds (1 link) or 15 pounds (2 links) + 1 coal per link | Any card |
| Develop | Iron (1-2) | Any card |
| Sell | None (may need Port connection) | Any card |
| Loan | -1/-2/-3 income levels | Any card |
| Pass | Nothing | Any card (still discard) |

**Rounds per Era:** 2P=10, 3P=9, 4P=8

**Industries in Lancashire:**
- 12 Cotton Mills
- 8 Ports
- 6 Shipyards
- 4 Iron Works
- 7 Coal Mines
