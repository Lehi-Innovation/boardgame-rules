---
title: "Android: Netrunner"
bgg_id: 124742
player_count: "2"
play_time: "45 min"
designer: "Richard Garfield, Lukas Litzsinger"
source_pdf: "android-netrunner-rules.pdf"
extracted_date: "2026-03-18"
summarized_date: "2026-03-18"
verification: "verified"
verification_date: "2026-06-13"
---
<!-- verification:begin -->
> ✅ **Verified** — this summary was fact-checked against the rulebook text and no significant issues were found.
>
> 📄 [Full rulebook text](https://jonnyallred.github.io/boardgame-rules/extracted/android-netrunner-rules.txt) · 🚩 [Report a rules error](https://github.com/Lehi-Innovation/boardgame-rules/issues/new?template=rule-error.yml&labels=rule-error&title=%5BRule%20error%5D%20Android%3A%20Netrunner&game=android-netrunner)
<!-- verification:end -->


## Overview

Android: Netrunner is an asymmetric two-player Living Card Game set in a cyberpunk future. One player is the Corp (corporation), installing and protecting agendas behind layers of ice (defensive programs). The other player is the Runner (hacker), making runs on the Corp's servers to steal those agendas. The Corp wins by scoring 7 agenda points or by flatline (the Runner takes more damage than the number of cards in his grip, or has a maximum hand size of less than zero at the end of his turn). The Runner wins by stealing 7 agenda points.

## Components

- Corp cards (identity, agendas, ice, assets, upgrades, operations)
- Runner cards (identity, programs, hardware, resources, events)
- Credit tokens, Advancement tokens, Tag tokens, Bad Publicity tokens
- Brain Damage tokens
- Click tracker
- Various token types

## Setup

1. Each player selects an Identity card (determines faction and deck-building rules).
2. Each player builds a deck (minimum deck size is determined by the chosen identity card; identities in the core set have a 45-card minimum).
3. The Corp's three central servers — R&D (draw deck), HQ (hand), and Archives (discard pile) — are a permanent part of the Corp's play area.
4. Each player draws 5 cards as a starting hand (mulligan option: shuffle back and draw 5 again, once).
5. Each player starts with 5 credits.

## Turn Structure

### Corp Turn

The Corp has 3 clicks per turn:
1. **Mandatory Draw:** Draw 1 card (free, not a click).
2. **Spend 3 Clicks:** Choose from available actions.
3. **Discard Phase:** Discard down to maximum hand size, if necessary.

### Runner Turn

The Runner has 4 clicks per turn. No mandatory draw.
1. **Spend 4 Clicks:** Choose from available actions.
2. **Discard Phase:** Discard down to maximum hand size, if necessary.

## Actions

### Corp Actions (1 click each unless noted)

| Action | Cost | Effect |
|--------|------|--------|
| Draw 1 card | 1 click | Take top card of R&D |
| Gain 1 credit | 1 click | Take 1 credit from bank |
| Install a card | 1 click | Place ice, asset, agenda, or upgrade in a server |
| Play an operation | 1 click | Play and resolve an operation card |
| Advance a card | 1 click + 1 credit | Place 1 advancement token on a card |
| Purge virus counters | 3 clicks | Remove all virus counters |
| Trash a resource | 1 click + 2 credits | Only if Runner is tagged |

### Runner Actions (1 click each unless noted)

| Action | Cost | Effect |
|--------|------|--------|
| Draw 1 card | 1 click | Take top card of Stack |
| Gain 1 credit | 1 click | Take 1 credit from bank |
| Install a card | 1 click | Install program, hardware, or resource |
| Play an event | 1 click | Play and resolve an event card |
| Make a run | 1 click | Initiate a run on a Corp server |
| Remove 1 tag | 1 click + 2 credits | Remove a tag token |

### Making a Run

1. Runner declares target server.
2. Runner approaches each piece of ice from outermost to innermost.
3. For each ice: the Corp may rez (pay to activate) ice only when it is being approached. Runner may use icebreakers to break subroutines. Unbroken subroutines fire (end run, deal damage, etc.).
4. If the Runner passes all ice, they access cards in the server.
5. Accessed agendas are stolen immediately — the Runner cannot decline to steal an accessed agenda. Other cards may be trashed by paying their trash cost.

## Scoring / Victory Conditions

| Condition | Winner |
|-----------|--------|
| Score/steal 7 agenda points | Corp scores, Runner steals |
| Runner takes more damage than the number of cards in his grip, or Runner's maximum hand size is below zero at end of his turn | Corp wins (flatline) |
| Corp must draw but R&D is empty | Runner wins (decked) |

## Special Rules & Edge Cases

- **Rezzing:** Corp pays the rez cost of ice or assets to activate them. Once rezzed, they stay active.
- **Tags:** The Runner can be tagged (by ice, operations, etc.). Tagged Runners are vulnerable: Corp can trash their resources, and certain cards deal extra damage to tagged Runners.
- **Damage Types:** Net damage (discard cards randomly from grip), meat damage (same), brain damage (permanently reduces hand size by 1 and discards 1 card from grip).
- **Memory Units (MU):** Runner has a memory limit (default 4 MU). Programs cost MU; excess programs must be trashed.
- **Unique cards:** Only 1 copy of a unique card can be installed at a time.
- **Ice Strength:** Icebreakers must match or exceed ice strength to interact with it. Boosting strength costs credits.

## Player Reference

**Corp Turn:** Mandatory draw + 3 clicks + Discard Phase

**Runner Turn:** 4 clicks + Discard Phase (no mandatory draw)

**Win Conditions:** 7 agenda points (either side) | Flatline (Corp) | R&D empty on draw (Runner)

**Server Types:**
- Central: R&D (deck), HQ (hand), Archives (discard)
- Remote: Created by Corp to hold agendas, assets, upgrades