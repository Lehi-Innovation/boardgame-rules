---
title: "Black Friday"
bgg_id: 39242
player_count: "2-5"
play_time: "45-60 min"
designer: "Friedemann Friese"
source_pdf: "black-friday-rules.pdf"
extracted_date: "2026-03-18"
summarized_date: "2026-03-18"
verification: "minor_issues"
verification_date: "2026-07-03"
---
<!-- verification:begin -->
> ✅ **Verified (minor gaps)** — fact-checked against the rulebook text; only small omissions were found, nothing that changes how the game is played or scored.
>
> 📄 [Full rulebook text](https://jonnyallred.github.io/boardgame-rules/extracted/black-friday-rules.txt) · 🚩 [Report a rules error](https://github.com/Lehi-Innovation/boardgame-rules/issues/new?template=rule-error.yml&labels=rule-error&title=%5BRule%20error%5D%20Black%20Friday&game=black-friday)
<!-- verification:end -->


## Overview

Black Friday is a stock market game where players are speculators trying to accumulate the greatest total wealth before the gold price hits $100. Players buy and sell shares in five colored companies, manipulate share prices, and spend cash to purchase gold bars. The game features the M.I.B.S. (Minimally Intelligent Broker Service) as an automated opponent. At game end, all remaining shares are sold and the player with the highest total wealth in cash and gold wins.

## Components

- 1 double-sided game board (2-4 players / 5 players)
- 140 shares (25 each in purple, yellow, green, blue, white; 15 black)
- 5 share price tokens
- 2 gold tokens (gold price track + purchased gold bars track)
- 20 big gold bars (value 5) and 20 small gold bars (value 1)
- 5 screens
- 5 double-sided level tiles
- 1 cloth bag
- 4 bonus tiles
- Money tokens (30x $1, 15x $5, 20x $10, 15x $50, 10x $100, 10x $200)

## Setup

1. Place the game board matching your player count (2-4 side or 5 side).
2. Place share price tokens on the 8th space of the share price table.
3. Place gold tokens on space "20" of the gold price track and space "0" of the purchased gold bars track.
4. Fill the bag with shares (remove 1 of each color for 2-4 players).
5. Place shares on the share market: 4 per space (2-4 players) or 5 per space (5 players).
6. Randomly draw 20 shares from the bag and add to the share market.
7. Adjust share prices: most scarce color moves to space 10, most common moves to space 6.
8. Place 2 shares of each color and 6 black shares on the "share sale" tracks.
9. Place 9 black shares on the share price table.
10. Each player draws 5 shares from the bag (hidden behind screen) and takes $100.
11. Determine starting player; distribute bonus tiles to non-starting players.
12. **M.I.B.S.:** Required with 2 players (plays as 3rd player); optional with 3-4 players.

## Turn Structure

Players take turns in clockwise order. On your turn, you must perform **exactly one** of the following actions:

1. **Buy shares** from the share market
2. **Sell shares** to the share sale track
3. **Buy gold**

In addition to your action, you may use your **bonus tile** (once per game). A price change is triggered mid-turn when the relevant track is filled; the price change resolves immediately, then the turn continues.

## Actions

### Level Tiles
The current level tile determines three limits that apply to every turn:
- **Share purchase/sale limit:** the maximum number of shares you may buy or sell in one action (starts at 1, rises to 5).
- **Gold purchase limit:** the maximum number of gold bars you may buy in one action (starts at 1, rises to 5).
- **Price-change draw count:** how many shares are drawn from the bag when a price change is triggered (starts at 5, rises to 12).

Levels increase only during a price change (never when a share price token moves into a new area during a regular action).

### Buy Shares
- Buy up to the current **purchase/sale limit** (at most 5) shares of one color from the share market.
- Pay the current price per share.
- Place purchased shares behind your screen.
- For each share bought, also place 1 share of the same color from the share market on the **share purchase track** (only 1 share total goes on the track per action, regardless of how many you buy).
- If the last share of a color is taken from the market, move its price token 1 space to the right.
- When a third share of a color is placed on the share purchase track, move its price token 1 space to the right (additional shares of that color do not further raise the price).
- **Price change trigger:** when all 5 (or 6 for 5-player) spaces of the share purchase track are filled with colored shares.

### Sell Shares
- Sell up to the current **purchase/sale limit** (at most 5) shares of one color from behind your screen.
- Place them on the share market and receive cash equal to the current price per share.
- Remove 1 share of the same color from the current share sale track and place it in the share market (only 1 share removed from the track per action). If no share of that color is on the track, remove a share of any color.
- The price token of the removed color drops 1 space to the left immediately.
- **Price change trigger:** when only 5 colored shares remain on the current share sale track (4 for 5-player).
- After the price change triggered by the second share sale track, switch to the third track. After the third track triggers a price change, refill the center track with 2 shares of each color from the market plus 2 black shares.

### Buy Gold
- Buy up to the current **gold purchase limit** (at most 5) gold bars at the current gold price.
- Pay the current gold price per bar; move the purchased-gold-bars token 1 space right per bar bought.
- Place 1 colored share of your choice from the share market on the **gold purchase track** (only 1 share per action).
- Every 5 small gold bars you accumulate are exchanged for 1 big gold bar.
- **Price change trigger:** when all 5 (or 6 for 5-player) spaces of the gold purchase track are filled with colored shares.

### Price Change
Triggered when a track (share purchase, gold purchase, or share sale) reaches its threshold. Steps:
1. Draw the number of shares from the bag specified by the current level tile.
2. **Adjust the gold price:** move the gold token up 1 space for each black share drawn, plus 1 space for every 3 gold bars marked on the purchased-gold-bars track (then reset that track to 0).
3. **Adjust share prices** using the overview on the board: if 0 black shares drawn, move each color's price token based on how many of that color were drawn; if exactly 1 black share drawn, return it to the bag and proceed as if 0 black; if 2+ black shares drawn, subtract that number from each color's count when moving tokens.
4. Place drawn colored shares on the share market; put all shares from the triggering track (plus adjacent black shares if it was a share sale track) into the bag.
5. If a color is still absent from the market after placing, raise its price token 1 space up.
6. **Check for level change:** if the most expensive color's price token has entered a new area of the price table, activate that level. Put the black share from each newly entered area into the bag. Levels never decrease.

## Scoring / Victory Conditions

- The game ends after any price adjustment in which the gold token reaches the **100 space** on the gold price track. Any further price increases are ignored.
- All players then **sell all remaining shares** at current prices (no price adjustments for these sales).
- Each player calculates their **total wealth** in dollars: cash + (each small gold bar × $100) + (each big gold bar × $500).
- The player with the **highest total wealth** wins.
- **Tiebreaker:** the player with the most wealth held in gold bars wins.

## Special Rules & Edge Cases

### M.I.B.S. (Automated Opponent)
- Required for 2 players (plays as a 3rd player, so follow 3-player rules); optional for 3-4 players (adds 1 player, so follow the next player-count rules); not used with 5 players.
- The M.I.B.S. always starts the game as the first player.
- Its assets (cash and shares) are always visible to all players.
- **Action priority:**
  1. **Buy shares or buy gold** — chosen as long as it has enough cash to buy the maximum allowed by the current limit. It always buys the cheaper offer (shares vs. gold bars). When buying shares it buys the cheapest color first.
  2. **Sell shares** — chosen when it cannot afford the maximum buy limit, as long as it still has shares available to sell; sells the most expensive color(s) first.
  3. **Partial buy** — if it has sold all its shares and still cannot afford the maximum, it buys as much as possible of the cheapest offer (shares or gold) with its remaining cash.
  4. **Market manipulation** — if there is not enough cash to buy anything at all (not even a partial amount), it places 1 share from the market on the gold purchase track (cheapest color first).
- The M.I.B.S. sells all remaining shares at game end.

### Black Shares
- Black shares have no share price and cannot be bought or sold normally.
- When drawn from the bag during a price change, each black share raises the gold price by 1 space.
- 9 black shares are pre-placed on the share price table in the areas that mark level thresholds; when the most expensive color's price token enters a new area during a price change, the black share from that area goes into the bag.
- 6 black shares are pre-placed next to the share sale tracks; when a share sale track triggers a price change, those adjacent black shares go into the bag.

### Level Tiles
- Double-sided tiles mark 10 share price levels and are stacked on the board.
- Levels only increase (never decrease); higher levels allow buying/selling more shares/gold and cause more shares to be drawn during price changes.
- A new level activates during a price change when the most expensive share's price token enters a new area of the price table (the black share from that area enters the bag).

### Bonus Tiles
- Non-starting players receive numbered bonus tiles (player 2 gets tile "2.", player 3 gets tile "3.", etc.) that provide cumulative one-time advantages used in addition to a regular action:
  - Tile 2: place/remove 1 share on a track (market manipulation without spending your action).
  - Tile 3: all of tile 2's advantages, plus sell 1 extra share beyond the current sale limit.
  - Tile 4: all of tile 3's advantages, plus buy 1 extra gold bar beyond the current purchase limit.
  - Tile 5: all of tile 4's advantages, plus buy 1 extra share beyond the current purchase limit.
- After using the bonus tile, place it in the box. It can trigger a price change.

## Player Reference

| Action | Limit | Track Effect |
|--------|-------|--------------|
| Buy Shares | Up to current level limit (max 5) of one color | Place 1 share on share purchase track; price change when track full |
| Sell Shares | Up to current level limit (max 5) of one color | Remove 1 share from share sale track; price change when ≤5 colored shares remain |
| Buy Gold | Up to current level limit (max 5) gold bars | Place 1 share on gold purchase track; move purchased-gold-bars token 1 right per bar; price change when track full |

| Gold Bar Values | Dollar Value at Game End |
|----------------|--------------------------|
| Small bar | $100 |
| Big bar | $500 |

| Game End Trigger | Gold token reaches space 100 on the gold price track |
|-----------------|------------------------------------------------------|
| Final step | All players sell remaining shares at current prices (no price adjustment) |
| Winner | Highest total wealth (cash + gold bars in dollars) |
| Tiebreaker | Most wealth held in gold bars |
