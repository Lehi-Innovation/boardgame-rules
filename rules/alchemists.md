---
title: "Alchemists"
bgg_id: 161970
player_count: "2-4"
play_time: "120 min"
designer: "Matus Kotry"
source_pdf: "alchemists-rules.pdf"
extracted_date: "2026-03-18"
summarized_date: "2026-03-18"
verification: "minor_issues"
verification_date: "2026-06-13"
---
<!-- verification:begin -->
> ✅ **Verified (minor gaps)** — fact-checked against the rulebook text; only small omissions were found, nothing that changes how the game is played or scored.
>
> 📄 [Full rulebook text](https://jonnyallred.github.io/boardgame-rules/extracted/alchemists-rules.txt) · 🚩 [Report a rules error](https://github.com/Lehi-Innovation/boardgame-rules/issues/new?template=rule-error.yml&labels=rule-error&title=%5BRule%20error%5D%20Alchemists&game=alchemists)
<!-- verification:end -->


## Overview

Alchemists is a deduction and worker-placement game where players are alchemists discovering the magical properties of 8 ingredients. Using an app to scan ingredient cards, players experiment to learn which alchemicals correspond to which ingredients, then publish theories. Points are earned through published theories (especially correct ones), artifacts, grants, and reputation. The player with the most points wins.

## Components

- Double-sided game board, theory board, exhibition board
- 4 Laboratory screens, 4 Results triangles, 4 Player boards
- 6 Adventurer tiles, 2 Conference tiles, 5 Grant tiles
- 8 Alchemical tokens, 104 Result tokens
- 36 Gold piece tokens, 44 Seal of approval tokens (11 per color)
- 6 Conflict tokens, Starting player token
- 8 Ingredient tiles, Gamemaster board
- 40 Ingredient cards, 22 Favor cards, 18 Artifact cards, 16 Bid cards
- 8 Plastic beaker figures, 24 Plastic cubes
- Pad of deduction grids, Token containers

## Setup

1. Place the game board: use one side for a 4-player game and the other side for a 2- or 3-player game.
2. Shuffle and place ingredient cards, artifact cards, and adventurer tiles.
3. Each player takes a screen, player board, results triangle, deduction grid, cubes, and beakers.
4. Launch the app on a shared device and enter the game code.

## Turn Structure

The game is played over 6 rounds. Each round has:

1. **Choose Turn Order:** Beginning with the starting player and proceeding clockwise, each player openly places their order marker on an unoccupied order space. Lower spaces grant more cards but give a disadvantage when resolving actions.
2. **Declare Actions:** In turn order (lowest order space first), each player places all their cubes on action spaces at once.
3. **Resolve Actions:** Actions resolve in a fixed clockwise order around the board.

## Actions

### Forage for Ingredients

Take 1 face-up ingredient from the row or draw 1 random ingredient from the deck.

### Transmute an Ingredient

Discard 1 ingredient card to gain 1 gold.

### Buy an Artifact

Pay gold to acquire an artifact card with powerful abilities.

### Test on a Student / Drink a Potion

Both actions involve mixing 2 ingredient cards using the app. The full potion result is revealed to all players, recorded on the results triangle and player board, and the ingredients are discarded face-down. The key differences concern negative potions:

- **Test on Student:** No reputation is lost by the experimenting player. However, after any player mixes a negative potion, all subsequent players who wish to use that action space that round must pay 1 gold piece to the student.
- **Drink Potion:** No gold payment is ever required, but negative potions affect the drinking player directly: insanity costs 1 reputation, paralysis moves your order marker to the paralysis space (playing last next round), and poison sends one of your cubes to the hospital (1 fewer cube next round).

### Sell a Potion

An adventurer requests specific potions. Before selling, if multiple players declared this action, all bid simultaneously using bid cards (values 0, −1, −2, −3) to determine selling order; more smiley faces go first, with normal play order as a tiebreaker. Each seller chooses one of the available potions and places a guarantee (exact match for 4 gold, correct sign for 3 gold, neutral or better for 2 gold, or anything for 1 gold), then mixes 2 ingredients using the app. If the result meets the guarantee, take that payment from the bank; if not, no payment is made. There is no refund mechanic. Only mixing a potion of the wrong sign causes a reputation loss of 1 point; no reputation is gained for a successful sale.

### Publish a Theory

Claim which alchemical corresponds to an ingredient. Pay 1 gold to the bank, place one of your seals face-down on the theory, and place the alchemical token on the theory board. Gain 1 reputation immediately. Seals are secret bets: gold-starred and silver-starred seals score points at the end of the game for correct theories but cost points for wrong ones; unstarred (color-hedged) seals provide protection against being penalized if a specific aspect is disproven.

You may also endorse an existing theory by adding your seal and paying 1 gold to the bank plus 1 gold to each player who already has a seal on that theory.

### Debunk a Theory

Demonstrate that a published theory is incorrect using the app. If successful, gain 2 reputation; players with seals on the debunked theory risk losing reputation or points depending on their seal type. If the attempt fails, lose 1 reputation for wasting colleagues' time.

### Present at the Exhibition

In the final round only, demonstrate potions on the exhibition board for reputation gains.

## Scoring / Victory Conditions

After 6 rounds, final scoring proceeds as follows:

1. **Convert Reputation to Points:** All reputation points become victory points.
2. **Artifacts:** Score victory points for each artifact.
3. **Grants:** Score victory points for each grant tile held.
4. **Gold:** Exchange remaining favor cards for 2 gold each, then convert gold at a fixed rate of 3 gold = 1 VP for all player counts. Leftover gold serves as a tiebreaker.
5. **The Big Revelation:** The app reveals the true alchemical for each ingredient. Go through each theory and reveal all seals. For correct theories: gold-starred seals score 5 VP, silver-starred seals score 3 VP, and unstarred seals score 0 VP. For incorrect theories: starred seals and improperly hedged unstarred seals each cost −4 VP; a properly hedged unstarred seal costs 0 VP.

Highest total VP wins; ties broken by leftover gold.

## Special Rules & Edge Cases

- **Alchemical System:** Each ingredient maps to 1 of 8 alchemicals (each with red/green/blue aspects, each positive or negative). When two are mixed, matching aspects produce a potion type.
- **App:** Scans ingredient cards and reveals the resulting potion. Mapping is randomized each game.
- **No-App Mode:** One player acts as gamemaster using a hidden reference sheet.
- **Favor Cards:** Drawn based on which order space is chosen (some spaces grant favor cards as part of their reward) and also earned at the end of each round for every pair of unused cubes. Provide small one-time bonuses.
- **Conferences:** Occur at the end of rounds 3 and 5. Players who have the required number of seals on the theory board gain 1 reputation; those who do not lose reputation as indicated on the conference tile.
- **Board Sides:** One side of the game board is used for 4-player games; the other side is used for 2- or 3-player games.

## Player Reference

**Round Flow:** Choose order spaces openly → Place action cubes → Resolve actions in order

**Key Actions:** Forage, Transmute, Buy Artifact, Test/Drink, Sell Potion, Publish Theory, Debunk

**Deduction:** 8 ingredients map to 8 alchemicals. Mix pairs to narrow down possibilities.

**VP Sources:** Reputation + Seals on correct theories + Artifacts + Grants + Gold