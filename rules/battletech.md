---
title: "BattleTech"
bgg_id: 1540
player_count: "2+"
play_time: "60-180 min"
designer: "Jordan Weisman, L. Ross Babcock III"
source_pdf: "battletech-rules.pdf"
extracted_date: "2026-03-18"
summarized_date: "2026-03-18"
verification: "verified"
verification_date: "2026-06-17"
---
<!-- verification:begin -->
> ✅ **Verified** — this summary was fact-checked against the rulebook text and no significant issues were found.
>
> 📄 [Full rulebook text](https://jonnyallred.github.io/boardgame-rules/extracted/battletech-rules.txt) · 🚩 [Report a rules error](https://github.com/Lehi-Innovation/boardgame-rules/issues/new?template=rule-error.yml&labels=rule-error&title=%5BRule%20error%5D%20BattleTech&game=battletech)
<!-- verification:end -->


## Overview

BattleTech is a tactical wargame set in the 31st century where players command giant humanoid war machines called BattleMechs ('Mechs). Each player controls one or more 'Mechs on a hex-based map, maneuvering for position, firing weapons, and managing heat buildup. 'Mechs are tracked using record sheets that detail armor, internal structure, weapons, equipment, and heat. The game combines strategic positioning with detailed combat resolution. Victory is typically achieved by destroying or disabling all opposing 'Mechs.

## Components

- Hex-based map sheets (various terrain)
- BattleMech miniatures or standees
- 'Mech record sheets (one per 'Mech)
- Two six-sided dice (2d6)
- Various reference tables and charts
- Markers/counters for tracking status

## Setup

1. Select a scenario or agree on force composition (each player selects 'Mechs of agreed Battle Value).
2. Each player takes the record sheet for each of their 'Mechs.
3. Place the map sheet(s) on the table.
4. Deploy 'Mechs according to scenario rules or agreed placement.
5. Determine initiative for the first turn.

## Turn Structure

Each game turn consists of 6 phases:

### 1. Initiative Phase
- Each player rolls 2d6. The **higher** roll wins initiative.
- The initiative **loser** acts first in all subsequent phases (movement, weapon attacks, physical attacks). The winner acts last.
- Ties are re-rolled.

### 2. Movement Phase
- Players alternate moving 'Mechs, starting with the initiative loser.
- Each 'Mech has one of four movement modes:
  - **Standing Still:** No movement; generates 0 movement heat.
  - **Walking:** Move up to the 'Mech's Walking MP. Generates 1 heat.
  - **Running:** Move up to the 'Mech's Running MP (Walking x 1.5, round up). Generates 2 heat.
  - **Jumping:** Move up to the 'Mech's Jump MP in any direction, ignoring terrain. Generates 1 heat per jump MP used (minimum 3).

### 3. Weapon Attack Phase
- Players alternate declaring and resolving weapon attacks.
- The initiative **loser** declares fire first (same as movement); the initiative winner acts last.
- Each weapon can fire once per turn.
- Resolve: declare target, check line of sight, check firing arcs, calculate target number, roll 2d6.

### 4. Physical Attack Phase
- After weapons fire, 'Mechs in close range may make physical attacks: **punches**, **kicks**, **charges**, **Death From Above**, and **push** attacks.
- Physical attacks use different hit calculations.

### 5. Heat Phase
- Total all heat generated this turn (from movement and weapons fire).
- Subtract heat dissipated by heat sinks.
- Track cumulative heat on the record sheet.
- Excessive heat causes penalties: movement reduction, to-hit modifiers, possible ammunition explosion, possible shutdown.

### 6. End Phase
- Resolve any remaining effects.
- Check for 'Mech destruction or pilot incapacitation.

## Actions

### Movement
- **Terrain costs:** Clear = 1 MP, Light Woods = 2 MP, Heavy Woods = 3 MP, Water (depth 1) = 2 MP, Hills (elevation change) = +1 or +2 MP.
- **Facing:** 'Mechs face a hex edge. Turning one hex face costs 1 MP (walking/running) or is free (jumping).
- **Minimum movement:** A 'Mech can always move 1 hex forward regardless of terrain cost.
- **Stacking:** Multiple 'Mechs cannot occupy the same hex.

### Weapon Attacks (G.A.T.O.R. System)
1. **G**unnery Skill: Base target number is the MechWarrior's Gunnery Skill (default 4).
2. **A**ttacker Movement: +1 (walked), +2 (ran), +3 (jumped).
3. **T**arget Movement: +0 (stood still) to +4+ (moved 18+ hexes).
4. **O**ther Modifiers: +1 per intervening light woods, +2 per heavy woods, +1 for partial cover, +1 for heat.
5. **R**ange: Short (+0), Medium (+2), Long (+4). Each weapon has specific range brackets.

Roll 2d6: if the roll >= target number, the attack hits.

### Hit Location
- Roll 2d6 on the Hit Location Table.
- Different tables for front, left side, right side, and rear attacks.
- Damage is applied to armor first, then internal structure.

### Physical Attacks

| Attack | Target | Damage | Modifier |
|--------|--------|--------|----------|
| Punch | Adjacent 'Mech (forward/side arc) | Attacker's total weight / 10 (round up) | Piloting skill +modifiers |
| Kick | Adjacent 'Mech (forward arc) | Attacker's total weight / 5 | Piloting skill -2 |
| Charge | Move into target hex | Attacker weight / 10 × hexes moved (round up); attacker takes target weight / 10 | Piloting skill +modifiers |
| Death From Above | Jump onto target | Attacker weight / 10 × 3 (round up); attacker takes attacker weight / 5 to legs | Piloting skill +modifiers |

### Heat Management

| Heat Level | Effect |
|-----------|--------|
| 0-4 | No effect |
| 5-9 | –1 Walking MP |
| 8-12 | +1 to weapon attack Target Numbers |
| 10-14 | –2 Walking MP |
| 13-16 | +2 to weapon attack Target Numbers |
| 14 | Must roll 2d6 ≥ 4 or shut down |
| 15-19 | –3 Walking MP |
| 17-23 | +3 to weapon attack Target Numbers |
| 18 | Must roll 2d6 ≥ 6 or shut down |
| 19-22 | Ammo may explode; roll 2d6 ≥ 4 to avoid |
| 20-24 | –4 Walking MP |
| 22 | Must roll 2d6 ≥ 8 or shut down |
| 23-27 | Ammo may explode; roll 2d6 ≥ 6 to avoid |
| 24+ | +4 to weapon attack Target Numbers |
| 25-29 | –5 Walking MP |
| 26 | Must roll 2d6 ≥ 10 or shut down |
| 28-30 | Ammo may explode; roll 2d6 ≥ 8 to avoid |
| 30 | Automatic shutdown (cannot be avoided) |

## Scoring / Victory Conditions

- Standard: The side with the last surviving 'Mech(s) on the map wins.
- If the last 'Mechs from each side are destroyed simultaneously in the same turn, or if the last remaining 'Mechs on each side cannot move and have no ability to damage one another, the game is a **draw**.
- A 'Mech is destroyed when: the center torso internal structure is reduced to 0, the head is destroyed, the engine sustains 3 critical hits, or an ammunition explosion destroys the 'Mech.
- Scenarios may have alternative victory conditions (hold an objective, escape, etc.) by mutual agreement or scenario rules.

## Special Rules & Edge Cases

### Prone 'Mechs
- A 'Mech may voluntarily drop prone (harder to hit at range, but vulnerable to melee).
- Standing up costs **2 MP** per attempt and requires a Piloting Skill Roll. The 'Mech may make repeated attempts as long as it has 2 MP remaining. Each attempt generates 1 heat point.

### Water
- Depth 1: 'Mechs wade (partial cover, reduced movement).
- Depth 2+: 'Mechs may be partially submerged; weapons may be restricted.

### Piloting Skill Rolls
- Required when: taking 20+ damage in a turn, losing a leg, being hit by a kick/charge, running on rough terrain, standing up.
- Roll 2d6 >= Piloting Skill + modifiers to stay standing. Failure = 'Mech falls prone.

### Critical Hits
- When internal structure takes damage, roll for critical hits.
- Roll 2d6: 2–7 = no critical hit; 8–9 = 1 critical hit location; 10–11 = 2 critical hit locations; 12 = Head/Limb Blown Off (if torso is hit, roll 3 critical hit locations instead).
- Critical hits disable equipment in the damaged location.

## Player Reference

| Movement Mode | MP Used | Heat Generated | To-Hit Modifier |
|--------------|---------|---------------|----------------|
| Standing | 0 | 0 | +0 |
| Walking | Up to Walk MP | 1 | +1 |
| Running | Up to Run MP | 2 | +2 |
| Jumping | Up to Jump MP | Jump MP used (min 3) | +3 |

| Attack Roll | 2d6 >= Target Number = Hit |
|------------|---------------------------|
| Base TN | Gunnery Skill (typically 4) |

| Damage Flow | Armor → Internal Structure → Critical Hits |
|------------|------------------------------------------|
