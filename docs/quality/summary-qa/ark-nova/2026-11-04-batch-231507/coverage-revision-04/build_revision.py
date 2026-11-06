import copy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
QA = HERE.parent
PRIOR = QA / 'coverage-revision-03'
BASE = QA / 'benchmark-v1.2'

def read(path): return json.loads(path.read_text())
def write(name, value): (HERE/name).write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n')
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

challenge = read(QA/'coverage-challenge-05/report.json')
sc03 = read(QA/'source-key-correction-SC03.json')
sc04 = read(QA/'source-key-precision-SC04.json')
q0 = read(PRIOR/'questions.json')
a0 = read(PRIOR/'answer-key.json')
f0 = read(PRIOR/'material-requested-facts.json')
m0 = read(PRIOR/'coverage-map.json')
l0 = read(PRIOR/'novelty-rejection-ledger.json')
assert challenge['result']['distinct_unrequested_procedural_gaps_requiring_new_question'] == 0
q = copy.deepcopy(q0); a = copy.deepcopy(a0); f = copy.deepcopy(f0)
for d in [q,a]:
    d['benchmark_version'] = 'coverage-revision-04-SC01-SC02-SC03-SC04'
q['questions'] = [r for r in q['questions'] if r['id'] != 'Q47']
a['answers'] = [r for r in a['answers'] if r['id'] != 'Q47']
del f['Q47']
for correction in [sc03, sc04]:
    x = correction['affected_id']
    idx = next(i for i,r in enumerate(a['answers']) if r['id'] == x)
    assert a['answers'][idx] == correction['old_entry']
    a['answers'][idx] = copy.deepcopy(correction['corrected_entry'])
    f[x]['material_requested_facts'] = copy.deepcopy(correction['corrected_entry']['material_requested_facts'])
    f[x]['source_references'] = correction['corrected_entry']['source_references']
f['Q07']['material_requested_facts'] = [f0['Q07']['material_requested_facts'][0].replace('Track bonuses immediate once. ', '')]
f['Q07']['contextual_source_facts_not_requested'] = ['Track bonuses immediate once.']
f['Q07']['requested_context_distinction'] = 'The unchanged frozen Q07 answer includes this source-supported bonus-timing context. The question does not request it; do not require it as a grading part or use Q07 as literal coverage of reputation-bonus cells. Range, CardsII reputation10 gate, overflow conversion and discard inspection remain requested.'
write('questions.json', q); write('answer-key.json', a); write('material-requested-facts.json', f)
active = {r['id'] for r in q['questions']}
assert len(active) == 94

cover47 = ['Q08','Q09','Q12','Q15','Q35','Q46']
edge_keys = {'question_ids','covered_by','procedure_covered_by','procedure_covered_by_active_ids','active_procedure_covering_ids'}
def rewrite(obj):
    if isinstance(obj,list): return [rewrite(v) for v in obj]
    if not isinstance(obj,dict): return obj
    result = {}
    for k,v in obj.items():
        if k in edge_keys and isinstance(v,list):
            result[k] = sorted({y for x in v for y in (cover47 if x=='Q47' else [x])}, key=lambda x:int(x[1:]))
        else: result[k] = rewrite(v)
    return result

remap = read(PRIOR/'transitive-retirement-map.json')
remap = {x: sorted({z for y in ids for z in (cover47 if y=='Q47' else [y])},key=lambda x:int(x[1:])) for x,ids in remap.items()}
remap['Q47'] = cover47
write('transitive-retirement-map.json', remap)

oldq47 = next(r for r in q0['questions'] if r['id']=='Q47')
olda47 = next(r for r in a0['answers'] if r['id']=='Q47')
n01 = next(r for r in challenge['findings'] if r['id']=='C05-N01')
archive47 = {'id':'Q47','status':'retired_pre_reader_strict_novelty','historical_question':oldq47,'historical_answer':olda47,
    'historical_material_fact_entry':f0['Q47'],'independent_decision':n01,'active_procedure_covering_ids':cover47}
write('rejected-candidate-entries.json', {'new_retirements':[archive47],
    'earlier_archives_preserved':['../coverage-revision-03/rejected-candidate-entries.json','../coverage-revision-02/rejected-candidate-entries.json','../coverage-revision-01/rejected-candidate-entries.json'],
    'stable_ids_never_reused':True})
