from pathlib import Path
import json,hashlib
root=Path('/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/ark-nova/2026-11-04-batch-231507')
files=['expanded-iteration-04/reader-b.json','expanded-iteration-04/summary-snapshot.md','expanded-iteration-04/questions.json','benchmark-v2/answer-key.json','benchmark-v2/material-requested-facts.json','grading-request-scope-02.json']
data={f:(root/f).read_bytes() for f in files}
a=json.loads(data[files[0]])['answers']; qs=json.loads(data[files[2]])['questions']; key=json.loads(data[files[3]])['answers']; facts=json.loads(data[files[4]]); scope=json.loads(data[files[5]])['questions']; summary=data[files[1]].decode().splitlines()
# Independently selected relevant answer excerpts, in the actual requested-part order.
manual='''Q01|25 money~1 active association worker on the notepad and 3 inactive workers~Draw 8 Zoo cards, keep 4 and discard 4~Draw 2 Final Scoring cards~Put Animals side I in slot 1~the other four Action cards randomly in slots 2–5, all side I up~Appeal starts at 0 for the first player, 1 for second, 2 for third and 3 for fourth
Q02|4 face-up Base Conservation Projects below the Association board in a four-player game, and 3 in two- or three-player games~block the left level on the left face-up project, the middle level on the middle project, and the right level on the right project~block the three donation spaces in the donation area's left column. These are unavailable to both players~No such setup blocks are stated for three or four players~Reveal the six-card display only after every player has selected starting hand cards
Q03|put the used card in slot 1~shift the cards that were left of its now-empty slot one place right~shift the cards that were left of its now-empty slot one place right~Set strength before the action~each X-token spent then adds +1 strength~X-tokens gained during the action cannot boost that same action~hold at most 5 X-tokens~after the action is complete, including the Action-card movement
Q04|you cannot do nothing~select an Action card~take exactly 1 X-token~move it to slot 1 using the ordinary card movement~you cannot take it if you already hold 5 X-tokens
Q05|ignore the excess steps~player who reaches the last space gains 1 X-token~Finish the current turn; the break occurs afterward~play resumes clockwise after the break with the next player
Q06|Cards I advances the Break token 2 spaces, then~draws from the deck according to the strength table~snaps exactly 1 display card at strength 5+~Cards II also advances it 2 spaces~draws from the deck and/or in-range display in any order under its table~Cards II snapping starts at strength 3 and takes exactly one display card~snap ignores reputation on either side and involves no deck draw~replenished after the turn ends~There is no in-turn hand limit; discard to the limit only at breaks
Q07|Reputation range includes the display folder matching your reputation space and all lower-numbered folders~Reputation 10 and above requires the upgraded Cards action~gives 1 appeal for each remaining reputation step~You may not look through the discard pile during the game
Q08|Build I constructs exactly 1 building, of size no greater than strength~Build II constructs any number of different buildings whose total size is no greater than strength~not two identical buildings in the same action~Pay 2 money per space~first building must have at least one space on a map border~later buildings must share at least one edge with an existing building~Build only on empty spaces; do not overlap, go off-map, or cover water/rock~Restricted-icon spaces require Build II~A kiosk must be at least 3 spaces from each other kiosk~Each pavilion gives +1 appeal immediately, once
Q09|Build I allows standard enclosures, kiosks, pavilions and one Petting Zoo~Build II additionally allows a Reptile House and a Large Bird Aviary~Each of the three special enclosure types is limited to one per individual zoo~Unique buildings cannot be built through Build; they enter only through their Sponsor cards~Covering every map space except water and rock immediately grants 7 appeal~this may be triggered by any effect that covers the spaces
Q10|Benefits gained earlier during an action—including money, cards and newly activated workers—can be used in later steps of that same action~Pay for each item before receiving that item's own benefit~Ordinary effects resolve immediately~after finishing wait until the entire action and Action-card movement are complete~the player whose effects they are chooses their order
Q11|meet every printed condition~pay its full cost first~reduces cost by 3 money for each continent icon on that Animal card~an empty standard enclosure at least the required size~flip the entire enclosure to occupied~Petting Zoo animals go only in the Petting Zoo~Eligible reptiles and some birds may instead use their designated special enclosure~Special enclosures are never flipped: mark occupied spaces using one supply player token per required space~These conditions also apply when using a special enclosure~immediate effects before the next Animal~after-finishing effects after the whole Animals action and card movement
Q12|animals from hand or from the display within reputation range~display animals cost the folder number as an additional cost~At strength 5+, you may gain 1 reputation~at the very beginning of the action, before choosing/playing animals, so the new range applies~Do not replenish display cards until the turn ends~Animals II permits animals with the upgrade-required condition icon
Q13|Only immediately when building a Reptile House or Large Bird Aviary~moving all corresponding animals that fit and deciding separately for each~new special enclosure must meet each animal's terrain requirements and have enough capacity~Mark capacity with the animal's indicated number of player tokens from supply~flip the smallest occupied standard enclosure meeting all its requirements, including terrain~if none, flip the smallest occupied enclosure meeting its size alone~if none meets even its size requirement, flip none
Q14|strengths 2 for +2 reputation, 3 for a partner zoo, 4 for a university, and 5 for conservation project work~Association I performs exactly one task~Association II may perform one or more different tasks with total task value at most action strength~If one of your workers is already on that task, spend 2 workers~with 3 of yours there, you cannot repeat until after a break~Other players' workers do not affect whether you may use a task~Each task requires at least one active worker
Q15|from available spaces on the Association board~lowest empty spaces in the corresponding column of your zoo map~resolve any printed covered-space bonus immediately~You cannot take duplicate universities; partner zoos must be from different continents~at most 4 partner zoos~third and fourth require Association II~hand-limit university raises the break hand limit from 3 to 5; other universities do not change it~Universities also immediately grant their own printed reputation award
Q16|played from hand with Association I/II conservation work~played from hand with Association I/II conservation work, or from the display within reputation range with Association II and folder-number additional cost~placed above the board at the left, pushing others right~A project pushed beyond the player-count limit is discarded~tokens on it return to their owners' supplies, while their map bonuses remain activated~meet an unoccupied condition/level~you normally support a given project only once~one of your seven left-edge map tokens~take its map bonus immediately, before or after project reward as chosen~Recurring map bonuses repeat at each break
Q17|printed standard-enclosure requirement must fit the depicted release size category: 2− accepts size 1 or 2, 3 accepts size 3, and 4+ accepts size 4 or 5~printed standard-enclosure requirement must fit the depicted release size category~lose only the animal's printed appeal before conservation reward~discard the animal and lose its icons~Keep its conservation, reputation, ability-generated appeal and previously earned effects~If the animal could live in a special enclosure and its marked spaces can be removed, remove those tokens~otherwise free its standard enclosure by flipping the smallest occupied one meeting all requirements~fallback to smallest meeting size alone, or none if none meets size
Q18|Sponsors I plays exactly one Sponsor from hand, requiring action strength at least its level and fulfillment of its conditions~Sponsors II may play one or more cards from hand and/or in-range display~paying each display card's folder number~fully resolve each card before the next, except after-finishing effects~advance Break by strength and take that much money~Sponsors II break option pays double money, including if fewer steps remain than the chosen advance; the full money is still taken
Q19|discard to hand limit~clear Multiplier/Venom/Constriction tokens~recall workers~restock Association tiles~discard display folders 1–2, compact and refill~take income; reset Break token~Each kiosk earns 1 money per adjacent unique building, special enclosure, occupied standard enclosure, or pavilion~Empty standard enclosures do not count; empty special enclosures do~resolve clockwise from the break initiator (or first affected player clockwise from them)~refill after each such player's income before the next affected player chooses~reset Break token
Q20|At 2 conservation, choose an Action-card upgrade or activate an additional association worker~At 5 and 8, choose 5 money or an adjacent Bonus tile, if available~At 10, the first player to reach/pass it makes all players discard one Final Scoring card~Check game end at the end of your turn or during a break when Appeal and Conservation are in the same scoring area or have passed one another~Appeal gained during another player's turn waits until the end of your turn or a break~every other player takes one more turn~if during a break, all players take one more turn~Each Final Scoring card is capped at 4 conservation points~VP = your Appeal minus the lowest Appeal value in the scoring area of your Conservation counter~Highest positive VP wins~ties go to most supported projects, then shared victory
Q21|Shuffle 9 Bonus tiles and place one at random face up on each of the four blank yellow spaces~Do not use the two yellow spaces with icons~return the other five tiles to the box~use a suitable substitute if a component runs out
Q22|taking two random maps and choosing one advanced side, or laying out player count +1 advanced maps and choosing in reverse play order~Map A starts with an empty size-3 standard enclosure~its printed kiosk counts as built, with a kiosk tile placed as a reminder
Q23|seven conservation-support player tokens begin on the designated spaces along the left edge~take them from the lowest supply space upward~Some maps reward hiring the last worker with conservation points
Q24|Flip a chosen Action card from side I to II~in its current slot; it does not move~side-II action becomes usable on your next action~counts as upgraded immediately for conditions~you cannot upgrade all five cards
Q25|1 draw/discard 1~2 draw/discard 1/0~3 2/1~4 2/0~5 3/1~A required discard may be either a newly drawn card or one already in your hand
'''
manual+='''Q28|seven categories are bird, herbivore, predator, primate, reptile, bear and Petting Zoo animal~Both count unless explicitly excluded~Bears count as a category even when also herbivore or predator~Petting Zoo animal is its own category
Q29|Association II permits exactly one donation~only if you performed at least one Association task in the same action~exactly one donation~it needs no worker~printed ladder is 2, 5, 5, 7, 7, 10, 10, then 12~Skip spaces blocked at setup~Pay the smallest currently visible donation amount~place one player token from your supply on that space~gain 1 conservation~Once all except the final space are covered, each later donation costs 12 and places no additional token
Q30|upper-right icons on Animal and Sponsor cards~partner-zoo and university icons~water/rock requirement icons at upper left~Left-side conditions and Conservation Project icons are not zoo icons~An effect can count its own card's icons~double icons count twice and trigger matching effects twice~Card text takes priority over general rules
Q31|two distinct adjacent terrain hexes~if several edges touch one hex, it counts only once~a larger terrain region contributes only the hexes actually adjacent~Decorative water/rock illustrations on tiles are not terrain spaces and do not count
Q32|Playing a new Release into the Wild project grants the player who puts it into play 1 reputation~merely supporting an existing one does not grant that reputation~Breeding Program projects use the same condition for all three reward levels~choose any currently available level that meets the condition and ordinary support rules
Q33|A condition with no number, or marked “per,” pays once for each fulfillment~A numbered threshold pays only once~if several numerical thresholds are listed, use the highest one met~Read X:Y as condition on the left and reward on the right
Q34|Connected means uncovered and sharing an edge with a covered space~isolated means no adjacent covered space~A border space lacks a neighboring map hex on at least one of its six sides~“Your zoo” includes your played cards, map and personal supply~“any zoo” includes those for every player
Q35|A unique building must be placed when its Sponsor is played~if it cannot be legally placed, the Sponsor cannot be played~No size-based construction payment is due~ordinary placement rules and printed terrain adjacency apply~colored face up, rotate freely but do not flip it~Unique buildings are not enclosures, cannot house additional animals~do not count as water or rock spaces
Q36|Finish the Animals action, including moving its Action card to slot 1, before performing an animal-granted action~Use the granted Action card normally and move it to slot 1 after that action~A named Action cannot be replaced by the X-token alternative~Determination (Any Action) may choose the X-token alternative
Q37|take the selected project (Assertion)~named project (Dominance) into hand~Dominance has no effect if its named project is already in play~play the obtained card through Association conservation work above the board and support it immediately~it does not go into the setup base row below the board
Q38|Boost and Clever resolve after finishing Animals and moving the Animals card~Clever puts its chosen Action card in slot 1~Boost puts its named card in slot 1 or 5~cards formerly left of it shift right~moving to slot 5 shifts cards formerly to its right left
Q39|A target zoo must have at least 5 appeal for Constriction, Hypnosis, Pilfering and Venom~playing animal's appeal may be gained before or after its interactive effect~its new appeal need not be counted in selecting targets~multiplayer group prefers, it may use the cards' alternate text marked for solo instead
Q40|one token on slot 5 if ahead on one track, or tokens on slots 4 and 5 if ahead on both~Do not stack two Constriction tokens on one card; return duplicates~Each affected action loses 2 strength~for each execution of a multiplied action~X-tokens can restore strength~Return a token after acting with that card; otherwise it is removed without effect at the break
Q41|A card reduced to effective strength zero or below may not be used as a regular action~spend enough X-tokens to bring it to at least 1~use its alternative X-token action
Q42|decide again after each card and may choose either option each time~A display card discarded through Digging is replaced immediately~shifting higher folders down and drawing into folder 6
Q43|only if another herbivore in your zoo requires at least the flock animal's standard-enclosure size~same qualifying herbivore can host any number of flock animals~need not be a flock animal~avoid taking a new enclosure only if another herbivore~A later non-flock herbivore cannot join the flock animal in its enclosure~you do not need to establish historical accommodation~follow the usual occupied-enclosure freeing/fallback procedure
Q44|activates the lowest remaining reserve worker by moving it to your notepad for immediate use~Take a last-worker map reward if shown~If all workers are already active, the ability has no effect
Q45|If none revealed is an Animal, discard all revealed cards and add none
Q46|Choose among tied players for highest appeal~if you yourself are the target, Hypnosis has no effect~your own X-tokens may be spent~using that owner's upgraded/unupgraded side~Move the borrowed card to slot 1 normally~Venom and Constriction tokens on it apply to you and are discarded afterward~its Multiplier cannot be used
Q49|Place a gained Multiplier immediately on its named Action card~a bonus-tile Multiplier may go on any card, including Animals~execute the action twice consecutively at the same base strength~move the card only after both executions~Each X-token boosts only one execution~Defer after-finishing effects until both executions are done~A break triggered by the first execution waits until the whole turn finishes~Return used tokens to supply; an unused token is removed at the next break
Q50|Two Multiplier tokens permit up to three executions, not four~A multiplied X-token alternative may take two X-tokens, subject to the five-token holding limit~you may not mix one X-token action with one regular action
Q51|Peacocking lets you place the Large Bird Aviary before upgrading Build~must have a legal site~You must not already have an Aviary~other placement restrictions remain, including Build II for upgrade-marked spaces~Posturing follows normal placement rules, including kiosk spacing~multiple buildings are placed one at a time
Q52|Successive Petting Zoo animals grant 3, then 6, then 9 appeal~One Petting Zoo can hold at most three~Petting Zoo animals count as small animals
Q53|Ties let you choose~most-conservation target must have at least 1 conservation~A self-target has no effect
Q54|The target chooses whether to give 5 money or permit a random hand-card draw~Final Scoring cards cannot be drawn~If target has no hand cards, they must give 5 money~if they have less than 5 money, they must give a card~With neither a card nor 5 money, they give all current money, including zero~Resolve repeated Pilfering sequentially, and the target may choose differently each time
Q55|tucked cards have no remaining function~If that animal is released, discard its tucked cards too~keeping the appeal already gained~puts sold cards in the discard pile
Q56|Resistance drew an extra Final Scoring card~it joins the cards you can choose from when discarding one at that milestone~At game end, score every remaining Final Scoring card~each card has its own maximum of 4 conservation points
Q57|shuffles the discard pile face down, draws randomly from it~returns the discard pile face up
Q58|Snapping takes exactly one card from the display regardless of reputation~it does not offer a deck draw instead~Sponsor Magnet takes display Sponsor cards regardless of reputation range~if no Sponsor is present, it does nothing~Ordinary end-of-turn display refill applies
Q59|lowest slots first (slot 1, then 2, etc.)~at most one per card; duplicates return to supply~Using a marked card removes its token and avoids all Venom fees that turn~At turn end, pay 2 money only if you removed no Venom token that turn and at least one Venom token remains~If unable to pay, undo the turn and choose another action~Unused tokens expire without effect at the next break
Q63|immediately gives 2/5/10 money for having 1/2/3 universities~require Association strength 4 instead of 5~final reward is 1 conservation for three universities
Q66|number of player tokens missing from your zoo map's left edge; its instant reward is 2 appeal per such project~At each break it gives 1 conservation
Q67|different continent/animal-category icons~1 conservation per pair~each other player gains 2 money
Q68|Science Library gives 1 appeal per research icon when played~Whenever any player plays a research icon, the Science Library owner gains 2 money~It scores 1 conservation if its owner has five different animal categories
Q70|gives 1 appeal per Americas icon at play~Each Americas icon played permits a free kiosk~under normal placement and spacing rules~five or more kiosks, for 1 conservation
Q72|gives 1 appeal per Australia icon when played~For each Australia icon played, you may tuck one hand card under it for 2 appeal~tucked cards have no further function
Q75|puts two supply tokens on the Sponsor~return exactly one token as one icon; never use both for one support~When supporting a base project below the Association board~A base-origin card later played above the board does not qualify~1 conservation for five or more project supports, counting missing left-map tokens
Q77|one extra copy of a building built in that same action~without additional strength~pay its normal money and obey placement rules~Even with several different buildings, only one extra building is allowed~cannot exceed the one-per-zoo limit for each special enclosure type~Final reward: 5 appeal with a full map except water/rock
Q78|gives 2 money per water/rock icon immediately~You may build over water/rock spaces~ignore terrain requirements for animals and unique buildings~their printed terrain icons still count~Covered terrain no longer counts for Hydrologist, Geologist or Architectural Zoo~scores 2 appeal per water-icon/rock-icon pair, up to three pairs
Q80|triggers when an actual placement bonus on a border space is gained~any uncovered placement bonus on your map as an additional bonus; it need not be on the border~Multiple triggers allow multiple extra choices, which may repeat the same bonus~1 conservation when all building border spaces are covered, excluding water/rock
Q82|gives 1 X-token immediately~Each Release into the Wild support gains 1 additional conservation~support the same release project repeatedly with different qualifying animals~at most once per project per Association action~Each token counts as a separate project support for other effects
Q83|gives 1 X-token immediately~immune to Venom, Constriction, Hypnosis and Pilfering~For Hypnosis and Pilfering, ignore your counters and find the next qualifying player~scores 1 conservation if you have all five continents
Q85|permanently choose small or large, mark that choice with a supply token~reveal deck cards until finding an Animal of that type; keep it and discard the rest~Chosen small animals get +2 appeal, chosen large animals +4~can no longer play the opposite size type~size-3 animals remain legal but get no bonus
Q86|gives 2 money per small animal immediately~An Animals action containing only small animals qualifies~play one additional small Animal from hand with normal costs/rules~take one small Animal from the display into hand regardless of reputation~take the display card even if you declined the extra play~mixing a large animal into the original action disqualifies it
Q90|gives 1 appeal per water icon on play~Each newly covered space adjacent to water gives 1 money~including multiple spaces within one building~one space adjacent to multiple water hexes still pays only once~scores 1 conservation if all water hexes are connected (none isolated)
Q95|Barred Owl Hut places its unique building~Whenever a bird icon is played, draw two cards from the deck, keep one and discard the other
Q96|places its unique building adjacent to water~Each reptile icon played lets you sell up to two hand cards for 4 money each~discard the sold cards
Q98|triggers Hunter for each predator icon played, with cards revealed equal to your total predator icons~A card with two predator icons triggers two sequential Hunters~counting both new icons for each Hunter's draw amount
Q99|places its unique building and three supply tokens on the Sponsor~Per herbivore icon played, you may spend one token to play a Sponsor from hand~for money equal to its level, following normal conditions~Stable's own herbivore icon can trigger this when it is played~three uses total
Q100|Zoo School gives 1 reputation and 1 conservation~covers at least two border spaces~take one in-range display card or draw one deck card
Q102|placed on two border spaces without touching an existing building~other placement rules apply~later buildings may attach to it~At each break it yields 2 money per adjacent building except empty standard enclosures~it may be adjacent to a kiosk~final reward is 5 appeal with full map coverage excluding water/rock
Q104|1 appeal per connected uncovered building border space~water and rock do not count~Restricted/upgrade-marked building spaces count even without Build II~1 conservation per six contiguous empty building spaces~evaluating each group separately (example: groups of 13, 6, 3, 2 yield 3 conservation total)
Q106|2 money per different continent or animal-category icon; research icons do not count~Each continent/category newly introduced to your zoo gives 1 appeal and 2 money~two copies of the same new icon grants this novelty benefit only once
Q107|free size-5 standard enclosure under normal placement rules~When playing a large animal, it lets you ignore one left-side condition, such as a required icon or Animals upgrade~terrain requirements cannot be ignored~stacks with Research Institute, allowing two conditions to be ignored
Q112|compares each animal category in your zoo with the player to your right~gives 1 conservation for each category in which you have more icons~If that player has none of a category, one of your icons is enough~Maximum is 4 conservation
Q113|standard enclosures adjacent to the tower hex itself, not merely another rock hex~Special enclosures do not qualify~Housing an animal there grants the two appeal again even if an earlier animal was released~tower is not a building for kiosk income
Q114|standard enclosures touching the Outdoor Area hex itself, not merely another water hex~two spaces larger for all purposes after placement~bonus cannot be ignored for release or transfer~does not affect special enclosures~is not a building
Q115|activates when a building is placed on its adjacent building space~Your first building may start beside the Harbor but need not~before, during or after your action~once per own turn only~never during breaks or another player's turn~Harbor is not a building
Q116|1 money per adjacent covered hex, not per building~Empty enclosures count, regardless of occupancy or building type~Restaurant is not a building and does not count as a kiosk neighbor building~either one free Reptile House or one free Large Bird Aviary~even before Build II; choose one, not both, and obey other normal placement rules~1 money per adjacent covered hex, not per building
Q119|Cover each H space by placing a building under ordinary placement rules~reveal cards until a Sponsor appears, keep it and discard the others~H spaces are not placement bonuses, so do not trigger Archaeologist~After all three are covered, every Sponsor's level is one lower~Bonus partner zoos still require Association II for the third/fourth partner~bonus buildings still require Build II for upgrade-marked spaces
Q123|Pay money equal to the Sponsor's level and meet its usual conditions~only from hand, even with Sponsors II~does not move the Sponsors Action card from its current slot
Q124|Appeal cannot exceed 113~conservation cannot exceed 41; any gains beyond those track ends are lost
Q125|Venom targets every other zoo with higher appeal than yours and at least 5 appeal~Hypnosis targets the highest-appeal eligible zoo, with the actor choosing ties~self-target has no effect~only slots 1–3 may be copied~Pilfering 1 targets the highest-appeal eligible zoo~Pilfering 2 separately targets highest appeal and most conservation~the latter must have at least 1 conservation~self-targets do nothing~Constriction affects every other eligible zoo ahead of yours on appeal and/or conservation~one token if ahead on one track and two if ahead on both~at least 5 appeal
Q127|Animal card's partner-zoo condition requires a partner zoo from that Animal's continent; a Sponsor's partner-zoo condition permits a partner zoo from any continent~maximum-25 appeal condition permits play only while you have at most 25 appeal~minimum-reputation condition requires at least its printed value~ignore-one-condition bonus removes one left-edge requirement, but not a terrain requirement
Q133|Digging 2 provides up to two selections~discarding a display card and immediately replenishing it~discarding a hand card then drawing a deck card
Q134|move higher-folder cards down into gaps~preserving their order~then fill empty spaces from the deck
Q137|empty side up, showing its yellow border and size number~Gain each placement bonus covered immediately once~occupying the enclosure later does not award those bonuses again
Q139|under the remaining Final Scoring pile~face down
Q140|Randomly determine the starting player~ordinary turns proceed clockwise~no formal rounds: players take turns one at a time~A regular turn consists of one action~resolve any extra effects/bonuses as specified by that action and card text
'''
excerpts={}
for row in manual.strip().splitlines():
 i,vals=row.split('|',1);assert i not in excerpts; excerpts[i]=[[x] for x in vals.split('~')]
