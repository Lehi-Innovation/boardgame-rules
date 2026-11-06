# Nemesis expanded bank v4

Reference-only correction of v3. All question wording and expected-answer strings preserved.

## Q01

In a four-player standard game, how many Escape Pods are selected, how are they distributed and oriented, and which tokens start in the Intruder bag?

**Expected:** Three random pods; lowest numbered in A, next B, next A, all Locked. Bag: 1 Blank, 4 Larvae, 1 Creeper, 1 Queen, 7 Adults.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "467-507"}]

## Q02

How are Objectives filtered and dealt, when does each player choose one, what happens to the rejected card, and do Eggs trigger that choice?

**Expected:** Remove Objectives requiring more players than present; deal one Personal and one Corporate secretly. First Intruder miniature of any type appearing triggers immediate choice by everyone before resolving its Encounter. Remove rejected card face down unseen. Eggs do not trigger it.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "589-602;1008-1028"}]

## Q03

You use an Action card with printed cost 2 while holding that card, two other Action cards and two Contamination cards. What is discarded, and can Contamination substitute for payment? What if the card offers OR effects?

**Expected:** Discard the played card and two additional Action cards face up. Contamination cannot pay costs. Choose one OR effect.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "987-998;1235-1250"}]

## Q04

A Character in a burning Room takes one Action then passes. When do they take Fire damage, can they act again this Player Phase, can they discard cards, and do later players rounds burn them again?

**Expected:** At end of their own round take 1 Light Wound. Passing bars further Actions this Phase and allows discarding any number from hand. No further Fire wounds from later players rounds this turn.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "723-747;1545-1565"}]

## Q05

Describe entering an empty unexplored Room: tile, Item Counter, Exploration effect, Noise roll and token destination. How do Silence, Danger and an already occupied destination alter the Noise roll?

**Expected:** Reveal Room and Exploration token; set counter to token number except Nest/Slime Room; resolve effect and remove Exploration token from game. Roll Noise in empty Room unless Silence or Danger exploration cancels it. Occupied Room (Character or Intruder) gives no movement Noise roll.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "1288-1300;1336-1353;1430-1473"}]

## Q06

What does Careful Movement cost and replace, when is it forbidden, and can a Closed Door be crossed or a miniature stop in a Corridor?

**Expected:** Cost 2 Action cards; replaces post-movement Noise roll with placing Noise in a chosen connected Corridor. Forbidden in Combat or when all destination Corridors have Noise. Closed Doors block player movement; no miniature stops in Corridors.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "1150-1168;1260-1285;3038-3041"}]

## Q07

You roll a number for a Corridor already holding Noise, with a Technical Corridors Entrance in your Room. Give the Encounter sequence, Noise removal, token destination and Surprise Attack comparison; do Contamination cards count?

**Expected:** Resolve Encounter: remove all connected Noise including Technical Corridors; draw bag token; place matching Intruder; compare token number to all cards in triggering hand including Contamination. Fewer cards causes Surprise Attack against triggerer, equal or more does not. Set token aside.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "1380-1389;1685-1720;1778-1794"}]

## Q08

How does Danger resolve with several eligible neighboring Intruders, and when none are eligible? Does moving an Intruder into your Room count as an Encounter? How does Slime affect Silence?

**Expected:** Move all neighboring Intruders not in Combat into current Room. If none eligible, put Noise in each connected Corridor lacking it including Technical Corridors. Moving Intruder into occupied Room is Combat, not Encounter. Slime converts Silence Noise/exploration results to Danger.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "1392-1411;1437-1454;1528-1542;1682-1684"}]

## Q09

During an Encounter you draw Blank. What happens to Noise and the Blank; when is an Adult added? Contrast Blank in bag development.

**Expected:** Encounter replaces connected Noise in every Corridor; return Blank; add Adult only if Blank was last token in bag and a spare Adult is available; no miniature or Surprise Attack. Development always attempts adding one available Adult then returns Blank.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "815-821;1721-1731"}]

## Q10

Two Intruders attempt to move together from the same Room through one Closed Door. Where do they end, what happens to the Door, can it later close, and would a Noise-triggered appearance be blocked by that Door?

