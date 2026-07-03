---
title: "Conflict of Heroes: Awakening the Bear! – Russia 1941-42"
bgg_id: 24800
player_count: "2-4"
play_time: "60-120 min"
designer: "Uwe Eickert"
source_pdf: "conflict-of-heroes-awakening-the-bear-russia-1941-42-rules.pdf"
extracted_date: "2026-03-19"
summarized_date: "2026-03-19"
verification: "verified"
verification_date: "2026-06-17"
---
<!-- verification:begin -->
> ✅ **Verified** — this summary was fact-checked against the rulebook text and no significant issues were found.
>
> 📄 [Full rulebook text](https://jonnyallred.github.io/boardgame-rules/extracted/conflict-of-heroes-awakening-the-bear-russia-1941-42-rules.txt) · 🚩 [Report a rules error](https://github.com/Lehi-Innovation/boardgame-rules/issues/new?template=rule-error.yml&labels=rule-error&title=%5BRule%20error%5D%20Conflict%20of%20Heroes%3A%20Awakening%20the%20Bear%21%20%E2%80%93%20Russia%201941-42&game=conflict-of-heroes-awakening-the-bear-russia-1941-42)
<!-- verification:end -->


## Overview

Conflict of Heroes: Awakening the Bear is a tactical WWII wargame covering Operation Barbarossa (1941-42) on the Eastern Front. Each counter represents a squad of infantry, a crewed gun, or a vehicle. The game uses an action point system where players alternate taking individual turns. Engagements are presented as firefights with different objectives worth victory points. The game is structured to teach rules progressively through scenarios.

## Components

- Hex map boards
- Unit counters (German and Soviet squads, guns, vehicles)
- Track sheets with Unit AP Track (green) and CAP Track (blue)
- Dice (2d6, and 3d6 for optional variable AP rule)
- Action cards (shuffled and dealt per firefight)
- Hit markers (drawn randomly from a pool; placed face-down)
- Spent markers (red-bar side of unit counters)
- Control markers (for victory hexes)
- Round marker

## Setup

1. Choose a firefight. The firefight sheet specifies units, map configuration, starting CAPs, number of rounds, and victory conditions.
2. Each player takes a track sheet and places a yellow victory point marker on 0 VPs and marks their starting CAPs on the blue CAP track.
3. Sort out units listed in the firefight and configure the maps as described.
4. Place units in their starting positions as specified.
5. Shuffle the hit markers face-down (effects side down, optionally into opaque cups for random drawing).
6. Select the action cards specified by the firefight; shuffle and deal each player the specified number.
7. Note any hidden units or artillery targets on paper.

## Turn Structure

A firefight consists of a set number of rounds. Each round proceeds as follows:

**Pre-Round Sequence (at the start of every round):**
1. Flip all spent unit counters back to their fresh sides.
2. Reduce or remove smoke counters.
3. Reset CAPs to starting value minus 1 per unit lost (CAPs do not carry over between rounds).
4. Draw cards specified by the firefight.
5. Target off-board artillery for next round; resolve artillery targeted last round.
6. Prepare reinforcements per firefight.
7. Both players roll 2d6 for initiative; highest result takes the first turn (re-roll on tie). Players may spend up to 2 CAPs to modify the roll.

**During the Round — Alternating Turns:**

On each turn, a player may take one of four actions:
1. **Unit (AP) Action:** Choose any fresh unit and activate it by setting the green Unit AP Track to 7 APs. The activated unit may then spend APs to take actions one at a time in subsequent turns. A player may have only one activated unit at a time; activating a new unit marks the current one as spent. An activated unit retains its remaining APs across multiple turns.
2. **Opportunity Action:** Take any one action (costing any number of APs) with any *fresh* (not yet activated or spent) unit. The unit is marked as spent after the action. This does not cost APs or CAPs from the player's pool.
3. **Command (CAP) Action:** Take one action with any fresh, activated, or spent unit by paying only CAPs. The unit's status is unchanged.
4. **Card Action:** Play an action card on any fresh, activated, or spent unit. The unit's status is unchanged.

A player may also **Stall** (costs 1 AP from the activated unit or 1 CAP) or **Pass** (costs nothing, but a currently activated unit must be marked spent and loses remaining APs). If both players pass consecutively, the round ends immediately.

**Round End:** Victory points are awarded, the round marker is advanced, and the next pre-round sequence begins.

**Game End:** The firefight ends after the last round is played, or when a firefight's victory conditions have been met.

## Actions

### Fire

The AP cost to fire is printed on the **top left corner** of the counter and varies by unit. Each fire action is a separate action. To fire, the attacking unit must have the target in its arc of fire, LOS, and range.

**Attack Value (AV):** AV = Unit Firepower (FP) + 2d6 roll. Up to 2 CAPs may be spent to modify the dice roll.

**Defense Value (DV):** DV = Unit Defense Rating (DR) + terrain defense modifier (DM). Fire from outside the target's arc of fire is a **flank attack** resolved against the weaker flank DR.

- Red FP is used against red (soft/unarmored) DR targets; blue FP against blue (armored) DR targets.
- If AV ≥ DV: the defender takes one hit (draw a hit marker randomly from the pile and place it face-down under the unit).
- **Critical Hit:** If AV > DV by 4 or more, the defender is immediately destroyed.
- If AV < DV: miss.

### Hit Markers

When a unit is hit, a hit marker is randomly drawn from the pile and placed face-down under the unit. Hit marker effects vary; examples include:
- **Stunned:** Unit can take no action other than rally.
- **Suppressed:** Unit's FP is reduced (specifics on the marker).
- **Panicked:** Unit cannot fire; flank DR increases.
- **Unnerved:** No stats affected.
- **KIA:** Unit is immediately killed on the first hit — remove it from the map.

Some vehicle hit markers are marked **No Rally** and cannot be removed. A unit that takes a second hit draws another marker independently (each hit marker's effect applies).

### Move

Foot units have a red movement cost in the **top right corner** of the counter. Moving into a hex costs the unit's movement cost in APs plus any terrain surcharge. Each hex moved is a separate action. There are **no stacking limits** — units may move through hexes occupied by friendly or enemy units (enemy close combat may result).

### Rally

A hit unit may attempt to remove one hit marker by rallying. Cost: **5 APs**. After paying, roll 2d6. If the result is ≥ the rally number on the hit marker, the rally succeeds and the marker is removed. Units may also rally via opportunity, command, or card actions. Each rally attempt is a separate action. Units in a hex with enemy units cannot rally. Some modifiers apply (e.g., cover terrain adds +1 to the roll; up to 2 CAPs can modify the roll).

### Opportunity Action

A fresh unit (not activated or spent) may take any one action as an opportunity action. The action's full AP cost is paid from the unit's own pool (the unit is set to 7 APs momentarily, takes one action, then is marked spent). This does not cost the active player any APs from the current activated unit or CAPs.

### Group Actions

Units in the same hex or continuous adjacent hexes may group move (and take other group actions). The total cost equals the highest movement cost among the grouping units. Each unit in the group is marked spent after the group action. Group rally and other group actions follow the same structure.

### Command (CAP) Actions

CAPs may be used to:
- Supplement an activated unit's APs on a 1-for-1 basis (spend as many CAPs as desired).
- Pay entirely for a command action by any fresh, activated, or spent unit without changing its spent/fresh status.
- Modify any dice roll (up to 2 CAPs, +1 per CAP) — must be declared before rolling.
- Stall (1 CAP), or pay costs for card actions.

## Scoring / Victory Conditions

Each firefight has specific VP objectives listed on the firefight sheet. Victory points are earned:
- **Immediately** when an enemy unit is destroyed (VP value recorded on the VP track). If a player destroys his own unit, the opponent gets those VPs.
- **During play** by controlling victory hexes (marked with control markers; control transfers when an opposing ground unit solely occupies the hex, even if it just passes through).
- **Special objectives** as defined per firefight.

The side with the highest VP total when the firefight ends is declared the winner. In case of a tie, both players lose.

A player can lose most of his command but still win if he has met his victory conditions and has more VPs than his opponent.

## Special Rules & Edge Cases

- **No stacking limits:** Units may occupy the same hex freely; stacked units are each attacked separately with separate dice rolls (one fire action hits all in the hex, at no extra AP cost).
- **CAPs reset each round:** CAPs are not carried over between rounds. The starting CAP total is reduced by 1 for each unit the player has lost in the game so far (placing destroyed units on the CAP track marks this reduction).
- **Flank attacks:** Fire originating from outside a unit's arc of fire is a flank attack, resolved against the unit's flank DR (printed above the front DR on the counter). Flank DR is typically weaker.
- **Vehicles** have separate front and flank DR values (blue for armored). Turreted vehicles can rotate their arc of fire without pivoting.
- **Facing:** Units have a forward facing and an arc of fire. Changing facing is not free for vehicles; pivoting costs 1 AP or 1 CAP.
- **Opportunity actions** allow a fresh unit to react immediately (fire, move, rally, etc.) without spending the activated unit's APs or any CAPs — but the acting unit is marked spent.
- **Action cards** are dealt at round start per the firefight. Playing a card is a Card Action; the affected unit's status is unchanged.
- **Line of sight (LOS):** LOS must be clear from the center of the attacker's hex to the center of the target's hex. Units do not block LOS. Terrain can block or hinder LOS.
- **Suppression and other hit effects** are drawn randomly from the hit marker pile and apply per the text on the marker.
- **Reinforcements** enter the map at locations specified by the firefight.
- **Programmed instruction:** The rulebook is organized to teach rules section by section with practice firefights between sections.

## Player Reference

| Counter Layout (Foot Units) |
|-----------------------------|
| Top left: AP cost to fire |
| Top right: Movement cost (red = foot unit) |
| Lower left: Firepower (red FP vs soft targets; blue FP vs armored targets) |
| Lower right: Defense Rating (red = soft/unarmored; blue = armored) |
| Flank DR printed above the front DR on the counter face |

| Action Point Budget |
|-------------------|
| Each unit when activated: 7 APs (set on green Unit AP Track) |
| CAPs: Shared pool per player (varies by scenario; resets each round minus 1 per unit lost; not carried over) |
| Rally cost: 5 APs |
| Fire cost: varies by unit (top left of counter; typically 2–4 APs) |
| Move cost: varies by unit and terrain (top right of counter plus terrain surcharge) |
| Stall: 1 AP from activated unit or 1 CAP |
