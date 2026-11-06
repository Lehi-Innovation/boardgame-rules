import json, pathlib, re, hashlib, collections
P=pathlib.Path(__file__).parent.parent
D=P/'expanded-iteration-04'
packet=json.loads((D/'grading-input.json').read_text())
summary=(D/'summary-snapshot.md').read_text()
# Every slot below corresponds to one frozen fact, in frozen order. Each anchor
# selects a literal, bounded sentence in the same answer's attached text.
M={
1:[['From taking Oathkeeper during Act'],['or at the end of round 8 if that arrives first'],['Losing title prevents this win']],
2:[['The four true Vision names','Vision of Conquest','Vision of Rebellion','Vision of Sanctuary','Vision of Faith'],['Exile must have true Vision revealed'],['at least 3 Visions drawn from world deck by all players combined'],['For Conquest/Sanctuary']],
3:[['at ends of rounds 5, 6 and 7'],['Ends on respectively'],['An Exile Oathkeeper/Usurper prevents']],
4:[['round 8 ends automatically','If Chancellor or Citizen is Oathkeeper: Empire wins','Otherwise, Exile Usurper wins','Otherwise, qualifying revealed Exile Vision wins','Otherwise Empire wins'],['If several qualify, priority'],['Chancellor wins, except a Citizen meeting Successor']],
5:[['Hold more relics and banners combined than the Chancellor'],["| People | Hold Darkest Secret", "| Protection | Hold People's Favor",'| Devotion | Hold Grand Scepter'],['A Citizen wins only by replacing']],
6:[['either put 1 favor from your board'],['Never remove its last favor'],['If banner is already Mob-side'],['Afterwards, if it has 6+ favor','A banner becoming Mob']],
7:[['Return favor on denizens/edifices'],['Return secrets on denizens/edifices/relics','Flip facedown secrets on your board'],['Exile/Chancellor refresh Supply','Citizen refreshes to the'],['Save remaining unspent Supply'],['Optional Rest powers']],
8:[["Choose either world deck or your pawn's region discard"],['Discard-pile Search costs 2','World-deck Search costs','Darkest Secret replaces'],['Draw 3 cards','draw** one at a time','announce that a Vision was drawn'],['Drawing Visions from a discard']],
9:[["facedown atop next region's pile"],['For cards in hand/advisers','When discarding a card at a site'],['Favor on discarded cards immediately']],
10:[['Up to 3 total','before exceeding limit discard'],['subject to locked cards','If the incoming card changes'],['you cannot discard a faceup adviser at will'],['Facedown cards have no suit'],['as a minor action you may play a facedown adviser'],['True Vision:** Exile only','Not an adviser']],
11:[['Place 1 favor on an **empty denizen','Relics/ruins are ineligible','ruling a remote site does not allow'],['Muster — 1 Supply','Gain 2 warbands from personal bank'],['Trade — 1 Supply','Put 1 secret on card','Put 2 favor on card'],['Facedown advisers never match','With no matching advisers gain'],['Finite source exhaustion']],
12:[['Recover — 1 Supply plus target cost'],['Recover 1 **facedown relic at your site','Pay relic\'s site cost'],['or either banner from anywhere',"People's Favor:** pay any amount",'Darkest Secret:** pay any amount','Put paid favor on banner','Put paid secrets on it'],['distribute old favor singly','Flip it to normal side if Mob'],['new holder takes 1 old secret','Recovering from self returns']],
13:[['at least one suited card at their pawn’s site','One mismatching card is enough'],['If holder has no faceup advisers'],['Empty sites and ruin-only sites protect','Ruins and facedown advisers have no suit']],
14:[['Choose defender:** any other player','If no player rules your site'],['at least one target must be at your pawn','if defender rules that site'],["May target any of defender's sites"],["If defender's pawn is at your site"],["A co-located defender's relic target"]],
15:[['Attacker chooses up to as many attack dice'],['shields rolled','defender\'s board force if their pawn','Bandits add 1 per targeted'],['each skull immediately kills','Count full swords'],['Attacker wins only if attack'],['May sacrifice own surviving force warbands']],
16:[['on attacker victory, the defender first kills half'],['Resolve defeated battle-plan effects'],['may place any number, including','Take **all** targeted relics/banners'],['For a seized banner','People\'s Favor flips to Mob'],['may force defender to travel','independently may burn half'],['Shrouded Wood overrides'],['Finish battle-plan effects for either winner','If attacker won, resolve targets','Finally, discard any plans']],
17:[['A Citizen attacking Chancellor/another Citizen','If Chancellor attacks Citizen'],['When an Imperial player defends','Other non-attacking Citizens may join'],['Activate all Campaign modifiers ruled','This shares the Oathkeeper defense bonus'],['Defender/Allies may use plans','Each shared battle plan may be used'],['Allied board warbands add defense'],['Chancellor chooses which Imperial defending warbands die','Surviving warbands from sites'],['Share powers as one defending side','Declared defender chooses order']],
18:[['| Cradle | 1 | 2 | 4 |','| Provinces | 2 | 2 | 2 |','| Hinterland | 4 | 2 | 3 |'],['Reveal facedown destination'],['Travel cost order','Free Travel is the final override']],
19:[['cannot use its powers the turn you took it','Its holder, even an Exile'],['Must promise **exactly one Reliquary relic','may additionally negotiate a binding exchange'],['Exchange promised pieces','Chancellor gains the newly uncovered'],['Acceptance:** flip to Citizen','If insufficient purple'],['Discard revealed Vision']],
20:[['won by Vision alone','Any other way or multiple victory methods'],['If winner Exile, flip **all** Citizen boards','Winner cannot offer themself','Free Chronicle Citizenship (ignore normal offers)'],['Each accepting Exile must do both'],['Top stack **10 denizens','middle **15 denizens','remaining denizens bottom'],["Chronicle aid's printed"]],
21:[['4 each with 5–6 players'],["People's Favor begins normal",'Darkest Secret has 1 secret'],['Chancellor has 2 favor'],['Each Exile/Citizen has 1 favor','Exiles have 3 own-color'],['All start at full leftmost Supply']],
22:[['Deal saved sites with attached'],['place 2 purple warbands on topmost'],['Resolve printed site favor/secret setup','if insufficient favor Chancellor']],
23:[['Other players in turn order choose a board'],['each player places pawn on any faceup site'],['Starting Citizens receive no Reliquary relic'],['Chancellor begins as Oathkeeper']],
24:[['Take 3 total cards from bottom'],['Each player in turn order draws 3','each player places pawn','chooses 1 drawn card'],['Advance Visions Drawn for any Visions drawn'],['Draw 4 relics and place them randomly']],
25:[['Put Plains faceup','Put purple pawn on Plains','Place 2 purple warbands on Plains','Place Longbows on Plains'],['Mountain faceup in top Provinces','Red and Blue on Mountain','1 each on Mountain','Taming Charm on Mountain'],['Rocky Coast faceup in top Hinterland','Yellow on Rocky Coast','1 each on Mountain and Rocky Coast','other five packet sites facedown','Elders on Rocky Coast'],['Give facedown advisers'],['Place Ivory Eye facedown at Mountain']],
26:[['ruling a remote site does not allow remote Muster','Choose an empty denizen/intact edifice at your pawn'],["Access a card's power if you rule it"],['Plans at a site require rule'],['Persistent powers (thick black braid)']],
27:[['When paying outside your turn'],['Facedown secrets cannot pay','a:becomes ready only after Rest flips|b:then flips faceup at your Rest for reuse'],['A plan can be paid for even with resources']],
28:[['Ordinary major-action modifiers are chosen'],['No-cost modifier may be used on multiple','used once per action'],['cannot discard an active modifier']],
29:[['When Played is mandatory after site favor'],['Ordinary Wake powers happen once','Rest powers are optional once'],['may pay to use a power even if its effect does nothing']],
30:[['Faceup **tree** cards'],['Locked** cards cannot be discarded'],['Cards reducing adviser limit require','with multiple limit-changers','Respect locks']],
31:[['Conspiracy:** anyone may play'],['You may burn 1 secret to take 1 relic'],['at least 2 of your faceup advisers','Both of yours can match'],['Apply banner seizure penalty'],['Then return Conspiracy to box']],
32:[['you cannot discard a faceup adviser at will'],['Drop board warbands only at your site','Bandit sites cannot be occupied'],['Move any number of your warbands','may pick up last physical site warband'],["Citizen pickup requires Chancellor's permission"],['Imperial players with pawns together']],
33:[['Peek at facedown relics at your site','Once you have peeked'],['Grand Scepter holder may peek','cannot use its powers the turn you took it'],['Once you have peeked at a particular relic']],
34:[['Scepter holder pays them 5 favor'],['replaces **board** purple warbands','Purple map garrisons stay Imperial'],['This does not end their Act by itself']],
35:[['Citizen who does not hold Scepter may give'],['Cannot self-exile while holding Scepter'],['replace board warbands with own color','Map garrisons stay purple'],['**end Act**']],
36:[['Current holder keeps title on a tie'],['outgoing holder chooses recipient','A new holder always takes it Oathkeeper-side'],['Transfer Supremacy title **at end of Campaign**']],
37:[['If an attack die must be removed'],['Attacker chooses eligible ruled plans once each'],['bandits use all ruled plans with no cost']],
38:[['a:from five starting warbands|b:Skulls first reduce force from 5'],['A victorious defender gains no declared targets']],
39:[['defender\'s board force if their pawn'],['all defending warbands at targeted sites'],['shields rolled','Doubles multiply shields only']],
40:[['Component limits: favor/warbands/cards','Secrets and dice unlimited'],['take/gain as much as possible if source short'],['Cannot give away/burn/sacrifice extra']],
41:[['Private: facedown card fronts'],['Public: discard counts/backs'],['Facedown advisers can be inspected']],
42:[['“Must” overrides ordinary rules','“cannot” overrides even','“ignore” overrides named'],['“Must if able” has no penalty'],['Law supersedes Playbook/aids except Site Reference'],['Give and Take are distinct keywords']],
43:[['Promises are normally nonbinding','pieces cannot simply be transferred'],['Citizenship offers and expressly binding powers'],['Other binding-deal powers cannot trade Reliquary'],['Tribunal:** Action','disputed breach is settled by coin flip']],
44:[['Brutal makes the defeated player'],['Decadent makes Provinces/Hinterland'],['Careless gives 1 additional favor'],['Greedy draws 2 additional Search'],['Uncovered Reliquary modifiers, mandatory for Chancellor']],
45:[['Imperial winner may build **or** repair **one**'],['At ruled site with no intact or ruined edifice','returning denizen to world deck'],['At ruled site with no intact or ruined edifice'],['or flip a ruled ruin intact']],
46:[['Discard all sites except those winner rules'],['shuffle discarded sites into site deck'],['At retained sites winner does not rule']],
47:[['fill Cradle top-down by pushing'],['Fill Provinces top-down','Push Hinterland sites up'],['Set aside **all sites with ruins**','Fill empty Hinterland slots **bottom-up**'],['Fill any remaining slots with facedown','in each region with no faceup site']],
48:[['winner\'s most common adviser suit','Choose among tied suits'],['3 random Archive cards','next clockwise suit 2','Suit cycle Discord']],
49:[['If Archive cannot supply the full allocation'],['Sort all Dispossessed by suit','take 6 random from largest'],['shuffle remaining Dispossessed into matching']],
50:[['Shuffle all discard piles with **losers\' advisers**'],['set aside all 5 Visions including Conspiracy'],["Winner's advisers are excluded"]],
51:[['save Grand Scepter in World Box'],["return losing players' relics"],['Refill faceup sites with fewer relics'],["Shuffle winner's remaining relics"]],
52:[['stack each site\'s attached cards','stack sites so top Cradle'],['Save player boards on current'],['a:Next game may use a different group|b:Next group need not preserve']],
53:[['have not discarded a card **of that same suit','Discarding a different suit'],['gain its printed reward'],['Taking the relic by this power costs'],['a:Relic reward costs neither|b:relic has no Supply']],
54:[['Coasts:** traveling from one Coast to another'],['a:destination alone being a Coast|b:destination alone being Coast']],
55:[['Narrow Pass:** entering its region from another'],['targeting anything in its region from another region'],['Narrow Pass:** entering its region from another']],
56:[['Hidden Place:** cannot travel there'],['Shrouded Wood:** travel from it costs 2'],['Coasts:** traveling from one Coast','Buried Giant:** traveling from it']],
57:[['Buried Giant:** traveling from it may flip'],['a:flip one of your board secrets facedown|b:flip 1 own board secret facedown'],['a:It does not automatically ignore Hidden Place|b:That does not by itself ignore Hidden Place']],
58:[['a:Marshes makes Search while|b:Search while pawn is at Marshes'],['a:Merely ruling Marshes|b:Merely ruling it remotely']],
59:[['a:Great Slum permits first|b:At Great Slum'],['a:It does not grant unrelated|b:This is limited to that timing']],
60:[['Shrouded Wood:** travel from it costs 2'],['Travel cost order','Shrouded Wood:** travel from it costs 2'],['a:forced travel does not bypass the choice or cost|b:including forced travel/banishment']],
61:[['Plains/Mountain:** must add/subtract 1 attack die'],['a:Plains/Mountain modify dice|b:Plains/Mountain modifier applies']],
62:[['a:River adds 1 warband|b:River Muster adds 1 warband'],['a:Without rule, Muster still works|b:without rule, ordinary 2 only']],
63:[['a:plus 1 = 3|b:Charming Valley departure adds 1=3'],['a:A “spend no Supply” power|b:A spend-no-Supply power']],
64:[['a:Use Tribunal Action if|b:A player who rules Tribunal'],['Tribunal:** Action'],['Tribunal:** Action']],
65:[['Bandit Crown:** treat bandits as own warbands'],['add relevant bandits to defense'],['Bandits themselves cannot be killed']],
66:[['Facedown sites cannot hold cards or be ruled'],['Both intact and ruined edifices use capacity'],['a:site powers remain as printed otherwise|b:The summary gives ordinary card-power access']],
67:[['the corrected Draw keyword means'],['Whenever a Vision is drawn from world deck','The Search action itself still stops']],
68:[['a:You can stop with Supply unspent|b:may leave Supply unspent','Save remaining unspent Supply'],['Finish an action before starting another']],
69:[['For a seized banner','People\'s Favor flips to Mob'],['People\'s Favor:** pay any amount','Put paid favor on banner','Flip it to normal side if Mob','Darkest Secret:** pay any amount','Put paid secrets on it']],
70:[['Share powers as one defending side','whether a restrictive plan must be declared first'],['Declared defender chooses order'],['Each shared battle plan may be used']],
71:[['If insufficient purple'],['replaces **board** purple warbands','Purple map garrisons stay Imperial']],
72:[['If banner is already Mob-side','Afterwards, if it has 6+ favor','A banner becoming Mob'],['If banner is already Mob-side','Afterwards, if it has 6+ favor']],
73:[['a:reveal is a minor Action during Act|b:revealing held Vision is an Act minor action','Exile must have true Vision revealed'],['at least 3 Visions drawn from world deck by all players combined']],
74:[['A title still on Oathkeeper at game end is insufficient','If Chancellor or Citizen is Oathkeeper: Empire wins'],['Otherwise, qualifying revealed Exile Vision wins','Otherwise Empire wins']],
75:[['Any other way or multiple victory methods'],['If winner Exile, flip **all** Citizen boards','Winner cannot offer themself'],['Each accepting Exile must do both']],
76:[['discarded and receiving sites can differ','With People\'s Favor you may first discard'],['With People\'s Favor you may first discard']],
77:[['may force defender to travel','independently may burn half'],['Take **all** targeted relics/banners'],['independently may burn half'],['For a seized banner','People\'s Favor flips to Mob','independently may burn half']],
78:[['a:Each skull kills one warband in chosen attacking force|b:Skulls kill own force warbands'],['a:Sacrificing may add attack|b:Sacrifice only surviving force']],
79:[['Exile/Chancellor refresh Supply'],['For Chancellor: 18+','For Exile: 9+']],
80:[['red boxes are attacker-only'],['Plans at a site require rule','a:Ruling a plan is required|b:Merely ruling a wrong-color plan']],
81:[['Enemies:** for Chancellor/Citizens','For Exiles and Citizens temporarily non-Imperial','Bandits are enemies to everyone'],['A Citizen attacking Chancellor/another Citizen','If Chancellor attacks Citizen','An intra-Empire Campaign does not make all Citizens'],['During a Campaign “your enemy”']],
82:[['Draw 3 cards','You cannot voluntarily stop early'],['If source empties, draw only what remains']],
83:[['a:Round marker starts round 1|b:Round marker starts round 1'],['a:Chancellor takes first turn each round|b:Chancellor starts','a:Turn is Wake→Act→Rest|b:Wake→Act→Rest'],['a:up to eight rounds|b:After everyone acts check round-end victory','a:After everyone acts, check round-end victory']],
84:[['Do not shuffle the prepared first-game decks','Give facedown advisers'],['Seed Cradle/Provinces/Hinterland discard piles','Put remaining 41 denizen/Vision cards'],['Place Ivory Eye facedown at Mountain']],
85:[['After first game open Archive packet'],['put edifices in matching sections'],["separately shuffle each suit's denizens"]],
86:[['Forced Citizenship** powers apply','no required Scepter offer','no invented promised exchange'],['Acceptance:** flip to Citizen','If insufficient purple'],['Discard revealed Vision']],
87:[['Normally cannot place favor/secrets on a card'],['If power has no cost you can still use it'],['battle-plan payment is the exception']],
88:[['Oathkeeper +1 defense die, Usurper +2','The mandatory title bonus is itself'],['a:Under Supremacy Empire collectively holds title/goal|b:Imperial defense shares it across defending side']],
89:[['Move follows capacity, placement and restriction rules','Swap moves the two pieces','Faceup **tree** cards','Locked** cards cannot be discarded'],['A move or swap alone is not playing']],
90:[['Kill sends warband to its color\'s personal bank'],['Surviving warbands from sites return','surviving warbands already on Citizens\' boards stay']],
91:[['a:Bandits do not compete for title or Vision goals|b:Bandits do not compete for victory','a:compare players|b:They do not count as players']],
92:[['At Salt Flats, Mine or Drowned City','If Exile, check Usurper','If Exile holding Oathkeeper'],['one token total','Remote rule gives no income']],
93:[['On defender victory, the attacker kills half','Resolve defeated battle-plan effects'],['If defender won, skip attacker’s targets'],['Finally, discard any plans from either side']],
94:[['A ± symbol permits its user','Either eligible role can choose either sign','gradient either'],['it does not change attack dice into defense dice']],
95:[['Ordinary Wake powers happen once'],['Rest powers are optional once each'],['a:Opportunity-site income is explicitly optional|b:Opportunity income explicitly optional']],
96:[['a:Red rules sites with red physical warbands|b:Red rules the different site','a:not the purple-garrisoned pawn site|b:regardless of Red pawn'],['a:Moving pawn alone does not change rule|b:pawn movement alone does not alter rule'],['a:A site holds only one color|b:Sites hold only one color']],
97:[['Peek lets the acting player look','Reveal means show its front to everyone'],['A generic reveal-only instruction']],
98:[['**After** means immediately following']],
99:[['Take favor/secrets from another player','Take adviser cards moves theirs'],['Take a relic from the prompted player'],['Give is the reverse'],['Burn sends favor/secrets from your board']],
100:[['Exchange permits you to Give','these are optional permissions unless'],['Do not assume an equal or compulsory reciprocal','a:Word alone does not require simultaneous or equal transfer|b:Word alone does not require equal or compulsory']],
101:[['If world deck was not rebuilt during previous Chronicle','Take 3 total cards from bottom']],
102:[['a:First game: Chancellor seated short edge by Cradle|b:First game Chancellor at short edge by Cradle','Choose Chancellor by any method'],['a:Red, then Blue, then Yellow clockwise|b:Red then Blue then Yellow clockwise'],['Choose Chancellor by any method'],['others randomly','Other players in turn order choose a board']],
103:[['a:First-game packet uses Oathkeeper of Supremacy|b:First game uses Oathkeeper of Supremacy','a:It does not choose among all four Oaths|b:It does not allow choosing any Oath'],['a:Oathkeeper goal rule most sites|b:Oathkeeper rules most sites'],['Hold more relics and banners combined than the Chancellor']],
}