**Expected:** Both stay in original Room and destroy Door simultaneously. Destroyed Door permits movement but cannot close except Plasma Torch. Noise-triggered appearance ignores Closed Door.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "1640-1673"}]

## Q11

An injured Intruder moves into Technical Corridors with Noise already there. What happens to its miniature, injuries, token and Noise? Can Characters or Doors normally use those Corridors?

**Expected:** Remove miniature, discard injuries, return matching token to bag; keep Noise. Characters barred except Mechanic Technical Corridors card and Technical Corridor Plans Item; Doors never placed there.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "1475-1507"}]

## Q12

Describe an ordinary Shoot versus Melee Action: card/ammo costs, target location, Contamination, a miss, and the two-hit die result.

**Expected:** Both cost 1 Action card against target in same Room. Shoot needs Weapon in Hand and spends 1 Ammo; normal two-hit deals 2 injuries subject to Weapon. Melee draws Contamination to Action discard before choosing target, miss causes Serious Wound, two-hit deals only 1 injury.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "1751-1776;1795-1806;1816-1839;3076-3091"}]

## Q13

After damage, how are Larva, Adult and Queen death checked, when is a Carcass placed, and what if a Queen check draws a Retreat arrow?

**Expected:** Larva dies at 1 injury without Carcass. Adult draws one Attack card blood, dies if blood <= current injuries and leaves Carcass. Queen draws two, sums blood and compares same way; any Retreat arrow causes retreat via Event-card corridor number, discard Event, rather than normal numerical resolution.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "1976-2033;2247-2252"}]

## Q14

A Character Escapes a Room with two Intruders toward an empty unexplored Room. When do attacks occur, who is targeted, what happens if they die, and what follows if they survive?

**Expected:** Pay Movement cost 1, choose neighboring Room. Before moving resolve separate Attack from each Intruder targeting escaper. Death leaves Corpse in starting Room; survival completes move and standard exploration/Noise.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "1841-1865;1898-1903"}]

## Q15

In an ordinary Intruder Attack with several Characters, how is the target chosen and ties broken; how is a hit determined; what changes for Larva and where does its Contamination go?

**Expected:** Fewest Action cards in hand; tie First Player or next in turn order. Matching attacker symbol on drawn Attack card means resolve effect; otherwise miss; ignore blood and discard card. Larva draws no Attack card: place miniature on target Character board and give Contamination on top of Action discard.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "1874-1953"}]

## Q16

At three Serious Wounds, does dressing one prevent death from a Light Wound? What happens at a third Light Wound otherwise, what does Heal remove, and where do a dead Characters Corpse and Heavy Objects go?

**Expected:** No: dressed still counts; any further Wound kills at three Serious. Third Light clears Light track and causes Serious Wound. Heal removes specified Light Wound or discards dressed Serious card. Place Corpse and drop Heavy Objects in death Room.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "2035-2089"}]

## Q17

Contrast Canteen/Shower scanning with Surgery: which cards are scanned and removed, how is a Larva handled, and what costs or turn consequences follow Surgery?

**Expected:** Canteen/Shower optionally scan hand Contamination, remove non-Infected; infected gives Larva and retains card, existing Larva means death/Creeper. Canteen heals 1 Light; Shower removes Slime. Surgery scans deck/hand/discard, removes infected and Larva, then 1 Light Wound, automatic pass, shuffle all cards including hand into deck; empty hand until next turn.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "2135-2150;2556-2566;2606-2621;2669-2682"}]

## Q18

How can uncarried Eggs be destroyed with Shoot/Melee, grenades, Molotov and Fire; which Melee penalties are waived, when is Noise rolled and when is the Nest destroyed?

**Expected:** Each injury from Shoot/Melee destroys 1 Egg. Egg melee draws no Contamination and causes no missed-attack wound. Grenade 2 Eggs, Molotov 1; Noise after every destruction attempt including miss. Fire destroys 1 uncarried Egg in Fire Damage. Nest destroyed when all Eggs taken/destroyed; mark Injury in Nest.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "2623-2662"}]

