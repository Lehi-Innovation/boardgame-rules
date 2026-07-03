---
title: "Cold War: CIA vs KGB"
bgg_id: 24742
player_count: "2"
play_time: "30-60 min"
designer: "Jérémy Pinget"
source_pdf: "cold-war-cia-vs-kgb-rules.pdf"
extracted_date: "2026-03-19"
summarized_date: "2026-03-19"
verification: "minor_issues"
verification_date: "2026-07-03"
---
<!-- verification:begin -->
> ✅ **Verified (minor gaps)** — fact-checked against the rulebook text; only small omissions were found, nothing that changes how the game is played or scored.
>
> 📄 [Full rulebook text](https://jonnyallred.github.io/boardgame-rules/extracted/cold-war-cia-vs-kgb-rules.txt) · 🚩 [Report a rules error](https://github.com/Lehi-Innovation/boardgame-rules/issues/new?template=rule-error.yml&labels=rule-error&title=%5BRule%20error%5D%20Cold%20War%3A%20CIA%20vs%20KGB&game=cold-war-cia-vs-kgb)
<!-- verification:end -->


## Overview

Cold War: CIA vs KGB is a two-player card game where one player controls the CIA and the other the KGB. Each game turn represents one year of conflict, with a single country or event becoming the focus of a covert ideological clash. Players send undercover agents to infiltrate and manipulate local groups to gain the upper hand. The first player to accumulate 100 victory points wins.

## Components

- 12 agent cards (6 CIA, 6 KGB)
- 21 objective cards (15 nations, 6 events)
- 24 group cards (6 military, 6 economic, 6 media, 6 political)
- 2 domination tokens (1 CIA blue, 1 KGB red)
- 1 balance token
- 2 score cards (1 CIA, 1 KGB)
- 2 score tokens
- 1 rulebook

## Setup

1. Shuffle objective cards; place facedown as the objective deck.
2. Shuffle group cards; place facedown as the group deck.
3. Each player takes their 6 agent cards facedown as their headquarters.
4. Each player takes their domination token, score card, and score token.
5. Assign the balance token randomly (one player hides it in a fist, the other guesses; if correct, the guesser takes the token, otherwise the hider keeps it).

## Turn Structure

Each game turn has six phases:

### Phase 1: Briefing
1. **Determine the Objective:** Flip the top objective card face up. This is the current objective.
2. **Assign the Balance Token:** The player with the lowest VP takes it. If tied, the player who lost last turn's Cease-fire takes it. If both players caused civil disorder last turn, the token stays with its current owner. First turn: assigned randomly.
3. **Shuffle the Group Deck:** Shuffle previous turn's discards back into the group deck (one player shuffles, the other cuts). If either player successfully used their Analyst last turn, that player then looks at the top three cards of the group deck and replaces them in any order.

### Phase 2: Planning
Each player secretly chooses one agent from their headquarters as their Agent X, placing it facedown. Agents who are terminated cannot be chosen. Agents on leave from last turn cannot be chosen. If a player used the Double Agent's agenda last turn (the "see opponent's Agent X" effect), they may look at their opponent's Agent X choice before choosing their own.

Once both players have chosen their Agents X, agents on leave return to their respective headquarters (ready for future turns).

### Phase 3: Influence Struggle
The balance token holder decides who goes first. Players alternate taking one action:
- **Recruit a Group:** Draw the top group card and place it face up (must recruit if you have no groups).
- **Activate a Group:** Mobilize (turn sideways) one ready group to use its power.
- **Pass:** Do nothing.

A player with no group cards must always recruit (cannot pass or activate). The phase ends when both players pass consecutively. Players try to accumulate Influence as close to the objective's Stability score as possible without exceeding it. A player may never recruit a group if it would make them exceed the objective's population limit.

### Phase 4: Cease-fire
1. The player with the highest Influence total that does not exceed the Stability score places their domination token on the objective.
2. **Ties:** Broken by the bias icons on the objective card — compare the largest faction icon first; the player with the highest Influence group of that faction wins. If neither has that faction, move to the next icon.
3. **Civil disorder:** If a player's Influence total exceeds the Stability, their Agent X is revealed and terminated (removed from the game permanently). Their opponent immediately claims the objective. Exception: the Deputy Director is never terminated even for civil disorder — he returns directly to headquarters instead.
4. If **both** players cause civil disorder, both Agents X are revealed and terminated (except the Deputy Director). The objective is placed facedown at the bottom of the objective deck — neither player claims it.

### Phase 5: Debriefing
1. Each player reveals their Agent X (unless terminated by civil disorder).
2. Agent agendas are resolved in initiative order, from lowest (1) to highest (6).
3. After all agendas are resolved, if neither player has claimed the objective through an agenda, the player who placed their domination token on the objective claims it and scores its VP.
4. Domination tokens are returned to their owners.
5. All group cards are discarded.

### Phase 6: Détente
1. Each surviving (non-terminated) Agent X goes on leave — placed faceup beside the player's headquarters, unavailable next turn. Exception: the Deputy Director never goes on leave; he returns directly to headquarters.
2. Each player updates their score token to reflect objectives claimed this turn.
3. Check for victory (see Scoring). If neither player has won, the next turn begins.

## Actions

### Group Factions and Powers
| Faction | Power |
|---------|-------|
| Military | Destroy any other group card in play (on either player's side); cannot destroy itself |
| Political | Steal a group from opponent or give them one of yours; cannot make either player exceed the population limit, nor make the opponent exceed Stability (but you may move an opponent's group to your own side even if it would cause you to exceed Stability — risky but legal); groups retain their ready/mobilized state |
| Economic | Switch the state of any other group card in play — turn a ready card mobilized or a mobilized card ready (if turning a ready card mobilized, that group's power does not take effect); cannot affect another economic card |
| Media | Look at the top card of the group deck, then choose to: recruit it (place it faceup in front of you), discard it, or leave it on top of the deck |

### Agent Abilities (resolved in initiative order, lowest first)
| Initiative | Agent | Agenda |
|------------|-------|--------|
| 1 | Master Spy | Causes the objective to be claimed by the player who did **not** place their domination token on it (reverses the outcome) |
| 2 | Deputy Director | No effect on the outcome; never terminated (even for civil disorder) and never goes on leave — returns directly to headquarters |
| 3 | Double Agent | **Either** sends one agent from the opponent's headquarters immediately on leave, **or** allows the Double Agent's player to see the opponent's Agent X during next turn's Planning phase before choosing their own. If two Double Agents face each other, only the one whose domination token was placed fulfills the agenda |
| 4 | Analyst | Allows the player to look at the top three cards of the group deck during next turn's Briefing phase and replace them in any order. If two Analysts face each other, only the one whose domination token was **not** placed fulfills the agenda |
| 5 | Assassin | If the Assassin's side placed its domination token: the opponent's Agent X is terminated (removed from game) **and** the objective is sent to the bottom of the objective deck |
| 6 | Director | If the Director's side placed its domination token: the Director's player wins an additional objective (the card at the bottom of the objective deck), scoring its VP in addition to the current objective |

Some agendas have different effects depending on which player's domination token is on the objective; see source card text. Do not resolve agendas for agents terminated by civil disorder.

## Scoring / Victory Conditions

- Each objective card has a VP value. The player who claims it scores that VP.
- First player to reach 100 VP during the Détente phase wins.
- If both players reach 100 VP in the same Détente phase, the higher total wins. If still tied, play additional turns until the tie is broken.

## Special Rules & Edge Cases

- **Civil disorder:** Exceeding the Stability score terminates your Agent X permanently. The opponent immediately claims the objective.
- Terminated agents cannot be chosen in future turns.
- Agents on leave skip one turn, then return to headquarters at the end of the Planning phase of the following turn.
- A player with no groups must recruit (cannot pass or activate).
- The population limit on objective cards restricts the maximum number of groups a player may have.
- Event objectives have special abilities detailed on the cards. Using an event card's special ability costs that card's VP — the player must discard it to the objective deck's discard pile and update their score token immediately. The rulebook does not describe any procedure for reshuffling this discard pile back into the objective deck, nor address what happens if the objective deck runs out.

## Player Reference

| Phase | Action |
|-------|--------|
| 1. Briefing | Reveal objective, assign balance token, shuffle groups |
| 2. Planning | Secretly choose Agent X (agents on leave return to HQ after both players choose) |
| 3. Influence Struggle | Recruit, activate, or pass (alternating); ends when both pass consecutively |
| 4. Cease-fire | Reveal domination token placement, apply tie-breaker (bias icons), resolve civil disorder |
| 5. Debriefing | Reveal agents, resolve agendas in initiative order (1→6), winner claims objective |
| 6. Détente | Surviving agents go on leave; update scores; check for 100 VP victory |
