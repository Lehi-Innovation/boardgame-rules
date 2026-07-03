---
title: "Antike"
bgg_id: 19600
player_count: "2-6"
play_time: "90-120 min"
designer: "Mac Gerdts"
source_pdf: "antike-rules.pdf"
extracted_date: "2026-03-18"
summarized_date: "2026-03-18"
verification: "minor_issues"
verification_date: "2026-06-13"
---
<!-- verification:begin -->
> ✅ **Verified (minor gaps)** — fact-checked against the rulebook text; only small omissions were found, nothing that changes how the game is played or scored.
>
> 📄 [Full rulebook text](https://jonnyallred.github.io/boardgame-rules/extracted/antike-rules.txt) · 🚩 [Report a rules error](https://github.com/Lehi-Innovation/boardgame-rules/issues/new?template=rule-error.yml&labels=rule-error&title=%5BRule%20error%5D%20Antike&game=antike)
<!-- verification:end -->


## Overview

Antike is a civilization-building strategy game set in the ancient world. Players lead nations (Greeks, Romans, Germanic tribes, Phoenicians, Carthaginians, Persians, Arabs, Egyptians, Babylonians) by producing resources, building temples, recruiting armies, advancing technology, and founding cities. Victory is achieved not by territorial conquest but by earning ancient personages (kings, scholars, generals, citizens, navigators). The first nation to collect the required number of personages wins. The game uses a rondel action-selection mechanism with no dice or cards.

## Components

- Double-sided game board (West: Roman Empire / East: Alexander's Empire), each with 50 provinces
- 12 nation cards
- 35 ancient personage cards (9 kings, 8 scholars, 7 generals, 6 citizens, 5 navigators)
- 1 "starting player" card
- Resource chips: iron (blue), marble (white), gold (yellow) in 1-, 2-, and 5-unit denominations
- 30 coins (substitute for any 1-unit resource)
- 20 white temples
- 150 city stones (25 per nation color)
- 102 legions in 6 colors, 102 galleys in 6 colors
- 36 octagonal game stones (for rondel, score, progress)
- 4 short rule cards, rule book

## Setup

1. Choose board side (West or East) and number of players.
2. Sort personage cards into 5 stacks. Set up resource chips, coins, and temples as the bank.
3. Distribute nation cards (draw randomly or draft starting with youngest). Nations participating depend on player count and board side.
4. Each nation receives starting resources: 1 iron, 2 marble, 3 gold.
5. Each nation gets 17 legions, 17 galleys, 25 city stones, and 6 game stones.
6. Place city stones on 3 starting cities (1 marble, 1 iron, 1 gold per nation card).
7. The nation with the red dot on its card starts; at the start of each round, all nations receive 1 coin.

**2-player variant:** Each player manages 2 nations independently. The game ends when any nation reaches 9 personages.

## Turn Structure

Each turn has 3 steps in order:

1. **Action Selection (Rondel):** Move your game stone clockwise on the 8-wedge rondel. The first 1-3 wedges are free; each additional wedge costs 1 resource of any type. You cannot stay on the same wedge two turns in a row (repeating costs 8 wedges = 5 resources).
2. **Found Cities (optional):** Found cities in provinces where you have military units. Cost: 1 marble + 1 iron + 1 gold per city.
3. **Win Personages:** Collect any personages whose requirements you now meet.

## Actions

The rondel has 8 wedges in 3 categories:

### Production Actions
| Wedge | Effect |
|-------|--------|
| **Marble** | Gain 1 marble per marble city (3 per marble city with temple) |
| **Iron** | Gain 1 iron per iron city (3 per iron city with temple) |
| **Gold** | Gain 1 gold per gold city (3 per gold city with temple) |

Production can be increased by know-hows: Market (+1 total per production action) and Currency (+2 total per production action).

### Utilization Actions
| Wedge | Effect |
|-------|--------|
| **Temple** | Build temples: 5 marble each. Triples city production, arming capacity, and defense. Max 1 temple per city. Max 20 temples on board. |
| **Arming** | Recruit legions/galleys: 1 iron each. Place in provinces with your cities. 1 unit per city without temple, 3 per city with temple. |
| **Know-How** | Buy advances with gold. 8 know-hows across 2 rows (see below). |

### Military Action
| Wedge | Effect |
|-------|--------|
| **Maneuver** (appears twice) | Phase 1: Move units across borders. Phase 2: Conquer enemy cities. |

**Movement Rules:**
- Legions cross red (land) borders; galleys cross blue (sea) borders. Some borders are both.
- By default each unit may carry out 1 maneuver action per turn. With Wheel, legions get 2 actions; with Roads, legions get 3. With Sailing, galleys get 2 actions; with Navigation, galleys get 3.
- If a legion and enemy legion meet, or galley and enemy galley, they destroy each other 1:1.

**Conquest:**
- A city's defense strength = 1 (without temple) or 3 (with temple), plus the number of defending military units in the province, plus 1 if the defender has Monarchy or 2 if the defender has Democracy.
- The attacking nation's active (still standing erect) units in the province must be at least equal to the defense strength.
- The conquering nation removes its own active units equal to the defense strength of the city.
- The defending nation removes its city stone, temple (if any), and all its military units from the province. The destroyed temple returns to the bank.
- The conquering nation places its city stone on the city.

### Know-How Track (8 advances)

There are two rows: **Basic know-hows** (top row) and **Secondary know-hows** (bottom row). A nation must own a basic know-how before obtaining the corresponding secondary know-how.

| Basic Know-How | Secondary Know-How | Effect |
|----------------|--------------------|--------|
| Wheel | Roads | Wheel: legions get 2 maneuver actions. Roads: legions get 3 maneuver actions. |
| Sailing | Navigation | Sailing: galleys get 2 maneuver actions. Navigation: galleys get 3 maneuver actions. |
| Market | Currency | Market: +1 unit per production action. Currency: +2 units per production action. |
| Monarchy | Democracy | Monarchy: +1 to city defense strength. Democracy: +2 to city defense strength. |

**Know-how costs:**
- 7 gold for a new basic know-how (no other nation has it yet)
- 10 gold for a new secondary know-how (no other nation has it yet)
- 3 gold for a basic know-how that one or more other nations already possess
- 5 gold for a secondary know-how that one or more other nations already possess

A nation acquiring a know-how that no other nation yet has earns 1 ancient scholar. Owning all 8 know-hows earns a bonus ancient personage (from the stack with the most remaining).

## Scoring / Victory Conditions

| Personage | Requirement | Available |
|-----------|-------------|-----------|
| **King** | Every 5 cities owned | 9 |
| **Scholar** | Each new know-how learned | 8 |
| **General** | Each enemy temple destroyed | 7 |
| **Citizen** | Every 3 temples owned | 6 |
| **Navigator** | Every 7 seas with your galley at turn end | 5 |

**Personages to win by player count:**

| Nations | Personages Needed |
|---------|-------------------|
| 6 | 7 |
| 5 | 8 |
| 4 | 9 |
| 3 | 10 |

Once won, personages can never be lost, even if the conditions are no longer met.

If all 35 personages are awarded with no winner, the first nation to destroy a temple thereafter wins.

## Special Rules & Edge Cases

- Coins substitute for any 1-unit resource at any time.
- At the start of each round, every nation receives 1 coin.
- A province can hold unlimited military units of any nation.
- Foreign units do not prevent founding cities or arming.
- Only galleys go in sea-only provinces; only legions in land-only provinces.
- If a game material runs out (legions, galleys, city stones, temples), no more can be created until some return to supply.
- Resource chips are unlimited; use substitutes if needed.

## Player Reference

| Action | Cost | Effect |
|--------|------|--------|
| Found city | 1M + 1I + 1G | Place city stone |
| Build temple | 5M | Triple production/defense/arming at city |
| Recruit unit | 1I each | Place at city (1 per city, 3 with temple) |
| Buy know-how | Gold (varies) | Permanent nation advance |
| Military move | Free (on Maneuver) | Move units per maneuver actions available |

| Rondel Movement | Cost |
|-----------------|------|
| 1-3 wedges | Free |
| 4+ wedges | 1 resource per extra wedge |
| Same wedge twice | 8 wedges = 5 resources |