## Q19

What permits or prevents entering an Escape Pod, what must you resolve first, how many Characters and Heavy Objects fit, and what are the options and consequences when you wait?

**Expected:** Use corresponding Evacuation Room Action cost 2 with unlocked pod and free space, no Intruder or Malfunction; roll Noise first and fail if Intruder reaches Room. Two Character spaces; Objects use none. Enter then launch immediately or wait; launch at first-round start in later Player Phase, voluntary free exit during round, no launch automatically passes. Intruder appearing in Section returns all pod occupants to Room; another boarder may launch immediately.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "2443-2463;2684-2737;3045-3047"}]

## Q20

Give the endgame checks in order. What happens with two Damaged Engines, a non-Earth destination (including Quarantine/Mars), and an infected survivor or one carrying a Larva? Do pod passengers need Contamination checks?

**Expected:** Engines then Coordinates then Contamination then Objectives. If ship survives to checks: two/three Damaged explodes kills all aboard incl Intruders; non-Earth kills sleepers but ship/Intruders survive, Quarantine sleeper survives Mars. All survivors including launched pod passengers scan all Contamination; any infected triggers shuffle all Action/Contamination draw 4, any Contamination kills else survives. Larva skips scanning and directly does shuffle/draw. Survivors then reveal/check chosen Objective.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "900-958"}]

## Q21

How are the basic and additional Room tiles and Exploration tokens placed at setup; what Coordinates, Destination, Time, Engines, Eggs and Weaknesses start on the board?

**Expected:** All 11 basic tiles face down in 1 slots; five random additional tiles face down in 2 slots, leftovers boxed unseen; random face-down Exploration per tile. Random face-down Coordinates, Destination B, Time green. Each numbered Engine has shuffled Damaged/Working pair face down, top true status. Five Eggs, three random face-down Weaknesses.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "438-550;2420-2422;2525-2527"}]

## Q22

How are Player Numbers assigned and Characters drafted; what does each Character receive and where do Characters and the initial Corpse begin? Are Quest Items usable immediately?

**Expected:** Random Help cards 1 through player count with matching Inventories assign Player Numbers; in number order draw two draft cards, reveal, choose one, shuffle other back. Receive board, ringed miniature in Hibernatorium, shuffled 10 Action cards, starting Weapon in Hand fully loaded, two horizontal inactive Quest Items; activate by printed quest then ordinary Items. Player 1 First Player; blue Corpse in Hibernatorium is Character Corpse Object.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "571-655;2374-2382"}]

## Q23

When are Action hands refilled and the First Player token passed; what happens when the Action deck empties, and what are the normal discard destinations and visibility?

**Expected:** At Player Phase start draw to 5, shuffle Action discard whenever required draw finds empty deck; then pass token left except first turn. Actions/Contamination to own Action discard, Items/Event/Attack/Serious Wounds to respective discard piles face up; markers to pools. Search example has explicit face-down return exception.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "677-688;703-721;2330-2339"}]

## Q24

Give the Event Phase order, which Intruders move on an Event card, what controls movement and when the event effect resolves; what happens when Event and Intruder Attack decks run out?

**Expected:** Time and active Self-Destruct advance, Intruders in Combat attack, Fire Damage, Event card movement then effect, bag development fully resolved before next turn. Move symbol-matching Intruders without Characters in Room via card-number Corridor; ducts remove miniature/return token. Discard Event unless instructed otherwise. Empty Event/Attack decks reshuffle their respective discard piles.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "750-838;1918-1920"}]

## Q25

In bag development, describe Larva, Creeper, Adult, Breeder and both Queen branches. Which tokens are removed or returned, who rolls Noise and when does the next turn begin?

**Expected:** Larva removed replaced by Adult; Creeper removed replaced by Breeder. Adult/Breeder all players in order roll Noise except in Combat then drawn token returned. Queen: Characters in Nest means place Queen and resolve Encounter; otherwise including undiscovered Nest add Egg; return Queen. Fully resolve all triggered Encounters/Surprise Attacks before new turn.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "787-829"}]

## Q26

