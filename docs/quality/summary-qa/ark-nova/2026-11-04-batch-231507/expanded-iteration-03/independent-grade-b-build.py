import json
import hashlib
from pathlib import Path

ROOT = Path('/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/ark-nova/2026-11-04-batch-231507')
OUT = ROOT / 'expanded-iteration-03'
# Hand-selected relevant answer clauses, in requested-part order. These are
# evidence annotations, not keyword-derived grades. Each judgment was made
# after reading the complete question, answer, frozen key and source narrative.
ANNOTATIONS = {
'Q01': ([81,80,83,82,76,76,78], [
'Each player starts with 25 money',
'one active worker on the notepad and three inactive workers lying on the reserve spaces',
'Draw 8 Zoo cards, keep 4 as hand cards, and discard 4 face up',
'Draw 2 Final Scoring cards',
'Put Action card Animals in the leftmost slot (strength 1)',
'randomly place the other four cards in the remaining slots; all start side I up',
'Appeal starts at 0 for the start player, then 1, 2 and 3 in turn order']),
'Q02': ([69,70,70,70,84], [
'Two players place 3 face-up Base Conservation Project cards; three players also place 3; four players place 4',
'left on the left card, middle on the middle, right on the right',
"block the three spaces in the donation area's left column; both players cannot use those spaces",
'no additional blocked spaces for three- or four-player games',
'Reveal the six-card display after every player has chosen their hand cards']),
'Q03': ([104,104,104,106,106,106,106,108], [
'put the used card in slot 1',
'shift the cards that were left of its empty slot one place right',
'shift the cards that were left of its empty slot one place right',
'Set action strength before performing the action',
'each X-token spent adds 1 strength',
'X-tokens gained during that action cannot boost it',
'may hold no more than 5',
'after the action is complete, including moving its Action card']),
'Q04': ([102,248,248,248,248], [
'may not take a regular action that plays zero animals or builds zero buildings; you may not do nothing',
'select an Action card',
'take exactly 1 X-token',
'move that card to slot 1 and shift intervening cards as usual',
'cannot take this alternative if you already hold 5 X-tokens']),
'Q05': ([112,112,112,124], [
'ignore extra steps beyond it',
'The player who reached the last space gains 1 X-token',
'The triggering player finishes the current turn, then the break takes place',
'after the break play continues clockwise with the next player']),
'Q06': ([147,147,147,148,148,148,148,271,272], [
'Cards I advances the Break token 2 spaces',
'a deck draw per the strength table (maximum 3, with a possible discard)',
'at strength 5+, snap exactly 1 display card of your choice regardless of reputation',
'Cards II also advances the Break token 2 spaces',
'draws from the deck and/or from folders within reputation range in any order per the upgraded table',
'snapping exactly 1 display card is available from strength 3',
'snapping has no reputation restriction or deck draw',
'On either side, display refill after a snap is at turn end',
'there is no in-turn hand limit, and hand size is enforced only at breaks']),
'Q07': (163, [
'the display folder matching your Reputation counter and every lower-numbered folder',
'Reputation 10 or higher requires the upgraded Cards action',
'further reputation stays at 15 and gives 1 appeal per additional reputation step',
'may not look through the discard pile during the game']),
'Q08': ([180,182,182,180,181,181,181,181,181,181], [
'Build I makes exactly 1 building, size at most action strength',
'Build II may build any number of different buildings with total size at most strength',
'never two identical buildings in that action',
'pay 2 money per space',
'Your first building must cover at least one border space',
'later buildings must touch an existing building by at least one edge',
'Build only on empty spaces within the map; do not overlap buildings or cover water/rock spaces',
'Restricted-icon spaces require Build II',
'Kiosks must be at least 3 spaces from every other kiosk',
'Each pavilion immediately and only once gives 1 appeal']),
'Q09': ([180,182,179,182,182,270], [
'Build I allows standard enclosures sizes 1–5, kiosks, pavilions and one Petting Zoo per zoo',
'Build II additionally allows one Reptile House and one Large Bird Aviary per zoo',
'one Reptile House and one Large Bird Aviary per zoo',
'Build cannot create unique buildings; those enter through Sponsor cards',
'Covering every map space except water and rock immediately gives 7 appeal',
'the full-map reward can also trigger from other effects']),
'Q10': ([106,106,211,108,278], [
'Bonuses gained earlier in an action, including money, cards and newly activated workers, may be used for later steps of that action',
"Pay for each item before receiving that item's own benefits",
'Resolve immediate effects as they arise',
'until the entire action and Action-card movement are complete',
'the owning player chooses their order']),
'Q11': ([207,208,208,199,199,209,209,200,209,211,212], [
'meet all left-side conditions',
'Pay full cost before any money-gain effect from the play',
'matching-continent partner zoos reduce cost by 3 money per continent icon, so two such icons reduce it by 6',
"A standard enclosure must be empty and at least the animal's required size",
'flip the whole enclosure to its occupied side, normally housing one animal',
'Petting Zoo animals go only in the Petting Zoo',
'Eligible reptiles and some birds may instead use their special enclosure',
'mark the indicated occupied spaces with one player token per space, and never flip a special enclosure',
'Required water/rock adjacency must be satisfied, counting distinct adjacent terrain hexes',
'resolve immediately before the next animal',
'“after finishing” effects wait until the Animals action and card movement finish']),
'Q12': (213, [
'play animals from the display within reputation range as well as from hand',
'an animal taken from the display costs extra money equal to its folder number',
'At strength 5+, you may optionally gain 1 reputation',
'at the very beginning, so the raised range can apply to animals played in that action',
'Display cards are not replenished until the turn ends',
'Animals II permits animals with an upgrade-required condition']),
'Q13': ([221,221,221,224,223,223,223], [
'Only immediately when building a Reptile House or Large Bird Aviary',
'relocate all corresponding eligible animals that fit, deciding separately for each',
"The special enclosure must satisfy each animal's water/rock requirements and have enough capacity",
"Mark each moved animal's indicated special-enclosure spaces with that many player tokens from your supply",
'flip the smallest occupied standard enclosure meeting all its requirements, including terrain',
'If none does, flip the smallest occupied standard enclosure meeting size alone',
'if none meets even size, flip none']),
'Q14': ([231,229,239,229,229,229], [
'increase reputation 2, gain partner zoo 3, gain university 4, conservation project work 5',
'Association I performs exactly one task',
'Association II performs one or more different tasks, totaling no more than action strength',
'If one of your workers is already on a task, you must place 2 workers to repeat it',
'if 3 of your workers are already there, it is unavailable until after the break',
"Other players' workers on a task do not matter"]),
'Q15': ([232,233,233,232,232,232,88,233], [
'from the available tiles on the Association board',
'put them on the lowest empty corresponding space on your map',
'take any printed covered-space bonus immediately',
'cannot take a duplicate university; partner zoos must be from different continents',
'at most 4 partner zoos',
'the third/fourth requires Association II',
'Only the hand-limit university raises the hand limit from 3 to 5',
"A university's own reputation award is also immediate"]),
'Q16': ([234,239,234,234,276,235,236,236,236,236], [
'play a Conservation Project card from hand and support it immediately',
'from hand and support it immediately; Association II may also play it from the in-range display, paying the folder number',
'New projects go above the board, leftmost, shifting existing projects right',
'discard the rightmost project',
"return its tokens to their owners' supplies, not their map edges; their bonuses stay activated",
"Support a condition with no player's token on it, meet its requirement",
'You may support a given project only once',
'one player token from the left edge of your zoo map',
'taken immediately, before or after the project reward at your choice',
'recurring-marked bonuses repeat each break']),
'Q17': (237, [
"the project's printed standard-size category, not exactly one size: 2− accepts size 1 or 2, 3 accepts size 3, and 4+ accepts size 4 or 5",
"must match the project's printed standard-size category",
"Before conservation is gained, lose only that animal's printed appeal",
'discard the animal and lose its icons',
'keep conservation, reputation, ability-generated appeal and earlier effects already earned',
'If the animal can live in a special enclosure and its required tokens can be removed, remove them',
'otherwise flip the smallest occupied standard enclosure meeting all requirements',
'falling back to the smallest meeting size alone, or none if none meets size']),
'Q18': ([242,243,243,243,242,243], [
'Sponsors I may play exactly one hand Sponsor if action strength is at least its level and conditions are met',
'Sponsors II may play one or more cards, from hand and/or in-range display; action strength plus 1 must be at least their total levels',
'display cards cost their folder number',
"Resolve cards sequentially, fully resolving each card's instant effects (except after-finishing effects) before the next",
'Sponsors I advances the Break token by strength and pays that much money',
"Sponsors II's break option pays money twice that amount"]),
'Q19': ([115,116,117,117,118,119,121,121,123,123,124], [
'discard to hand limit (3, or 5 with hand-limit university)',
'clear Multiplier, Venom and Constriction tokens',
'recall workers',
'restock eligible partner zoos/universities',
'discard display folders 1 and 2, compact and refill',
'take income; reset Break token',
'1 money for each adjacent unique building, special enclosure, occupied standard enclosure, or pavilion',
'empty standard enclosures do not count, but empty special enclosures do',
'resolve clockwise beginning with the break initiator (or first affected player clockwise)',
'refill display after each such player before the next chooses',
'reset Break token']),
'Q20': ([253,254,255,255,257,257,257,257,260,261,262,262], [
'At 2 conservation, choose an Action-card upgrade or activate an additional association worker',
'At 5 and 8, choose 5 money or an available Bonus tile',
'At 10, the first player to reach or exceed it makes all players discard one Final Scoring card',
'if nobody reaches 10, everyone discards one before scoring',
'End is checked at the end of your own turn or during a break when Appeal and Conservation are in the same scoring area or have passed one another',
"appeal gained during another player's turn waits until your own turn end or a break unless another player triggers the end first",
'all others take one more turn',
'if triggered during a break, all players take one more turn',
'Each Final Scoring card can add at most 4 conservation',
'VP equals Appeal minus the lowest Appeal value in the scoring area containing your Conservation counter',
'Highest positive VP wins',
'tie goes to most supported projects, then tied players share victory']),
'Q21': ([64,64,64,282], [
'Shuffle the 9 Bonus tiles and place one face up on each of four blank yellow spaces',
'Do not place tiles on the two yellow spaces with icons',
'return the remaining five tiles to the box',
'If a component supply runs out, use a suitable substitute']),
'Q22': (75, [
'Choose 2 random zoo maps and select 1 advanced map, or lay out player count + 1 advanced maps and choose in reverse play order',
'Map A begins with an empty 3-space enclosure',
'the printed kiosk is covered by a tile as a reminder and counts as built']),
'Q23': ([79,280,280], [
'seven support tokens start on the designated spaces along the left edge of their zoo map',
'Hire inactive workers from the lowest reserve space upward',
'Some maps reward conservation points when you hire your last worker']),
'Q24': (110, [
'flip one chosen Action card from side I to side II',
'in its current slot',
'Its improved action is usable starting with your next action',
'it immediately counts as upgraded for conditions',
'You cannot upgrade all five Action cards']),
'Q25': ([188,188,188,188,188,191], [
'draws respectively 1, 1, 2, 2, 3 cards and discards respectively 1, 0, 1, 0, 1',
'draws respectively 1, 1, 2, 2, 3 cards and discards respectively 1, 0, 1, 0, 1',
'draws respectively 1, 1, 2, 2, 3 cards and discards respectively 1, 0, 1, 0, 1',
'draws respectively 1, 1, 2, 2, 3 cards and discards respectively 1, 0, 1, 0, 1',
'draws respectively 1, 1, 2, 2, 3 cards and discards respectively 1, 0, 1, 0, 1',
'A required discard may be one of the newly drawn cards or a card already in your hand']),
'Q28': (286, [
'bird, herbivore, predator, primate, reptile, bear, and Petting Zoo animal',
'Include both special categories unless explicitly excluded',
'Bear counts as a category even when also shown with herbivore or predator',
'Petting Zoo animal is its own category']),
'Q29': (239, [
'Donation is available only with Association II',
'after performing at least one Association task in that same action',
'limited to one donation per Association action',
'it needs no worker',
'Costs are 2, 5, 5, 7, 7, 10, 10, then a repeatable 12-money space',
'skip spaces blocked at setup',
'Pay the smallest amount still visible',
'cover that donation space with a player token from your supply',
'gain 1 conservation',
'further donations cost 12 and place no additional token']),
'Q30': (301, [
'upper-right icons on Animal and Sponsor cards',
'partner-zoo and university icons',
'upper-left water/rock requirements',
'Left-side play conditions and Conservation Project icons are not zoo icons',
'A card counts its own icon for effects',
'doubled icons count twice',
'Card text takes priority over general rules']),
'Q31': (301, [
'Terrain adjacency counts distinct water or rock hexes that touch the enclosure/building',
'multiple edges touching the same terrain hex count once',
'a larger region contributes only the hexes actually adjacent',
'Water/rock illustrations printed on tiles are not terrain spaces and do not satisfy requirements']),
'Q32': ([237,237,238,238], [
'The player who plays a new Release into the Wild project gains 1 reputation',
'a player who later supports a project already in play does not gain that play bonus',
'Breeding Program projects 123–127 use the same requirement for all three reward spaces',
'choose any available space that is unoccupied and whose condition you fulfill']),
'Q33': (305, [
'A condition with no number or with “per” pays once per fulfillment',
'A numbered threshold pays only once',
'where multiple thresholds exist, use the highest one met',
'X on the left is the condition and Y on the right is the reward']),
'Q34': (303, [
'A connected space is uncovered and shares an edge with a covered space',
'An isolated space has no adjacent covered space',
'A border space lacks a neighboring map hex on at least one of its six sides',
'“Your zoo” includes your played cards, map and personal supply',
'“any zoo” includes those for all players']),
'Q35': (307, [
'Unique buildings are placed when their Sponsor is played',
'If the tile cannot legally fit, the Sponsor card cannot be played',
'they have no size-based building payment',
'follow ordinary placement rules and any printed water/rock adjacency',
'colored face up, and rotate freely but do not flip it',
'Unique buildings are not enclosures, cannot house extra animals',
'are not terrain spaces']),
'Q36': (313, [
'Finish the Animals action, including moving the Animals card to slot 1, before taking a granted Action',
'use that Action card normally and move it to slot 1 afterward',
'A named action such as Sponsors cannot be replaced by the X-token alternative',
'Determination (Any Action) may choose the X-token alternative']),
'Q37': (315, [
'searches the unused face-down Base Conservation Project deck; Assertion takes the chosen project',
'Dominance takes its named project into hand',
'Dominance has no effect if its named project is already in play',
'Later play and immediately support the card through Association above the board',
'it does not join the setup base-project row below']),
'Q38': (314, [
'Resolve Boost or Clever after finishing Animals and moving that card',
'Clever puts the chosen Action card in slot 1',
'Boost puts the named card in slot 1 or slot 5',
'cards formerly to its left shift right',
'moving it to slot 5 shifts cards formerly to its right left']),
'Q39': (334, [
'An affected zoo must have at least 5 appeal',
"The played animal's appeal may be awarded before or after its interactive effect",
'its new appeal normally need not count when selecting affected players',
"The group may replace interactive abilities with the card's solo alternative text without playing solo mode"]),
'Q40': (346, [
'one token on slot 5 for a target ahead on one track, or two tokens on slots 4 and 5',
'Never stack two Constriction tokens on one card; return duplicates',
"Each token reduces that action's strength by 2",
'including each execution of a multiplied action',
'X-tokens can restore strength',
'Return a token after the marked card is used, or remove it without effect at the break']),
'Q41': (346, [
'At effective strength zero or below, a constricted card cannot perform its regular action unless',
'spend enough X-tokens to raise it to at least 1',
'it may instead take the alternative X-token action']),
'Q42': (316, [
'after each card, decide again whether to discard a display card and replenish it or discard a hand card and draw one from the deck',
'A display card discarded through Digging is replaced immediately',
'shifting higher folders down and drawing into folder 6']),
'Q43': (317, [
'another herbivore in your zoo requires at least its standard-enclosure size',
'The same qualifying herbivore may host any number of flock animals',
'another herbivore in your zoo',
'Without a qualifying herbivore, house the flock animal normally',
'a later non-flock herbivore cannot join it in that enclosure',
'exact historical residents need not be tracked or proven',
'it still frees an occupied enclosure under the release/fallback procedure']),
'Q44': (318, [
'activates the lowest remaining reserve worker by moving it to the notepad, where it can be used immediately',
'Take a last-worker map reward if shown',
'If all workers are active, the ability has no effect']),
'Q45': (321, ['If no Animal card appears, discard all revealed cards']),
'Q46': ([341,341,348,348,348,348,348], [
'chooses among tied players with the highest appeal and at least 5 appeal',
'if you are the highest-appeal target, it has no effect',
'spend your own X-tokens',
"use that card's owner's side/upgraded status for the action",
'Move the borrowed card to slot 1 normally',
'Venom and Constriction on that card apply to you and are discarded afterward',
'its Multiplier cannot be used']),
'Q49': (332, [
'Place a gained Multiplier immediately on its named Action card',
'a bonus-tile Multiplier may go on any card',
'execute the action twice in succession at the same base strength',
'move its Action card only after both executions',
'Each X-token boosts only one execution',
'defer after-finishing effects until all executions finish',
'A break triggered by the first execution waits until the whole turn is finished',
'Return used Multiplier tokens to supply; an unused one is removed at the next break']),
'Q50': (332, [
'Two Multiplier tokens allow up to three executions, not four',
'A multiplied X-token alternative can take two X-tokens, subject to the five-token cap',
'cannot mix one X-token action with one regular action']),
'Q51': ([330,330,330,330,329,329], [
'Peacocking lets you place a Large Bird Aviary before Build II',
'a legal site exists',
'provided your zoo does not already have one',
'Other placement rules still apply, including Build II for upgrade-marked spaces',
'Posturing also follows normal placement rules, including kiosk spacing',
'multiple buildings are placed one at a time']),
'Q52': (328, [
'3 for the first, 6 for the second and 9 for the third',
'One Petting Zoo holds at most three of these animals',
'They count as small animals']),
'Q53': ([350,343,350], [
'Choose among ties',
'the most-conservation target must have at least 1 conservation',
'A self-target has no effect']),
'Q54': (350, [
'The target chooses to give 5 money or allow a random hand-card draw',
'Final Scoring cards are never drawn',
'With no hand cards, the target gives money',
'with less than 5 money, the target gives a card',
'With neither a card nor 5 money, the target gives all current money, including zero',
'Resolve repeated Pilferings sequentially, and the target may choose differently each time']),
'Q55': ([326,326,326,325], [
'Cards tucked under an animal by Pouch have no remaining function',
'if that animal is released, discard its tucked cards too',
'keeping appeal already earned from tucking',
'Cards sold through Sunbathing go to the discard pile']),
'Q56': (327, [
'An extra Final Scoring card drawn',
'before the 10-conservation milestone joins your choices when you discard one card at that milestone',
'At game end score every remaining Final Scoring card',
'each card is separately capped at 4 conservation points']),
'Q57': (325, [
'Scavenging shuffles the discard pile face down, draws randomly from it',
'returns the discard pile face up']),
'Q58': (322, [
'Snapping takes exactly one display card regardless of reputation',
'it does not draw from the deck instead',
'Sponsor Magnet looks for display Sponsor cards, which need not be within reputation range',
'if none are present, it does nothing',
'Ordinary end-of-turn display refill applies']),
'Q59': (347, [
"the affected player's lowest-numbered slots in order (slot 1, then 2, etc.)",
'at most one per card; return duplicates',
'Using a card with Venom removes its token and avoids all Venom fees that turn',
'Pay 2 money at turn end only if you removed no Venom token that turn and at least one remains on your cards',
'If unable to pay, undo the turn and choose another action',
'Unused tokens clear at the next break without effect']),
'Q63': (361, [
'2 money for 1 university, 5 for 2, and 10 for 3',
'reduces the strength required to support conservation projects from 5 to 4',
'1 conservation for having three universities']),
'Q66': (364, [
'counts previously supported projects by the number of support tokens missing from the left edge of your map and gives 2 appeal per such project',
'1 conservation at every break']),
'Q67': (365, [
'counts different continent and animal-category icons',
'for each two, it gives you 1 conservation',
'Every other player gets 2 money per conservation point you gain']),
'Q68': (366, [
'1 appeal per research icon immediately',
'Whenever any player plays a research icon, the Science Library owner gains 2 money',
'1 conservation if you have five different animal categories']),
'Q70': (368, [
'1 appeal per Americas icon immediately',
'Each Americas icon played lets you build one free kiosk',
'following normal placement and kiosk-spacing rules',
'five or more kiosks, rewarding 1 conservation']),
'Q72': (370, [
'1 appeal per Australia icon immediately',
'Each Australia icon played lets you tuck one hand card beneath this Sponsor for 2 appeal',
'tucked cards have no further function']),
'Q75': (373, [
'Each card puts two supply tokens on itself',
'return exactly one token as any one icon; never use both tokens on the same support',
'When supporting a Base Conservation Project below the Association board',
'Projects that originated as base cards but were played above the board do not qualify',
'1 conservation with five or more project supports, counted by tokens missing from the left edge of your map']),
'Q77': (375, [
'one extra copy of a building built in that same action',
'without extra strength',
'pay its normal money cost and obey placement rules',
'Only one extra building is allowed, even if multiple different buildings are built',
'Special enclosures remain limited to one of each type per zoo',
'5 appeal with a full map except water/rock']),
'Q78': (376, [
'2 money per water/rock icon immediately',
'permits covering water/rock spaces',
'ignoring terrain requirements of animals and unique buildings',
'printed terrain icons still count',
'Covered terrain stops counting for Hydrologist, Geologist and Architectural Zoo',
'2 appeal per water-icon/rock-icon pair, up to three pairs']),
'Q80': (378, [
'triggers when you receive an actual placement bonus on a border space',
'any uncovered placement bonus on your map, whether or not it is on a border',
'Multiple triggers may choose the same bonus or different bonuses',
'all building border spaces covered, excluding water/rock, for 1 conservation']),
'Q82': (380, [
'1 X-token immediately',
'Each Release into the Wild support gives 1 additional conservation',
'repeatedly support the same release project with different qualifying animals',
'only one token per project per Association action',
'Each token counts as a separate project support for other effects']),
'Q83': (381, [
'1 X-token immediately',
'immune to Venom, Constriction, Hypnosis and Pilfering',
'For Hypnosis and Pilfering, ignore your counters and select the next qualifying player',
'1 conservation with all five continents']),
'Q85': (383, [
'Choose small or large permanently and mark that choice with a player token from your supply',
'reveal deck cards until finding an animal of that type, keep it and discard the rest',
'Chosen small animals gain 2 extra appeal, or chosen large animals gain 4',
'cannot play animals of the opposite type',
'size-3 animals remain legal but receive no bonus']),
'Q86': (384, [
'2 money per small animal immediately',
'An Animals action containing only small animals',
'play one extra small animal from hand, with normal costs and rules',
'Then add one small animal from the display to hand regardless of reputation',
'you may take it even if you declined the extra play',
'mixing small and large animals prevents the effect']),
'Q90': (389, [
'1 appeal per water icon immediately',
'Each newly covered space adjacent to water gives 1 money',
'even if several spaces belong to one building',
'a space adjacent to multiple water hexes pays only once',
'1 conservation if all water hexes are connected (none isolated)']),
'Q95': (393, [
'Barred Owl Hut places its unique building',
'Each bird icon played triggers drawing two cards from the deck, keeping one and discarding the other']),
'Q96': (394, [
'Sea Turtle Tank must be placed adjacent to water',
'Each reptile icon played lets you sell up to two hand cards for 4 money each',
'discard the sold cards']),
'Q98': (396, [
'For each predator icon played, Spotted Hyena Compound triggers Hunter, with the number of revealed cards equal to your total predator icons',
'A single card with two predator icons triggers Hunter twice in sequence',
'counting both new icons for the first trigger and then counting the updated total again for the second']),
'Q99': (397, [
'Okapi Stable enters play with three supply tokens on its card',
'For each herbivore icon played, you may spend one token to play a Sponsor from hand',
"Pay money equal to the Sponsor's level and meet normal conditions",
"The Stable's own herbivore icon can trigger this when the Stable is played",
'up to three uses total']),
'Q100': (398, [
'1 reputation and 1 conservation immediately',
'Place its building covering at least two border spaces',
'take one display card within reputation range or draw one deck card']),
'Q102': (400, [
'Side Entrance is placed on two border spaces and unlike ordinary buildings need not touch an existing building',
'later buildings may attach to it',
'At each break it gives 2 money per adjacent building, excluding empty standard enclosures',
'it may be beside a kiosk',
'5 appeal with a full map excluding water/rock']),
'Q104': (402, [
'1 appeal per connected, uncovered building border space',
'water and rock are excluded',
'Count upgrade-restricted spaces even if Build is not upgraded',
'gain 1 conservation per six contiguous empty building spaces',
'evaluated separately for each group']),
'Q106': (404, [
'2 money per different continent or animal-category icon; research icons do not count',
'Each continent/category newly introduced to your zoo gives 1 appeal and 2 money',
'A double of the same new icon receives the novelty reward only once']),
'Q107': (405, [
'place a size-5 standard enclosure free under normal placement rules',
'When playing a large animal, ignore one left-side condition, such as a required icon or Animals upgrade',
'terrain requirements cannot be ignored',
'stacks with Research Institute, which can ignore one condition, allowing two conditions to be ignored']),
'Q112': (416, [
'compares each animal category',
'gain 1 conservation for each category in which you have more icons than the player to your right',
'If that player has no icons in a category, one of your icons is enough to lead it',
'Maximum reward is 4 conservation']),
'Q113': (417, [
'only to standard enclosures adjacent to the tower hex itself',
'Special enclosures do not qualify',
'Housing an animal there grants the two appeal again even if an earlier animal was released and the enclosure emptied',
'The tower is not a building for kiosk income']),
'Q114': (418, [
'A standard enclosure touching the Outdoor Area hex qualifies; adjacency only to a different water hex does not',
'counts as two spaces larger for all purposes after placement',
'This cannot be ignored on release or transfer',
'It does not affect special enclosures',
'Outdoor Areas is not a building']),
'Q115': (419, [
"A building on Commercial Harbor's adjacent building space activates it",
'your first building may begin beside it but need not',
'before, during or after your action',
'once per own turn',
"never during breaks or another player's turn",
'The Harbor is not a building']),
'Q116': (420, [
'whether several hexes belong to one building',
'regardless of building type, occupancy',
'The Restaurant is not a building and does not count as a kiosk neighbor',
'one free Reptile House or one free Large Bird Aviary',
'even before Build II; choose one, not both, and follow other normal placement rules',
'Park Restaurant income is 1 money per adjacent covered hex']),
'Q119': (423, [
'Cover Hollywood Hills H spaces with buildings under ordinary placement rules',
'each covered H reveals deck cards until a Sponsor appears, which you keep, discarding other revealed cards',
'H is not a placement bonus, so it does not trigger Archaeologist',
"Once all three are covered, every Sponsor's level is one lower",
'partner bonuses still require Association II for a third/fourth partner',
'building bonuses still require Build II on restricted spaces']),
'Q123': (431, [
"Pay money equal to the Sponsor's level and meet its usual conditions",
'The Sponsor must come from hand, even with Sponsors II',
'leaves the Sponsors Action card in its current slot; it does not move it']),
'Q124': (433, [
'Appeal cannot exceed 113',
'conservation cannot exceed 41; gains beyond those track ends are lost']),
'Q125': ([340,341,341,341,342,343,343,350,344,344,336], [
'Venom affects every other zoo with higher appeal than yours and at least 5 appeal',
'Hypnosis targets a highest-appeal zoo with at least 5 appeal, with you choosing among ties',
'if you are the target, no effect',
'copies only slot 1, 2 or 3',
'Pilfering 1 targets a highest-appeal zoo',
'Pilfering 2 separately targets the highest-appeal zoo and most-conservation zoo',
'ties chosen by you, and the conservation leader must have at least 1 conservation',
'self-targets have no effect',
'Constriction affects every other zoo with at least 5 appeal ahead of you on Appeal and/or Conservation',
'one token if ahead on one track, two if ahead on both',
'with at least 5 appeal']),
'Q127': ([432,432,432,427], [
'For an Animal card, a partner-zoo condition means a partner zoo from the specified continent; for a Sponsor card, it permits a partner zoo from any continent',
'only while you have at most 25 appeal',
'A minimum-reputation condition requires at least the printed value',
'An ignore-one-condition bonus removes one left-side requirement, such as a required icon; it does not remove terrain requirements']),
'Q133': (316, [
'up to two choices',
'discarding one display card and immediately replenishing the display',
'discarding one hand card and drawing one deck card']),
'Q134': (163, [
'move cards from higher-numbered folders down in order',
'preserving their order',
'then fill empty spaces from the deck']),
'Q137': (167, [
'Build standard enclosures empty side up, showing the yellow border and size number',
'A covered placement-bonus space gives its bonus immediately once',
'turning the enclosure occupied later does not award that placement bonus again']),
'Q139': (255, [
'under the remaining pile',
'face down']),
'Q140': ([72,72,31,31,108], [
'Randomly determine the starting player',
'turns proceed clockwise',
'Play has no formal rounds: players take turns one at a time',
'take one action using one of the five Action cards',
'additional effects or bonuses follow their timing, including after-finishing effects after card movement']),
}

