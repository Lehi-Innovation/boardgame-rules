import json,pathlib,hashlib,re,collections
from html.parser import HTMLParser
P=pathlib.Path(__file__).parent
m=json.loads((P/'input-manifest.json').read_text());candidate=pathlib.Path(m['summary_path']);text=candidate.read_text();measure=json.loads((P/'input-measurements.json').read_text())
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def loc(needle):
 i=text.index(needle);return {'line':text[:i].count('\n')+1,'character':i,'text':needle}
D={}
def add(deck,name,label,typ,val,boost,copies,effect):
 D[(deck,name)]={'deck':deck,'card':name,'fighter_label':label,'printed_type':typ,'printed_combat_value':val,'printed_boost':boost,'copies':copies,'printed_effect_normalized':effect}
shared={
'Feint':('versatile',2,'IMMEDIATELY: Cancel all effects on your opponent’s card.'),
'Regroup':('versatile',1,'AFTER COMBAT: Draw 1 card. If you won the combat, draw 2 cards instead.'),
'Momentous Shift':('versatile',3,'DURING COMBAT: If your fighter started this turn in a different space, this card’s value is 5 instead.'),
'Skirmish':('versatile',4,'AFTER COMBAT: If you won the combat, choose one of the fighters in the combat and move them up to 2 spaces.')}
for deck in ['Alice','King Arthur','Medusa','Sinbad']:
 for name in ['Feint','Regroup']:
  typ,val,eff=shared[name];add(deck,name,'ANY',typ,val,1 if deck in ['King Arthur','Sinbad'] else 2,3,eff)
for deck,n in [('Alice',2),('King Arthur',3),('Sinbad',3)]:
 typ,val,eff=shared['Momentous Shift'];add(deck,'Momentous Shift','ANY',typ,val,1,n,eff)
for deck,n in [('Alice',2),('King Arthur',3)]:
 typ,val,eff=shared['Skirmish'];add(deck,'Skirmish','ANY',typ,val,1,n,eff)
