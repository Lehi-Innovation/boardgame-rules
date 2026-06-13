---
title: "Arborea"
bgg_id: 371077
player_count: "1-5"
play_time: "60-120 min"
designer: "Caezar Al Jassar, Kuly"
source_pdf: "arborea-rules.pdf"
extracted_date: "2026-03-18"
summarized_date: "2026-03-18"
verification: "verified"
verification_date: "2026-06-13"
---
<!-- verification:begin -->
> ✅ **Verified** — this summary was fact-checked against the rulebook text and no significant issues were found.
>
> 📄 [Full rulebook text](https://jonnyallred.github.io/boardgame-rules/extracted/arborea-rules.txt) · 🚩 [Report a rules error](https://github.com/Lehi-Innovation/boardgame-rules/issues/new?template=rule-error.yml&labels=rule-error&title=%5BRule%20error%5D%20Arborea&game=arborea)
<!-- verification:end -->


## Overview

Arborea is a worker placement game with a time-based mechanism. Players are Patron Spirits guiding villagers to heal and regenerate a cataclysm-scarred landscape. You send villagers on pilgrimage tracks that advance over time, and when activated, villagers follow trails to regenerate biomes, complete ecosystem cards, train new villagers, and attract creatures. The player with the most Regeneration Points (RP) wins.

## Components

- Game board with 4 pilgrimage tracks
- 8 pilgrimage track tiles
- Ecosystem cards (multiple decks by biome requirement count)
- 6 borderland tiles
- 4 season tiles
- Biome tiles (6 types: tree, flower, mushroom, weed, sponge, water)
- Creature tokens
- Sun counters (time track)
- Per player: player board, 8 gift cubes, 2 elder villagers, 3 young villagers, 3 veteran villagers, spirit counter, season counters, RP counters, player aid

## Setup

1. Place board centrally. Randomly place 8 pilgrimage track tiles (2 per track) on outermost spaces.
2. Shuffle ecosystem decks separately; place by requirement count (fewest left, most right).
3. Randomly place 6 borderland tiles on column tops.
4. Randomly place 4 season tiles on season spots.
5. Place biome tiles on matching '0' spots of biome reserve.
6. Place creatures in outer regions.
7. Place sun counter on time track per player count.
8. Each player takes player board, components, starting ecosystem card, and a starting ecosystem task.
9. In reverse player order, each player sends 1 villager to a pilgrimage track and advances that track 1 step.

## Turn Structure

Turns are taken clockwise. Each turn has 4 steps:

1. **Pilgrimage:** You MUST either send a villager to a track OR advance a track 1 step. You may spend 3 spirit to do one of these a second time.
2. **Activate Villagers:** Activate up to 3 villagers waiting at trail beginnings. First 2 are free; 3rd costs 2 spirit.
3. **Complete Ecosystem Task:** You may complete 1 current ecosystem task if you have the required biomes.
4. **Update:** Update biome reserve and advance pilgrimage tracks. For each of your elder or young villagers on a pilgrimage track, advance that track 1 step. For each of your veteran villagers on a pilgrimage track, advance that track 2 steps.

The triggering player takes 2 sun counters when the sun counter reaches the last time track spot. At the end of their next turn they discard one counter, and at the end of the turn after that they discard the last counter, at which point endgame scoring begins.

## Actions

**Sending a Villager:** Place a villager from your supply onto a pilgrimage track square. If the square has a season icon, advance your matching season track. Cannot place on an occupied square.

**Advancing a Track:** Push the track tiles 1 step toward center. All players may take villagers off the track to place them at trail beginnings. After 4 total steps, the inner tile swaps to the start.

**Activating a Villager:** Follow the trail from beginning to end, collecting all rewards encountered:
- **Biome rewards (main reward):** Increase the **top half** of the corresponding biome tile on the reserve (max 8). The bottom half catches up during step 4, earning RP along the way.
- **Ecosystem rewards (main reward):** Take an ecosystem card as a current task (max 3 tasks).
- **Train villager rewards (main reward):** Move young/veteran villagers from reserves to supply.
- **Invite creatures (main reward):** Take a creature from the borderlands and place it on your invited creatures space, gaining spirit as shown on that creature's row.
- **Attract a creature (secondary reward):** Advance the sun counter one step and move a creature from the outer regions to the topmost empty spot on its borderlands column, gaining the printed reward (or the borderland tile reward if it is the first creature of that type attracted).
- **Water trail cost:** Before activating a villager on a water trail, you must spend between 2 and 6 spirit depending on the trail. You cannot activate a villager on a water trail if you cannot pay the required spirit cost.

**Villager Types:**
- **Elder villagers:** Return to your supply after activation and can be reused. Cannot use the bottommost sage reward.
- **Young villagers:** Return to their reserve after activation and must be trained again before reuse.
- **Veteran villagers:** Return to their reserve after activation and must be trained again before reuse. Advance pilgrimage tracks 2 steps (instead of 1) during step 4. Can use the bottommost sage reward.

**Completing Ecosystem Tasks:** Spend the required combination of biomes (reducing the top half of the reserve tiles) to complete a task card. The card joins your ecosystem grid, and you gain any listed rewards. Water is a wild biome that can substitute any other biome type, but only if that other biome's tile has already reached the '0' spot on the biome reserve.

**Creatures:** Placed on your ecosystem grid at intersections between 4 habitats. At game end, creatures score RP based on surrounding biome types and adjacent habitats.

## Scoring / Victory Conditions

**End-Game Scoring (in order):**
1. For each creature still in captivity, lose 3 spirit.
2. RP from your position on the spirit track (may be negative).
3. RP from season tiles (each tile checks its condition against your personal achievements, multiplied by your position on that season track, maximum 8 RP per tile).
4. RP from creatures placed in your ecosystem (based on surrounding habitats and creature-specific rules).

Gifts affect scoring indirectly: the Wiseowl creature scores 1 RP per every 2 gifts given, where a gift on the 2nd spot counts as 2 gifts and a gift on the 3rd spot counts as 3 gifts for this scoring. One season tile also scores 1 RP per gift given to sages (with gifts at spots 2 or 3 counting as 2 or 3 gifts respectively).

The player with the most RP wins. Tiebreakers in order:
1. Most creatures on ecosystem.
2. Most spirit.
3. Most advancement on season tracks.
4. Tied players share victory.

## Special Rules & Edge Cases

- Spirit is a limited resource; spending 3 spirit for extra pilgrimage actions or 2 spirit for a 3rd activation is powerful but costly.
- Biome reserve is shared among all players.
- You cannot discard ecosystem tasks once taken; choose carefully.
- When a villager reaches the last trails of a track, they must step off.
- Players may take villagers off tracks simultaneously, but can request turn-order resolution.
- Creatures in captivity at game end each cost you 3 spirit. When you invite at least one new creature in a turn, you may also place one captivity creature onto your ecosystem.
- Creatures score based on the specific habitats adjacent to their spot in your ecosystem.

## Player Reference

| Turn Step | Action | Cost |
|-----------|--------|------|
| 1. Pilgrimage | Send villager OR advance track | Free (2nd: 3 spirit) |
| 2. Activate | Activate up to 3 villagers | Free/Free/2 spirit |
| 3. Complete | Complete 1 ecosystem task | Required biomes |
| 4. Update | Update reserve; advance tracks 1 step per elder/young, 2 steps per veteran | Automatic |

| Biome Types | Icon |
|------------|------|
| Tree, Flower, Mushroom, Weed, Sponge, Water | Various |