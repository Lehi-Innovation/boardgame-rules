#!/usr/bin/env python3
"""Re-runnable read-only verification of completed review12/v22 objects; no semantic inference."""
from pathlib import Path
import json,hashlib,collections
from bs4 import BeautifulSoup
from PIL import Image
BASE=Path(__file__).parent
B=Path('/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/spirit-island/2026-11-05-batch-002957')
H=lambda b:hashlib.sha256(b).hexdigest()
def J(p):return json.loads(Path(p).read_bytes())
def canon(o):return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
checks=[]
def check(name,test):
 assert test,name
 checks.append(name)
expected={'scope-coverage-12-completed-read-ledger.json':'2a8cd4cf24fc18ee5dcc6117e2b19728a992985c0b0809ec7e49d8e3701644da','question-key-scope-review-12-completed.json':'4c03859b6fd06efe2e537468acf7d250a9ca6f4ff9daba5294296a2a74306408','coverage-review-12-completed.json':'87bc6ece03ff137860236244a3742ce1cfb7d96cb0fa51350f31f9872e29bd33'}
for n,h in expected.items():check('frozen output '+n,H((B/n).read_bytes())==h)
L=J(B/'scope-coverage-12-completed-read-ledger.json');R=J(B/'question-key-scope-review-12-completed.json');C=J(B/'coverage-review-12-completed.json')
old=J(L['original_ledger']['path']);check('original ledger exact binding',H(Path(L['original_ledger']['path']).read_bytes())==L['original_ledger']['sha256']=='0912aa42e2ad7f3550d430dc760ff1016b156d61b056a6f365439022a44f4928')
for stage in L['chronology']:
 for p,h in stage.get('frozen_artifacts',{}).items():check('original immutable '+p,H(Path(p).read_bytes())==h)
manifest=J(B/'scope12-currentmap-input-manifest.json')
for p,v in manifest['inputs'].items():check('manifest current '+p,H(Path(p).read_bytes())==v['sha256']and len(Path(p).read_bytes().decode())==v['characters'])
def slices_valid(v):
 raw=Path(v['path']).read_bytes();t=raw.decode();check('full text '+v['path'],H(raw)==v['full_byte_sha256']and len(raw)==v['byte_length']and len(t)==v['character_length']);pos=0
 for i,z in enumerate(v['slices']):
  check('slice '+v['path']+'#'+str(i),z['start']==pos and 0<z['end']-pos<=z['character_cap']<=6000 and z['max_output_tokens']>=4000 and z['truncated']is False and z['received']is True and H(t[pos:z['end']].encode())==z['utf8_sha256']);pos=z['end']
 check('continuous end '+v['path'],pos==len(t))
for p,v in L['new_text_inputs'].items():check('path field '+p,p==v['path']);slices_valid(v)
check('5new complete files91ranges',len(L['new_text_inputs'])==5 and sum(len(v['slices'])for v in L['new_text_inputs'].values())==91)
for v in L['reused_primary_text_inputs']:
 prior=old['text_inputs'][v['path']];check('exact original full binding '+v['path'],{k:v[k]for k in prior}==prior and v['new_delivery']is False);slices_valid(v)
check('12reused source text files72prior ranges',len(L['reused_primary_text_inputs'])==12 and sum(len(v['slices'])for v in L['reused_primary_text_inputs'])==72)
oldimages={v['path']:v for v in old['images']}
for v in L['reused_images']:
 check('exact original image binding '+v['path'],{k:v[k]for k in oldimages[v['path']]}==oldimages[v['path']]and v['new_visual_delivery']is False and H(Path(v['path']).read_bytes())==v['sha256'])
 with Image.open(v['path'])as im:im.verify()
check('54unique reused images',len(L['reused_images'])==len({v['path']for v in L['reused_images']})==54)
for v in L['new_visual_reopens']:check('new whole native image reopen '+v['path'],H(Path(v['path']).read_bytes())==v['sha256']and v['new_visual_delivery']and v['fully_viewed']and v['view_detail']=='original')
check('3new native face reopens',len(L['new_visual_reopens'])==3)
for v in L['new_source_reopens']:
 raw=Path(v['path']).read_bytes();t=raw.decode();a,b=v['character_range'];check('new precise source range '+str([a,b]),H(raw)==v['full_byte_sha256']and len(t)==v['character_length']and 0<=a<b<=len(t)and b-a<=6000 and v['max_output_tokens']>=4000 and not v['truncated']and v['received']and H(t[a:b].encode())==v['slice_utf8_sha256'])
for d in L['reused_membership_derivations']:
 raw=Path(d['source_path']).read_bytes();soup=BeautifulSoup(raw.decode(),'html.parser')
 for n in soup(['script','style','noscript']):n.decompose()
 out=soup.get_text('\n',strip=True).encode();check('publisher membership prose exact reproduction',H(raw)==d['original_html_sha256']and out==Path(d['output_path']).read_bytes()and H(out)==d['output_sha256'])