When do Fire and Malfunction exhaustion end the game; what if the target Room already has that marker, and where do removed markers go? What happens to sleepers and Intruders when hull integrity is lost?

**Expected:** Eight of each; required new placement with no pool marker explodes/loses hull integrity, all aboard including sleepers/Intruders die. Existing same marker means nothing happens; max one per Room. Removed markers return to pools.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "879-896;1545-1630"}]

## Q27

What does a Malfunction disable and leave usable, where can it never be placed, and does it change an Engine token or harm an already-hibernating Character?

**Expected:** Disables Room Action and Computer; Search still works. Never in Nest or Room Covered In Slime. Special Rooms can malfunction; Engine Working/Damaged unaffected and already-hibernating Characters unaffected. Repair cards/Tools can remove marker.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "1587-1630"}]

## Q28

Which Items may be hidden, what do other players see, what is the Inventory limit, and what must happen on use? How are Heavy Items/Objects, added Items and Duct Tape handled?

**Expected:** Normal Items hidden in unlimited Inventory, others see backs/colors; used Item shown. Heavy Items/Objects public in two Hands, third requires dropping one. Added Items act as one with base card. Duct Tape combines two Heavy Items into one Hand, never Objects.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "2200-2246"}]

## Q29

What happens to an Item versus an Object voluntarily dropped, when and at what Action cost may you drop, and how do found Weapons differ from starting Weapons in Ammo?

**Expected:** Drop freely during own turn no Action; Objects stay in Room, Items discarded/lost. Found Weapon has 1 Ammo versus starting fully loaded, neither exceeds capacity.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "632-635;2232-2235;2270-2276"}]

## Q30

How does Search choose its deck, draw and keep cards, return the rejected card, change the Item Counter, and handle zero Items, Special Rooms and Blue Items?

**Expected:** Search Action card: draw two matching Room color Red/Yellow/Green, white choose one of three; keep one, rejected face down back into same deck per example. Counter reduced one, zero bars Search except e.g. Scavenging. Special Rooms cannot Search; Blue crafted never Search.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "2330-2373;2741-2749"}]

## Q31

How does Craft pay its Action and components, must the result be available, can you inspect the deck, and what Crafted Items exist?

**Expected:** Cost one Action card plus discard two Items with blue component icons matching two grey result icons, choose/take available card not random draw; unavailable cannot build. May inspect deck any time. Antidote, Taser, Flamethrower, Molotov Cocktail.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "1203-1210;2283-2329;3038-3041"}]

## Q32

Who pays for a Trade and who may join; can you give something for nothing, exchange Ammo, or need a separate Pick Up Action for a searched Heavy Item?

**Expected:** Initiator pays one Action card; Characters in same Room may agree to exchange Items/Objects including gifts. Cannot exchange Ammo. Pick Up Heavy Object cost one applies Corpses/Carcasses/Eggs, not searched Heavy Items.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "1180-1202;3038-3041"}]

## Q33

How do you reveal Weaknesses: what Object corresponds to each card, where must it be, is it consumed, who benefits and must you personally research for a Discover Weakness Objective?

**Expected:** Character Corpse, Intruder Egg, Intruder Carcass correspond to three face-down slots. Research matching Object present in Laboratory, carried or uncarried, reveal and leave card on board, Object not consumed. Discovered rules benefit all; anyone can do research for Objective.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "1102-1120;2090-2121;2506-2518"}]

## Q34

What are the common prerequisites and cost for Room Actions, what does a Computer icon itself do, and how does Fire affect Room Actions or Searching?

**Expected:** Cost two Action cards, Character in matching Room unless explicit special ability, no Combat or Malfunction. Computer icon only significant when another rule references it, unavailable under Malfunction. Fire alone bars neither Room Action nor Search.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "1584-1586;2405-2422;3045-3047"}]

## Q35

What exactly does the Armory recharge, by how much, and what limits apply?

**Expected:** Add two Ammo to one Energy Weapon, never Classic Weapons, never above printed capacity.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "2423-2429"}]

## Q36

What are the three mutually exclusive Emergency Room treatments; does dressing remove the Wound or merely its effect, and do identical Serious Wound effects stack?

