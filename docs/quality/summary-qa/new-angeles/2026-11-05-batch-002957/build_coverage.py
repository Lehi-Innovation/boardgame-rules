from pathlib import Path
import json,re,hashlib
B=Path(__file__).parent;V=B/'expanded-candidate-v1';q=json.loads((V/'questions.json').read_text());k=json.loads((V/'answer-key.json').read_text());qmap={x['id']:x for x in q['questions']};km={x['id']:x for x in k['answers']}
mapids={
'S01':[1],'S02':[1],'S03':[1],'S04':[1,2],'S05':[1,16,17],'S06':[1],'S07':[1,21],
'R01':[77],'A01':[3,14,26],'A02':[2,23],'A03':[18],'A04':[3,14,41],'A05':[3,78],
'D01':[4,17],'D02':[4],'D03':[5],'D04':[5,79],'D05':[6],'D06':[4,6,35],'D07':[7],'D08':[24,42,49],
'P01':[8,19],'P02':[8,18,80],'P03':[9],'P04':[20,53],'E01':[19,81],'E02':[17,12,76],'E03':[19],
'Q01':[15,67],'Q02':[15],'Q03':[15,16],'M01':[10,21,59],'M02':[21],'M03':[10,61],'M04':[10],'M05':[10,51],'M06':[18,21],
'U01':[9,12,82],'I01':[11],'I02':[11,52,64],'C01':[12],'T01':[13],'T02':[13,43],'H01':[17,18],'X01':[14,26,41],'W01':[22],'W02':[16,81],'W03':[16]}
rows=[]
text=(B/'source-inventory/source-inventory.md').read_text();section=text.split('## Core procedure and branch inventory\n',1)[1].split('## Exact corporation',1)[0]
for line in section.splitlines():
 m=re.match(r'\| ([A-Z]\d\d) \| (.*?) \| (.*?) \|$',line)
 if not m:continue
 ident,procedure,source=m.groups();ids=[f'Q{x:02d}' for x in mapids[ident]]
 rows.append({'passage_id':ident,'source_refs':[source],'procedural_content':procedure,'actually_asked_coverage':[{'question_id':i,'question':qmap[i]['question'],'asked_fact_anchor':km[i]['required_facts']} for i in ids],'status':'mapped; independent scope review pending'})
asset_ids={0:[28],1:[42],2:[43],3:[23],4:[7],5:[32],6:[31],7:[47],8:[29],9:[40],10:[30],11:[24],12:[44],13:[37],14:[49],15:[33],16:[46],17:[26],18:[33,34],19:[45],20:[36],21:[35],22:[47],23:[48],24:[48],25:[37],26:[27],27:[47],28:[38],29:[41],30:[35],31:[17],32:[25],33:[39]}
# Gurren is intentionally not separately memorized: fixed payment on discard/claim; its procedural timing is within Q37 sequential first-claim handling.
components=[]
for i,ids in asset_ids.items():components.append({'source':f'asset-cards-face.jpg zero-based cell{i}','questions':[f'Q{x:02d}' for x in ids] if i!=13 else [],'coverage_kind':'distinct printed procedural branch' if i!=13 else 'consultation-only fixed payout; no independent exact-value coverage credit','note':'Q37 asks generic first-claim timing, not Gurren’s amount. Fixed Gurren payout adds no distinct procedure beyond existing on-claim discard/payout effects, so no exact-value memorization question or credit.' if i==13 else ''})
components += [{'source':'all corporation sheet cells0–5 bothsides','questions':['Q02','Q12'],'coverage_kind':'all draws/contracts and FAQ exceptions'}, {'source':'emergency faces0–5','questions':['Q07','Q50'],'coverage_kind':'status lifecycle and complete procedures'}]
action_map={'Labor':[52,54,51,53],'Media':[58,58,55,56],'Security':[62,59,61,62],'Construction':[21,63,64,65],'Biotech':[66,66,67,68]}
# Correct actual IDs are derived from wording rather than handwritten offsets.
def find(term):return [x['id'] for x in q['questions'] if term in x['question']]
for family,names in {'Labor':['Efficiency Experts','High-Risk Investments','Labor Solutions','Liquidation'],'Media':['Media Circus','24/7 Live Feeds','Puff Piece','Spin Doctors'],'Security':['Arrest Orders','Full Deployment','Riot Control','Scorched Earth'],'Construction':['Ark Construction','Gentrification','Budget Renovations','Vanity Project'],'Biotech':['Clean Slate','Clinical Trials','Information Procurement','Unorthodox Knowledge']}.items():
 for slot,name in enumerate(names):
  ids=find(name)
  components.append({'source':f'{family} action group{slot} cells{slot*5}–{slot*5+4}','name':name,'questions':ids or ['Q21','Q08'],'coverage_kind':'printed timing/exception/conditional branch' if ids else 'ordinary placement and development capacity/modifier already asked; no new card-specific procedure','consultation_only':'Five duplicate copies do not create five rule questions.'})
for group,terms in [('investment',['Energy Sector','Banking','Healthcare','Populist']),('event',['Helium-3','Human First Starts','Beanstalk Owned','Activist Cells','Record Unemployment','Humanity Labor'])]:
 for term in terms:components.append({'source':group+' family '+term,'questions':find(term),'coverage_kind':'printed consequential condition/timing family; exact duplicate formulas grouped'})