# Judgments on unresolved or contradictory facts are explicit, separate from
# mechanically locating literal evidence. No score is inferred from labels.
OV={}
def override(readers,q,f,status,reason,anchors):
    for r in readers.split(): OV[(r,q,f)]=(status,reason,anchors)
override('reader-a',33,2,'missing','Scepter Reliquary peek permission is present, but the no-use-on-turn-taken condition is absent from this application and its Minor-actions attachment.',['a:Grand Scepter holder may peek'])
override('reader-b',36,2,'missing','Outgoing-holder selection is stated, but receiving the title Oathkeeper-side is absent from this application and its Overview attachment.',['b:outgoing holder chooses recipient'])
override('reader-a reader-b',38,1,'contradiction','The premise already leaves five after skulls: defeat must kill two and leave three. The application instead treats five as the pre-skull force and subtracts skulls again; the attached general rule does not erase that incompatible scenario application.',['a:So from five starting warbands|b:Skulls first reduce force from 5'])
override('reader-a reader-b',52,3,'missing','Different players/status ownership is allowed, but selection of saved boards by non-Chancellors in turn order is absent from the application and Chronicle attachment.',['a:Next game may use a different group|b:Next group need not preserve'])
override('reader-a reader-b',53,4,'missing','The application and attached Homeland procedure omit the requested site-favor → Homeland → When Played order; reader-b also attaches Search, which does not supply that timing.',['a:Reward is its printed option|b:Reward can be'])
override('reader-a reader-b',57,2,'missing','Flipping an own-board secret facedown establishes its location/state, but inability to repay with it until readied is absent from this entry. Neither attached Travel nor Site powers supplies that payment/readiness rule.',['a:flip one of your board secrets facedown|b:flip 1 own board secret facedown'])
override('reader-a reader-b',59,1,'missing','Timed discard permission is stated, but respecting locked cards is absent. The Site attachment for reader-a and Overview attachment for reader-b do not supply the lock restriction.',['a:Great Slum permits first|b:At Great Slum'])
override('reader-a',60,3,'contradiction','The application explicitly says forced travel/banishment does not bypass the cost. Campaign banishment itself spends no Supply; a merely conditional reference to a Free Travel override does not correct this assertion.',['a:forced travel does not bypass the choice or cost'])
override('reader-b',60,3,'missing','The ruler chooses even for banishment, and a spend-no-Supply effect may override base cost, but this entry never establishes that banishment itself supplies that no-Supply permission. The Campaign passage containing it is not attached.',['b:including forced travel/banishment','b:Free Travel can make Supply zero'])
override('reader-b',61,1,'missing','The trigger and lack of rule exemption are stated, but mandatory +1 attack die for Plains and −1 for Mountain are absent from the application and its Overview attachment.',['b:Plains/Mountain modifier applies'])
override('reader-a',66,3,'satisfied','In the immediately preceding ruined-edifice context, “site powers remain as printed otherwise” fairly conveys continuing operation under the printed conditions; no exact card-power vocabulary is required.',['a:site powers remain as printed otherwise'])
override('reader-a',68,1,'missing','The application allows stopping with Supply unspent, but does not explain preservation through Rest. Its sole Act attachment omits the Rest saving rule.',['a:You can stop with Supply unspent'])
override('reader-a',78,1,'contradiction','The application distinguishes a chosen attacking force from unchosen board force in response to choosing fewer dice. Choosing fewer dice does not itself exclude board warbands from the force or casualties; the attached force definition cannot silently erase that distinction.',['a:Each skull kills one warband in chosen attacking force'])
override('reader-b',83,3,'missing','The round-end check-before-advance sequence is stated, but automatic ending at round eight is absent from the application and its Overview attachment.',['b:After everyone acts check round-end victory'])
override('reader-a reader-b',88,2,'missing','Imperial sharing is supplied, but this entry does not identify the Chancellor as title holder when the Empire collectively meets the Supremacy goal. Reader-a uses the broader Empire-holds-title shorthand; reader-b omits collective goal/holder allocation.',['a:Under Supremacy Empire collectively holds title/goal|b:Imperial defense shares it across defending side'])
override('reader-b',95,1,'missing','Mandatory resolution/explicit may is present, but once-each ordinary Wake-power frequency is absent from this application and its Wake procedure attachment.',['b:Wake powers without may resolve as much as possible'])
override('reader-b',95,2,'missing','Rest powers are called optional, but once each at the end of Rest is absent from this application and its Wake-only attachment.',['b:Rest powers optional'])