**Expected:** Dress all Serious OR heal one dressed Serious OR heal all Light. Dress flips/ignores effect but retains Serious count; identical Serious effects do not stack.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "2068-2089;2437-2442"}]

## Q37

What does sending a Signal actually do and what is its game use; can Comms be absent from a normal game?

**Expected:** Comms Room Action puts Status marker on own Signal space, used for Objectives only. Basic Room so always aboard.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "1087-1092;2420-2422;2430-2436"}]

## Q38

How does Fire Control affect a chosen Room and its Intruders if the Room has Fire, or has none?

**Expected:** Choose any one Room, remove Fire if present; all its Intruders flee random directions, one Event card drawn per Intruder. Works with no Fire.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "2464-2475"}]

## Q39

Describe starting, stopping and restarting Self-Destruct, advancing it, the yellow threshold, its final space, a jump while active and a Character already hibernating.

**Expected:** Start marker first green, advance one whenever Time moves. Stop removes marker; restart green. Yellow irreversible and unlocks all pods but they can relock. Skull explodes; hyperspace jump with active sequence still destroyed. Cannot start if anyone hibernating.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "2476-2505"}]

## Q40

Which Room can Airlock Control target, what Door condition is required, what happens immediately, and what cancels or completes the procedure and when?

**Expected:** Any other Yellow Room with no Destroyed Doors in connected Corridors; close every connected Door, mark procedure. Opening any before Player Phase end removes token/cancels. All closed after all players pass kills all Characters/Intruders immediately, remove token and Fire.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "2528-2547"}]

## Q41

When does Cabins increase a hand and to what size; what disables it and is it a paid Room Action?

**Expected:** Passive at start of new turn draws to six instead of five if Character there and no Intruders; Malfunction disables. No paid Action.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "2548-2555"}]

## Q42

Can Command Center select a distant Room and individually open some Doors and close others, including a Destroyed Door?

**Expected:** Choose any one Room and individually open/close any connected Doors, need not all same. Destroyed Door cannot close except Plasma Torch.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "1654-1660;2567-2573"}]

## Q43

What can Engine Control Room check or change and how do Malfunctions in an Engine Room affect that check?

**Expected:** Check status of all three Engines even if corresponding Engine Room malfunctions; cannot change status from Control Room.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "2574-2583"}]

## Q44

What does Hatch Control System change and how does Monitoring Room inspect a location: explored or unexplored, what components, secrecy and replacement?

**Expected:** Hatch flips one Pod Locked/Unlocked. Monitoring secretly looks at one unexplored Room tile and its Exploration token, replaces both, may lie.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "2584-2598"}]

## Q45

Does entering Room Covered With Slime require an Action to acquire Slime, can it have an Item Counter or Malfunction, can Slime stack, and does showering extinguish Fire?

**Expected:** Entry automatically gives Slime; no paid Action. No Item Counter, never Malfunction. Max one Slime, extra does nothing; Clothes/Shower remove. Shower does not remove Fire and Fire allowed there.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "1351-1353;1528-1544;1599-1601;2599-2621"}]

## Q46

In Cockpit what can you learn or change, who sees the information, what does Destination refer to and which restrictions apply after someone hibernates or an Intruder is present?

**Expected:** Check Coordinates secretly and replace, may lie and should remember; Set Destination moves marker to chosen track space referring to one of four card destinations. No Set with Intruder in Cockpit; no change after any hibernation; common Room prerequisites apply.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "2750-2773"}]

## Q47

How does Engine checking differ from repairing/breaking; what can stay secret, what must be announced and do you need a prior check or functioning Engine Room?

**Expected:** Check secretly top token only may lie. Repairs Action or Tools permits take both tokens secretly restack any order. Need announce whether order changed, not whether repaired. Works without prior check and despite Malfunction. Top true status, two Working needed.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "2774-2808"}]

## Q48

When is hibernation legal, what roll and failure condition apply, what leaves play on success, and which later ship actions are forbidden? Does later Malfunction wake sleepers?