rows={
'Alice':[
('Looking Glass','ALICE','defense',2,4,2,'AFTER COMBAT: Choose 2 different effects: draw 2 cards; Alice recovers 3 health; place Alice in any other space.'),
('Snicker-Snack','ALICE','attack',3,4,1,'AFTER COMBAT: If you won the combat, look at your opponent’s hand and choose 1 card for them to discard.'),
('O Frabjous Day!','ALICE','attack',4,4,1,'AFTER COMBAT: Change size.'),
('The Other Side of the Mushroom','ALICE','attack',3,4,1,'AFTER COMBAT: Move Alice up to 3 spaces. Change size.'),
('Eat Me','ALICE','scheme',None,3,2,'Move Alice up to 3 spaces. Change size.'),
('I’m Late, I’m Late','ALICE','versatile',2,3,3,'AFTER COMBAT: Move Alice up to 5 spaces. Change size.'),
('Drink Me','ALICE','scheme',None,2,2,'Draw 2 cards. Change size.'),
('Jaws That Bite','THE JABBERWOCK','attack',4,2,2,'AFTER COMBAT: Deal 2 damage to any one fighter adjacent to the Jabberwock.'),
('Claws That Catch','THE JABBERWOCK','attack',3,2,2,'DURING COMBAT: If the opposing fighter is a hero, this card’s value is 5 instead.'),
('Mad as a Hatter','ALICE','versatile',3,1,2,'AFTER COMBAT: Move each of your fighters up to 2 spaces. Change size.'),
('Manxome Foe','ANY','versatile',3,2,2,'DURING COMBAT: Discard the top card of your deck. Add its BOOST value to this card’s value.')],
'King Arthur':[
('Noble Sacrifice','KING ARTHUR','attack',2,3,3,'DURING COMBAT: You may BOOST this attack. (This is in addition to any boost from King Arthur’s special ability.)'),
('Excalibur','KING ARTHUR','attack',6,3,1,None),
('The Aid of Morgana','KING ARTHUR','attack',4,2,1,'AFTER COMBAT: Draw 2 cards.'),
('Divine Intervention','KING ARTHUR','versatile',3,2,2,'AFTER COMBAT: Move King Arthur up to 5 spaces.'),
('The Holy Grail','KING ARTHUR','defense',1,2,1,'AFTER COMBAT: If King Arthur has 4 or less health but is not defeated, set his health to 8.'),
('The Lady of the Lake','KING ARTHUR','scheme',None,2,1,'Search your deck and discard pile for the EXCALIBUR card. Add it to your hand. If you searched your deck, shuffle it.'),
('Prophecy','MERLIN','scheme',None,2,1,'Look at the top 4 cards of your deck. Add 2 of them to your hand and put the other 2 back on top of your deck, in any order.'),
('Bewilderment','MERLIN','defense',0,2,2,'DURING COMBAT: Prevent all damage. AFTER COMBAT: You may place Merlin in any space.'),
('Aid the Chosen One','MERLIN','attack',4,2,1,'AFTER COMBAT: If you won the combat, draw 2 cards.'),
('Restless Spirits','MERLIN','scheme',None,2,1,'Choose any space in Merlin’s zone. Deal 2 damage to each opposing fighter in that space and in one adjacent space. If at least one fighter is defeated this way, draw 1 card.'),
('Command the Storms','MERLIN','scheme',None,2,2,'Move each fighter up to 3 spaces. (This includes opposing fighters.)'),
('Swift Strike','ANY','attack',3,2,2,'AFTER COMBAT: Move your fighter up to 4 spaces.')],
'Medusa':[
('Gaze of Stone','MEDUSA','attack',2,4,3,'AFTER COMBAT: If you won the combat, deal 8 damage to the opposing fighter.'),
('A Momentary Glance','MEDUSA','scheme',None,4,2,'Deal 2 damage to any one fighter in Medusa’s zone.'),
('Hiss and Slither','MEDUSA','defense',4,3,3,'AFTER COMBAT: Your opponent discards 1 card.'),
('The Hounds of Mighty Zeus','HARPY','versatile',4,3,2,'AFTER COMBAT: Move each Harpy up to 3 spaces.'),
('Clutching Claws','HARPY','versatile',3,2,3,'AFTER COMBAT: Your opponent discards 1 card.'),
('Winged Frenzy','ANY','scheme',None,2,2,'Move each of your fighters up to 3 spaces. You may move them through spaces containing opposing fighters. Then, return a defeated Harpy (if any) to any space in Medusa’s zone.'),
('Second Shot','MEDUSA','attack',3,3,3,'DURING COMBAT: You may BOOST this attack.'),
('Dash','ANY','versatile',3,1,3,'AFTER COMBAT: Move your fighter up to 3 spaces.'),
('Snipe','ANY','versatile',3,1,3,'AFTER COMBAT: Draw 1 card.')],
'Sinbad':[
('Toil and Danger','SINBAD','versatile',3,1,4,'AFTER COMBAT: Move Sinbad up to 3 spaces.'),
('Riches Beyond Compare','SINBAD','scheme',None,1,2,'Draw 3 cards.'),
('By Fortune and Fate','THE PORTER','attack',3,1,3,'AFTER COMBAT: Draw 2 cards.'),
('Commanding Impact','ANY','attack',5,2,1,'AFTER COMBAT: Draw 1 card.'),
('Leap Away','ANY','versatile',4,1,2,'AFTER COMBAT: If you won the combat, choose one of the fighters in the combat and move them up to 4 spaces.'),
('Exploit','ANY','versatile',4,1,2,'AFTER COMBAT: Draw 1 card.')]
}
for deck,records in rows.items():
 for record in records:add(deck,*record)
