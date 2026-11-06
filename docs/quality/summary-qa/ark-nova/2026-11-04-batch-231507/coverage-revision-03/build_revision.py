import copy
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent;QA=HERE.parent;PRIOR=QA/'coverage-revision-02';BASE=QA/'benchmark-v1.2'
def read(path):return json.loads(path.read_text())
def write(name,value):(HERE/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

q0=read(PRIOR/'questions.json');a0=read(PRIOR/'answer-key.json');f0=read(PRIOR/'material-requested-facts.json');m0=read(PRIOR/'coverage-map.json');l0=read(PRIOR/'novelty-rejection-ledger.json')
bq=read(BASE/'questions.json');ba=read(BASE/'answer-key.json')
challenge=read(QA/'coverage-challenge-03/report.json');adjud=read(QA/'novelty-adjudication-04/report.json')
assert adjud['counts']['all_retire']==37
retired=set(adjud['retire_ids'])
decisions={r['id']:r for r in adjud['decisions']}
assert 'Q70' not in retired
assert {r['target'] for r in challenge['novelty_rejections']}<=retired
assert bq['questions']==q0['questions'][:20]
assert [r['id'] for r,s in zip(ba['answers'],a0['answers'][:20]) if r!=s]==['Q17']
new=read(HERE/'provisional-Q140.json')
newq={'id':new['id'],'question':new['question']}
newa={k:new[k] for k in ['id','expected_answer','material_requested_facts','source_references']}
q=copy.deepcopy(q0);a=copy.deepcopy(a0)
for d in [q,a]:d.update(benchmark_version='coverage-revision-03-SC01-SC02',baseline_benchmark='benchmark-v1.2 / SC01 size bands + SC02 mandatory special-enclosure priority')
q['questions']=copy.deepcopy(bq['questions'])+[copy.deepcopy(r) for r in q0['questions'][20:] if r['id'] not in retired]+[newq]
a['answers']=copy.deepcopy(ba['answers'])+[copy.deepcopy(r) for r in a0['answers'][20:] if r['id'] not in retired]+[newa]
active={r['id'] for r in q['questions']}
assert len(active)==95
assert active==set(adjud['surviving_input_ids'])|{'Q140'}
write('questions.json',q);write('answer-key.json',a)

remap={qid:decisions[qid]['transitive_surviving_covering_ids'] for qid in retired}
def survivors(qid,seen=()):
    if qid in active:return [qid]
    assert qid not in seen,(qid,seen)
    assert qid in remap,('Unknown coverage edge',qid)
    result=[]
    for child in remap[qid]:result.extend(survivors(child,seen+(qid,)))
    return sorted(set(result),key=lambda x:int(x[1:]))
resolved={qid:survivors(qid) for qid in retired}
assert all(set(ids)<=active for ids in resolved.values())
write('transitive-retirement-map.json',resolved)

archive=[];lookups=[]
for qid in sorted(retired,key=lambda x:int(x[1:])):
    oldquestion=next(r for r in q0['questions'] if r['id']==qid)
    oldanswer=next(r for r in a0['answers'] if r['id']==qid)
    archive.append({'id':qid,'status':'retired_pre_reader_strict_novelty','historical_question':oldquestion,'historical_answer':oldanswer,
        'historical_material_fact_entry':f0[qid],'independent_decision':decisions[qid],'active_procedure_covering_ids':resolved[qid]})
    lookups.append({'lookup_id':'lookup-'+qid,'retired_id':qid,'source_references':oldanswer['source_references'],
        'all_printed_or_contextual_facts_preserved':copy.deepcopy(f0[qid]['material_requested_facts']),
        'historical_expected_answer':oldanswer['expected_answer'],'procedure_covered_by':resolved[qid],
        'coverage_caution':'Active IDs request the shared procedures, not necessarily every retired numeric cell or named card permission. Exact source facts remain lookup evidence without standalone question credit.'})
write('rejected-candidate-entries.json',{'new_retirements':archive,'earlier_archives_preserved':['../coverage-revision-02/rejected-candidate-entries.json','../coverage-revision-01/rejected-candidate-entries.json'],'stable_ids_never_reused':True})

facts={qid:copy.deepcopy(r) for qid,r in f0.items() if qid in active}
facts['Q140']={k:new[k] for k in ['material_requested_facts','source_references']}
facts['Q17']['source_references']=ba['answers'][16]['source_references']
facts['Q17']['origin']='benchmark-v1.2 explicit SC01 bands and SC02 mandatory-priority clarification'
facts['Q17']['material_requested_facts']=[
 'Depicted2− accepts printed standard requirement1or2; depicted3 requires exactly3; depicted4+ accepts4or5. Actual occupied enclosure size and special-enclosure capacity do not set the band.',
 'Lose only printed appeal before conservation reward; discard the animal and its icons, retaining ability-earned appeal, reputation/conservation and past effects.',
 'If the released animal is eligible for the special enclosure and the indicated number of special-enclosure tokens can be removed, you must remove those tokens. Only otherwise use the smallest occupied standard enclosure meeting all requirements, then size-only, then none if none fits.',
 'The same freeing procedure applies to flock animals.'
]
write('material-requested-facts.json',facts)

def rewrite_live_refs(obj):
    if isinstance(obj,list):return [rewrite_live_refs(x) for x in obj]
    if not isinstance(obj,dict):return obj
    result={}
    for k,v in obj.items():
        if k in ['question_ids','covered_by','procedure_covered_by','procedure_covered_by_active_ids','active_procedure_covering_ids'] and isinstance(v,list):
            result[k]=sorted({qid for original in v for qid in survivors(original)},key=lambda x:int(x[1:]))
        else:result[k]=rewrite_live_refs(v)
    return result

m=rewrite_live_refs(copy.deepcopy(m0));m['revision']='coverage-revision-03'
m['authoring_role']='Source-only bank author after independent strict-novelty adjudication; fresh saturation acceptance pending.'
m['baseline_benchmark']='benchmark-v1.2 / explicit SC01+SC02'
for old,p in zip(m0['passages'],m['passages']):
    retired_here=[qid for qid in old['question_ids'] if qid in retired]
    if retired_here:
        p['coverage_mode']='shared_procedure_questions_plus_separate_printed_lookup_evidence'
        p['lookup_fact_ids']=['lookup-'+qid for qid in sorted(set(retired_here),key=lambda x:int(x[1:]))]
        p['coverage_caution']='The active questions cover shared procedures, not a literal request for every retired identity, number or table cell. Consult retained lookup facts for the actual printed data.'
byid={p['passage_id']:p for p in m['passages']}
byid['M05b']['question_ids'].append('Q140')
byid['M05b']['revision03_note']='Random start-player selection and clockwise normal order are explicitly requested by newQ140.'
byid['M06a']['question_ids']=['Q03','Q19','Q140']
byid['M06a']['revision03_note']='Q140 now requests noformalrounds, clockwise normal turns and onenormalaction with additional effects/bonuses; Q03/Q19 did not ask those facts.'
for pid in ['GAB.constriction','GAB.hypnosis','GAB.pilfering_targets','GAB.venom']:
    byid[pid]['question_ids']=sorted(set(byid[pid]['question_ids']+['Q39','Q125']),key=lambda x:int(x[1:]))
    byid[pid]['revision03_note']='C03-F03 precision repair: eligibility and own-appeal timing map toQ39; target sets and Hypnosis slots toQ125. No new novelty credit.'
m['passages'].append({'passage_id':'M05_M06.normal_gameplay','source':'Main PDF p5 global setup7; Main PDF p6 Gameplay firsttwo paragraphs',
 'passage':'Randomly determine start player; ordinary turns clockwise withoutformalrounds; oneaction per ordinary turn may triggeradditional effects/bonuses, withbreaks as required.',
 'disposition':'covered','question_ids':['Q140'],'novelty_credit':'Previously unasked normal-gameplay/start-player procedure; clockwise order is shared context, not a second question.'})
m['source_key_corrections'].append({'id':'SC02','question_id':'Q17','baseline':'benchmark-v1.2','rule':'Mandatory remove-special-tokens priority when eligible and enough indicated tokens can be removed; only otherwise standard-enclosure fallback. SC01 separately preserves printed2−/3/4+ bands.','primary_source':'Glossary p1 Release into the Wild mustalways/onlyif wording.'})
earlier_lookup=rewrite_live_refs(read(PRIOR/'shared-source-lookup-facts.json'))
m['shared_source_lookup_facts']=earlier_lookup+lookups
write('shared-source-lookup-facts.json',earlier_lookup+lookups)
assert len(m['passages'])==232
assert len({p['passage_id'] for p in m['passages']})==232
assert all(set(p['question_ids'])<=active for p in m['passages'])
assert active<={qid for p in m['passages'] for qid in p['question_ids']}
assert all(set(r['procedure_covered_by'])<=active for r in m['shared_source_lookup_facts'])
write('coverage-map.json',m)

# Neutral versioned source/key evidence, excluding unrelated historical process details.
sc01=read(QA/'source-key-correction-SC01.json')
sc02=read(QA/'source-key-clarification-SC02.json')
corrections=[{'id':'SC01','type':'depicted release-band clarification','source_references':sc01['source_references'],'old_entry':sc01['old_entry'],'corrected_entry':sc01['corrected_entry'],'baseline':'benchmark-v1.1'},
 {'id':'SC02','type':'mandatory special-enclosure token priority','primary_source':'Glossary p1 Release into the Wild mustalways/onlyif','old_expected_answer':sc02['old_expected_answer'],'new_expected_answer':sc02['new_expected_answer'],'baseline':'benchmark-v1.2','corrected_entry':ba['answers'][16]}]
write('source-key-corrections.json',corrections)
resolutions=[
 {'finding':'C03-F01','decision':'addQ140','source':'Main pp5–6','map_records':['M05b','M06a','M05_M06.normal_gameplay']},
 {'finding':'C03-F02','decision':'Apply final independent adjudication04: retireall27challenged plus10additional; preserve every printed fact and full historical entry; transitively remap all procedure edges to95actual surviving prompts.','retire_count':37,'adjudicator_verdict':adjud['verdict'],'coordinator_criterion':'Core table completeness itself does not establish new procedural novelty.'},
 {'finding':'C03-F03','decision':'AddQ39/Q125 targeting/eligibility edges toConstriction,Hypnosis,Pilfering-targets,Venom source passages, withoutnewquestioncredit.'},
 {'finding':'Q17 wording','decision':'Inherit exactbenchmark-v1.2 Q17 object; mandatoryspecialtokenpriority, retainingSC01 bands and oldkeyversionevidence. Other19originalkeys unchanged.'}
]
write('challenge-findings-resolution.json',resolutions)
write('independent-novelty-decisions.json',{'adjudication_report':'../novelty-adjudication-04/report.json','report_sha256':digest(QA/'novelty-adjudication-04/report.json'),'counts':adjud['counts'],'retire_ids':adjud['retire_ids'],'decisions':adjud['decisions'],'no_new_gaps':adjud['new_gaps'],'accepted_gap':'Q140'})

accepted=[copy.deepcopy(r) for r in l0['accepted_candidates'] if r['id'] not in retired]+[{'id':'Q140','decision':'add_distinct_missing_gameplay_cluster','material_requested_facts':new['material_requested_facts'],'source_references':new['source_references'],'novelty_reason':new['novelty_reason']}]
ledger={'game':'Ark Nova','revision':'coverage-revision-03','active_question_count':95,'highest_historical_id':'Q140','stable_ids_never_reused':True,
 'baseline':'benchmark-v1.2 with explicit SC01+SC02','original20questionobjects_unchanged':True,'other19originalkeyobjects_unchanged':True,
 'Q17_exactbenchmark_v1_2':True,'Q06_Q42_exact':True,'retained_other_question_and_keyobjects_unchanged':True,
 'accepted_candidates':accepted,'current_retirement_count':37,'current_retire_ids':sorted(retired,key=lambda x:int(x[1:])),
 'all_rejected_historical_ids':sorted(set(l0['all_rejected_historical_ids'])|retired,key=lambda x:int(x[1:])),
 'adjudication_verdict':adjud['verdict'],'retirement_map':resolved,
 'criterion':'A distinct source-supported procedure/outcome/priority/timing/exception is novel; complete numerical tables, names/icon/resource substitutions and unchanged combinations alone are lookup evidence. Actual prompt wording governs procedural coverage; keys cannot silently expand prompts.',
 'retirement_basis':'Pre-reader independent source novelty adjudication only; no reader output or grade read or used.',
 'explicit_keep_borderlines':{qid:decisions[qid] for qid in ['Q70','Q72','Q96','Q100']},
 'source_corrections':corrections,
 'revision_passes':[{'pass':1,'new_ids':['Q140'],'addition_count':1,'target':'Normal gameplay gap,SC02 baseline, final37 noveltyretirements, transitive remapping, fourGABprecisionrepairs, fullsource reread','source_map_complete_after_pass':True}],
 'closure_passes':[],'terminal_zero_addition_passes':0,'open_source_gaps':[],'independent_saturation_accepted':False,
 'prior_closure_claims':'Historical author zero-pass claims were overturned; neither count nor those claims establishes final independent acceptance.',
 'next_step':'Two terminal author source-to-question passes after complete final map, followed by fresh independent saturation challenge.'}
write('novelty-rejection-ledger.json',ledger)
print('Final adjudication applied:95active stableIDs throughQ140;37retirements preserve source lookup and archives;232passage map;SC02baseline exact. Terminal passes pending.')