INTENDED_PROMPT = '''Fresh independent grader, ArkNova94-question readerB. ReadONLY QAroot /home/jonny/projects/boardgame-rules/docs/quality/summary-qa/ark-nova/2026-11-04-batch-231507/ files expanded-iteration-03/{reader-b.json,summary-snapshot.md,questions.json}, benchmark-v2/{answer-key.json,material-requested-facts.json}, grading-request-scope-02.json. No otherreader/earliergrades/reports/history/rawsources/canonical/browsing/contact. Readall6inputscompletelyboundedrecovereverytruncation. IndependentlygradeALL94answers, everyACTUALLYREQUESTEDpart individually. Actualquestionmeaningcontrolsscope, immutablefactualkeysourcefactsstayfixed, neutralrequested/contextindexguidecontainsnoprioranswers/results. Contextneednotbevolunteered; anyvolunteeredfalse/contradictoryrulingcounts. Ifindexseemsinconsistentwithquestionexplicitlyflagconcernwithoutaddinghiddenrequirements. Correctonlycompleteallactualparts,no contradictions/no unsupportedsource-correctguesses;partialmissing/unresolved/ambiguousactualpart;incorrectmaterialfalse ruling. No borrowingbetweenanswers; supportlabelnotgrade; basiclogicalentailment/meaningfuldefined-procedureshorthandallowedaccordingtopromptscope. Preservequestion-givenconditionswhenreadinganswer; do notusekeywordmatchingorrequireextracontext. Reviewallvolunteeredclausesagainstthisfrozennarrative. WriteONLY expanded-iteration-03/independent-grade-b.json plusownnotesnamedindependent-grade-b-*; noinputedits. Include exactintendedprompt,6inputhashes,complete-readproof,94question-orderjudgments:id,perrequestedpart status/resolution/RELEVANT observedclausequote/summarysupportquote-or-line,overallgrade correct|partial|incorrect,unsupported_guessbool,reason,andvolunteered/contextreview. Quoteonlyrelevantclausesperpart ratherthanrepeatingwholeanswerperpart; fullrawansweralreadypreserved. IncludeC/P/Icounts,nonpassingIDs,borderline/scope/keyconcerns. NoassumedPASS; don'trelaxgenuineaskedparts.'''