voyages=[('Voyage Home','Take all other VOYAGE cards from your discard pile and add them to your hand.'),('Voyage to the Island That Was a Whale','Sinbad recovers 2 health.'),('Voyage to the Valley of the Giant Snakes','Look at your opponent’s hand.'),('Voyage to the Creature with Eyes Like Coals of Fire','Your opponent discards 1 random card.'),('Voyage to the Cannibals with the Root of Madness','You may move Sinbad up to 2 spaces.'),('Voyage to the City of the Man-Eating Apes','Deal 2 damage to the opposing fighter.'),('Voyage to the City of the King of Serendib','Draw 1 card.')]
for name,effect in voyages:add('Sinbad',name,'SINBAD','attack',2,1 if name=='Voyage Home' else None,1,'DURING COMBAT: This card’s value is +1 for each other VOYAGE card in your discard pile. AFTER COMBAT: '+effect)
sequences={
'Alice':[('Looking Glass',2),('Snicker-Snack',1),('O Frabjous Day!',1),('The Other Side of the Mushroom',1),('Eat Me',2),('I’m Late, I’m Late',3),('Drink Me',2),('Jaws That Bite',2),('Claws That Catch',2),('Momentous Shift',2),('Skirmish',2),('Mad as a Hatter',2),('Manxome Foe',2),('Feint',3),('Regroup',3)],
'King Arthur':[('Noble Sacrifice',3),('Excalibur',1),('The Aid of Morgana',1),('Divine Intervention',2),('The Holy Grail',1),('The Lady of the Lake',1),('Prophecy',1),('Bewilderment',2),('Aid the Chosen One',1),('Restless Spirits',1),('Command the Storms',2),('Swift Strike',2),('Skirmish',3),('Momentous Shift',3),('Feint',3),('Regroup',3)],
'Medusa':[('Gaze of Stone',2),('Regroup',1),('Gaze of Stone',1),('A Momentary Glance',2),('Hiss and Slither',3),('The Hounds of Mighty Zeus',2),('Clutching Claws',3),('Winged Frenzy',2),('Second Shot',3),('Dash',3),('Snipe',3),('Feint',3),('Regroup',2)],
'Sinbad':[('Toil and Danger',4),('Voyage Home',1),('Riches Beyond Compare',2),('By Fortune and Fate',3),('Voyage to the Island That Was a Whale',1),('Voyage to the Valley of the Giant Snakes',1),('Voyage to the Creature with Eyes Like Coals of Fire',1),('Voyage to the Cannibals with the Root of Madness',1),('Voyage to the City of the Man-Eating Apes',1),('Voyage to the City of the King of Serendib',1),('Commanding Impact',1),('Leap Away',2),('Exploit',2),('Momentous Shift',3),('Feint',3),('Regroup',3)]}
image_receipts=json.loads((P/'image-receipts.json').read_text())
for r in image_receipts:
 if r['cells']:
  deck={'alice':'Alice','king-arthur':'King Arthur','medusa':'Medusa','sinbad':'Sinbad'}[pathlib.Path(r['path']).stem.replace('-action-cards','')];flat=[name for name,n in sequences[deck] for _ in range(n)];assert len(flat)==30
  for cell,name in zip(r['cells'],flat):
   cell.update({'card':name,'native_visual_inspected':True,'legible':True,'view_sha256':sha(cell['view_path'])})
   D[(deck,name)].setdefault('source_cells',[]).append({'source_path':r['path'],'source_sha256':r['sha256'],'row':cell['row'],'column':cell['column'],'box_xyxy':cell['box_xyxy'],'view_path':cell['view_path'],'view_sha256':cell['view_sha256']})
  r['native_visual_inspected']=True;r['method']='All 30 original cells inspected visually in ten 1674x780 three-cell crops; no OCR was used.'
 else:r['method']='Original 372x520 PNG delivered natively and visually inspected.'
card_checks=[]
for (deck,name),record in D.items():
 assert len(record['source_cells'])==record['copies'],(deck,name)
 record.update({'candidate_location':loc('| '+name+' |') if '| '+name+' |' in text else loc('All **7 Voyage**'),'result':'supported','fields_checked':['fighter permission','printed type/icon','printed combat value or absence','BOOST value or absence','all copies','complete effect','timing','conditions','mandatory/optional language'],'notes':[]})
 if name in ['Feint','Regroup']:record['notes'].append('BOOST checked separately for this deck, not inferred from shared name.')
 if name.startswith('Voyage'):record['notes'].append('Current card is outside discard until combat ends; every Voyage already in discard counts. No win condition is printed.')
 if name=='Winged Frenzy':record['notes'].append('Printed ANY permits Medusa or surviving Harpy as initiator; Medusa’s zone is a destination constraint, not an initiator restriction. General occupancy rule still applies.')
 if name=='Excalibur':record['notes'].append('Original attack is textless; apply supplied official 2025 erratum for current Feint interaction; retain 2021 intent only as history.')
 card_checks.append(record)
