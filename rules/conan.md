---
title: "Conan"
bgg_id: 160010
player_count: "2-5"
play_time: "60-90 min"
designer: "Frédéric Henry, Pascal Bernard, Antoine Bauza"
source_pdf: "conan-rules.pdf"
extracted_date: "2026-03-19"
summarized_date: "2026-03-19"
verification: "verified"
verification_date: "2026-06-17"
---
<!-- verification:begin -->
> ✅ **Verified** — this summary was fact-checked against the rulebook text and no significant issues were found.
>
> 📄 [Full rulebook text](https://jonnyallred.github.io/boardgame-rules/extracted/conan-rules.txt) · 🚩 [Report a rules error](https://github.com/Lehi-Innovation/boardgame-rules/issues/new?template=rule-error.yml&labels=rule-error&title=%5BRule%20error%5D%20Conan&game=conan)
<!-- verification:end -->


## Overview

Conan is an asymmetric miniatures board game set in Robert E. Howard's Hyborian Age. One player is the Overlord controlling monsters, villains, and minions, while the other players each control one hero (Conan and his companions). The game is scenario-driven; each scenario defines the map, forces, objectives, and time limit. The Overlord has a unique "Book of Skelos" energy management system. Heroes must complete objectives before time runs out.

## Components

- Modular game boards
- Painted miniatures (heroes, monsters, minions)
- Hero character sheets
- Overlord "Book of Skelos" board with Overlord tiles
- Energy gems
- Dice (various colors for attack/defense)
- Equipment cards, spell cards
- Scenario booklet
- Tokens (wounds, special conditions)

## Setup

1. Select a scenario from the scenario booklet.
2. Assemble the game board per scenario map.
3. The Overlord places minion and monster miniatures per scenario.
4. Each hero player selects their hero and takes their character sheet.
5. The Overlord sets up the Book of Skelos with Overlord tiles in the specified order.
6. Distribute starting equipment cards to heroes.
7. Place energy gems per hero and Overlord setup.

## Turn Structure

Heroes and the Overlord alternate turns (starting side set by scenario). The heroes' turn has four phases in order:

### 1. Start Phase
All energy gems the heroes spent during the Overlord's turn are moved to their Fatigue zone.

### 2. Stance Phase
Each hero chooses **aggressive** or **cautious** stance, then recovers gems from their Fatigue zone to their Reserve zone:

| Stance | Heroes alive (none dead) | 1 dead | 2+ dead | Restrictions |
|--------|--------------------------|--------|---------|--------------|
| Aggressive | 2 gems | 3 gems | 4 gems | May perform any action |
| Cautious | 5 gems | 6 gems | 7 gems | May only Guard and Reroll; cannot Move, Melee Attack, Ranged Attack, Manipulate, drop objects, or cast spells (except reaction spells) |

### 3. Action Phase
Aggressive heroes act in any order, freely coordinating. A hero may act, then hand off to a companion, then act again later. The phase ends when heroes cannot or choose not to act further. (Heroes may save gems in Reserve to Guard during the Overlord's turn.)

### 4. End Phase
Each hero moves all gems from their action spaces, ally tiles, and spell cards to their Fatigue zone. Play passes to the Overlord.

### Overlord Turn
The Overlord uses the Book of Skelos energy system:
1. The Overlord has a track of tiles representing minion groups.
2. To activate a tile, the Overlord spends gems to slide the tile, activating that minion group.
3. Tiles at the far end of the track are cheaper to activate; recently used tiles cost more.
4. Activated minions can move, attack heroes, and perform special actions.
5. The turn marker advances one space at the start of the Overlord's turn.

## Actions

### Hero Actions
| Action | Effect |
|--------|--------|
| **Move** | At the start of the Action phase, an aggressive hero gains free movement points equal to their base movement value (no gems required). To move beyond that, assign 1 gem to the Move space per extra movement point. Crossing one area border costs 1 movement point; terrain effects and hindering can increase this cost. |
| **Melee Attack** | Spend gems for attack dice; roll against target's defense |
| **Ranged Attack** | Spend gems to fire at targets in line of sight |
| **Manipulation** | Interact with scenario objects (pick locks, carry items) |
| **Guard** | Reserve gems for defensive rerolls during enemy attacks |
| **Reroll** | Spend gems to reroll dice |

### Overlord Actions
- Activate minion groups by spending gems and sliding tiles.
- Minions move and attack heroes per their stats.
- Play event cards for special effects.
- Use monster special abilities.

### Combat
1. Attacker spends gems and rolls attack dice (orange = weak, red = strong).
2. Defender rolls defense dice.
3. Each hit symbol on attack dice minus each shield on defense dice = wounds.
4. Heroes have wound tracks; filling it means defeat.
5. Minions typically have 1 life point each.

## Scoring / Victory Conditions

Scenario-dependent. Typically:
- **Heroes win** by completing the scenario objective within the time limit (turns).
- **Overlord wins** by preventing heroes from completing objectives, killing all heroes, or running out the clock.

## Special Rules & Edge Cases

- **Stance and gem recovery** is the core resource loop: heroes choose aggressive (2 gems recovered, full actions) or cautious (5 gems recovered, Guard/Reroll only) each turn. More heroes dead = more gems recovered regardless of stance.
- **Guard** lets heroes assign gems to roll defense dice when attacked; a hero can Guard during the Overlord's turn using gems saved in their Reserve zone.
- **Armor** is a passive defense bonus from equipment that applies to every attack automatically, whether or not the hero Guards.
- **Hindering:** When enemies in an area equal or outnumber friendly characters, moving out costs extra movement points and rolled dice have symbols ignored. Melee attacks and Guard are not affected by hindering.
- **Wound zone:** When a hero takes damage, gems move first from Fatigue zone, then from action spaces/spell cards/ally tiles, then from Reserve zone. A hero dies when all gems are in the Wound zone.
- **Line of sight** matters for ranged attacks; models do not block LoS but can hinder ranged attacks.
- **Equipment cards** provide permanent or one-use bonuses (weapons, shields, items).
- **Spells** are cast by assigning gems to the spell card; gems on spell cards are moved to Fatigue at the end of each turn (End Phase).
- The Overlord's tile sliding mechanic means recently activated groups are expensive to reactivate, forcing strategic rotation.
- Some scenarios have special rules for reinforcements, traps, or environmental effects.

## Player Reference

| Dice Colors | Power Level |
|------------|-------------|
| Yellow | Weakest |
| Orange | Medium |
| Red | Strongest |

**Hero Energy Cycle:**
Gems start in Reserve zone → Assigned to action spaces → Move to Fatigue zone at End Phase → Recovered to Reserve zone during Stance Phase (amount depends on stance and number of fallen heroes).

Gems lost to damage move from Fatigue → Wound zone (then from action spaces/spell cards, then from Reserve). Hero dies when all gems are in Wound zone.

**Stance Recovery Summary:**

| Stance | 0 dead | 1 dead | 2+ dead |
|--------|--------|--------|---------|
| Aggressive | 2 | 3 | 4 |
| Cautious | 5 | 6 | 7 |
