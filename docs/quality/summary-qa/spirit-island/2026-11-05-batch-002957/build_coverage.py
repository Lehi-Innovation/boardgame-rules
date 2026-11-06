from pathlib import Path
import json,hashlib
B=Path(__file__).parent
q=json.loads((B/'expanded-v4/questions.json').read_text()); k=json.loads((B/'expanded-v4/answer-key.json').read_text())['answers']
faq=json.loads((B/'faq-applicability-review.json').read_text())['applicable_rulings']
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
book=Path('extracted/spirit-island-rules.txt');lines=book.read_text().splitlines(True)
rows=[]
def passage(name,start,end,ids,scope='included',reason=None):
 text=''.join(lines[start-1:end]);rows.append({'passage':name,'source_file':str(book.resolve()),'extraction_lines':[start,end],'character_range':[sum(map(len,lines[:start-1])),sum(map(len,lines[:end]))],'source_passage_sha256':hashlib.sha256(text.encode()).hexdigest(),'question_ids':ids.split() if ids else [],'scope':scope,'reason':reason})
passage('Overview shared victory/defeat',94,107,'Q20')
passage('Introductory setup/Power Progressions',112,125,'Q01 Q55')
passage('Invader board and component figure',127,233,'Q01 Q20 Q22 Q33',reason='Figure procedures mapped; exact box quantities are reference inventory rather than standalone questions.')
passage('Fear board setup',238,244,'Q01')
passage('Blight setup',245,257,'Q01 Q14 Q55')
passage('Island and supply setup',258,267,'Q01 Q21 Q22 Q17')
passage('Player setup',268,278,'Q22 Q23')
passage('Initial Explore',279,282,'Q01 Q09 Q10')
passage('Invader deck setup',284,297,'Q01')
passage('Setup layout diagrams pp6-7',298,377,'Q21 Q22',reason='PDF images pages6-7 inspected; layout itself is setup choice, not numerical trivia.')
passage('Phase order / simultaneous play',379,387,'Q04 Q05 Q24 Q103')
passage('Optional timeboxing',388,398,'','excluded','Optional playstyle/timekeeping recommendation; no change to core action resolution or outcome rule.')
passage('Decision authority',399,412,'Q54')
passage('Ordered Power example',413,429,'Q05 Q16 Q19')
passage('Spirit phase Growth',430,435,'Q02 Q03 Q24 Q36')
passage('Spirit phase Energy',436,438,'Q04 Q102')
passage('Spirit phase Play/pay',439,451,'Q04 Q17 Q37 Q38')
passage('Fast Power phase',452,460,'Q05 Q16 Q29')
passage('Invader phase sequence/Blighted effect',465,481,'Q103')
passage('Fear resolution',482,486,'Q11 Q12 Q51 Q99')
passage('Invader eligibility and Ravage',487,522,'Q06 Q07 Q31 Q46 Q98 Q101')
passage('Fear through Fear / each player / land order',523,541,'Q12 Q26 Q51 Q54 Q99')
passage('Blight cascade and Presence sidebar',542,553,'Q13 Q14 Q43 Q44')
passage('Build',556,568,'Q08')
passage('Explore',569,588,'Q09 Q28 Q48 Q49')
passage('Advance cards',589,592,'Q10 Q50')
passage('Slow phase',593,595,'Q05 Q50')
passage('Time Passes',596,605,'Q30')
passage('Reminder, Stage II and III',607,626,'Q09 Q10 Q47')
passage('Worked Ravage/Build/Explore examples',630,738,'Q06 Q08 Q09 Q13')
passage('Victory/Terror/sacrifice and defeat',741,762,'Q20 Q45 Q103',reason='Original immediate language superseded by FAQ action-tree timing.')
passage('Fear generation',763,825,'Q11 Q12 Q18 Q20')
passage('Boards/lands',835,848,'Q21 Q47')
passage('Presence and Sacred Sites',849,857,'Q03 Q13 Q23 Q43 Q69')
passage('Energy and Card Plays',858,868,'Q04 Q102')
passage('Spirit panel/special rules/Growth',889,915,'Q02 Q22 Q24 Q71')
passage('Presence tracks and Reclaim One',916,944,'Q02 Q25 Q26')
passage('Innates',945,955,'Q15 Q27 Q29')
passage('Common Growth/repositioning/threshold sidebars',957,982,'Q02 Q03 Q15 Q25 Q36')
passage('Invaders and supply/Health',997,1022,'Q09 Q18 Q31 Q32 Q33 Q52')
passage('Blight',1023,1039,'Q13 Q14 Q43 Q44 Q45 Q94')
passage('Damage tracking',1040,1075,'Q18 Q30 Q31')
passage('Dahan',1078,1094,'Q06 Q07 Q18 Q33')
passage('Power anatomy cost/Elements/speed',1095,1114,'Q04 Q05 Q26 Q90')
passage('Power anatomy Range/Target',1115,1126,'Q05 Q21 Q28 Q34 Q42')
passage('Power anatomy effects',1127,1141,'Q16 Q29 Q30 Q34')
passage('Thresholds / Instead',1167,1199,'Q15 Q27 Q29 Q70')
passage('Do as much as possible',1200,1202,'Q16 Q29')
passage('Forego Power / fewer Elements',1203,1209,'Q15 Q16 Q29 Q70')
passage('One target/turn/use',1210,1220,'Q05 Q15 Q30 Q34')
passage('Temporary effects and targeting examples',1221,1235,'Q16 Q29 Q30')
passage('Gaining Power Cards',1237,1249,'Q17 Q37 Q39 Q55')
passage('Damage/destroy/remove/replace',1250,1260,'Q18 Q32 Q52 Q91')
passage('Defend',1261,1267,'Q07 Q31 Q58 Q101')
passage('Removing Blight',1268,1271,'Q14 Q44')
passage('Forgetting / Damage / destruction sidebars',1273,1304,'Q17 Q18 Q39 Q97')
passage('Gather/Push',1308,1320,'Q19 Q35 Q36')
passage('Repeat',1321,1335,'Q40 Q41 Q42 Q78 Q95')
passage('Gather/Push example',1336,1355,'Q19 Q35 Q50')
passage('Gameplay tips and optional reminder techniques',1358,1448,'Q05 Q09 Q13 Q19 Q30 Q50','reference','Rule reminders duplicate tested rules; strategy and convenience practices excluded as non-normative.')
passage('Optional easier-game variants',1449,1464,'','excluded','Optional difficulty modules outside assigned standard scope.')
passage('Solo',1466,1473,'Q54')
passage('Adversaries',1474,1514,'','excluded','Explicitly excluded optional module.')
passage('Scenarios/thematic/scoring',1516,1571,'','excluded','Explicitly excluded optional modules and optional performance scoring.')
passage('Lore/credits/design/difficulty charts',1573,1840,'','excluded','Nonprocedural lore/credits or excluded difficulty modules.')
passage('Glossary Action through Ocean',1841,1994,'Q01 Q02 Q03 Q04 Q06 Q08 Q09 Q13 Q14 Q15 Q17 Q18 Q19 Q20 Q21 Q22 Q23 Q25 Q28 Q30 Q32 Q33 Q34 Q35 Q39 Q40 Q45 Q52 Q102 Q103',reason='Definitions restate procedures mapped above; excluded module definitions remain out of scope.')
passage('Glossary Outnumber through Your Land',1996,2068,'Q03 Q05 Q07 Q15 Q17 Q19 Q21 Q23 Q25 Q30 Q40 Q42 Q53',reason='Includes normative Outnumber (Q53), Up To (Q19), Reclaim One (Q25), Repeat (Q40).')
passage('Iconography and target/range reference',2070,2141,'Q18 Q19 Q21 Q23 Q28 Q34 Q54',reason='PDF pages17/32 inspected to recover lost icons/slashes.')
passage('Track icons and full turn order reference',2142,2171,'Q02 Q25 Q26 Q30 Q103')
overrides={'setup-last-explore':['Q01'],'setup-solo':['Q54'],'setup-13':[],'energy-carry':['Q04'],'innate-once':['Q15'],'repeat-new-power':['Q40'],'damage-choice':['Q18'],'fear-destruction-additive':['Q18'],'fear-current-level':['Q11','Q12'],'blight-amount':['Q06','Q13'],'explore-occupied':['Q09'],'invader-two-terrain':['Q10','Q47'],'invader-skip':['Q07'],'ravage-simultaneous':['Q06','Q101'],'defend-both':['Q31'],'flag-ignored':['Q10'],'solo-another':['Q54'],'unlimited-components':['Q33']}
fmap=[]
for x in faq:
 anchors=[s['entry_anchor'] for s in x['sources']];ids=[z['id'] for z in k if any(a in ' '.join(z['source_refs']) for a in anchors)]
 ids=ids or overrides.get(x['id'],[])
 fmap.append({'ruling_id':x['id'],'rule':x['applicable_rule'],'source_refs':x['sources'],'question_ids':ids,'scope':'included' if ids else 'excluded','reason':None if ids else '13 disks is component inventory/printing-spare clarification; not a distinct procedural benchmark question.'})