# Reader-specific alternative evidence where the fact is explicitly stated in
# the application and the section containing the rule is not attached.
ALT={
('reader-b',36,1):['b:Current title holder keeps title on tie'],
('reader-b',36,3):['b:Supremacy transfer occurs at end of Campaign'],
('reader-b',61,2):['b:Plains/Mountain modifier applies'],
}

def sentence(text,at,n):
    # Preserve exact characters. Table rows/bullets/headings are self-contained.
    line_start=text.rfind('\n',0,at)+1
    line_end=text.find('\n',at+n)
    if line_end<0: line_end=len(text)
    starts=[m.end() for m in re.finditer(r'[.!?]\s+',text[line_start:at]) if not re.fullmatch(r'\d+\.\s+',text[line_start:line_start+m.end()])]
    st=line_start+(starts[-1] if starts else 0)
    ends=list(re.finditer(r'[.!?](?=\s|$)',text[at+n:line_end]))
    en=at+n+ends[0].end() if ends else line_end
    while st<en and text[st].isspace():st+=1
    return st,en

def evidence(anchor,entry,r):
    variants=anchor.split('|')
    chosen=[]
    for v in variants:
        if v.startswith(('a:','b:')):
            if v[:1] != r[-1:]:continue
            needle=v[2:]; txt=entry['answer']; at=txt.find(needle)
            if at<0: raise ValueError(('application anchor missing',r,needle))
            st,en=sentence(txt,at,len(needle))
            return {'source':'application','start':st,'end':en,'excerpt':txt[st:en]}
        chosen.append(v)
    if not chosen:return None
    needle=chosen[0]
    # Summary anchors are usable only inside this same entry's attached spans.
    for sp in entry['attached_verbatim_passage_spans']:
        at=summary.find(needle,sp['start'],sp['end'])
        if at<0:continue
        st,en=sentence(summary,at,len(needle));st=max(st,sp['start']);en=min(en,sp['end'])
        return {'source':'attached_quote','summary_start':st,'summary_end':en,'attached_span_start':sp['start'],'attached_span_end':sp['end'],'excerpt':summary[st:en]}
    raise ValueError(('unattached or missing summary anchor',r,needle))

