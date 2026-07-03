---
title: "City of Heroes Collectible Card Game"
bgg_id: 19766
player_count: "2"
play_time: "30 min"
designer: "David Williams"
source_pdf: "city-of-heroes-collectible-card-game-rules.pdf"
extracted_date: "2026-03-19"
summarized_date: "2026-03-19"
verification: "verified"
verification_date: "2026-06-17"
---
<!-- verification:begin -->
> ✅ **Verified** — this summary was fact-checked against the rulebook text and no significant issues were found.
>
> 📄 [Full rulebook text](https://jonnyallred.github.io/boardgame-rules/extracted/city-of-heroes-collectible-card-game-rules.txt) · 🚩 [Report a rules error](https://github.com/Lehi-Innovation/boardgame-rules/issues/new?template=rule-error.yml&labels=rule-error&title=%5BRule%20error%5D%20City%20of%20Heroes%20Collectible%20Card%20Game&game=city-of-heroes-collectible-card-game)
<!-- verification:end -->


## Overview

The City of Heroes Collectible Card Game is a two-player (or multiplayer) CCG based on the City of Heroes MMORPG. Players build decks around hero archetypes (Blaster, Scrapper, Defender, Controller, Tanker) and battle each other using a continuous alternating-priority structure. There are no phases or turn structure — the active player takes one action, then priority passes to the next player.

## Components

- Hero cards (one per player; each has accuracy, defense, health, archetype, travel power, powersets, and starting powers)
- Sidekick cards (minor supers that help your hero)
- Power cards (attach to supers; click-based abilities)
- Enhancement cards (attach to powers; modify power abilities)
- Edge cards (one-time-use ability cards)
- Mission cards (stay in play; represent villain influence with threats and rewards)

## Setup

1. Each player searches their deck for their hero card and that hero's starting powers, then simultaneously reveals them. The hero enters play in Toe-to-Toe tactics mode with starting powers attached.
2. All players shuffle their decks and present them to an opponent for an optional cut.
3. Each player draws a starting hand of 5 cards.
4. Choose a starting player at random. All players agree on subsequent turn order (default: clockwise). The starting player receives priority and the game begins.

## Turn Structure

There are no phases. The game is played by players taking actions in turn order:

1. The active player (the player with priority) chooses and performs one action.
2. After the action and all subsequent reacts resolve, priority passes to the next player.
3. Repeat continuously — there is no end-of-turn or round structure.

## Actions

Each time a player has priority they must choose exactly one of the following actions:

### Power Up
Choose a power, enhancement, or sidekick card from hand and put it into play. Powers and enhancements attach to a chosen super (discarded if requirements not met or a copy is already attached). Only one sidekick may be in play at a time.

### Act
Choose an edge card from hand, an innate ability on a super you control, or a ready power attached to a super you control. Pay costs (including charging the power), choose targets, and resolve effects. Attack abilities (Melee or Ranged) follow a specific resolution sequence: pay costs → charge power → declare targets and pay any chasing costs → compare accuracy vs. defense (accuracy ≥ defense = hit; accuracy < defense = miss).

### Move
Choose one of your supers. That super switches tactics mode between Toe-to-Toe and Run-'n'-Gun.

### Assemble
Search your deck for a sidekick card, reveal it, and put it in your hand. Shuffle and present for a cut afterward.

### Recharge
Recharge all powers attached to supers you control one click toward ready. (A toggle power that is turned on may be skipped.)

### Mission
Play a mission card from hand into play. Any previously in-play mission is discarded. A player may not have more than one mission in play, and a mission of the same name may not be re-played once completed.

### Rest
Draw two cards.

### Defeat
Pay the defeat cost on a mission currently in play to complete it. Place the completed mission under one of your supers to record the completion. Cannot be taken if no mission with a defeat cost is in play.

### Power Down
Turn off an active toggle power you control.

## Scoring / Victory Conditions

- **Single player (2-player) game:** A player loses when their hero's health total is 0 or less when priority is passed. The last player whose hero has health greater than zero wins.
- **Multiplayer game:** A team wins when it is the only team with at least one hero with a health total greater than zero.

There is no tiebreaker rule specified for simultaneous hero defeats.

## Special Rules & Edge Cases

### Click System (Charging Powers)
Powers are the only cards that can be clicked. Powers have a charging icon: click powers require 1, 2, or 3 clicks to activate; toggle powers require 2 clicks to turn on (turned off by Recharge or Power Down action); constant powers (marked "C") are not charged when activated. A power may have at most 3 clicks; effects cannot charge it further. A super may not have more than 2 toggle powers turned on at the same time.

### Tactics Modes
Every super is always in exactly one of two tactics modes: **Toe-to-Toe** (close range) or **Run-'n'-Gun** (ranged). Tactics mode affects chasing costs for attacks. Missions are always considered Toe-to-Toe. Chasing costs (paid by discarding cards) apply as follows:
- Melee attack, attacker Toe-to-Toe, target Run-'n'-Gun: discard 1 card.
- Melee attack, both in Run-'n'-Gun: discard 2 cards.
- Ranged attack, both in Run-'n'-Gun: discard 1 card.
- All other combinations: no chasing cost.

### Reacts
Reacts are abilities that can be played outside the normal action structure at specific trigger moments (before, when, or after a specified event). Playing a react does not use up the player's next action. Multiple players may react to the same trigger; start with the active player and proceed in turn order.

### Inspirations
Almost every non-hero card has an inspiration icon (Insight, Luck, Respite, Catch a Breath, Break Free, or Enrage). Any such card may be discarded from hand to use its inspiration ability instead of its printed abilities. Inspiration abilities:
- **Insight:** React — when your super targets with an attack: +2 Accuracy for that attack.
- **Luck:** React — when your super is targeted by an attack: +2 Defense for that attack.
- **Respite:** Action — Heal one of your supers 2 hit points.
- **Catch a Breath:** Action — Draw three cards.
- **Break Free:** React — before performing an action: end 1 status effect on one of your supers.
- **Enrage:** React — before targeting an attack: the attack does +1 damage (of each damage type).

### Archetypes and Travel Powers
Archetypes (Blaster, Scrapper, Defender, Controller, Tanker) and travel powers (Flight, Superspeed, Superjump, Teleport) have **no inherent abilities**. They are referenced by card text requirements and effects only.

### Status Effects
There are three status effects: Stun, Knockdown, and Immobilize.
- **Stun:** The super may not be chosen for Move, and none of its powers may be chosen for an Act action (innate abilities are still usable). Receiving Stun also turns off all toggle powers.
- **Knockdown:** Controller must discard 2 cards as an additional cost to choose this super for Move, or to choose one of its powers for an Act action (innate abilities are unaffected).
- **Immobilize:** The super may not be chosen for Move; chasing costs during its attacks cannot be paid.

Status effects have a duration measured in actions of the affected player. Multiple instances of the same status effect do not combine durations.

### Missions
Mission cards have defense and health. They may be attacked like an opposing super (always treated as Toe-to-Toe). A mission is completed when its health reaches 0 or its defeat cost is paid during a Defeat action. Once completed, the mission is placed under the super that defeated it.

### Hand Size and Deck
Maximum hand size is 10 cards; excess must be discarded immediately. If a player's deck is ever empty, the discard pile is shuffled and becomes the new deck (cut offered to an opponent). Constructed format: minimum 40 cards. Limited format: minimum 25 cards. Maximum 3 copies of any individual card in either format.

### Card Text Overrides Rules
Any time a card contradicts these rules, the card takes precedence. If one card says you can do something and another says you can't, the prohibition takes precedence.

## Player Reference

| Action | Effect |
|--------|--------|
| Power Up | Put a power/enhancement/sidekick from hand into play |
| Act | Use an edge, innate ability, or ready power (includes attacks) |
| Move | Switch one of your supers between Toe-to-Toe and Run-'n'-Gun |
| Assemble | Search deck for a sidekick, put it in hand; shuffle and cut |
| Recharge | Recharge all your powers one click toward ready |
| Mission | Play a mission card from hand into play |
| Rest | Draw two cards |
| Defeat | Pay defeat cost on a mission in play to complete it |
| Power Down | Turn off an active toggle power you control |

| Inspiration | Ability |
|-------------|---------|
| Insight | React: +2 Accuracy to your attack |
| Luck | React: +2 Defense when your super is targeted |
| Respite | Action: Heal 2 hp on one of your supers |
| Catch a Breath | Action: Draw three cards |
| Break Free | React: End 1 status effect on one of your supers |
| Enrage | React: +1 damage (each type) to your attack |
