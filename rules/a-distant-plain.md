---
title: "A Distant Plain"
bgg_id: 127518
player_count: "1-4"
play_time: "120-360 min"
designer: "Brian Train, Volko Ruhnke"
source_pdf: "a-distant-plain-rules.pdf"
extracted_date: "2026-03-18"
summarized_date: "2026-03-18"
verification: "verified"
verification_date: "2026-06-17"
---
<!-- verification:begin -->
> ✅ **Verified** — this summary was fact-checked against the rulebook text and no significant issues were found.
>
> 📄 [Full rulebook text](https://jonnyallred.github.io/boardgame-rules/extracted/a-distant-plain-rules.txt) · 🚩 [Report a rules error](https://github.com/Lehi-Innovation/boardgame-rules/issues/new?template=rule-error.yml&labels=rule-error&title=%5BRule%20error%5D%20A%20Distant%20Plain&game=a-distant-plain)
<!-- verification:end -->


## Overview

A Distant Plain is a COIN Series (Volume III) game depicting counterinsurgency conflict in modern Afghanistan. Each player controls one of four Factions -- the international Coalition, the Afghan Government, the Islamist Taliban, or narco-trafficking Warlords -- using military, political, and economic actions to influence the Afghan population. Cards regulate turn order, events, and victory checks. Non-player rules enable solitaire, 2-player, or 3-player games.

## Components

- 1 mounted 22"x34" game board (map of Afghanistan)
- 78-card deck (Event cards + Propaganda cards)
- 158 wooden force pieces (medium/light blue, tan, black, green; some embossed)
- 7 embossed cylinders
- 6 red and 6 white pawns
- Marker sheet
- Sequence of Play sheet
- 4 Faction player aid foldouts
- 1 Non-player aid foldout
- 1 Random Spaces sheet
- 3 six-sided dice (tan, black, green)

## Setup

Per scenario instructions (pages 19-20 of rulebook). Each faction places forces and markers per the setup chart. Shuffle Event deck with Propaganda cards mixed in at designated intervals.

## Turn Structure

Cards are played from the deck one at a time, with the next card always revealed to all players.

### Card Resolution
1. Reveal the next card from the deck (one card always showing ahead).
2. The current Event card shows **faction eligibility order** (4 factions listed).
3. The **1st Eligible Faction** may: Execute the Event (shaded or unshaded text), Conduct an Operation (with optional Special Activity), or Pass.
4. The **2nd Eligible Faction's** options depend on what the 1st Eligible chose:
   - If 1st executed an **Operation only**: 2nd may execute a Limited Operation (1 space, no Special Activity).
   - If 1st executed **Op + Special Activity**: 2nd may execute a Limited Operation or the Event.
   - If 1st executed the **Event**: 2nd may execute an Operation (with optional Special Activity).
   - Or Pass (gain resources as above).
5. Factions that Execute an Event or Operation become **Ineligible** for the next card.
6. Factions that Pass or were not Eligible remain Eligible.

### Propaganda Rounds
When a Propaganda card is drawn, all factions execute a sequence:
1. **Victory Check** -- Each faction checks if it meets its victory condition; if any does, game ends.
2. **Resources** -- Factions collect resources (Government earns Aid + LoC economic values; Insurgents earn per Base/Guerrilla count).
3. **Support Phase** -- COIN Factions (Coalition and Government) may spend Resources to shift spaces toward Support; Taliban may spend Resources to shift toward Opposition.
4. **Redeploy** -- Government loses cubes to Desertion; Coalition and Government reposition Troops; Taliban must redeploy Guerrillas lacking local Bases to Pakistan or Taliban-Controlled spaces.
5. **Reset** -- All factions become Eligible; Terror and Sabotage markers removed; Guerrillas flipped Underground.

## Actions

### Operations (per Faction)

| Faction | Operations |
|---------|-----------|
| **Coalition** | Train, Patrol, Sweep, Assault |
| **Government** | Train, Patrol, Sweep, Assault |
| **Taliban** | Rally, March, Attack, Terror |
| **Warlords** | Rally, March, Attack, Terror |

### Special Activities (one per Operation)

| Faction | Special Activities |
|---------|-------------------|
| **Coalition** | Surge, Transport, Airstrike |
| **Government** | Govern, Transport, Eradicate |
| **Taliban** | Infiltrate, Suborn, Extort |
| **Warlords** | Cultivate, Suborn, Traffic |

### Key Operations
- **Train:** Place Government/Coalition forces; build bases.
- **Rally:** Place Insurgent forces; build bases.
- **Sweep/Patrol:** Activate (reveal) underground guerrillas.
- **March:** Move insurgent forces.
- **Assault/Attack:** Remove enemy forces from spaces.
- **Terror:** Place Terror markers; shift population toward Opposition.

## Scoring / Victory Conditions

Each faction has a unique victory condition checked during Propaganda Rounds (section 7.2). All conditions use "exceeds" (strictly greater than) the listed threshold:

| Faction | Victory Condition |
|---------|------------------|
| **Coalition** | Total Population in Support + number of Coalition pieces in Available Forces box > 30 |
| **Government** | Total COIN-Controlled Population + Patronage > 35 |
| **Taliban** | Total Population in Opposition + number of Taliban Bases on the map > 20 |
| **Warlords** | Uncontrolled Afghan Population > 15 AND Warlord Resources > 40 |

If no faction wins after the final Propaganda card, the faction with the highest victory margin wins. Victory margin = how far a faction is beyond or short of its condition (positive = past goal; negative/zero = not reached). Tiebreakers: Non-players, then Warlords, then Government, then Taliban.

## Special Rules & Edge Cases

- **Control:** A Province or Kabul is COIN-Controlled if the Coalition and Government pieces together exceed all other Factions combined; it is Taliban-Controlled if Taliban pieces alone exceed all others combined. If neither applies, the space is uncontrolled. Warlords cannot Control spaces.
- **Support/Opposition:** Population spaces range from Active Support through Neutral to Active Opposition.
- **Underground vs. Active:** Guerrillas start underground (hidden) and must be Activated (revealed) before they can be targeted by Assault.
- **Lines of Communication (LoCs):** Roads that can hold forces; important for economic value and government control.
- **Patronage:** Represents corruption; Government gains resources but Coalition loses support.
- **Pakistan:** Neighboring provinces where Taliban can safely base.
- **Non-Player rules:** Detailed flowcharts for running AI-controlled factions.

## Player Reference

| Faction | Color | Force Types |
|---------|-------|-------------|
| Coalition | Medium blue | Troops, Bases |
| Government | Light blue | Troops, Police, Bases |
| Taliban | Black | Guerrillas, Bases |
| Warlords | Green | Guerrillas, Bases |

| Map Spaces | Types |
|------------|-------|
| Mountain Province | Harder to Assault |
| Plains Province | Standard |
| City (Kabul) | High population |
| Lines of Communication | Roads, economic value |
| Pashtun spaces | Cultural alignment |
| Pakistan provinces | Taliban safe haven |