lookups = rewrite(read(PRIOR/'shared-source-lookup-facts.json'))
lookups.append({'lookup_id':'lookup-Q47','retired_id':'Q47','source_references':olda47['source_references'],
    'all_printed_or_contextual_facts_preserved':f0['Q47']['material_requested_facts'],'historical_expected_answer':olda47['expected_answer'],
    'procedure_covered_by':cover47,'coverage_caution':'Four examples instantiate the Q46 copied-side policy and separately requested ordinary permissions. The examples remain lookup/context and do not earn another standalone question.',
    'four_example_policy_and_permission_edges':[
        {'example':1,'source':'Glossary p2 example1','policy_question_ids':['Q46'],'permission_question_ids':['Q08','Q09'],'printed_fact':'Copied BuildII can build a special enclosure and cover upgrade spaces even if own Build isI.'},
        {'example':2,'source':'Glossary p2 example2','policy_question_ids':['Q46'],'permission_question_ids':['Q12'],'printed_fact':'Copied AnimalsII can play an upgrade-required animal even if own Animals isI.'},
        {'example':3,'source':'Glossary p3 example3','policy_question_ids':['Q46'],'permission_question_ids':['Q15'],'printed_fact':'Copied AssociationI cannot gain a third partner even if own Association isII.'},
        {'example':4,'source':'Glossary p3 example4','policy_question_ids':['Q46'],'permission_question_ids':['Q09','Q35'],'printed_fact':'Unique building played by copied Sponsors still uses own Build side for upgrade-marked space permission.'}]})
write('shared-source-lookup-facts.json',lookups)
m = rewrite(copy.deepcopy(m0)); m['revision'] = 'coverage-revision-04'
m['authoring_role'] = 'Source-only author applying challenge05; fresh final independent acceptance pending.'
byid = {r['passage_id']:r for r in m['passages']}
resolutions = []
for i, repair in enumerate(challenge['mapping_precision_repairs'],1):
    for pid in repair['passage_ids']:
        p = byid[pid]
        p['question_ids'] = [x for x in p['question_ids'] if x not in repair.get('remove_question_edges',[])]
        assert set(repair.get('retain_question_edges',[])) <= set(p['question_ids'])
        if 'new_lookup_fact_ids' in repair:
            p['lookup_fact_ids'] = [x for x in p.get('lookup_fact_ids',[]) if x not in repair['old_lookup_fact_ids']] + repair['new_lookup_fact_ids']
        if 'add_lookup_fact_ids' in repair:
            p['lookup_fact_ids'] = list(dict.fromkeys(p.get('lookup_fact_ids',[])+repair['add_lookup_fact_ids']))
        if repair.get('field')=='novelty_credit':
            p['novelty_credit'] = 'None separately: actual printed capped aggregate is retained in lookup-Q138; active prompts cover shared immediate/count/scope/cap procedures.'
        if repair.get('field')=='revision_note':
            p['revision_note'] = 'F02 retained: complete printed income payoff table is lookup-Q136 without standalone question credit. Q19 requests break order and income procedure, not every payoff cell.'
        p['revision04_precision_note'] = repair['reason']
    resolutions.append({'group':i,**repair,'status':'applied'})
byid['GAB.hypnosis_four_upgrade_examples'].update(question_ids=cover47,lookup_fact_ids=['lookup-Q47'],
    coverage_mode='shared_policy_and_existing_action_permissions_plus_preserved_four_example_lookup',
    revision04_note='Q47 retired as direct policy instantiation, C05-N01. Q46 asks copied-side policy; ordinary permission questions remain separately referenced. All four examples retained without novelty credit.')
byid['GAB.digging']['passage'] = 'Digging offers up to two optional selections; choose display-discard/refill or hand-discard/deck-draw after each result; immediate display refill uses ordered compaction'
byid['M13e']['passage'] = 'Up to two optional selections from display-discard/refill or hand-discard/deck-draw; choice-by-choice decisions and immediate refill'
for x in ['GAB.digging','M13e']:
    byid[x]['revision04_source_correction'] = 'SC03: Main p13 lower hand-fan Crested Porcupine says Choose up to2x. This is an optional maximum, not two mandatory selections; Q42 unchanged.'
byid['FAQ.map5_special']['passage'] = 'One Reptile House or one Large Bird Aviary free before Build upgrade; choose one, not both, obey normal placement restrictions'
byid['GM.5']['revision04_precision_note'] = 'SC04 names the special-bonus alternatives as Reptile House or Large Bird Aviary, one only, free before Build upgrade with normal placement restrictions; all other Map5 income clauses unchanged.'
byid['M02g']['revision_note'] = 'F01 retained as source evidence: different-category counting and the complete Species Diversity tier table remain lookup-Q135; earlier prompts cover category counting and support procedures. The printed table does not earn standalone novelty credit.'
for x in ['M09c','M09e']:
    byid[x]['requested_context_distinction'] = 'Q07 requests range, CardsII reputation10 gate, overflow conversion and discard inspection. Its unchanged key sentence Track bonuses immediate once is unrequested source context, not an additional Q07 grading part. Shared immediate-effect timing is requested by Q10 and the printed reputation cells remain lookup-Q131.'