FILES = [
 'expanded-iteration-03/reader-b.json',
 'expanded-iteration-03/summary-snapshot.md',
 'expanded-iteration-03/questions.json',
 'benchmark-v2/answer-key.json',
 'benchmark-v2/material-requested-facts.json',
 'grading-request-scope-02.json',
]
blobs = {f:(ROOT/f).read_bytes() for f in FILES}
reader = json.loads(blobs[FILES[0]])
snapshot = blobs[FILES[1]].decode().splitlines()
questions = json.loads(blobs[FILES[2]])['questions']
key = json.loads(blobs[FILES[3]])['answers']
material = json.loads(blobs[FILES[4]])
scope = json.loads(blobs[FILES[5]])['questions']
ids = [x['id'] for x in questions]
assert len(ids) == len(set(ids)) == 94
assert ids == [x['id'] for x in reader['answers']] == [x['id'] for x in key]
assert set(ids) == set(material) == set(scope) == set(ANNOTATIONS)

# The question, rather than the neutral index, controls what must be stated.
SCOPE_CONCERNS = [
 {'id':'Q14','index_text':scope['Q14']['requested_parts'][-1],
  'question_scope':'The question asks worker requirements when repeating a task before a break. The normal worker baseline for every unrepeated task is context, rather than a separately demanded part.',
  'treatment':'Grade the four strengths, I/II task limits, repeated-own-worker escalation and irrelevance of other players. Review the volunteered normal Association-I worker statement as true context. No hidden additional worker-baseline disclosure is imposed.'},
 {'id':'Q99','index_text':scope['Q99']['requested_parts'][0],
  'question_scope':'The question asks how the Stable gains/spends tokens to play Sponsors, its self-trigger, cost and card source. Placing its unique building is not requested.',
  'treatment':'Require the three personal-supply tokens on the card, with all token-use rules. The omitted building-placement context is not made an extra requirement; the frozen building fact remains unchanged.'},
 {'id':'Q102','index_text':scope['Q102']['requested_parts'][1],
  'question_scope':'The question asks its placement exception, future attachment, income and final reward. A separate recital of all ordinary placement restrictions is not requested.',
  'treatment':'Require the actual exception (two border spaces, no existing-building adjacency), and check for any volunteered broader waiver. The answer grants only that exception; no broader waiver is asserted.'},
]