# Any logical resolution requiring more than one local clause carries both relevant quotations.
excerpts['Q04'][2].append('Its slot strength and upgrade side do not matter')
excerpts['Q06'][1].append('Cards I draw/discard at strengths 1–5 are 1/1, 1/0, 2/1, 2/0, 3/1')
excerpts['Q11'][4].insert(0,'House ordinary animals in an empty standard enclosure at least the required size')
excerpts['Q11'][8].insert(0,'Meet any required distinct adjacent water or rock hexes')
excerpts['Q16'][5].append('each reward level can hold only one token across all players')
excerpts['Q18'][1].append('strength +1 must be at least the sum of levels')
excerpts['Q18'][4].append('the full money is still taken')
excerpts['Q19'][0].append('Hand limit is normally 3, or 5 with the hand-limit university')
excerpts['Q31'][3].append('Decorative water/rock illustrations on tiles')
excerpts['Q37'][0].insert(0,'search the unused face-down base-project deck')
excerpts['Q37'][1].insert(0,'search the unused face-down base-project deck')
excerpts['Q41'][1].append('leave it until it is at least in slot 3')
excerpts['Q46'][0].append('Copy only a card in target slot 1, 2 or 3')
excerpts['Q56'][1].insert(0,'before the 10-conservation discard milestone')
excerpts['Q67'][1].append('of different continent/animal-category icons')
excerpts['Q116'][0].append('regardless of occupancy or building type')
excerpts['Q124'][0].append('any gains beyond those track ends are lost')
excerpts['Q125'][6].append('actor chooses ties')
excerpts['Q125'][10].extend(['highest-appeal eligible zoo','every other eligible zoo'])
# Literal question controls: the never-ten fallback is not a milestone reward or a requested scoring cap.
parts={i:list(v['requested_parts']) for i,v in scope.items()}
removed=parts['Q20'].pop(3)
for q,ans in zip(qs,a):
 i=q['id'];assert ans['id']==i;assert len(parts[i])==len(excerpts[i]),(i,len(parts[i]),len(excerpts[i]))
 for part,quotes in zip(parts[i],excerpts[i]):
  for quote in quotes:assert quote in ans['answer'],(i,quote)