missing=[x['ruling_id'] for x in fmap if not x['question_ids'] and x['ruling_id']!='setup-13'];assert not missing,missing
accept=[]
for bank in ['expanded-v1','expanded-v2','expanded-v3','expanded-v4']:
 for e in json.loads((B/bank/'novelty.json').read_text()):accept.append({**e,'bank':bank,'decision':'accepted'})
for x in accept:
 if x['id'] in ['Q32','Q100']:
  x['decision']='retained regression; novelty rejected on re-review'
  x['reason']='Earlier frozen entry retained unchanged rather than shrinking benchmark. Q32 concretizes the survival/Health rule already in Q18; Q100 human cleanup is covered by Q77. Not counted toward meaningful additions.'
rejects=[
 {'pass':5,'candidate':'Another Town/City Build count','decision':'rejected','because':'Same more-Towns-versus-otherwise branch as Q08; changed numbers add no rule.'},
 {'pass':5,'candidate':'More high-Damage Ravages','decision':'rejected','because':'One Blight regardless of excess and efficient Dahan allocation already Q06/Q13/Q31.'},
 {'pass':5,'candidate':'Different cascade path or player count','decision':'rejected','because':'Same one-adjacent cascade/pool formulas Q13/Q14/Q43/Q44/Q94.'},
 {'pass':5,'candidate':'Repeat another unmodified Power','decision':'rejected','because':'No timing or exception beyond Q40–42/Q95.'},
 {'pass':5,'candidate':'Twice as many Elements','decision':'rejected','because':'Innate once and Elements checked-not-spent already Q15/Q70.'},
 {'pass':5,'candidate':'More Fear overflow counts','decision':'rejected','because':'Same reset/carryover branch Q11.'},
 {'pass':5,'candidate':'Health-removal modified Health values','decision':'rejected','because':'Current Health versus Damage Q52, pooled limits Q92; changed values add none.'},
 {'pass':5,'candidate':'Six-player setup, extra board, thematic maps','decision':'excluded','because':'Outside original standard 1–4 balanced-board scope.'},
 {'pass':5,'candidate':'Negative individual Invader Damage and land-wide bonuses','decision':'excluded','because':'Supplied examples require expansion mechanisms; no in-scope source instance requiring another question.'},
 {'pass':6,'candidate':'Different Fear card gained in Slow versus Ravage','decision':'rejected','because':'Both wait until next Fear step; Q11/Q12/Q50 distinguish current Fear-step generation.'},
 {'pass':6,'candidate':'Another modified Range origin/terrain','decision':'rejected','because':'Source and target constraints persist Q28/Q71; changed terrain adds none.'},
 {'pass':6,'candidate':'Another Bringer hypothetical Damage split','decision':'rejected','because':'Single use versus separate/Repeat and real prior Damage fully Q78–83.'},
 {'pass':6,'candidate':'Ocean Drowning at different player count','decision':'rejected','because':'Printed-Health exchange rule and make-change branch Q75.'},
 {'pass':6,'candidate':'Different order of Stage III terrains','decision':'rejected','because':'Interleaved land order/list eligibility and outcomes Q45/Q46/Q47.'},
 {'pass':6,'candidate':'Counting exact colored markers or all eight Element names','decision':'excluded','because':'Component/reference trivia, not a distinct procedural ruling.'},
 {'pass':6,'candidate':'Timeboxing the Spirit Phase or forgiving earlier mistakes','decision':'excluded','because':'Optional playstyle/learning advice, no core action outcome rule.'},
 {'pass':6,'candidate':'Events, Aspects, Russia, England, Sweden, Scenarios','decision':'excluded','because':'Outside scope, even when FAQ examples are tagged Core.'},
 {'pass':6,'candidate':'Optional victory/defeat points formulas','decision':'excluded','because':'Optional performance scoring explicitly excluded; standard shared outcomes tested.'}]
