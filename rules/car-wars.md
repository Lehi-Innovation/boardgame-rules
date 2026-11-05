---
title: "Car Wars"
bgg_id: 2795
player_count: "1-8 (best with 4-6)"
designer: "Chad Irby and Steve Jackson"
source_pdf: "car-wars-rules.pdf"
extracted_date: "2026-08-07"
summarized_date: "2026-08-07"
rulebook_version: "Steve Jackson Games (copyright 1990, 2014, 2015)"
verification: "verified"
verification_date: "2026-08-08"
---
<!-- verification:begin -->
> ✅ **Verified** — this summary was fact-checked against the rulebook text and no significant issues were found.
>
> 📄 [Full rulebook text](https://lehi-innovation.github.io/boardgame-rules/extracted/car-wars-rules.txt) · 🚩 [Report a rules error](https://github.com/Lehi-Innovation/boardgame-rules/issues/new?template=rule-error.yml&labels=rule-error&title=%5BRule%20error%5D%20Car%20Wars&game=car-wars)
<!-- verification:end -->


## Overview

Car Wars is a tactical vehicular-combat game set roughly 50 years in the future (the "present" of the game world advances with real time; this edition is set in 2040), in a United States fractured by a second civil war, food shortages, and collapsing central authority. In this world, "autoduelling" — armed, armored car combat — is both a legal televised sport (fought in arenas and on closed tracks in front of the American Autoduel Association's cameras) and a fact of daily survival on lawless highways. Players design or select armored, weaponized cars, motorcycles, or trikes and fight using a detailed simultaneous-ish, phase-based movement and combat system.

The game is played on a square-grid map at 1/180 scale (1 inch = 15 feet). Each game turn represents one second of real time and is broken into five phases; a vehicle's speed determines which phases it moves in and how far. Within a turn, drivers manage their vehicle's speed and Handling Class/Status to attempt maneuvers without losing control, while gunners and drivers fire weapons at other vehicles and pedestrians, tracking damage location by location (armor, then specific components) until a target is destroyed, disabled, or forced to surrender.

There is no single fixed victory condition — the winner is determined by whichever scenario is being played (see Scoring / Victory Conditions). Most arena and road scenarios are won by being the last vehicle still able to move and fight; races and highway pursuits use distance- or survival-based objectives instead. In continuing campaign play, characters who survive duels accumulate skills, Prestige, and Wealth, which carry over from game to game.

## Components

### Physical play aids
| Component | Notes |
|---|---|
| Six-sided dice | Supplied by the players; notation "d" = one die, "2d-1" = roll 2 dice and subtract 1, "1/2d" = roll 1 die and divide by 2 (round up) |
| Arena Map | Six gates; heavy black walls (80 DP — vehicles can't cross them, pedestrians can't climb them, nothing shoots or crashes through); black "B" squares are pedestrian bunkers; white areas are low walls (can be shot over but not crossed by vehicles) |
| Racetrack Map | Played in oval or figure-8 configuration; boundary walls have 80 DP; black dots at road forks are crash barriers (half damage on collision); gray shoulder areas can be ruled to have no effect, a +D1 maneuver penalty, or worse |
| Vehicle Record Sheet(s) | One per vehicle; tracks weapons, ammunition remaining, armor by location, other components, and a Handling Class/Status log per turn (blank sheets are provided for photocopying) |
| Car counter | 1 inch long |
| Cycle counter | 1/2 inch long |
| Trike counter | 1 inch long, like a car |
| Pedestrian counter | 1/2" x 1/4"; only the front 1/4" square is the actual pedestrian |
| Debris counter | 1/2" x 1/4"; may show one or two squares of debris |
| Obstacle counter | Represents a pothole, loose wheel, or similar large hazard; roughly 50-100 lbs, one space if carried |
| Mine / spike / oil-slick counters | Placed by dropped weapons; remain until triggered (mines, spikes) or indefinitely (oil) |
| Smoke and paint cloud counters | 1" x 1/2" typically |
| Turning Key | A scaled template for plotting maneuvers and Crash Table results without needing the grid; also allows play at any physical scale |

### Vehicle-design catalog
The bulk of the rules is a modular kit for building duel vehicles:

| Category | Options in this rulebook |
|---|---|
| Body types (cars) | 9: Subcompact, Compact, Mid-sized, Sedan, Luxury, Station Wagon, Pickup, Camper, Van |
| Chassis grades | 4: Light, Standard, Heavy, Extra-Heavy (adjusts max load and price) |
| Suspension grades | Cars: Light/standard, Improved, Heavy, Off-Road. Separate, cheaper lines exist for cycles and trikes |
| Power plants | 6 named tiers: Small, Medium, Large, Super, Sport, Thundercat (cars); parallel Small/Medium/Large/Super Cycle and Super Trike tiers for two-/three-wheelers |
| Tires | 4 base grades (Standard, Heavy-Duty, Puncture-Resistant, Solid) plus optional Steelbelting, Radial, Off-Road, and Fireproofing modifications |
| Armor types | 5: standard ablative plastic, Fireproof (FP), Laser-Reflective (LR), Laser-Reflective Fireproof (LRFP), Metal |
| Vehicular weapons | ~20 named weapons across 8 categories: small-bore projectile, large-bore projectile, rocket, laser, flamethrower, dropped solid, dropped liquid, dropped gas |
| Hand weapons | ~19 types (pistols through bazookas and knives) plus 12 grenade types |
| Accessories | 20+ items split into Offense, Defense, and Miscellaneous |
| Characters | Drivers, gunners, passengers, and pedestrians, each tracking Skills, Prestige, and Wealth |

## Setup

1. **Pick a scenario** (see Scoring / Victory Conditions and Chapter 9). Spread out one of the included maps — taping it down is recommended — or draw a custom layout on 1/4" graph paper for arenas, parking lots, or obstacle courses.
2. **Select or build vehicles.** Make a Vehicle Record Sheet for each car, cycle, or trike, and choose a counter, miniature, or model to represent it on the map. Set each vehicle's beginning speed and Handling Status on its record sheet.
3. **Roll for reflexes.** Every driver rolls 1 die at the start of the duel: a 5 raises that vehicle's Handling Class by 1 for the duration of combat, a 6 (or higher, after skill bonuses) raises it by 2. Reflexes of non-driver occupants do not count.
4. **Place vehicles** in their starting positions and begin play.

**Highway Chase forking (racetrack map used for pursuits):** when the lead car in a pursuit reaches a fork, ignore the fork and take the straighter path if the angle exceeds 90°. If the angle is 90° or less, roll 1 die: 1-2 the leader takes the right path, 3-4 the left path, 5-6 the leader's choice. Other cars must follow the leader through the same fork or be considered lost. Whenever a 6 is rolled at a fork, the pursuing player may drop six debris markers, from a foot above the map, in front of the lead car (redrop any that land closer than 6" to the leader).

## Turn Structure

Each turn represents one second and is divided into **5 phases** of 1/5 second each. A referee (optional, but recommended for multi-player games) tracks a control marker for each vehicle against the Movement Chart, cross-indexed by current speed, and calls out which vehicles move in which phase.

1. **Speed changes.** At the start of any phase in which it has not yet done so this turn, a vehicle may accelerate or decelerate once, up to its built maximum acceleration (5, 10, or 15 mph) or a safe 10 mph of deceleration (greater deceleration requires a maneuver roll — see Player Reference). This is resolved before that phase's movement.
2. **Movement.** Vehicles scheduled to move in the phase do so: vehicles at even speeds below 60 mph move an ordinary 1" (during which they may fold in one maneuver); vehicles at odd speeds below 60 mph make a straight 1/2" half-move instead (no maneuver, except a Pivot); vehicles above 50 mph move 2" in some phases, and odd speeds above 50 mph owe an additional half-move on top of that. When two or more vehicles are due to move in the same phase, the faster vehicle moves first; ties are broken in favor of the driver with better reflexes (or the vehicle's owner's choice if reflexes also tie).
3. **Maneuvers and hazards.** A maneuver may replace 1" of that phase's movement (only one maneuver per vehicle per phase). Maneuvers and hazards (enemy fire, hitting debris, road conditions, etc.) reduce Handling Status; each reduction may force a Control Table roll and, on a failure, a Crash Table roll (see Special Rules & Edge Cases).
4. **Combat.** Any character may fire a weapon in any phase after that vehicle has moved, by announcing the weapon and target and rolling to hit. A given weapon or character normally fires only once per turn (exceptions: automatic fire, multiple gunners, linked weapons).
5. **Simultaneous resolution.** All damage from a phase's attacks and collisions is applied simultaneously at the end of that phase (armor loss, component destruction, Handling Status changes, and any resulting debris/obstacle placement).
6. **End of turn.** Every vehicle recovers Handling Status (by its Handling Class, as modified by suspension/equipment/tire loss, plus the driver's relevant skill bonus, minimum 1 point, never above its starting Handling Class). Burning vehicles roll for fire/explosion effects. A vehicle whose driver was just killed or incapacitated may begin the process of getting a substitute driver into position.

## Actions

### Movement maneuvers
Any maneuver's Difficulty (D) rating is subtracted from Handling Status when performed, and is also subtracted from any to-hit roll made in the same phase.

| Maneuver | Difficulty | Details |
|---|---|---|
| Bend | D1 per 15° of turn (15°=D1, 30°=D2, 45°=D3, 60°=D4, 75°=D5, 90°=D6) | Move 1" forward, then angle to one side, keeping one rear corner fixed |
| Drift | D1 | Move 1" forward and up to 1/4" to one side, same facing |
| Steep Drift | D3 | Move 1" forward and 1/4"-1/2" to one side, same facing |
| Swerve | Difficulty of the equivalent bend, +1 | A drift, then immediately a bend in the opposite direction (drift must come first) |
| Controlled Skid | Bend/swerve difficulty plus a skid-distance tier | Declare a bend or swerve, then a skid distance: 1/4" adds D1 (−1 to aimed fire, no deceleration/tire damage); 1/2" adds D2 (−3 to fire, −5 mph, no tire damage); 3/4" adds D3 (−6 to fire, −5 mph, 1 tire-damage point each); 1" adds D4 (no aimed fire the rest of the turn, −10 mph, 2 tire-damage points each) |
| Bootlegger Reverse (J-turn) | D7 | Only from 20-35 mph starting speed; skids to face backward and stops; 1 point of damage to each tire; no aimed fire until the vehicle stops; cannot be combined with other maneuvers; cycles and oversized vehicles cannot attempt it |
| T-Stop | D1 per 10 mph decelerated | Only from 20-35 mph; rotates 90° and skids to a halt, losing 20 mph per inch moved, 1 tire-damage point per full 20 mph lost; no aimed fire once started |
| Pivot | D0 | Only at 5 mph: move 1/4" straight, then pivot any amount around a fixed rear corner (instead of the normal 1/2" half-move) |
| Evening-Out | D0 | After a maneuver parallel to the grid, nudge the counter onto the grid lines; no speed or handling effect |
| Reverse Movement | Same maneuver's normal difficulty +1 | Any non-cycle vehicle may reverse at up to 1/5 top speed; must stop for one full turn to switch between forward and reverse; a cycle can only be walked backward by its rider at 2.5 mph |
| Fishtail | Not a chosen maneuver — Crash Table result only | One front corner stays fixed while the opposite rear corner slides 1/4" (minor) or 1/2" (major) to the side |

### Combat actions
- **Fire a vehicular weapon.** Announce the weapon and target, then roll 2d6, needing the weapon's listed to-hit number or better (e.g., a Machine Gun needs 7+); apply all applicable modifiers (see Player Reference). A natural 2 is always a miss; a natural 12 is not an automatic hit. If, after modifiers, a 13+ would be needed, the shot cannot hit but may still be fired to build sustained-fire bonus.
- **Put a weapon on/off automatic.** Doing either is a firing action. An automatic weapon fires every turn, straight out from its mount (no specific target, no computer bonus, cannot target tires/turrets), until it runs dry or is switched off; having one weapon on automatic lets its owner also aim and fire a second weapon that turn. A turreted weapon cannot be put on automatic.
- **Fire linked weapons.** Two or more identical weapons on the same side (or in a turret) can be wired to one trigger and fired together; each still makes its own to-hit roll, but shares all modifiers. Non-identical weapons can be linked, but only one may be aimed — the rest act as if on automatic. A Smart Link ($500) allows weapons in different locations (e.g., a turret and the hull) to be aimed and fired together at the same target.
- **Fire or throw a hand weapon/grenade.** Any character not firing a vehicle weapon that turn may use a hand weapon instead. The driver of a moving vehicle is at −3 to hit with hand weapons, a gunner or passenger at −1; stationary characters and pedestrians fire at listed values. Thrown grenades need 9+ on 2d6 to land on the intended square (see Special Rules & Edge Cases for scatter).
- **Ram / collide.** Colliding with another vehicle, a pedestrian, or a fixed object is resolved as a Head-On, Rear-End, T-Bone, or Sideswipe collision (see Special Rules & Edge Cases).
- **Hand-to-hand attack.** An adjacent pedestrian may strike another pedestrian (needs a 2+ to hit before modifiers, typically ~5+ net) or a vehicle (automatic hit at point-blank range with a hand weapon, minimum 1 point of damage).

### Vehicle and crew actions
- **Mount/dismount.** Standing beside a cycle for one full turn mounts it; the rider must then stay motionless 3 more seconds before moving off. Entering a larger vehicle takes a turn standing beside it (opening the door), a turn to get in, and a turn to close the door. Starting any vehicle takes 3 seconds; it may fire immediately but cannot move until the 4th turn.
- **Jump from a moving vehicle.** Take damage as if hit by a sideswipe from a DM-1 vehicle traveling 10 mph slower than the jumper's actual speed; the jumper lands in an adjacent square and may act on the next turn.
- **Reload.** A hand weapon's magazine takes 1 turn to replace (nothing else may be done that turn); a bazooka takes 2 seconds to reload (1 second with two people helping).
- **Raise/lower a pop-up turret.** A firing action, taking 1 turn.
- **Remote-detonate mines.** A firing action; lets mines be set off on command instead of by contact (doubles the minedropper's cost if both contact and remote triggering are wanted).
- **Repair, jury-rig, salvage, or install** a component — requires the Mechanic skill (see Player Reference for the Repair Chart and difficulty tiers).
- **Pick up / carry / drop an obstacle** — pedestrian only: 1 turn to pick up, 1 square per turn while carrying (no weapon use while carrying), 1 turn to drop.
- **Use a skill** — either a straight skill roll (2d6 + skill bonus vs. a target set by the referee, base success on 7+) or a Contest of Skill against another character.

## Scoring / Victory Conditions

Car Wars has no single universal win condition — each scenario defines its own. To build a scenario, decide: general type (arena/racetrack combat, highway chase, off-road confrontation, etc.), starting vehicles, starting characters and their skill-point budgets, setup positions, and objectives/how victory is determined. The rulebook provides these ready-made scenarios:

- **Amateur Night** (learning scenario): each player gets a free arena-supplied duel vehicle (usually a Killer Kart). All cars enter simultaneously, at up to 20 mph, from different gates. **The last surviving car wins.** A driver may flee through any gate (on foot or driving) to save himself but cannot re-enter; a car may still be shot at until it is entirely clear of the arena. The winner keeps all vehicles used in the event (mostly worth only salvage value). After winning three Amateur Nights, a character becomes a "professional" and can no longer compete as an amateur.
- **Other Arena Events**: typically capped by vehicle cost (e.g., "Division 20" = a $20,000 ceiling per car) and fought every-car-for-itself (team play is also possible). **Usually won by the last survivor**, though a scenario may instead award points for kills, ramp jumps, or other feats to reward exciting play over stalling ("turtle" tactics).
- **Road Duel** (2 players): each gets a fixed budget to pick or build one car. A random roll decides who starts in front; 2d6 sets the starting gap in inches. Both vehicles start at 60 mph, heading the same direction. **The survivor wins.**
- **Pack Attack** (multiplayer): one player gets $17,000 to build a single car; the remaining players share $25,000 to field at least 5 cycles. The car starts with a 12" lead; every vehicle starts at 80 mph. **The cycles win by destroying the car. The car wins by destroying all the cycles, by losing its pursuers at a fork in the road, or by extending its lead to more than 30".**

### Defining a "kill" (campaign scoring)
A **kill** is scored when an enemy vehicle can no longer move or fire — whether from direct attack, a combat crash, surrender, or abandonment by its crew. The occupants need not die. If a vehicle can no longer move but still has working weapons, it is not a kill unless and until it surrenders. If the crew abandons or surrenders a vehicle, that counts as a kill; a damaged vehicle that escapes to safety does not. Killing a pedestrian is never a vehicle kill.

### Prestige (campaign meta-game)
Every character starts at 0 Prestige. Arena combat always counts; road combat only counts if witnessed/filmed (a 2-in-6 chance per fight, referee's discretion for higher chances in some settings). An **ace** has 5 confirmed kills; a **double ace** has 10.

| Event | Prestige |
|---|---|
| Entering combat | +1 |
| Winning an event | +2 |
| Each kill your vehicle scores | +2 |
| Your vehicle is killed, you survive unhurt | −1 |
| Your vehicle is killed, you survive injured | −2 |
| You abandon a vehicle that can still move and fire | −1 |
| You leave the arena in a vehicle that can still move and fire | −1 |
| You attack with hand weapons while outside a vehicle | +1 |
| You kill a vehicle occupied by a character with Prestige 15-20 | +1 |
| You kill a vehicle occupied by a character with Prestige over 20 | +2 |
| Becoming an ace | +5 |
| Becoming a double ace | +10 |
| Excellent play/lucky shots/survival (awarded by group vote) | up to +3/game |
| Death: heroic / ordinary combat / mundane / cowardly | −1 / −2 / −3 / −5 |

**Advantages:** with cash prizes on the line, Prestige 10+ earns a cash bonus equal to your Prestige as a percentage (Prestige 17 = +17%). Prestige 15+ gives a 25% discount on new vehicle purchases and repairs; Prestige 25+ gives a 50% discount (sponsorship money).

### Skill points (character advancement)
Surviving a combat earns 1 point toward the vehicle skill used (Driver, Cyclist, etc.); scoring a kill earns 1 more toward that same skill (if the driver himself fires the killing shot, he earns both a Driver point and a Gunner point). A pedestrian entering combat earns 1 general point; a pedestrian who kills/knocks out another pedestrian earns 1 point in the skill used; a pedestrian who kills a vehicle earns 5 points. Firing hand weapons from inside a vehicle earns no points except by referee discretion. Sample general-award values: winning an arena event +3, surviving one +1, conspicuous bravery +2, risking your life for a teammate +2, an unusual tactic +1, escaping an ambush alive +1, knocking out a vehicle for salvage +1, winning a highway duel +1 (+2 if outnumbered), completing a mission +5 to +15.

### Wealth
Every character starts at 0 Wealth. Money comes from selling salvaged cars/parts, arena prizes (a typical purse is 0.5x to 1.5x the total value of the competing vehicles), road salvage from ambushed targets, paid missions, and deals with other players. Living expenses run $150/week; a character with no money must sell something or starve, and a character with no money and no car has his Prestige reduced to zero and is out of the game.

## Special Rules & Edge Cases

### Damage, fire, and explosion
- **Humans** have 3 DP: the first hit wounds, the second knocks unconscious, the third kills. Standard Body Armor also has 3 DP and is damaged first, effectively doubling survivability. A wounded character's skills are at −2. A wounded/killed driver is a D2 hazard for the vehicle, and all of that driver's skill/reflex bonuses are lost until he recovers.
- **Fire chance:** if a vehicle's power plant, flamethrower, or flaming-oil jet is hit by enemy fire, there is a 2-in-6 chance of catching fire that turn; a 4-in-6 chance if the hit came from a laser, flamethrower, or flaming-oil weapon.
- A **fire extinguisher** has a 3-in-6 chance to put out a fire at the end of each turn (4-in-6 for an Improved Fire Extinguisher). An unextinguished fire does 1 point of damage to every occupant, every vehicle component (including tires), and the armor on every side, each turn it burns.
- A **burning vehicle carrying** a flamethrower, flaming-oil jet, rocket/missile weapon, or AT gun may explode: roll 1d each turn the fire persists; on a 1 it explodes, killing all occupants and doing 1d damage to pedestrians/vehicles within 2".
- **Fire Modifier / Burn Duration** (cumulative; roll under the total to ignite): Flamethrower FM 4; a laser hit FM 1; Thermite Grenade FM 2 (burn duration 1 turn); White Phosphorus Grenade FM 2 (burn duration 1 turn). Each subsequent turn of an active weapon's burn duration adds its Fire Modifier again to that turn's ignition roll.
- **Fireproof (FP) armor** cannot itself catch fire (though breached components behind it can); **Laser-Reflective (LR) armor** halves laser damage (round down) and ignores laser fire-modifiers, but still burns normally from other sources.

### Collisions and fixed objects
- Every collision is a **Head-On, Rear-End, T-Bone, or Sideswipe** (same-direction or opposite-direction), determined from the collision diagrams; on a boundary case, the defender chooses.
- **Damage Modifier (DM)** by vehicle weight: 0-2,000 lbs = 1/3; 2,001-4,000 = 2/3; 4,001-8,000 = 1; 8,001-12,000 = 2; 12,001-16,000 = 3; 16,001-20,000 = 4; 20,001-24,000 = 5; DM increases by 1 for every additional 4,000 lbs beyond that. A pedestrian's DM is 1/5. (Worked examples from the text: a Shogun 100 at 800 lbs is DM 1/3; a Killer Kart at 2,300 lbs is DM 2/3; a Hotshot at 6,600 lbs is DM 1.)
- **Ram damage** (dice rolled) scales with collision speed via the Movement Chart's "Ram" column; two worked examples from the text: a 40 mph collision does 3d damage, an 80 mph collision does 11d damage. Multiply the dice result by your own DM to find the damage you inflict; damage you receive is the other vehicle's roll times their DM.
- After computing ram damage, each vehicle's post-collision **Temporary Speed** is found by cross-indexing your DM against the opposing DM (or a fixed object's rating) for a fraction (1, 3/4, 1/2, 1/4, or 0); multiply your original speed by that fraction and round up to the nearest 5 mph.
  - **Head-On:** both vehicles take ram damage at (V1 speed + V2 speed); the faster vehicle's new speed is its Temporary Speed minus the slower vehicle's; the slower vehicle drops to 0 and conforms to the faster one's path.
  - **Rear-End:** ram damage is based on (V1 speed − V2 speed); both vehicles end up moving at the sum of their two Temporary Speeds.
  - **T-Bone:** ram damage is based on V1's speed alone; only V1 recalculates to its Temporary Speed, V2's speed is unaffected (though its direction may change).
  - **Sideswipe:** net speed is the difference (same direction) or sum (opposite directions) of the two speeds, divided by 4 and rounded up to the nearest 5 mph — this is the "Swipe-Speed" used for ram damage; neither vehicle's actual speed changes.
- **Metal armor** absorbs up to 3x its rated value before damage penetrates to the interior (excess damage passes through); every natural 6 rolled on a damage die permanently reduces the metal armor's value by 1 point (every 5 or 6 for burst-effect weapons); a single collision can strip at most half of the metal armor on the affected side (round up).
- **Concussion (optional):** divide the speed change caused by a ram by 10 (round up); each occupant rolls 2d needing that number or higher or be stunned (unable to fire or drive) for as many phases as the roll was missed by (minimum: rest of the turn). Safety Seats, Impact Armor, and Roll Cages each add +1 to this roll. Stunning a driver adds a D2 hazard to the crash.
- **Fixed objects** (trees, walls, boulders) have a DP rating and return exactly as much damage as they absorb, up to their DP, at which point they break. Ramming through a **building** requires doing damage equal to twice the building's DP in one hit (a "double breach").

### Off-road, water, and terrain
- Driving off-road with unmodified suspension costs Handling Class: Motorcycle (with or without sidecar) −2, Trike −1, Car (4- or 6-wheel) −3. Off-Road suspension and Off-Road tires remove these penalties (radial-tire bonuses don't apply off-road).
- Off-road, every maneuver (not hazards) gets +D1 difficulty. A standard car/pickup/van going off-road faster than 10 mph rolls 2d at the start of each turn: 2-3 = underbody takes 1 point of damage, 4-5 = one random tire takes 1 point (roll extra times per 20 mph over 10: twice above 30 mph, three times above 50 mph, and so on). Solid and Off-Road tires never take this damage; vehicles with Off-Road suspension and all cycles/trikes are built high enough to skip the underbody check entirely.
- **Ditches** under 2 feet across are a D3 hazard at ≤20 mph but only D1 at higher speed (the vehicle flies over). Ditches 2-4 feet across are impassable below 20 mph (the vehicle falls in and takes full collision damage against the far wall); a D3 hazard from 25-40 mph; D1 again at 45+ mph.
- **Water** deeper than 1.5 feet can't be crossed without Off-Road suspension (which allows up to 3 feet); deeper water "drowns" the power plant exactly as if it had been destroyed (no lasting damage — it works again after 1d hours once out of the water). Standing water over 0.5 ft is a D2 hazard on entry, and decelerates the vehicle 5 mph/turn per 0.5 ft of depth (you must accelerate 5 mph just to hold speed). No maneuver harder than an unmodified D3 can be attempted in water.
- **Jumping** with a 20°-40° takeoff angle carries a vehicle 15 feet for every 10 mph of speed over 20 (30 mph = 15 ft, 40 mph = 30 ft, etc.); a 15°-19° or 41°-45° angle halves the distance; angles outside 15°-45° cannot launch a jump. Landing is a D1 hazard, +D1 per full 30 feet flown, −1 if landing downhill, +1 if landing uphill; roll 1d per non-solid tire on landing, and on a 1-3 that tire takes 1 point of damage.
- **Falling** (off a cliff/curb) takes a set amount of time before impact (a 1-inch/15-foot fall takes 1 full second, per the rulebook's worked example); the vehicle can't accelerate, decelerate, maneuver, or jump while falling, though it may fire at −2; it takes standard collision damage on impact.

### Tires, wheels, and loss of control
- Losing the **last tire or wheel** on one corner drops Handling Status to −6 immediately and permanently reduces Handling Class by 2 (tire only) or 3 (whole wheel, if the destroying hit came from mines/grenades/gunfire); treat it as a D6 hazard for the resulting Crash Table roll.
- Any vehicle that loses wheels at **two corners** (or any cycle/trike that loses even one wheel) goes straight to Crash Table 1, can no longer steer, accelerate, or brake, and must decelerate 30 mph every turn.
- **Debris**: hits any vehicle that touches its square (once per phase regardless of how many squares are entered); roll 1d per tire, subtract 3, for that tire's damage (1-3 on the die = no damage); it's a D1 hazard. Debris is created when a vehicle takes 10+ points of damage in one phase (1 random counter placed at the hit location) or explodes (5 random counters dropped from a foot up).
- **Obstacles**: a D3 hazard, checked the same way as debris; created when a vehicle loses a whole wheel, takes 20+ hits in one phase, or loses a point of metal armor.
- **Spikes**: entering the exact square rolls 1d, 1-4 = each tire takes 1d damage; an adjacent square rolls 1d, 1-2 = the same. Spikes last indefinitely; solid/plasticore tires take half damage. **Mines**: crossing the counter triggers on a 1-4 (1d), an adjacent square on a 1-2; each tire within 1" takes 1d damage and the triggering vehicle's underbody takes 2d (the Spear 1000 mine instead does 1d−3 to tires and 2d+3 to the underbody); the counter is removed once set off. **Oil slicks** add D2 to any maneuver and D2 to any hazard's severity without being a hazard themselves, and last indefinitely; flaming oil is a D1 hazard to drive over, adds D2 to maneuvers/hazards, burns for 5 turns, then becomes an ordinary smoke cloud.
- **Paint and smoke**: smoke lasts about one minute, paint about one second (removed at the end of the following turn); tracing a line of fire through either costs −1 per 1/2" of cloud (rounded up), and lasers cannot fire through either at all (Infrared lasers can, at a damage penalty). A vehicle that touches a paint cloud is at −2 to hit for the rest of that turn plus the next three turns.

### Buildings and cover
- A building is targeted at **+10** to hit (it's stationary and huge). Damage equal to or greater than its DP creates a breach; smaller hits accumulate no lasting effect. A building collapses once its accumulated breaches equal its DP (some buildings list two DP numbers, X(Y): X damage per breach, Y breaches to collapse). A collapsing building does damage dice equal to its DP to everyone and everything inside; cars take this to their top armor.
- **Rubble**: no vehicles may enter it; pedestrians move through it 1 square per turn (phase 1 only). It still blocks line of sight between roads. A pedestrian firing from within rubble is "braced" (+1 to hit) but is at −4 to be hit himself.
- **Height**: firing at a higher target is at −1 per 10 feet of height difference; firing down has no penalty (but thrown weapons like grenades are −1 per 10 feet either way). Targets above the third floor generally can't be hit by street-level vehicular weapons unless the firer is farther away than the target is high.
- **Missed shots** in a building scenario keep traveling: a horizontal miss continues until it exits the map or hits an obstacle (and can hit anyone directly in its path, at an extra −2); a miss fired upward hits one story higher on a 1-2, two stories higher on a 3-4, or clears the building on a 5-6; a downward miss overshoots by 1-6 inches.

### Uncontrolled vehicles and substitute drivers
- If a **motorcycle's driver** is killed or knocked out, the cycle immediately rolls on Crash Table 1 with +4 added. Any other ground vehicle instead continues straight ahead, decelerating 5 mph per turn until it stops or hits something.
- A **sidecar passenger** can steer an incapacitated cycle but not use the brake/accelerator, and can fire a weapon only on a turn he isn't steering. In a larger vehicle, a front-seat gunner or passenger may take over — operating either the controls or the weapons (not both) in a turn — but every maneuver he makes carries an extra D2 difficulty. No vehicle may seat more than two people in front.
- Getting a dead driver out of the seat and a new one in takes 5 turns; the new driver may accelerate and/or fire starting on the 6th turn.

### Weapons, ammunition, and linking
- No more than **1/3 of a vehicle's total spaces** may hold weapons that fire in any one direction (round down); motorcycles and sidecars are exempt.
- Every driver and gunner position takes **2 spaces** (1 for the person, 1 for the controls); a passenger takes 1 space and no controls space. Only one driver per vehicle, but multiple gunners are allowed.
- **Grenade scatter:** a thrown grenade needs 9+ on 2d to hit its exact square (a natural 12 is required for a perfect landing); any lesser success rolls on the Direction table (right/left/long/short/combinations) and a Distance table scaled to how badly the to-hit roll was missed by. Maximum throw range is 5"; grenades thrown from a moving vehicle are at −2, and a grenade that would land behind the thrower is instead placed at his feet.
- **Targeting computers** ($1,000, +1 to-hit for one crew position; Hi-Res $4,000, +2) and Single-Weapon Computers ($500/+1 or Hi-Res $2,500/+2, tied to one weapon and position) cannot be combined with each other or with a Cyberlink for stacking bonuses.

### Pedestrians
- Base movement is 12.5 mph (1/4" per phase); a pedestrian may **Sprint** for +5 mph for up to 10 seconds, then continue at base speed for up to 10 more seconds before having to rest 1 second for every 2 seconds spent sprinting.
- Pedestrians have 3 DP (wound/unconscious/kill), may carry up to 6 Grenade-Equivalents (GEs) of gear, and can fire only once per turn (after which they can't move that turn); sprinting or crawling pedestrians cannot fire at all.
- **Spikes/oil for pedestrians:** entering a spike square risks 1d−4 damage on a 2d roll of 2-3; entering oil requires a 2d roll of 5+ (then 7+, 9+, 11+ for consecutive oil squares) to stay standing, or the pedestrian falls and must spend a second (with a roll of 7+) to stand back up.

## Player Reference

### Deceleration difficulty (beyond a free 10 mph/turn)
| Deceleration | Difficulty | Extra effect |
|---|---|---|
| 15 mph | D1 | — |
| 20 mph | D2 | — |
| 25 mph | D3 | — |
| 30 mph | D5 | — |
| 35 mph | D7 | 2 hits of damage to each tire |
| 40 mph | D9 | 1d damage to each tire |
| 45 mph | D11 | 1d+3 damage to each tire |
| More than 45 mph | Impossible without special equipment | — |

### Sample hazard difficulties
Hitting a curb, obstacle, or pedestrian D3; hitting loose debris D1; taking 1-5 hits of enemy fire D1, 6-9 hits D2, 10+ hits D3; driver injured/killed D2; losing the first tire/wheel of a pair D2; losing the last tire/wheel on a corner D6.

### Road condition modifiers (added to maneuver/hazard difficulty)
Off-road +D1; light rain +D1; heavy rain +D2; gravel +D1; oil +D2; light snow +D2; heavy snow +D3; ice/packed snow +D4. Banked curves reduce inward bends/swerves by −D1 (steep banking −D2) and increase outward ones by +D1 (+D2 steep); drifting outward is −D1, inward +D1.

### Key targeting modifiers (cumulative)
| Situation | Modifier |
|---|---|
| Point blank (<1") | +4 |
| Long range, per full 4" beyond that | −1 (4-7.99"=−1, 8-11.99"=−2, 12-15.99"=−3, ...) |
| Target/firer not moving | +1 each |
| Target speed 30-37.5 / 40-47.5 / 50-57.5 / 60-67.5 / 70-77.5 / 80+ mph | −1 / −2 / −3 / −4 / −5 / −6 |
| Compact or subcompact target | −1 |
| Car, from front or rear | −1 |
| Motorcycle/sidecar, from side / front-rear | −2 / −3 |
| Pedestrian (prone: −4; prone behind full cover, head up to fire: −6) | −3 |
| Vehicle tire | −3 |
| Turret | −2 |
| Building | +10 |
| Ground (for burst/scatter shots) | +4 |
| Smoke or paint, per 1/2" in the way (rounded up) | −1 |
| Rain | −2 |
| Heavy rain, fog, or night | −3 |
| Target in rubble | −4 |
| Firer blinded by searchlight | −10 |
| Targeting Computer / Hi-Res Computer / Cyberlink | +1 / +2 / +3 |
| Sustained fire, 2nd consecutive shot at same target with same weapon | +1 |
| Attacker skidded/fishtailed this turn (minor / moderate-or-worse) | −3 / −6 |
| Not in target side's arc of fire | −2 |
| Hazard or maneuver fired in the same phase | minus that hazard/maneuver's D rating |

### Vehicular weapons (Chapter 6)
| Weapon | To-Hit | Damage | DP | Cost | Weight | Spaces | Shots (reload cost) |
|---|---|---|---|---|---|---|---|
| Autocannon (AC) | 6 | 3d | 4 | $6,500 | 500 lbs | 3 | 10 ($75 & 10 lbs each) |
| Machine Gun (MG) | 7 | 1d | 3 | $1,000 | 150 lbs | 1 | 20 ($25 & 2.5 lbs each); area effect |
| Vulcan Machine Gun (VMG) | 6 | 2d | 3 | $2,000 | 350 lbs | 2 | 20 ($35 & 5 lbs each); area effect |
| Anti-Tank Gun (ATG) | 8 | 3d | 5 | $2,000 | 600 lbs | 3 | 10 ($50 & 10 lbs each) |
| Grenade Launcher (GL) | 7 | by grenade type | 2 | $1,000 | 200 lbs | 2 | 10 grenades |
| Spike Gun (SG) | 7 | 1d | 2 | $750 | 150 lbs | 2 | 10 ($40 & 10 lbs each); area effect; −4 to fire directly at a target for 1d to tires/pedestrians only |
| Heavy Rocket (HR) | 9 | 3d | 2 | $200 | 100 lbs | 1 | 1 shot |
| Light Rocket (LtR) | 9 | 1d | 1 | $75 | 25 lbs | 1/2 | 1 shot |
| Medium Rocket (MR) | 9 | 2d | 2 | $140 | 50 lbs | 1 | 1 shot; burst effect |
| Micromissile Launcher (MML) | 8 | 1d | 2 | $750 | 100 lbs | 1 | 10 ($20 & 2.5 lbs each); burst effect |
| Mini Rocket (MNR) | 9 | 1d−1 | 1 | $50 | 20 lbs | 1/3 | 1 shot; burst effect |
| Multi-Fire Rocket Pod (MFR, "Six-Shooter") | 9 | 1d/rocket | 3 (1 dmg pt destroys 2 rockets) | $450 | 150 lbs | 2 | fires 6 rockets at once, rolled separately |
| Rocket Launcher (RL) | 8 | 2d | 2 | $1,000 | 200 lbs | 2 | 10 ($35 & 5 lbs each) |
| Light Laser (LL) | 6 | 1d | 2 | $3,000 | 200 lbs | 1 | area effect; 1 power unit/shot |
| Medium Laser (ML) | 6 | 2d | 2 | $5,500 | 350 lbs | 2 | area effect; 2 power units/shot |
| Laser (L) | 6 | 3d | 2 | $8,000 | 500 lbs | 2 | area effect; 2 power units/shot |
| Heavy Laser (HL) | 6 | 4d | 2 | $12,000 | 1,000 lbs | 3 | area effect; 3 power units/shot |
| Flamethrower (FT) | 6 | 1d | 2 | $500 | 450 lbs | 2 | 10 ($25 & 5 lbs each); area effect; max range 10" |
| Paint Spray (PS) | — | paint cloud | 2 | $400 | 25 lbs | 1 | 25 ($10 & 2 lbs each) |
| Smokescreen (SS) | — | smoke cloud | 4 | $250 | 25 lbs | 1 | 10 ($10 & 5 lbs each) |
| Flaming Oil Jet (FOJ) | — | 1d−2/turn to tires & underbody | 3 | $300 | 30 lbs | 2 | 25 ($35 & 2 lbs each) |
| Oil Jet (OJ) | — | slick only | 3 | $250 | 25 lbs | 2 | 25 ($10 & 2 lbs each) |
| Minedropper (MD) | — | 2d underbody, 1d/tire within 1" | 2 | $500 | 150 lbs | 2 | 10 ($50 & 5 lbs each); burst effect |
| Spear 1000 Minedropper (SMD) | — | 2d+3 underbody, 1d−3/tire within 1" | 2 | $750 | 150 lbs | 2 | 5 ($100 & 10 lbs each) |
| Spikedropper (SD) | — | tire damage on contact | 4 | $100 | 25 lbs | 1 | 10 ($20 & 5 lbs each) |

An Infrared version of any laser costs double and can fire through smoke/paint at −1 per die of damage for every 1/2" of cloud penetrated.

### Grenade types (all 1 Grenade-Equivalent to carry)
| Type | Cost | Effect |
|---|---|---|
| Concussion | $40 | 1 pt damage in a 1" radius; stun/unconsciousness effects out to 2" |
| Explosive | $25 | 1d to vehicles within 1/2", 1d to pedestrians within 2" |
| Fake | $5 | Looks real; does nothing |
| Flaming Oil | $75 | Creates a 1/2"x1/2" slick, ignites after 1 phase |
| Flash | $150 | Blinds for 1 second within 2" at night; doubled if the target wears LI goggles |
| Flechette | $20 | 1d to pedestrians/cyclists in a 2" radius; no effect on vehicles |
| Foam | $30 | Extinguishes fire in a 1" area on a roll of 1 (1d); can also be used as a visibility-blocker like paint |
| Paint | $20 | 1"x1" paint cloud |
| Smoke | $20 | 1"x1" smoke cloud |
| Tear Gas | $30 | 1"x1" cloud, lasts 1 minute; unprotected victims suffer stun/accuracy penalties |
| Thermite | $100 | 1d to everything within 1/2"; fire modifier 2, burn duration 1 |
| White Phosphorus | $75 | 1d to pedestrians (half to vehicles) within 1/2"; creates a smoke cloud; fire modifier 2, burn duration 1 |

### Vehicle-design key numbers
- **Chassis:** Light −10% weight capacity/−20% price; Standard: no change; Heavy +10% weight capacity/+50% price; Extra-Heavy +20% weight capacity/+100% price.
- **Car suspension:** Light (standard, included in body price); Improved 100% of body cost → base HC 2; Heavy 150% of body cost → base HC 3; Off-Road 500% of body cost → base HC 2 and negates off-road handling penalties. A van (or pickup over 5,500 lbs) has 1 less HC than a lighter vehicle with the same suspension; a subcompact has 1 more.
- **Trike suspension:** Light (free) → HC 0; Improved (100% of frame cost) → HC 1; Heavy (200% of frame cost) → HC 2 (max regular-trike HC is 3; a reversed trike gets +1 HC over an equivalent regular trike).
- **Cycle suspension cost tiers** follow the same no-extra/100%/200%/300%-of-frame-cost structure as trikes, topping out with an Off-Road option at 300% of frame cost.
- **Power plants:** Medium $1,000 (1,400 power factors); Large $2,000 (2,000 power factors); Super $3,000 (2,600 power factors); Sport $6,000 (3,000 power factors); Thundercat $12,000 (6,700 power factors).
- **Acceleration:** power factors < 1/3 of vehicle weight = vehicle won't move; 1/3 to <1/2 of weight = 5 mph/turn; 1/2 to <weight = 10 mph/turn; ≥ weight = 15 mph/turn.
- **Top speed formula (electric plants):** 360 x power factors / (power factors + weight), rounded down to a multiple of 2.5 mph.
- **Power capacity:** car/truck plants hold (spaces x 50) power units; cycle plants hold (DP x 25). A vehicle at ~60% of top speed ("cruising speed") gets about 200 miles of range; at top speed, about 100 miles. Every turn spent over a plant's derived maximum speed costs 1 power unit per full 10 mph over that limit (doubling at 20 mph over, etc.). Firing a laser costs power units too: 1 for a Light Laser, 2 for a Medium Laser or standard Laser, 3 for a Heavy Laser. A recharge takes about 10 minutes and costs $1 per 5 power units.
- **Tires:** Standard $50, Heavy-Duty $100 (plus Puncture-Resistant and Solid grades). Steelbelting: +50% cost/weight, +25% DP (round down). Radial: +150% cost, +20% weight, −1 DP, +1 HC if all wheels match. Off-Road tires: +20% cost, +5 lbs, +1 HC off-road only, no highway benefit. Fireproofing doubles tire cost.
- **Metal armor** costs 2.5x and weighs 5x standard plastic armor. **Fireproof** doubles cost, same weight. **Laser-Reflective** adds 10% to cost/weight. **Laser-Reflective Fireproof** costs 2.5x and weighs +10%.
- **Repairs:** armor $50/hit (x the armor type's cost modifier) or full replacement at original cost +10%; a component with 1 hit costs 10% of its price to fix, 2 hits 30%, 3 hits 50% (increasing thereafter); doing the labor yourself cuts the price by 1/3. Salvage value = original cost − repair cost (half that if sold rather than kept).

### Mechanic skill — Repair Chart difficulty tiers
Impossible (cannot be attempted): repair damaged tires, repair a computer. Very Hard: jury-rig a rocket or laser. Hard: jury-rig other components; repair a laser, rocket, radio, or power plant. Medium: repair any other weapon; reweld/patch armor; salvage a radio, power plant, or computer. Easy: replace a weapon link; salvage other items from a wreck. Trivial (anyone can attempt): reload ammunition; replace/salvage a tire; salvage spare magazines/unused ammo. A successful repair roll restores 1 DP (3 for armor); a mechanic may try once per hour (every 30 minutes at Mechanic +3). Modifiers: improvised tools −2, mini-mechanic tool −1, portable shop +1, full garage +2.

### Skills at a glance
Area Knowledge (know a region; free for home town), Climbing (free at base; trees −1, fences −2, buildings −3 to −5), Computer Tech (program/hack computers), Cyclist (ride cycles/trikes; −3 HC if untrained), Driver (drive 4/6-wheelers and reversed trikes; −2 HC if untrained; each + also adds to the reflex roll and to Handling Status recovered per turn; subtract the bonus from Crash Table rolls), Fast-Talk (talk your way out of trouble), Gunner (fire vehicular/tripod weapons; −3/−2 if untrained; +1 to-hit per level), Handgunner (fire hand weapons/grenades; −2 to hit if untrained with aimed hand weapons, grenades unaffected; +1 to-hit per level), Luck (+1/level to generic "roll and pray" checks only), Martial Arts (base = 2 hand-to-hand attacks/turn; +1 = +1 to hit; +2 = +1 damage; +3 = another attack; cycle repeats), Mechanic (see Repair Chart; max +3, learned only through career time, not skill points), Paramedic (save a character at 0 DP within 20 turns; briefly revive an unconscious victim), Running (free at base; +2.5 mph/level; Sprint adds +5 mph for up to 10 seconds), Security (defeat security systems), Streetwise (find contacts and illegal activity).

### Phase checklist (per turn)
1. Eligible vehicles accelerate/decelerate (once each, before moving). 2. Vehicles move in phase order per the Movement Chart (fastest first, reflexes break ties). 3. Maneuvers/hazards reduce Handling Status; failed Control Table rolls go to a Crash Table. 4. Weapons are fired and to-hit rolls made. 5. End of phase: all that phase's damage, debris, and obstacles resolve simultaneously. 6. End of turn: Handling Status recovers (min 1, capped at starting HC); fire/explosion checks for burning vehicles.