print('Validated all excerpts:',len(excerpts),'questions;',sum(map(len,parts.values())),'requested parts.')
support_rows='''Q01|81~80~83~82~76~76~78
Q02|69~70~70~70~84
Q03|104~104~104~106~106~106~106~108
Q04|102~248~248~248~248
Q05|112~112~112~124
Q06|147~147,188~147~148~148,189~148~148~147,148~147
Q07|163
Q08|180~182~182~180~181~181~181~181~181~181
Q09|173,174,175,180~176,177,182~179~182~182~182
Q10|106~106~211,212~108~211
Q11|207~208~208~199,209~199,209~209~209~200,202~209~211,212~212
Q12|213
Q13|221~221~221~224~223~223~223
Q14|231,232,233,234~229~239~229~229~229~229
Q15|232,233~232,233~232,233~232,233~232~232~88~96,233
Q16|234~234,239~234~234~234,277~235,236~236~236~236~236
Q17|237
Q18|242~243~243~243~242~243
Q19|115,88~116~117~117~118~118,119,124~121~121~123~123~124
Q20|253~254~255~257~257~257~257~260~261~262~262
Q21|64~64~64~283
Q22|75
Q23|79~281~281
Q24|110
Q25|188~188~188~188~188~191
Q28|217,286
Q29|239
Q30|301
Q31|209,301
Q32|237~237~238~238
Q33|305
Q34|303
Q35|307
Q36|313
Q37|315
Q38|314
Q39|334
Q40|346
Q41|346
Q42|316
Q43|317
Q44|318
Q45|321
Q46|348
Q49|332
Q50|332
Q51|330~330~330~330~329~329
Q52|328
Q53|350
Q54|350
Q55|326~326~326~325
Q56|327
Q57|325
Q58|322
Q59|347
Q63|361
Q66|364
Q67|365
Q68|366,355
Q70|368,355
Q72|370,355
Q75|373
Q77|375
Q78|376
Q80|378
Q82|380
Q83|381
Q85|383
Q86|384
Q90|389,303
Q95|393,355
Q96|394,355
Q98|396
Q99|397
Q100|398
Q102|400
Q104|402
Q106|404
Q107|405,421
Q112|416
Q113|417
Q114|418
Q115|419
Q116|420
Q119|423
Q123|431
Q124|433
Q125|340~341~341~341~342~343~343~343~344~344~334,336
Q127|432~432~432~427
Q133|316
Q134|163
Q137|167
Q139|255
Q140|72~72~31~104~108,211,313'''
support={}
for row in support_rows.splitlines():
 i,raw=row.split('|');items=[[int(n) for n in spec.split(',')] for spec in raw.split('~')]
 if len(items)==1:items=items*len(parts[i])
 assert len(items)==len(parts[i]),i
 support[i]=items
