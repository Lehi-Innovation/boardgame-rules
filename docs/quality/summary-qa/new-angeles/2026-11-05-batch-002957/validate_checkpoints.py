from pathlib import Path
import json,hashlib,collections,importlib.util,sys
sys.dont_write_bytecode=True
B=Path(__file__).parent
canon=lambda x:json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
report={'status':'in_progress_checkpoint_not_completion','banks':{},'iterations':{},'errors':[]}
base={}
for name in ['seed-v1','seed-v2','seed-v3']:
 q=json.loads((B/name/'questions.json').read_text())['questions'];k=json.loads((B/name/'answer-key.json').read_text())['answers'];freeze=json.loads((B/name/'freeze.json').read_text())
 assert all(h(B/name/n)==sha for n,sha in freeze['hashes'].items());assert len(q)==20==len(k)
 assert len({x['id'] for x in q})==20 and {x['id'] for x in q}=={x['id'] for x in k}
 base[name]=(q,k);report['banks'][name]={'count':20,'freeze_hashes_intact':True,'question_record_hashes':{x['id']:hashlib.sha256(canon(x)).hexdigest() for x in q},'key_record_hashes':{x['id']:hashlib.sha256(canon(x)).hexdigest() for x in k}}
assert base['seed-v1'][0]==base['seed-v2'][0]==base['seed-v3'][0]
for old,new,changed in [('seed-v1','seed-v2','Q20'),('seed-v2','seed-v3','Q17')]:
 diff=[a['id'] for a,b in zip(base[old][1],base[new][1]) if a!=b];assert diff==[changed];report['banks'][new]['only_declared_key_change']=diff
for name,seed in [('expanded-candidate-v1','seed-v2'),('expanded-candidate-v2','seed-v3'),('expanded-candidate-v3','seed-v3')]:
 q=json.loads((B/name/'questions.json').read_text())['questions'];k=json.loads((B/name/'answer-key.json').read_text())['answers'];assert q[:20]==base[seed][0] and k[:20]==base[seed][1];assert len(q)==len(k)==len({x['id'] for x in q});report['banks'][name]={'count':len(q),'seed_entries_preserved':True,'seed_version':seed,'reference_only_ids':[] if name.endswith('v1') else ['Q68','Q73','Q76']}
q2=json.loads((B/'expanded-candidate-v2/questions.json').read_text())['questions'];k2=json.loads((B/'expanded-candidate-v2/answer-key.json').read_text())['answers'];q3=json.loads((B/'expanded-candidate-v3/questions.json').read_text())['questions'];k3=json.loads((B/'expanded-candidate-v3/answer-key.json').read_text())['answers'];assert q3[:89]==q2 and k3[:89]==k2
helper=Path('docs/quality/summary-qa/batches/2026-11-05-batch-002957/generic-reader-method/v10/source_units.py');spec=importlib.util.spec_from_file_location('qa_generic',helper);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
for n,seed in [(1,'seed-v1'),(2,'seed-v2'),(3,'seed-v2'),(4,'seed-v3')]:
 I=B/f'seed-luna-iteration-{n:02d}';q=json.loads((I/'questions.json').read_text());ids=[x['id'] for x in q['questions']];assert q['questions']==base[seed][0];assert h(I/'summary-snapshot.md')==json.loads((I/'input-manifest.json').read_text())['hashes']['summary-snapshot.md'];s=(I/'summary-snapshot.md').read_text();entry_report={};grade_records=[]
 for block in [1,2]:
  g=json.loads((I/f'grading/grades-{block}.json').read_text());grade_records+=g.get('entries',g.get('grades',[]))
 for letter in ['a','b']:
  r=json.loads((I/f'reader-{letter}.json').read_text());a=r['answers'];assert collections.Counter(x['id'] for x in a)==collections.Counter(ids)
  grades=[x for x in grade_records if x['reader']=='reader_'+letter];assert collections.Counter(x.get('id',x.get('question_id')) for x in grades)==collections.Counter(ids)
  rawmap={x['id']:x for x in a};raw_links=[]
  for x in grades:
   ident=x.get('id',x.get('question_id'));raw=rawmap[ident];stored=x.get('raw_entry',x.get('raw_response',x.get('raw_answer')))
   if isinstance(stored,dict):assert stored==raw;mode='complete entry equality'
   elif isinstance(stored,str):assert stored==raw['answer'];mode='answer equality; complete raw file retained'
   else:
    assert x.get('answer')==raw['answer'];assert x.get('raw_evidence')==raw['evidence'];mode='answer/evidence equality; complete raw file retained'
   raw_links.append({'id':ident,'raw_record_sha256':hashlib.sha256(canon(raw)).hexdigest(),'grade_record_sha256':hashlib.sha256(canon(x)).hexdigest(),'link_verification':mode})
  unit_checks=0
  if n>=3:
   for answer in a:
    for unit in answer['evidence']:mod.validate_record(s,unit);unit_checks+=1
  entry_report[letter]={'all_expected_ids_exactly_once':True,'all_expected_grades_exactly_once':True,'raw_output_sha256':h(I/f'reader-{letter}.json'),'raw_grade_links':raw_links,'generic_units_validated':unit_checks}
 delivery=json.loads((I/'actual-delivery-verification.json').read_text());assert all(v['all_input_data_verified_complete'] for v in delivery.values());assert len(delivery)==2
 report['iterations'][I.name]={'benchmark':seed,'count':20,'readers':entry_report,'actual_complete_input_delivery':True,'requested_actual_models_efforts_verified':all(v['model_provenance']['model_effort_verified'] for v in delivery.values())}
# The original source packet is readonly; check every byte fingerprint.
source=json.loads((B/'input-manifest.json').read_text())['sources'];assert all(h(p)==v['sha256'] for p,v in source.items());report['authoritative_sources_unchanged']=True
report['canonical_snapshot_status']={'canonical_sha256':h('rules/new-angeles.md'),'last_seed_snapshot_sha256':h(B/'seed-luna-iteration-04/summary-snapshot.md'),'changed_for_expanded_coverage':True,'final_exact_match_not_yet_claimed':True}
report['outstanding']=['NEW independent92-question coverage/key/scope challenge','SG01 coordinator/human scope decision pending','Final expanded bank/key freeze','Two NEW full-bank Luna readers and strict complete grading','NEW independent source-only audit on exact final bytes','Coordinator stamping and requested post-stamp exact-byte checks']
(B/'checkpoint-validation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');print('Validated4historicalpairs:160rawanswers and160primarygrades linked; all input/hash/model checks; all seed03/04generic units exact. Not completion.')