for correction in [sc03,sc04]:
    m['source_key_corrections'].append({'id':correction['id'],'question_id':correction['affected_id'],
        'classification':correction['classification'],'evidence_file':correction['id']+'-source-key-evidence.json',
        'no_new_question_credit':True})
m['shared_source_lookup_facts'] = lookups
write('coverage-map.json',m)
write('mapping-precision-resolutions.json',resolutions)
write('SC03-source-key-evidence.json',sc03); write('SC04-source-key-evidence.json',sc04)
corrections = read(PRIOR/'source-key-corrections.json')
for correction in [sc03,sc04]:
    corrections.append({k:copy.deepcopy(v) for k,v in correction.items() if k!='reader_state'})
write('source-key-corrections.json',corrections)
write('challenge-findings-resolution.json', {'challenge_report':'../coverage-challenge-05/report.json',
    'source_report_sha256':sha(QA/'coverage-challenge-05/report.json'),'new_distinct_question_gaps':0,
    'findings':[
        {'finding':'C05-K01','resolution':'Exact SC03 corrected Q133 key and facts; optional maximum in ledger and both map descriptions.'},
        {'finding':'C05-N01','resolution':'Retire only Q47; full historical key/facts and four examples remain lookup, with live policy/permission edges.'},
        {'finding':'C05-K02','resolution':'Exact SC04 corrected Q116 key/facts; name one Reptile House or one Large Bird Aviary, free before upgrade with normal placement.'},
        {'finding':'C05-P01','resolution':'Frozen Q07 key unchanged; separate source-supported Track bonuses immediate once as unrequested context in facts index, not grading requirement.'}],
    'mapping_groups_applied':14,'no_new_question_ids':True})
ledger = copy.deepcopy(l0)
ledger.update(revision='coverage-revision-04',active_question_count=94,current_retirement_count=1,current_retire_ids=['Q47'],
    all_rejected_historical_ids=sorted(set(l0['all_rejected_historical_ids'])|{'Q47'},key=lambda x:int(x[1:])),
    source_corrections=corrections,retirement_map=remap)
ledger['accepted_candidates'] = [r for r in ledger['accepted_candidates'] if r['id']!='Q47']
for r in ledger['accepted_candidates']:
    if r['id'] in ['Q116','Q133']:
        facts_key = 'new_requested_facts' if 'new_requested_facts' in r else 'material_requested_facts'
        r[facts_key] = copy.deepcopy(f[r['id']]['material_requested_facts'])
        r['source_correction'] = 'SC03' if r['id']=='Q133' else 'SC04'
ledger['grading_precision'] = {'Q07':'Frozen key unchanged; Track bonuses immediate once is source-supported contextual information, not a requested grading part.'}
ledger['current_novelty_rejection'] = n01
ledger['prior_revision_passes'] = l0['revision_passes']
ledger['prior_author_closure_passes'] = l0['closure_passes']
ledger['revision_passes'] = [{'pass':1,'addition_count':0,'new_ids':[],
    'target':'Apply all challenge05 findings: Q47 retirement, exact SC03/SC04, Q07 requested/context classification, 14 mapping groups.',
    'source_map_complete_after_pass':True}]
ledger['closure_passes'] = []; ledger['terminal_zero_addition_passes'] = 0
ledger['next_step'] = 'Two terminal source-map author passes after complete repairs, preservation checks, then fresh independent challenge.'
ledger['retirement_basis'] = 'Pre-reader strict-novelty finding C05-N01; no reader output or grade read or used.'
ledger['retained_other_question_and_keyobjects_unchanged'] = 'All question objects unchanged; all surviving keys unchanged except explicitly versioned Q116/SC04 and Q133/SC03.'
write('novelty-rejection-ledger.json',ledger)

assert q['questions'][:20] == read(BASE/'questions.json')['questions']
assert a['answers'][:20] == read(BASE/'answer-key.json')['answers']
assert len(m['passages']) == 232
assert len(ledger['accepted_candidates']) == 74
assert len(ledger['all_rejected_historical_ids']) == 46
assert all(set(r['question_ids']) <= active for r in m['passages'])
assert all(set(ids) <= active for ids in remap.values())
print('Prepared94 active questions,232 passage records,46 historical retirements; all14 mapping repairs applied. Terminal passes pending.')
