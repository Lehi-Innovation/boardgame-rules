"""Verify completed93 pair02 original grades, fixed v9 scope and one neutral."""
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

B=Path(__file__).resolve().parent
ROOT=B.parents[4]
R=ROOT/'docs/quality/summary-qa/new-angeles'/B.name
D=R/'expanded-luna-iteration-02'
load=lambda p:json.loads(p.read_text())
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
canonical=lambda v:hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
questions={x['id']:x for x in load(D/'questions.json')['questions']}
key={x['id']:x for x in load(R/'expanded-candidate-v9/answer-key.json')['answers']}
scope={x['id']:x for x in load(R/'expanded-candidate-v9/asked-clause-map.json')}
selection=load(D/'reader-output-manifest.json')
raw_paths={w:Path(selection[w]) for w in 'ab'}
raw={w:{x['id']:x for x in load(p)['answers']} for w,p in raw_paths.items()}
for w in 'ab': assert list(raw[w])==list(questions)
initial=Path(selection['a_initial_incomplete_path'])
assert H(initial)==selection['a_initial_incomplete_sha256'] and initial!=raw_paths['a']
plan=load(D/'grading/input-manifest.json')
totals={w:Counter() for w in 'ab'}; facts={w:0 for w in 'ab'}; assessments={w:0 for w in 'ab'}; seen=set(); reports=[]; split_vectors=[]
for task in plan['blocks']:
    pp=Path(task['pack']); rp=Path(task['output']); assert H(pp)==task['pack_sha256']
    pack=load(pp); report=load(rp); ids=task['ids']; assert pack['ids']==ids
    for name,h in pack['source_file_hashes'].items(): assert H(Path(name))==h
    assert pack['questions']==[questions[i] for i in ids]
    assert pack['fixed_key']==[key[i] for i in ids]
    assert pack['asked_clause_map']==[scope[i] for i in ids]
    for w in 'ab':
        assert pack['complete_raw_reader_entries'][w]==[raw[w][i] for i in ids]
        for ident in ids: assert pack['raw_entry_sha256'][w][ident]==canonical(raw[w][ident])
    records=report.get('grades',report.get('records'))
    assert len(records)==len(ids)*2
    actual=set()
    for x in records:
        w,i=x['reader'],x['id']; assert w in 'ab' and i in ids and (w,i) not in actual
        actual.add((w,i)); assert x['raw_entry_sha256']==canonical(raw[w][i])
        if len(x['asked_fact_assessments'])!=len(scope[i]['asked_facts']):
            assert i in ['Q65','Q67','Q68','Q69','Q72','Q73','Q75','Q76','Q77']
            split_vectors.append({'reader':w,'id':i,'mapped':scope[i]['asked_facts'],'grader_split_clauses':[a.get('required_clause',a.get('asked_fact')) for a in x['asked_fact_assessments']]})
        assert x['label'] in ['Correct','Partial','Incorrect']
        if x['material_wrong_claims']: assert x['label']=='Incorrect'
        totals[w][x['label']]+=1;facts[w]+=len(scope[i]['asked_facts']);assessments[w]+=len(x['asked_fact_assessments'])
    assert actual=={(w,i) for w in 'ab' for i in ids} and not actual.intersection(seen)
    seen.update(actual); reports.append({'path':str(rp),'sha256':H(rp),'pack':str(pp),'pack_sha256':H(pp),'ids':ids})
assert len(reports)==6 and seen=={(w,i) for w in 'ab' for i in questions}
assert all(facts[w]==sum(len(x['asked_facts']) for x in scope.values()) for w in 'ab')
counts={w:{label:totals[w][label] for label in ['Correct','Partial','Incorrect']} for w in 'ab'}
np=D/'grading/fresh-borderline-adjudication.json'; ip=D/'grading/fresh-borderline-input.json'
neutral=load(np); inp=load(ip); entries={(x['reader'],x['id']):x for x in inp['entries']}
assert set(entries)=={('a','Q16'),('a','Q73'),('a','Q87')}
for (w,i),entry in entries.items(): assert entry['complete_raw_entry']==raw[w][i]
effective={w:Counter(totals[w]) for w in 'ab'}
labels={(x['reader'],x['id']):x['label'] for task in plan['blocks'] for x in load(Path(task['output'])).get('grades',load(Path(task['output'])).get('records'))}
for x in neutral['records']:
    w,i=x['reader'],x['id'];assert (w,i) in entries and x['raw_entry_sha256']==canonical(raw[w][i])
    if x['material_wrong_claims']: assert x['label']=='Incorrect'
    effective[w][labels[w,i]]-=1;effective[w][x['label']]+=1
assert {(x['reader'],x['id']) for x in neutral['records']}==set(entries)
proof={'verified':True,'checked_at_utc':datetime.now(timezone.utc).isoformat(),'N':len(questions),'complete_original_entries':len(seen),'mapped_requirement_vector_assessments':facts,'actual_grader_split_clause_assessments':assessments,'compound_vectors_split_without_loss_manually_reviewed':split_vectors,'primary_fixed_v9_scores':counts,'one_neutral_effective_scores':{w:{k:effective[w][k] for k in ['Correct','Partial','Incorrect']} for w in 'ab'},'reports':reports,'raw_file_sha256':{w:H(p) for w,p in raw_paths.items()},'selected_same_reader_completed_output':selection,'initial_unfinished_artifact_preserved':True,'one_neutral':{'report':str(np),'sha256':H(np),'input':str(ip),'input_sha256':H(ip),'cases':list(map(list,entries))},'limits':['All93 old questions judged against original v9 asks; newQ94 not retroactively imposed.','One neutral Q87 correctly identifies unasked card-reference background; preserve old map and version genuine scope correction.','Only whole-entry grades accepted; no cross-answer borrowing or receipt/format cap.','Integrity verification separate from independent actual model/input checks; no full-core/source-gap/publication approval.']}
out=B/'coordinator-checks/new-angeles-expanded02-primary-and-one-neutral-integrity.json';assert not out.exists()
out.write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps({'verified':True,'entries':len(seen),'facts':facts,'primary':counts,'effective':proof['one_neutral_effective_scores'],'proof':str(out)}))