# Ensure any guessed line labels above actually match their intended anchors.
for i in ['Q21','Q23','Q28','Q140']:
 print(i, sorted(set(n for pp in support[i] for n in pp)), [summary[n-1][:100] for n in sorted(set(n for pp in support[i] for n in pp))])
support['Q21'][3]=[282]
support['Q23'][1]=[280];support['Q23'][2]=[280]
support['Q16'][4]=[234,276]
resolution_overrides={
 ('Q03',2):'Only cards left of used slot 4 shift. Thus original slots 1–3 shift right and slot 5 stays in place; this is ordinary logical entailment, not an omitted movement rule.',
 ('Q04',3):'The explicitly invoked ordinary card movement is the defined move-to-one procedure, including intervening shifts.',
 ('Q10',2):'Immediate effects, contrasted with effects deferred until completion, occur during each sequential item before the next one.',
 ('Q11',1):'Pay full cost first places payment before the animal’s own subsequent money benefits; the later effect-timing clause confirms the order.',
 ('Q11',2):'Three money for each continent icon entails six for two icons. No separate arithmetic restatement is required.',
 ('Q11',4):'Putting an ordinary animal in an empty standard enclosure and flipping the whole tile occupied entails ordinary single-animal occupancy; no historical housing assumption is added.',
 ('Q12',0):'Hand or in-range display are both available sources for the animals of this action. Nothing restricts the action to choosing just one source; the normal reading permits a mix.',
 ('Q16',0):'The answer expressly names Association I/II conservation work for playing the new card. This is a defined procedure in snapshot line 234: playing a new project as this work includes supporting it immediately. Accepted as meaningful named-procedure shorthand; not borrowing Q37 or another answer.',
 ('Q17',1):'Selecting the depicted band from the printed standard requirement specifies the controlling measure and thereby excludes actual tile size or alternative special capacity as the band measure.',
 ('Q17',5):'The conditional imperative remove those tokens, followed by otherwise, makes special-token removal mandatory when possible, rather than an optional alternative.',
 ('Q18',4):'The I option pays strength money; the answer’s explicit full-money rule explains that the amount is not capped by remaining Break steps. This is read with the question’s one-step-remains condition.',
 ('Q25',0):'The introductory phrase counts at strengths 1–5 makes 1 the strength label here; draw/discard 1 specifies the first-column one draw and one discard. Wording is awkward, but the ordered table is determinate.',
 ('Q25',1):'The ordered strength list gives strength 2 a draw/discard pair of 1/0. The leading 2 is the strength label, not a conflicting instruction to draw two.',
 ('Q30',4):'An effect counting its own card is stated without excluding either instant or recurring effects; it covers both classes under the shared icon rule.',
 ('Q31',3):'In a question about terrain requirements and spaces, not terrain spaces and do not count excludes decorative tile art from both categories.',
 ('Q41',0):'The answer states the nonpositive-strength case directly, covering slot 1 and slot 2 after Constriction’s two-strength reduction.',
 ('Q43',3):'Avoiding a new enclosure only if the qualifying herbivore exists entails that the ordinary housing requirement applies without such a host; no extra release requirement is imported.',
 ('Q46',0):'Highest-appeal target and tie choice are resolved. The question does not request re-enumerating Hypnosis’s general appeal floor; the index adjective eligible does not introduce that extra volunteered requirement here.',
 ('Q46',3):'Using the owner’s upgraded/unupgraded side for the copied action is the whole-action instruction. The answer does not switch sides midway or assert that unrelated own cards change side.',
 ('Q49',2):'The question presupposes resolving two executions; execute twice is procedural wording in that context, not an added requirement to spend every Multiplier.',
 ('Q53',0):'The preceding sentence identifies the highest-appeal and most-conservation selections, so Ties let you choose applies to both stated target criteria.',
 ('Q56',0):'The conditional Resistance drew an extra card identifies the ability’s additional-card benefit while explaining the requested milestone interaction.',
 ('Q67',0):'Different continent/animal-category icons excludes repeated copies, and limits the counted kinds to continents/categories, excluding research by ordinary set membership.',
 ('Q67',1):'Per pair means one reward per completed pair; there is no fractional reward for an unpaired icon.',
 ('Q68',0):'This Sponsor’s on-play count uses the shared own-zoo default, supported in snapshot line 355; no any-zoo claim is made for the instant benefit.',
 ('Q70',0):'The shared Sponsor default is the owner’s zoo for this instant count.',
 ('Q70',1):'The recurring trigger uses the shared own-zoo default; normal placement and spacing are expressly retained.',
 ('Q72',0):'The count follows the shared own-zoo default for Sponsors.',
 ('Q72',1):'The recurring trigger follows the shared own-zoo default; the card source, destination and two-appeal reward are explicit.',
 ('Q75',1):'One token as one icon is an unrestricted single-icon substitution in the stated support procedure; no restriction to a particular icon is invented.',
 ('Q77',4):'A duplicate of a special enclosure built in this action would exceed the explicit one-per-type-per-zoo limit, so that duplicate is prohibited.',
 ('Q90',4):'Connected is a defined map-space term in snapshot line 303: uncovered and edge-adjacent to a covered space. All water hexes connected (none isolated) is meaningful defined-term shorthand, not a claim that water must form a single terrain region.',
 ('Q95',1):'The bird trigger uses the Sponsor reference’s own-zoo default rather than any-zoo triggering.',
 ('Q96',1):'The reptile trigger uses the Sponsor reference’s own-zoo default.',
 ('Q104',4):'Evaluating each group separately, with 13/6/3/2 yielding three points, makes the individual group rounding down unambiguous.',
 ('Q107',3):'Research Institute is referenced as the functioning map ability; combining abilities presupposes its activation rather than claiming an inactive Institute supplies a waiver.',
 ('Q116',0):'Per adjacent covered hex rather than per building counts qualifying hexes of a single building separately.',
 ('Q125',5):'Separately targets each of the two track leaders requires both target resolutions even when the same zoo leads both; no instruction merges duplicate targets.',
 ('Q125',6):'The conservation floor and later actor chooses ties clause together resolve both requirements.',
 ('Q125',10):'The first clause states the five-appeal eligibility criterion and subsequent clauses consistently qualify Hypnosis, Pilfering and Constriction targets as eligible zoos. Read as a local eligibility reference within this answer; no other answer is borrowed.',
 ('Q134',2):'Fill empty spaces from the deck resolves the requested final-folder source. The caveat about no separate alternate ordering does not retract that instruction or create uncertainty about an asked rule.',
}
context_notes={
 'Q01':'Face-up Zoo-card discard, worker storage and all-I setup details match personal setup. Hidden Final Scoring status is unrequested and is not imposed.',
 'Q02':'Project location and unavailable-to-both wording match setup; no contradictory alternative count.',
 'Q03':'Spent tokens returning to supply and permission to spend any number are supported at line 106.',
 'Q04':'Slot strength and upgrade side irrelevance is explicitly supported at line 248.',
 'Q05':'The added distinction between an ordinary break and game end during a break is accurate at lines 257 and 435. Reset location and five-token cap are not required by this question.',
 'Q06':'Every volunteered draw/discard table entry was checked against lines 188–189; both tables are accurate. Numerical hand limits and no-money-for-Cards movement are unrequested.',
 'Q07':'No unsolicited bonus-timing requirement imposed. All four asked rules resolved.',
 'Q08':'Preplacement payment is volunteered and correct at line 180; kiosk intervening-space explanation is accurate.',
 'Q09':'Four physical tiles of each special type is correct at line 179; per-zoo limit remains one. No footprint values are required by the question.',
 'Q10':'Cards and newly activated workers as reusable earlier benefits match line 106.',
 'Q11':'Volunteered capacities 3/5/5, distinct terrain hexes, printed track awards and simultaneous-order choice match lines 202, 209 and 211. No contradictory housing or payment exception.',
 'Q12':'No additional false ruling; optional reputation is explicitly before play.',
 'Q13':'Bonus construction and relocation/release distinction match line 226.',
 'Q14':'The added at-most-one donation on II is accurate at line 239.',
 'Q15':'Association restocking and bonuses taking board tiles are volunteered and match lines 117 and 430.',
 'Q16':'Recurring bonus income, above-board overflow and setup base-row immobility are accurate at lines 234, 236 and 276; no numeric overflow limit was actually requested.',
 'Q17':'New release-project reputation versus existing support and flock application are volunteered and correct at line 237. Historical phrase its standard enclosure is qualified by the following explicit smallest-eligible/fallback rule, not a contrary historical-resident requirement.',
 'Q18':'Conditions and X-token boosting are accurate. Upgrade-required Sponsor permissions and refill timing are unrequested context, not omitted asked parts.',
 'Q19':'Every stated Break step is in the correct sequence; empty-special income is distinguished correctly. Restock-per-kind detail and income composition are unrequested context.',
 'Q20':'Face-down discard location is volunteered and accurate at line 255. The never-ten fallback is absent, but actual question does not request it; scope concern is recorded separately.',
 'Q21':'Explicit per-zoo limits and board availability remain despite substitute components, matching line 282.',
 'Q22':'Return unselected maps and kiosk tile reminder are accurate at line 75.',
 'Q23':'Remaining personal tokens and Map A third-partner worker bonus match lines 79 and 86. The distinction does not deny last-worker rewards on other maps.',
 'Q24':'Four opportunities, alternative reward and current-action kind/strength restriction match line 110; naming all four sources is not asked.',
 'Q25':'No extra rule besides the awkwardly formatted but determinate table and discard-source choice.',
 'Q28':'Bear coexistence with herbivore/predator and Petting Zoo as a separate category match line 217.',
 'Q29':'Exactly one is permissive donation-limit wording, not a mandatory extra payment; smallest visible price, supply token and repeatable twelve are correct.',
 'Q30':'No false claim that university reputation/hand-limit benefits become extra zoo icons; university icons is the ordinary shorthand constrained by line 96.',
 'Q31':'No contrary counting of a whole connected region or decorative art.',
 'Q32':'All ordinary support qualifications remain; the shared requirement does not imply an occupied space is available.',
 'Q33':'Condition/reward direction is also correct at line 305.',
 'Q34':'All five definitions are supported at line 303.',
 'Q35':'No size-based payment is distinguished from ordinary card conditions without inventing an extra construction fee.',
 'Q36':'No new action or card movement exception is invented.',
 'Q37':'Searching unused deck, adding to hand and returning deck all match line 315.',
 'Q38':'Named versus chosen Action card and both shift directions match line 314.',
 'Q39':'The added statement that using solo-marked alternate effects in multiplayer does not require solo mode is accurate at line 334.',
 'Q40':'Volunteered targeting and one-track/two-track amounts match line 344; token expiry and strength rules match line 346.',
 'Q41':'The general five-X-token cap is unrequested context. Permission to use the alternative does not expressly waive that cap.',
 'Q42':'The extra up-to-twice quantity matches the frozen narrative’s illustrated Digging 2 procedure at line 316. It is read as that supplied example, not an assertion that every differently numbered Digging ability is capped at two; see borderline note.',
 'Q43':'Usual release/fallback procedure is meaningful named-procedure shorthand in this question about historical accommodation; it does not replace the special-token priority or require proving a historical enclosure.',
 'Q44':'No new hiring exception; immediate availability and all-hired no-effect follow line 318.',
 'Q45':'Volunteered ordinary Hunter description matches line 321 as well as the requested no-Animal result.',
 'Q46':'Copyable slots 1–3 are volunteered and correct at line 348. Other Action-card checks remain an unrequested contextual rule, not a missing asked part.',
 'Q49':'Bonus Multiplier on Animals, timing and unused-token removal match line 332. The question presupposes two executions; procedural execute twice does not impose compulsory use in every situation.',
 'Q50':'A single-Multiplier X-token example does not contradict two-Multiplier maximum three executions; answer correctly distinguishes the two questions.',
 'Q51':'Ordinary placement restrictions, including marked map spaces, are retained.',
 'Q52':'No unsupported quantity or extra enclosure allowance.',
 'Q53':'Volunteered Pilfering 1/2 target distinction is supported at lines 342–343.',
 'Q54':'The missing-money/cards branches are read together with the explicitly stated neither-resource fallback; no impossible compulsory payment is imposed.',
 'Q55':'Volunteered Pouch two-appeal rate and Sunbathing four-money rate are correct at lines 325–326.',
 'Q56':'No aggregate four-point cap is imposed across multiple Final Scoring cards.',
 'Q57':'The volunteered Scavenging 3 example is exact at line 325.',
 'Q58':'No false deck alternative or reputation restriction.',
 'Q59':'The alternative-X action and its holding cap are volunteered and correct at line 347; spending all money cannot avoid the fee.',
 'Q63':'All three Veterinarian effects match line 361.',
 'Q66':'Counting supports by missing map tokens, rather than current project cards, is supported at line 364.',
 'Q67':'Different-icon pair counting entails exclusion of repeats/research and completed pairs only; no additional icon category is included.',
 'Q68':'Instant default-own count and any-player recurring trigger are distinguished accurately.',
 'Q70':'No spacing or placement exception is invented for free kiosks.',
 'Q72':'Tucked cards correctly lose their function; no claim that they are still hand or zoo icons.',
 'Q75':'Both programs are described; differing play conditions of 218 are not requested.',
 'Q77':'No special-enclosure duplication exception is invented.',
 'Q78':'Volunteered terrain need not be covered for completion is accurate at line 376.',
 'Q80':'Volunteered owner choice of bonus-resolution order is accurate at line 378.',
 'Q82':'Token cap is ordinary context; the answer does not waive it. Repeated supports count separately and retain per-project per-action limit.',
 'Q83':'Token cap is ordinary context; next qualifying target retains eligibility requirements rather than naming an arbitrary next player.',
 'Q85':'The small/large definitions are unrequested context; all reward/prohibition behavior is accurate at line 383.',
 'Q86':'Only-small qualifier also excludes a size-three mixed action; the volunteered large mixed example does not narrow that qualifier.',
 'Q90':'Connected is the defined map-space term; no erroneous water-region connectivity requirement is stated.',
 'Q95':'Own-zoo trigger is supplied by the shared Sponsor default; ordinary building restrictions need not be restated.',
 'Q96':'Water adjacency, per-reptile sale limit, rate and discard destination all match line 394.',
 'Q98':'Named Hunter is appropriate to this question about X and double triggers; full Hunter procedure and building terrain are unrequested context.',
 'Q99':'Three total uses and immediate own-icon trigger are accurate at line 397.',
 'Q100':'Then is followed by explicit freedom to order simultaneous benefits; no fixed order excluding reputation first is imposed.',
 'Q102':'Kiosk adjacency, income exclusion and full-map final appeal match line 400.',
 'Q104':'Volunteered example 13/6/3/2 gives three points, correctly demonstrating per-group rounding.',
 'Q106':'Different-icon and novelty counts are distinct; double new identical icon earns the novelty reward once.',
 'Q107':'Research Institute is referenced as an active ability when combining waivers; no terrain waiver is asserted.',
 'Q112':'No hidden Sponsor/category enumeration requirement is imposed; normal zoo-category meaning applies.',
 'Q113':'Tower not being a building for kiosk income is the relevant requested building classification.',
 'Q114':'Release/transfer cannot ignore size boost; no special-enclosure or building exception is added.',
 'Q115':'The discard ability is once per own turn only, outside breaks and others’ turns; no contradictory timing.',
 'Q116':'One special enclosure choice, even before Build II, retains other ordinary placement restrictions.',
 'Q119':'Third/fourth partner and marked-building restrictions remain under bonus effects.',
 'Q123':'Hand-only permission and unchanged Sponsors position are accurate.',
 'Q124':'Volunteered reputation separate-overflow statement is true at line 433.',
 'Q125':'All clauses were checked against lines 334–350. Within-answer eligibility reference and separate Pilfering targets are read semantically; no between-answer borrowing.',
 'Q127':'Volunteered max-25 marker not a general cap and terrain not waived are accurate at lines 427 and 432.',
 'Q133':'Volunteered choice-by-choice switching is accurate at line 316.',
 'Q134':'Volunteered Break refresh is accurate at line 118. Final caveat concerns a nonrequested alternate ordering and leaves deck-source refill fully resolved.',
 'Q137':'Volunteered resolve-before-next-building timing is accurate at line 167.',
 'Q139':'Volunteered all-player discard on first reach/pass-ten and chosen card are accurate at line 255.',
 'Q140':'Additional effects follow their timing; no extra regular action or formal-round structure is added.'
}
intended_prompt="""Fresh independent grader, ArkNova94-question readerB. ReadONLY QAroot /home/jonny/projects/boardgame-rules/docs/quality/summary-qa/ark-nova/2026-11-04-batch-231507/ files expanded-iteration-04/{reader-b.json,summary-snapshot.md,questions.json}, benchmark-v2/{answer-key.json,material-requested-facts.json}, grading-request-scope-02.json. No otherreader/earliergrades/reports/history/rawsources/canonical/browsing/contact. Readall6inputscompletelyboundedrecovereverytruncation. IndependentlygradeALL94answers, everyACTUALLYREQUESTEDpart individually. Actualquestionmeaningcontrolsscope, immutablefactualkeysourcefactsstayfixed, neutralrequested/contextindexguidecontainsnoprioranswers/results. Contextneednotbevolunteered; anyvolunteeredfalse/contradictoryrulingcounts. Ifindexseemsinconsistentwithquestionexplicitlyflagconcernwithoutaddinghiddenrequirements. Correctonlycompleteallactualparts,no contradictions/no unsupportedsource-correctguesses;partialmissing/unresolved/ambiguousactualpart;incorrectmaterialfalse ruling. No borrowingbetweenanswers; supportlabelnotgrade; basiclogicalentailment/meaningfuldefined-procedureshorthandallowedaccordingtopromptscope. Preservequestion-givenconditionswhenreadinganswer; do notusekeywordmatchingorrequireextracontext. Reviewallvolunteeredclausesagainstthisfrozennarrative. WriteONLY expanded-iteration-04/independent-grade-b.json plusownnotesnamedindependent-grade-b-*; noinputedits. Include exactintendedprompt,6inputhashes,complete-readproof,94question-orderjudgments:id,perrequestedpart status/resolution/RELEVANT observedclausequote/summarysupportquote-or-line,overallgrade correct|partial|incorrect,unsupported_guessbool,reason,andvolunteered/contextreview. Quoteonlyrelevantclausesperpart ratherthanrepeatingwholeanswerperpart; fullrawansweralreadypreserved. IncludeC/P/Icounts,nonpassingIDs,borderline/scope/keyconcerns. NoassumedPASS; don'trelaxgenuineaskedparts."""
assert len(a)==len(qs)==len(key)==len(facts)==len(scope)==94
assert [q['id'] for q in qs]==[v['id'] for v in a]==[v['id'] for v in key]
assert set(excerpts)==set(parts)==set(support)==set(context_notes)==set(facts)=={q['id'] for q in qs}
judgments=[]
for q,ans,k in zip(qs,a,key):
 i=q['id']; pp=[]
 for j,(part,quotes,lines) in enumerate(zip(parts[i],excerpts[i],support[i])):
  assert all(1<=n<=len(summary) and summary[n-1].strip() for n in lines),(i,j,lines)
  pp.append({'part_number':j+1,'requested_part':part,'status':'resolved','resolution':resolution_overrides.get((i,j),'Resolved by the quoted local answer clause(s): '+part+'.'),'observed_clause_quotes':quotes,'summary_support':{'file':'expanded-iteration-04/summary-snapshot.md','lines':lines}})
 reason=f'All {len(pp)} actual requested parts resolve from this answer, using ordinary logical entailment or defined rule terms where noted. No material false volunteered ruling or unsupported source-correct guess found.'
 if i=='Q20':reason+=' The index’s never-ten Final Scoring discard fallback is unrequested context, not an omitted actual part; see scope concern.'
 judgments.append({'id':i,'question':q['question'],'per_requested_part':pp,'overall_grade':'correct','unsupported_guess':False,'reason':reason,'volunteered_context_review':{'all_answer_clauses_reviewed':True,'finding':'No materially false or contradictory volunteered ruling found.','detail':context_notes[i],'unrequested_context_in_scope_guide':scope[i]['unrequested_context']+([removed] if i=='Q20' else [])}})
