---
title: Captain Sonar
bgg_id: 171131
player_count: 2-8
play_time: 45-60 minutes
designer: Roberto Fraga, Yohan Lemonnier
source_pdf: captain-sonar-rules.pdf
extracted_date: 2026-03-18
summarized_date: 2026-03-18
verification: "verified"
verification_date: "2026-06-17"
---
<!-- verification:begin -->
> ✅ **Verified** — this summary was fact-checked against the rulebook text and no significant issues were found.
>
> 📄 [Full rulebook text](https://jonnyallred.github.io/boardgame-rules/extracted/captain-sonar-rules.txt) · 🚩 [Report a rules error](https://github.com/Lehi-Innovation/boardgame-rules/issues/new?template=rule-error.yml&labels=rule-error&title=%5BRule%20error%5D%20Captain%20Sonar&game=captain-sonar)
<!-- verification:end -->


## Overview

Captain Sonar is a real-time team game where two submarines hunt each other on a grid map. Each team of up to 4 players takes on distinct roles: Captain (navigation), First Mate (systems), Engineer (maintenance), and Radio Operator (tracking). In real-time mode, both teams play simultaneously, shouting orders and tracking the enemy. In turn-by-turn mode, teams alternate. The first team to score 4 damage on the enemy submarine wins.

## Components

- 2 screens (placed end-to-end in the center of the table)
- 2 sets of 12 role sheets (one set per team, each two-sided: light side for turn-by-turn, dark side for real-time)
  - Per team: 1 First Mate sheet, 1 Engineer sheet, 5 Captain sheets (1 per scenario), 5 Radio Operator sheets (1 per scenario)
- 2 transparent Radio Operator sheets
- 8 erasable marker pens

## Setup

1. Both teams choose the same map. Each team takes a Captain screen, Radio Operator screen, Engineer sheet, and First Mate sheet.
2. Each team secretly places their starting position on their Captain screen by marking it.
3. Both teams must agree on whether to play real-time or turn-by-turn mode.
4. Assign roles within each team (Captain, First Mate, Engineer, Radio Operator).

## Turn Structure

**Real-Time Mode:** Both teams play simultaneously with no turns. The Captain announces each movement direction aloud ("Heading North/South/East/West!"). There is no pause between moves unless the Captain calls "Stop" to use a system or surface.

**Turn-By-Turn Mode:** Teams alternate. On your team's turn, the Captain chooses one action: move, surface, or use a system.

**Movement:** The Captain announces a cardinal direction and draws the path on their screen. The submarine moves one space. The sub cannot cross its own path, islands, or map edges.

**After each move:**
- The First Mate marks one space on any system gauge.
- The Engineer crosses off one breakdown symbol in the zone matching the movement direction.

## Actions

**Systems (activated when fully charged by the First Mate):**

- **Torpedo (range 1-4):** The Captain announces target coordinates. Deals 2 damage to direct hit, 1 damage to adjacent spaces. The target Captain must announce if hit.
- **Mine (deploy + detonate):** Deploy a mine on an adjacent space. Later, detonate by announcing coordinates. Same damage as torpedo.
- **Drone:** The Captain names a sector. The enemy Captain must truthfully answer whether their sub is in that sector.
- **Sonar:** The enemy Captain must give 2 pieces of information about their position (row, column, or sector) — one must be true, one must be false.
- **Silence:** The submarine moves 0-4 spaces in one direction without announcing direction. The Radio Operator only knows "Silence was activated."
- **Scenario-specific systems:** Some maps include unique systems.

**Surfacing:** The Captain raises a fist and announces "SURFACE," then declares the submarine's current sector aloud to the enemy.
- **Turn-by-turn mode:** Surfacing uses the Captain's turn. The Engineer erases ALL breakdowns. The enemy team then takes **three turns in a row** (if the enemy also surfaces during those turns, any remaining turns are lost). Then play resumes normally.
- **Real-time mode:** Teammates secure the submarine by each drawing a line around one of the four sub sections on the Engineer's sheet and writing initials, passing the sheet until all four sections are secured. The enemy Engineer confirms no lines are drawn outside the white outline. The Engineer then erases all section lines, initials, and ALL breakdowns. When complete, the Engineer announces "READY TO DIVE" and the Captain announces "DIVE." While surfaced, the enemy team continues playing. The Captain resets his route (erasing it but keeping current position and mine positions).

## Scoring / Victory Conditions

Each submarine has 4 health points. A team wins by reducing the enemy submarine to 0 health. Direct torpedo or mine hits deal 2 damage; indirect hits (adjacent space) deal 1 damage.

If a submarine surfaces, the enemy knows which sector it is in.

## Special Rules & Edge Cases

- The submarine cannot cross its own path line (it must surface or use silence to reset/reposition).
- If the Captain cannot announce a course (blocked by islands, mines, or own route), the submarine must immediately surface (BLACKOUT).
- A team cannot activate two systems in a row; the Captain must announce a course between activations.
- **Engineer breakdowns:** Each time the Captain announces a direction, the Engineer crosses off one symbol in the matching compass panel (North/South/East/West). A system cannot be activated if **at least one** symbol corresponding to that system is crossed out. (Each symbol corresponds to two systems: Mine+Torpedo share symbols, Drone+Sonar share symbols, Silence+Scenario share symbols.)
- **Central Circuits self-repair:** Symbols in the Central Circuits are grouped into circuits of four (linked by colored lines). When all four symbols on a circuit are crossed out, that circuit **self-repairs** — the Engineer erases those four symbols. Surfacing also repairs all Central Circuit breakdowns.
- **Radiation breakdowns (Reactor):** When ALL radiation symbols are crossed out, the submarine suffers 1 damage and the Engineer erases ALL breakdowns from the entire sheet. Surfacing also repairs all Reactor breakdowns.
- **Complete area breakdown:** When all symbols in a single compass panel (both Central Circuits and Reactor) are crossed out, the submarine suffers 1 damage and the Engineer erases ALL breakdowns.
- The Radio Operator uses the transparent sheet overlaid on the map to track the enemy sub's position using the directions announced by the enemy Captain.
- In real-time mode, the Captain must wait for the First Mate and Engineer to announce "OK" before announcing a new course.
- With fewer than 8 players, one player takes multiple roles (e.g., 3-player team: Captain + First Mate; 2-player team: Captain + First Mate + Engineer). In 2- or 3-player games, turn-by-turn mode is required.
- Self-damage: A submarine can be damaged by its own torpedo or mine if it is adjacent to or on the impact space.

## Player Reference

| Role | Responsibility |
|------|---------------|
| Captain | Navigate, call directions, activate systems, choose targets |
| First Mate | Charge systems (one mark per move) |
| Engineer | Manage breakdowns (one mark per move, in matching zone) |
| Radio Operator | Track enemy position using announced directions |

**Systems charge costs:** Torpedo = 3, Mine = 3, Drone = 4, Sonar = 3, Silence = 6

**Damage:** Direct hit = 2, Adjacent = 1, Health = 4 total
