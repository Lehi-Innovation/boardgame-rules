---
title: "Aftermath"
bgg_id: 281946
player_count: "1-4"
play_time: "90 min"
designer: "Jerry Hawthorne"
source_pdf: "aftermath-rules.pdf"
extracted_date: "2026-03-18"
summarized_date: "2026-03-18"
verification: "inaccurate"
verification_date: "2026-07-02"
---

# Aftermath

<!-- verification:begin -->
> ❗ **Known errors** — an audit found inaccuracies in this summary that could mislead players: Re-audit+fix: omits the entire Enemy Turn combat-resolution phase and Defeated Enemy/Character rules that Turn Structure invokes. Until it is re-written, prefer the full rulebook text linked below.
>
> 📄 [Full rulebook text](https://jonnyallred.github.io/boardgame-rules/extracted/aftermath-rules.txt) · 🚩 [Report a rules error](https://github.com/Lehi-Innovation/boardgame-rules/issues/new?template=rule-error.yml&labels=rule-error&title=%5BRule%20error%5D%20Aftermath&game=aftermath)
<!-- verification:end -->

## Overview

A cooperative adventure book game where players are small rodents surviving in a post-apocalyptic world after a mysterious "Calamity" wiped out humanity. Players explore dangerous terrain, forage for supplies, accomplish missions, and battle vicious predators. The game uses an Adventure Book with illustrated maps, a campaign system with persistent progression, and deck-building mechanics for character abilities.

## Components

- 1 Rulebook and 1 Adventure Book
- 23 Plastic figures
- 2 Resolution dice
- 1 Sideboard and 1 Campaign Dashboard
- 1 Downtown Travel Map
- 47 Card Discovery Deck
- 4 Character cards
- 37 Basic Action cards, 4 Character Influence cards
- 51 Item cards, 17 Status cards, 20 Ability cards
- 17 Encounter cards, 8 Mission cards, 22 Enemy cards, 10 Environment cards
- 13 Vehicle Travel cards
- Various tokens: Situation, Wound (25), Scavenge (21), Battery (8), Objective (4), Fire (5), Roach (8), and more
- Vehicle standees (Truck, Jeep, Enemy vehicles)
- Deck boxes for Discovery, Banished, Character, and Colony Supply

## Setup

Follow the Adventure Book for scenario-specific setup. General setup includes placing character figures, building action decks, setting up the sideboard with enemy and environment cards, and reading the Adventure Book entry for the current mission.

## Turn Structure

Players take individual turns in clockwise order. Each player's turn consists of five steps in order:

1. **Draw:** Draw until you have 5 action cards in hand. You may discard any cards from a previous turn before drawing.
2. **Resolve Calamity:** If you drew the Calamity card, reveal and discard it. Roll the black die and add the result to the current Time dial value. If the total equals or exceeds the Calamity threshold on the current Adventure Book page, resolve the Calamity entry.
3. **Place Threat:** Place any threat (black) cards drawn onto the threat track in random order.
4. **Perform Actions:** Play action cards to perform as many actions as you like.
5. **Check Threat:** If the situation is **safe** and there are 4 or more threat cards on the threat track, go to the Calamity entry. If the situation is **hostile** and the number of threat cards equals or exceeds the number of enemies on the threat track, resolve an enemy turn.

## Actions

### Player Actions
- **Move**: Play action cards; total value = movement points. Spend 1 point to cross a dashed line; 3 points to cross a solid colored line (unless all played cards match that line's color).
- **Melee Attack**: If the situation is hostile, target an enemy in your space. Resolve an opposed Strength skill test against the enemy's defense value. Success inflicts 1 wound.
- **Ranged Attack**: If the situation is hostile, target an enemy up to 1 space away (or farther with a ranged weapon) within line of sight. Resolve an opposed Agility skill test against the enemy's defense value. Success inflicts 1 wound.
- **Scavenge**: Target a Scavenge token on your space. Resolve an Instinct skill test at the token's difficulty. Success gains the listed prize.
- **Communicate**: Only when the situation is safe. Target an enemy sharing your space. Resolve an opposed Instinct skill test at that enemy's communication value. Success removes the enemy and 1 threat card from play and increases the Morale dial by 1. Failure makes the situation hostile.
- **Recover**: Attempt to remove a negative status effect by resolving the skill test on that status card.
- **Activate Ability**: Play white cards with combined value equal to or greater than the ability's cost to use a character ability.
- **Encourage**: Give an action card to a player who has 2 or fewer action cards in hand.
- **Equip/Trade**: Discard any action card to move items between equipped slots and backpack, or exchange items with a character sharing your space.

### Resolution Dice
Most actions require a skill test. Play an action card with the matching attribute symbol, then optionally play additional cards matching the first card's color or number value. Roll the white resolution die and add: die result + card value(s) + character attribute bonus + equipped item bonuses. If the total equals or exceeds the difficulty, the test succeeds. For **opposed** skill tests, also roll the black resolution die and add its result to the difficulty.

### Character Classes
Each character has a unique species, class, starting ability, starting item, attribute bonuses, and a personal goal.

## Scoring / Victory Conditions

**Campaign Win:** To win the campaign, players must complete the personal goal of at least 4 characters. Once a goal is completed it stays completed regardless of future game state.

**Campaign Loss:** If the Food dial or the Morale dial on the campaign dashboard ever reaches 0, the campaign is lost. Players must go to Adventure Book page 100, entry 100-23, then reset and start a new campaign.

**Mission Success/Failure (per session):** Players complete the main mission goal as described in the Adventure Book. If all characters are simultaneously defeated (out of play), the main mission fails. Going over a mission's allotted Time does not immediately fail the mission, but exposes the colony to greater risk per Adventure Book resolution.

## Special Rules & Edge Cases

- **Nesting:** At the end of any player's turn when the situation is safe, the party may nest: (1) each character may spend 1 Food to remove 1 normal wound; (2) all toxic wounds become normal wounds; (3) discard all negative status effects; (4) discard all batteries from items; (5) spend Scrap to repair broken items; (6) Time +1.
- Campaign persistence: Items, abilities, and discoveries carry between sessions via deck boxes.
- Colony Supply deck represents the shared resources of the mouse colony.
- Banished deck box holds permanently removed cards.
- Vehicle travel uses special cards and rules.
- Each character has a personal goal listed on their character card; completing the personal goals of at least 4 characters is required to win the campaign.
- Enemy behavior is determined by threat cards: the value on the threat card under each enemy card selects that enemy's action for its activation.

## Player Reference

### Character Stats
- Name, Class, Species
- Attribute Bonuses (varies by character)
- Starting Ability and Item
- Life Value
- Personal Goal

### Key Token Types
| Token | Purpose |
|-------|---------|
| Wound | Damage tracking |
| Scavenge | Resource collection |
| Battery | Power source |
| Objective | Mission goals |
