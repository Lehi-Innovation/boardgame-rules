# Rules correction evidence

Audit date: 2026-11-04. Targeted corrections in 21 games were checked against local rulebook extractions. All repaired games remain flagged pending independent re-audit. These findings do not constitute a full-game PASS verdict.

Each section shows the final rules diff against the starting revision, followed by the source passages supporting those changes. Verification banners are omitted from the diffs. Original audit reasons remain in `semantic-audit-results.yaml` under `previous_reason`.

## a-feast-for-odin

[A Feast for Odin](../../../rules/a-feast-for-odin.md): ore placement restrictions.

### Corrected rules

```diff
--- Original summary
+++ Corrected summary
@@ -71,9 +71,9 @@
 | **Emigration** | Use longships or knarrs to emigrate (flip for points) |
 
 ### Goods Tile Placement
-- Green (craft) and blue (luxury) goods can be placed on home board, exploration boards, houses.
+- Green (craft) and blue (luxury) goods can be placed on the home board, exploration boards, stone houses, and long houses. Sheds instead take wood and stone.
 - Orange (food) and red (animal products) can go in stone houses and long houses; orange and red food tiles are also placed on the Banquet Table during the Feast phase.
-- Ore and silver can fill gaps in placement areas. **Ore cannot be placed on the Banquet Table; silver coins can.**
+- Ore and silver can fill gaps on the home board and exploration boards. **Ore cannot be placed in stone houses, long houses, or on the Banquet Table.** Stone and long houses accept silver; sheds require wood and stone.
 - Once placed, tiles cannot be removed.
 - Tiles must fit within the placement area; no overlapping.
 
@@ -128,11 +128,11 @@
 
 | Goods Colors | Placement |
 |---|---|
-| Green (craft) | Home board, exploration boards, houses |
-| Blue (luxury) | Home board, exploration boards, houses |
+| Green (craft) | Home board, exploration boards, stone houses, long houses |
+| Blue (luxury) | Home board, exploration boards, stone houses, long houses |
 | Orange (food) | Stone houses, long houses, and Banquet Table (feast) |
 | Red (animal products) | Stone houses, long houses, and Banquet Table (feast) |
-| Ore | Any placement area (ore cannot go on Banquet Table) |
+| Ore | Home board and exploration boards; also upgrades whaling boats and longships. Not in houses or on the Banquet Table. |
 | Silver | Any placement area and Banquet Table (silver on boards is worthless at scoring) |
 
 | Ship Types | |
```

### Rulebook evidence

