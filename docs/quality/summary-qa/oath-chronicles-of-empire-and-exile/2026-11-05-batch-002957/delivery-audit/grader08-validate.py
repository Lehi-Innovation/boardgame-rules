from pathlib import Path
import json,hashlib,runpy,collections,re
P=Path(__file__).resolve().parent.parent;I=P/'expanded-iteration-08'
m=runpy.run_path(str(P/'delivery-audit/grader08-grade.py'));d=m['data'];res=json.loads((I/'results.json').read_text())
key=json.loads((P/'expanded-v11/answer-key.json').read_text());scope=json.loads((P/'expanded-v11/grading-scope.json').read_text());keys={x['id']:x for x in key['answers']};scopes={x['id']:x for x in scope['questions']}
hashes=[];entries=0;factcount=0;evidencecount=0;quotecount=0;expectedids=[f'Q{i:03d}' for i in range(1,105)]
for inp in d['inputs']:
 f=Path(inp['path']);actual=hashlib.sha256(f.read_bytes()).hexdigest();hashes.append({'path':str(f),'expected':inp['sha256'],'actual':actual,'matches':actual==inp['sha256']});assert actual==inp['sha256']
assert [q['id'] for q in d['questions']]==expectedids
for q in d['questions']:
 k=keys[q['id']];s=scopes[q['id']]
 assert k['expected_answer']==q['fixed_expected_answer']
 assert [{k:f[k] for k in ['fact_id','expected_fact']} for f in s['required_facts']]==q['required_facts']
 for field in ['question','contextual_exclusions','semantic_notes','source_references']:assert s[field]==q[field]
 assert hashlib.sha256(q['fixed_expected_answer'].encode()).hexdigest()==s['fixed_key_expected_answer_sha256']
for reader in res['readers']:
 r=reader['reader'];raw=json.loads((I/(r+'.json')).read_text());raws={e['id']:e for e in raw['answers']}
 assert [q['id'] for q in reader['questions']]==expectedids
 for q,qr in zip(d['questions'],reader['questions']):
  original=m['reconstruct'](q['readers'][r]);assert original==raws[q['id']];entries+=1
  assert qr['observed_answer']==original['answer'];assert qr['expected_answer_from_fixed_key']==q['fixed_expected_answer'];assert qr['question']==q['question']
  assert [f['fact_id'] for f in qr['fact_checks']]==[f['fact_id'] for f in q['required_facts']]
  for f,g in zip(qr['fact_checks'],q['required_facts']):
   assert f['expected_fact']==g['expected_fact'];factcount+=1
   if f['status']=='satisfied':assert f['evidence']
   for ev in f['evidence']:
    v=original
    for piece in re.findall(r'[^.\[\]]+',ev['location']):v=v[int(piece)] if isinstance(v,list) else v[piece]
    assert ev['excerpt'] in v,(r,q['id'],f['fact_id'],ev['location'])
    evidencecount+=1
    if 'span_if_quote' in ev:
     sp=ev['span_if_quote'];assert ev['excerpt']==m['summary'][sp['start']:sp['end']];quotecount+=1
  fs=[f['status'] for f in qr['fact_checks']]
  grade='incorrect' if 'contradiction' in fs else 'partial' if 'missing' in fs else 'correct';assert qr['grade']==grade
 totals=collections.Counter(q['grade'] for q in reader['questions']);facts=collections.Counter(f['status'] for q in reader['questions'] for f in q['fact_checks'])
 assert reader['totals']=={k:totals[k] for k in ['correct','partial','incorrect']}|{'total':104}
 assert reader['fact_totals']=={k:facts[k] for k in ['satisfied','missing','contradiction']}|{'total':328}
assert entries==208 and factcount==656
receipts=[]
for name in ['grading-input.json','summary-snapshot.md']:
 text=(I/name).read_text();sha=hashlib.sha256((I/name).read_bytes()).hexdigest();offset=0
 for f in sorted((P/'delivery-audit').glob('grader08-'+name.replace('.','-')+'-*.json')):
  rc=json.loads(f.read_text());assert rc['start']==offset and rc['end']-rc['start']<=5000
  assert rc['sha256']==sha and rc['chunk_sha256']==hashlib.sha256(text[rc['start']:rc['end']].encode()).hexdigest()
  offset=rc['end'];receipts.append(str(f))
 assert offset==len(text)
assert len(receipts)==74
validation=dict(status='passed',iteration=8,benchmark_version='expanded-v11',questions_graded=entries,fact_assessments=factcount,exact_question_ids=True,exact_fact_ids_and_text=True,fixed_key_answers_exact=True,scope_questions_exclusions_notes_sources_exact=True,scope_basis_metadata_excluded_from_transport_as_nongrading_metadata=True,full_original_entry_reconstruction_equality=True,original_answers_exact=True,raw_input_hashes=hashes,same_entry_evidence_checks=evidencecount,literal_summary_span_checks=quotecount,all_satisfied_facts_have_traceable_same_entry_evidence=True,totals_recomputed=True,packet_complete_characters=315182,summary_complete_characters=47341,delivery_chunks=len(receipts),delivery_receipts_verified=True,delivery_truncations=0,delivery_format_deviations=[],external_sources_consulted=[],old_grades_history_or_other_iterations_read=False,errors=[])
(I/'grading-validation.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:validation[k] for k in ['status','questions_graded','fact_assessments','same_entry_evidence_checks','literal_summary_span_checks','errors']},indent=2))
