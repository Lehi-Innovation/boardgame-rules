from pathlib import Path
import difflib
R=Path(__file__).resolve().parent;p=Path('rules/nemesis.md');old=p.read_text();s=old
s=s.replace('This summary covers the standard semi-cooperative core.','This summary covers the standard semi-cooperative core using the original manual and the base-game clarifications in the official FAQ v2.2 (16 April 2025; filename v2.1).')
s=s.replace('Once you pass you may perform NO further Actions this Phase (flip your Help card to its "Pass" side).','Once you pass you may perform no further normal Actions this Phase (flip your Help card to its "Pass" side). **Exception: the official FAQ allows Interruption after passing.**')
s=s.replace('Once you pass you sit out the rest of the Phase.','Once you pass you sit out normal rounds for the rest of the Phase (Interruption remains permitted).')
s=s.replace('after passing you sit out the rest of the Phase.','after passing you sit out normal rounds for the rest of the Phase (Interruption remains permitted).')
s=s.replace('**Adult** — all players roll for Noise in order (a player whose Character is in Combat does not roll). Return the token to the bag.','**Adult** — return the token to the bag **immediately before** all players roll for Noise in order (skip Characters in Combat). An Encounter from those rolls may draw that same Adult token (FAQ Rules 7).')
s=s.replace('Unmarked Actions work in or out of Combat.','Unmarked card and Item Actions work in or out of Combat subject to their requirements. **Basic Actions in Combat are limited to Shoot, Melee and Basic Movement as Escape: no Trade, Craft, Pick Up Heavy Object or Quest Item activation.** Room Actions remain forbidden (FAQ Actions 3–5).')
s=s.replace('You cannot Carefully Move if all Corridors connected to the destination already hold Noise markers, and you cannot use it while in Combat.','You cannot Carefully Move if all Corridors connected to the destination already hold Noise markers, and you cannot use it while in Combat. The FAQ clarifies that Careful Movement also replaces automatic Silence/Danger Exploration results with its chosen Noise placement; Reconnaissance cancels those automatic results too.')
s=s.replace('discards the other face down back into that deck.','puts the other face down at the **bottom** of that deck (FAQ Actions 6).')
s=s.replace('and discards the other face down back into that deck.','and puts the other face down at the **bottom** of that deck (FAQ Actions 6).')
s=s.replace('but they may harm them indirectly:','but they may harm them indirectly:')
s=s.replace('resolve an Intruder Attack — one separate Attack per Intruder in the Room.','resolve an Intruder Attack — one separate Attack per Intruder in the Room, starting with the larger ones (Queen, Breeder, Adult, Larva; FAQ Rules 5).')
s=s.replace('While waiting: you may launch at the start of your first round in each Player Phase, or exit voluntarily (free, no Action — place your miniature back in the Room for that Pod); if you don\'t launch in your round, you automatically pass the turn.','Entering and waiting passes the current turn. At the start of your first round in the **next Player Phase**, choose: stay and pass; launch; or exit for free into the corresponding Section Room and play a full round of 2 Actions (FAQ Rules 2). Waiting Characters count as present in that Room for Noise rolls from bag development (FAQ Rules 1). A later Malfunction in the Section does not affect a Character already in a Pod: launching, waiting and exiting remain possible; it only blocks new entry (FAQ Rules 3).')
s=s.replace('On any **yellow** space: the sequence can no longer be aborted, and all Escape Pods unlock instantly (they can be re-Locked).','At the **first yellow** space: the sequence can no longer be aborted, and all Escape Pods unlock instantly. They can be re-Locked; subsequent yellow spaces do not unlock them again (FAQ Rules 25).')
s=s.replace('when the Self-Destruct marker reaches any **yellow** space, all Escape Pods unlock automatically (they can be Locked again)','when the Self-Destruct marker first reaches a **yellow** space, all Escape Pods unlock automatically (they can be Locked again; later yellow spaces do not unlock them again)')
s=s.replace('You cannot start Self-Destruct while any Character is hibernating.','Characters cannot start Self-Destruct while any Character is hibernating; the **Coolant Leak Event can** start it despite sleepers (FAQ Rules 14).')
s=s.replace('— initiate (or stop) the Self-Destruct sequence (cannot start while anyone is hibernating).','— initiate (or stop) the Self-Destruct sequence (Characters cannot start it while anyone is hibernating; Coolant Leak Event is an exception).')
s=s.replace('all Escape Pods unlock instantly (they can be re-Locked).','all Escape Pods unlock instantly (they can be re-Locked; later yellow spaces do not re-unlock them).')
s=s.replace('A Malfunction makes a Room\'s Computer unavailable.','A Malfunction makes a Room\'s Computer unavailable. Malfunction markers cannot be placed in unexplored Rooms, whereas Fire markers can (FAQ Rules 22).')
s=s.replace('**Infest (Larva attack):** a Larva does not draw Attack cards. Instead: remove the Larva miniature from the board and place it on the target\'s Character board (on the miniature picture), and the target gains 1 Contamination card.','**Infest (Larva attack):** a Larva does not draw Attack cards. Instead: remove the Larva miniature from the board and place it on the target\'s Character board (on the miniature picture), and the target gains 1 Contamination card. If the target already has a Larva, the attacking Larva disappears, the existing one stays, and the Character only gains the Contamination card; this attack does not automatically kill them (FAQ Rules 12).')
s=s.replace('If you die, your Corpse stays','If you die, your Corpse stays')
# Add base-game FAQ details in a sourced section, using exact labels rather than unsupported card inference.
faq='''## FAQ & Rulings

The [official Nemesis FAQ](https://awakenrealms.com/images/download/Nemesis/ENG/Nemesis_FAQ_v2.1.pdf) identifies itself as **v2.2, 16 April 2025**. Only its base-game Rules, Actions, Rooms and Items sections apply here; cooperative, Intruder-player and expansion rulings are excluded. These clarifications take precedence over ambiguous manual wording.

### Rounds, events, damage and Intruders

- An empty hand does **not** automatically make you pass after completing 2 Actions. Wait for your next round to pass; that extra round can incur another Fire or Bleeding effect (Actions 18). Interruption may still be played after passing, but it requires being in the same Room as the Character performing the interrupted Action; a remote Order via Intercom cannot be Interrupted from elsewhere (Rules 21; Actions 17).
- Remove an Event that says to remove itself even when its other effect cannot resolve (Rules 6). Discarded/dead Intruder tokens return to the unused token pool and remain reusable; they are not removed permanently (Rules 19).
- A retreating Intruder meeting a Closed Door destroys it and stays. With **The Way of Moving** Weakness, an affected Intruder other than a Breeder or Queen instead does nothing at that Door (Rules 8).
- **Vulnerability to Fire** gives 1 additional Injury per damage instance (x + 1), rather than per individual Injury. A Flamethrower double-crosshair hit therefore deals 3 Injuries; Fire in the Nest destroys 2 Eggs per Fire Damage step with this Weakness (Rules 11; Rooms 7).
- A sleeper takes no later Fire wounds in the Hibernatorium, though ship destruction and the endgame survival checks still matter (Rules 13). Destruction of the ship fulfills kill-Queen/destroy-Nest requirements; your Character must still survive and fulfill their Objective (Rules 26).
- Two Light Wounds suffered while already at 2 Light Wounds become 1 Serious Wound plus 1 remaining Light Wound (Rules 23). On death in standard play, Heavy Objects drop in the Room, while Item cards disappear from the game (Rules 24).

### Actions and character abilities

- Empty Actions that make no meaningful game-state change should be disallowed, including starting Trade with no intention of exchange. Honest negotiations may end with no trade. Any Characters in the Room can trade with each other, including pairs who did not initiate/pay (Actions 1–2).
- Quest activation is a Basic Action printed on its card, forbidden in Combat but allowed in a Malfunctioning Room (Actions 3; Items 10). The Hand Serious Wound does not increase Basic Shoot cost, and does not affect Scout's Motion Scanner, which is a unique reaction rather than an Item Action (Rules 9; Items 7).
- **Covering Fire:** Soldier may use it for themselves alone. Both moving Characters go in the direction of their choice, then perform one Noise roll; an Encounter checks Surprise against Soldier (Actions 7).
- **Full Auto:** remove all Ammo, perform one Shoot Action; damage adds the Shoot result, half discarded Ammo rounded down, and the Assault Rifle's +1 bonus (Actions 8).
- **Nerves of Steel:** you may see the Intruder Attack card before choosing it. It can protect Soldier when another Character triggered a Surprise Attack, but only Soldier benefits; other Characters still take effects such as Frenzy (Actions 9–10).
- Captain cannot use **Order** while personally in Combat. Intercom may make someone else Move out of Combat, applying normal Escape. **Motivation with Intercom** affects all Characters in Rooms with a Computer as well as all Characters in Captain's Room (Actions 12–13).
- Entering via **Technical Corridors** Action or **Technical Corridor Plans** ignores a Door Exploration token because the entry Corridor cannot be determined (Actions 14).
- **Rest** with no Larva before the Action cannot kill you merely because several scanned cards are Infected: place just 1 Larva. Rest can be fatal if a Larva was already on the board before it (Actions 19).

### Rooms, Eggs and Items

- Storage's Room Action works repeatedly even with its Item Counter at zero, paying the normal cost and obeying normal Room restrictions. Its counter limits only the Search Action card (Rooms 6).
- Intranet research still requires the **Object itself in the Laboratory**, regardless of Scientist's location. Research means Analyse; the Object is retained, including for Objectives (Rooms 3–4).
- Throwing a Grenade/Molotov at Nest Eggs from another Room makes you roll Noise in **your own Room**, not the Nest. An Egg taken from the Intruder board and dropped back in the Nest is a normal Heavy Object and does not restore the Nest's Egg total/hit points (Rooms 2, 9).
- Smoke Grenade's affected player chooses and discards 1 Action card from their hand (Items 1). Medkit and Bandages may be used on other Characters (Items 2).
- Energy Charge cannot directly reload another Character's Weapon: trade them the Charge so they use it in their own round. Adding Extended Magazine or Auto Loader to a used/empty Energy Weapon immediately grants extra Ammo. A newly Crafted Flamethrower starts **fully loaded**, rather than the one Ammo of a searched Weapon (Items 3, 5–6).
- Alcohol's Infected scan does not place a Larva; instead gain a new Contamination card (Items 4).
- **Antidote:** scan all your Contamination cards in hand, deck and discard; remove all Infected cards from the game, gain 1 new Contamination card, and reshuffle that new card with non-Infected scanned Contamination and Action cards, except cards retained in your hand. Then pass; you may keep hand cards. Surgery instead shuffles the entire hand too and does not give a new Contamination card, while applying its own Larva removal and 1-Light-Wound cost (Items 9; Rooms 1).

'''
s=s.replace('## Player Reference\n\n',faq+'## Player Reference\n\n')
(R/'repair-06-faq.patch').write_text(''.join(difflib.unified_diff(old.splitlines(True),s.splitlines(True),fromfile='manual-only',tofile='manual-plus-official-FAQ')));p.write_text(s)
print('updated',len(s))