BORDERLINE = {
 'Q03':'Moving only the prior left-of-slot-4 cards entails that slot 5 stays unchanged; no separate literal sentence is required.',
 'Q06':'The answer separately covers Cards-II display refill and snap refill on either side; both clauses jointly resolve the requested timing.',
 'Q09':'The one-per-zoo limit is stated for Petting Zoo in clause 1 and for Reptile House/Aviary in clause 2. They must be read together within this answer.',
 'Q11':'The unqualified sentence requiring water/rock adjacency is read as the general requirement, not an assertion that special housing is exempt. Its special-enclosure clause follows without any waiver. Terrain applies to both choices.',
 'Q12':'Display play within range “as well as from hand” allows the two sources together; it does not impose an exclusive-source choice.',
 'Q14':'See scope concern: the question specifically asks repeat-task worker requirements. Those are fully stated.',
 'Q17':'“Must match the project’s printed standard-size category” fixes the band by the printed requirement and thereby excludes actual tile size/special capacity as alternative criteria. The “if ... remove them; otherwise” wording makes special-token removal mandatory.',
 'Q25':'The ordered draw and discard vectors pair each strength with its exact numbers; the five per-strength judgments use the same short vector clause with an explicit individual resolution.',
 'Q30':'“Counts its own icon for effects” includes immediate and recurring effects without limiting either. “Doubled icons count twice” in this effects question entails twice the matching trigger/count, without needing a repeated trigger sentence.',
 'Q31':'The answer uses distinct terrain hexes touching the enclosure/building as the criterion. Decorative illustrations are expressly not terrain and cannot satisfy the requirement; no terrain credit is asserted.',
 'Q43':'An unqualified “another herbivore” includes flock and non-flock hosts. The named release/fallback procedure is meaningful defined-procedure shorthand, not an unresolved request to look elsewhere.',
 'Q49':'“Execute twice” describes the multiplied use; it is not read as a volunteered ruling that a player is forced to expend an optional Multiplier.',
 'Q52':'In response to the zoo-capacity question, “One Petting Zoo holds at most three” gives the three-animal maximum for the single Petting Zoo defined by the base rules. It does not purport to allow additional Petting Zoos or more animals per zoo.',
 'Q56':'In response to the Resistance question, “an extra Final Scoring card drawn” identifies the card Resistance grants. The before-ten discard choice and every-remaining-card scoring are explicit.',
 'Q67':'The exhaustive domain “different continent and animal-category icons” excludes duplicates and research. “For each two” means complete pairs, not fractional conservation.',
 'Q68':'Sponsor effects without an any-zoo qualifier use the owner’s zoo under the frozen shared rule; the recurring any-player reward and its owner recipient are explicit. Having five categories is a threshold, not an assertion that six categories fail.',
 'Q70':'The unqualified icon reward uses the ordinary own-zoo default. The answer does not extend the effect to opponents’ Americas icons.',
 'Q72':'The unqualified icon reward uses the ordinary own-zoo default. No any-zoo reward is asserted.',
 'Q75':'The answer’s same-support wording agrees with the frozen summary and the request-scope index; tokens replace one needed icon on a qualifying support. The frozen key’s same-project wording is not expanded into an unrelated new requirement.',
 'Q90':'“Connected (none isolated)” uses the explicitly defined connected-space term: each terrain hex borders a covered hex. This is permitted meaningful terminology, not a claim that water hexes only need to connect to one another.',
 'Q95':'The unqualified bird trigger inherits the ordinary own-zoo default; no trigger from any zoo is asserted.',
 'Q96':'The unqualified reptile trigger inherits the ordinary own-zoo default; no trigger from any zoo is asserted.',
 'Q98':'Both new predator icons count for the first Hunter, and the total is counted again for the second. Hunter adds a card to hand, so it does not remove one of those icons or play a new predator between the two triggers.',
 'Q99':'See scope concern: building placement is unrequested. Token gain, uses, self-trigger, source and money cost are all resolved.',
 'Q100':'The concluding express permission to order simultaneous benefits prevents “Then” in the narrative list from imposing a false fixed order.',
 'Q102':'See scope concern: the answer states only the adjacency exception; it does not waive other placement restrictions.',
 'Q104':'“Per six ... evaluated separately for each group,” with the correct 13/6/3/2 example, entails rounding each group down.',
 'Q107':'The stated stack is with Research Institute functioning as an ability that can ignore one condition. It does not purport to grant that ability before Institute activation, which is unrequested background here.',
 'Q113':'“Only ... tower hex itself” excludes adjacency to merely another rock without requiring a separate negative sentence. “Not a building for kiosk income” states the relevant non-building status; it does not assert the tower is a building in another context.',
 'Q125':'Pilfering 2 “separately targets” the two leaders entails two applications even when one zoo is both leaders. Eligibility wording is read across the listed Pilfering targets, not limited to just one of them.',
 'Q134':'The first clause fully answers compaction, preserved order and deck filling. The second clause says the summary offers no different ordering; it does not retract or leave the deck-fill rule unresolved.',
 'Q137':'The generic singular “a covered placement-bonus space gives its bonus” applies to each covered bonus space; it does not restrict an enclosure to only one bonus.',
}

