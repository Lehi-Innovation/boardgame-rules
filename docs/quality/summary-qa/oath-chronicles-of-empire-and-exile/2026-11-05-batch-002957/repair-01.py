from pathlib import Path
import json,shutil,hashlib,difflib
P=Path(__file__).resolve().parent;s=Path('rules/oath-chronicles-of-empire-and-exile.md');t=s.read_text()
t=t.replace('Draw up to 3 available cards.','Draw 3 cards, taking fewer only if the source runs out, a world-deck Vision stops you, or a modifier reduces the draw. You cannot voluntarily stop early.')
t=t.replace('Up to 3 cards; world Vision stops draw','Draw 3 unless a stop/reduction applies; world Vision stops draw')
t=t.replace('discard an adviser. Faceup advisers','discard an adviser, subject to locked cards. If the incoming card changes the adviser limit, check against the new limit before playing it; use the lowest of multiple limits. Faceup advisers')
t=t.replace('starting anywhere and moving away from world deck through banks, wrapping.','starting at any chosen bank, then moving away from the world deck through successive banks and wrapping as needed (the printed bank order). Do not return the old favor to the previous holder.')
t=t.replace('3. **Battle plans:** attacker chooses ruled plans once each, then defender.','3. **Battle plans:** red boxes are attacker-only, blue defender-only, gradient either. Attacker chooses eligible ruled plans once each, then defender chooses eligible ruled plans.')
t=t.replace('8. Resolve victorious battle-plan effects, then any end-of-Campaign plan discards.','8. **Finish battle-plan effects:** resolve victorious effects, then any end-of-Campaign plan discards. Defeated effects have already resolved immediately after casualties in step 6; do not skip either timing.')
t=t.replace('Respect site travel restrictions, notably Shrouded Wood.','Respect site travel restrictions. **Shrouded Wood overrides the attacker’s destination choice** if its enemy ruler chooses where the pawn must go.')
old='**Imperial defense:** when an Imperial player defends, Chancellor automatically joins as Ally.'
t=t.replace(old,'**Imperial defense:** apply every relevant change below.\n\n- When an Imperial player defends, Chancellor automatically joins as Ally.')
t=t.replace('Other non-attacking Citizens may join','Other non-attacking Citizens may join',1)
t=t.replace('Activate all Campaign modifiers ruled by defender/Allies;','\n- Activate all Campaign modifiers ruled by defender/Allies;')
t=t.replace('Defender/Allies may use plans','\n- Defender/Allies may use plans')
t=t.replace('On powers, “you,”','\n- On powers, “you,”')
t=t.replace('Declared defender decides contested timing, priority and who uses a shared power. Chancellor controls loss selection as above.','Declared defender decides contested timing, priority and who uses a shared power.\n- Chancellor chooses which Imperial defending warbands die. Surviving warbands from sites return to Chancellor’s board; surviving Citizens’ board warbands stay on those Citizens’ boards.')
t=t.replace('An intra-Empire Campaign does not make all Citizens non-Imperial;','\n- An intra-Empire Campaign does not make all Citizens non-Imperial;')
t=t.replace('An existing Usurper may instead win at round-eight check.','**Exception to waiting for another Wake:** an existing Usurper may win at the end of round 8, before a following Wake, under the ordered endgame checks. An Oathkeeper who has not flipped yet cannot win by this method.')
t=t.replace('and have not discarded a card there this turn, gain printed favor from matching bank, 2 warbands, or take its relic as Recover, as shown. A relic Recover still pays normal relic cost but no Supply.','and have not discarded a card **of that same suit at that site this turn**, gain its printed reward: 1 secret from shared bank, favor from matching suit bank, 2 warbands, or take its relic treating this as Recover. Discarding a different suit there does not suppress it. Taking the relic by this power costs neither Supply nor the ordinary site resource cost.')
t=t.replace('binding exchanges of favor, secrets, relics and banners, including combined future terms and penalties.','binding immediate exchanges of favor and secrets, as well as binding future actions in combination with any player and agreed penalties. This does not grant unrestricted immediate relic/banner transfers.')
t=t.replace('2. **Citizenship:** if winner Exile,','2. **Citizenship:** if winner Exile,')
t=t.replace('Acceptors flip Citizen and replace all garrisons at sites they rule with **one winner-color warband per site**.','Each accepting Exile must do both: **flip their board to Citizen** and **replace every garrison at each site they rule with exactly one winner-color warband at that site**, regardless of the old garrison size.')
needle='**Bandit Crown:**'
t=t.replace(needle,'**Enemies:** for Chancellor/Citizens, enemies are Exiles, not fellow Imperial players. For Exiles and Citizens temporarily non-Imperial during the specified Campaigns, enemies are any other players. Bandits are enemies to everyone and vice versa. During a Campaign “your enemy” means the opposing side: defender and Allies for attacker; attacker for defenders.\n\n'+needle)
needle='**Exile another Citizen:**'
extra='**Uncovered Reliquary modifiers, mandatory for Chancellor:** Brutal makes the defeated player kill their entire force when Chancellor attacks, even if Chancellor loses. Decadent makes Provinces/Hinterland-to-Cradle Travel cost no Supply, but Travel to Hinterland costs +1. Careless gives 1 additional favor on every Trade, even when trading for secrets, but 1 fewer secret when trading for secrets. Greedy draws 2 additional Search cards (still stopping at a world Vision) but prohibits Search costing more than 2 Supply.\n\n'
t=t.replace(needle,extra+needle)
s.write_text(t)
(P/'repair-01.patch').write_text(''.join(difflib.unified_diff((P/'seed-iteration-01/summary-snapshot.md').read_text().splitlines(True),t.splitlines(True),fromfile='seed-iteration-01',tofile='canonical-repair-01')))
x=json.loads((P/'progress.json').read_text());x.update(phase='seed-repair-retest',source_audit={'early_verdict':'MAJOR','findings':6,'repair':'repair-01.patch'});(P/'progress.json').write_text(json.dumps(x,indent=2)+'\n')
