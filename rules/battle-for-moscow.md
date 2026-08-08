---
title: "Battle for Moscow"
bgg_id: 6544
player_count: "2"
source_pdf: "battle-for-moscow-rules.pdf"
extracted_date: "2026-08-07"
summarized_date: "2026-08-07"
rulebook_version: "v1.0"
verification: "unverified"
verification_date: "2026-08-08"
---

# Battle for Moscow

<!-- verification:begin -->
> ⚠️ **Unverified** — this AI-generated summary has not yet been fact-checked against the rulebook. Double-check critical rules against the full rulebook text linked below.
>
> 📄 [Full rulebook text](https://lehi-innovation.github.io/boardgame-rules/extracted/battle-for-moscow-rules.txt) · 🚩 [Report a rules error](https://github.com/Lehi-Innovation/boardgame-rules/issues/new?template=rule-error.yml&labels=rule-error&title=%5BRule%20error%5D%20Battle%20for%20Moscow&game=battle-for-moscow)
<!-- verification:end -->

## Overview

Battle for Moscow is a two-player hex-and-counter wargame simulating Operation Typhoon, the German Army's final 1941 offensive to break Russian resistance and capture Moscow. One player commands the Germans, the other the Russians (Soviet Union). German ground units represent corps of approximately 25,000 soldiers each; Russian ground units represent armies of approximately 40,000 men each. Players move their units across a hexagonal map and resolve combat by totaling the Strength Points of adjacent opposing units into a simplified odds ratio, then rolling a die and consulting the Combat Results Table (CRT) to apply the outcome. The game runs for 7 Game Turns. The Germans win by holding Moscow at the end of the game; the Russians win by holding Moscow plus at least one other city; any other outcome is a draw.

## Components

| Component | Quantity |
|---|---|
| Map (11" x 17") | 1 |
| Square game pieces (units) | 1 set of 40, 5/8" |
| Player Aid sheet (terrain effects + turn track) | 1 |
| Rules booklet | 1 |
| Battlesson sheet | 1 |
| Six-sided die | Not included — players must supply their own |

Each unit is a double-sided piece: a full-strength (front) side and a reduced-strength (back) side worth half the full-strength Combat Strength, rounded down. Every unit shows a Combat Strength (its value in Strength Points), a Movement Allowance (in Movement Points), a unit type (Infantry, Shock — infantry with massive artillery reserves — or Panzer/Tank/Armor), and a Unit Size and ID, which are for historical interest only and have no effect on play. The German player controls field-gray/light-gray units; the Russian player controls red/pink units.

## Setup

1. Place the Game Turn marker on the "1" box of the Game Turn Track, and place the Russian 1st Shock Army on the "4" box (it arrives later as a Reinforcement — see Reinforcements below).
2. Take the remaining sixteen Russian armies and flip them to their reduced-strength side. Place one reduced-strength Russian unit on each hex marked with a red star; since all Russian units have the same strength, it doesn't matter which unit goes where. Two Russian units will be left over after this placement.
3. The German player then sets up one full-strength German unit on each hex marked with a black cross. This exact placement is very important, since it determines what the Germans are capable of doing on Game Turn 1.
4. The German player commences Game Turn 1 starting directly with his Combat Phase, then follows the normal Sequence of Play until the last Game Turn is completed. Because all German units begin the game at full strength and are physically placed in their starting positions, the German player receives neither a Replacement Phase nor a (Special) Panzer Movement Phase on Game Turn 1 — his first turn begins at Phase 3 (Combat).

## Turn Structure

The game lasts 7 Game Turns. Each Game Turn represents roughly one to two weeks of real time (Turns 3 and 4 each represent about two weeks, because mud slows the battle). Each Game Turn is divided into 9 Phases performed in the exact order below; all actions in one phase must finish before the next begins. The first four phases are the German Player Turn, and the next four are the Russian Player Turn:

**German Player Turn**
1. German Replacement Phase — the Germans receive replacements.
2. German (Special) Panzer Movement Phase — all German Panzer units may move.
3. German Combat Phase — all German units may attack.
4. German Movement Phase — all German units may move (including Panzers that already moved in Phase 2).

**Russian Player Turn**
5. Russian Replacement Phase — the Russians receive replacements.
6. Russian (Special) Rail Movement Phase — all Russian units that begin this phase on a rail line may move along it.
7. Russian Combat Phase — all Russian units may attack.
8. Russian Movement Phase — all Russian units may move (including those that already moved by rail in Phase 6).

**Administrative**
9. Housekeeping Phase — advance the Game Turn marker, or, if the last Game Turn was just played, stop and determine the winner.

On Game Turn 1 only, the German player skips Phases 1 and 2 and begins directly with his Combat Phase (see Setup, step 4).

## Actions

### Movement

Units move during the Movement Phases (2, 4, 6, and 8). Each unit has a Movement Allowance representing how many hexes it can move in each eligible Movement Phase, subject to weather and terrain effects (given on the Player Aid Sheet). In a Movement Phase, a player moves any or all of his units that qualify for that phase (only Panzers in the Panzer Movement Phase; only Russian units already on a rail line in the Rail Movement Phase). Units move one at a time, hex to hex, in any direction or combination of directions.

- **Russian Rail Movement**: Russian units that start the Rail Movement Phase on a rail line may move only along rail-connected hexes, at a cost of 1 Movement Point per hex regardless of terrain (e.g., a forest hex still costs only 1 hex of rail movement).
- **Restrictions**: a unit can never enter a hex containing an enemy unit. A unit can enter a hex with a friendly unit, but only one unit may occupy a hex at the end of each Phase (no stacking).
- **Zone of Control**: a unit entering an Enemy Zone of Control (EZOC) must immediately end its movement for that Movement Phase. There is no penalty for leaving an EZOC.
- River hexsides cost nothing extra to cross for movement — rivers affect combat only, never movement.

### Combat

Combat is resolved during the Combat Phases (3 and 7). All friendly units may attack adjacent enemy units; attacking is completely voluntary, and units are never compelled to attack. A "Battle" is an attack on one enemy unit by any or all of the attacking player's adjacent units, resolved with a single die roll. The attacking player first announces all his Battles for the phase — declaring in advance which enemy units he will attack and which of his own units will attack them. A single unit may attack only once per Combat Phase, and a single enemy unit may be attacked only once per Combat Phase. Once all of a player's Battles for the phase have been announced, he cannot change his mind (Battle Commitment).

**Battle Sequence** (performed for each Battle, in any order the attacker desires):
1. Total the Combat Strengths of all attacking units in that Battle.
2. Divide this total by the defending unit's Combat Strength, dropping any remainder, to get an odds level on the Combat Results Table.
3. Determine whether terrain has lowered the odds column.
4. Roll the die and cross-index the row of the number rolled with the odds column to determine the result.
5. Apply the combat result immediately.
6. Advance after combat: if the defending unit is no longer in its hex (eliminated or forced to retreat), one attacking unit may immediately move into the defender's just-vacated hex.
7. Resolve the next pending Battle, if any.

**Odds modifiers:**
- **Long Odds**: after Step 2, odds above 6:1 are reduced to 6:1. After Step 3, if the odds are below 1:1, the attack has no effect on either side.
- **Terrain Effects** (cumulative): if the defending unit is in a forest, in a major city (Moscow or Tula), or is a Russian unit in a fortification hex, reduce the odds by one level. If all of the attacking units in a Battle are across a river from the defender, reduce the odds by one further level.

**Combat Results** (from the Combat Results Table):
- **NE (No Effect)**: nothing happens.
- **DR (Defender Retreat)**: the defender retreats two hexes toward its own board edge, chosen by the attacker; each hex of retreat must take the unit further from the original hex (no zigzagging). The unit must avoid entering an EZOC if possible; if it must retreat through an EZOC hex it loses one step, and if it is forced to end its retreat in an EZOC it is eliminated. It may never retreat into or through an enemy-occupied hex, nor end its retreat in a friendly-occupied hex. If there is no retreat path satisfying all these conditions, the unit is eliminated instead.
- **Stand Fast**: when defending in a Major City hex only, the defender may convert a DR result into a single step loss with no retreat.
- **DRL (Defender Retreat and Loss)**: the defending unit first takes a step loss; then, if it survives, it retreats as described for a DR result.
- **DE (Defender Eliminated)**: the defending unit is entirely eliminated, whether it is currently at full-strength or half-strength.
- **EX (Exchange)**: the defending unit first takes a step loss as in a DRL. The attacking player must then lose at least the same amount of Strength Points from among the attacking units in that Battle (a loss when a full-strength unit is reduced to half-strength is measured as its original strength minus its reduced strength). If the defender survived, it must then retreat as per a DR result. If the defender is eliminated because it was unable to retreat, the attacker does not have to match that additional loss.
- **AL (Attacker Loss)**: one attacking unit, of the attacker's choice, takes a step loss as described in a DRL. It does not retreat. No attacking units ever retreat in Battle for Moscow.

A step loss flips a full-strength unit to its reduced-strength side; a half-strength unit that takes a loss is eliminated (removed from the map).

## Scoring / Victory Conditions

- The **Germans win** if they control Moscow at the end of Game Turn 7.
- The **Russians win** if they control Moscow and any one other city.
- **Any other result** — for example, the Germans controlling every city except Moscow — is a **draw**.
- "Friendly controlled" means that a player's units were the last ones to enter that city. All cities are owned by the Russians at the beginning of the game except for those that start occupied by German units.

## Special Rules & Edge Cases

### Zones of Control (ZOC)

Each unit has a Zone of Control consisting of the six hexes surrounding it, including hexes occupied by enemy units.
- **Movement effect**: a unit entering an Enemy Zone of Control must immediately end its movement for that Movement Phase; units may move directly from one EZOC hex into another EZOC hex, but must then stop.
- **Combat effect**: units cannot end a retreat in an EZOC — they are eliminated if they do.
- **Replacement effect**: ZOCs also affect whether a path can be traced for replacements (see below).
- Unlike some other wargames, friendly units never negate the effects of enemy Zones of Control.

### Replacements

Both players receive replacements on their own Player Turns (Phases 1 and 5). The number of replacement steps received each turn is listed on the Game Turn Record Track. Each replacement step lets a player either (1) place a new half-strength unit on the map — using one previously eliminated, or, for the Russians, one that was not set up on the map at the start of the game — or (2) flip a half-strength unit currently on the map to its full-strength side. Two replacement steps cannot be used in the same Player Turn to create a new full-strength unit from an off-map unit; that requires two turns' worth of replacement steps (one received each turn). Any replacement step not used that turn is permanently lost.

- **Russian replacements** appear along the northeast, east, or southeast (red-bordered) map edges, in an empty hex not in an Enemy ZOC, or in an empty, friendly-controlled city (marked with white-dashed hexside markings) that is in communication with those red-bordered edges (at most one unit per city; no stacking). Existing reduced-strength Russian units being restored to full strength must also be in communication with a red-bordered edge. As an exception, the Russians can bring in or restore a unit in Moscow even if it is not in communication with a red-bordered edge. "In communication" means being able to trace a path of any length from the hex in question to a red-bordered edge, without (excluding the origin hex) entering a hex containing an enemy unit or an Enemy ZOC.
- **German replacements** appear and trace communication the same way, except to and along the west (black-bordered) map edge; Moscow has no special properties for the Germans.

### Reinforcements

Only the Russians receive a reinforcement unit — the 1st Shock Army — which sets up as indicated in the Setup Rule (arriving on the "4" box of the Game Turn Track). It is placed on its full-strength side in any hex along the northeast, east, or southeast (red-bordered) map edge that is not occupied by another unit and not in an Enemy ZOC.

### Mud

Turns 3 and 4 are "mud" turns; all other turns are "clear" and have no special effect.
- **Movement**: all movement, except Russian Rail Movement, is reduced to one hex per Phase.
- **Combat**: the Combat Strengths of Panzer and Tank units are totaled and then halved when attacking only (never when defending); fractions are retained when halving (half of 9 is 4.5). Infantry unit strength is unaffected. If an Exchange (EX) result occurs on a mud turn, the attacker's losses are based on the units' printed (full) strengths, not their halved mud-turn values.

## Player Reference

### Game Turn Sequence (9 Phases)

| # | Phase | Side |
|---|---|---|
| 1 | Replacement | German |
| 2 | (Special) Panzer Movement | German |
| 3 | Combat | German |
| 4 | Movement | German |
| 5 | Replacement | Russian |
| 6 | (Special) Rail Movement | Russian |
| 7 | Combat | Russian |
| 8 | Movement | Russian |
| 9 | Housekeeping | — |

### Combat Results Table Outcomes

| Result | Effect |
|---|---|
| NE | No effect |
| DR | Defender retreats 2 hexes |
| Stand Fast | Major-city defender only: 1 step loss, no retreat (instead of DR) |
| DRL | Defender takes step loss, then retreats if it survives |
| DE | Defender eliminated entirely |
| EX | Defender takes step loss (+ retreats if it survives); attacker must match the Strength Point loss |
| AL | One attacking unit takes a step loss; no retreat |

### Key Numbers

- **Game length**: 7 Game Turns (each turn = ~1–2 weeks of real time).
- **Mud turns**: 3 and 4 (movement capped at 1 hex/phase except Russian rail; Panzer/Tank attack strength halved).
- **Long Odds cap**: 6:1 maximum; below 1:1 has no effect.
- **Cumulative terrain odds shifts**: forest, major city (Moscow/Tula), or Russian fortification = −1 level each; all attackers across a river = −1 level.
- **Unit strength**: reduced-strength (back) side = half of full-strength Combat Strength, rounded down.
- **ZOC**: 6 surrounding hexes per unit.
- **Victory**: Germans need Moscow at end of Turn 7; Russians need Moscow plus 1 other city; otherwise a draw.