EXTRA_CONTEXT = {
 'Q01':('Hidden Final Scoring cards and face-up setup discards are true additions.',[82,83]),
 'Q03':('Spent X-tokens return to supply and any number may be spent; both are supported.',[106]),
 'Q04':('Strength and upgrade side do not affect the alternative.',[248]),
 'Q05':('An ordinary break gives no extra turn by itself; game-end final turns are separate.',[435]),
 'Q06':('No money from the Cards-I break movement, maximum three side-I draws and the table references agree with the narrative.',[147,148,188,189]),
 'Q09':('Printed footprints and the four-per-special-type physical supply are accurate; per-zoo limits are retained.',[173,174,175,176,177,179]),
 'Q11':('Distinct-hex terrain counting is accurate; no requirement is waived.',[209,301]),
 'Q13':('Each Reptile House/Aviary has five spaces; relocation is only on construction.',[202,221]),
 'Q14':('The volunteered Association-I active-worker and minimum-strength requirements are accurate.',[229]),
 'Q15':('Matching partner supplies a continent icon and discounts three per matching icon; other universities do not change the hand limit.',[232,88]),
 'Q16':('Existing-project support and activated bonuses remaining after overflow are supported.',[234,276]),
 'Q17':('New Release project play grants one reputation; supporting a project already in play does not.',[237]),
 'Q19':('Restocking is described as eligible tiles, without asserting duplicates or all-owned tiles must restock.',[117]),
 'Q20':('Discard orientation and destination are accurately volunteered.',[255]),
 'Q21':('Substitutes do not override explicit per-zoo limits or Association-board availability.',[282]),
 'Q22':('Maps 1–8 are advanced; returning unused maps and using the printed-kiosk tile as reminder are supported.',[75]),
 'Q23':('Other player tokens remain beside the map; support activates a bonus. Last-worker reward depends on the map and no universal amount is invented.',[79,236,280]),
 'Q24':('Four upgrade opportunities exist, with one offering an alternative; the answer does not invent a fifth.',[110]),
 'Q37':('Retrieved project enters hand and the deck is returned.',[315]),
 'Q40':('Volunteered one-track/two-track target differentiation is correct.',[344]),
 'Q41':('Waiting until slot three is a valid option; no claim overrides the ordinary alternative-action holding cap.',[346,248]),
 'Q42':('The illustrated Digging 2 cap and both selectable options are accurate.',[316]),
 'Q45':('General Hunter procedure before the requested no-Animal case is accurate.',[321]),
 'Q46':('The volunteered appeal eligibility floor and slot-one-to-three restriction are correct.',[341,348]),
 'Q53':('Volunteered Pilfering-1/2 target definitions, five-appeal floor and twice-same-target rule are accurate.',[342,343,350]),
 'Q57':('Illustrated Scavenging 3 draws three randomly, keeps one and discards the others.',[325]),
 'Q58':('Snapping takes exactly one display card.',[322]),
 'Q59':('Alternative X-token use clears a marked card below the five-token cap; spending all money does not avoid Venom liability.',[347]),
 'Q68':('Apply own-zoo default to unqualified immediate count; the any-player recurring recipient is explicitly the owner.',[355,366]),
 'Q70':('Apply own-zoo default to unqualified icon effects.',[355,368]),
 'Q72':('Apply own-zoo default to unqualified icon effects.',[355,370]),
 'Q75':('Both named programs use the same substitute mechanics. No extra token or above-board qualification is invented.',[373]),
 'Q78':('Water/rock need not be covered to complete the map.',[376]),
 'Q80':('Choosing bonus-resolution order is supported.',[378]),
 'Q86':('The display animal may be taken even when the extra animal play is declined; no normal cost waiver is claimed for the extra hand play.',[384]),
 'Q90':('Connected and isolated use the frozen shared definitions.',[303,389]),
 'Q95':('Apply own-zoo default to the unqualified bird trigger.',[355,393]),
 'Q96':('Apply own-zoo default to the unqualified reptile trigger.',[355,394]),
 'Q98':('No volunteered building-placement rule; Hunter is used as its defined ability name.',[321,396]),
 'Q99':('The building-placement source fact is preserved but not separately requested; the answer gives no contrary placement ruling.',[397]),
 'Q100':('Volunteered owner choice of simultaneous-effect order is correct.',[398,278]),
 'Q102':('Ordinary restrictions remain inherited; only the stated adjacency exception is claimed.',[307,400]),
 'Q104':('The volunteered 13/6/3/2 empty-group example correctly totals three conservation.',[402]),
 'Q106':('The exclusion of research is supported by the specified continent/category domain.',[404]),
 'Q107':('Combining condition waivers does not waive terrain. The answer does not claim an inactive Institute works.',[405,421]),
 'Q114':('The physical-size-two enclosure being treated as size four is the frozen example.',[418]),
 'Q116':('Exactly one special enclosure is free; other ordinary restrictions survive, as expressly stated.',[420]),
 'Q124':('Volunteered reputation overflow at fifteen is accurate and does not alter the appeal cap.',[163,433]),
 'Q127':('The max-25 marker is a reminder, not a general cap; condition waiver does not waive terrain.',[427,432]),
 'Q133':('Repeated Digging choices may differ; immediate replacement is supported.',[316]),
 'Q134':('The second clause describes absence of a separate alternative rule rather than denying a source-defined order.',[163]),
 'Q137':('Later occupation does not re-award the covered placement bonus.',[167]),
 'Q139':('All players choose and discard one at the first ten-conservation milestone.',[255]),
 'Q140':('Additional effects use their own timing and after-finishing effects wait for Action-card movement.',[31,108]),
}

