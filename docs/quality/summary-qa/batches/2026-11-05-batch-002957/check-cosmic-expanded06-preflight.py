"""Bind the new staged process to unchanged original168 Q/key/scope/source bytes."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
B=Path(__file__).resolve().parent;R=B.parents[4]
G=R/'docs/quality/summary-qa/cosmic-encounter'/B.name;D=G/'expanded-iteration-06';O=G/'expanded-iteration-05'
J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=J(D/'input-manifest.json');checks=[]
for path,digest in m['sha256'].items():
    p=Path(path);assert H(p)==digest;checks.append({'path':path,'sha256':digest})
assert (D/'summary-snapshot.md').read_bytes()==(O/'summary-snapshot.md').read_bytes()==(R/'rules/cosmic-encounter.md').read_bytes()
assert H(D/'summary-snapshot.md')=='787b88677123fc93751d1605a99e4c724faadaa891f1b0c103bcb296075952b9'
q=J(D/'questions.json')['questions'];oldq=J(O/'questions.json')['questions']
k=J(D/'answer-key.json')['answers'];oldk=J(O/'answer-key.json')['answers']
s=J(D/'actual-question-scope.json')['questions'];olds=J(O/'actual-question-scope.json')['questions']
assert q==oldq and k==oldk and s==olds
ids=[x['id'] for x in q];assert len(ids)==len(set(ids))==m['question_count']==168 and ids==m['expected_ids']
assert sum(len(x['required_facts']) for x in k)==m['raw_key_fact_count']==547
assert m['required_semantic_unit_count']==696 and m['bank_version']=='expanded-candidate-16'
assert (D/'source-scope.json').read_bytes()==(O/'source-scope.json').read_bytes()==Path(m['source_scope_manifest']).read_bytes()
review=J(B/'coordinator-checks/cosmic-v7-v15-prospective-generic-staged-method-review.json')
template=Path(review['template_path']);code=Path(review['code_path'])
assert H(template)==review['template_sha256']=='fa796a701b1ec51db1c654e51b839bbbbb858ba8d6642a155937f8c34f1b1b6a'
assert H(code)==review['code_sha256']==H(D/'generic-method-code.py')==m['generic_code_sha256']=='1aa766ef0da8209f5cd0ee6268466407a7c1bf1681f14df193b96a3920aec133'
readerq=J(D/'reader-questions-final.json');assert readerq['questions']==q
process=readerq['reader_process'];instructions=process['instructions']
assert hashlib.sha256(instructions.encode()).hexdigest()==process['instructions_sha256']
assert process['method_code_sha256']==H(code)
renders=[]
for actual_code in [code.read_text(),code.read_text().rstrip('\n')]:
    rendered=template.read_text().replace('SUMMARY_PATH',str(D/'summary-snapshot.md')).replace('QUESTIONS_PATH',str(D/'reader-questions-final.json')).replace('METHOD_CODE_SHA256',H(code)).replace('METHOD_CODE',actual_code)
    if rendered==instructions:renders.append('full_final_LF' if actual_code.endswith('\n') else 'one_template_supplied_final_LF')
assert renders
normalized={}
for who in 'ab':
    raw=(D/f'reader-{who}-prompt.txt').read_text()
    for path in m['reader_work_paths'][who].values():raw=raw.replace(path,'OWN_WORK_PATH_'+('DRAFT' if path.endswith('-draft.json') else 'FINAL'))
    raw=raw.replace('"'+who+'"','"READER_LABEL"')
    normalized[who]=raw
assert normalized['a']==normalized['b']
assert m['stage_schedule']=={'draft_batch_size':10,'review_batch_size':20}
assert m['fixed_draft_batch_count']==17 and m['fixed_review_batch_count']==9 and m['grading_only_after_both_complete_review']
assert m['reader_protocol_version']==7 and not m['human_interpretation_adopted'] and not m['final_scope_freeze'] and not m['completion_readiness']
proof={'verified':True,'checked_at_utc':datetime.now(timezone.utc).isoformat(),'N':168,'raw_key_facts':547,'unchanged_semantic_units':696,'guide_sha256':H(D/'summary-snapshot.md'),'all13_manifest_hashes_verified':checks,'all_literal_Q_key_scope_records_exact05_and_candidate16':True,'clean_source_policy_exact_unchanged':True,'generic_template_sha256':H(template),'generic_code_sha256':H(code),'actual_shared_rendered_process_sha256':process['instructions_sha256'],'render_variant':renders,'native_dispatch_prompts_same_except_owned_work_paths_and_labels':True,'declared_schedule':{'readiness':'zero answers before authoring','draft':17,'review':9,'draft_records_per_turn':10,'review_records_per_turn':20},'limits':['New staged fresh168 trial; no factual feedback or new reader vote within its own predeclared stages. All closed drafts/final originals retained.','Actual model cohort, readiness delivery, full final336 originals/grades/one neutral if needed remain separate.','Source15 freeze17 and prior coverage proofs reused unchanged; essential FAQ authority gap still prevents unqualified core/stamp/publication approval.']}
out=B/'coordinator-checks/cosmic-expanded06-current168-v7-frozen-input-continuity.json';assert not out.exists();out.write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps({'verified':True,'N':168,'hashes':len(checks),'process_sha256':process['instructions_sha256'],'proof':str(out)}))