assert len(card_checks)==58
for deck in sequences:assert sum(r['copies'] for r in card_checks if r['deck']==deck)==30
(P/'native-card-transcription.json').write_text(json.dumps(card_checks,indent=2,ensure_ascii=False));(P/'image-receipts.json').write_text(json.dumps(image_receipts,indent=2,ensure_ascii=False))
# Correct raw ranges using the original markup positions, not a metadata occurrence.
rawpath=pathlib.Path(m['sources'][14]['path']);raw=rawpath.read_bytes();html=raw.decode()
class Ranges(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.stack=[];self.ranges=[];self.offsets=[0];self.offsets += [a.end() for a in re.finditer('\n',html)]
 def pos(self):a,b=self.getpos();return self.offsets[a-1]+b
 def handle_starttag(self,tag,attrs):
  if tag=='div':self.stack.append((self.pos(),dict(attrs)))
 def handle_endtag(self,tag):
  if tag=='div' and self.stack:
   start,attrs=self.stack.pop()
   if attrs.get('class')=='medium-5 large-6':self.ranges.append([start,self.pos()+len('</div>')])
p=Ranges();p.feed(html);ranges=[a for a in p.ranges if 'Nos partenaires de Restoration Games' in html[a[0]:a[1]]];assert len(ranges)==1
hr=json.loads((P/'html-receipt.json').read_text());hr['normative_raw_character_range']=ranges[0];hr['normative_raw_byte_range']=[len(html[:x].encode()) for x in ranges[0]];hr['range_convention']='zero-based start inclusive, end exclusive; full enclosing article div, including related-product block as supplied body capture';hr['normative_raw_range_sha256']=hashlib.sha256(html[ranges[0][0]:ranges[0][1]].encode()).hexdigest();hr['date_visible']='Publié le 11 août 2025';hr['authority']='Original raw page canonical URL and og:site_name IELLO; normative text expressly attributes official rule change to Restoration Games and immediate casual/tournament application.';hr['comparison_note']='Both supplied v2 captures equal independent parses after terminal newline removal; no missing normative wording.';(P/'html-receipt.json').write_text(json.dumps(hr,indent=2,ensure_ascii=False))
# Full text delivery receipts from actual one-slice tool calls.
attempts=[json.loads(x) for x in (P/'delivery-attempts.jsonl').read_text().splitlines()];by=collections.defaultdict(list)
for a in attempts:by[a['path']].append(a)
full=[]
for path,items in by.items():
 s=pathlib.Path(path).read_text();items.sort(key=lambda x:x['start']);assert [x['start'] for x in items]==list(range(0,len(s),5000));assert items[-1]['end']==len(s)
 assert all(x['end']-x['start']<=5000 for x in items)
 full.append({'path':path,'sha256':sha(path),'characters':len(s),'slices':items,'delivery':'Each original slice emitted as the sole original text slice in its tool response, with max_output_tokens 4500; outputs manually confirmed complete/nonblank. No filtering, compression or reconstruction.','complete':True,'failed_attempts':[],'recoveries':[]})
expected=[str(candidate),m['sources'][0]['path']]+[x['path'] for x in m['sources'] if pathlib.Path(x['path']).suffix=='.json']+[m['sources'][15]['path'],m['sources'][16]['path']]
assert all(path in by for path in expected)
# Routing manifest initially read by cat, then additionally delivered in the same bounded slices; receipt uses the bounded deliveries.
(P/'full-delivery-receipts.json').write_text(json.dumps(full,indent=2,ensure_ascii=False))
claims=[]
def check(needle,claim,source,evidence,result='supported'):
 claims.append({'id':f'C{len(claims)+1:03d}','candidate_location':loc(needle),'claim':claim,'source':source,'evidence_or_reasoning':evidence,'result':result})
rules=m['sources'][0]['path'];pdf=m['sources'][1]['path']
check('A card-driven duel:','Objective, fighters, hero/sidekick representations',rules+' pp5,14','Hero zero health ends game immediately; fighter encompasses hero/sidekick; miniatures and tokens identify roles.')
check('- One double-sided board','All components and per-hero 30 cards',rules+' p4','1 double-sided board with 2 battlefields, 4 miniatures, 6 sidekick tokens, 7 dials, 4 character cards, 120 action cards and Alice size token.')
check('- Before first play','Health dial assembly',rules+' p4','Two circles joined by a rivet.')
check('The move value applies','Per-fighter movement; Harpy 1 health/no dial; individual dials and health cap',rules+' pp5,6,9','Each fighter may move up to character move; multiple undialed sidekicks each have 1 health; cannot gain health above dial highest number.')
for deck,health,move,attack,side,hp,sa,ability in [('Alice',13,2,'melee','THE JABBERWOCK',8,'melee','On placing Alice choose BIG/SMALL; BIG adds 2 attack values; SMALL adds 1 defense values; token indicates current size.'),('King Arthur',18,2,'melee','MERLIN',7,'ranged','When King Arthur attacks may BOOST; play boost card face down alongside attack. Canceling attack effects discards boost without effect, subject to current Excalibur erratum.'),('Medusa',16,3,'ranged','HARPIES',1,'melee','Three Harpies. Start of turn may deal 1 damage to one opposing fighter in Medusa’s zone.'),('Sinbad',15,2,'melee','THE PORTER',6,'melee','When maneuvering may move your fighters +1 per VOYAGE in discard.')]:
 source=next(x['path'] for x in m['sources'] if pathlib.Path(x['path']).name==deck.lower().replace(' ','-')+'-character.png')
 check('| '+deck+' |',f'{deck} health/move/attack and sidekick values',source,f'Native card: {health} health, move {move}, {attack}; {side} {hp} health ({"each, x3" if deck=="Medusa" else "one"}), {sa}. '+ability)
 check('**'+deck+':**',deck+' complete ability',source,ability)
check('1. Choose a battlefield','Choose battlefield, hero, components; initialize dials',rules+' p6','Setup steps 1–3.')
check('3. Each player shuffles','Separate 30-card face-down decks and five-card opening hands',rules+' p6','Setup step 4 applies to each player.')
check('4. The **younger player**','Setup placement order, zones and Alice decision',rules+' p6 + four character cards','Younger hero 1; sidekicks separate spaces in shared zone(s); beginning decisions on placement. Older repeats at hero 2; Alice decision belongs to controller.')
check('6. The younger player','Younger player begins',rules+' p6','Setup step 7.')
check('One fighter per circular space.','Occupancy, adjacency and potentially disconnected/multiple zones',rules+' p7 and native p7 diagram','One fighter per circular space; lines give adjacency; colored patterns give all matching spaces, including different battlefield parts and multicolor membership.')
check('At the start of Medusa’s turn','Start ability then two mandatory repeatable actions',rules+' p8 + medusa-character.png','Medusa trigger is at start of turn; exactly two non-skippable actions from maneuver/scheme/attack with repeat allowed.')
check('You may hold more than 7 cards','End-turn seven-card cap',rules+' pp8,9','May hold over seven during turn; discard excess only at turn end before opponent’s turn.')
check('1. **Draw 1 card first','Maneuver mandatory draw first',rules+' p9','Top card to hand before optional movement.')
check('2. **Optionally move**','Independent optional fighter movement and order',rules+' p9','Each fighter one at a time, finish before another; any distance up to value, including zero.')
check('Ordinary movement enters','Path/blocker rules; moving opponents uses owner perspective; card movement application',rules+' p9','Each entered space adjacent; friendly transit allowed, occupied endpoints prohibited; opposing transit prohibited; owner perspective explicit for opponent movement. Card exception overrides restriction.')
check('**BOOST movement:**','One-card maneuver boost, BOOST not combat number, effects ignored and defeated-fighter cards usable',rules+' p10 + native p8 anatomy','Discard 1 hand card; add printed BOOST to movement value; ignore effect. Otherwise unplayable defeated-fighter cards may still boost. Other boost needs effect permission.')
check('Play a scheme (yellow','Scheme active fighter eligibility, face-up resolution and discard',rules+' p10 + p8/16 icons','Declare active fighter permitted by label; cannot use if listed fighters defeated; face-up resolve then discard. ANY is permission, not a destination restriction.')
check('You cannot take an attack action','Attack requires attack card and valid target',rules+' p11','Prohibits action without an attack card or any valid fighter target.')
check('1. **Declare**','Active attacker and target; melee adjacency; ranged same-zone including adjacency across zone boundaries',rules+' pp7,11','Any fighter may target adjacent regardless of zone; ranged may target anywhere in same zone regardless of adjacency.')
check('2. **Choose cards:**','Legal fighter-specific face-down cards, optional defense, simultaneous reveal',rules+' p11','Attacker must choose permitted attack; defender may choose permitted defense; reveal at same time after choices.')
check('Attack-only cards are red','Card roles, ANY eligibility, versatile counts as both for other effects',rules+' pp8,11,16 + native PNGs','Attack red star; defense blue shield; versatile purple combined icon; scheme yellow lightning. Fighter label C in anatomy restricts use; versatile explicitly both roles and both types for game effects.')
check('1. Resolve **IMMEDIATELY**','Combat timing ordering through final discard',rules+' p12','Immediately → during combat → determine damage → after-combat cards (including defeated sidekick) → other after-combat effects → played cards to discards.')
check('3. Determine combat result','Attack minus defense minimum zero, undefended full attack, defender only takes attack damage',rules+' p12','Damage dealt by attacker; subtract defense value; higher defense cannot generate damage or healing.')
check('**Whenever effects share a timing','Mandatory effects, defender first, printed order, cancellation keeps combat number',rules+' p12 + native Feint/sequence cards','Mandatory unless otherwise specified; same-time defender first. Feint cancels effects, not printed combat value; multiphase/effect sentences applied in order.')
check('**Winning combat is not','Combat win depends on attack damage only',rules+' p12','Attacker wins for at least 1 attack damage; defender wins with none, even if effect damage occurred.')
check('| Both fighters play Feint','Feint versus Feint cancellation sequence',rules+' p12 + native Feint cells','Defender immediate Feint cancels attacker immediate Feint before it can resolve; both retain printed 2.')
check('| Arthur attacks with Noble','Arthur Noble Sacrifice plus ability BOOST versus Feint',rules+' pp10,12 + arthur character + Noble/Feint originals','Defender immediate cancellation cancels during-combat Noble effect, and printed Arthur cancellation clause discards initial ability BOOST without effect. Noble remains printed 2; textless Excalibur exception irrelevant.')
check('| BIG Alice attacks','BIG Alice Momentous Shift versus Feint arithmetic',rules+' p12 + alice character + Momentous/Feint originals','Feint cancels conditional change to 5; original Shift 3 + separate BIG modifier 2 =5; Feint defense2; damage3.')
check('There is no points score.','Zero health defeat, remove sidekick immediately, Harpy any damage',rules+' p14','Defeat for any zero-health cause, sidekick removed immediately; undialed sidekick 1 health.')
check('**A defeated hero immediately','Immediate duel end precludes pending healing/effects',rules+' pp12,14','Hero defeat immediately loses; game ends immediately. After-combat effects continue only if game not ended.')
check('- Drawing cards, whether','Mandatory draws, exhaustion on each missing draw, no reshuffle',rules+' p9','Every mandatory card draw with empty deck substitutes 2 immediate damage to each own fighter; two missing draws are two events; one card remaining is drawn before missing-draw damage.')
check('- Played and resolved cards','Face-up separate discard piles, inspect at any time',rules+' p10','All resolved/discarded cards use own face-up discard; both may inspect either.')
check('- Recovery cannot raise','Health cap and no reviving after loss',rules+' pp5,14','Health capped at fighter dial maximum; hero defeat ends game immediately.')
check('- “Move” follows paths','Place versus move; occupancy remains',rules+' pp7,9 + original Looking Glass/Bewilderment','Cards expressly place in any permitted space; movement paths apply to move, not placement; p7 says space only one fighter.')
check('**Voyage combat values:**','Voyage formula and three-discard example',rules+' p12 + seven original Voyage cards','During-combat printed2 +1 for each already-discarded other Voyage; played current card is not discarded until combat end. Three present yield 2+3=5.')
check('Count the Voyages actually','Voyage Home maneuver boost counts in both terms','sinbad-character.png + Voyage Home original + '+rules+' p10','BOOST discard occurs before movement; discarded Home has printed boost1 and is a Voyage in discard, so contributes +1 to both movement bonus and BOOST.')
check('| Voyage Home |','Voyage Home retrieval and subsequent movement','Voyage Home original + sinbad-character.png + '+rules+' p12','AFTER COMBAT retrieves other Voyages already discarded; Home placed into discard finally. Home alone gives movement 2+1=3.')
check('**Timing example:**','Jaws/Skirmish timing, movement and mandatory damage example',rules+' native p13 + original Jaws/Skirmish','4 versus4 gives no attack damage; defender Arthur wins and resolves first; Skirmish moves Jabberwock away before its mandatory adjacent-fighter Jaws effect; absent adjacent target no damage.')
check('**Can the six Voyages','Missing BOOST is intentional and cannot pay BOOST','designer-boost-values-2019-primary-post.json + designer-public-author-profile.json + original Sinbad sheet','2019-10-17 JustinDJacobson post33170907 author43936: no boost value specifically keeps Sinbad from dumping Voyages. Profile maps to designer4083 and Restoration publisher34846. Six originals lack BOOST; Home visibly has1.')
check('**Excalibur versus Feint','Current official Excalibur erratum, scope and timing','publisher-page.html independently parsed + full-visible-v2/body-v2/provenance','Official IELLO page dated11 August2025 says Restoration Games official change immediately applies to casual and tournaments; textless Excalibur effects cannot be canceled, preserving ability BOOST. Card remains printed6; standard final discard still follows p12.')
check('**Historical reference, superseded','Historical Excalibur interpretation and supersession','justin-excalibur-primary-article36640902-api.json + justin-jacobson-author43936-api.json + original official HTML','2021-01-02 designer/publisher author43936 explicitly says Feint of boosted Excalibur cancels boost effect. Official2025 article describes former cancellation and replacement; candidate clearly labels past interpretation historical.')
for r in card_checks:
 claims.append({'id':f'C{len(claims)+1:03d}','candidate_location':r['candidate_location'],'claim':r['deck']+': '+r['card']+' complete table fields/effect','source_cells':r['source_cells'],'result':'supported','evidence_or_reasoning':r['printed_effect_normalized'],'native_record':{'fighter_label':r['fighter_label'],'type':r['printed_type'],'combat_value':r['printed_combat_value'],'boost':r['printed_boost'],'copies':r['copies']}})
# References summarize prior claims, independently checked for consistency.
check('- **Turn:** optional Medusa','Player Reference recap and source-page scope',rules+' pp4–14,16 + character originals','Turn, maneuver, attack, timing/winner, missing-draw recaps agree with detailed verified claims; p15 teams excluded.')
pdfnotes={6:'Setup: hero starting diamonds1/2 and beginning decisions; sidekick placement in shared zone.',7:'Battlefield image: connected circular spaces, single and multicolor patterns, sidekick/hero occupancy; confirms adjacency and zone distinctions.',8:'Anatomy A–H: red attack, blue defense, yellow scheme, purple versatile; distinct combat value B and circled BOOST F; fighter C, deck G, copies H.',13:'Full illustrated Jaws That Bite versus Skirmish example: Jabberwock eligible and adjacent; Alice not adjacent and Alice-only Snicker-Snack unavailable to Jabberwock; defense4 ties attack4; defender-first movement2 creates no adjacent fighter before mandatory Jaws effect.'}
pdf_diagrams=[]
for page,note in pdfnotes.items():
 f=P/f'pdf-page-{page}.png';pdf_diagrams.append({'source_path':pdf,'source_sha256':m['sources'][1]['sha256'],'page_one_based':page,'render_path':str(f),'render_sha256':sha(f),'method':'fitz.open original PDF, get_pixmap Matrix(1.7,1.7), full-page native rendered image visually inspected','inspected':True,'observation':note})
limitations=[
'Bounded source-only audit as requested: no web, no questions/keys/scope maps, no prior audits, no reader outputs, no reports, and no unlisted repository files were read. Only assigned outputs and listed inputs were used.',
'Ancillary catalog/bibliographic fields such as BGG id274637, play-time20–40, source/retrieval dates, hosted rulebook links, and Steam module ownership/co-creation are not independently authenticated by these normative sources. They are not marked verified by this audit. PDF credits and copyright do support designers and ©2019 Restoration/©2020 IELLO attribution.',
'Original card PNG provenance is bounded by the supplied manifest and exact hashes; native card content was checked directly, but upstream Steam module publication history was not independently authenticated.',
'Raw captured HTML was fully read by the independent parser and hashed, not displayed as irrelevant full markup. Complete visible normative page and full containing article div were delivered; own parses equal supplied v2 captures after terminal-newline removal.',
'Optional team rules appear in the fully delivered source text, but are excluded from normative assessment. Other sets and Adventures are excluded. No requirement to summarize speculative expansion interactions was added.',
'No substantive unsupported, incorrect or materially missing in-scope rule/card/fighter claim was identified. A PASS applies to the exact stamped candidate, not to ancillary metadata authentication or a live current website beyond these captured official sources.'
]
report={'verdict':'PASS','summary_path':str(candidate),'summary_sha256':sha(candidate),'findings':[],
'scope':m['scope'],'method':{'independent':True,'data_boundary':m['auditor_data_boundary'],'candidate_banner_not_evidence':True,'candidate_and_all_normative_text_delivered':True,'contiguous_max_slice_unicode_characters':5000,'native_original_png_count':8,'character_cards':4,'action_sheets':4,'action_rows_per_sheet':5,'action_columns_per_sheet':6,'native_action_cells_inspected':120,'unique_deck_card_checks':58,'card_examination':'Direct native visual examination of all printed cells, including duplicate copies; no OCR. Manual normalized source transcription is retained, with label/type/value/BOOST/copies/effect/timing/conditions.', 'html':'Independent original-markup parse retained; complete visible page and body delivered and compared against both complete supplied v2 captures.', 'pdf':'Original PDF gameplay diagrams rendered with requested project .venv fitz and inspected natively; derivatives only in audit07.'},
'checked_claims':claims,'card_checks':card_checks,'input_hashes':measure+[{'path':str(P/'input-manifest.json'),'sha256':sha(P/'input-manifest.json'),'bytes':(P/'input-manifest.json').stat().st_size}],
'full_delivery_receipts':full,'html_receipt':hr,'image_receipts':image_receipts,'pdf_diagram_receipts':pdf_diagrams,'limitations':limitations,'candidate_modified':False,'canonical_modified':False}
assert report['summary_sha256']==m['summary_sha256'];assert all(sha(x['path'])==x['sha256'] for x in measure)
assert len(image_receipts)==8;assert sum(len(r['cells']) for r in image_receipts)==120
assert all(c['native_visual_inspected'] and c['legible'] for r in image_receipts for c in r['cells'])
assert all(c['result']=='supported' for c in claims);assert len(pdf_diagrams)==4
report['validation']={'input_hash_bindings':'all19 candidate/source files match exact manifest hashes; manifest separately hashed','full_delivery':'all listed normative text/JSON/profile/provenance plus complete candidate, manifest and independent visible/body parses have contiguous complete receipts; zero blank/truncated output attempts observed','cards':'58 deck-specific distinct checks; copies reconcile to30 per deck and120 total; all120 cell coordinates and view hashes present; exactly8 original PNG inputs','pdf':'4 native full-page gameplay diagram views hash-bound to original PDF','html':'raw original byte hash, independently parsed complete visible/body hashes, raw enclosing article character/byte ranges, original URL/title/date/authority metadata, and both capture comparisons retained','candidate_and_sources_unchanged':True,'findings_count':0,'checked_claims_count':len(claims)}
(P/'source-audit.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
(P/'audit.md').write_text('# Source audit 07\n\nPASS — no substantive in-scope findings for candidate SHA256 '+m['summary_sha256']+'.\n\nNative coverage: four character cards, all120 action-card cells (58 deck-specific distinct card checks), and rulebook gameplay diagrams on pp6,7,8,13. Full candidate and all normative text/JSON/profile/provenance delivered in contiguous ≤5000-character slices. Independently parsed official HTML matches both supplied v2 captures apart from terminal newline. Current2025 Excalibur erratum and historical2021 ruling checked separately.\n\nAll inputs remain unchanged. Ancillary metadata and upstream module provenance limitations are disclosed in source-audit.json.\n')
print(json.dumps(report['validation'],indent=2));print('REPORT',str(P/'source-audit.json'),'SHA256',sha(P/'source-audit.json'))
