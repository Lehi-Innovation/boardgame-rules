---
title: "Gloomhaven"
bgg_id: 174430
player_count: "1-4"
play_time: "60-120 min"
designer: "Isaac Childres"
source_pdf: "gloomhaven-rules.pdf"
extracted_date: "2026-03-20"
summarized_date: "2026-08-05"
verification: "verified"
verification_date: "2026-08-08"
---
<!-- verification:begin -->
> ✅ **Verified** — this summary was fact-checked against the rulebook text and no significant issues were found.
>
> 📄 [Full rulebook text](https://lehi-innovation.github.io/boardgame-rules/extracted/gloomhaven-rules.txt) · 🚩 [Report a rules error](https://github.com/Lehi-Innovation/boardgame-rules/issues/new?template=rule-error.yml&labels=rule-error&title=%5BRule%20error%5D%20Gloomhaven&game=gloomhaven)
<!-- verification:end -->


## Overview

Gloomhaven is a cooperative game of battling monsters and advancing each player's individual goals, designed to be played as a campaign: a group strings together a series of scenarios using the Scenario Book, unlocking new content as they progress. Any revealed scenario can also be played as a stand-alone experience (casual mode). Each scenario is tactical combat on a modular hex map — players act with two-card ability hands, monsters are automated by their own ability decks, and attacks are resolved with attack modifier card decks instead of dice. A scenario is won by meeting its victory condition; if all characters become exhausted first, the scenario is lost.

## Components

- 1 rule book, 1 scenario book, 1 town records book, 1 map board
- 18 character miniatures, 17 character boards, 17 character pads, 35 character tuck boxes
- 504 character ability cards
- 457 attack modifier cards
- 253 item cards
- 232 monster ability cards, 240 monster standees, 24 plastic stands
- 47 monster stat sheets, 6 monster stat sleeves
- 150 event cards, 24 battle goal cards, 24 personal quest cards
- 9 random scenario cards, 40 random dungeon cards
- 30 two-sided map tiles, 155 two-sided overlay tiles
- 50 money tokens, 46 damage tokens, 60 status tokens, 85 character tokens
- 32 summon tokens, 12 objective tokens, 10 scenario aid tokens
- 4 HP/XP tracking dials, 4 player reference cards
- 6 wood element discs, 1 element infusion board, 1 round tracker
- 1 party pad, 3 sealed envelopes, 4 sticker sheets

## Setup

1. Pick a scenario in the Scenario Book. Lay out its map tiles, connected by doors, and set up the overlay tiles, monsters, and money tokens for the **first room only**. Randomize monster standee numbers when placing. Read the scenario introduction and apply any negative effects in its "Special Rules."
2. Each player has a character (only one copy of each class per scenario; the Brute, Tinkerer, Spellweaver, Scoundrel, Cragheart, and Mindthief are available when the box is first opened). Take the character mat, character tokens, HP/XP tracking dial, and the class's ability cards.
3. Set out each monster type's statistic card, rotated/sleeved to the chosen scenario level, with its shuffled ability deck. Shuffle an attack modifier deck for each player and one for the monsters — a standard deck is twenty cards, and may be modified by perks, items, scenario effects, and CURSE/BLESS.
4. Deal each player **two** battle goal cards; each secretly keeps one and discards the other. Battle goals stay secret until the scenario ends.
5. Players choose which owned items to equip (adding any -1 cards to their modifier decks that equipped items specify), then select a hand of ability cards from their available card pool equal to their class's hand limit.
6. Set all six elements to "Inert" on the element infusion table. Apply the effects of any preceding road or city event.
7. Players place their figures on any empty starting hex shown on the scenario map.

**Scenario level:** 0-7, chosen before starting and unchangeable once begun. Recommended ("Normal") = average party level ÷ 2, rounded up; -1 for Easy, +1 for Hard, +2 for Very Hard. Scenario level sets monster stats, trap damage (a "damage" trap inflicts 2+L, where L is the scenario level), gold conversion, and scenario-completion bonus XP.

**Solo play / open information:** one player running 2+ characters (or a group playing with fully open hand information) should raise the monster level and trap damage by 1 without raising gold conversion or bonus experience.

## Turn Structure

A scenario is a series of rounds, played until the players meet the victory condition or fail. Each round:

### 1. Card Selection
- Each player secretly selects two cards from their hand to play facedown, choosing one as the **leading card** (its initiative number sets their turn order), **or** declares a long rest (only possible with 2+ cards in the discard pile).
- A player with one or no cards in hand must long rest; if they also have one or no cards in their discard pile, they are **exhausted** instead.
- Players may not reveal card names or numeric values to each other, but may discuss plans in general terms.

### 2. Determine Initiative
- Reveal one monster ability card for each monster type with at least one figure on the map; players not long-resting reveal their two cards, leading card on top.
- All figures act from lowest to highest initiative. Long-resting players count as initiative 99.
- Ties: player vs. player — compare non-leading cards (then players decide); player vs. monster — player first; monster vs. monster — players decide.

### 3. Figure Turns (characters and monsters interleaved by initiative)

**Character turn:** perform the top action of one played card and the bottom action of the other, in either order (the leading designation no longer matters). Abilities within an action resolve in the written order and cannot be interrupted by the other card's action; each card goes to its pile (discard, lost, or active area) as soon as its action completes. You may skip any part of an action **except** parts that impose a negative effect on you or your allies. Instead of its printed action, any card may be used as "Attack 2" (top) or "Move 2" (bottom) — used that way, it is always discarded. Items may be used any time on your turn, before, during, or after your two actions.

**Monster turns:** each monster type acts at its ability card's initiative — elites first, then normals, each rank in ascending standee number — following the AI focus/movement rules (see Special Rules).

**Summon turns:** a character's summons act directly before that character each round (see Actions — Summon).

### 4. End of Round
- If a standard "2x" or "Null" modifier card was drawn from a deck this round, shuffle that deck's discards back into it (a modifier deck is also reshuffled any time it runs out mid-draw).
- If a monster ability card drawn this round shows the shuffle symbol, shuffle that monster type's ability discards back into its deck.
- Move element tokens one column left: Strong → Waning, Waning → Inert.
- Move round-bonus cards from active areas to the appropriate discard/lost pile.
- Players who are able may take a short rest.
- Advance the round tracker one space (only needed in scenarios that care about the round number).

## Actions

### Move
"Move X" = move up to X hexes. Figures move through allies but not enemies, obstacles, or walls, and cannot end movement in an occupied hex. Traps and terrain take effect when entered with normal movement. Difficult terrain costs 2 movement points per hex (Jump, Flying, and forced movement ignore it). Hazardous terrain inflicts half of trap damage (rounded down) on entry via normal or forced movement and stays on the board. **Jump** ignores figures and terrain during movement, but the final hex counts as normal movement. **Flying** ignores figures and terrain for the whole move (including forced movement) but must end in an unoccupied hex. Traps are sprung by normal or forced movement (not Jump/Flying), apply their effect, and are removed.

**Revealing a room:** moving onto a closed door tile at any point of a move flips it open and immediately reveals the adjacent room — place its monsters (standee numbers randomized), money tokens, and overlay tiles per the Scenario Book, scaled to the number of characters **including exhausted ones**. Draw an ability card for any newly present monster type that lacks one. When the revealing character's turn ends, any revealed monster type with a lower initiative than that character immediately acts (in initiative order); the rest act at their normal place in the round — so all newly revealed monsters take a turn in the round they are revealed.

### Attack
"Attack X" deals base damage X to an enemy within range. Melee attacks have a default range of 1; ranged attacks list "Range Y." A ranged attack against an adjacent enemy has Disadvantage. Attacks require line-of-sight (a corner-to-corner line touching no wall); only walls block line-of-sight, and range is never counted through walls.

Attack value is modified **in this order**, per target: (1) attacker's bonuses/penalties (active cards, items, +1 for attacking a poisoned figure, etc.); (2) one attack modifier card drawn from the attacker's deck ("Null" = no damage; "2x" = attack value doubled; rolling modifiers chain — keep drawing and add the effects together); (3) the defender's defensive bonuses (e.g., Shield). A monster brought to 0 or fewer HP dies immediately; remaining attack effects don't apply to it, and it drops a money token on its hex unless it was summoned or spawned.

- **Advantage:** draw 2 modifier cards, use the better; **Disadvantage:** draw 2, use the worse (rolling modifiers are disregarded on Disadvantage). If ambiguous which is better/worse, use the first card drawn. Advantage and Disadvantage don't stack, and one of each cancels out.
- **Area attacks:** the diagram may be rotated freely; each target is a separate attack (own modifier card) within one attack action. An area attack that includes the attacker's own (grey) hex is melee. For ranged area attacks only one targeted hex must be in range. The same ability can't hit one enemy twice, and attacks never target allies (ally-helping abilities "affect" instead of "target").
- **Attack effects** (applied after damage, whether or not damage got through; optional except experience): **PUSH X / PULL X** — forced movement away from/toward the attacker, through allies but not enemies, unaffected by difficult terrain; **PIERCE X** — ignore up to X of the target's Shield (exception: applied during damage calculation, not after); **ADD TARGET** — add another target in range, which receives all the attack's effects and conditions.

### Conditions
Only one of each condition type can be on a figure at a time, but conditions can be reapplied to refresh their duration. Negative conditions apply to every target of the ability, after its main effect, even if the attack did no damage. Positive conditions can only be given to yourself or allies and can't be removed early.

| Condition | Effect | Removal |
|-----------|--------|---------|
| POISON | All enemies add +1 Attack against the figure | A Heal on the figure removes POISON — and the Heal then does nothing else (no HP restored) |
| WOUND | 1 damage at the start of each of its turns | A Heal removes WOUND and continues normally (if the figure is also poisoned, the Heal removes both and does nothing else) |
| IMMOBILIZE | Cannot perform move abilities | End of its next turn |
| DISARM | Cannot perform attack abilities | End of its next turn |
| STUN | Cannot perform any abilities or use items, except (characters) long rest; a stunned player still plays two cards or rests, and played cards are simply discarded unused | End of its next turn |
| MUDDLE | Disadvantage on all its attacks | End of its next turn |
| CURSE | Shuffle a CURSE card into the figure's remaining attack modifier deck (max 10 per deck; monster and character curse cards are separate sets) | When drawn, remove it from the deck instead of discarding |
| INVISIBLE | Cannot be focused on or targeted by enemies (monsters treat invisible characters as obstacles); doesn't affect allies' interactions | End of its next turn |
| STRENGTHEN | Advantage on all its attacks | End of its next turn |
| BLESS | Shuffle a BLESS card into the figure's remaining attack modifier deck | When drawn, remove it from the deck instead of discarding |

### Elements
Abilities can infuse one of six elements (Fire, Ice, Air, Earth, Light, Dark): performing any part of the action moves that element to "Strong" **at the end of that figure's turn** — so an element can never be created and consumed on the same turn, but anyone acting later that round may use it. Consuming: if an ability shows a crossed-out element with an augment, and that element is in the Strong **or** Waning column, you may move it to Inert to gain the augment. One icon can't consume two infusions; an augment listing multiple elements needs all of them. At the end of every round all infusions wane one column (Strong → Waning → Inert). Monsters infuse and consume too — they always consume when possible, and every activated monster of the type benefits. A multi-colored circle means any one element (players' choice).

### Active Bonuses, Shield, Retaliate
Cards with a **persistent bonus** symbol stay in the active area, ticking a token per triggering event, and go to the lost pile when all uses are spent (you must use the bonus when it applies, even if it doesn't help; unlimited ones may stay out all scenario). **Round bonus** cards stay active until the end of the round. Active-area cards still count as discarded or lost and may be moved to their pile at any time, ending the bonus.
- **Shield X:** reduces incoming attack value by X; only applies against attacks; multiple shields stack.
- **Retaliate X:** attacker within range (default: adjacent; "Range Y" extends it) suffers X damage per attack made, resolved after the triggering attack. No retaliation if the attack kills or exhausts the retaliator. Stacks; retaliate is not an attack or targeted effect.

### Heal / Summon / Recover / Loot
- **Heal X:** restore X HP to yourself or one ally, labeled either "Range Y" (any ally within Y hexes and line-of-sight, or yourself) or "Self." HP can't exceed the maximum on the character mat. See POISON/WOUND above for the condition interactions.
- **Summon:** place the summon in an empty hex adjacent to the summoner (no empty hex = the summon ability can't be used). The summon card is a persistent bonus in the active area; the summon leaves the board when its HP hit 0, its card leaves the active area, or the summoner is exhausted. A summon **takes its turn directly before its summoner** each round, as a separate turn — but **never in the round it was summoned**. It is not controlled by its owner: it follows automated monster rules with a permanent "Move+0, Attack+0" card, drawing from the owning player's attack modifier deck; multiple summons act in the order summoned. Summon kills are credited to the summon's owner. Summons do not loot at end of turn.
- **Recover / Refresh:** recover returns discarded or lost **ability cards** (as specified) to hand; refresh restores spent or consumed **item cards**. Cards marked with the "cannot recover" symbol can never be recovered/refreshed once lost or consumed.
- **Loot X:** pick up **every** money token and treasure tile within range X (positions of monsters/obstacles don't matter, but line-of-sight is required). Money is personal. Looting a treasure tile: check the treasure index immediately; looting an item you already own sells the copy immediately. **End-of-turn looting:** a character must pick up money/treasure in the hex they occupy at the end of their turn.

### Experience
Only actions showing an XP value grant experience, and only if you use one or more of that action's abilities (never for playing the card alone); some XP is conditional (e.g., on consuming an element). Persistent-bonus cards can grant XP as charges are spent. **Killing monsters gives no automatic XP.**

### Character Damage
When a character suffers damage, the player chooses: lower their HP by that amount, **or** negate the damage by losing one card from hand or two cards from the discard pile (other effects of the attack still apply). The two cards chosen this round can't be lost this way before you act.

### Resting
- **Short rest** (during end-of-round cleanup, needs 2+ discarded cards): shuffle your discard pile, put one random card in your lost pile, return the rest to hand. Once per rest you may instead keep the randomly lost card by suffering 1 damage and randomly losing a different discarded card.
- **Long rest** (declared instead of card selection, needs 2+ discarded cards): your whole turn, at initiative 99. Choose one discarded card to lose, return the rest to hand, perform "Heal 2, Self," and refresh all your spent item cards.

### Items
Items can be used at any time within their card text, even mid-ability, with no per-turn limit — but an item that affects an attack must be used before the modifier card is drawn. **Spent** items turn sideways and refresh on a long rest; **consumed** items flip facedown and only come back via specific refresh abilities during a scenario (all items refresh between scenarios). Equip limits: 1 head, 1 body, 1 legs, two one-hand OR one two-hand, and small items up to half your level rounded up. No duplicates of an item may be owned.

## Scoring / Victory Conditions

**Scenario end:** a scenario ends in success or failure; once the success/failure condition triggers, the remainder of the round is played out, then the scenario ends. Win by meeting the scenario's victory condition (e.g., "Kill all enemies") — losing all characters to exhaustion fails the scenario.

**Exhaustion — two ways:**
1. A character **drops below 1 HP** on the hit point tracker, or
2. At the start of a round they cannot play two cards from hand (one or zero in hand) **and** cannot rest (one or zero in the discard pile). Exhaustion by cards doesn't change current HP.

Either way, all the character's ability cards go to the lost pile, the figure is removed from the map, and they cannot participate in the scenario in any way — there is no coming back that scenario. If all characters are exhausted, the scenario is lost.

**After any scenario (win or lose):** tally each character's XP and convert looted money tokens to gold (the gold per token depends on scenario level — see the rulebook chart; unlooted tokens are worth nothing). Recover all lost/discarded cards, refresh all items, reset HP to maximum, and strip BLESS, CURSE, and scenario/item-added cards from all modifier decks. Battle goals are shuffled back regardless of completion.

**On success only:** each character who met their battle goal earns its checkmarks (three checkmarks = an extra perk, up to six perks this way), and everyone gains bonus XP equal to **4 + 2× scenario level**. An exhausted character still gets battle-goal credit, rewards, and everything collected before exhausting — there is no penalty for having been exhausted. In a campaign, success also unlocks the scenario's conclusion text and listed rewards (achievements, gold/XP "each," prosperity, new scenarios, items or item designs).

**Campaign vs. casual:** campaign-mode scenarios require the listed achievements and can each be completed only once per world in campaign mode; casual mode allows replaying any revealed scenario (XP, money, treasure, battle goals, and personal-quest progress still count, but story rewards are disregarded).

## Special Rules & Edge Cases

- **Monster focus:** each monster, before acting, focuses on the enemy (character or character-summon) it could perform its current attack on with the least movement — shortest path to attack range and line-of-sight (a reachable path matters, not whether it gets there this turn; no attack on its card = treat as melee). Movement ties break by proximity in hexes; then by earliest initiative (a summon is focused before its summoner, even the round it appears; a long-resting character is focused last). If no focus is possible (paths blocked), the monster stays put, skipping move and attack but performing its other abilities.
- **Monster movement:** "Move±X" adjusts its stat-card base move. With no attack after the move, it closes to be adjacent to its focus by the shortest path. With an attack after, it moves the fewest hexes needed for its best attack: adjacent for single-target melee; positioned to hit its focus plus the most other enemies for multi-target; for ranged attacks it moves (even away) until it can shoot its focus without Disadvantage, prioritizing that over secondary targets. Monsters without Flying treat traps and hazardous terrain as obstacles unless crossing them is the only way to any focus — then they cross as few negative hexes as possible.
- **Monster attacks & abilities:** monsters always attack their focus (plus as many others as possible on multi-target attacks; extra attacks pick further focuses normally). Unstated attack range = the stat card's range. Monster heals target self or the ally that has lost the most HP in range. Monster-summoned monsters arrive adjacent to the summoner as close to an enemy as possible, never act the round summoned, and drop no money (the summon fails if no empty hex or standee is available). Monster ability-card bonuses last only until the end of that round. Monsters never loot at end of turn and cannot loot treasure tiles; a monster loot action permanently removes the money tokens it grabs.
- **Ambiguity:** whenever monster AI leaves multiple equally valid options (movement hexes, heal/attack targets, push/pull directions), the players choose.
- **Bosses:** have their own stat cards but act from a universal "Boss" ability deck; they are neither normal nor elite, their stats often scale with character count ("C"), and each lists conditions it is immune to.
- **Special scenario rules:** spawned monsters appear at (or nearest to) their spot — spawned at end of round, they activate next round; spawned mid-round, they activate like revealed monsters. Locked doors act as walls until the scenario's condition opens them. Pressure plates trigger effects when a character occupies one at end of turn. Obstacles with hit points are enemies for ability purposes (initiative 99 for summon focusing, immune to conditions) and are destroyed below 1 HP by damage only. Named monsters are neither normal nor elite.
- **Attack modifier deck maintenance:** drawing a standard "Null" or "2x" flags the deck — at the end of that round shuffle its discards back in; an empty deck reshuffles immediately when a draw is needed. BLESS and CURSE cards are removed from the deck when drawn. Scenario/item-added cards come out at scenario end.
- **Card loss:** actions marked with the loss symbol send the card to the lost pile — recoverable in-scenario only via special recover actions.
- **City & road events:** travel to a new scenario requires resolving a road event unless the scenario is linked, repeated, reached from Gloomhaven with a link, or played casually. Read the front, collectively pick option A or B, then flip and resolve all outcomes whose conditions match (class icon, reputation range, paying collective gold, or "otherwise"), top to bottom. "Collective" rewards/penalties are shared out; "each" applies per character; you can never lose more than you have (and never a perk-costing checkmark, negative money, XP below your level's minimum, or town prosperity below its level minimum). One city event may be completed per visit to Gloomhaven — same mechanics, generally better outcomes.
- **Reputation:** per-party, starts at 0, ranges -20 to +20; gates event outcomes, modifies shop prices (discount when high, surcharge when low), and triggers certain envelope/box unlocks.
- **Town visits:** shop items sell back at half price rounded down (starting supply: items 001–014); no trading between characters. Once per visit each player may donate 10 gold to the Sanctuary to add two BLESS cards to their deck for the next scenario. Leveling up happens only in town: each level adds one card (of that level or lower) to your pool, one perk, and more HP — hand size never changes. New characters may start at any level up to town prosperity, with gold equal to 15×(L+1) and the minimum XP for that level.
- **Personal quests & retirement:** each new character keeps one of two dealt personal quest cards. Fulfilling it forces retirement on the next Gloomhaven visit: materials return to the box, items to the supply, money is lost, the town gains 1 prosperity, new content unlocks (usually a class), and that player's future characters each gain one extra cumulative perk.
- **Enhancements:** once "The Power of Enhancement" is unlocked, gold buys permanent stickers on ability cards (costs scale with card level, prior enhancements, and multi-target abilities); a class's enhanced cards can't exceed the town's prosperity level.
- **Permanent death (variant):** characters die permanently below 1 HP instead of exhausting; card-exhausted characters stay on the map as initiative-99 targets.
- **Reduced randomness (variant):** treat BLESS and standard "2x" as +2, CURSE and standard "Null" as -2 (still reshuffling as usual).

## Player Reference

**Round:** Card selection (2 cards or long rest) → Reveal & sort initiative (low acts first; long rest = 99) → Figure turns → End-of-round cleanup

**Character turn:** top action of one card + bottom action of the other, either order; any card can instead be "Attack 2" (top) / "Move 2" (bottom) and is then discarded

**Initiative ties:** player beats monster; players compare non-leading cards

**Damage to you:** take it, or negate by losing 1 hand card / 2 discarded cards

**Exhausted when:** below 1 HP, **or** can't play 2 cards and can't rest at round start — figure removed for the rest of the scenario

**Rests (need 2+ discarded cards; always lose 1):**
- Short: end of round, random loss (may suffer 1 damage once to re-roll)
- Long: initiative 99, choose the loss, Heal 2 Self, refresh spent items

**Summons:** act right before their summoner, never on the round summoned

**Heal vs. conditions:** removes POISON — then heals nothing else; removes WOUND and heals normally

**Elements:** infuse at end of turn → Strong; consume from Strong or Waning; all wane one step at end of round

**Modifier decks:** reshuffle discards at end of any round in which a Null/2x was drawn (or immediately when empty); BLESS/CURSE leave the deck when drawn
