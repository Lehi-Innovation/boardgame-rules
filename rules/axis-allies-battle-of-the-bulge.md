---
title: "Axis & Allies: Battle of the Bulge"
bgg_id: 22457
player_count: "2"
play_time: "180-240 min"
designer: "Larry Harris Jr."
source_pdf: "axis-allies-battle-of-the-bulge-rules.pdf"
extracted_date: "2026-03-18"
summarized_date: "2026-03-18"
verification: "inaccurate"
verification_date: "2026-07-03"
---
<!-- verification:begin -->
> ❗ **Known errors** — an audit found inaccuracies in this summary that could mislead players: The summary omits the Board Upkeep front-line auto-claim rule — the actual mechanism that determines Axis territorial/VP gains each turn — so a reader could not correctly update the front line or score the game from the summary alone.. Until it is re-written, prefer the full rulebook text linked below.
>
> 📄 [Full rulebook text](https://jonnyallred.github.io/boardgame-rules/extracted/axis-allies-battle-of-the-bulge-rules.txt) · 🚩 [Report a rules error](https://github.com/Lehi-Innovation/boardgame-rules/issues/new?template=rule-error.yml&labels=rule-error&title=%5BRule%20error%5D%20Axis%20%26%20Allies%3A%20Battle%20of%20the%20Bulge&game=axis-allies-battle-of-the-bulge)
<!-- verification:end -->


## Overview

Axis & Allies: Battle of the Bulge is a two-player World War II strategy game recreating the 1944 German Ardennes offensive. One player controls the Axis (Germany) attempting to capture cities and towns worth 24 victory points, while the other controls the Allies (United Kingdom and United States) trying to prevent this by the end of turn 8. The game uses a hex-based map of the Belgian/German border region, supply tokens to fuel attacks and movement, and a unique combat strip system for resolving battles. Weather plays a key role: aircraft cannot fly during the first four turns.

## Components

- 1 Game board (hex map of the Ardennes region)
- 12 Twelve-sided dice
- 1 Turn marker
- 1 Victory point marker
- 1 Axis reinforcement chart
- 3 Allies reinforcement charts (Northern, Southern, Western)
- 2 Reference charts
- 6 Combat strips (Infantry, Tanks, Artillery, Trucks, Supplies, Air units)
- 36 Front line markers
- 110 Supply tokens (100 ones, 10 fives)
- 135 Plastic chips (125 gray = +1 unit, 10 red = +5 units)
- 58 Axis playing pieces (gray): 20 Infantry, 16 Tanks, 12 Artillery, 6 Trucks, 3 Fighters, 1 Bomber
- 80 Allies playing pieces: 29 Infantry, 14 Tanks, 13 Artillery, 12 Trucks, 9 Fighters, 3 Bombers (mix of tan/UK and green/US)

## Setup

1. Choose who plays Axis and Allies. Axis sits near the eastern edge, Allies near the western/southern edge.
2. Place units on the board as indicated by printed silhouettes on each hex. Gray chips under units indicate additional units.
3. Place the turn marker on the turn track and victory point marker on the victory point track.
4. Place units on reinforcement charts as indicated (each row corresponds to a specific turn colour).
5. Allies start with 3 reinforcement charts, 5 Trucks, 3 Bombers, and 9 Fighters in off-board area.
6. Axis starts with 1 reinforcement chart, 2 Trucks, 1 Bomber, and 3 Fighters in off-board area.
7. Place front line markers along the starting front line printed on the board.

## Turn Structure

The game lasts up to 8 turns, each identified by a colour: Red (1), Blue (2), Green (3), Yellow (4), Black (5), Gray (6), Purple (7), White (8). Each turn has 4 phases:

| Phase | Description |
|---|---|
| 1. Air Combat | Skip on turns 1-4 (bad weather). On turns 5-8, deploy and resolve air combat |
| 2. Ground Combat | Players alternate attacking hex-by-hex, paying Supply tokens per attack |
| 3. Movement & Reinforcement | Move ground units (costs Supply), bring in reinforcements via Trucks |
| 4. Board Upkeep | Update front line markers and victory point track |

## Actions

### Unit Types and Combat Values

| Unit | Attack Dice | Movement | Special |
|---|---|---|---|
| Infantry | 1 | 1 hex | Zone of control |
| Tank | 2 | 1 hex off-road or unlimited on connected roads | Blitz (extra 1-hex move for extra Supply); can't cross rivers |
| Artillery | 3 | 1 hex; can't cross rivers | Zone of control |
| Fighter | 1 | Placed in any hex, no Supply needed | Dogfight; removed at end of air phase |
| Bomber | 4 (see exception) | Placed in any hex, no Supply needed | Dogfight; removed at end of air phase |
| Truck | - | Unlimited on roads | Carries 6 Infantry/Artillery/Supply tokens; non-combat |
| Supply Token | - | Cannot move on its own | Fuel for attacks and movement; carried by Trucks |

**Exception — dogfights:** The Fighter=1 and Bomber=4 attack dice above apply only when air units attack ground units (Air Combat step III). During dogfighting (Air Combat step I, air-vs-air combat in a shared hex), each air unit rolls only 1 die regardless of type — Bombers roll just 1 die each in a dogfight, not 4.

### Zone of Control

Infantry, Tank, and Artillery exert a zone of control in a 1-hex radius. Enemy ground units entering or leaving a hex in an enemy zone of control must stop. Units cannot retreat into enemy zones of control.

### Ground Combat

1. **Choose attacking hex** that hasn't attacked this turn.
2. **Choose target hexes** (adjacent hexes containing enemy units).
3. **Pay Supply tokens** (1 per target hex, drawn from attacking hex or adjacent friendly hexes).
4. **Prepare combat strips** matching defending units.
5. **Roll attack dice** equal to total attack power (Infantry=1, Tank=2, Artillery=3). Each result of 6 or less is a hit.
6. **Assign hits** by counting boxes on combat strips to the die result number.
7. **Resolve hits:** 1 hit on Infantry/Tank/Artillery = retreat; 2 hits = destroyed. Any hit on Truck or Supply = destroyed.
8. **Pass initiative** to the other player. Combat continues until both players decline further attacks.

### Air Combat (Turns 5-8 only)

1. Roll for initiative; winner chooses who places air units first.
2. Both players place all their air units (Allies: 3 Bombers, 9 Fighters; Axis: 1 Bomber, 3 Fighters) regardless of prior losses.
3. **Dogfighting** (Step I): In any hex where both players have air units, resolve dogfighting rounds until one side is eliminated. Each player simultaneously rolls one die per air unit they have in the hex — **Bombers roll only 1 die each in a dogfight, not their normal 4** — hit on 6 or less. Each side then assigns its hits to the other player's air units using the air combat strip; any air unit hit at least once is destroyed after both sides assign hits.
4. **Anti-aircraft fire** (Step II): The player with ground units in the hex rolls 1 die per unit type present (Infantry, Tank, Artillery, Truck, Supply token — max 5 dice), hit on 6 or less, and assigns hits to the defending air units via the air combat strip.
5. **Air units attack ground units** (Step III): Surviving air units attack ground units in the hex, rolling their full attack dice (Fighter=1, Bomber=4) — this is the only step where Bombers use their 4-dice value.
6. Return all air units to off-board area.

### Movement & Reinforcement

- Pay 1 Supply token to activate all ground units in a hex for movement.
- Trucks move for free along roads. Trucks carry up to 6 units/tokens.
- Reinforcements arrive per the reinforcement chart row matching the current turn colour.
- Free Trucks on board may return to off-board area before movement begins.
- Stacking limit: 12 units per hex total (Infantry, Tanks, Artillery, and Trucks each count as 1; any number of Supply tokens in a hex counts as 1). Sub-limits: maximum 6 Infantry, 6 Tanks, and 3 Artillery per hex.
- **Supply income:** Each turn, Axis receives 9 Supply tokens and Allies receive 11 Supply tokens (placed in off-board area).
- **Commandeering:** Ground units can't move into a hex occupied by an enemy Infantry, Tank, or Artillery, but Infantry, Tanks, and Artillery CAN move into a hex containing enemy Trucks and/or Supply tokens. Doing so immediately captures those Trucks/tokens — their owner can no longer move or use them — and the mover commandeers (takes ownership of) them when the front line markers are updated during Board Upkeep, after which they may be used freely. Moving through such a hex without stopping does not capture or commandeer anything; at least one unit must stop in the hex.

## Scoring / Victory Conditions

- **Axis wins** by controlling cities and towns worth a total of **24 victory points** at any point.
- **Allies win** by preventing the Axis from reaching 24 victory points by the end of turn 8.
- The historical Axis advance captured 23 VP worth of territory, so the Axis player must do slightly better than history.
- Victory points are tallied at the end of each turn based on cities/towns on the Axis side of the front line.

## Special Rules & Edge Cases

- **First turn surprise attack:** On turn 1 (Red), only the Axis player attacks during Ground Combat. The Allies cannot attack.
- **River barriers:** Only Infantry can cross river barriers (including when retreating). Tanks and Artillery cannot.
- **Blitz:** Pay an extra Supply token when activating a hex to give all Tanks in that hex an additional 1-hex move after their normal move. The blitz move can be on-road or off-road and can enter/leave enemy zones of control.
- **Stacking limit:** Maximum 12 units per hex (Infantry, Tanks, Artillery, and Trucks each count as 1 unit; any number of Supply tokens in a hex counts as 1 unit). Sub-limits: maximum 6 Infantry, maximum 6 Tanks, maximum 3 Artillery per hex. Air units do not count toward the stacking limit.
- **Retreating:** Units that take 1 hit must retreat 1 hex. If unable to retreat (zone of control, stacking limit, river barrier), the unit is destroyed instead.
- **Commandeering enemy Trucks/Supply:** Moving an Infantry, Artillery, or Tank into a hex containing enemy Trucks or Supply tokens immediately captures them (the original owner can no longer move or use them); the capturing player then commandeers (gains full ownership of) them once front line markers are updated in Board Upkeep. Merely passing through such a hex does not capture anything — a unit must stop there.
- **Rolling more than 12 dice:** Roll all 12, assign hits using chips, then reroll remaining dice as needed.
- **More than 6 defending units:** Count hits first, then reroll just those dice to assign them on the expanded combat strips (up to 12 boxes).

### Optional Rules

- **Ongoing Campaign:** Keep records of your games. Track the best Axis or Allied score each player can achieve; reverse roles and compare results; maintain a running tally of Axis scores across multiple games to see who comes out ahead over time.
- **Custom Setup:** The Allies player sets up their starting units (including Supply tokens) in any hexes on their side of the front line, provided combat units cover every hex on the Axis side of the front line with zone of control. Then the Axis player sets up their units with the same supply-coverage requirement, but Axis starting units cannot be placed outside their army's designated starting areas (6th Panzer, 5th Panzer, and 7th Army sections).

## Player Reference

**Turns:** 8 turns (Red, Blue, Green, Yellow, Black, Gray, Purple, White)

**Phases:** Air Combat (turns 5-8 only) -> Ground Combat -> Movement & Reinforcement -> Board Upkeep

**Attack dice:** Infantry=1, Tank=2, Artillery=3, Fighter=1, Bomber=4. Hit on 6 or less (d12). **Exception:** in dogfights (air-vs-air combat), every air unit including Bombers rolls only 1 die each — the Bomber's 4-dice value applies only when air units attack ground units.

**Supply cost:** 1 token per hex attacked; 1 token per hex activated for movement

**Victory:** Axis needs 24 VP from cities/towns. Allies need to hold until end of turn 8.

**Stacking:** 12 units/hex (max 6 Infantry, 6 Tanks, 3 Artillery; Supply tokens count as 1 unit collectively; air units exempt)

**Supply income:** Axis 9 tokens/turn; Allies 11 tokens/turn

**Commandeering:** Moving Infantry/Tank/Artillery into a hex with enemy Trucks/Supply tokens captures them on the spot (owner loses use of them); capturer commandeers (owns) them once front line markers update in Board Upkeep. Must stop in the hex — passing through doesn't count.

**Weather:** No air units on turns 1-4; air units available on turns 5-8
