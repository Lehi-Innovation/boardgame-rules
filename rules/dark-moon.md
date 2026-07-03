---
title: "Dark Moon"
bgg_id: 111124
player_count: "3-7"
play_time: "60-75 min"
designer: "Evan Derrick"
source_pdf: "dark-moon-rules.pdf"
extracted_date: "2026-03-19"
summarized_date: "2026-03-19"
verification: "minor_issues"
verification_date: "2026-07-03"
---
<!-- verification:begin -->
> ✅ **Verified (minor gaps)** — fact-checked against the rulebook text; only small omissions were found, nothing that changes how the game is played or scored.
>
> 📄 [Full rulebook text](https://jonnyallred.github.io/boardgame-rules/extracted/dark-moon-rules.txt) · 🚩 [Report a rules error](https://github.com/Lehi-Innovation/boardgame-rules/issues/new?template=rule-error.yml&labels=rule-error&title=%5BRule%20error%5D%20Dark%20Moon&game=dark-moon)
<!-- verification:end -->


## Overview

Dark Moon is a team-based game of paranoia and betrayal set on a space outpost. Players are secretly divided into Uninfected and Infected teams. The Uninfected must survive by completing three Events and a Final Event. The Infected want to destroy the outpost by breaching shields, damaging the outpost beyond repair, or compromising life support. Dice rolls are private — players submit dice publicly, creating opportunities for deception.

## Components

- 1 game board (Outpost master control panel)
- 10 player screens (7 Uninfected, 3 Infected)
- 7 Character cards (each with unique ability)
- 1 Commander card
- 7 Status cards (4 Uninfected, 3 Infected)
- 42 Task cards (21 silver-backed for 3/5/7 players, 21 black-backed for 4/6 players)
- 16 Event cards
- 6 Final Event cards
- 14 black Strong dice (faces shown as images in rulebook; mostly positive values with some negatives — predominantly positive)
- 14 red Weak dice (faces shown as images in rulebook; mostly negative values with some positives — predominantly negative)
- 1 blue Commander die
- 7 Participation tokens, 7 Quarantine tokens
- 14 Die tokens, 1 Sabotage token
- 18 Damage tokens, 6 Shield tokens, 6 Fatigue tokens, 6 Outpost tokens
- 18 cubes (13 blue Event, 1 blue Difficulty, 1 red Suspicion, 1 black Success)

## Setup

1. Place 2 Shield tokens on the first 2 spots of the Shield Track; remaining 4 in a pile.
2. Randomly draw and place 2 Outpost tokens on the Outpost Status panel (effects apply immediately). Rest in facedown pile.
3. Place Fatigue, Sabotage, Die, and Quarantine tokens near the board.
4. Place Suspicion cube at start of VOTE track; Difficulty and Success cubes above Difficulty track; Event cubes in pile.
5. Shuffle and deal 1 Character card faceup to each player.
6. Give each player matching Uninfected Player Screen.
7. Give each player 2 black Strong dice and 2 red Weak dice.
8. Give each player 1 Participation token.
9. Randomly determine starting Commander via Fatigue token draw. Commander gets Commander card and blue Commander die.
10. Draw and place 1 Final Event card faceup on Camera 4 space.
11. Prepare Status cards per player count (see table), shuffle, deal 1 facedown to each player.
12. Use correct Task deck (silver for 3/5/7 players; black for 4/6 players).
13. Shuffle Event deck. Commander draws 2 Event cards, places 1 faceup on Camera 1, discards the other to bottom of deck.
14. Player left of Commander starts; play proceeds clockwise.

**Status Cards by Player Count:**

| Players | Infected | Uninfected | Task Deck |
|---------|----------|------------|-----------|
| 3 | 1 | 2 | Silver |
| 4 | 1 | 3 | Black |
| 5 | 2 | 3 | Silver |
| 6 | 2 | 4 | Black |
| 7 | 3 | 4 | Silver |

## Turn Structure

Each turn follows these steps:

1. **Retrieve Dice** — Retrieve dice from Available Resources pool up to your die limit.
2. **Perform an Action** — Choose 1 action (if the Outpost station for that action isn't damaged).
3. **Choose a Task Card** — Draw 2 Task cards, play 1 faceup, discard the other facedown.
4. **Resolve the Task Card** — Resolve Malfunction or Complication.
5. **Add an Event Cube** (conditional) — If Task succeeded and card shows Event cube icon.
6. **Complete the Event** (conditional) — If all Event cubes filled.
7. **Select a New Event** (conditional) — Commander draws 2, chooses 1.
8. **Advance Suspicion Cube** (conditional) — If Task card shows suspicion icon.
9. **Hold a Vote** (conditional) — If Suspicion cube reaches vote space.

## Actions

### Repair Shield
Roll up to 3 dice privately, submit 1. Positive = success (remove farthest Shield token). Negative = fail.

### Repair Life Support
Roll up to 3 dice, submit 1. Positive = remove 1 Fatigue token (shuffled back). Negative = fail.

### Repair Outpost
Roll up to 3 dice, submit 1. Positive = remove 1 Outpost token (shuffled back, action restored). Always available regardless of damage.

### Call a Vote
Vote to quarantine or release a player. All players simultaneously reveal:
- Black Strong die = vote Uninfected (should NOT be quarantined)
- Red Weak die = vote Infected (SHOULD be quarantined)
- Empty hand = abstain

Majority wins. Ties broken by Commander. Dice used in vote return behind screens.

### Issue Order
Choose another player to either: retrieve 2 spent dice OR perform any 2 actions (neither can be Issue Order). Ordered player cannot use their Character ability.

### Lone Wolf
Roll up to 3 dice, submit 2. If both positive, add 1 Event cube to current Event/Final Event. May complete the Event.

### Reveal as Infected
A player holding an Infected Status card may reveal it to publicly switch to the Infected team. Revealing triggers all of the following, in order:
- If the player is not quarantined, they immediately execute the Infection Power on their Status card. They then roll any available die; if the result is positive, they may execute the Infection Power a second time.
- They discard their Character card, their Quarantine token (if they were quarantined), any Die tokens, and their Uninfected player screen, and take an Infected player screen instead. If the revealing player was the Commander, the Commander card passes to the first player to their left and the Commander die is placed in the Available Resources pool.
- Observing their new (lower) die limit on the Infected player screen, they discard down to two dice, returning any extra dice to the Available Resources pool.
- Their turn ends immediately — unless the reveal was their first action after being issued an order, in which case they may immediately take an Infected action.

Once revealed, an Infected player no longer has access to the normal actions above; instead they choose from five Infected-only actions (see below). Revealed Infected players also no longer draw Task cards at the end of their turn, can no longer participate in votes, and can no longer be voted on, quarantined, or fatigued. They still choose IN or OUT and submit dice normally during Malfunction Tasks (passing still lets them take up to two dice from the Available Resources pool), and they are unaffected by the Command Outpost token (they always retrieve two dice when passing).

### Infected-Only Actions
Available only to a player who has revealed as Infected; these replace that player's access to the normal actions above.

- **Sabotage** — Place the Sabotage token on the Shield Control, Outpost Status, or Life Support label to make repairs there harder (see Special Rules & Edge Cases), or move an existing Sabotage token to a different area. Only one area may be sabotaged at a time.
- **Test Commander** — The Commander must roll all of their active dice and submit one. Positive = success, nothing happens. Negative = the Infected player may draw a Damage token of their choice. If the Commander has no active dice, it is an automatic failure.
- **Demoralize** — Beginning with the first player to the Infected player's left, all players must replace all of their active black Strong dice with red Weak dice, until there are no more Weak dice left in the Available Resources pool.
- **Interference** — Draw three Task cards. Discard as many as desired and return the remaining cards to the top of the Task deck in any order chosen.
- **Energy Spike** — If there are 0-1 Shield tokens on the board, add one Shield token and, if applicable, test the shields. If there are two or more Shield tokens on the board, roll any die to test the shields; if it matches the Failure Condition, draw either a Fatigue or Outpost token.

## Scoring / Victory Conditions

### Uninfected Win
Complete 3 Events and the Final Event before the Infected destroy the outpost.

### Infected Win (any one of these)
1. **Shield Breach**: All 6 Shield tokens placed on the Shield Track.
2. **Outpost Destroyed**: All 6 Outpost tokens placed on the Outpost Status panel.
3. **Life Support Failure**: All 6 Fatigue tokens placed on players.

The Infected win **instantly** when any condition is met.

## Special Rules & Edge Cases

- **Dice are private**: Players may never reveal what they rolled. Only submitted dice are public.
- **Quarantine**: Quarantined players have their die limit reduced by 2 (they always keep at least 1 die). On their turn, a quarantined player retrieves dice normally but may only use the actions CALL VOTE, ISSUE ORDER, and REVEAL AS INFECTED. They do NOT draw Task cards at the end of their turn. They may still participate in votes and Malfunction Tasks normally. If the Commander is quarantined, the Commander card passes to the player who called the vote (or to the first non-quarantined player to the left if the vote-caller is also quarantined).
- **Sabotage token**: Placed by revealed Infected players to make repairs harder. A player repairing a sabotaged area must discard 2 additional dice after the repair attempt (whether it succeeded or not), removing the Sabotage token. Only one area may be sabotaged at a time.
- **Commander die** (blue): Only the Commander retrieves and uses it. Cannot be used for voting.
- **Die tokens**: Increase or decrease a player's die limit.
- **Fatigue tokens**: When drawn, match to a character in play; that character flips their card and becomes fatigued (cannot use their special ability, may only submit 1 die during Malfunction Tasks). If the character is not in play, the token still counts toward the Infected team's win condition but penalizes no one.
- **Malfunction resolution**: All participating players must roll and submit at least 1 die. Players who pass (choose OUT) may take up to 2 dice from Available Resources instead. Players may reroll their dice multiple times but must submit at least 1 die each time they roll. Success = final total >= difficulty number. Failure = consequence on card.
- **Complication tasks**: Require specific player choices rather than dice rolling.
- **Shield testing**: Whenever Shield tokens are placed on the board (from a failed Malfunction, an Event card, an Infection Power, or an ENERGY SPIKE action), the active player rolls any available die to test the shield. Check the result against the current Failure Condition shown on the Shield track (-1, "ANY +", -2, "ANY –" for the 4 positions respectively). If the result matches the Failure Condition, the active player must choose to draw either a Fatigue token or an Outpost token and place it on the board.
- **Fatigue**: A fatigued character cannot use their special ability and may only submit a single die during Malfunction Tasks. Fatigue is removed by a successful REPAIR LIFE SUPPORT action.
- When the Task deck runs out, shuffle discards to form new deck (don't reveal facedown cards).
- After completing 3 Events, the Final Event is revealed. Completing it wins for Uninfected.
- The 3-4 player game removes the "Voluntary Blood Testing" card from Status cards.

## Player Reference

**Turn Sequence:**
1. Retrieve dice to limit → 2. Action → 3. Draw 2 Tasks, play 1 → 4. Resolve Task → 5-9. Conditional steps

**Strong Die (Black):** Faces shown as images in rulebook (predominantly positive)
**Weak Die (Red):** Faces shown as images in rulebook (predominantly negative)
**Commander Die (Blue):** Special (Commander only)

**Actions Quick List:**
- Repair Shield / Life Support / Outpost (roll ≤3, submit 1)
- Call a Vote (quarantine/release)
- Issue Order (costs no dice, target does 2 actions)
- Lone Wolf (roll ≤3, submit 2, both must be positive)
- Reveal as Infected (see Actions section for transition effects)

**Infected-Only Actions (replace normal actions after revealing):**
- Sabotage (place/move Sabotage token; repairing a sabotaged area costs 2 extra dice)
- Test Commander (Commander rolls & submits 1 die; negative = Infected player draws a Damage token; no active dice = automatic failure)
- Demoralize (players from the Infected player's left replace Strong dice with Weak dice until the pool has none left)
- Interference (draw 3 Tasks, discard any number, return the rest to top of deck in any order)
- Energy Spike (add/test a Shield token if 0-1 on board; otherwise roll to test shields, drawing a Fatigue/Outpost token on a match)

**Infected Win Conditions (any one):**
- 6 Shield tokens placed
- 6 Outpost tokens placed
- 6 Fatigue tokens placed
