---
title: "Bonaparte at Marengo"
bgg_id: 15839
player_count: "2"
play_time: "120 min"
designer: "Bowen Simmons"
source_pdf: "bonaparte-at-marengo-rules.pdf"
extracted_date: "2026-03-18"
summarized_date: "2026-03-18"
verification: "verified"
verification_date: "2026-06-17"
---
<!-- verification:begin -->
> ✅ **Verified** — this summary was fact-checked against the rulebook text and no significant issues were found.
>
> 📄 [Full rulebook text](https://jonnyallred.github.io/boardgame-rules/extracted/bonaparte-at-marengo-rules.txt) · 🚩 [Report a rules error](https://github.com/Lehi-Innovation/boardgame-rules/issues/new?template=rule-error.yml&labels=rule-error&title=%5BRule%20error%5D%20Bonaparte%20at%20Marengo&game=bonaparte-at-marengo)
<!-- verification:end -->


## Overview

Bonaparte at Marengo is a two-player wargame simulating the Battle of Marengo on June 14, 1800. One player controls the French and the other the Austrians. The game plays over 16 rounds (each representing one hour). The Austrian army enters from the west and attempts to destroy French forces and drive east to control the map. The French start scattered, with some pieces needing activation before they can move. There are no dice — combat is resolved by strength comparison with terrain effects designed into the map. Pieces are normally face-down (fog of war): only the owning player sees a piece's type and strength.

## Components

- 80 wooden block playing pieces (French=blue, Austrian=red)
  - Infantry pieces (1–3 strength)
  - Cavalry pieces (1–2 strength)
  - Artillery pieces (1 strength)
  - Replacement pieces for handling losses
- 1 Game board (22" × 30" map of Marengo battlefield)
- 3 Markers (1 time track, 2 morale)
- 2 Rules booklets

## Setup

1. Place marker on 6:00 AM on the Time Track.
2. Place morale markers at their printed starting positions on the Morale Track.
3. Sort pieces: French "At Start" group, four Reinforcement Entry groups (one Austrian, three French), and replacement pieces.
4. **French At Start:** Austrian player shakes French At-Start pieces in a box without looking. French player blind-draws the correct number for each starting locale and places pieces face-down.
5. Reinforcement pieces are turned face-down by their owner. Players may shuffle to conceal piece identities.
6. French pieces on the map at start cannot move until activated (see French Activation below).

### French Activation
French at-start pieces are inactive (cannot move) until activated:
- Automatically activated if an adjacent locale is enemy-occupied at the start of the French player's turn.
- French player may select pieces for activation: 1 piece on the very first turn; 2 pieces per turn thereafter, provided a French setup locale was ever enemy-occupied or it is 11:00 AM or later.

Once activated, a piece stays activated. French reinforcements do not need to be activated; they can move normally when they enter play. An inactive (unactivated) piece may still block or retreat from maneuver attacks even though it cannot move.

## Turn Structure

**16 rounds**, each divided into two turns: Austrian first, then French.

Each turn has 4 steps:
1. **Resolve artillery bombardments** declared in the previous turn.
2. **Conduct assaults** (infantry and cavalry assaults).
3. **Conduct movement.**
4. **Declare artillery bombardments** for the next turn.

After each round, advance the Time Track marker by one space.

**Command Limit:** A player may move no more than 3 groups and/or conduct no more than 3 assaults per turn (combined). Exceptions that do **not** count against the limit: blocking a maneuver attack, conducting artillery bombardments, retreating, and moving by primary road.

## Actions

### Movement
- Each piece may either move within its locale (reserve ↔ blocking) or move to an adjacent locale.
- Moving to a non-adjacent locale in one turn requires road movement: the piece must start its turn in reserve in a locale with a road, and every approach/locale it passes through must be connected by an unbroken road and not occupied by enemy pieces. Road moves are always single pieces; a piece is in reserve at the end of a road move.
- **Road capacity:** only 3 pieces may cross any one approach by any one road in a single turn. The first piece to cross is on its first move of the turn and may move 3 locales; the second piece is on its second move and may move 2 locales; the third piece is on its third move and may move 1 locale. Moves must be made in order (a piece on an earlier move cannot cross after a piece on a later move) and in the same direction; a piece may wait on one of its moves so another piece can use the road. An approach crossed by more than one road has independent capacity per road.
- **Primary road movement:** unlimited per turn; does not count against the command limit.
- Cannot exceed a locale's printed capacity limit (applies to the entire locale — no sub-limits for reserve vs. blocking).
- A piece may block an approach only if the locale opposite that approach is enemy-occupied. If enemy pieces leave, the blocking pieces must move into reserve.
- Cannot move across an impassable approach or an approach blocked by enemy pieces (blocked approaches may only be crossed by assault).

### Reinforcement Entry
- A reinforcement piece enters the map using road movement from its entry point, following the same road-capacity rule as normal road movement: the first piece to enter from a given entry point in a turn is on its first move and may move 3 locales, the second is on its second move and may move 2 locales, and the third is on its third move and may move 1 locale.
- A piece may not enter if the entry locale is at its capacity limit or enemy-occupied; it must wait until the condition no longer applies. If more pieces are waiting than can enter in one turn, the remainder enter in later turns.
- Order of entry among a player's own reinforcements is up to that player, and entry is entirely optional each turn — a player is never required to bring in reinforcements just because he is able to.
- **Austrian pontoon bridge exception:** in addition to road entry, the Austrian player may bring in one additional piece per turn using non-road movement (representing the historical Bormida pontoon bridge). This piece is likewise barred from entering if the entry locale is at capacity or enemy-occupied, and it counts as its own separate group for the command limit.

### Maneuver Attacks
A maneuver attack occurs when friendly pieces move into an enemy-occupied locale across an approach that is **not** blocked by enemy pieces:
- **Blocking is possible only if both conditions hold:** (1) the attacking pieces started their turn in reserve — if the attacking pieces started their turn already blocking the approach, the attack cannot be blocked; and (2) the enemy (defending) player has one or more pieces in reserve in the locale. Only when both conditions are met may the defender choose to block, by moving one or more of those reserve pieces to block the approach. (This does not count against the defender's command limit.)
- **Blocked result:** The attacker may leave pieces in place, advance to block the opposite approach, or split the group (costs an extra command). No strength comparison — the block simply stops the advance.
- **Successful result:** If the two conditions above are not both met, or the defender chooses not to block, all defending pieces in the locale must retreat (see Retreats). The attacking pieces then move into reserve in that locale.
- *Note: There is no strength comparison in a maneuver attack. The attack either is blocked by the defender's choice (only possible when both gating conditions are met) or it succeeds and forces a retreat.*

### Artillery Bombardment
- Declared at the end of a turn (step 4); resolved at the start of the next turn (step 1). Artillery can fire only every other turn (may not declare while a bombardment is still pending).
- The artillery piece must be **blocking an approach**; it may not be in reserve. The target must be in the locale opposite that approach.
- The artillery piece may move in the same turn it **declares** a bombardment, but may **not** move in the turn the bombardment is **resolved**.
- **Strength:** Artillery strength minus terrain penalty on the opposite approach (penalty applies only if target is in that opposing approach; no penalty if target is in reserve or another approach).
- **Losses:** Each point of bombardment strength removes 1 strength point from the defending player's chosen piece. If attack strength ≥ piece's strength, the piece is eliminated.
- An artillery piece may not assault in the same turn it declares or resolves a bombardment.

### Assaults
An assault is an advance by pieces across an approach **blocked by enemy pieces**. The attacking pieces must be blocking that approach; the target is the locale opposite.

Assault resolution sequence:
1. **Attacking leading pieces declared:** The attacker names which pieces are leading (turned face-up). Only infantry or cavalry with strength ≥ 2 may lead; each leading piece's strength must exceed the approach's terrain penalty; all leaders must be the same type (all infantry or all cavalry). Maximum 1 leader if approach is narrow, 2 if wide. Cavalry cannot lead into cavalry-obstructing terrain.
2. **Artillery defense declared:** If the defender has artillery that did not bombard last turn, the defender may declare artillery defense (turn it face-up).
3. **Artillery defense resolved:** Each strength point of defending artillery inflicts 1 strength-point loss on the attacking leading pieces.
4. **Defending leading pieces declared:** Defender names which pieces are leading (turned face-up; must be infantry or cavalry, not artillery; all same type). Maximum 1 leader if narrow, 2 if wide. Cavalry cannot lead defense of a cavalry-obstructing approach.
5. **Assault strength calculated:** Sum the strengths of attacking leading pieces (after artillery-defense losses), then subtract the terrain penalty for the attacked approach (infantry penalty if leaders are infantry; cavalry penalty if cavalry). Result may be negative.
6. **Assault result calculated:** Subtract the sum of defending leading pieces' strengths from the assault strength. Positive result = attackers win; zero or negative = defenders win.
7. **Losses applied:** The winning side loses 1 strength point. The losing side loses 1 + 1 per point the result was above or below zero.
8. **Cavalry pursuit (optional):** If the winner has non-leading cavalry in the assault and the loser's leading pieces were not cavalry, the winner may declare cavalry pursuit (turn pursuing cavalry face-up; max 1 pursuer if narrow, 2 if wide; cannot declare if either occupied approach is cavalry-obstructing; does not count against command limit).
9. **Cavalry pursuit losses:** Pursuing cavalry loses 1 strength point. Enemy pieces lose strength equal to pursuit strength (pursuing cavalry's total strength minus terrain penalty of the approach occupied by the pieces being pursued).
10. **Outcome:** If defenders won: attacking pieces withdraw into reserve in their own locale; defenders remain. If attackers won: all defending player's pieces in the locale must retreat; attacking pieces advance into reserve in the assaulted locale (cavalry may then use continuation).

*Losses are applied first to leading pieces, then to non-leaders. The enemy player distributes losses among leaders; the friendly player distributes among non-leaders. Losses cannot exceed the strength of participating pieces.*

**Movement restrictions around assaults:**
- A piece may not conduct an assault and move in the same turn; if a piece conducts an assault, it may not move until the next turn.
- If a locale is taken by assault, no other friendly pieces may move into that locale that turn other than those that participated in the assault (assaulting cavalry may still use continuation into that locale as usual).
- If the attacking pieces are defeated in an assault, no friendly pieces may move across that same approach for the rest of that turn, even if the defending pieces blocking it were eliminated by the assault. Friendly pieces may still assault or move into the locale across other approaches.

### Retreats
Forced retreat (from maneuver attack or lost assault) requires all of the affected player's pieces in the locale to retreat. Retreats do not count against the command limit. Pieces are turned face-up at the start of the retreat.

**Losses on retreat:**
- Artillery pieces forced to retreat are **eliminated**.
- Infantry in reserve: lose 1 strength point.
- Cavalry in reserve: no loss.
- Any piece blocking an approach (infantry or cavalry): lose 1 strength point per approach vacated (exception: participants in the assault that caused the retreat do not suffer additional losses beyond those in the assault).

**Retreat restrictions:** Pieces may not retreat into the locale they came from, across an impassable approach, into an enemy-occupied locale, or into a locale that would exceed its capacity. If no valid retreat exists, the pieces are eliminated.

## Scoring / Victory Conditions

The game ends after 16 rounds (or when one player chooses to stop after demoralization — see below).

**Demoralization:** Every time a piece loses a strength point, the owning army's morale marker moves down by one. If it reaches zero, that army is **demoralized**. A demoralized army cannot conduct assaults and suffers a −1 strength penalty per piece in assault defense (bombardment, artillery defense, and cavalry pursuit strengths are unaffected). If only one army is demoralized during a round, the non-demoralized army gains 5 morale points at the start of the next round.

**Victory:**
- If at the end of the game **one army is demoralized and the other is not**, the non-demoralized army's player wins.
- If **both or neither** army is demoralized, territorial objectives serve as a tiebreaker. There are eight objective locales at the east end of the map marked with stars in three colors (red, blue, green). **Austrian player wins** if their pieces occupy at least two of those eight locales **from at least two different colors**. **French player wins** if the Austrian player does not achieve this (i.e., Austrians occupy no objectives, or all occupied objectives are the same color).

## Special Rules & Edge Cases

### Fog of War
- Pieces are normally face-down. Only the owning player sees type and strength.
- Pieces are turned face-up when required by rules (leading pieces in assault, bombarding artillery, retreating pieces). They are turned face-down again at the end of the relevant step.
- At the start of a player's turn, they may do an out-of-sight shuffle of pieces together in the same locale to restore secrecy.

### Piece Types and Terrain
| Type | Notes |
|------|-------|
| Infantry | Main combat force; suffers infantry attack penalties |
| Cavalry | Restricted by cavalry-obstructing approaches; may use continuation after moves |
| Artillery | Bombards at range; cannot move and resolve bombardment in same turn; eliminated if forced to retreat |

### Terrain Effects
- **Approach width:** Narrow = max 1 leading piece; Wide = max 2.
- **Impassable approach:** No movement or attack.
- **Cavalry-obstructing approach:** Cavalry cannot lead an assault through it or lead the defense of it.
- **Attack penalties:** One or more symbols on an approach reduce attacker strength by the same amount per symbol type (infantry, cavalry, or artillery penalty).

### Capacity Limits
Each locale has a printed capacity (maximum total pieces for that player). No sub-limits for reserve vs. blocking.

### Cavalry Continuation
A cavalry piece that ends its move in reserve may continue and block an approach in that locale if the opposite locale is enemy-occupied. Splitting off for continuation costs one extra command limit point.

## Player Reference

**Sequence of Play (each turn):**
1. Resolve previous artillery bombardments
2. Conduct assaults (up to command limit)
3. Conduct movement (up to command limit; groups + assaults combined ≤ 3)
4. Declare new artillery bombardments

**Command Limit:** 3 per turn (groups moved + assaults). Exceptions (free): blocking a maneuver attack, retreating, artillery bombardment, primary road movement.

**Unit Strengths:**

| Type | Maximum Strength |
|------|-----------------|
| Infantry | 3 |
| Cavalry | 2 |
| Artillery | 1 |

**Retreat Losses Summary:**
| Situation | Loss |
|-----------|------|
| Artillery, any position | Eliminated |
| Infantry in reserve | −1 strength |
| Cavalry in reserve | None |
| Infantry or cavalry blocking approach | −1 strength per approach |

**Victory Summary:**
| Condition | Winner |
|-----------|--------|
| One side demoralized, other not | Non-demoralized side |
| Both/neither demoralized | Territorial tiebreaker |
| Austrian holds ≥2 objectives from ≥2 colors | Austrian |
| Austrian fails territorial condition | French |

**Game Length:** 16 rounds, each representing one hour of the day of battle; the Time Track marker starts on 6:00 AM at setup (the source does not state an explicit end time).
