---
title: "BattleCON: War of Indines"
bgg_id: 89409
player_count: "2"
play_time: "20-60 min"
designer: "D. Brad Talton Jr."
source_pdf: "battlecon-war-of-indines-rules.pdf"
extracted_date: "2026-03-18"
summarized_date: "2026-03-18"
verification: "verified"
verification_date: "2026-06-17"
---
<!-- verification:begin -->
> ✅ **Verified** — this summary was fact-checked against the rulebook text and no significant issues were found.
>
> 📄 [Full rulebook text](https://jonnyallred.github.io/boardgame-rules/extracted/battlecon-war-of-indines-rules.txt) · 🚩 [Report a rules error](https://github.com/Lehi-Innovation/boardgame-rules/issues/new?template=rule-error.yml&labels=rule-error&title=%5BRule%20error%5D%20BattleCON%3A%20War%20of%20Indines&game=battlecon-war-of-indines)
<!-- verification:end -->


## Overview

BattleCON: War of Indines is a two-player card game inspired by 2D fighting video games. Each player selects a unique character and fights duels by simultaneously selecting attack pairs (a Style card + a Base card). Attacks are revealed simultaneously, and priority determines who strikes first. Characters move along a 7-space linear board, using positioning, timing, and their unique abilities to reduce their opponent's life to zero. A match consists of best-of-three duels.

## Components

- 18 Unique character cards with special abilities
- Style cards (unique per character)
- Base cards (shared generic set per character)
- 7-space linear game board
- Life trackers (20 life points per player)
- Tokens and counters

## Setup

1. Each player selects a different character.
2. Each player takes all 7 of that character's cards (1 character card, 5 styles, and 1 base), plus a set of 6 generic bases, forming their starting hand.
3. Place both character tokens on the board: one on space 2, the other on space 6 (4 spaces apart, each on their owner's left-hand side).
4. Each player finds the two bases and two styles marked with icons "1" and "2" and places them in their two discard piles (discard 1 and discard 2). These cards are unavailable at the start of the game.
5. Set both players' life to 20.
6. Place any tokens or markers required by each character's unique abilities.

## Turn Structure

Each turn is called a "beat." Beats follow this sequence:

### 1. Select Attack Pairs (Simultaneous)
Both players secretly choose one Style card and one Base card from their hand to form their attack pair. Place them face-down.

### 2. Ante Tokens
Players may ante tokens (if their character's unique ability provides them) for additional effects. Tokens can be added but never taken back once placed.

### 3. Reveal Attack Pairs
Both players simultaneously flip their attack pairs face-up. Reveal effects trigger. Then check the priorities of both attacks.

**Clash:** If the total priorities tie, a Clash occurs. Both players play a new base face-down from their hands. Reveal simultaneously; the new base replaces the old one (hiding its effects and stats). Check for another clash. If players run out of cards during a clash, they pick up all bases in the attack and continue. When the clash resolves, only the top card remains in play; all cards beneath it return to the players' hands.

Once any clashes are resolved, Start of Beat effects of both attacks trigger (higher-priority character's effects first).

### 4. Execute Attacks
The player with higher priority is the **Active Player**; the other is the **Reactive Player**.

The active player activates their attack:
1. Resolve any Before Activating effects.
2. Check if the opponent is within range. Range is counted in spaces (the attacker's space is zero; adjacent is range 1).
3. If in range, resolve On Hit effects, then deal damage equal to the attack's Power (reduced by the defender's **Soak** value, if any).
4. If any damage was dealt, resolve On Damage effects. If the damage taken is greater than the defender's Stun Guard, the defender is stunned (see Stun below). If the defender's life reaches 0 or fewer, the duel ends immediately.
5. Resolve any After Activating effects (regardless of whether the attack hit).

If not stunned, the reactive player activates their attack in the same way. A stunned player skips activation entirely, including Before Activating and After Activating effects.

### 5. Recycle
Both players resolve End of Beat effects (active player first; stunned players may still resolve End of Beat effects). Then each player picks up their second discard pile, shifts the first discard pile to the second, and places this beat's attack pair face-up into the first discard pile.

## Actions

### Attack Pair Components

**Style Cards** (unique per character):
- Provide modifiers to Priority, Range, Power, and Stun Guard.
- May include special abilities (Before Activating, On Hit, After Activating, etc.).

**Base Cards** (shared set):
| Base | Priority | Range | Power | Special |
|------|----------|-------|-------|---------|
| Strike | 3 | 1-2 | 4 | Standard attack |
| Shot | 2 | 3-5 | 3 | Ranged attack |
| Drive | 4 | 1 | 3 | Advance 1-2 spaces |
| Burst | 1 | 2-3 | 3 | Retreat 1-2 spaces |
| Grasp | 5 | 1 | 2 | Move opponent 1 space |
| Dash | 9 | - | - | Move 1-3 spaces; no attack |

### Movement
- Movement is along the 7-space linear board.
- "Advance" (forwards) = move toward opponent.
- "Retreat" (backwards) = move away from opponent.
- When moving, characters **hop over** opponents — the space occupied by the opponent is not counted against movement. A character can pass through or end up on the other side of the opponent.
- If a movement effect specifies a fixed number of spaces (e.g., "move 1 or 2 spaces forwards"), it is mandatory; the player must take a legal movement option. "Move up to X" allows choosing zero.
- Characters cannot move past space 1 or space 7 (board edges). If a move is fully blocked by a wall, it is ignored.

### Stun and Stun Guard
A character is stunned whenever they take damage **greater than** their Stun Guard value. Attacks with no Stun Guard specified have an implied Stun Guard of 0. A hit for zero damage does not stun.

Multiple Stun Guard effects stack (e.g., Stun Guard 2 + Stun Guard 5 = Stun Guard 7).

### Soak
Some attacks or abilities provide a **Soak** value (e.g., Soak 3). Whenever that player would take damage during the beat, it is reduced by the Soak amount. Multiple Soak effects stack. Soak is always a passive effect.

## Scoring / Victory Conditions

- Each duel starts at 20 life. The first player whose life reaches 0 or fewer is eliminated; the other player wins the duel.
- A duel ends only when a player's life drops below zero from damage (during step 4 of a beat). Other effects cannot reduce a player below 1 life.
- A match awards the winner of each duel 1 match point. The first player to reach 2 match points wins the match (a standard match is thus typically two or three duels).

## Special Rules & Edge Cases

- **Card Rotation**: Cards used this beat and last beat are unavailable. Cards from 2 beats ago return to hand at the Recycle step. This creates a 2-beat cooldown that prevents spamming the same attack.
- **Unique Abilities**: Each character has one or more Unique Abilities that define their playstyle (e.g., Cadenza's Iron Body, Kallistar's Elemental Form, Khadath's Gate Trap, Hikaru's Geomantic Assault).
- **Overdrive Finish**: Triggered by pairing the Special Action card with a Strike, Drive, or the character's unique base. A character must have **7 or fewer** life points to use an Overdrive Finish. If life is too high, it becomes a Cancel instead. The Overdrive Finish always wins priority ties without clashing. The discard pile does not cycle the turn a Finish is used; the base played with it returns to hand.
- **Pulse**: Special Action + Burst or Dash. Negates the opponent's entire action; the Pulse player then pushes the opponent and themselves any number of spaces backwards. If both players Pulse simultaneously, both push each other back as far as possible. Discard pile does not cycle for the Pulse user.
- **Cancel**: Special Action + Grasp or Shot. Return the paired base to hand, remove Cancel from the game, then select a new attack pair. Tokens anted still apply.
- **Clash**: Occurs when both players' priority values tie at reveal. Both players play a new base face-down; the new base overlays the old one. This continues until no tie. All cards beneath the final top card return to hand.
- **Special Actions**: Each player receives one Special Action card at the start of a duel. After use, it is removed from the game until the end of the duel.
- **Board Edges**: Characters cannot move past space 1 or space 7.

## Player Reference

### Beat Sequence
1. Both players select Style + Base face-down
2. Ante tokens (characters with tokens may ante before reveal)
3. Reveal simultaneously; resolve Reveal effects; check for Clash (priority tie → both play new base face-down, repeat until resolved)
4. Start of Beat effects (higher priority first)
5. Active player (higher priority): Before Activating → range check → On Hit/damage/Soak → stun check → After Activating
6. Reactive player (if not stunned): same steps
7. Recycle: End of Beat effects, then shift discard piles (pick up discard 2 → discard 1 becomes discard 2 → current pair becomes discard 1)

### Key Stats
| Stat | Effect |
|------|--------|
| Priority | Determines who attacks first; tie = Clash |
| Range | Distance(s) at which the attack hits (attacker's space = 0) |
| Power | Damage dealt on hit (reduced by opponent's Soak) |
| Stun Guard | Player is stunned only if damage taken is **greater than** this value |
| Soak | Reduces incoming damage by this amount (passive, stacks) |

### Quick Reference
- Starting life: 20
- Starting positions: spaces 2 and 6
- Board size: 7 spaces
- Match: First to 2 match points (each duel won = 1 match point)
- Card cycle: 2-beat cooldown (discard 1 unavailable, discard 2 unavailable)
- Overdrive Finish: requires 7 or fewer life points
- Movement: characters hop over opponents (opponent's space not counted)