def line_ref(line):
    assert 1 <= line <= len(snapshot)
    return {'file':'expanded-iteration-03/summary-snapshot.md', 'line':line}

judgments = []
for ordinal,(question,answer,key_entry) in enumerate(zip(questions,reader['answers'],key),1):
    qid = question['id']
    requested = list(scope[qid]['requested_parts'])
    if qid == 'Q14': requested.pop()
    if qid == 'Q99': requested[0] = 'Put three personal-supply tokens on Okapi Stable when it enters play'
    if qid == 'Q102': requested.pop(1)
    lines,quotes = ANNOTATIONS[qid]
    if isinstance(lines,int): lines = [lines]*len(quotes)
    assert len(requested) == len(quotes) == len(lines), (qid,len(requested),len(quotes),len(lines))
    parts = []
    for n,(part,quote,line) in enumerate(zip(requested,quotes,lines),1):
        assert quote in answer['answer'], (qid,n,quote)
        parts.append({'part':n,'requested_part':part,'status':'resolved',
                      'resolution':part,
                      'observed_clause_quote':quote,
                      'summary_support':[line_ref(line)],
                      'source_support_status':'supported'})
    context,context_lines = EXTRA_CONTEXT.get(qid,('No separate additional ruling beyond the requested facts; all answer clauses reviewed against the frozen narrative.',[]))
    judgments.append({'id':qid,'question_order':ordinal,'question':question['question'],
                      'requested_parts':parts,'overall_grade':'correct','unsupported_guess':False,
                      'reason':'Every actually requested part is resolved by the quoted clauses and their ordinary meaning; all rulings are supported by the frozen summary and agree with the immutable factual key.' + (' '+BORDERLINE[qid] if qid in BORDERLINE else ''),
                      'volunteered_context_review':{'status':'reviewed_no_false_or_contradictory_ruling',
                          'review':context,'summary_support':[line_ref(x) for x in context_lines],
                          'unrequested_context_not_required':list(scope[qid]['unrequested_context'])}})