components += [{'source':'all six setup and nine demand cards, seven rivals','questions':['Q01','Q15','Q16'],'coverage_kind':'identical procedures with instance values; no extra question for changed starting districts/targets/failure amounts/identity names'}]
rejections=[
{'candidate':'Another counteroffer cost with larger ordinal','reason':'Same escalation branch already Q05/Q28; changed number only.'},
{'candidate':'Different city district numbers for duplicate spillover','reason':'Same exiting-path/duplicate/prisec/Root outcome Q10, Q21.'},
{'candidate':'Another unnamed illness action in two rather than three ill districts','reason':'Same once-per-action trigger Q11; mere count change.'},
{'candidate':'Every one of100 action copies','reason':'Only20distinct instructions; five copies each do not add procedure.'},
{'candidate':'Every setup placement list and demand target vector','reason':'Same setup placement/demand comparison procedure; instance memorization, no new branch.'},
{'candidate':'Separate Banking/Entertainment formula questions','reason':'Identical formula/cap, grouped in one reference question.'},
{'candidate':'Separate Gang Wars/Tri-Maf and Crumbling/Rolling formula questions','reason':'Identical upper effects, only later placements/counts differ; grouped.'},
{'candidate':'Gurren fixed5capital isolated lookup','reason':'No new timing beyond when-claimed discard already tested by Q37/Q49; fixed amount consultation retained in summary.'},
{'candidate':'Arrest Orders absent reserve/impossible cost success; universal do-as-much-as-possible','reason':'No explicit universal feasibility/priority rule in assigned sources; do not invent. Printed normal instruction asked Q62, narrow unresolved edge separately recorded.'},
{'candidate':'A general stack for multiple simultaneous newly enabled assets','reason':'Source only supplies RR6.4 ordering and named FAQ exceptions. Unsupported generalized interrupt stack is not a question.'},
{'candidate':'Introductory first-game setup and preset hands','reason':'Explicitly excluded from assigned normal complete-setup scope.'},
{'candidate':'Expansion/variant-only effect assumed by hypothetical','reason':'No positive base source; excluded scope cannot import a special rule.'}
]
ledger={'scope':'FFG2016 base4–6, complete setup, official2018FAQ; printed component procedures','source_inventory_method':'Parent complete source review plus independent source-only inventory; every source-linked fact must be actually asked, contextual key background alone not coverage. Fresh review pending.','passes':[{'pass':1,'focus':'Printed exceptions, card-specific timing, actor/cost/priority and scoring branches','accepted_ids':[f'Q{i:02d}' for i in range(21,77)],'accepted_count':56},{'pass':2,'focus':'All core source procedural passages versus actually asked clauses; scope corrected facts','accepted_ids':[f'Q{i:02d}' for i in range(77,83)],'accepted_count':6}], 'acceptance':json.loads((V/'accepted-candidates.json').read_text()),'rejections':rejections,'stopping_rule':{'consecutive_zero_addition_passes':0,'independent_challenge':'pending'}}
(V/'coverage-map.json').write_text(json.dumps({'core_passages':rows,'component_families':components},indent=2,ensure_ascii=False)+'\n');(V/'coverage-ledger.json').write_text(json.dumps(ledger,indent=2,ensure_ascii=False)+'\n')
# Each required-fact item is a candidate asked-clause mapping; reviewer must remove context-only credit without changing frozen seed entries.
scopes=[]
for x in q['questions']:
 key=km[x['id']];facts=key['required_facts'];context=list(key.get('contextual_background',[]))
 if x['id']=='Q05':context += ['Only topmost current counteroffer operative; earlier cards retained only for cost. This is actually asked in Q79, not independently in Q05.']
 if x['id']=='Q09':context += ['Production before unrest is context, per fresh scope adjudication; requested state branches remain mandatory.']
 if x['id']=='Q18':context += ['Supply zero floor is background, not independently asked in Q18.']
 if x['id']=='Q05': facts=[f for f in facts if not f.startswith('topmost')]
 if x['id']=='Q08':
  facts=['0 credits and1 entertainment under orgcrime/development','protest permits production then becomes strike','starting strike/outage produces no resources','normal Production only android districts']
  context += ['Alternative starting unrest outcomes and ascending district order are not additional clauses in Q08.']
 if x['id']=='Q09': facts=[f for f in facts if f!='production before unrest']
 if x['id']=='Q14':
  facts=[f for f in facts if f!='cannot exhaust twice']; context += ['An exhausted asset cannot exhaust again; not separately asked by this timing/readying question.']
 if x['id']=='Q18': facts=[f.replace('supply final cap and zero floor','supply final cap') for f in facts]
 if x['id']=='Q20':
  facts=['Liquidation produces without exploiting; do not add normal exploitation consequences','Liquidation ignores orgcrime; development and supply caps still apply','Caprice cannot affect Unorthodox Knowledge','Unorthodox resolver not bound by stated resolution']
  context += ['Liquidation target must not be strike/outage; printed strike instruction remains true but full card procedure is not separately asked by Q20. Material false assertions still count.']
 scopes.append({'id':x['id'],'question':x['question'],'candidate_required_asked_facts':facts,'contextual_background':context,'scope_status':'fresh independent review pending'})
(V/'asked-clause-map.json').write_text(json.dumps(scopes,indent=2,ensure_ascii=False)+'\n')
print(len(rows),'coreproceduralpassages mapped;',len(components),'componentfamilies; candidateN',len(q['questions']))
