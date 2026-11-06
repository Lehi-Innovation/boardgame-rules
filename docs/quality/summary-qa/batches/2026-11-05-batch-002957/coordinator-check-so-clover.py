from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json,hashlib,tempfile,sys
base=Path(__file__).parent;root=base.parents[4];sys.path.insert(0,str(root));r=root/'docs/quality/summary-qa/so-clover'/base.name;it=r/'stamped-iteration-03'
from scripts.validate import validate_rules_file
from scripts.stamp_verification import stamp_file,load_audit_results
j=lambda p:json.loads(p.read_text());h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
q=j(it/'questions.json');k=j(it/'answer-key.json');oq=j(r/'benchmark-v1/questions.json');ok=j(r/'benchmark-v1/answer-key.json');assert q['questions']==oq['questions'];assert k['answers']==ok['answers'];ids=[x['id'] for x in q['questions']];assert len(ids)==len(set(ids))==20
qs={x['id']:x for x in q['questions']};ks={x['id']:x for x in k['answers']};assert set(ks)==set(ids)
for path,value in j(it/'input-manifest.json')['inputs'].items():assert h(Path(path))==value,(path,value,h(Path(path)))
results=j(it/'results.json');scores={}
for reader in ['reader-a','reader-b']:
 raw=j(it/(reader+'.json'));answers={x['id']:x for x in raw['answers']};assert len(raw['answers'])==len(answers)==20 and set(answers)==set(ids)
 group=results['reader_results'][reader];grades=group['grades'];assert len(grades)==20 and set(x['id'] for x in grades)==set(ids)
 for grade in grades:
  ident=grade['id'];assert grade['grade']=='correct';assert not grade['unsupported_guess'];assert not grade['missing_or_wrong'];assert grade['observed_answer']==answers[ident]['answer'];assert grade['question']==qs[ident]['question'];assert grade['expected_answer']==ks[ident]['expected_answer'];assert grade['required_facts']==ks[ident]['required_facts']
 assert group['totals']=={'correct':20,'partial':0,'incorrect':0,'unresolved':0,'unsupported_guesses':0};scores[reader]=group['totals']
models=j(it/'model-provenance.json');assert len(models)==2 and len({x['session_id'] for x in models})==2
for item in models:
 assert item['verified'] and item['fork_turns']=='none';assert item['turn_context_records'] and all(x['model']=='gpt-6-luna' and x['effort']=='high' for x in item['turn_context_records'])
post_models=j(r/'post-stamp-model-provenance.json');auditors=[x for x in post_models if 'stamped03' in x['task'] and 'reader' not in x['task']];assert len(auditors)==1,auditors
assert auditors[0]['verified'] and all(x['model']=='gpt-6.1-sol' and x['effort']=='high' for x in auditors[0]['turn_context_records'])
source_audit=j(it/'source-audit.json');canonical=root/'rules/so-clover.md';assert source_audit['verdict']=='PASS' and source_audit['findings']==[];assert source_audit['summary_sha256']==h(canonical)==h(it/'summary-snapshot.md');assert canonical.read_bytes()==(it/'summary-snapshot.md').read_bytes()
for entry in source_audit['inputs_read']:assert h(Path(entry['path']))==entry['sha256']
coverage=j(r/'coverage-ledger.json');assert coverage['coverage_stopping_rule_met'] and coverage['core_procedural_coverage_complete'];assert coverage['consecutive_zero_addition_passes']>=2;assert (r/'coverage-review.json').is_file();assert not validate_rules_file(str(canonical))
with tempfile.TemporaryDirectory(prefix='so-clover-stamp-check-') as tmp:
 p=Path(tmp)/'so-clover.md';p.write_bytes(canonical.read_bytes());stamp_file(str(p),load_audit_results(),stamp_date='2026-11-05');assert p.read_bytes()==canonical.read_bytes()
report={'game':'So Clover!','checked_at':datetime.now(ZoneInfo('America/Phoenix')).isoformat(),'approved':True,'source_audit_verdict':'PASS','source_audit_path':str(it/'source-audit.json'),'summary_sha256':h(canonical),'question_count':20,'final_reader_scores':scores,'reader_session_ids':[x['session_id'] for x in models],'source_auditor_session_id':auditors[0]['session_id'],'original_questions_and_keys_unchanged':True,'all_frozen_and_source_audit_hashes_match':True,'all_ids_once_and_saved_grade_correspondence_verified':True,'actual_models_and_efforts_verified':True,'coverage_stopping_rule_and_independent_challenge_inspected':True,'canonical_equals_final_snapshot':True,'structural_validation_passed':True,'stamp_idempotent':True,'phase':'complete'}
out=base/'coordinator-checks';out.mkdir(exist_ok=True);(out/'so-clover.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));p=base/'coordinator-approvals.json';a=j(p);a['so-clover']=report;p.write_text(json.dumps(a,indent=2)+'\n')