Source: [extracted/a-feast-for-odin-rules.txt, lines 371–381](../../../extracted/a-feast-for-odin-rules.txt#L371).

```text
Your home board and the exploration boards have spaces that you 
must cover with goods tiles to avoid negative points. 
“Fur” can be effectively worth 
8 points if you use it to cover 
eight spaces with negative points. 
The sheds, stone houses, and long houses also have spaces with 
negative points, which you should cover with goods tiles.
• Sheds require wood and stone.
• The stone and long houses are special in that they allow you to 
place orange and red food tiles in them as well as the usual 
green and blue goods and silver coins, but not ore.
```

Source: [extracted/a-feast-for-odin-rules.txt, lines 735–753](../../../extracted/a-feast-for-odin-rules.txt#L735).

```text

Placing Goods on the Exploration Boards
As with the home board: at any time, you may place green craft 
products and blue luxury goods as well as silver coins and ore 
tokens on empty spaces of the exploration boards, according to 
the same rules. 
A lot of goods spaces on the exploration boards are surrounded 
by less than 8 other spaces, which makes it easier to enclose them 
for the bonus.
To unlock the rune stone and ore bonus on Bear Island, you only 
need to cover six spaces.
Placing Goods on the House Tiles 
At any time, you may place orange farm goods, red animal 
products, green craft products, and blue luxury goods as well as 
silver coins on empty spaces of your houses. 
Orange tiles cannot be orthogonally adjacent to other orange tiles, 
and red tiles cannot be orthogonally adjacent to other red tiles 
(diagonal adjacency is allowed, as shown in the illustration on 
the house tiles). 
```

Review status: pending independent audit.

## caverna-the-cave-farmers

[Caverna: The Cave Farmers](../../../rules/caverna-the-cave-farmers.md): grain scoring rounding.

### Corrected rules

```diff
--- Original summary
+++ Corrected summary
@@ -86,7 +86,7 @@
 | Category | Points |
 |----------|--------|
 | Animals (each, including Dogs) | 1 Gold per animal |
-| Grain (each) | 0.5 Gold |
+| Grain (total in supply and on Fields) | Divide the total by 2 and round up to whole Gold points |
 | Vegetables (each) | 1 Gold |
 | Rubies (each) | 1 Gold |
 | Gold coins | Face value |
```

### Rulebook evidence

Source: [extracted/caverna-the-cave-farmers-rules.txt, lines 1310–1312](../../../extracted/caverna-the-cave-farmers-rules.txt#L1310).

```text
	 ½ Gold per Grain (rounded up): Count all of your Grain tokens – both those in your 
supply and those still left on Fields. Divide this number by 2 and round it up. This is the 
number of Gold points you get for Grain.
```

Review status: pending independent audit.

## dragonwood

[Dragonwood](../../../rules/dragonwood.md): failed-capture card returns.

### Corrected rules

```diff
--- Original summary
+++ Corrected summary
@@ -55,9 +55,9 @@
 4. Compare dice total (+ Enhancement bonuses) to the target value for that method on the card.
 5. If your total equals or exceeds the value, you capture the card.
 
-**Creatures:** Captured Creatures go face down in your victory pile. If you fail, the Creature stays in the Landscape and you discard 1 card from your hand as a wound. Either way, all played Adventurer cards go to the discard pile.
+**Creatures:** Captured Creatures go face down in your victory pile, and the Adventurer cards used are discarded. If you fail, the Creature stays in the Landscape: discard 1 Adventurer card as a wound and return the rest of the played Adventurer cards to your hand.
 
-**Enhancements:** Captured Enhancements go face up in front of you for ongoing use (unless the card specifies single use). On failure, discard 1 card as a wound. Enhancements **cannot** be used to capture other Enhancements.
+**Enhancements:** Captured Enhancements go face up in front of you for ongoing use (unless the card specifies single use). On failure, discard 1 card as a wound and return the other played Adventurer cards to your hand. Enhancements **cannot** be used to capture other Enhancements.
 
 **Events:** When an Event card enters the Landscape, read it immediately, apply its effect to all players, then remove it from the game and draw a replacement.
 
```

### Rulebook evidence

Source: [extracted/dragonwood-rules.txt, lines 103–108](../../../extracted/dragonwood-rules.txt#L103).

```text
If you defeat a Creature, take the card from the landscape and place it face 
down in a “victory” pile next to you. Place all the Adventurer cards you used 
in the discard pile. 
However, if your roll doesn’t beat the Creature, it remains in the Landscape. 
As a penalty, you must discard 1 card from your hand as a “wound” for not 
defeating it. (Take the rest of the Adventurer cards back into your hand.)
```

Source: [extracted/dragonwood-rules.txt, lines 109–122](../../../extracted/dragonwood-rules.txt#L109).

```text
ENHANCEMENTS
If you capture an Enhancement, take the card and place it face up in front of 
you. This card can then be used throughout the rest of the game (or only once, 
if specified on the card). 
Place all the Adventurer cards you used in the discard pile. Like with Creatures, 
if your roll does not match or beat the total on the Enhancement card, you must 
discard 1 card from your hand.
Capturing Notes:
 Enhancements may not be used to capture other Enhancements.
 You may always use a single card, which earns you 1 die. 
 (In this case you may count it as either a Strike, Stomp or Scream.)
 You may only try to capture 1 Creature or Enhancement per turn.
 You may roll a maximum of 6 dice at any time. 
REPLENISHING THE LANDSCAPE
```

Review status: pending independent audit.

## egizia

[Egizia](../../../rules/egizia.md): Joker crews, stone conversion, and unsupported final scoring.

### Corrected rules

```diff
--- Original summary
+++ Corrected summary
@@ -115,10 +115,9 @@
 - Co-operation bonus (1/3/6 points for 1/2/3 building sites used).
 
 ### Final Scoring
-1. **Stone market conversion:** If a player's marker is on one of the bottom two spaces, they may sell remaining stones for 1 point per stone (up to 10, rounded down).
-2. **Grave tiles:** Sum the values and score per table (1-10 = 2 points, 11-20 = 5 points, 21+ = 9 points).
+1. **Stone market conversion:** If a player's marker is on one of the bottom two spaces, they may sell remaining stones for 1 point per 2 stones, rounding the points down.
+2. **Grave tiles:** Sum their values and use the printed final-scoring table in the rulebook; the extracted text omits its point values.
 3. **Sphinx cards:** Check each sphinx card for fulfilled conditions and score accordingly. Categories include: building conditions ("X is built"), having stones in certain buildings, reaching last levels, having productive quarries/fields, and construction crew conditions.
-4. **Scarab bonus:** For each 10 points already scored (on the scoring table), gain an additional point.
 
 The player with the most points wins. Tiebreaker: the player whose stone is in front on the scoring track.
 
@@ -126,7 +125,7 @@
 
 - A player can use each construction crew in each round only once. After use, turn it over; it returns at the beginning of the next round.
 - Construction crews are used but not consumed.
-- The Joker construction crew can only be used alone, never with another crew.
+- The Joker construction crew can never be used alone; it may be combined with another crew once per round.
 - If a player does not build, they take their ship back from the building site.
 - A player building on speculation (no ship at site) can do so if another player with a ship chose not to build.
 - The water ring must always stay on one of the 3 round fields on the board.
```

### Rulebook evidence

Source: [extracted/egizia-rules.txt, lines 755–756](../../../extracted/egizia-rules.txt#L755).

```text
1. If the player‘s marker is on one of the bottom two spaces of the stone market, he may sell his remaining stones. For 
each 2 stones he sells, he scores 1 point (rounded down).
```

Source: [extracted/egizia-rules.txt, lines 611–615](../../../extracted/egizia-rules.txt#L611).

```text
s The player can use each construction crew in each round only once.
s After using a construction crew he turns over the tile and turns it back at the beginning of the next round (thus, 
Construction crews are used, but not consumed). 
s The player can never use the Joker construction crew alone. He can use it once per round with another construction 
crew and then must, likewise, turn it over.
```

Source: [extracted/egizia-rules.txt, lines 757–767](../../../extracted/egizia-rules.txt#L757).

```text
2. The player sums the values of his grave tiles and scores points according to the following table:
 
 
value of the grave tiles 
points
 
1-10 
 
11-20 
 
21 or more 
```

Source: [extracted/egizia-rules.txt, lines 752–771](../../../extracted/egizia-rules.txt#L752).

```text
Player 
 begins and executes the following 3 steps. Then player 
 does the same, and so on.
1. If the player‘s marker is on one of the bottom two spaces of the stone market, he may sell his remaining stones. For 
each 2 stones he sells, he scores 1 point (rounded down).
2. The player sums the values of his grave tiles and scores points according to the following table:
 
 
value of the grave tiles 
points
 
1-10 
 
11-20 
 
21 or more 
3. The player checks his sphinx cards to see which have conditions he has fulﬁ lled and scores those points accordingly. For 
complete descriptions of the sphinx cards, see page 11.
The player with the most points is the winner. If players are tied, the player whose stone is in front on that space of the 
scoring track is the winner.
```

Review status: pending independent audit.

## el-grande

[El Grande](../../../rules/el-grande.md): Grande movement and Home Bonus.

### Corrected rules

```diff
--- Original summary
+++ Corrected summary
@@ -75,6 +75,8 @@
 
 Ties: Tied players each receive the points for the lower position and the higher position is eliminated.
 
+**Home Bonus:** When a region is scored, its sole Caballero-majority holder gains +2 points if their Grande is in that region. No Home Bonus is awarded for a tied majority.
+
 ### Game End
 After 9 rounds (or 6 for shorter game: skip rounds 1, 4, 7). Player with the most points wins.
 
@@ -83,7 +85,7 @@
 - Power cards are permanently discarded after use (can only be recovered via certain action cards).
 - All power card values played in a round must be unique.
 - If provinces run out, a player may remove their own Caballeros from the board to their court.
-- The Grande always remains in its home region and counts for scoring there.
+- In the standard game, a Grande marks the region eligible for its owner’s +2 Home Bonus and does not count as a Caballero. Certain action cards can move it, subject to the King’s Region restriction. Counting the Grande as 1 Caballero is an optional Home Region Advantages variant.
 - Action cards include various special effects: move the King, rearrange Caballeros, score specific regions, retrieve power cards, etc.
 - The King card (5-pile) is turned face up every round and never permanently discarded.
 - Shorter game (6 rounds): Skip rounds 1, 4, and 7; play only rounds 2-3, 5-6, 8-9 with scoring after 3 and 6.
```

### Rulebook evidence

Source: [extracted/el-grande-rules.txt, lines 180–182](../../../extracted/el-grande-rules.txt#L180).

```text
Home Bonuses 
If a player has the most Caballeros in the region where their Grande stands when that region is scored, they 
receive an additional two points. They do not receive the bonus if they are tied for first in this region. 
```

Source: [extracted/el-grande-rules.txt, lines 464–471](../../../extracted/el-grande-rules.txt#L464).

```text
Grande. (two cards) 
You may move your Grande 
into a different region, unless it 
is in the King’s region, in which 
case it cannot move. You may 
choose any region except the 
Castillo and the King's region. You may choose a 
region which already contains several Grandes. 
```

Source: [extracted/el-grande-rules.txt, lines 506–512](../../../extracted/el-grande-rules.txt#L506).

```text
Variant Rules 
The following variant rules may be used in any combination. 
Short Game 
For an alternate version of the shorter game play rounds 1–6, skipping rounds 7–9 and the final scoring. 
Home Region Advantages 
The Grande piece counts as 1 for determining who has the most in a region. 
If all of the Caballeros that you add to the board by non-special action go into the Home region then you may 
```

Review status: pending independent audit.

## five-tribes-the-djinns-of-naqala

[Five Tribes: The Djinns of Naqala](../../../rules/five-tribes-the-djinns-of-naqala.md): market actions, Djinn costs, Fakirs, sales, and game end.

### Corrected rules

```diff
--- Original summary
+++ Corrected summary
@@ -60,7 +60,7 @@
 
 **2.5 Tile Actions** -- Perform the action of the tile where you ended your move.
 
-**2.6 Merchandise Sale (if applicable)** -- Fill the Resource card display back to 9 cards.
+**2.6 Merchandise Sale (optional)** -- Sell one or more sets of distinct Merchandise cards for Gold Coins using the set-value table. Fakirs cannot be sold. Then clean up by refilling the Resource display to 9 and the Djinn display to 3.
 
 ## Actions
 
@@ -72,17 +72,17 @@
 | **Elders** | White | Keep them. Score 2 VP each at game end. May spend to invoke Djinns. |
 | **Merchants** | Green | Return to bag. Take an equal number of Resource cards from the display (left to right). |
 | **Builders** | Blue | Return to bag. Score Gold Coins equal to number of blue Builders collected x number of blue-valued tiles surrounding (and including) the final tile. |
-| **Assassins** | Red | Return to bag. Kill (remove from the game) 1 meeple on the final tile or a tile within range (# of Assassins collected). May kill another player's Vizier/Elder (returns to their supply). If killing empties a tile, place your Camel there. |
+| **Assassins** | Red | Return to bag. Kill 1 meeple within range (number of Assassins collected, orthogonal distance), returning it to the bag; alternatively, kill 1 Vizier or Elder held by an opponent, also returning it to the bag. If killing empties a tile, place your Camel there. |
 
 ### Tile Actions
 
 | Tile | Action |
 |------|--------|
-| **Small Market** (compulsory) | Draw top 3 Resource cards; keep 1, discard others face-up. |
-| **Large Market** (compulsory) | Draw top 6 Resource cards; keep 2, discard others face-up. |
+| **Small Market** (optional) | Pay 3 Gold Coins to choose 1 of the first 3 visible Resource cards. |
+| **Large Market** (optional) | Pay 6 Gold Coins to choose 2 of the first 6 visible Resource cards; if only 1 remains, the cost is still 6. |
 | **Oasis** | Place 1 Palm Tree on this tile (adds 3 VP for tile owner at end). |
 | **Village** | Place 1 Palace on this tile (adds 5 VP for tile owner at end). |
-| **Sacred Place** | Pay 1 or 2 Elders (or Fakirs as wild) to take 1 face-up Djinn or draw 2 to pick 1. |
+| **Sacred Place** (optional) | Pay 2 Elders OR 1 Elder + 1 Fakir to take 1 visible Djinn. Return Elders to the bag and discard the Fakir. |
 
 ### Djinns
 
@@ -90,9 +90,7 @@
 
 ## Scoring / Victory Conditions
 
-The game ends when:
-- A player places their last Camel, OR
-- No legal meeple move exists for any player.
+The game ends at the end of the turn in which a player places their last Camel or no legal meeple move remains. Finish all players’ remaining actions in that turn before scoring; players unable to move may still use applicable Djinn powers.
 
 Players sum their Victory Points:
 
@@ -113,16 +111,16 @@
 |----------|---|---|---|---|---|---|---|---|---|
 | VP | 1 | 3 | 7 | 13 | 21 | 30 | 40 | 50 | 60 |
 
-Fakirs are wild: each Fakir may substitute for any 1 Merchandise in a set.
+Fakirs are not Merchandise and do not score in Merchandise sets. They can enhance Builders and Assassins or be combined with an Elder to acquire a Djinn.
 
-The player with the highest total VP wins. Ties broken by most Gold Coins remaining.
+The player with the highest total VP wins. Tied players share victory.
 
 ## Special Rules & Edge Cases
 
 - **2-Player Game**: Each player uses 2 Turn markers and 11 Camels. Both markers are bid separately, meaning a player can play twice per turn or even back-to-back.
 - **Assassins and Tile Control**: It is possible to control 2 tiles in 1 turn: the tile where you end your move (if emptied) and a tile emptied by Assassin kills. You must take the first tile; the second requires having Camels left.
 - **Resource Display**: After Merchants collect cards, gaps are NOT refilled until that player's Clean-Up step. The next Merchant action in the same turn may have fewer choices.
-- **Fakirs**: Count as wild for Merchandise sets and for paying for Djinns (substitute for Elders).
+- **Fakirs**: Do not score in Merchandise sets. Discard to enhance Builders or Assassin range, or pay 1 Elder + 1 Fakir for a visible Djinn.
 - **Tile Control**: Once a Camel is placed, that tile's ownership never changes, even if new meeples are dropped on it.
 - **Last Meeple Rule**: You can pass through empty tiles (dropping meeples), but you can NEVER end on an empty tile.
 - **Loops**: Require at least 5 meeples to complete. No immediate backtracking, but returning to a tile after an intervening tile is allowed.
```

### Rulebook evidence

Source: [extracted/five-tribes-the-djinns-of-naqala-rules.txt, lines 350–352](../../../extracted/five-tribes-the-djinns-of-naqala-rules.txt#L350).

```text
For all other symbols, the Tile’s Action is NOT compulsory: You
can take this action if you wish, provided you are able, and willing,
to pay its corresponding cost.
```

Source: [extracted/five-tribes-the-djinns-of-naqala-rules.txt, lines 385–397](../../../extracted/five-tribes-the-djinns-of-naqala-rules.txt#L385).

```text
SMALL MARKET
Pay 3 Gold Coins and pick one Resource
card of your choice from among the ﬁrst 3 visible
(at the start of the line). As always, do not
replace any of the Resource cards you took yet!
LARGE MARKET
Pay 6 Gold Coins and pick 2 Resource
cards of your choice from among the ﬁrst 6
visible (at the start of the line). In the unlikely
event there is only 1 Resource card left to pick,
you must still pay 6 Gold Coins if you wish to
pick it in a Large Market. As always, do not
replace any of the Resource cards you took yet!
```

Source: [extracted/five-tribes-the-djinns-of-naqala-rules.txt, lines 398–403](../../../extracted/five-tribes-the-djinns-of-naqala-rules.txt#L398).

```text
SACRED PLACES
Pay either 2 Elders OR 1 Elder + 1 Fakir to take
the Djinn of your choice, from among those
visible (place these Elders back in the bag, and
discard the Fakir). Do not replace the Djinn
card you take yet! (see Clean-Up). 
```

Source: [extracted/five-tribes-the-djinns-of-naqala-rules.txt, lines 121–122](../../../extracted/five-tribes-the-djinns-of-naqala-rules.txt#L121).

```text
! Sum of VPs for each series of Merchandise (but not
Fakirs) you own that are all different
```

Source: [extracted/five-tribes-the-djinns-of-naqala-rules.txt, lines 306–308](../../../extracted/five-tribes-the-djinns-of-naqala-rules.txt#L306).

```text
BONUS: You can discard as many Fakir cards from your
hand as you wish, to increment that multiplier factor
by 1 for each Fakir discarded. 
```

Source: [extracted/five-tribes-the-djinns-of-naqala-rules.txt, lines 321–323](../../../extracted/five-tribes-the-djinns-of-naqala-rules.txt#L321).

```text
BONUS: You can discard as many Fakir cards from your
hand as you wish to increase the range of your Assassins,
1 more Tile in distance for each Fakir.
```

Source: [extracted/five-tribes-the-djinns-of-naqala-rules.txt, lines 465–471](../../../extracted/five-tribes-the-djinns-of-naqala-rules.txt#L465).

```text
doubt, see Victory Points on p. 3).
The player with the most VPs wins
the game and becomes Great Sultan
of Naqala! In the unlikely event two
(or more players) are tied, they will
have to learn how to share power
as Sultans – or play again!
```

Source: [extracted/five-tribes-the-djinns-of-naqala-rules.txt, lines 353–382](../../../extracted/five-tribes-the-djinns-of-naqala-rules.txt#L353).

```text
2.6 Merchandise Sale (Optional)
Before wrapping up your actions for this turn, once all your Tribe
and Tile Actions are done, you may, IF YOU WISH, sell some
Merchandise (but not Fakirs) before ending your turn. 
To do so, discard one or more suits of Merchandise cards, all
different from each other, and immediately take from the bank the
corresponding number of Gold Coins: 1 - 3 - 7 - 13 - 21 - 30 - 40 - 50 or
60 depending on how many different Merchandise cards you hold
in a suit.
Note: Only sell when you are desperately short on Gold Coins
to bet on your turn order. Otherwise you are usually better oﬀ
keeping Merchandise to try and sell a larger suit later on. Even
if you don’t succeed in accumulating more Merchandise cards
of other types, you will be able to at least sell your suit(s) at
the same price on your last turn!
3. Clean-Up
Once all players have taken turns playing all their Actions, before
moving on to the next Bid for Turn Order Phase, the player closest
to the piles of Djinns and Resource cards must :
! Replenish the row of Resource cards:
Shift any Resource card that may still be face up to the front of
the row and draw new ones to make a total of 9 face up available.
In the unlikely event you run out of Resource cards in the Draw
pile, reshuffle any discards; if there are no cards left, then none
can be taken.
! Replenish the row of Djinns cards:
Shift any Djinn card that may still be face up to the front of the
row and draw new ones to make a total of 3 face up available.
In the unlikely event you run out of Djinn cards in the Draw
pile, reshuffle any discards.
```

Source: [extracted/five-tribes-the-djinns-of-naqala-rules.txt, lines 420–420](../../../extracted/five-tribes-the-djinns-of-naqala-rules.txt#L420).

```text
The Fakirs can’t be sold.
```

Source: [extracted/five-tribes-the-djinns-of-naqala-rules.txt, lines 441–459](../../../extracted/five-tribes-the-djinns-of-naqala-rules.txt#L441).

```text
Wonder games or visit us at:
End of the Game
The Game stops at the end of the Turn during which either of
these 2 events occur:
! A player drops his last Camel on a Tile:
The player takes control of the Tile by placing his last Camel
and finishes his actions as normal; the game ends once ALL
players have had a chance to take their actions for this turn
too. The game then ends and final scores are computed.
! No more legal Meeples movement is possible:
This player, and all players after him, can no longer make any
move; they may still be able, and want, to take some other
actions, i.e. invoke the special powers of some of the Djinns
they own, and can do so before passing to the next player.
Once all players have played the Actions they could still take
(or passed), the Turn finishes; the game ends and scores are
computed.
Note: Correctly betting on your last turn can thus be crucial. An
imprudent player may bid some Gold Coins but still ﬁnd himself
```

Source: [extracted/five-tribes-the-djinns-of-naqala-rules.txt, lines 309–323](../../../extracted/five-tribes-the-djinns-of-naqala-rules.txt#L309).

```text
Red Assassins Tribe 
Put these Red Meeples immediately back in the bag.
Kill ONE other Meeple: Remove it and immediately
place it back in the bag. 
This Meeple could either be:
! 1 Meeple of the color of your choice, located on
a Tile no farther away from your ﬁnal Tile than 1
Tile per Assassin you just dropped in the bag
(always counting sideways, never diagonally, for
distance purposes)
! Or 1 Yellow or 1 White Meeple currently held by
one of your Opponents in front of him/her.
BONUS: You can discard as many Fakir cards from your
hand as you wish to increase the range of your Assassins,
1 more Tile in distance for each Fakir.
```

Review status: pending independent audit.

## flamecraft

[Flamecraft](../../../rules/flamecraft.md): hand and Goods limits, final turns, scoring, and tiebreakers.

### Corrected rules

```diff
--- Original summary
+++ Corrected summary
@@ -46,7 +46,7 @@
 
 ### 3. End of Turn
 - **Expand Town**: If you filled a Shop's last slot, draw a new Shop face-down on an empty Town space. Reveal it now.
-- **Discard**: Discard down to 7 Artisan Dragons and 7 Goods tokens in hand/supply.
+- **Limits**: Return excess Artisan Dragons to the bottom of their deck until you have at most 6 in hand; return excess Goods to the supply until you have at most 7 tokens of each type.
 - **Refresh**: Refill face-up Enchantments and Artisan Dragons in the Park to 5 each.
 
 ## Actions
@@ -65,15 +65,13 @@
 Enchantments grant Reputation, Fancy Dragons, Artisan Dragons, or Coins when cast. They also add a permanent Good production to the Shop.
 
 ### Fancy Dragons
-Secret goal cards that score Reputation when fulfilled (e.g., "have 3 Enchantments at Shops you visited" or "have placed Dragons at 4 different Shops"). Reveal and score at any time during your turn when conditions are met.
+Fancy Dragons have secret goals. Sun Dragons may be revealed and scored once during your turn when their goals are met. Moon Dragons score fulfilled goals at game end; if an ability scores one earlier, it cannot score again. Turn in Coins for Reputation before scoring end-game Fancy Dragons.
 
 ## Scoring / Victory Conditions
 
-The game ends immediately when either:
-- The Artisan Dragon deck runs out, OR
-- The Enchantment deck runs out.
+Drawing or revealing the last card of the Artisan Dragon deck or Enchantment deck triggers the game end. Finish that turn, then each player gets one final turn, including the player who triggered the end.
 
-Finish the current round so all players have equal turns. The player furthest ahead on the Reputation track wins. Ties broken by: most unspent Coins (each worth 1 Reputation), then most Goods, then most Artisan Dragons in hand.
+For final scoring, add 1 Reputation per leftover Coin and the rewards for fulfilled end-game Fancy Dragons. Highest Reputation wins. Ties are broken by most Artisan Dragons in hand, then most leftover Goods; if still tied, share the victory.
 
 ## Special Rules & Edge Cases
 
@@ -82,7 +80,7 @@
 - **Town Capacity**: 12 Shop spaces in 1-2 player games; up to 14 in 3-5 player games. If Town is full, ignore "Filling a Shop."
 - **Enchantment Limit**: Each Shop can have at most 3 Enchantments.
 - **Visiting Occupied Shops**: You must have enough Goods/Coins to pay each opponent 1 Good/Coin to visit their Shop.
-- **Dragon/Goods Limits**: Max 7 Artisan Dragons in hand; max 7 Goods tokens in supply.
+- **Dragon/Goods Limits**: At end of turn, max 6 Artisan Dragons in hand and max 7 Goods tokens of each type. Coins and Fancy Dragons have no limit.
 
 ## Player Reference
 
```

### Rulebook evidence

Source: [extracted/flamecraft-rules.txt, lines 443–460](../../../extracted/flamecraft-rules.txt#L443).

```text
DRAGONS & GOODS LIMIT: Return Dragons and Goods until you have no 
more than 6 Artisan Dragons and 7 Goods of each type.
REFRESH PARK & ENCHANTMENTS: Draw new faceup Artisan Dragons 
and Enchantments until there are 5 of each.
Expand Town
If you filled any Shops on your turn and 
drew new ones, flip these new Shops 
faceup. They are now available for players 
to visit.
Dragons & Goods Limit
At the end of your turn, you may have no more 
than 6 Artisan Dragons in your hand. If you do, 
you must return Dragons of your choice to the 
bottom of the Artisan deck until you have 6. 
Additionally, you may have no more than 7 
tokens of each Goods type. If you have more 
than 7 of any type, you must return tokens to the 
appropriate piles until you have 7.
```

Source: [extracted/flamecraft-rules.txt, lines 478–498](../../../extracted/flamecraft-rules.txt#L478).

```text
End of the Game
When the last card in either the Artisan deck or Enchantment 
deck is drawn or revealed, this triggers the end of the game. Each 
player gets 1 final turn, including the player who triggered the 
game end. 
Once all players have had a final turn, players gain end-game 
Reputation as follows:
LEFTOVER COINS: Each player returns all Coins in their supply 
to the Fountain and gains 1
 per returned Coin.
FANCY DRAGONS: Each player reveals each Fancy Dragon 
with a 
 icon whose goals they’ve fulfilled and scores the 
indicated amount of 
Whoever has the highest Reputation score wins!
Tiebreakers
In the case of a tie, the tied player with the most Artisan Dragons 
left in their hand wins. If still tied, the tied player with the most 
leftover Goods in their supply wins . If still tied, they share 
a well-deserved victory!
These unique Dragons are attracted to the activities of 
```

Source: [extracted/flamecraft-rules.txt, lines 443–470](../../../extracted/flamecraft-rules.txt#L443).

```text
DRAGONS & GOODS LIMIT: Return Dragons and Goods until you have no 
more than 6 Artisan Dragons and 7 Goods of each type.
REFRESH PARK & ENCHANTMENTS: Draw new faceup Artisan Dragons 
and Enchantments until there are 5 of each.
Expand Town
If you filled any Shops on your turn and 
drew new ones, flip these new Shops 
faceup. They are now available for players 
to visit.
Dragons & Goods Limit
At the end of your turn, you may have no more 
than 6 Artisan Dragons in your hand. If you do, 
you must return Dragons of your choice to the 
bottom of the Artisan deck until you have 6. 
Additionally, you may have no more than 7 
tokens of each Goods type. If you have more 
than 7 of any type, you must return tokens to the 
appropriate piles until you have 7.
Refresh Park & 
Enchantments
If there are fewer than 5 faceup Artisan 
Dragons or Enchantments, reveal new cards from 
the appropriate decks until there are 5 each. 
If the Artisan deck or Enchantment deck runs out, 
this triggers the end of the game (see “End of 
the Game,” next page).
There is no limit to the number of Coins and Fancy 
Dragons you can have. These do not need to be 
```

Source: [extracted/flamecraft-rules.txt, lines 505–536](../../../extracted/flamecraft-rules.txt#L505).

```text
by using abilities. There is no limit to the 
number of Fancy Dragons you can have.
Each Fancy Dragon has a specific goal. If you 
fulfill a Fancy Dragon’s goal, it will shower you 
with Reputation and other rewards. 
MOON DRAGONS
These Fancy Dragons are only scored at the end of the 
game. When the game ends, reveal all your 
and gain rewards from each of them whose goal you have 
fulfilled.
If an ability lets you score a 
during the game, you can’t score it 
again at the end of the game. 
SUN DRAGONS
These Fancy Dragons can only be scored during the 
game. If you have fulfilled a 
 Dragon’s goal, you may 
reveal it at any time on your turn to gain its rewards. If 
its goal requires you to spend Goods, return these to the 
appropriate piles. 
You can only score each of your 
 
Dragons once per game. Leave scored 
 Dragons faceup in front of you.
Fancy Dragons
 You must turn in all your Coins before scoring 
your Fancy Dragons. This means you can’t use 
Coins to fulfill your Fancy Dragons’ goals.
TYPE
GOAL & 
REWARD

```

Review status: pending independent audit.

## forbidden-sky

[Forbidden Sky](../../../rules/forbidden-sky.md): launch requirements, abandonment loss, and wind movement.

### Corrected rules

```diff
--- Original summary
+++ Corrected summary
@@ -39,7 +39,7 @@
 ### 2. Draw and Resolve Storm Cards
 
 Draw Storm cards equal to the Storm Intensity level. Resolve each:
-- **High Winds**: Blow all unprotected pawns in the indicated direction. If blown off the platform, lose 1 rope. If rope runs out, game over. Wind Shelter tiles protect from this.
+- **High Winds**: Blow all unprotected pawns in the indicated direction. If the wind would push a pawn off the platform or across an unconnected cloud gap, the pawn stays in place and loses 1 rope. If rope runs out, game over. Wind Shelter tiles protect from this.
 - **Lightning Strikes!**: All lightning rods get struck. Any pawn on a tile connected to a lightning rod by wires (physical or printed) loses 1 health. Faraday Cage tiles protect from this.
 - **Storm Intensifies**: Increase Storm meter by 1.
 
@@ -70,20 +70,20 @@
 
 ## Scoring / Victory Conditions
 
-**Win**: Complete the circuit shown on your Blueprint card. All components (required capacitors, lightning rods, and launch pad) must be wired into one continuous circuit. Then the rocket launches automatically.
+**Win**: Wire the required Blueprint components into a series circuit, leaving one wire unconnected. Place the rocket on the launch pad and get every player onto one of its four tiles. Add the final wire to complete the circuit and launch the rocket.
 
 **Lose** (any of these):
 - Any player's health reaches 0
 - Any player's rope meter reaches 0 (blown off the platform)
 - Storm meter reaches the skull
-- Draw pile runs out before circuit is complete
+- The rocket launches before every player is on a launch pad tile
 
 ## Special Rules & Edge Cases
 
 - **Real Circuit**: The game includes real wire components that must form an actual electrical circuit. The rocket lights up and makes sound when the circuit is complete.
 - **Lightning Propagation**: Lightning travels through ALL connected wires (physical and printed on tiles). Be careful about connecting lightning rods to tiles where players stand.
 - **Wind Direction**: The compass on the starting grid indicates the direction of wind. High Winds cards reference this compass.
-- **Falling Off**: If blown off the platform edge, lose 1 rope and return to the nearest tile. If rope runs out, everyone loses.
+- **Falling Off**: If wind movement would take a pawn off the platform or across an unconnected cloud gap, leave the pawn in place and reduce its rope meter by 1. If the rope snaps, everyone loses.
 - **Component Placement**: You may place more components than your Blueprint requires, but you cannot exceed the total supply.
 - **Equipment Sharing**: Equipment cards can be passed to players on the same tile for free.
 
@@ -102,4 +102,4 @@
 | Wire | Connect 2 adjacent components with a wire |
 
 ### Win Condition
-- Complete the Blueprint circuit with all required components wired together
+- Get everyone onto launch pad tiles before connecting the last wire of the required Blueprint circuit
```

### Rulebook evidence

Source: [extracted/forbidden-sky-rules.txt, lines 240–251](../../../extracted/forbidden-sky-rules.txt#L240).

```text
Creating the Circuit
In order to take off in the rocket, you must wire the launch pad into 
a circuit, using the components listed on your blueprint card. 
The blueprint shows the minimum number of each kind of component 
that must be used. (You may use more.) The components must be in 
a true series circuit, that is, they must be connected in a circle starting 
with a wire connected to one side of the launch pad and ending with 
a wire connected to the opposite side of the launch pad. 
Watch out! As soon as the very last wire is placed, the rocket will launch! 
Be sure each pawn is on one of the four tiles holding the launch pad 
before you place the last wire, or the rocket will leave adventurers 
behind—and everyone will lose the game!
```

Source: [extracted/forbidden-sky-rules.txt, lines 345–359](../../../extracted/forbidden-sky-rules.txt#L345).

```text
Winning the Game
Get to the Launch Pad! Once you have wired the required 
components into a circuit (except one final wire that you’ll use to 
take off), first place the rocket onto the launch pad. Then everyone 
should head to one of the four tiles containing the launch pad. 
(You all don’t have to be on the same tile.) As a final step, one player 
must add the last wire (either on their turn or by Remote Fuser) 
to complete the circuit and launch the rocket for the win!
Losing the Game
There are 4 possible ways to lose:
1.	 Electrocuted. If the clip on any player’s health meter reaches .
2.	 Fall. If the clip on any player’s rope meter reaches .
3.	 Swept Away. If the clip on the Storm meter reaches .
4.	 Abandoned. If the rocket takes off before everyone is on 
a launch pad tile.
```

Source: [extracted/forbidden-sky-rules.txt, lines 354–359](../../../extracted/forbidden-sky-rules.txt#L354).

```text
There are 4 possible ways to lose:
1.	 Electrocuted. If the clip on any player’s health meter reaches .
2.	 Fall. If the clip on any player’s rope meter reaches .
3.	 Swept Away. If the clip on the Storm meter reaches .
4.	 Abandoned. If the rocket takes off before everyone is on 
a launch pad tile.
```

Source: [extracted/forbidden-sky-rules.txt, lines 364–375](../../../extracted/forbidden-sky-rules.txt#L364).

```text
High Winds
These 4 cards “blow” the adventurers one tile in 
the direction of the arrow on the wind compass. 
If a pawn cannot move because there is no tile 
in that direction, then that adventurer’s rope gets 
worn by 1 point instead. (Lower the rope clip on 
the adventurer card to the next lowest tick mark.) 
If there’s a tile in that direction but it is only 
connected by clouds (the platform surface is not attached) the pawn 
does not move and that adventurer’s rope loses 1 point instead. 
If a clip reaches the symbol, the rope has snapped, that character 
falls 7,000 feet, and everyone loses the game.
```

Review status: pending independent audit.

## fort

[Fort](../../../rules/fort.md): game-end triggers, scoring, recruitment, and card rewards.

### Corrected rules

```diff
--- Original summary
+++ Corrected summary
@@ -47,7 +47,8 @@
 ### Phase 3: Recruit
 You may recruit 1 Kid card from:
 - The face-up Park (3 cards), OR
-- Any opponent's Yard.
+- Any player's Yard, including your own, OR
+- The top of the Park deck.
 
 Add the recruited card to your discard pile. If from the Park, replace from the deck.
 
@@ -78,30 +79,27 @@
 | 5 | 6 | 5 resources (specific) | Gain Macaroni Sculpture |
 
 ### Made-Up Rules
-One-time or ongoing benefits gained at Fort Level 1 and when drawn.
+At Fort Level 1, privately choose one Made-Up Rule from the central stack. It scores points at game end.
 
 ### Perks
-Persistent abilities gained at Fort Level 2 (choose from face-up row).
+At Fort Level 2, choose a Perk from the face-up row. Some Perks have persistent effects; others can be used once per game.
 
 ### Macaroni Sculpture
-The first player to reach Fort Level 5 takes the Macaroni Sculpture (worth 2 VP at game end).
+The first player to reach Fort Level 5 takes the Macaroni Sculpture (worth 4 VP at game end).
 
 ## Scoring / Victory Conditions
 
-The game ends at the end of the round when any player reaches Fort Level 5 (all players get equal turns).
+The game end triggers when any player has 25 or more VP on the Victory Track, any player reaches Fort Level 5, or the Park deck is empty (even if face-up Park cards remain). The leader finishes their turn, then finish the current round so all players have equal turns.
 
 **Final Scoring:**
 | Source | Points |
 |--------|--------|
 | Fort Level | VP per level (printed on player board) |
-| Pack | 1 VP per resource in Pack |
-| Lookout | 1 VP per card in Lookout |
-| Made-Up Rules | VP as indicated |
-| Perks | VP as indicated |
-| Macaroni Sculpture | 2 VP (if held) |
+| Made-Up Rule | VP as indicated by your card, if any |
+| Macaroni Sculpture | 4 VP (if held) |
 | Victory Track | VP accumulated during game |
 
-Highest total VP wins. Tiebreaker: highest Fort Level, then most resources in Pack.
+Highest total VP wins. Tiebreaker: highest Fort Level; if still tied, share the victory.
 
 ## Special Rules & Edge Cases
 
@@ -126,4 +124,4 @@
 Skateboard, Shovel, Glue, Squirtgun, Crown, Book (+ wild Coin)
 
 ### Game End Trigger
-Any player reaches Fort Level 5 (finish the round)
+Any player reaches 25 VP on the track, any player reaches Fort Level 5, or the Park deck is empty (finish the round)
```

### Rulebook evidence

Source: [extracted/fort-rules.txt, lines 253–255](../../../extracted/fort-rules.txt#L253).

```text
When you reach Level 5, take the macaroni sculpture card, unless 
another player already has it. This triggers the end of the game, and it 
scores you 4 victory points at the end.
```

Source: [extracted/fort-rules.txt, lines 256–263](../../../extracted/fort-rules.txt#L256).

```text
End of Game
The end of the game triggers in any one of these three ways:
Any player has 25 or more victory points on the Victory Track
Any player reaches Fort Level 5
The Park deck is empty (even if the Park still has cards)
When the end of the game triggers, the leader finishes their turn, then 
the players finish the current round of turns (so that all the players 
have taken the same number of turns).
```

Source: [extracted/fort-rules.txt, lines 263–272](../../../extracted/fort-rules.txt#L263).

```text
have taken the same number of turns).
At the end of that round, each player reveals their made-up rule (if 
any) and adds up their victory points from their:
Victory Track
Fort Level
Made-Up Rule (if any)
Macaroni Sculpture (if any)
The player with the most victory points is the winner. If there is a tie, 
the tied player with the highest Fort Level wins. If still tied, share the 
victory. 
```

Source: [extracted/fort-rules.txt, lines 270–272](../../../extracted/fort-rules.txt#L270).

```text
The player with the most victory points is the winner. If there is a tie, 
the tied player with the highest Fort Level wins. If still tied, share the 
victory. 
```

Source: [extracted/fort-rules.txt, lines 245–249](../../../extracted/fort-rules.txt#L245).

```text
your Lookout and one more resource in your Pack.
When you reach Level 1, privately choose a made-up rule card 
(page 15) from the central stack and put it in front of you facedown. 
Your made-up rule will score you points at the end of the game.
When you reach Level 2, choose a face-up perk card (page 16) from 
```

Source: [extracted/fort-rules.txt, lines 249–252](../../../extracted/fort-rules.txt#L249).

```text
When you reach Level 2, choose a face-up perk card (page 16) from 
the central row and put it in front of you. Some perks have persistent 
effects that you will have for the entire game, while other perks can 
only be used once per game.
```

Source: [extracted/fort-rules.txt, lines 212–221](../../../extracted/fort-rules.txt#L212).

```text
to your turn, as long as you discard a matching card each time.
Phase 3: Recruit
Time to make a new friend! Maybe you’ll take someone else’s?
You must recruit one card, placing it in your discard pile. You may 
recruit in one of three ways:
Take any card from the Park. Immediately draw a new card 
from the Park deck to replace it.
Take any card from any player’s Yard. They do not draw a 
new card.
Draw a card from the Park deck.
```

Review status: pending independent audit.

## my-city

[My City](../../../rules/my-city.md): campaign progress scoring and passing.

### Corrected rules

```diff
--- Original summary
+++ Corrected summary
@@ -36,7 +36,7 @@
 - Each building tile must be placed on empty spaces on your game board.
 - Tiles cannot overlap previously placed tiles or extend off the board.
 - Tiles must be placed in valid positions following the episode's placement rules.
-- If you cannot or choose not to place a tile, you pass and set it aside.
+- If you cannot or choose not to place a tile, you may pass, setting it aside and losing 1 point. At 0 points you cannot pass: you must end your participation in the episode. You may also end participation voluntarily without losing a point.
 
 ### Scoring Elements (Evolve Over Episodes)
 
@@ -47,7 +47,7 @@
 
 ## Scoring / Victory Conditions
 
-At the end of each episode, players score based on the current episode's rules. Scores are tracked on the scoring track across all 24 episodes.
+At the end of each episode, score using that episode’s rules. Episode scores determine who colors in progress symbols; the scoring track is used for the current episode, not a cumulative campaign score.
 
 ### Legacy Elements
 
@@ -57,7 +57,7 @@
 - Stickers that modify the game board
 - Story developments that change rules
 
-The player with the most cumulative victory points after all 24 episodes wins the campaign.
+The player with the most colored-in progress symbols after all 24 episodes wins the campaign.
 
 ### Eternal Game
 
@@ -79,4 +79,4 @@
 | Place | All players simultaneously place matching tile or pass |
 | Score | End of episode: score according to current rules |
 | Chapter | Open envelope for new rules and components |
-| Campaign | 24 episodes across 8 chapters; track cumulative score |
+| Campaign | 24 episodes across 8 chapters; most progress symbols wins |
```

### Rulebook evidence

Source: [extracted/my-city-rules.txt, lines 54–59](../../../extracted/my-city-rules.txt#L54).

```text
in the space at the top, right next to the animal symbol. 
•	 Each player gets a scoring token and sets it on the number 
10 of his or her board’s scoring track. 
This scoring token is used to indicate your points 
during the episode and, most importantly, at the 
end of the episode. 
```

Source: [extracted/my-city-rules.txt, lines 81–87](../../../extracted/my-city-rules.txt#L81).

```text
allowed. All players place their buildings at the same time. 
At the end of each episode, you get points for your buildings, 
which you mark on your scoring track. Whoever gets the most 
or second-most points in an episode is allowed to color in two or 
one progress symbols, respectively. These progress symbols appear 
as circles in two rows at the top edge of the game board. The 
player who has colored in the most progress symbols after 
```

Source: [extracted/my-city-rules.txt, lines 169–180](../../../extracted/my-city-rules.txt#L169).

```text
that are already constructed.
•	 Once a building is placed, it cannot be moved. 
•	 Passing: If a player cannot or does not want to construct 
a building, he or she is allowed to pass. He or she announces 
this out loud and places the building face down in front of 
himself or herself. He or she then has to move the scoring 
token one step backward on the scoring track.
Important: If the scoring token is already on zero, 
passing is not an option. In this case, if the player cannot 
or does not want to construct the building, he or she 
must end his or her participation in the episode. He or 
she is then not allowed to place any more buildings.
```

Source: [extracted/my-city-rules.txt, lines 360–367](../../../extracted/my-city-rules.txt#L360).

```text
•	 Ending participation in an episode: After turning over 
each construction card, each player is always allowed to 
decide whether to end his or her own participation in 
the episode. He or she announces this out loud and turns 
the unconstructed building over. When he or she does 
this, the player does not lose any points on the scoring 
track. He or she only loses a point if he or she passes but 
stays in the episode. 
```

Review status: pending independent audit.

## mysterium

[Mysterium](../../../rules/mysterium.md): Crow tokens, visions, timed guesses, and the final vote.

### Corrected rules

```diff
--- Original summary
+++ Corrected summary
@@ -32,7 +32,7 @@
 
 ### Phase 1: Vision
 
-1. The Ghost distributes Vision cards face down to each Psychic who has not yet solved their current clue type (suspect/location/object).
+1. The Ghost gives each active Psychic one vision of one or more face-up Vision cards, then immediately refills their own hand to 7 before giving the next vision.
 2. Psychics simultaneously examine their Vision cards and discuss amongst themselves.
 3. Each Psychic places their Intuition pawn on the card they believe matches their clue.
 4. Other Psychics may place Clairvoyancy tokens (approve/reject) on each guess.
@@ -41,7 +41,7 @@
 
 1. The Ghost reveals whether each Psychic's guess is correct or incorrect.
 2. **Correct**: The Psychic advances to the next clue type (suspect -> location -> object).
-3. **Incorrect**: The Psychic stays on the same clue type. The Ghost may spend a Crow token to give an extra Vision card.
+3. **Incorrect**: The Psychic stays on the same clue type and keeps their Vision cards for the next hour.
 4. Advance the clock 1 hour.
 
 ## Actions
@@ -49,7 +49,7 @@
 ### Ghost Actions
 
 - Distribute 1+ Vision cards to each active Psychic (trying to hint at the correct suspect/location/object).
-- Spend Crow tokens to give additional Vision cards to struggling Psychics.
+- Use a Crow token at any time to discard up to 7 Vision cards from the Ghost’s own hand and draw the same number of replacements; uses are limited by difficulty.
 - Cannot speak or gesture; communication is only through Vision cards.
 
 ### Psychic Actions
@@ -74,12 +74,12 @@
 2. The Ghost places 3 Vision cards (representing the true culprit) face down.
 3. Based on Clairvoyancy Level, Psychics can see 1, 2, or all 3 of these cards.
 4. Each Psychic secretly votes for which suspect group they believe is the true culprit.
-5. Majority vote wins. If correct, all players win. If incorrect, all players lose.
+5. The group with the most votes is selected. If groups tie, the vote of the Psychic with the highest Clairvoyancy Level determines the choice among them; age breaks a tie in Clairvoyancy Level. If the selected group is correct, all players win; otherwise all lose.
 
 ## Special Rules & Edge Cases
 
 - **Difficulty levels**: Easy (more Crow tokens, fewer suspect cards), Medium, Hard (fewer Crow tokens, more suspect cards).
-- The Ghost may use the hourglass to limit discussion time.
+- After giving the last Psychic their vision, the Ghost starts the 2-minute hourglass. Guesses and Clairvoyancy tokens must be finalized before time runs out.
 - Vision cards used are discarded; the Ghost draws replacements.
 - If the Vision card deck runs out, reshuffle discards.
 - In 2-3 player games, the Clairvoyancy system is not used.
@@ -92,5 +92,5 @@
 | Revelation | Ghost confirms correct/incorrect; advance or stay |
 | Clock | Advance 1 hour per round; 7 hours maximum |
 | Final | Ghost plays 3 cards for true culprit; Psychics vote |
-| Win | All Psychics solve their 3 clues AND majority identifies true culprit |
+| Win | All Psychics solve their 3 clues AND the selected final group identifies the true culprit |
 | Lose | Any Psychic unsolved after 7 hours, or wrong final vote |
```

### Rulebook evidence

Source: [extracted/mysterium-rules.txt, lines 152–167](../../../extracted/mysterium-rules.txt#L152).

```text
Psychic finds the correct card among the cards 
of the table (i.e. the one that matches the card 
hidden behind the Screen). To create a vision, the 
Ghost may use one or several Vision Cards from 
their hand.
Once the Ghost has created their vision, they give 
the chosen Vision Card(s) to that Psychic face 
up, and push the Ghost Token matching that 
Psychic’s color against the Screen to mark that 
this Psychic now received their vision. A Psychic 
cannot receive more that one vision on each turn.
Then, the Ghost immediately draws new 
Vision Cards until they have 7 cards 
in hand. If the drawing pile runs out, 
shuffle the discarded Vision Cards 
to create a new pile.
```

Source: [extracted/mysterium-rules.txt, lines 182–186](../../../extracted/mysterium-rules.txt#L182).

```text
Once the Ghost has drawn their new cards, they choose another Psychic and repeat this process, until all Psychics have received their Vision Cards for this turn. 
As soon as the last Psychic has received a vision, the Ghost turns over the Hourglass (time: 2 minutes).
As soon a Psychic receives their Vision Cards, they can look at them and show them to the other Psychics. Together, they can try to interpret the cards to deduce 
which card (Character, Location or Object, depending on their Progress Track and Intuition Pawn) they are supposed to identify. Psychics can talk to each other 
without restriction – they simply cannot talk to the Ghost. 
```

Source: [extracted/mysterium-rules.txt, lines 266–277](../../../extracted/mysterium-rules.txt#L266).

```text
If, as a Psychic, you chose any other card: 
• Each Psychic that placed a 
 Clairvoyancy Token next to your Intuition 
Pawn move their Clairvoyancy Level Token one space forward.
• For Psychics that placed a 
 Clairvoyancy Token, nothing happens.
• All used Clairvoyancy Tokens are discarded to the Clock Board on the 
matching colored spots.
• Move your Intuition Pawn back to the Progress Board where it was at the 
beginning of your turn.
• Keep all of your Vision Cards. The Ghost will complete your vision with new 
cards on the next turn.
```

Source: [extracted/mysterium-rules.txt, lines 198–202](../../../extracted/mysterium-rules.txt#L198).

```text
Discarding Vision Cards
Creating a vision might be difficult. As the Ghost, you may want to discard your hand to replace it with more inspiring cards. If you want 
to do so, place one of your Crow Tokens on your Screen. Discard up to 7 cards and draw the same number of cards to replace them.
You can discard cards at any time; however, you can only use the Crow a limited number of times, depending on the difficulty level 
that you chose. If you run out of Crow Tokens, then you can no longer discard your Vision Cards to replace them.
```

Source: [extracted/mysterium-rules.txt, lines 379–388](../../../extracted/mysterium-rules.txt#L379).

```text
Clairvoyancy Token on the group with the matching number.
• If a group has more Clairvoyancy Tokens than any other, then that group is chosen as the suspected Culprit’s group.
• If there is no majority on a given group, then the vote of the Psychic with the highest Clairvoyance Level (or the eldest Psychic if there is a tie) determines 
which group (amongst the tied groups) is the suspected Culprit’s group.
You may now reveal the Culprit Token. If the Psychics chose the correct group (the one with the same number), then you all win: the culprit is exposed! If, however, 
you chose the wrong group, then you all lose, and the Ghost’s soul keeps wandering in limbo…
Rules for 2 or 3 players
For 2- or 3-player games, use the following adjustments. 
Phase 1: Reconstruction of Events 
• The Clairvoyancy Track, the Clairvoyancy Level Tokens and the Clairvoyancy Tokens are not used.
```

Source: [extracted/mysterium-rules.txt, lines 182–192](../../../extracted/mysterium-rules.txt#L182).

```text
Once the Ghost has drawn their new cards, they choose another Psychic and repeat this process, until all Psychics have received their Vision Cards for this turn. 
As soon as the last Psychic has received a vision, the Ghost turns over the Hourglass (time: 2 minutes).
As soon a Psychic receives their Vision Cards, they can look at them and show them to the other Psychics. Together, they can try to interpret the cards to deduce 
which card (Character, Location or Object, depending on their Progress Track and Intuition Pawn) they are supposed to identify. Psychics can talk to each other 
without restriction – they simply cannot talk to the Ghost. 
Note: Psychics may start to discuss and even place their pawns and tokens as soon as they receive their cards, even if the Hourglass has not yet been turned over. 
All Psychics try to resolve the vision that they received. They must place 
their Intuition Pawn before the time runs out. As long as there is time 
remaining, Psychics may change their mind and move their Intuition 
Pawn; their decision is final once the time is up.
Note: Several Psychics may place their Intuition Pawn on the 
```

Review status: pending independent audit.

## oceans

[Oceans](../../../rules/oceans.md): surviving population scoring and the trait-card tiebreaker.

### Corrected rules

```diff
--- Original summary
+++ Corrected summary
@@ -65,7 +65,7 @@
 
 **Last round triggers** when the final (3rd) Ocean zone runs out of population. Complete the round so all players have equal turns.
 
-Score: 1 point per population token behind your screen + bonus token value. **Highest score wins.**
+Score 1 point per population token behind your screen, plus 1 point per population token on your surviving species, plus your Bonus Token value. **Highest score wins.** Ties are broken by most trait cards on surviving species. The rulebook’s final tie clause is the first tied player to get a fishing-boat job in Alaska.
 
 ## Special Rules & Edge Cases
 
```

### Rulebook evidence

Source: [extracted/oceans-rules.txt, lines 405–411](../../../extracted/oceans-rules.txt#L405).

```text
Players score:
•	 1 point for each population in their score pile.
•	 1 point for each population on their surviving species.
•	 the points listed on their Bonus Token.
The player with the highest score wins. In case of a tie, the tied player with the most trait 
cards on their species wins. If there is still a tie, the first person to get a job on a fishing boat 
in Alaska is the winner!
```

Review status: pending independent audit.

## olympos

[Olympos](../../../rules/olympos.md): development costs, Wonder requirements, final turns, and scoring.

### Corrected rules

```diff
--- Original summary
+++ Corrected summary
@@ -51,11 +51,11 @@
 5. **Pay:** Advance on Time Track by total APs spent.
 
 ### Action B: Development
-Make a Discovery or build a Wonder using Territory tokens and/or Resource cubes. Territory tokens are permanent (not consumed); Resource cubes are spent.
+Make a Discovery by satisfying its resource requirements with Territory tokens and/or Resource cubes. Territory tokens are retained; Resource cubes are spent. Wonders instead require the printed number of Stars from tokens, discoveries, relevant column bonuses, and cards.
 
 - Take the Discovery tile and gain its power.
 - Claim a bonus from below the Discovery on the development board.
-- Development costs **2 AP** on the Time Track.
+- Making a Discovery or building a Wonder costs **7 AP** on the Time Track before applicable discovery discounts.
 
 ## Actions
 
@@ -67,17 +67,20 @@
 
 ## Scoring / Victory Conditions
 
-Game ends when **all players** have reached or passed the mandatory end space on the Time Track.
+After passing the last Zeus space, a player may pass or take one final action on their next turn. That action must not move them past the Cross space. Score after every player has finished.
 
 **Scoring:**
-- Discovery tiles: Prestige value printed on each
-- Wonder tiles: Prestige value
-- Star tokens (from Tribes): 3 Prestige each
-- Destiny card bonuses
-- Territory tokens: some end-game scoring
-- Atlantis territories: additional Prestige
+- Final Time Track position: 0–5 Prestige
+- Prestige tokens: their face values
+- Controlled normal territories: 1 point each; Atlantis territories: 2 each (conquered settlers do not score)
+- Discoveries: 2 points each; Wonders: 8–12 points each
+- Poetry and Philosophy: 3 and 5 bonus points respectively, in addition to the 2 points per Discovery tile
+- Bonuses from Absolutism, City, Science, and Engineering; Engineering awards 3 points per Star token
+- Each unplayed Destiny card: 1 point
+- Keres penalty: −2 points for each affected player
+- Resource cubes and Hourglass tokens: 0 points
 
-Highest total Prestige wins.
+Highest total Prestige wins. Ties are broken by most Discovery and Wonder tiles combined.
 
 ## Special Rules & Edge Cases
 
@@ -96,8 +99,8 @@
 
 **Expansion:** Create Settler (2 AP) + Move (1 AP/land, 2 AP/sea) + Combat (1-3 AP) → Advance on Track
 
-**Development:** Pay resources → Take Discovery tile + Bonus → Advance 2 AP
+**Development:** Satisfy Discovery resources or Wonder Stars → Take tile and applicable bonus → Advance 7 AP before discounts
 
 **Hourglass:** 1 token = 1 free AP (use before advancing)
 
-**Game end:** All players pass end space on Time Track
+**Game end:** After passing the last Zeus space, optionally take one final action that does not pass the Cross space; score once all players finish
```

### Rulebook evidence

Source: [extracted/olympos-rules.txt, lines 271–290](../../../extracted/olympos-rules.txt#L271).

```text
identical resources and 1 other different resource (for example, 
3 Gold and 1 Wood).
- To develop Philosophy (bottom/right), the player must pay 
two pairs of resources and two other resources, all different. 
For example, 2 Grain, 2 Wood, 1 Gold and 1 Stone.
The resources used are either Territory tokens or resource 
cubes or both. For example, a player could pay for Surgery with 
2 Grain Territory tokens and a Wood Territory token (all of 
which he keeps) and a Wood cube (which is returned to 
the general stock).
Acquisition: if a player can pay for a discovery using 
a combination of Territory tokens and/or resource cubes, 
then he simply takes the Discovery tile concerned and plac-
es it in front of him. He is now allowed to use the tile’s spe-
cial power (see last page).
Note: a player can only make a given discovery once. It is 
therefore impossible to discover Agriculture twice, for exam-
ple.
Bonus: the player then takes one of his color’s tokens 
from the general stock and places it on any available 
```

Source: [extracted/olympos-rules.txt, lines 331–345](../../../extracted/olympos-rules.txt#L331).

```text
2) Wonders: each Wonder costs the number of Stars 
shown. To build a Wonder, the player must have the correct 
number of Star symbols. Players acquire a star:
For each Star token in front of them;
If they own the Architecture or Engineering discove-
ries;
For each bonus token in the same column as the 
Wonder concerned;
For certain cards.
The player then takes the Wonder tile and places it in 
front of him. This Wonder will earn him victory points at 
the end of the game.
Cost: 7 action points. The player therefore advances his 
token 7 spaces on the Time Track. This ends his turn.
Note: the Architecture discovery reduces this cost.
```

Source: [extracted/olympos-rules.txt, lines 308–311](../../../extracted/olympos-rules.txt#L308).

```text
Cost: 7 action points. The player therefore moves his to-
ken 7 spaces along the Time Track. This ends his turn.
Note: the Money and Agriculture discoveries reduce this 
cost.
```

Source: [extracted/olympos-rules.txt, lines 462–472](../../../extracted/olympos-rules.txt#L462).

```text
End of the game
When a player has passed the last Zeus space on the 
Time Track and it is his turn again, he has the option of 
passing or taking a final turn. If he passes, that ends 
his game. If he takes a final turn, he undertakes one last 
action but this must not result in him going past the Cross 
space. When all the players have finished, the points are 
added up.
Note: the remaining players continue playing until they have 
each reached or passed the last Zeus space on the Time Track 
and taken their optional final action.
```

Source: [extracted/olympos-rules.txt, lines 473–502](../../../extracted/olympos-rules.txt#L473).

```text
Distribution of prestige points: the Time Track is 
now used to show the players’ scores. The track is marked 
every 5 spaces in order to help with the scoring.
Add up the players’ prestige:
The player’s final position on the Time Track 
earns between 0 and 5 points.
Each Prestige token earns the player the value 
shown.
Territories : 
	
• Each “normal” territory is worth 1 point (a 
conquered settler does not earn any points).
	
• Each Atlantis territory is worth 2 points (a 
conquered settler does not earn any points).
Each discovery tile is worth 2 points.
Each Wonder is worth between 8 and 12 
points. The Poetry and Philosophy discoveries 
are worth 3 and 5 points respectively.
The Absolutism, City, Science and Engineer-
ing discoveries provide bonus points (see later).
Deduct 2 points from each player affected by the 
Keres Olympos card.
Each Destiny card in a player’s hand is worth 1 
point.
Note: resource cubes and Hourglass tokens do not 
provide any points.
The player with the most Prestige points wins 
the game. In the event of a tie, the player with the most 
discovery and Wonder tiles wins.
```

Source: [extracted/olympos-rules.txt, lines 612–617](../../../extracted/olympos-rules.txt#L612).

```text
Engineering: 
the 
player 
benefits from a Star and earns 
3 points for each of his Star 
tokens at the end of the game.
```

Source: [extracted/olympos-rules.txt, lines 588–591](../../../extracted/olympos-rules.txt#L588).

```text
Poetry, Philosophy: these are worth 3 and 
5 bonus points respectively at the end of the 
game in addition to the 2 points earned for a 
discovery tile.
```

Review status: pending independent audit.

## ora-et-labora

[Ora et Labora](../../../rules/ora-et-labora.md): landscape extra actions, harvesting, and building placement.

### Corrected rules

```diff
--- Original summary
+++ Corrected summary
@@ -30,16 +30,16 @@
 The game is played over a set number of rounds. On each turn, a player must perform exactly **one** of the following actions:
 
 ### 1. Cut Peat / Fell Trees
-Take peat or wood resources from your estate. Place landscape tiles.
+Remove one moor card to cut peat or one forest card to fell trees. Take the indicated resource quantity from the production wheel, then move that resource indicator to 0.
 
 ### 2. Build a Building
-Pay the required resources and place a building card on your estate. Buildings must be placed adjacent to existing buildings following placement rules.
+Pay the required resources and place a building on a permitted empty landscape space. Cloister buildings must be orthogonally adjacent to another cloister building; other buildings follow their printed terrain requirements.
 
 ### 3. Use a Building
 Place one of your Clergy members on a building (yours or another player's) and activate its production ability.
 
-### 4. Buy a Landscape
-Purchase additional land strips to expand your estate.
+### Extra Action: Buy a Landscape
+In addition to your main action, you may buy one landscape per turn and one per settlement phase. Pay for the topmost district or plot and place it immediately.
 
 After all players have taken their turns, the production wheel advances, increasing all resource availability.
 
@@ -47,11 +47,11 @@
 
 | Action | Description |
 |--------|-------------|
-| **Cut Peat** | Gain peat resources, place moor tiles |
-| **Fell Trees** | Gain wood resources, place forest tiles |
+| **Cut Peat** | Remove a moor card; take peat from the production wheel |
+| **Fell Trees** | Remove a forest card; take wood from the production wheel |
 | **Build** | Pay resources to construct a building on your estate |
 | **Use Building** | Assign Clergy to activate a building's production |
-| **Buy Landscape** | Expand your estate with new land |
+| **Buy Landscape (extra action)** | Buy and immediately place new land; once per turn and once per settlement phase |
 
 **Using buildings:** You may use your own buildings for free or pay another player to use theirs. The Prior can use any building; the Lay Brother has restrictions. After use, Clergy return at specific times.
 
@@ -80,7 +80,7 @@
 
 ## Player Reference
 
-**Turn:** Choose 1 action: Cut Peat / Fell Trees / Build / Use Building / Buy Landscape
+**Turn:** Choose 1 main action: Cut Peat or Fell Trees / Build / Use Building. You may also buy 1 landscape as an extra action.
 
 **Production wheel:** Advances each round; resources accumulate
 
```

### Rulebook evidence

Source: [extracted/ora-et-labora-rules.txt, lines 364–367](../../../extracted/ora-et-labora-rules.txt#L364).

```text
Additional Actions
In addition to carrying out one of the actions outlined above, 
you may carry out as many additional actions on your turn 
as you wish (before or after your main action). 
```

Source: [extracted/ora-et-labora-rules.txt, lines 442–446](../../../extracted/ora-et-labora-rules.txt#L442).

```text
Extra Action Buy a landscape
You may buy a landscape once per turn and once per settlement phase (see below). 
There are rectangular districts as well as square plots. The topmost tile on both 
piles is available for purchase. Their prices are shown at bottom right. (You must place 
the landscape as soon as you buy it; you may not set it aside temporarily.) 
```

Source: [extracted/ora-et-labora-rules.txt, lines 273–281](../../../extracted/ora-et-labora-rules.txt#L273).

```text
Action Fell trees
Remove (maximum) 1 forest card from your landscapes. The production wheel 
indicates how many wood goods tiles you take from the general supply. Move 
the wood goods indicator to the 0 space of the production wheel. 
Action Cut peat
Remove (maximum) 1 moor card from your landscapes. The 
production wheel indicates how many peat goods tiles you take 
from the general supply. Move the peat goods indicator to the 
0 space of the production wheel.
```

Source: [extracted/ora-et-labora-rules.txt, lines 335–345](../../../extracted/ora-et-labora-rules.txt#L335).

```text
Action Build a building
You may build an available building from the open display by paying the 
building costs, located in the upper left hand corner of the building card. 
(There are four different building materials: wood, clay, straw and stone.) 
Place the building card onto an empty landscape space. 
The building rules
• Important! Cloister buildings, recognizable by their 
yellow colored title and symbol boxes, must always be 
adjacent (horizontally or vertically) to other cloister buildings. 
• The landscape type a building card can be built on is indicated in the upper left 
hand corner of the card as well as in the illustration’s background color. There 
```

Source: [extracted/ora-et-labora-rules.txt, lines 183–190](../../../extracted/ora-et-labora-rules.txt#L183).

```text
The Action Options
Phase 4 of a round is the action phase. You have three options for this action. 
• You can place one of your own clergymen (prior or lay brother) or issue a work contract 
to another player: In that case, the other player must place one of his own clergymen. 
• You can fell trees or cut peat and take the corresponding production amount. 
• You can build a building. 
Action Place a clergyman in order to use a building 
You can either place one of your own clergymen (a lay brother or the prior) or request that 
```

Review status: pending independent audit.

## pandemic-legacy-season-0

[Pandemic Legacy: Season 0](../../../rules/pandemic-legacy-season-0.md): flight and team actions and Mop Up.

### Corrected rules

```diff
--- Original summary
+++ Corrected summary
@@ -37,24 +37,26 @@
 Each player turn has 5 steps:
 
 ### 1. Check Surveillance
-Check if your current city has enemy surveillance that affects your alias.
+If you start your turn in a city with surveillance, lose 1 cover per surveillance symbol (maximum 3). Ignore surveillance if there is a safehouse in your city.
 
 ### 2. Do 4 Actions
-Choose 4 actions from the available options:
+Choose up to 4 actions from the available options:
 
 | Action | Description |
 |--------|-------------|
 | **Drive/Ferry** | Move to a connected city |
-| **Direct Flight** | Discard a City card to fly to that city |
-| **Charter Flight** | Discard the card matching your city to fly anywhere |
-| **Shuttle Flight** | Move between cities with safe houses |
+| **Commercial Flight** | Reveal an Allied City card or discard a Neutral City card to move to its city; cannot fly to a Soviet city this way |
+| **Unrecorded Flight** | Discard the card matching your city to move to any city, including Soviet cities |
 | **Build Safe House** | Discard matching City card to place a safe house |
 | **Remove Agent** | Remove 1 agent from your city |
-| **Acquire Team** | Gain a team token for special abilities |
+| **Assemble Team** | At a safehouse, discard 5 City cards matching your city’s affiliation to place a team of that affiliation there |
+| **Drive/Ferry Team** | Move a team to an adjacent city; your pawn need not be with it |
+| **Identify Target City** | At a safehouse, discard 3 City cards matching the region of an unknown target objective to identify its city |
+| **Acquire Targets** | Resolve a target objective using an active team in the target city; follow the objective and debrief instructions |
 | **Share Knowledge** | Exchange City cards with another player in the same city |
 
 ### 3. Mop Up
-Resolve any end-of-action effects.
+Remove all agents in each city with an active team.
 
 ### 4. Draw 2 Player Cards
 Draw from the Player deck. If an Escalation card is drawn, escalation occurs.
```

### Rulebook evidence

Source: [extracted/pandemic-legacy-season-0-rules.txt, lines 146–158](../../../extracted/pandemic-legacy-season-0-rules.txt#L146).

```text
COMMERCIAL FLIGHT 
i1 
N 
This action varies as follows: 
 
Reveal an Allied City card in your hand to move to the 
matching city {revealed cards are not discarded). 
Discard a Neutral City card to move to the matching city. 
You cannot move to a Soviet city using the Commercial 
Flight action. 
UNRECORDED FLIGHT 
Discard the City card matching your city to move to any 
city on the board (including a Soviet city). 
```

Source: [extracted/pandemic-legacy-season-0-rules.txt, lines 178–179](../../../extracted/pandemic-legacy-season-0-rules.txt#L178).

```text
Note: Unlike Pandemic, there is no "Shuttle Flight" action (you cannot 
move directly from one safehouse to another). 
```

Source: [extracted/pandemic-legacy-season-0-rules.txt, lines 180–210](../../../extracted/pandemic-legacy-season-0-rules.txt#L180).

```text
IDENTIFY TARGET CITY 
While at a safehouse, discard 3 City cards matching 
your region to reveal an unknown target city of 
that region under an Objective card (see "Unknown 
Target Cities" to the right). 
For example, while in a safehouse in Africa, you may discard 3 Africa 
City cards to identify an unknown target city in Africa. This objective 
now has a known city. You must still complete the objective using the 
"Acquire Targets" action. 
ASSEMBLE TEAM 
f'l\lJ/1 
While at a safehouse, discard 5 City cards matching 
-\\ 1 
the affiliation of your city to place a team of that 
 affiliation there. 
If all af the teams of that affiliation are already on the board, you may 
relacate a team of that affiliatian from a different city to your city. 
DRIVE/ FERRY TEAM 
Move a team to an adjacent city. You do not have to be in 
-------► the city of the team you are moving. Multiple teams can be in 
the same city. Teams are not affected by surveillance (except 
through certain Incident effects). 
ACQUIRE TARGETS 
 Complete an objective with a known or unknown target city . 
'&J Remember to read the matching debrief entry . 
KNOWN TARGET CITIES 
To acquire targets in a known city, you 
must position an active team in the 
city shown on the card. Do the Acquire 
Targets action, mark the objective 
with a "Complete" token, and read its 
```

Source: [extracted/pandemic-legacy-season-0-rules.txt, lines 227–264](../../../extracted/pandemic-legacy-season-0-rules.txt#L227).

```text
UNKNOWN TARGET CITIES 
Certain objectives have an unknown 
target city. You must still position an active 
team in a specific city, but you do not 
know which. 
During the game, you can discover the 
target city through process of elimination 
or by using the Identify Target City action. 
@co.,,,.feted:ReadDabrieflll 
@Fail ... :ReadO.bria!mJ 
SETTING UP AN UNKNOWN TARGET CITY 
You find and set up objective cards with unknown target cities as you 
draw and resolve cards from the Legacy deck. To set up an unknown 
target city: 
.. Remove all City cards listed on the objective from the Player 
deck. Prologue Example: For the "Retrieve Proiect MEDUSA 
Sample" obiective, remove all the Europe City cards . 
• Randomly place one of those cards facedown under the 
Objective card without looking at it. This card is the 
target city . 
• ShufAe the remaining City cards back into the Player deck. 
ELIMINATING POSSIBLE TARGET CITIES 
When you draw a card from the Player deck 
that matches the region of an unknown target 
city, you eliminate that city as a possible target 
(it cannot be the City card under the objective). 
Use the tracking tokens to mark which cities have 
been eliminated. 
ACQUIRING TARGETS IN AN UNKNOWN CITY 
To acquire targets in an unknown city, you must position active teams 
in the city (or cities) you think might be the correct city. Then, do the 
Acquire Targets action and reveal the City card under the objective. 
If you have an active team positioned in that city, mark the objective 
with a "Complete" token. Otherwise, mark it with a "Failed" token. In 
either case, immediately read the appropriate debrief entry. 
Important! You can place teams in multiple possible cities to increase 
your odds. As long as there is an active team in the correct city, the 
objective is complete. 
```

Source: [extracted/pandemic-legacy-season-0-rules.txt, lines 287–290](../../../extracted/pandemic-legacy-season-0-rules.txt#L287).

```text

3. MOP UP
Your teams do what they were sent to do. 
Remove all agents in each city with an active team. 
```

Source: [extracted/pandemic-legacy-season-0-rules.txt, lines 135–142](../../../extracted/pandemic-legacy-season-0-rules.txt#L135).

```text
2. DO ACTIONS
Time is limited. You can't do everything you want. 
You can do up to 4 actions each turn. 
Select any combination of the following actions. You can do the same 
action several times, each time counting as 1 action. Your character's 
special abilities may change how an action is done. Some actions 
involve discarding a card from your hand; these discards go to the 
Player discard pile. 
```

Source: [extracted/pandemic-legacy-season-0-rules.txt, lines 130–134](../../../extracted/pandemic-legacy-season-0-rules.txt#L130).

```text
1. CHECK SURVEILLANCE
The Soviets are watching every minute of every day. 
If you start your turn in a city with surveillance, lose 1 cover for each 
surveillance symbol (®) in that city (max 3). 
Ignore this if there is a safehouse in your city. 
```

Review status: pending independent audit.

## pandemic-legacy-season-2

[Pandemic Legacy: Season 2](../../../rules/pandemic-legacy-season-2.md): exposure, plague placement, and Infection-deck exhaustion.

### Corrected rules

```diff
--- Original summary
+++ Corrected summary
@@ -35,32 +35,34 @@
 
 On your turn, perform these steps in order:
 
-### 1. Do 4 Actions
-Choose from available actions (see below).
+### 1. Check for Exposure
+If you start your turn in a location with one or more Plague cubes, gain one exposure.
 
-### 2. Draw 2 Player Cards
+### 2. Do 4 Actions
+Choose up to 4 actions from the available options (see below).
+
+### 3. Draw 2 Player Cards
 Resolve any Epidemics immediately. Discard down to 7 cards if over limit.
 
-### 3. Infect Cities
-Draw Infection cards equal to the infection rate. For each city drawn, remove 1 supply cube. If a city has no supply cubes, place an Incident marker (like an outbreak in Season 1).
+### 4. Infect Cities
+Draw Infection cards equal to the infection rate. For each city drawn, remove 1 supply cube. If a city has no Supply cubes, place a Plague cube and advance the Incident marker 1 space. If it already has 3 Plague cubes, resolve an outbreak instead of adding a fourth.
 
 ## Actions
 
 | Action | Description |
 |--------|-------------|
-| **Drive/Sail** | Move to an adjacent connected location |
-| **Direct Flight** | Discard a card to fly to the named city |
-| **Charter Flight** | Discard the card matching your city to fly anywhere |
+| **Drive/Ferry** | Move to an adjacent location connected by a line |
+| **Sail** | Discard a City card to move to its city along a sea route; both locations need anchor symbols |
+| **Charter Boat** | Discard the card matching your current city to move along a sea route to another location with an anchor symbol |
 | **Deliver Supplies** | Place supply cubes from your character card onto your current location |
-| **Pick Up Supplies** | Take supply cubes from your location onto your character card |
-| **Make Supplies** | Take 1 supply cube from the stockpile onto your character card (must be at a supply center) |
+| **Make Supplies** | Take 1 Supply cube from the stockpile onto your Character card; no supply center is required |
+| **Produce Supplies** | At a haven or supply center, discard a Produce Supplies card for Local Production or System-Wide Production (the latter is unavailable in the prologue) |
 | **Share Knowledge** | Give/take a City card matching your current city to/from another player in the same city |
 | **Build Supply Center** | Discard 5 cards of your city's color to build a supply center |
 | **Recon** | Discard specific cards at a supply center location to explore new areas of the world (reveal hidden map sections) |
 
 ### Free Actions
-- Transfer supply cubes between players at the same location
-- Play Event cards
+During the Do Actions step, before, between, or after paid actions, you may pick up any number of Supply cubes from your location or transfer supplies to or from a consenting player there. These free actions cannot interrupt another action. Event cards can be played at any time subject to their own restrictions.
 
 ## Scoring / Victory Conditions
 
@@ -68,20 +70,21 @@
 
 **Lose conditions:**
 - 8 incidents occur
-- Infection deck runs out
-- Player deck runs out
+- A player cannot draw 2 Player cards after their actions
 
 **Campaign structure:** Same as Season 1 -- win a month to advance; lose and get one retry before moving on. Each game ends with production units spent on upgrades.
 
 ## Special Rules & Edge Cases
 
-**Supply cubes vs. Disease cubes:** The core mechanic is inverted from Season 1. Instead of removing disease cubes, you add supply cubes to cities. When the infection deck draws a city, supplies are consumed (removed). Cities without supplies suffer incidents.
+**Supply cubes vs. Disease cubes:** The core mechanic is inverted from Season 1. Instead of removing disease cubes, you add supply cubes to cities. When the infection deck draws a city, supplies are consumed (removed). Cities without supplies gain a Plague cube and cause an incident; a city already containing 3 Plague cubes has an outbreak instead.
 
 **Recon:** This action lets players discover new parts of the world. Specific card combinations at supply centers unlock packages that reveal new map sections, cities, and game content.
 
-**Produce Supplies cards:** Special Player cards that, when drawn, allow a system-wide production phase where supply cubes are distributed to cities.
+**Produce Supplies cards:** Spend an action to discard one while at a haven or supply center. Local Production fills that location to its population. System-Wide Production fills all havens and supply centers to their populations, marks a checkbox, and destroys the card when its last box is filled. System-Wide Production is unavailable in the prologue.
 
-**Exposure:** Characters can become exposed to the plague under certain conditions, gaining exposure marks that carry forward between games.
+**Exposure:** At the start of your turn, gain one exposure if your location has one or more Plague cubes. Scratch the next exposure box, resolving any scar or skull revealed.
+
+**Infection deck exhaustion:** Reshuffle the exhausted Infection deck and advance the Infection Rate marker 1 space. If this changes the rate during the Infect step, finish drawing at the old rate.
 
 **Havens:** Starting locations on the sea that serve as safe bases of operations.
 
@@ -95,8 +98,9 @@
 
 | Phase | Action |
 |-------|--------|
-| 1. Actions | Perform 4 actions |
-| 2. Draw | Draw 2 Player cards; resolve Epidemics |
-| 3. Infect | Draw Infection cards; remove supply cubes from drawn cities |
+| 1. Exposure | Gain one exposure if your location has any Plague cubes |
+| 2. Actions | Perform up to 4 actions |
+| 3. Draw | Draw 2 Player cards; resolve Epidemics |
+| 4. Infect | Draw Infection cards; remove supplies or add Plague cubes and record incidents; resolve outbreaks at 3 Plague cubes |
 
 **Core difference from Season 1:** You ADD supplies to cities (good). Infection REMOVES supplies (bad). No supplies = incidents (like outbreaks).
```

### Rulebook evidence

Source: [extracted/pandemic-legacy-season-2-rules.txt, lines 662–666](../../../extracted/pandemic-legacy-season-2-rules.txt#L662).

```text
EACH PLAYER TURN IS DIVIDED INTO 4 STEPS:
1.	 Check for exposure.
2.	 Do 4 actions.
3.	 Draw 2 Player cards.
4.	 Infect cities.
```

Source: [extracted/pandemic-legacy-season-2-rules.txt, lines 688–691](../../../extracted/pandemic-legacy-season-2-rules.txt#L688).

```text
CHECK FOR EXPOSURE
If you start your turn in a location with 1 or more Plague 
cubes, gain an exposure (see Exposure, Scars, and 
Death on page 16). 
```

Source: [extracted/pandemic-legacy-season-2-rules.txt, lines 930–955](../../../extracted/pandemic-legacy-season-2-rules.txt#L930).

```text
is below the space of the Infection Rate track that has 
the Infection Rate marker. Flip these cards over one at a 
time, infecting the city named on each card.
To infect a city, remove 1 Supply cube from it and return 
it to the stockpile. If the city has no Supply cubes, 
instead place a Plague cube and record the incident (see 
Incidents, below). If the city already has 3 Plague cubes, 
do not place a 4th cube. Instead, an outbreak of the 
plague occurs in the city (see Outbreaks, next column). 
Discard this card to the Infection discard pile. 
RULE STICKER S
RULE STICKER T
 
In the rare case you get through the entire Infection 
deck, reshuffle it and move the Infection Rate marker 
forward 1 space on the Infection Rate track. If this 
causes the rate to change during the “Infect” step, use 
the old rate when determining how many cards to draw.
INCIDENTS
An incident happens whenever a Plague 
cube is placed into a location. Move the 
Incident marker forward 1 space on the 
Incident track. 
If the Incident marker reaches the 
last space (skull), the game ends 
and the players lose.
```

Source: [extracted/pandemic-legacy-season-2-rules.txt, lines 991–996](../../../extracted/pandemic-legacy-season-2-rules.txt#L991).

```text
turn after you win or lose, even if you would like to.
There are multiple ways for the game to end in a loss:
• Immediately when the Incident marker reaches 
the last space of the Incident track.
• If a player cannot draw 2 player cards after 
their actions.
```

Source: [extracted/pandemic-legacy-season-2-rules.txt, lines 943–947](../../../extracted/pandemic-legacy-season-2-rules.txt#L943).

```text
In the rare case you get through the entire Infection 
deck, reshuffle it and move the Infection Rate marker 
forward 1 space on the Infection Rate track. If this 
causes the rate to change during the “Infect” step, use 
the old rate when determining how many cards to draw.
```

Source: [extracted/pandemic-legacy-season-2-rules.txt, lines 1022–1029](../../../extracted/pandemic-legacy-season-2-rules.txt#L1022).

```text
It’s a dangerous world out there and characters will gain 
exposures. (One way is to start a turn in a location with 
a Plague cube. See page 10.)
When a character gains an exposure, scratch off the next 
box on the character’s exposure track (starting at the 
leftmost box). If there is nothing under the box, there is 
no immediate effect.
SCARS
```

Source: [extracted/pandemic-legacy-season-2-rules.txt, lines 688–698](../../../extracted/pandemic-legacy-season-2-rules.txt#L688).

```text
CHECK FOR EXPOSURE
If you start your turn in a location with 1 or more Plague 
cubes, gain an exposure (see Exposure, Scars, and 
Death on page 16). 
 
ATH
RULE STICKER F
 
DO 4 ACTIONS
After checking for exposure, you may do up to 4 actions 
and an unlimited number of free actions each turn.
```

Source: [extracted/pandemic-legacy-season-2-rules.txt, lines 696–708](../../../extracted/pandemic-legacy-season-2-rules.txt#L696).

```text
DO 4 ACTIONS
After checking for exposure, you may do up to 4 actions 
and an unlimited number of free actions each turn.
Select any combination of the actions listed below. 
You may do the same action several times, each time 
counting as 1 action (unless it’s a free action). Your 
character’s job and abilities may change how an action is 
done. Some actions involve discarding a card from your 
hand; all these discards go to the Player discard pile.
Free actions do not count toward your 4 actions 
per turn. Free actions must be done during the 
“Do 4 actions” step of your turn either before, between, 
or after any other actions that you take. You must 
```

Source: [extracted/pandemic-legacy-season-2-rules.txt, lines 709–722](../../../extracted/pandemic-legacy-season-2-rules.txt#L709).

```text
complete an action before starting another action.
MOVEMENT ACTIONS 
RULE STICKER G
Move to an adjacent location connected 
by a line.
Discard a card to move to the city named on 
the card, provided you can trace a sea route 
to it. (Both locations will have an anchor symbol.) 
Discard the City card that matches your current 
city to move to any location, provided you 
can trace a sea route to it. (Both locations will have an 
anchor symbol.) 
 You cannot do the Sail and Charter Boat actions 
over land. We hope you understand why.
```

Source: [extracted/pandemic-legacy-season-2-rules.txt, lines 724–744](../../../extracted/pandemic-legacy-season-2-rules.txt#L724).

```text
OTHER ACTIONS
Take 1 Supply cube from the stockpile and put 
it onto your Character card. You can hold any 
number of Supply cubes.
Discard a Produce Supplies card while in a 
haven or supply center to do the Produce 
Supplies action.
If you use its “Local Production” ability, 
fill your current haven or supply center to 
its population with Supply cubes. If the 
location already has Supply cubes equal to 
or above its population, do not place more.
If you use its “System-Wide Production” ability, fill 
all havens and supply centers on the grid to their 
population, then check a box on the card (you must still 
be in a haven or supply center). When the last check box 
is filled on the card, destroy the card.
If there aren’t enough Supply cubes in the stockpile to 
fill locations to their populations, put as many as you can 
in any order you like.
Put as many Supply cubes as you like from your 
```

Source: [extracted/pandemic-legacy-season-2-rules.txt, lines 146–148](../../../extracted/pandemic-legacy-season-2-rules.txt#L146).

```text
• You cannot do the Recon action.
• You cannot do System-Wide Production 
when you play Produce Supplies cards.
```

Source: [extracted/pandemic-legacy-season-2-rules.txt, lines 672–676](../../../extracted/pandemic-legacy-season-2-rules.txt#L672).

```text
Your hand can have City, Produce Supplies, and 
Event cards in it. City cards are used in some 
actions, Produce Supplies cards are used to bring 
supplies from the stockpile to havens and supply 
centers, and Event cards can be played at any time.
```

Source: [extracted/pandemic-legacy-season-2-rules.txt, lines 705–708](../../../extracted/pandemic-legacy-season-2-rules.txt#L705).

```text
Free actions do not count toward your 4 actions 
per turn. Free actions must be done during the 
“Do 4 actions” step of your turn either before, between, 
or after any other actions that you take. You must 
```

Source: [extracted/pandemic-legacy-season-2-rules.txt, lines 777–790](../../../extracted/pandemic-legacy-season-2-rules.txt#L777).

```text
These actions must be taken during the “Do Actions” 
step but do not count toward your 4 actions for the 
turn. Free actions cannot be used to interrupt other 
actions. For example, you cannot do the Pick Up 
Supplies action on the haven in the Mediterranean 
while using the Sail action to get from London to Cairo.
Take as many Supply cubes as you like 
from your location and put them onto your 
Character card.
Give as many Supply cubes as you like to 
a player in your location or take as many 
Supply cubes as you like from that player 
(with their permission). 
RULE STICKER I
```

Source: [extracted/pandemic-legacy-season-2-rules.txt, lines 728–744](../../../extracted/pandemic-legacy-season-2-rules.txt#L728).

```text
Discard a Produce Supplies card while in a 
haven or supply center to do the Produce 
Supplies action.
If you use its “Local Production” ability, 
fill your current haven or supply center to 
its population with Supply cubes. If the 
location already has Supply cubes equal to 
or above its population, do not place more.
If you use its “System-Wide Production” ability, fill 
all havens and supply centers on the grid to their 
population, then check a box on the card (you must still 
be in a haven or supply center). When the last check box 
is filled on the card, destroy the card.
If there aren’t enough Supply cubes in the stockpile to 
fill locations to their populations, put as many as you can 
in any order you like.
Put as many Supply cubes as you like from your 
```

Review status: pending independent audit.

## parks

[PARKS](../../../rules/parks.md): Campfire timing, Gear costs, First Hiker, scoring, and tiebreaker.

### Corrected rules

```diff
--- Original summary
+++ Corrected summary
@@ -39,7 +39,7 @@
 2. If the site has a Weather token, take it as a bonus.
 3. Perform the site's action.
 
-**Campfire rule:** If another Hiker (even your own) occupies a site, you cannot visit it UNLESS you flip your Campfire to the extinguished side. Your Campfire resets (re-lights) at the start of each season.
+**Campfire rule:** If another Hiker (even your own) occupies a site, you cannot visit it UNLESS you flip your Campfire to the extinguished side. Your Campfire relights immediately whenever one of your Hikers reaches Trail End.
 
 ### Season End
 A Season ends when all Hikers reach the Trail End. The player with the Camera may take a Photo at the reduced cost. Shuffle in one more Advanced Site for the next Season's Trail (making trails progressively longer).
@@ -65,7 +65,7 @@
 At Trail End, you may perform ONE of these:
 - **Visit a Park:** Spend the tokens shown on a face-up Park card to claim it.
 - **Reserve a Park:** Take a Park card to reserve for a future visit.
-- **Buy Gear:** Spend tokens shown on a Gear card to claim it and gain its ongoing ability.
+- **Buy Gear:** Spend Sunshine equal to the Gear card’s cost to claim it and gain its ability. At Trail End, the first Hiker to Buy Gear gets a 1-Sunshine discount; in 4+ player games, the first two Hikers get this discount.
 
 ### Wildlife Tokens
 Wildlife tokens are wild and can substitute for any other token when visiting Parks or taking Photos. They CANNOT be used in Canteens or for buying Gear.
@@ -82,8 +82,9 @@
 - Points from visited Park cards
 - 1 point per Photo taken
 - Points from your Personal Bonus (Year card)
+- 1 point for holding the First Hiker Marker
 
-**Highest total wins.** Tiebreaker: most unspent tokens.
+**Highest total wins.** Tiebreaker: most visited Parks. If still tied, share the win.
 
 ## Special Rules & Edge Cases
 
@@ -94,7 +95,7 @@
 - The Trail grows by 1 site each Season (new Advanced Site added).
 - Gear cards provide persistent abilities for the rest of the game.
 - At the end of the game, unvisited reserved Parks score 0 points.
-- The First Hiker Marker passes to the player who reached the Trail End first each Season.
+- The first Hiker to choose Reserve a Park at Trail End gains the First Hiker Marker.
 
 ## Player Reference
 
```

### Rulebook evidence

Source: [extracted/parks-rules.txt, lines 200–208](../../../extracted/parks-rules.txt#L200).

```text
CAMPFIRES • Sometimes, a Hiker is aleady at 
the Site you want to visit. To visit a Site that is 
occupied by another Hiker(s)—including your 
own—you must use your Campfire by flipping it 
over to the extinguished side. If your Campfire is 
extinguished, you cannot visit a Site occupied by 
another Hiker­—including your own. A player’s 
Campfire will relight when one of their Hikers 
reaches Trail End. 
```

Source: [extracted/parks-rules.txt, lines 216–219](../../../extracted/parks-rules.txt#L216).

```text
Trail End gives Hikers a moment to reflect on the journey. When a Hiker 
arrives here, the player immediately relights their Campfire if it is ex-
tinguished, and then chooses one of the available areas for their Hiker—
placing it vertically in the farthest right available slot of that area:
```

Source: [extracted/parks-rules.txt, lines 233–248](../../../extracted/parks-rules.txt#L233).

```text
BUY GEAR • Gear supplements your journey—giving extra benefits at Trail 
Sites or making it easier to visit certain Parks. To buy Gear cards, place your 
Hiker on the BUY GEAR area. Select one of the three available Gear cards on 
the board and turn in 
 Sunshine equal to its cost. All Gear cards have on-
going abilities, and some have an additional INSTANT action, activated one 
time immediately upon purchase. Place the Gear you acquire face up in front 
of you and utilize their ongoing abilities to their full potential. 
In a game of 3 or fewer players, the first Hiker to BUY GEAR, places their Hik-
er on the 
 slot without 4+ on it—this gives them a 1 Sunshine discount on 
their Gear purchase. After this, any number of other players may buy Gear, 
but do not receive the discount. In games with 4+ players, the slot farthest 
right is also available, so the first two Hikers to choose this option each re-
ceive a 1 
 discount on their Gear card.
```

Source: [extracted/parks-rules.txt, lines 227–232](../../../extracted/parks-rules.txt#L227).

```text
The first player to place their Hiker here also gains the 
 First Hiker Marker 
as a benefit by placing their Hiker in the far right slot. After this, any number 
of other players may still Reserve Parks here, but they do not gain the 
. The 
First Hiker Marker is worth 1 POINT at the end of the game. 
```

Source: [extracted/parks-rules.txt, lines 289–296](../../../extracted/parks-rules.txt#L289).

```text
When the fourth Season ends with its Photo opportunity, the 
game is over. All players reveal their Year cards, and then score 
points from their Parks, Photos, and Personal Bonus for their 
Year. The 
 also gives 1 Point to the player who has it.
The player with the most points at the end is the winner of 
Parks! If tied, the win goes to the player who visited the most 
Parks. If still tied, the win is shared.
```

Source: [extracted/parks-rules.txt, lines 220–232](../../../extracted/parks-rules.txt#L220).

```text
RESERVE A PARK • To Reserve a Park, choose one of the three available 
Parks on the board or draw the card on the top of the Parks deck. Place the 
Park card face up horizontally in front of you—keeping it separate from your 
vertically-stacked visited Parks. If a Park was reserved from a board slot, re-
veal a new Park from the Parks deck into the empty slot. When taking the Visit 
a Park action on a future turn, you may visit one of your reserved Parks or one 
of the three available on the board.
The first player to place their Hiker here also gains the 
 First Hiker Marker 
as a benefit by placing their Hiker in the far right slot. After this, any number 
of other players may still Reserve Parks here, but they do not gain the 
. The 
First Hiker Marker is worth 1 POINT at the end of the game. 
```

Review status: pending independent audit.

## project-l

[Project L](../../../rules/project-l.md): piece returns, Finishing Touches, penalties, and tiebreakers.

### Corrected rules

```diff
--- Original summary
+++ Corrected summary
@@ -47,26 +47,31 @@
 ## Actions
 
 ### Completing Puzzles
-When all spaces in a puzzle are filled with correctly colored pieces, the puzzle is complete.
-- Gain the new piece shown on the puzzle tile (take it from the reserve and add to your supply).
-- The puzzle is set aside for end-game scoring (points shown on the tile).
-- All pieces used to fill the puzzle return to the reserve.
+At the end of an action, a puzzle is complete when its recessed area is completely filled with pieces.
+1. Return all pieces from the puzzle to your personal supply.
+2. Take the reward piece shown on the puzzle from the reserve and add it to your personal supply.
+3. Set the completed puzzle aside for end-game scoring.
 
 ## Scoring / Victory Conditions
 
 ### Game End
 The game ends when the Black puzzle deck runs out. Complete the current round, then play one additional full round.
 
+### Finishing Touches
+After the final round, you may place any number of pieces from your supply into your puzzles, losing 1 point per piece placed. Make all these placements before resolving any completions, so pieces cannot be reused between puzzles during this step. Puzzles completed this way give no reward piece.
+
 ### Final Scoring
-- Each completed puzzle scores its printed point value.
-- Each unfinished puzzle scores 0 points.
-- The player with the most points wins. Tiebreaker: the player who went later in turn order.
+- Add each completed puzzle’s printed points.
+- Subtract each unfinished puzzle’s printed points.
+- Subtract 1 point per piece placed during Finishing Touches.
+- Highest score wins. Ties are broken by most completed puzzles, then most leftover pieces. If still tied, share the victory.
 
 ## Special Rules & Edge Cases
 
 - Maximum 4 unfinished puzzles at any time. You cannot take a new puzzle if you already have 4.
 - The Master Action can only be used once per turn.
-- Once a piece is placed in a puzzle, it cannot be moved or removed.
+- Once a piece is placed in a puzzle, it cannot be moved or removed until the puzzle is completed.
+- After the Black deck empties, each player may take at most 1 Black puzzle per turn; Black puzzles taken before the trigger do not count toward that turn’s limit.
 - If a level has no pieces remaining in the reserve when upgrading, take from the next available level.
 - When refilling puzzle rows, if the deck runs out, fill as many spots as possible.
 
```

### Rulebook evidence

Source: [extracted/project-l-rules.txt, lines 189–196](../../../extracted/project-l-rules.txt#L189).

```text
COMPLETING PUZZLES
At the end of an action in which the 
recessed area of a puzzle is completely 
filled with pieces, that puzzle is 
considered completed. Multiple puzzles 
may be completed with a single action. 
When you complete a puzzle, follow these 
steps in order:
```

Source: [extracted/project-l-rules.txt, lines 196–211](../../../extracted/project-l-rules.txt#L196).

```text
steps in order:
1 	 Return all the pieces from the puzzle 
to your personal supply. 
2 	 Take a new piece (as depicted on the 
puzzle) from the reserve and place it in 
your personal supply.
	
Note: If there are no pieces in the 
supply of the depicted type, take 
a piece of your choice from the next 
available level instead. 
3 	 Place the puzzle face down on your 
Victory Point pile to the left of your 
Player mat.
If you have any actions remaining after 
completing a puzzle, you continue with 
```

Source: [extracted/project-l-rules.txt, lines 239–268](../../../extracted/project-l-rules.txt#L239).

```text
action. For each piece placed this way, 
1 point is deducted from that player’s final 
score.
Note: You must perform all of your 
Finishing Touches before any of your 
puzzles are considered completed. i.e. 
you cannot complete one puzzle with 
a Finishing Touch and then use the pieces 
gained from that to perform additional 
Finishing Touches.
Also, completed puzzles at this time do 
not give any bonus piece.
Each player counts up their points as 
follows:
•	Total of the points on all the puzzles in 
your Victory Point pile. 
•	Deduct points for each incomplete 
puzzle, equal to its point value.
•	Deduct 1 point for every piece you placed 
during Finishing Touches. 
The player with the most points wins!
•	In case of a tie, the player who has 
completed the most puzzles wins. 
•	If there is still a tie, the player with the 
most pieces leftover wins. 
•	If there is still a tie, all tied players share 
the victory. You are all awesome! 
GAMEPLAY VARIANTS
There are more ways to play Project L – try 
the gameplay variants that are either in 
```

Source: [extracted/project-l-rules.txt, lines 180–181](../../../extracted/project-l-rules.txt#L180).

```text
a puzzle, it cannot be later moved or 
removed until that puzzle is completed.
```

Source: [extracted/project-l-rules.txt, lines 219–232](../../../extracted/project-l-rules.txt#L219).

```text
triggered, any Black puzzles taken are not 
replaced. Also, each player may now only 
take a maximum of 1 Black puzzle during 
their turn (this includes the player who 
triggered the end of the game, any puzzles 
they may have taken before the end of the 
game was triggered do not count towards 
this limit).
Known Victory Points
If you want to play a more strategic 
game, play with your Victory Point pile 
face up, so that everyone can see the 
points everyone else has scored. This 
should be agreed by all players before 
```

Source: [extracted/project-l-rules.txt, lines 189–211](../../../extracted/project-l-rules.txt#L189).

```text
COMPLETING PUZZLES
At the end of an action in which the 
recessed area of a puzzle is completely 
filled with pieces, that puzzle is 
considered completed. Multiple puzzles 
may be completed with a single action. 
When you complete a puzzle, follow these 
steps in order:
1 	 Return all the pieces from the puzzle 
to your personal supply. 
2 	 Take a new piece (as depicted on the 
puzzle) from the reserve and place it in 
your personal supply.
	
Note: If there are no pieces in the 
supply of the depicted type, take 
a piece of your choice from the next 
available level instead. 
3 	 Place the puzzle face down on your 
Victory Point pile to the left of your 
Player mat.
If you have any actions remaining after 
completing a puzzle, you continue with 
```

Review status: pending independent audit.

## quarriors

[Quarriors!](../../../rules/quarriors.md): five-phase turn, summoning costs, and empty-market game end.

### Corrected rules

```diff
--- Original summary
+++ Corrected summary
@@ -23,12 +23,11 @@
 
 ## Turn Structure
 
-1. **Score Creatures** in your Ready Area that survived since your last turn (+Glory).
-2. **Draw and Roll** 6 dice from your bag.
-3. **Ready Spells and Summon Creatures** from your roll.
-4. **Attack** opponents' creatures with your creatures.
-5. **Capture** one die from the Wilds by spending Quiddity.
-6. **Move to Used Pile** all dice in your Active Pool.
+1. **Score Creatures** in your Ready Area (+Glory); move scored creatures and attached spells to Used.
+2. **Draw, Roll, and Ready Dice**: draw and roll 6 dice, ready spells, and pay Quiddity to summon creatures.
+3. **Attack** opponents’ creatures with your creatures.
+4. **Capture** one die from the Wilds by spending Quiddity (optional).
+5. **Move Dice to Used**: clear your Active Pool and Spent Pile.
 
 ## Actions
 
@@ -39,7 +38,7 @@
 Draw 6 dice from your bag and roll them. This is your Active Pool. If your bag has fewer than 6 dice, draw what remains, move your Used Pile into your bag, then draw and roll the rest.
 
 ### Ready Spells and Summon Creatures
-Dice showing a creature or spell icon can be moved to your Ready Area. Spells may have immediate effects. Creatures enter play with their rolled attack and defense values.
+Spells showing their icon can be readied for free. To summon a creature showing its icon, pay Quiddity equal to its rolled level, then move it to your Ready Area with the rolled attack and defense values.
 
 ### Attack
 Total the attack values of all your summoned creatures. Each opponent totals their creatures' defense. Apply your attack to each opponent's creatures independently. If damage meets or exceeds a creature's defense, it is destroyed (sent to opponent's Used Pile). Excess damage carries over within each opponent's creatures.
@@ -58,7 +57,9 @@
 | 3 | 15 |
 | 4 | 12 |
 
-Score Glory when your creatures survive a full round (from your turn to the start of your next turn). First to reach the target wins immediately.
+Score Glory for creatures in your Ready Area at the start of your turn. Reaching the target wins immediately.
+
+The game also ends immediately if 4 or more Creature Power Cards in the Wilds are empty after a player captures a Quarry die. In that case, highest Glory wins; ties are broken by most dice in the Ready Area, then shared victory.
 
 ## Special Rules & Edge Cases
 
@@ -82,8 +83,7 @@
 | Phase | Action |
 |---|---|
 | 1. Score | Glory for surviving creatures |
-| 2. Draw & Roll | Draw 6 dice from bag |
-| 3. Summon | Ready creatures and spells |
-| 4. Attack | Total attack vs. each opponent |
-| 5. Capture | Buy 1 die from Wilds |
-| 6. Cleanup | All dice to Used Pile |
+| 2. Draw, Roll & Ready | Draw 6 dice; ready spells and pay to summon creatures |
+| 3. Attack | Total attack vs. each opponent |
+| 4. Capture | Buy 1 die from Wilds (optional) |
+| 5. Cleanup | Active Pool and Spent Pile dice to Used Pile |
```

### Rulebook evidence

Source: [extracted/quarriors-rules.txt, lines 158–166](../../../extracted/quarriors-rules.txt#L158).

```text
1. Score Creatures
2. Draw, Roll, and Ready Dice
3. Attack Your Rivals
5. Move Dice to Your Used Pile
Phase 4 is optional. You may skip this phase if you don’t want to take that action. The other phases are required: you cannot 
skip them even if you want to! 
So to review: Score your creatures. Roll dice, ready dice, roll some more dice, ready dice etc. Attack! Buy a die. Move dice from 
this turn to your Used Pile.
ON YOUR TURN
```

Source: [extracted/quarriors-rules.txt, lines 186–199](../../../extracted/quarriors-rules.txt#L186).

```text
Find the matching Power Card for each Creature in your Ready Area. The number in the top right corner of the Power Card 
tells you how much Glory you earn for that Creature. Move your marker forward on the Glory Track that many spaces. If you 
now have enough Glory to win the game, the game immediately ends and you win!
Next, you must move all Creature Dice (and Spells attached to them) from your Ready Area to your Used Pile.
Culling Dice
After scoring, you may choose to “cull” your collection. Each Creature that scores allows you to cull any one die from your 
Used Pile (including the Creature that just scored or any spells attached to it). When you cull a die, return it to the matching 
Power Card in the Wilds. That die is again available for any player to capture. You may only cull dice in your Used Pile. Culling 
dice allows you to modify your collection by removing dice you don’t want any more.
Example: Quinn starts his turn with one Creature in his Ready Area: a Strong Witching Hag. He scores 3 Glory for the Creature and moves it to his Used Pile. 
The Strong Witching Hag has an ability that allows Quinn to move a different Creature Die from his Used Pile to his Active Pool when the Strong Witching Hag 
scores. He chooses to move his Scavenging Goblin to his Active Pool (he will roll that die with the others in Phase 2). Then he decides to cull the Assistant Die 
from his Used Pile, returning it to the Wilds.
Phase 2: Draw, Roll, and Ready Dice
```

Source: [extracted/quarriors-rules.txt, lines 217–247](../../../extracted/quarriors-rules.txt#L217).

```text
used immediately after rolling your dice. Dice 
with Immediate Effects showing are never 
placed in your Ready Area.
Example: Quinn has rolled two dice with Immediate Effects, a Portal and an Assistant: His Portal Die shows a 
“Draw” symbol for 2 dice, so he spends the Portal Die (adding it to his Spent Pile) to draw 2 more dice from his bag, 
rolls them both, and adds them to his Active Pool.
Quinn’s Assistant Die allows him to re-roll the Assistant Die and any one other die. He picks up the Assistant Die 
and one of his Quiddity Dice and re-rolls them, returning both to his Active Pool. Note that if he rolled the re-roll 
effect on his Assistant Die again, he could use it a second time.
Remember: A player can choose the order which they resolve any Immediate Effects they rolled. If he wanted, Quinn could have 
used the Assistant effect before the Portal effect. The Immediate Effects do not occur simultaneously!
g g

Ready Spells and Summon Creatures
Once you are finished resolving your Immediate Effects, take 
a moment to look at the dice still in your Active Pool. You may 
move any Spell Dice showing the Spell Icon to your Ready 
Area. These dice become “Spells” that you can later cast (see 
“Spells” on page 8). You do not have to spend any Quiddity to 
ready your Spells.
Creature Dice that show a Creature Icon can be 
“summoned.” You must spend Quiddity equal to the Creature’s 
level (in the upper left corner of the die face) to summon it. 
Spend dice from your Active Pool to get the Quiddity you 
need. After spending the required Quiddity, move the die to 
your Ready Area. It is now a ferocious warrior, ready to attack 
your foes and earn Glory!
You can summon all the Creatures you want to summon 
during your turn, as long as you can pay the Quiddity costs. 
You can even summon some Creatures, resolve any special 
abilities, then summon some more.
```

Source: [extracted/quarriors-rules.txt, lines 317–335](../../../extracted/quarriors-rules.txt#L317).

```text
Phase 4: Capture One Quarry Die From the Wilds
After your attack phase is complete, you may spend any Quiddity you have left to capture one Quarry die from the Wilds. 
You are never required to capture dice. The cost (in Quiddity) of each die is shown in the upper left corner of the matching 
Power Card. Spend dice from your Active Pool to pay the required cost. In addition, you may have gained Quiddity from your 
Immediate Effects, Creatures, or Spells. You may also spend this Quiddity now. All Quarry dice you capture are added to your 
Used Pile. If there are 4 (or more) empty Creature Power Cards in the Wilds after you capture a Quarry die, the game ends 
(see “Winning the Game” below)!
Note: Some Creature abilities or Spell effects allow you to capture more than one die on your turn.
Example: Quinn has a lot of unspent Quiddity. Counting the bonus he received from the Scavenging Goblin’s ability and the Quiddity symbols on all of the dice 
left in his Active Pool, he has a total of 7 Quiddity! That’s enough to capture a Heavenly Seraph from the Wilds. Since Quinn can only capture one die each turn, 
if he had any Quiddity left over it would be lost.
Phase 5: Move Dice to Your Used Pile
It can be very useful to keep spells around for future turns, so choose carefully.
After you move the dice to your Used Pile, your turn is over. The player to your left can now begin their turn!
 WINNING THE GAME
The goal of the game is to earn Glory. The primary way to gain Glory is by summoning and 
protecting your Creatures until the scoring phase of your next turn. All Glory you gain is 
recorded on the Glory Track.
There are two ways that the game can end:
```

Source: [extracted/quarriors-rules.txt, lines 336–346](../../../extracted/quarriors-rules.txt#L336).

```text
1. If any player earns enough Glory to reach the goal shown on the chart to the right, the 
game immediately ends and that player wins!
Glory Goals
# of Players
Required Glory

2. If there are four or more empty Creature Power Cards (cards with no Quarry dice on them) after a player captures a 
Quarry die the game immediately ends. Only Power Cards that match the Creature Dice are counted: empty Spell Power Cards 
or Basic Resource Cards are not counted to determine if the game ends.
If the game ends because of empty Power Cards, the player with the highest Glory wins the game! If there is a tie, the tied 
player with the most dice in their Ready Area wins. If they are still tied, they share the victory!
```

Review status: pending independent audit.

## raids

[Raids](../../../rules/raids.md): sold Goods, Mjöllnir scoring, and tied victory.

### Corrected rules

```diff
--- Original summary
+++ Corrected summary
@@ -72,11 +72,12 @@
 - Coins collected during the game
 - Pennant tiles on your Longship
 - Rune tile sets
-- Goods remaining on your Longship
+- Sold Goods tiles beside your Longship, worth their printed Glory; unsold Goods still on your Longship score 0
+- Mjöllnir tiles: 1 Glory per Viking on your Longship for each simple Mjöllnir, or 2 per Viking for each double Mjöllnir
 - Harbor tile bonuses each Voyage
 - Defeating Monsters
 
-After 4 Voyages, total all Glory. The player with the most Glory wins.
+After 4 Voyages, total all Glory. The player with the most Glory wins; tied players share the victory.
 
 ## Special Rules & Edge Cases
 
```

### Rulebook evidence

Source: [extracted/raids-rules.txt, lines 395–405](../../../extracted/raids-rules.txt#L395).

```text
Simple Mjöllnir  
This tile gives you 1 
Glory point per Viking 
on your Longship at 
the end of the game.
Double Mjöllnir  
This tile gives you 
2 Glory points per 
Viking on your 
Longship at the end of 
the game. 
```

Source: [extracted/raids-rules.txt, lines 424–437](../../../extracted/raids-rules.txt#L424).

```text
△Scoring Glory points
There are many things that give you Glory points: 
Coins : Count the value shown on each Coin.
Runes : Score Glory points for each set of Runes you have, earning points 
for the number of Runes in each set.
Mjöllnirs : Score Glory points by multiplying the number 
of Mjöllnirs you have by the number of Vikings on your 
Pennants, Goods, and Monsters : Score Glory points 
as shown on each tile you have on or next to your 
Longship board. Exception: Goods tiles still on your 
Longship do not give you any Glory points.. 
After adding up all of your Glory points, the player 
with the most points wins the game. If there is a tie, 
both players share the victory. 
```

Review status: pending independent audit.

## rajas-of-the-ganges

[Rajas of the Ganges](../../../rules/rajas-of-the-ganges.md): final-stage timing and fame-gap tiebreaker.

### Corrected rules

```diff
--- Original summary
+++ Corrected summary
@@ -2,7 +2,7 @@
 
 ## Overview
 
-A dice-placement and worker-placement game set in 16th-century India. Players are Indian nobles (Rajas/Ranis) developing their province by constructing buildings, trading goods, and navigating the Ganges River. The game features two scoring tracks (fame and money) that advance toward each other -- when they meet or cross, that player wins immediately. Dice serve as workers and currency throughout.
+A dice-placement and worker-placement game set in 16th-century India. Players are Indian nobles (Rajas/Ranis) developing their province by constructing buildings, trading goods, and navigating the Ganges River. The game features two scoring tracks (fame and money) that advance toward each other -- when they meet or cross, the end of the game is triggered and the current stage is completed. Dice serve as workers and currency throughout.
 
 ## Components
 
@@ -52,9 +52,9 @@
 - **Fame track** (advances forward)
 - **Money track** (advances forward from the other end)
 
-**Immediate win:** The game ends immediately when a player's fame marker and money marker **meet or cross** on the tracks. That player wins.
+**Game end:** When a player’s fame and money markers meet or cross, finish the current stage. Players between that player and the current starting player may each place one more worker, if they have one, and resolve its action.
 
-If multiple players would cross simultaneously (unlikely), compare total advancement.
+If more than one player’s markers have crossed, compare the gap between their markers in fame points. The largest gap wins; if tied, the first player whose markers crossed wins.
 
 ## Special Rules & Edge Cases
 
```

### Rulebook evidence

Source: [extracted/rajas-of-the-ganges-rules.txt, lines 534–539](../../../extracted/rajas-of-the-ganges-rules.txt#L534).

```text
As soon as one player manages to have his fame marker and his money 
marker converge or pass each other, the end of the game is triggered. The 
current stage will still be completed – i.e., all players who are sitting between 
the player who has triggered the end of the game and the current starting 
player still have a chance to win and may place one more worker (provided 
they have any left) and carry out the applicable action.
```

Source: [extracted/rajas-of-the-ganges-rules.txt, lines 549–567](../../../extracted/rajas-of-the-ganges-rules.txt#L549).

```text
After that, players check who has won. If there are two or more players whose 
markers passed each other on their final turn, each of the players involved 
counts the difference of fame points between his money marker and his fame 
marker; the player with the most points wins the game. In case of a tie, the 
first player whose two markers passed each other wins.
(To find out who is second and third, etc., count the number of fame points 
that are still separating your fame marker from your money marker.)
on the river, and from the raja in the palace are good sources of money.
Such bonus spaces can get you extra dice as well. The palace also provides 
opportunities to obtain and exchange individual dice.
To fulfill the winning conditions, you need to establish a well thought-out road 
network within your province and gain as many special yields as possible. To 
this end, you will use the building action on the gameboard, for which you pay 
money and dice. Buildings in your province give you fame points; markets give 
you money.
Example: Rajesh’s money marker has passed his fame marker. His money marker is now on space 65 of the money track, his fame marker on space 30 
of the fame track. Then Leila has her final turn. She also manages to have her two markers pass each other. Her money marker ends up on space 52 of 
the money track, her fame marker on space 37 of the fame track. So Rajesh and Leila both have a difference of 2 fame points (it doesn’t matter where 
the money marker is). Since Rajesh was the first to have his two markers pass each other, he ekes out the win.
```

Review status: pending independent audit.