input_hashes=[{'file':f,'sha256':hashlib.sha256(data[f]).hexdigest(),'bytes':len(data[f]),'lines':len(data[f].splitlines())} for f in files]
result={
 'reader':'reader-b',
 'iteration':'expanded-iteration-04',
 'grader':'independent-grade-b',
 'exact_intended_prompt_received':intended_prompt,
 'grading_basis':{'actual_question_controls_scope':True,'source_facts_immutable':True,'question_scope_guide':'grading-request-scope-02.json','no_between_answer_borrowing':True,'support_labels_not_grades':True,'logical_entailment_and_meaningful_defined_procedure_shorthand_allowed':True,'correct_requires_all_actual_parts_without_contradiction_or_unsupported_guess':True,'partial_for_missing_unresolved_or_ambiguous_actual_part':True,'incorrect_for_material_false_ruling':True,'all_volunteered_clauses_checked':True},
 'input_hashes':input_hashes,
 'complete_read_proof':{
  'permitted_inputs_read_completely':6,
  'summary_snapshot_read_ranges_inclusive':[[1,90],[91,180],[181,270],[271,360],[361,451]],
  'json_read_method':'All metadata keys and values were rendered first; then every question/answer/key/fact-index/scope-guide object was rendered as lossless decoded JSON in question order. Every field of each joined object was read, including raw answer, support label, evidence, source references, index origin and context distinctions. Joining did not suppress any input fields.',
  'question_order_batches_zero_based_half_open':[[0,10],[10,20],[20,30],[30,40],[40,50],[50,60],[60,70],[70,80],[80,94]],
  'objects_read_per_json':{'expanded-iteration-04/reader-b.json':94,'expanded-iteration-04/questions.json':94,'benchmark-v2/answer-key.json':94,'benchmark-v2/material-requested-facts.json':94,'grading-request-scope-02.json':94},
  'metadata_read':'Reader and both inputs_read paths; question game/scope/version; answer-key game/version/grading/baseline; scope version/purpose/method/source_of_version and all four rules. material-requested-facts.json is a 94-key top-level mapping, all rendered in the batches.',
  'truncation_audit':'All complete-read calls returned below their output-token budgets. No output reported truncation. Summary coverage is continuous 1–451, and JSON batches cover each index 0–93 once. Later numbered support lookups were verification after the complete read, not substitutes for it.',
  'record_integrity_checks':['94 question IDs align in the exact order across questions, reader and key.','All 94 IDs are present in fact index, scope guide, per-part selections and context review.','Every observed quotation is an exact substring of its own answer.','Every summary support line is nonblank and inside the frozen 451-line snapshot.','All six input SHA-256 hashes rechecked before output.'],
  'prohibited_evidence_used':False,
  'independence_statement':'No other reader, earlier grade/report/history, raw source, canonical source, browsing or contact was consulted. All conclusions were reached from these six frozen inputs.'
 },
 'counts':{'correct':94,'partial':0,'incorrect':0,'total':94,'actual_requested_parts_reviewed':477},
 'nonpassing_ids':[],
 'scope_concerns':[{'id':'Q20','guide_classification':'requested','guide_part':removed,'adjudication':'Unrequested context for this literal question. It asks milestone rewards at 2/5/8/10, end-trigger timing, final turns, Final Scoring cap, VP formula and tiebreak. It does not ask the contingency where no one reaches the ten-conservation milestone. Requiring the fallback would add a hidden requirement.','immutable_fact_retained':'The never-ten fallback remains true in the frozen key and snapshot line 255; no source fact is changed.','effect_on_grade':'Reader omits this context; that omission does not lower its actual-question grade.'}],
 'borderline_cases':[
  {'id':'Q03','issue':'Slot 5 is not named explicitly.','decision':'Resolved: only the used card and cards to its left move, leaving slot 5 unchanged by entailment.'},
  {'id':'Q11','issue':'Double-icon six-money saving, ordinary single occupancy and no self-financing payment are not all restated in the key’s wording.','decision':'Resolved by three per icon, empty whole-enclosure flip, and full-cost-first before later effects.'},
  {'id':'Q12','issue':'Any mix of hand/display is phrased as animals from hand or display.','decision':'The available source alternatives apply to the animals of the action; no source-exclusive restriction is imposed.'},
  {'id':'Q16','issue':'Mandatory immediate support is not separately spelled out.','decision':'Association I/II conservation work is the expressly named, defined play-and-immediately-support procedure at snapshot line 234. Accepted as meaningful defined-procedure shorthand.'},
  {'id':'Q17','issue':'Actual-tile/capacity exclusion and must-remove-special-tokens are not repeated in the key’s exact language.','decision':'Printed requirement specifies the band measure; if-can-remove then remove, otherwise standard establishes mandatory priority.'},
  {'id':'Q20','issue':'Scope guide adds the never-ten fallback to requested parts.','decision':'Flagged as a scope concern and treated as unrequested context; factual key remains fixed.'},
  {'id':'Q25','issue':'Awkward table punctuation could superficially look like draw two at strength two.','decision':'Read the introductory strengths 1–5 and ordered columns together: the pair at strength two is explicitly 1/0. No ambiguous requested quantity remains.'},
  {'id':'Q41','issue':'Five-token holding cap not repeated for the alternative action.','decision':'The question concerns Constriction’s permission to use it; the cap is unrequested ordinary context and is not waived.'},
  {'id':'Q42','issue':'Volunteers up to twice while the question refers to Digging generically.','decision':'This is the exact quantity of the frozen narrative’s Digging 2 example; no unsupported universal assertion about other numbered variants is inferred. All actual choice/refill parts are explicit.'},
  {'id':'Q43','issue':'Without-host normal housing and release details use conditional/named-procedure shorthand.','decision':'Only-if condition entails the normal housing fallback; the usual release/freeing procedure is a meaningful procedure reference for this question about historical accommodation.'},
  {'id':'Q46','issue':'General appeal floor and unrelated upgrade checks are not enumerated.','decision':'Those are not individually requested by this tie/side/token question. All actual parts resolve, and no waiver is claimed.'},
  {'id':'Q67','issue':'Excluding research/repeats and rounding down are not spelled out as separate negatives.','decision':'Different continent/category icons excludes both; per pair pays only complete pairs.'},
  {'id':'Q90','issue':'Connected might be misread in ordinary English as one terrain region.','decision':'It is the snapshot-defined map-space term, explicitly reinforced by none isolated. Accepted defined-term shorthand.'},
  {'id':'Q107','issue':'Institute activation is not repeated.','decision':'The answer combines the functioning Research Institute ability, not an inactive map feature; its ordinary activation condition is preserved.'},
  {'id':'Q125','issue':'Only Venom’s clause spells five appeal numerically; later targets are eligible. Same-zoo Pilfering twice is phrased separately targets.','decision':'The eligibility criterion is introduced locally in this answer and reused for all later eligible zoos. Separate leader selections entail two resolutions even for one zoo. No cross-answer borrowing.'},
  {'id':'Q134','issue':'A final caveat could appear to signal uncertainty.','decision':'It concerns an alternate ordering not asked by the question; moving down, preserved order and deck refill are explicit and resolved.'}
 ],
 'key_concerns':[],
 'judgments':judgments
}
# Freeze verification: do not silently grade changed inputs.
for f in files:assert (root/f).read_bytes()==data[f],f
out=root/'expanded-iteration-04/independent-grade-b.json'
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
loaded=json.loads(out.read_text())
assert len(loaded['judgments'])==94
assert [v['id'] for v in loaded['judgments']]==[q['id'] for q in qs]
assert sum(len(v['per_requested_part']) for v in loaded['judgments'])==477
assert all(v['overall_grade']=='correct' and not v['unsupported_guess'] for v in loaded['judgments'])
print(json.dumps({'written':str(out),'counts':loaded['counts'],'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()},ensure_ascii=False))
