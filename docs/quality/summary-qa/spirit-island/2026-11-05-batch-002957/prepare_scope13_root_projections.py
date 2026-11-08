"""Reversible parent-only encoding of repeated verdicts; never a grader input."""
from pathlib import Path
import collections
import copy
import hashlib
import json

B=Path(__file__).resolve().parent
load=lambda p:json.loads(p.read_text())
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
k=load(B/'question-key-scope-review-13.json')
c=load(B/'coverage-review-13.json')
case=load(B/'novelty-adjudication-18/proposals.json')
assert k['checked_questions']==c['checked_questions']
side={};rows=[]
for row in k['checked_questions']:
    assert row['fixed_key_verdict']==row['asked_fact_mapping_verdict']=='PASS'
    assert row['context_boundary_checked'] is True
    fs=row['fact_checks'];assert len(fs)==row['required_fact_count']
    grouped=collections.OrderedDict()
    for fact in fs:
        grouped.setdefault(fact['clause_id'],[]).append(fact)
        assert fact['literal_ask_fit']==fact['primary_source_correctness']==fact['fixed_key_semantic_support']=='PASS'
    clauses=[]
    for clause,facts in grouped.items():
        assert [x['fact_index'] for x in facts]==list(range(len(facts)))
        clauses.append([clause,len(facts)])
    rows.append([row['id'],row['scope_result_independently_validated'],clauses])
    side[row['id']]={'literal_question_sha256':row['literal_question_sha256'],'fixed_answer_sha256':row['fixed_answer_sha256'],'fact_sha256':[x['fact_sha256'] for x in fs]}
core=copy.deepcopy(k)
core['checked_questions']={'$lossless_uniform_verdict_codec':{
    'question_template':{'fixed_key_verdict':'PASS','asked_fact_mapping_verdict':'PASS','context_boundary_checked':True},
    'fact_template':{'literal_ask_fit':'PASS','primary_source_correctness':'PASS','fixed_key_semantic_support':'PASS'},
    'expansion':'For each [id,scope,clauses] row, expand every [clause_id,count] with fact indices0..count-1 and all three PASS values. Count is the sum of clause counts. Restore exact source hashes from the technical sidecar. All172 question judgments and all504 fact-verdict instances reconstruct exactly in both raw reports.',
    'rows':rows}}
for key in ['input_hashes','read_evidence']:
    side[key]=core[key];core[key]={'$technical_sidecar':key}
extras={key:value for key,value in c.items() if key not in k or k[key]!=value}
for key in ['remaining_gaps','coverage_map_classification_findings','independent_complete_challenge','stopping_assessment']:
    assert extras[key]==case['proposed_set'][key]
    extras[key]={'$previously_read_complete_proposals_field':key}
projection={'key_and_scope_report':core,'coverage_report_derivation':{'all_other_fields_exactly_equal_key_report':True,'different_or_additional_fields':extras},'complete_proposals_file_sha256':H(B/'novelty-adjudication-18/proposals.json')}
restored=copy.deepcopy(core);restored_rows=[]
for ident,scope,clauses in rows:
    data=side[ident];facts=[];hashes=iter(data['fact_sha256'])
    for clause,count in clauses:
        for i in range(count):
            facts.append({'clause_id':clause,'fact_index':i,'fact_sha256':next(hashes),'literal_ask_fit':'PASS','primary_source_correctness':'PASS','fixed_key_semantic_support':'PASS'})
    restored_rows.append({'id':ident,'literal_question_sha256':data['literal_question_sha256'],'fixed_answer_sha256':data['fixed_answer_sha256'],'required_fact_count':len(facts),'fixed_key_verdict':'PASS','asked_fact_mapping_verdict':'PASS','fact_checks':facts,'context_boundary_checked':True,'scope_result_independently_validated':scope})
restored['checked_questions']=restored_rows
for key in ['input_hashes','read_evidence']:restored[key]=side[key]
assert restored==k
restored_c=copy.deepcopy(restored)
for key,value in extras.items():
    restored_c[key]=case['proposed_set'][key] if isinstance(value,dict) and '$previously_read_complete_proposals_field' in value else value
assert restored_c==c
for name,value in [('scope13-parent-lossless-joint-semantic.json',projection),('scope13-parent-lossless-technical-sidecar.json',side)]:
    p=B/name;assert not p.exists()
    p.write_text(json.dumps(value,ensure_ascii=False,separators=(',',':'))+'\n')
    print(json.dumps({'path':str(p),'characters':len(p.read_text()),'sha256':H(p)}))
print('Both full raw reports reconstruct exactly; originals unchanged.')