E=B/'expanded-v22';Q=J(E/'questions.json')['questions'];K=J(E/'answer-key.json')['answers'];M=J(E/'asked-fact-map.json')['questions'];S=J(E/'core-scope-credit.json')['questions'];ids=[f'Q{i:02}'for i in range(1,173)]
for name,rows in [('Q',Q),('K',K),('M',M),('S',S),('Rquestion',R['question_checks']),('Rscope',R['scope_validation']),('Cquestion',C['question_checks']),('Cscope',C['scope_validation'])]:check('172orderedIDs '+name,[x['id']for x in rows]==ids)
for name,comp in L['original_current_object_comparisons'].items():
 a=J(comp['old_path']);b=J(comp['current_path']);field='answers'if name=='answer-key.json'else'questions';check('comparison complete hashes '+name,H(Path(comp['old_path']).read_bytes())==comp['old_full_byte_sha256']and H(Path(comp['current_path']).read_bytes())==comp['current_full_byte_sha256'])
 for row,x,y in zip(comp['rows'],a[field],b[field]):check('comparison exact row '+name+row['id'],row['old_object_sha256']==H(canon(x))and row['current_object_sha256']==H(canon(y))and row['exact_object_equal']==(x==y))
flat=[]
for qi,x in enumerate(M):
 for ci,c in enumerate(x['requested_clauses']):
  for fi,f in enumerate(c['required_facts']):flat.append((x['id'],c['clause_id'],f,f'/questions/{qi}/requested_clauses/{ci}/required_facts/{fi}'))
check('507facts and no deletion',len(flat)==len(R['required_fact_checks'])==len(C['required_fact_checks'])==507)
for i,(qid,cid,f,ptr)in enumerate(flat):
 row=R['required_fact_checks'][i];check('exact fact_index '+str(i),row['fact_index']==i and row['question_id']==qid and row['clause_id']==cid and row['required_fact']==f and row['json_pointer']==ptr and row['required_fact_utf8_sha256']==H(f.encode()))
for qi,(q,k,m,s)in enumerate(zip(Q,K,M,S)):
 check('independent row input binding '+q['id'],R['question_checks'][qi]['literal_question_sha256']==H(q['question'].encode())and R['question_checks'][qi]['fixed_answer_sha256']==H(k['answer'].encode())and R['question_checks'][qi]['map_row_sha256']==H(canon(m))and R['scope_validation'][qi]['current_scope_row_sha256']==H(canon(s))and R['scope_validation'][qi]['zero_base_novelty_subclauses_preserved']==s.get('noncredited_clauses',[]))
for report in[R,C]:
 check('current benchmark and ledger linkage',report['benchmark']=='expanded-v22'and report['read_evidence']=={'ledger_path':str(B/'scope-coverage-12-completed-read-ledger.json'),'sha256':expected['scope-coverage-12-completed-read-ledger.json'],'complete':True})
 for p,h in report['input_hashes'].items():check('report exact input '+p,H(Path(p).read_bytes())==h)
 for key in['fixed_key_findings','asked_fact_mapping_findings','missing_truly_asked_facts_in_map','missing_truly_asked_facts_in_fixed_key','scope_findings']:check('recorded zero findings '+key,report[key]==[])
 check('recorded current PASS outcomes',report['verdict']==report['fixed_key_verdict']==report['asked_fact_mapping_verdict']==report['scope_verdict']=='PASS')
check('shared report fields exact',all(R[k]==C[k]for k in set(R)&set(C)))
check('coverage stopping record0gaps',C['coverage_verdict']==C['stopping_verdict']=='PASS'and C['remaining_gap_count']==0 and C['remaining_gaps']==[])
check('33cards16panels bindings',len(C['complete_corpus_challenge']['card_face_challenge'])==33 and len(C['complete_corpus_challenge']['native_original_panel_challenge'])==16)
check('31core2excluded card identities',collections.Counter(x['membership']for x in C['complete_corpus_challenge']['card_face_challenge'])=={'original_core':31,'excluded_Branch_and_Claw':2})
check('explicit Q09Q65Q117Q118 check records',[x['question_id']for x in R['explicit_affected_and_related_checks']]==['Q09','Q65','Q117','Q118'])
result={'validator_path':str(Path(__file__).resolve()),'validator_sha256':H(Path(__file__).read_bytes()),'all_machine_checks_passed':True,'check_count':len(checks),'checks':checks,'frozen_outputs':expected,'limitations':'This verifies exact filesystem objects, hashes, binding, scope-preservation and recorded outcomes. It does not independently prove historical delivery/perception or semantic correctness; those are the original reviewer attestations and independent source judgments documented separately. No peer/summary/reader/publication inputs inspected.'}
print(json.dumps(result,ensure_ascii=False,indent=2))
