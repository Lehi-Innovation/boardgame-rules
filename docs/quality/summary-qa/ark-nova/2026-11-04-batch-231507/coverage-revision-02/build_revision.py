import copy
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
QA=HERE.parent
PRIOR=QA/'coverage-revision-01'
DRAFT=QA/'coverage-draft'
def read(path):return json.loads(path.read_text())
def write(name,value):(HERE/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

q0=read(PRIOR/'questions.json');a0=read(PRIOR/'answer-key.json');f0=read(PRIOR/'material-requested-facts.json')
m0=read(PRIOR/'coverage-map.json');l0=read(PRIOR/'novelty-rejection-ledger.json')
challenge=read(QA/'coverage-challenge-02/report.json')
reject={r['target']:r for r in challenge['novelty_rejections'] if 'target' in r}
assert set(reject)=={'Q65','Q84','Q101','Q128'}

new=[
 {'id':'Q138','question':'How does the illustrated Eurasian Lynx Iconic Animal: Europe ability calculate its appeal reward, when is it gained, and whose Europe icons count?',
  'expected_answer':'When the animal is played, immediately gain 1 appeal for each Europe icon in all players’ zoos combined, including your own zoo, up to a maximum of 8 appeal from this ability. Its own Europe icon counts under the normal self-counting rule.',
  'material_requested_facts':['The reward is an immediate on-play aggregate over all players’ zoos, including your own, rather than only your zoo or future icon plays.','Gain 1 appeal per Europe icon in that combined total, capped at 8 appeal from this ability.','The played Lynx own Europe icon counts under the existing self-counting rule.'],
  'source_references':'source_pdfs/ark-nova-rules.pdf PDF p12, Example: Playing animals (immediate effect), Eurasian Lynx printed card text in both newly drawn card and lower hand fan: Iconic Animal: Europe; Gain1appeal for each Europe icon in all zoos(max8). Glossary p1 Cards Always Count Themselves supplies existing self-counting context.',
  'novelty':'Immediate capped all-zoos aggregation is unrequested elsewhere; changing the continent name alone would not be novel.'},
 {'id':'Q139','question':'Where do players put the Final Scoring card discarded when the first player reaches 10 conservation points, and in what orientation?',
  'expected_answer':'Place it facedown under the pile of remaining Final Scoring cards.',
  'material_requested_facts':['Return the discarded card underneath the remaining Final Scoring pile.','Place it facedown.'],
  'source_references':'source_pdfs/ark-nova-rules.pdf PDF p18, Appeal and Conservation Points, 10conservation points bullet: Place them facedown under the pile of remaining Final Scoring cards.',
  'novelty':'Return underneath a different deck is a previously unrequested destination. Facedown orientation is associated context, not separate novelty.'}
]
q=copy.deepcopy(q0);a=copy.deepcopy(a0)
q['benchmark_version']='coverage-revision-02-source-corrected';a['benchmark_version']=q['benchmark_version']
q['questions']=[copy.deepcopy(r) for r in q0['questions'] if r['id'] not in reject]+[{k:r[k] for k in ['id','question']} for r in new]
a['answers']=[copy.deepcopy(r) for r in a0['answers'] if r['id'] not in reject]+[{k:r[k] for k in ['id','expected_answer','source_references','material_requested_facts']} for r in new]
active={r['id'] for r in q['questions']}
assert len(active)==131
for old,newlist in [(q0['questions'],q['questions']),(a0['answers'],a['answers'])]:
    for r in old:
        if r['id'] not in reject:assert r==next(x for x in newlist if x['id']==r['id'])
assert q['questions'][:20]==q0['questions'][:20]
assert a['answers'][:20]==a0['answers'][:20]
write('questions.json',q);write('answer-key.json',a);write('new-questions.json',new)
facts={qid:copy.deepcopy(r) for qid,r in f0.items() if qid not in reject}
for r in new:facts[r['id']]={k:r[k] for k in ['material_requested_facts','source_references']}
write('material-requested-facts.json',facts)
archive=[{'id':qid,'status':'rejected_standalone_novelty_not_active','independent_rejection':r,
    'historical_question':next(x for x in q0['questions'] if x['id']==qid),
    'historical_answer':next(x for x in a0['answers'] if x['id']==qid),'historical_material_facts':f0[qid]} for qid,r in reject.items()]
write('rejected-candidate-entries.json',{'current_revision_rejections':archive,
    'earlier_archive_preserved_at':'../coverage-revision-01/rejected-candidate-entries.json','earlier_rejected_ids':l0['rejected_historical_ids'],'prior_archive_not_modified':True})

# Exact source lookup cells stay visible; these do not receive separate novelty credit.
lookup=[
 {'id':'lookup205','source':'Glossary p4 Sponsor205 Gorilla Field Research','printed_facts':['On play gain2reputation and1conservation.'],'procedure_covered_by':['Q10','Q11','Q18'],'rejected_id':'Q65'},
 {'id':'lookup226','source':'Glossary p6 Sponsor226 Foreign Institute','printed_facts':['On play gain2reputation.','At final scoring gain1conservation if all5continent icons are in your zoo.'],'procedure_covered_by':['Q10','Q18','Q20','Q83'],'rejected_id':'Q84'},
 {'id':'lookup255_256','source':'Glossary p7 Sponsor255 Adventure Playground and256 Water Playground','printed_facts':['Each gives4appeal on play and requires its unique building.','Adventure Playground requires at least1rock neighbor; Water Playground requires at least1water neighbor.'],'procedure_covered_by':['Q10','Q11','Q31','Q35','Q92'],'rejected_id':'Q101'},
 {'id':'lookup_uni3','source':'Main p7 Map A university-column diagram','printed_facts':['Third university slot grants2conservation immediately.'],'procedure_covered_by':['Q15','Q120','Q121'],'rejected_id':'Q128'}
]
write('shared-source-lookup-facts.json',lookup)
remap={r['rejected_id']:r['procedure_covered_by'] for r in lookup}
m=copy.deepcopy(m0);m['revision']='coverage-revision-02'
m['authoring_role']='Bank author revision after fresh challenge02; independent saturation acceptance pending.'
for p in m['passages']:
    original=list(p['question_ids']);updated=[]
    for qid in original:updated.extend(remap.get(qid,[qid]))
    p['question_ids']=sorted(set(updated),key=lambda x:int(x[1:]))
    removed=[qid for qid in original if qid in reject]
    if removed:p['revision02_note']='Standalone named/numeric lookup question(s) '+','.join(removed)+' rejected; actual procedures map to active earlier questions. Printed cells retained in shared-source-lookup-facts.json.'
byid={p['passage_id']:p for p in m['passages']}
byid['M12b']['question_ids']=sorted(set(byid['M12b']['question_ids']+['Q95','Q130','Q138']),key=lambda x:int(x[1:]))
byid['M12b']['passage']='Caiman standard/special choice; newly drawn Lynx can become second animal; printed Owl Perception4/Marabou Scavenging2 instantiate existing selection procedures; Lynx immediate capped all-zoos Europe aggregate'
byid['M12b']['revision02_note']='C02-F01 corrects the prior omission of embedded Lynx effect; sequence alone did not test that aggregate.'
byid['M18b']['question_ids'].append('Q139')
byid['M18b']['passage']='Conservation milestones2upgrade/worker,5/8money/tile,10all discard1FinalScoring and return facedown underneath remaining FinalScoringpile'
byid['M18b']['revision02_note']='C02-F02: Q20 retains timing/choice; Q139 explicitly requests the previously unasked destination.'
for pid in ['GSP.205','GSP.226','GSP.255','GSP.256']:
    byid[pid]['coverage_mode']='shared_procedure_plus_retained_printed_lookup_not_standalone_novelty'
    byid[pid]['printed_lookup_fact_file']='shared-source-lookup-facts.json'
for pid in ['M06d','M07c']:
    byid[pid]['revision02_university_note']='The third-university2conservation cell is retained as shared diagram evidence; Q15 supplies placement/bonus procedure. It no longer earns standaloneQ128 novelty credit.'
m['passages'] += [
 {'passage_id':'M12c','source':'Main PDF p12, both Eurasian Lynx cards in immediate-effect example','passage':'Iconic Animal Europe immediate1appeal per Europe icon in all zoos combined, max8; own icon counts','disposition':'covered','question_ids':['Q30','Q138'],'novelty_credit':'Q138 immediate capped aggregate; Q30 self-counting is existing context.'},
 {'passage_id':'M18e','source':'Main PDF p18, 10conservation milestone, discard-destination sentence','passage':'Discarded FinalScoring card is placed facedown underneath remaining FinalScoringpile','disposition':'covered','question_ids':['Q139','Q20'],'novelty_credit':'Q139 deck destination; Q20 timing/choice is existing context.'}
]
m['shared_source_lookup_facts']=lookup
assert len(m['passages'])==231
assert all(set(p['question_ids'])<=active for p in m['passages'])
assert active<={qid for p in m['passages'] for qid in p['question_ids']}
assert all(set(r['procedure_covered_by'])<=active for r in lookup)
write('coverage-map.json',m)

resolutions=[
 {'finding':'C02-F01','resolution':'AddQ138, primary p12 Lynx effect verified in both pictured cards; update M12b and add M12c.','question_ids':['Q138'],'primary_sources':['Main p12 Eurasian Lynx printed Iconic Animal Europe effect','Glossary p1 own-icon context']},
 {'finding':'C02-F02','resolution':'AddQ139, exact p18 discard-destination sentence; update M18b and add M18e.','question_ids':['Q139'],'primary_sources':['Main p18 10conservation milestone']},
 {'finding':'C02-F03','resolution':'Archive Q65/Q84/Q101/Q128 full entries/reasons and retain printed lookup facts; all procedural coverage remapped to active earlier questions with no deadQ65edge.','rejected_ids':sorted(reject,key=lambda x:int(x[1:])),'primary_sources':['Glossary p4 Sponsor205','Glossary p6 Sponsor226','Glossary p7 Sponsors255–256','Main p7 MapA university-column diagram']}
]
write('challenge-findings-resolution.json',resolutions)
accepted=[copy.deepcopy(r) for r in l0['accepted_candidates'] if r['id'] not in reject]
accepted += [{'id':r['id'],'decision':'add_distinct_source_procedure','new_requested_facts':r['material_requested_facts'],'source_references':r['source_references'],'novelty_reason':r['novelty']} for r in new]
ledger={'game':'Ark Nova','revision':'coverage-revision-02','active_question_count':131,'highest_historical_id':'Q139','historical_candidate_count':139,
    'baseline':'Corrected benchmark-v1.1 inherited unchanged via revision01','retained_question_and_key_objects_unchanged':True,'renumbered_ids':False,
    'all_rejected_historical_ids':sorted(set(l0['rejected_historical_ids'])|set(reject),key=lambda x:int(x[1:])),
    'accepted_candidates':accepted,'current_novelty_rejections':challenge['novelty_rejections'],
    'earlier_novelty_rejections':l0['novelty_rejections'],
    'dead_edge_resolution':{'Q84_requested_covering_Q65':'Resolved to activeQ10/Q18 for immediate reward; final condition toQ83 withQ20 final timing. No source map or active coverage dependency points toQ65.'},
    'prior_zero_pass_status':'Overturned by fresh challenge02; preserved original revision01 and draft claims are historical only.',
    'revision_passes':[{'pass':1,'target':'Fresh33-page primary reading and embedded-card/destination verification','new_ids':['Q138','Q139'],'addition_count':2,'novelty_rejections':['Q65','Q84','Q101','Q128'],'source_map_complete_after_pass':True}],
    'closure_passes':[],'terminal_zero_addition_passes':0,'independent_final_audit_claimed':False,'reader_results_used':False,'open_source_gaps':[],
    'next_step':'Two post-map targeted author passes, then fresh independent saturation challenge.'}
write('novelty-rejection-ledger.json',ledger)
print('131 active stable IDs throughQ139; retained question/key objects exact. 231 primary passage records, all remapped IDs active. New findingsF01–F03 resolved; closure passes pending.')
