---
title: "Commands & Colors: Ancients"
bgg_id: 14105
player_count: "2"
play_time: "60 min"
designer: "Richard Borg"
source_pdf: "commands-colors-ancients-rules.pdf"
extracted_date: "2026-03-19"
summarized_date: "2026-03-19"
verification: "inaccurate"
verification_date: "2026-07-03"
---
<!-- verification:begin -->
> ❗ **Known errors** — an audit found inaccuracies in this summary that could mislead players: Summary omits the game's "Support" flag-ignoring mechanic (units supported by two adjacent friendly units/leader, and full-strength warriors/barbarian chariots, may disregard one flag) — only leader-attachment flag-ignoring is documented, w. Until it is re-written, prefer the full rulebook text linked below.
>
> 📄 [Full rulebook text](https://jonnyallred.github.io/boardgame-rules/extracted/commands-colors-ancients-rules.txt) · 🚩 [Report a rules error](https://github.com/Lehi-Innovation/boardgame-rules/issues/new?template=rule-error.yml&labels=rule-error&title=%5BRule%20error%5D%20Commands%20%26%20Colors%3A%20Ancients&game=commands-colors-ancients)
<!-- verification:end -->


## Overview

Commands & Colors: Ancients is a card-driven light wargame covering ancient battles from the Roman era and beyond. Players deploy blocks representing infantry, cavalry, chariots, elephants, and leaders on a hex battlefield divided into three sections (left flank, center, right flank). Command cards drive the action, determining which sections and how many units you can order. Battle dice resolve combat. The first player to collect a set number of victory banners (by eliminating enemy units) wins.

## Components

- Game board (hexagonal grid divided into left, center, right sections)
- Wooden blocks with unit stickers (multiple nationalities)
- Command cards deck
- Battle dice (custom symbols)
- Victory banner tokens
- Terrain hexes and overlays
- Scenario booklet

## Setup

1. Select a scenario from the booklet.
2. Place terrain hexes and overlays per scenario map.
3. Each player places their unit blocks per scenario setup.
4. Shuffle command cards; deal each player a starting hand (size varies by scenario).
5. Set victory banner requirements per scenario.
6. Determine first player per scenario.

## Turn Structure

1. **Play a Command Card:** Choose and play one command card from your hand.
2. **Order Units:** Activate the specified units in the designated section(s).
3. **Move Units:** Move ordered units according to movement rules.
4. **Battle:** Ordered units in range attack enemy units.
5. **Draw a Card:** Draw one command card to replenish your hand.

## Actions

### Command Cards
- **Section cards:** Order a number of units in one or more sections (e.g., "Order 3 units on the Left").
- **Tactic cards:** Special orders with unique effects (mounted charge, darken the sky, etc.).

### Movement
| Unit Type | Movement (hexes) | Battle After Move? |
|-----------|------------------|--------------------|
| Light Infantry | 1 or 2 | Yes |
| Auxilia Infantry | 1 and battle, or 2 and no battle | Conditional |
| Medium Infantry | 1 | Yes |
| Warrior Infantry | 1 (or 2 to charge into close combat) | Yes |
| Heavy Infantry | 1 | Yes |
| Light Cavalry | 1–4 | Yes |
| Medium Cavalry | 1–3 | Yes |
| Heavy Cavalry | 1–2 | Yes |
| War Machine | 1 (may not battle at all if it moves; must hold position to battle) | Ranged or close combat, position only |
| Elephants | 1–2 | Yes |
| Leaders (alone) | 1–3 | N/A |

### Combat Basics
There are two types of battle: **Ranged Combat** (fire) and **Close Combat**. An ordered unit may use only one type of battle when it battles, even if it is capable of both; a player may freely switch between Ranged Combat and Close Combat from one unit to the next during the battle phase. A unit adjacent to an enemy unit must Close Combat that adjacent unit if it chooses to battle — it may not use Ranged Combat against the adjacent enemy or any other enemy unit in range. Both types of battle are optional (an ordered unit does not have to battle), except: a warrior unit that moves two hexes to "charge" into range must then Close Combat if any possible target remains.

1. Determine the number of battle dice based on unit type and situation (see Ranged Combat / Close Combat below), then reduce for terrain if applicable.
2. Roll dice. Each symbol matches a unit type:
   - Matching color/shape symbol = 1 hit on that unit type.
   - Swords = 1 hit in Close Combat on most units (exceptions: light infantry, light cavalry, war machines do NOT score hits on sword symbols in Close Combat). Swords never score a hit in Ranged Combat.
   - Flag = force target to retreat its full maximum movement allowance per flag (e.g., 1 flag forces light cavalry to retreat 4 hexes, medium cavalry 3 hexes, light infantry 2 hexes; exceptions: warriors retreat 2 hexes per flag, elephants and auxilia retreat only 1 hex per flag). A flag never scores a hit.
   - Leader helmet = 1 hit in Close Combat only, if a friendly leader is attached to or adjacent to the battling unit (leaders have no effect in Ranged Combat; not effective for elephants).
3. Remove blocks for each hit. When a unit loses its last block, it is eliminated.
4. Eliminated units (and eliminated leaders) earn the attacker 1 victory banner.
5. Apply any retreats caused by flags (see Retreat, under Special Rules & Edge Cases).

### Ranged Combat
Only units with missile weapons may fire: light infantry, light sling infantry, light bow infantry, light cavalry, light bow cavalry, auxilia, and heavy war machines. Light barbarian chariots can never use Ranged Combat.

1. Announce the firing unit and its target. The target must be within range and within line of sight (an unobstructed line from the firing unit's hex center to the target's hex center; a unit, leader, obstructing terrain, or the battlefield edge blocks line of sight).
2. Range by firing unit type:

| Firing Unit | Range |
|---|---|
| Light infantry, light cavalry, auxilia | 2 hexes |
| Light bow infantry, light sling infantry, light bow cavalry | 3 hexes |
| Heavy war machine | 6 hexes |

3. Dice: 2 battle dice if the firing unit held its position (did not move) before firing; 1 die if it moved. Exceptions: an auxilia unit that moves two hexes may not fire at all, and a heavy war machine that moves may not fire at all.
4. Resolve hits as in Combat Basics above, except a leader symbol, a sword, or a non-matching unit symbol is a miss with no effect.
5. **A target unit may not Battle Back after a Ranged Combat attack, and may not Evade a Ranged Combat attack.**
6. Apply any retreats caused by flags.

### Close Combat
A unit battling an adjacent enemy unit is in Close Combat.

1. The defender may choose to Evade instead of fighting, if eligible (see Special Rules & Edge Cases).
2. Determine terrain dice reduction, then roll battle dice (see Player Reference for dice counts by unit type) and resolve hits as in Combat Basics above.
3. Apply retreats.
4. If the attack eliminated the defending unit or forced it to retreat from its hex, the attacker may take a Momentum Advance into the vacated hex and a bonus Close Combat (see Special Rules & Edge Cases).
5. Battle Back: the defender may battle back against the attacker if it has one or more blocks remaining and did not retreat from its hex (see Special Rules & Edge Cases).

## Scoring / Victory Conditions

Collect victory banners by eliminating enemy units. The victory banner target is set per scenario (usually 5 to 8). First player to reach the target wins.

## Special Rules & Edge Cases

- **Leaders** convert helmet symbols into hits in close combat for attached/adjacent friendly units; a unit with an attached leader may also ignore 1 flag (bolster morale). If a leader is killed the opponent earns 1 victory banner.
- **Retreat distance:** Each flag forces the target unit to retreat its full maximum movement allowance toward its own side (not just 1 hex). A light cavalry unit facing 1 flag retreats 4 hexes; facing 2 flags it retreats 8 hexes. Exceptions: warriors retreat 2 hexes per flag; elephants and auxilia retreat only 1 hex per flag, regardless of their normal movement rate.
- **Retreating** onto impassable terrain, off the board, or onto a hex occupied by any unit costs 1 block per unfulfilled hex of retreat. If the unit is left with no blocks it is eliminated.
- **Battle back:** The defending unit may battle back if it survived the close combat attack without retreating from its hex. A unit that was forced to retreat (even if it ends adjacent to the attacker) may not battle back. A target unit may never battle back against a Ranged Combat attack.
- **Momentum Advance & Bonus Close Combat:** After a unit's Close Combat eliminates the defending unit or forces it to retreat from its hex, the attacker may (optionally) advance into the vacated hex; declining forfeits any bonus Close Combat that turn. A unit that takes a Momentum Advance may then make one optional bonus Close Combat against any adjacent enemy unit (not necessarily the one that just retreated) if it is a warrior unit, a non-warrior foot unit with an attached leader (except war machines), or a camel, cataphracted camel, cavalry, cataphracted cavalry, chariot, barbarian chariot, or elephant unit. Cavalry units (light, light bow, medium, heavy, heavy cataphracted) may also move one additional hex after the initial Momentum Advance, in any direction (optional; camels, chariots, and elephants count as mounted but not cavalry and do not get this extra hex). After a successful bonus Close Combat, the unit may Momentum Advance again into the newly vacated hex but may not battle a third time this turn; a cavalry unit doing so may only move onto the vacated hex (no extra hex). Momentum Advance is not allowed if: the defender Evaded; the defender was a lone leader forced to Evade; the attacking unit was Battling Back; the unit was ordered by a First Strike card (though its target remains eligible); terrain restricts it; or the attacking unit is a war machine (war machines may never Momentum Advance).
- **Close combat dice:** Light infantry and light cavalry use 2 dice; auxilia 3 dice; medium infantry 4 dice; heavy infantry 5 dice; light cavalry 2 dice; medium cavalry 3 dice; heavy cavalry 4 dice; war machine 2 dice (stays in position only; may not move and close combat); elephant rolls the same number of dice as the unit it is attacking normally rolls against it.
- **War machines:** May move 1 hex, but may not battle at all if they move. If they hold position instead, they may battle with 2 dice — either Ranged Combat (up to 6 hexes range, requires line of sight) or Close Combat against an adjacent unit. They may evade and, if not eliminated, are removed from the board (crew escapes, no victory banner). War machines may never make a Momentum Advance.
- **Evasion:** Light units (light infantry, light sling infantry, light bow infantry, light cavalry, light bow cavalry, barbarian chariots), war machines, and some mounted units may evade close combat. The evading unit moves 2 hexes toward its own baseline; the attacker rolls dice but only matching unit symbols score hits (swords, flags, and helmets are ignored). Auxilia, medium infantry, warrior, heavy infantry, and elephants may never evade.
- **Elephants** rampage when forced to retreat: before moving, roll 2 dice against each adjacent unit (friend and foe); a matching symbol scores 1 hit, a helmet eliminates a lone leader. After rampage, the elephant retreats; if its path is blocked, units in the path each lose 1 block per hex the elephant cannot fulfill.
- **Terrain** modifies movement, line of sight, and the number of battle dice rolled.

## Player Reference

| Battle Dice Symbols | Effect |
|---------------------|--------|
| Light (green circle) | 1 hit on light units (green circle symbol, with or without white border) |
| Medium (blue triangle) | 1 hit on medium units (blue triangle symbol, with or without white border) |
| Heavy (red square) | 1 hit on heavy units (red square symbol, with or without white border) |
| Sword (crossed swords) | 1 hit in close combat on most units; NO hit from light infantry, light cavalry, or war machines in close combat; ignored entirely in ranged combat |
| Flag | Force retreat of full maximum movement per flag (not 1 hex). Exceptions: warriors retreat 2 hexes/flag; elephants and auxilia retreat 1 hex/flag. Does not score a hit |
| Leader (helmet) | 1 hit if a friendly leader is attached to or adjacent to the battling unit (close combat only; not ranged combat; not effective for elephants) |

**Ranged Combat Range & Dice**

| Firing Unit | Range | Dice (held position / moved) |
|---|---|---|
| Light infantry, light cavalry, auxilia | 2 hexes | 2 / 1 (auxilia: 0 if it moved 2 hexes) |
| Light bow infantry, light sling infantry, light bow cavalry | 3 hexes | 2 / 1 |
| Heavy war machine | 6 hexes | 2 / 0 (cannot fire at all if it moved) |

Ranged Combat requires line of sight and may not target an adjacent enemy. A target of Ranged Combat may not Battle Back or Evade. Light barbarian chariots can never use Ranged Combat.

**Close Combat Dice by Unit Type**

| Unit | Dice |
|------|------|
| Light infantry / light bow / light sling | 2 |
| Auxilia | 3 |
| Medium infantry | 4 |
| Warrior infantry | 3 (4 at full strength) |
| Heavy infantry | 5 |
| War machine | 2 (position only; cannot move and close combat) |
| Light cavalry / light bow cavalry | 2 |
| Medium cavalry | 3 |
| Heavy cavalry (regular or cataphracted) | 4 |
| Elephant | same as target unit's normal dice vs. elephants |