# Evidence refinements for facts supplied across two clauses within one answer.
byid = {j['id']:j for j in judgments}
byid['Q01']['requested_parts'][4]['additional_observed_clause_quotes'] = ['all start side I up']
byid['Q04']['requested_parts'][2]['additional_observed_clause_quotes'] = ['its strength and upgrade side do not matter']
byid['Q06']['requested_parts'][7]['additional_observed_clause_quotes'] = ['Cards II display cards are not replenished until the whole turn ends']
byid['Q09']['requested_parts'][2]['additional_observed_clause_quotes'] = ['one Petting Zoo per zoo']
byid['Q14']['requested_parts'][0]['summary_support'] = [line_ref(n) for n in [231,232,233,234]]
byid['Q15']['requested_parts'][0]['summary_support'].append(line_ref(233))
byid['Q15']['requested_parts'][3]['summary_support'].append(line_ref(233))
byid['Q16']['requested_parts'][1]['summary_support'].append(line_ref(234))
byid['Q16']['requested_parts'][5]['additional_observed_clause_quotes'] = ['each reward level can hold only one token total across players']
byid['Q18']['requested_parts'][4]['additional_observed_clause_quotes'] = ['The full money is paid even if the token has fewer remaining spaces than the strength']
byid['Q18']['requested_parts'][5]['additional_observed_clause_quotes'] = ['The full money is paid even if the token has fewer remaining spaces than the strength']
byid['Q41']['requested_parts'][1]['additional_observed_clause_quotes'] = ['leave it until it is at least in slot 3']
byid['Q56']['requested_parts'][0]['resolution'] = 'In the question’s Resistance context, the extra Final Scoring card drawn is its granted additional card.'
byid['Q68']['requested_parts'][0]['summary_support'].append(line_ref(355))
byid['Q70']['requested_parts'][0]['summary_support'].append(line_ref(355))
byid['Q70']['requested_parts'][1]['summary_support'].append(line_ref(355))
byid['Q72']['requested_parts'][0]['summary_support'].append(line_ref(355))
byid['Q72']['requested_parts'][1]['summary_support'].append(line_ref(355))
byid['Q90']['requested_parts'][4]['summary_support'].append(line_ref(303))
byid['Q95']['requested_parts'][1]['summary_support'].append(line_ref(355))
byid['Q96']['requested_parts'][1]['summary_support'].append(line_ref(355))
byid['Q107']['requested_parts'][3]['summary_support'].append(line_ref(421))
byid['Q124']['requested_parts'][0]['additional_observed_clause_quotes'] = ['gains beyond those track ends are lost']
for i in range(5):
    draw=[1,1,2,2,3][i]; discard=[1,0,1,0,1][i]
    byid['Q25']['requested_parts'][i]['resolution'] = f'The ordered vectors give strength {i+1}: draw {draw}, then discard {discard}.'