ledger={'benchmark':'expanded-v4','question_count':103,'novelty_policy':'New source-supported rule, defined outcome branch, or timing/exception interaction; no cosmetic/numerical variants. Preserve all earlier frozen entries.','source_hierarchy':'Current assigned 32-page CORE; applicable original-core Living FAQ corrections supersede conflicting original wording. FAQ pages are broad; excluded modules do not enter scope.','book_passages':rows,'faq_rulings':fmap,'acceptance_ledger':accept,'rejection_ledger':rejects,'passes':[{'pass':1,'focus':'Standard rules and source-supported core FAQ/Spirit/card interactions','new_questions':69,'ids':'Q21–Q89','meaningful_after_novelty_recheck':68},{'pass':2,'focus':'FAQ inventory unmatched branches, timing, conditional failures','new_questions':11,'ids':'Q90–Q100','meaningful_after_novelty_recheck':10},{'pass':3,'focus':'Resource ownership and simultaneous defensive site loss','new_questions':2,'ids':'Q101–Q102'},{'pass':4,'focus':'Phase priority and all core loss checkpoints','new_questions':1,'ids':'Q103'},{'pass':5,'focus':'Recheck every mapped core passage, boundaries, quantities, supply and targets','new_questions':0},{'pass':6,'focus':'Challenge timing/priority/exception interactions, original Spirit/card FAQ and exclusions','new_questions':0}],'stopping_rule':{'consecutive_zero_addition_passes':[5,6],'all_in_scope_procedural_passages_mapped':True,'independent_challenge':'pending','claim':'Working saturation within documented sources/scope and novelty criteria, not all conceivable scenarios.'},'input_hashes':{str(p):H(p) for p in [B/'expanded-v4/questions.json',B/'expanded-v4/answer-key.json',book]}}
(B/'coverage-ledger.json').write_text(json.dumps(ledger,indent=2,ensure_ascii=False)+'\n')
print('Mapped',len(rows),'rulebook passages and',len(fmap),'FAQ rulings; all in-scope procedures have IDs. Two zero-addition passes saved; independent challenge pending.')