**Expected:** Only Time on blue, functioning Hibernatorium without Intruder; Room Action cost two, Noise roll, appearing Intruder fails. Success remove Character miniature and participation until end checks. Destination change and starting Self-Destruct prohibited. Later Malfunction has no effect on sleepers.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "1608-1611;2809-2834"}]

## Q49

What ends the game when Time runs out or the last active Character leaves/dies/hibernates; how is an active Self-Destruct resolved and do Intruders die from a normal jump?

**Expected:** Time final red immediate jump, awake aboard die; Intruders unharmed. Last alive non-hibernating aboard leaves/dies/hibernates: advance active Self-Destruct to final red and destroy ship, else advance Time final red and jump. Then survival/victory checks if survivors.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "869-899"}]

## Q50

Can a Character directly attack another, and may an Action still harm other crew indirectly? Give source-supported examples.

**Expected:** Never directly attack Characters; indirect harm permitted, e.g. grenade at Intruder with crew present, trap in burning Room, Self-Destruct.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "2383-2403"}]

## Q51

You must place an Adult but all eight models are on board. What explicit procedure applies, and what if an Intruder enters an unexplored Room by movement?

**Expected:** Remove Adults not in Combat and return corresponding tokens to bag if possible, then place Adult in Encounter Room. Moving Intruder into unexplored Room does not reveal Room/token and is not removed.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "1412-1429"}]

## Q52

For shooting, describe the target-size restrictions of the small curled and larger curved Intruder die symbols; what happens on those same symbols in Melee against an ineligible target?

**Expected:** Small curled symbol hits Larva/Creeper for one only; larger curved hits Larva/Creeper/Adult for one only; other targets missed. Same target restrictions in Melee; miss causes Serious Wound.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "1755-1776;1816-1839"}, {"path": "nemesis-original-rules.pdf", "printed_pages": [18, 19], "basis": "Visual inspection of matching original-edition diagram/icons"}]

## Q53

At the final Contamination check, a survivor has no Larva and every Contamination card scans non-Infected. Must they perform the four-card draw or remove those cards, and does an earlier launched Pod escape the Objective check?

**Expected:** No four-card draw unless infected found or Larva on board; end scan does not instruct removing non-infected. Pod passenger still needs surviving Contamination check and chosen Objective fulfillment.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "935-958;2712-2720"}]

## Q54

Which two component symbols are required for each Crafted Item: Antidote, Taser, Flamethrower and Molotov Cocktail? Describe the symbols rather than guessing Item-card names.

**Expected:** Antidote: flame and medical cross. Taser: battery/lightning and wrench/tool. Flamethrower: flame and wrench/tool. Molotov Cocktail: flame and folded cloth/fabric. Each takes two matching blue-component Item cards.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "2283-2329"}, {"path": "nemesis-original-rules.pdf", "printed_pages": [23], "basis": "Visual inspection of matching original-edition diagram/icons"}]

## Q55

What defines being in Combat, how do In Combat Only and Out of Combat Only restrictions work, and may an unmarked Action or Item be used in either situation? Do Eggs cause Combat?

**Expected:** Sharing Room with Intruder defines Combat, not Eggs. In Combat Only requires Combat, Out of Combat Only requires none. Unmarked may be used in or out of Combat, subject to its other requirements.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "1129-1143"}]

## Q56

For an Objective that Player X cannot survive, must you personally kill them, does hibernating or escaping count as death, and how does only survivor differ? What must your own Character do regardless?

**Expected:** X must be dead at game end; need not be killed by own Actions; hibernating or escaping alive is not death. Only survivor means nobody else survives. Own Character must survive by launched Pod or successful hibernation, plus meet Objective.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "1057-1086"}]

## Q57

If a Door token must be placed and none are in the pool, what happens? How are Open, Closed and Destroyed Doors represented, and may two Door tokens share one Corridor or be placed in Technical Corridors?

**Expected:** Take any Door token elsewhere on board and move to required Corridor. Open no token, Closed standing, Destroyed lying. Max one per Corridor; none in Technical Corridors.

Source: [{"path": "extracted/nemesis-rules.txt", "extraction_lines": "1499-1500;1631-1673"}]