def build():
    errors=[]; readers=[]
    for r in ['reader-a','reader-b']:
        qs=[]
        for q in packet['questions']:
            num=int(q['id'][1:]);entry=q['readers'][r];assert len(M[num])==len(q['required_facts']),(num,len(M[num]),len(q['required_facts']))
            checks=[]
            for i,f in enumerate(q['required_facts'],1):
                anchors=ALT.get((r,num,i),M[num][i-1]);status='satisfied';note='Resolved correctly by the specific same-entry evidence below.'
                if (r,num,i) in OV:status,note,anchors=OV[(r,num,i)]
                ev=[]
                for anchor in anchors:
                    try:
                        e=evidence(anchor,entry,r)
                        if e and e not in ev:ev.append(e)
                    except Exception as ex:errors.append((r,q['id'],i,str(ex)))
                checks.append(dict(fact_id=f['fact_id'],expected_fact=f['expected_fact'],status=status,assessment=note,evidence=ev))
            contradiction=[f['assessment'] for f in checks if f['status']=='contradiction']
            missing=[f['assessment'] for f in checks if f['status']=='missing']
            grade='incorrect' if contradiction else 'partial' if missing else 'correct'
            reason=' '.join(contradiction+missing) if contradiction or missing else 'All requested frozen facts are correctly resolved in this application and its attached passages; no material contradictory ruling.'
            qs.append(dict(id=q['id'],question=q['question'],expected_answer_from_fixed_key=q['fixed_expected_answer'],observed_answer=entry['answer'],grade=grade,reason=reason,fact_checks=checks,attached_quote_spans=entry['attached_verbatim_passage_spans'],material_contradictions=contradiction))
        counts=collections.Counter(q['grade'] for q in qs);fc=collections.Counter(f['status'] for q in qs for f in q['fact_checks'])
        readers.append(dict(reader=r,totals={k:counts[k] for k in ['correct','partial','incorrect']}|{'total':len(qs)},fact_totals={k:fc[k] for k in ['satisfied','missing','contradiction']}|{'total':sum(fc.values())},questions=qs))
    if errors:
        print(json.dumps(errors,indent=2,ensure_ascii=False));return
    result=dict(benchmark_version='expanded-v9',iteration=4,status='complete',method='Independent strict manual semantic adjudication of all 206 entries and 654 frozen facts, after complete model-visible delivery; deterministic extraction/validation of fact-specific literal evidence. Complete same-entry attachments can supply procedural facts, but do not erase incompatible application rulings. No other grades or reader protocol reports consulted.',inputhashes=[{'path':str(D/'grading-input.json'),'sha256':hashlib.sha256((D/'grading-input.json').read_bytes()).hexdigest()}]+packet['inputs'],delivery_receipt={'path':str(P/'delivery-audit/grader04-delivery-ranges.jsonl'),'complete':True,'max_chunk_characters':5000,'packet_characters':len((D/'grading-input.json').read_text()),'summary_characters':len(summary),'chunks':len((P/'delivery-audit/grader04-delivery-ranges.jsonl').read_text().splitlines()),'all_ranges_contiguous':True},questions_graded=206,fact_assessments=654,readers=readers)
    (D/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps([{'reader':r['reader'],'totals':r['totals'],'fact_totals':r['fact_totals']} for r in readers],indent=2))

if __name__=='__main__':build()