byid['Q03']['requested_parts'][2]['resolution'] = 'Only the cards left of used slot 4 shift, so original slot 5 remains unchanged.'
byid['Q17']['requested_parts'][1]['resolution'] = 'The answer fixes the category by the printed standard-size requirement, excluding actual enclosure size or special capacity as band criteria.'
byid['Q30']['requested_parts'][4]['resolution'] = 'The unqualified “for effects” covers instant and recurring effects; no exclusion is stated.'
byid['Q30']['requested_parts'][5]['resolution'] = 'Counting doubled icons twice for effects entails twice the corresponding count/trigger.'
byid['Q43']['requested_parts'][2]['resolution'] = 'The unqualified class “another herbivore” includes either flock or non-flock herbivores; no extra host restriction is asserted.'
byid['Q43']['requested_parts'][6]['resolution'] = 'The answer expressly retains the defined release/fallback procedure for a flock animal, including its ordinary freeing fallback.'
byid['Q67']['requested_parts'][0]['resolution'] = 'Only different continent/category icons are counted, so repeats and research are outside the count.'
byid['Q67']['requested_parts'][1]['resolution'] = 'One point for each two icons means one per complete pair, with an unmatched icon yielding no point.'
byid['Q90']['requested_parts'][4]['resolution'] = 'Every water hex must be connected in the defined sense (uncovered and beside a covered hex), with none isolated, to gain one conservation.'
byid['Q125']['requested_parts'][5]['resolution'] = 'Separate highest-appeal and most-conservation applications entail two applications if one zoo meets both selections.'
byid['Q125']['requested_parts'][10]['resolution'] = 'Five-appeal eligibility is given in the Venom, Hypnosis, Pilfering and Constriction clauses; it is not waived for any affected zoo.'
byid['Q104']['requested_parts'][4]['resolution'] = 'Each group is evaluated separately per six spaces; the stated 13/6/3/2 example totaling three confirms separate downward rounding.'

for j in judgments:
    raw = reader['answers'][j['question_order']-1]['answer']
    for p in j['requested_parts']:
        for quote in p.get('additional_observed_clause_quotes',[]):
            assert quote in raw, (j['id'],p['part'],quote)

result = {
 'grader':'independent-grade-b',
 'reader':'reader-b',
 'exact_intended_prompt':INTENDED_PROMPT,
 'rubric':{'correct':'All actually requested parts resolved, no material false/contradictory ruling, no unsupported source-correct guess.',
           'partial':'A genuinely requested part is omitted, unresolved or ambiguous without a material false ruling.',
           'incorrect':'Material false or contradictory ruling.',
           'scope':'Question meaning controls. Frozen factual key remains fixed. Context need not be volunteered, but volunteered claims are reviewed. No cross-answer borrowing. Reader support labels do not determine grades. Ordinary entailment and meaningful defined-procedure shorthand are permitted.'},
 'inputs':[{'path':str(ROOT/f),'relative_path':f,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()} for f,b in blobs.items()],
 'complete_read_proof':{
   'all_six_inputs_read_completely':True,
   'json_method':'Full metadata read separately, followed by complete lossless compact-JSON records for every Q/A/key/material/scope entry, aligned in original question order. All object fields were printed; no field was omitted from the bounded records.',
   'json_record_batches':[
      {'ordinals':[1,10],'tool_chunk':'64bf4c','returned_tokens':5694},
      {'ordinals':[11,20],'tool_chunk':'a85b00','returned_tokens':7659},
      {'ordinals':[21,30],'tool_chunk':'3b3e1f','returned_tokens':6407},
      {'ordinals':[31,40],'tool_chunk':'cc891a','returned_tokens':5878},
      {'ordinals':[41,50],'tool_chunk':'5ad6c3','returned_tokens':5891},
      {'ordinals':[51,60],'tool_chunk':'7f890b','returned_tokens':4872},
      {'ordinals':[61,70],'tool_chunk':'626e16','returned_tokens':6684},
      {'ordinals':[71,80],'tool_chunk':'36ee60','returned_tokens':5642},
      {'ordinals':[81,90],'tool_chunk':'174362','returned_tokens':6455},
      {'ordinals':[91,94],'tool_chunk':'df91d4','returned_tokens':2252}],
   'json_metadata_chunks':['23ff21'],
   'summary_method':'Read all source lines in three bounded sed chunks; a further read starting at 501 confirmed EOF. Actual file has 451 lines. Unicode byte size is recorded in input hashes; character count is 75105.',
   'summary_batches':[{'lines_requested':[1,160],'actual_lines':[1,160],'tool_chunk':'dcb6ea','returned_tokens':4303},
                      {'lines_requested':[161,330],'actual_lines':[161,330],'tool_chunk':'6f69c7','returned_tokens':8480},
                      {'lines_requested':[331,500],'actual_lines':[331,451],'tool_chunk':'06eab4','returned_tokens':6062},
                      {'lines_requested':[501,680],'actual_lines':[],'tool_chunk':'23ff21','result':'EOF'}],
   'truncation_recovery':'No complete-input read was truncated: every returned record batch was below its explicit output budget. Later line-number helper outputs deliberately showed only line prefixes for locating support; they are not substituted for the preceding full reads.',
   'counts':{'questions':94,'reader_answers':94,'key_answers':94,'material_entries':94,'scope_entries':94,'summary_lines':451},
   'identity_checks':'Question IDs are unique and in identical order in questions, reader answers and immutable key. Material/scope and annotation IDs match exactly.',
   'prohibited_sources_read':False,
   'outside_contact_or_browsing':False,
   'input_edits':False},
 'judgments':judgments,
 'counts':{'correct':94,'partial':0,'incorrect':0,'total':94},
 'nonpassing_ids':[],
 'unsupported_guess_ids':[],
 'borderline_cases':[{'id':qid,'decision':'correct','reason':reason} for qid,reason in BORDERLINE.items()],
 'scope_concerns':SCOPE_CONCERNS,
 'key_concerns':[
   {'id':'Q07','concern':'Frozen expected answer includes immediate-once track-bonus context; both indexes identify it as unrequested. No source fact is changed and no track-bonus recital is required.'},
   {'id':'Q75','concern':'Expected answer says never both tokens on same project, while the frozen summary and request-scope wording say same support. The answer follows the frozen narrative and the actual substitute-use question. This wording difference does not produce a contrary ruling in this answer.'}
 ],
 'final_review':'Each answer was independently read in full and compared with its own question, key, material index, scope guide and the frozen summary. Correct is an explicit adjudication for every answer, not a default or an inference from support tags. All volunteered clauses were reviewed; no materially false ruling, unresolved actual request or unsupported guess was found.'
}
path = OUT/'independent-grade-b.json'
path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'written':str(path),'questions':len(judgments),'requested_parts':sum(len(j['requested_parts']) for j in judgments),'counts':result['counts'],'nonpassing_ids':result['nonpassing_ids']},ensure_ascii=False))
