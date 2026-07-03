---
title: "Borodino"
bgg_id: 252
player_count: "2"
play_time: "240-480 min"
designer: "Richard Berg"
source_pdf: "borodino-rules.pdf"
extracted_date: "2026-03-18"
summarized_date: "2026-03-18"
verification: "verified"
verification_date: "2026-06-17"
---
<!-- verification:begin -->
> ✅ **Verified** — this summary was fact-checked against the rulebook text and no significant issues were found.
>
> 📄 [Full rulebook text](https://jonnyallred.github.io/boardgame-rules/extracted/borodino-rules.txt) · 🚩 [Report a rules error](https://github.com/Lehi-Innovation/boardgame-rules/issues/new?template=rule-error.yml&labels=rule-error&title=%5BRule%20error%5D%20Borodino&game=borodino)
<!-- verification:end -->


## Overview

Borodino is a two-player hex-and-counter wargame covering the famous 1812 battle between Napoleon's French army and Kutuzov's Russian forces, using the Triumph & Glory system (version 2.2). The game emphasizes activation-based play where units move only when their Activation Marker is drawn from a randomized pool. Players issue Orders to their corps, maneuver infantry, cavalry, and artillery across the battlefield, resolve fire and shock combat, and attempt to break enemy morale. The game includes scenarios for both the preliminary Battle of Schevardino Redoubt and the main Battle of Borodino.

## Components

- 1 Map (22" x 34", hex grid, ~325 yards per hex)
- 1.5 Counter sheets (infantry, cavalry, artillery units; leaders; activation markers; orders markers)
- 1 Rules booklet
- 1 Player aid card
- 1 Ten-sided die

## Setup

Setup and initial procedures differ significantly between the two scenarios.

### Battle of Schevardino Redoubt (Introductory)
Smaller scenario using a portion of the map. French attack Russian advance positions. This scenario does **not** use the Command and Activation systems of the full game: it uses no Activation Markers and no Orders system — all units are considered "Under Orders" throughout. See the distinct Schevardino turn sequence under Turn Structure below.

### Battle of Borodino (Full)
Full map deployment. Units are placed according to a detailed hex-by-hex Order of Battle for each corps/command as given in the scenario's deployment listing; the rulebook specifies hex coordinates only and does not narrate terrain features beyond that.

For the Borodino scenario, at the start of play:
1. Place units per the scenario's Order-of-Battle hex listing.
2. Each player secretly assigns Orders status (Under Orders vs. No Orders) to each Orders Command, marking each with an Orders marker placed near the command on the map or in the Command/Orders box printed on the map. The number of commands a player may place Under Orders is limited by the Overall Commander's Orders Rating for that scenario (5.21-5.23).
3. Proceed to the Turn Structure below (Activation Markers for all on-map units and reinforcements are placed in The Pool each turn, as part of the Initiative Determination Phase, 5.32).

## Turn Structure

The sequence below is used by the **Borodino** scenario (the full Command and Activation system). The **Schevardino** scenario uses a distinct, simpler sequence with no Activation Markers, Orders, or Pool — see the "Schevardino Scenario Sequence" subsection at the end of this section.

### Borodino Scenario Sequence

Each game turn follows a fixed sequence:

### A. Orders Phase
1. Players roll for possible Orders Delay (risk of not receiving orders). Napoleon does not roll for delay.
2. Players decide which Orders Commands receive Orders (Under Orders or No Orders).

### B. Initiative Determination Phase
1. Each player rolls 1D10, adds their Overall Commander's Orders Rating. Highest total has Initiative.
2. Initiative Player selects one Activation Marker to activate first.
3. All other Activation Markers go into The Pool (opaque cup).

### C. Activation Phase (repeated)
1. Draw an Activation Marker from The Pool.
2. Reveal Order Status for each command in the Activation Group. Commands with No Orders may attempt to convert.
3. **Activation Sequence (in order):**
   a. Artillery Fire
   b. Unit Movement
   c. Shock Combat and/or Cavalry Charge
   d. Rally (for units that did nothing else)
4. Repeat until The Pool is empty.

### D. Reserve Phase
Each player may activate one Reserve Group.

### E. Group Morale Phase
1. Check for Collapse (groups that have taken heavy losses may collapse).
2. Recovery Phase: Attempt to recover Disordered units. Move units from Withdrawn Box to Recovery Box.

### F. Overall Commander Movement Phase
Each player may move their Overall Commander.

### Schevardino Scenario Sequence
This scenario does not use Activation Markers, the Orders system, or The Pool; all units are considered "Under Orders." It consists of five (5) Turns. In each Turn, the French move and fight with all their "active" units, followed by the Russians doing the same with theirs; each side gets to "go" only once per Turn, but may use all of its currently active units.

- **French activation:** Only Compans' Division starts active. At the beginning of each Turn (including the first), the French player may activate one (and only one) additional, previously inactive, command — from Morand's Division, Friant's Division, I Cavalry Corps, II Cavalry Corps, or V Corps. Once activated, a command remains active for the rest of the battle. Exception: V Corps may not be activated until the 3rd Turn at the earliest.
- **Russian activation:** All Russian units start active and available, except the 2nd Grenadiers and their accompanying VIII Corps infantry, which become active and available starting Turn 2.
- Victory is determined at the end of Turn 5 (see Scoring / Victory Conditions).

## Actions

### Orders and Activation
- **Under Orders:** Commands operate normally with full movement and combat ability.
- **No Orders:** Commands are restricted; may attempt to convert to Under Orders when their Activation Marker is drawn.
- **Orders Delay:** At the start of each turn, players roll to see if corps commanders delay receiving orders (representing communication difficulties). Modified by the Orders Commander's Delay Rating.
- **Reserve:** In the Reserve Phase, each player may activate one Orders Command (the Initiative Player, if any, chooses who goes first; otherwise each player rolls a die, high roll going first). To be eligible, at least one unit of the Orders Command must be within the Overall Commander's Orders Range. Within an activated command, only units not adjacent to an enemy unit may actually be activated as Reserves — units adjacent to an enemy are excluded from acting, but the rest of the command's eligible (non-adjacent) units may still be activated. The Reserve Phase may not be used to activate commands that did not have an Activation Marker in the Pool. Units activated as Reserves function as if they have No Orders; they may not roll to change orders, nor may they Rally. Each non-artillery unit that moves during a Reserve Activation must roll for possible Disorder (Disordered if roll > Cohesion; an already-Disordered unit that fails this roll instead Withdraws). Artillery does not roll for Disorder when moving as a Reserve, but does roll if it fires.

### Movement
- Movement points vary by unit type (infantry, cavalry, artillery).
- Terrain affects movement costs (woods, cultivated ground, villages, roads/paths, streams/fords, elevation, redoubts, etc.).
- **Horse Artillery:** Movement allowance of 8 (most mobile artillery).
- **Zones of Control (ZOC):** Combat units exert ZOC into adjacent hexes, affecting enemy movement and retreat.

### Artillery Fire
- Artillery fires at enemy units within range (Effective and Maximum range).
- Fire resolution uses the Fire Table: roll D10, apply modifiers (range, terrain, target type).
- Results include Disorder, losses, or no effect.
- Artillery can fire before friendly units move.

### Shock Combat
- Occurs when units move adjacent to or into enemy hexes.
- Compare Shock Strength plus die roll plus modifiers.
- Results include Disorder, Retreat (Cohesion Check), Withdrawal, or Elimination. Rout is not used in this version; it has been replaced by Withdrawal.
- **Commitment:** Individual units have a Commitment rating determining their ability to engage.
- **Multi-Group Shock (9.23):** Infantry, Charging Cavalry, and non-Charging Cavalry may NOT combine their strengths when attacking the same unit. Each group's attack is resolved separately in the order: Cavalry Charge, Cavalry Shock, then Infantry Shock. There is no combined-arms bonus for mixed attacks.

### Cavalry Charge
- Special form of Shock initiated by cavalry units.
- Cavalry may pursue retreating enemies.
- Defending infantry may form square against cavalry charges (reduces cavalry effectiveness but makes infantry vulnerable to artillery).
- **Counter-charge:** Defending cavalry may counter-charge attacking cavalry.

### Rally and Recovery
- **Rally:** Disordered units that did not move, fire, or engage in combat may attempt to rally during their activation.
- **Recovery:** Units in the Recovery Box attempt to return to play during the Group Morale Phase. Success depends on Cohesion rating.
- **Withdrawal:** Replaced the Rout mechanic. Units forced to withdraw move to the Withdrawn Box and may recover in subsequent turns.

## Scoring / Victory Conditions

Victory conditions vary by scenario:

### Schevardino Scenario
- The player who occupies the Schevardino Redoubt at the end of Turn 5 wins.

### Borodino Scenario
- Victory is determined by Victory Points (VP) totaled at the end of the game. The player with the most VP wins; the larger the margin, the greater the victory.
- **Group Collapse VP:** The French earn 3 VP for each Russian Activation Group (other than the Russian Imperial Guard/V Corps) that Collapses, and 10 VP for the Russian Imperial Guard. The Russians earn 4 VP for each French Activation Group (other than the French Imperial Guard) that Collapses, and 10 VP for the French Imperial Guard.
- **Geographic VP:** The side occupying hex 3417 at game end earns 10 VP. (Both sides can earn this if the occupying side changes; only the occupier at game end earns it.) The game ends at the conclusion of the 1945 game-turn.

## Special Rules & Edge Cases

- **Kutuzov's Orders Rating:** Varies depending on which Russian army he is activating.
- **Napoleon's Orders:** Napoleon does not roll for Orders Delay (he issues orders directly).
- **Redoubts, Villages & Castles:** Infantry units (only) in these hexes have frontal facing into all six hexes surrounding them, meaning they may fire/shock in any direction rather than only through their normal Frontal hexsides (6.11).
- **Cohesion:** The most important unit rating, representing morale, training, and weaponry combined. Used for rally, recovery, and combat resolution.
- **Stacking:** Generally 2 units per hex, except brigades from the same parent unit plus 1 artillery (3 units total).
- **Facing:** Facing affects combat only (it has no effect on movement or Zones of Control, and a unit may change facing freely during or after movement). A unit may fire or shock only from its Frontal hexsides; a unit attacked through its Rear hexes suffers negative effects.
- **Group Morale/Collapse:** When an Activation Group takes sufficient losses, it may Collapse, causing all units in the group to become Disordered and potentially withdraw.

## Player Reference

**Sequence of Play (Borodino scenario):**
1. Orders Phase (delay rolls, assign orders)
2. Initiative Phase (roll D10 + Commander rating; winner picks first activation)
3. Activation Phase (draw markers, execute: Fire -> Move -> Shock -> Rally)
4. Reserve Phase (activate 1 reserve group each)
5. Group Morale Phase (check collapse, recovery attempts)
6. Overall Commander Movement

**Sequence of Play (Schevardino scenario):** No AM/Orders/Pool — 5 Turns, each Turn the French move and fight with all active units, then the Russians do the same (see Turn Structure for the command-activation-by-turn details).

**Unit Types:**

| Type | Key Stats |
|------|-----------|
| Infantry | Shock strength, Cohesion, Defensive Fire DRM |
| Cavalry | Shock strength, Cohesion, Cavalry Type (Lt/Hv/Cossack) |
| Artillery | Fire strength, Effective/Max range |
| Leaders | Command Rating, Orders Rating, Orders Range |

**Combat Resolution:** Roll D10, apply DRMs, consult appropriate table (Fire Table or Shock Table).

**Game Scale:** ~325 yards/hex, ~75 minutes/turn, ~200 men per infantry strength point.
