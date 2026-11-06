from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;PROV=json.loads((P/'model-provenance.json').read_text())['agents']
def strings(x):
 if isinstance(x,str):
  yield x
  try:
   y=json.loads(x)
   if y!=x:yield from strings(y)
  except (ValueError,RecursionError):pass
 elif isinstance(x,list):
  for y in x:yield from strings(y)
 elif isinstance(x,dict):
  if x.get('type') in ['image','input_image','image_url']:return
  for k,y in x.items():
   if k not in ['data','image_url','encrypted_content']:yield from strings(y)
def outputs(task):
 agent=next(x for x in PROV if x['task']=='/root/'+task);records=[]
 for ordinal,line in enumerate(Path(agent['runtime_source_path']).open()):
  d=json.loads(line);v=d.get('payload',{})
  if d.get('type')=='response_item' and v.get('type')=='custom_tool_call_output':records.append((ordinal,'\n'.join(strings(v.get('output')))))
 return agent,records
jobs=[]
# Auditor uses named source IDs with a separate path/hash inventory.
f=P/'source-audit-01/source-audit.json';d=json.loads(f.read_text());index={r['id']:r for r in d['input_hashes']};receipts=[]
for x in d['delivery_receipt']['text_read_receipts']:
 source=index[x['source']];receipts.append({'path':source['path'],'sha256':source['sha256'],'length':x['character_length'],'ranges':x['contiguous_ranges']})
jobs.append(('final_source_audit_01',f,receipts))
for task,name in [('seed3_grader','seed-iteration-03/results.json'),('seed4_grader','seed-iteration-04/results.json')]:
 f=P/name;d=json.loads(f.read_text());r=d['delivery_receipt'];items=[dict(v,path=k) for k,v in r.items()] if isinstance(r,dict) else r
 jobs.append((task,f,[{'path':x['path'],'sha256':x['sha256'],'length':x['char_length'],'ranges':x['all_actually_read_ranges']} for x in items]))
f=P/'coverage-scope-v5-review.json';d=json.loads(f.read_text());jobs.append(('final_coverage_scope_v5',f,[{'path':x['path'],'sha256':x['sha256'],'length':x['characters'],'ranges':x['delivered_bounds']} for x in d['input_text_delivery_receipts']]))
f=P/'coverage-scope-v6-challenge.json';d=json.loads(f.read_text());jobs.append(('coverage_scope_v6_challenge',f,[{'path':x['path'],'sha256':x['sha256'],'length':x['characters_unicode'],'ranges':[[r['start_inclusive'],r['end_exclusive']] for r in x['ranges']]} for x in d['delivery_receipts']['text_sources']]))
f=P/'coverage-scope-v7-confirmation.json'
if f.exists():
 d=json.loads(f.read_text());jobs.append(('coverage_scope_v6_challenge',f,[{'path':x['path'],'sha256':x['sha256'],'length':x['characters_unicode'],'ranges':[[r['start_inclusive'],r['end_exclusive']] for r in x['ranges']]} for x in d['delivery_receipts']['complete_new_texts']]))
f=P/'source-audit-02/source-audit.json';d=json.loads(f.read_text());index={r['path']:r for r in d['input_hashes']}
jobs.append(('current_source_audit_02',f,[{'path':x['path'],'sha256':(index[x['path']]['sha256'] if x['path'] in index else x['slices'][0]['slice_utf8_sha256']),'length':x['characters'],'ranges':[[r['start'],r['end']] for r in x['slices']]} for x in d['full_delivery_receipts']]))
f=P/'current-v8-review/coverage-key-scope.json';d=json.loads(f.read_text())
jobs.append(('current_v8_scope_coverage',f,[{'path':x['path'],'sha256':x['sha256'],'length':x['chars'],'ranges':[[r['start_inclusive'],r['end_exclusive']] for r in x['slices']]} for x in d['delivery_receipts']['text'] if x['slices']]))
f=P/'current-v9-final-review/coverage-key-scope.json';d=json.loads(f.read_text())
jobs.append(('current_v9_final_challenge',f,[{'path':x['path'],'sha256':x['sha256'],'length':x['characters'],'ranges':x['bounds']} for x in d['text_receipts'] if 'bounds' in x]))
f=P/'source-research/iello-2025-official-erratum/independent-source-review.json';d=json.loads(f.read_text())
# This narrow source reviewer read both complete publisher texts. Other core
# excerpts were explicitly selected context and are not claimed as full delivery.
publisher_receipts=[]
for x in d['complete_delivery_receipts']['bounded_full_normative_and_visible_text_reads']:
 if x['mode']!='complete text delivered to model':continue
 source=Path(x['path'])
 publisher_receipts.append({'path':x['path'],'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'length':x['source_characters'],'ranges':[[x['character_range_start_inclusive'],x['character_range_end_exclusive']]]})
jobs.append(('iello_2025_erratum_review',f,publisher_receipts))
f=P/'expanded-iteration-01/adjudication/whole-answer-assessment.json'
if f.exists():
 d=json.loads(f.read_text());jobs.append(('expanded01_whole_answer_adjudicator',f,[{'path':x['path'],'sha256':x['sha256'],'length':x['unicode_char_length'],'ranges':[[r['start'],r['end']] for r in x['read_ranges']]} for x in d['read_receipts']]))
f=P/'source-audit-03/source-audit.json'
if f.exists():
 d=json.loads(f.read_text());audit3_receipts=[]
 for x in d['full_delivery_receipts']:
  if not x.get('slices'):continue
  if x.get('parsed_visible_path'):
   assert hashlib.sha256(Path(x['path']).read_bytes()).hexdigest()==x['sha256']
   assert Path(x['parsed_visible_path']).read_text()==(P/'source-research/iello-2025-official-erratum/publisher-full-visible-text-v2.txt').read_text().strip()
   audit3_receipts.append({'path':x['parsed_visible_path'],'sha256':x['parsed_visible_sha256'],'length':x['parsed_visible_characters'],'ranges':[[r['start'],r['end']] for r in x['slices']]})
  else:audit3_receipts.append({'path':x['path'],'sha256':x['sha256'],'length':x['characters'],'ranges':[[r['start'],r['end']] for r in x['slices']]})
 jobs.append(('current_source_audit_03',f,audit3_receipts))
f=P/'source-audit-05/source-audit.json'
if f.exists():
 d=json.loads(f.read_text());html=d['html_receipt']
 assert hashlib.sha256(Path(html['raw_path']).read_bytes()).hexdigest()==html['raw_sha256']
 assert hashlib.sha256(Path(html['parsed_visible_path']).read_bytes()).hexdigest()==html['parsed_visible_sha256']
 assert Path(html['parsed_visible_path']).read_text()==(P/'source-research/iello-2025-official-erratum/publisher-full-visible-text-v2.txt').read_text()
 jobs.append(('current_source_audit_05',f,[{'path':x['path'],'sha256':x['sha256'],'length':x['characters'],'ranges':[[r['start'],r['end']] for r in x['slices']]} for x in d['full_delivery_receipts']]))
f=P/'source-audit-06/source-audit.json'
if f.exists():
 d=json.loads(f.read_text());html=d['html_receipt']
 assert hashlib.sha256(Path(html['raw_html_path']).read_bytes()).hexdigest()==html['raw_html_sha256']
 assert hashlib.sha256(Path(html['parsed_path']).read_bytes()).hexdigest()==html['parsed_sha256']
 assert Path(html['parsed_path']).read_text().strip()==(P/'source-research/iello-2025-official-erratum/publisher-full-visible-text-v2.txt').read_text().strip()
 jobs.append(('current_source_audit_06',f,[{'path':x['path'],'sha256':x['sha256'],'length':x['characters'],'ranges':[r if isinstance(r,list) else [r['start'],r['end']] for r in x['slices']]} for x in d['full_delivery_receipts']]))
f=P/'source-audit-07/source-audit.json'
if f.exists():
 d=json.loads(f.read_text());html=d['html_receipt']
 assert hashlib.sha256(Path(html['raw_path']).read_bytes()).hexdigest()==html['raw_sha256']
 for derived,capture,key in [('independent-visible.txt','publisher-full-visible-text-v2.txt','visible_sha256'),('independent-body.txt','publisher-article-body-v2.txt','body_sha256')]:
  path=f.parent/derived;assert hashlib.sha256(path.read_bytes()).hexdigest()==html[key]
  assert path.read_text().strip()==(P/'source-research/iello-2025-official-erratum'/capture).read_text().strip()
 jobs.append(('current_source_audit_07',f,[{'path':x['path'],'sha256':x['sha256'],'length':x['characters'],'ranges':[[r['start'],r['end']] for r in x['slices']]} for x in d['full_delivery_receipts']]))
f=P/'expanded-iteration-09/adjudication/q01-a-assessment.json'
if f.exists():
 d=json.loads(f.read_text());jobs.append(('expanded09_whole_answer_adjudicator',f,[{'path':x['path'],'sha256':x['sha256'],'length':x['characters'],'ranges':[[r['start'],r['end']] for r in x['slices']]} for x in d['delivery_receipts']]))
f=P/'expanded-iteration-11/adjudication/q63-b-assessment.json'
if f.exists():
 d=json.loads(f.read_text());jobs.append(('expanded11_whole_entry_adjudicator',f,[{'path':x['path'],'sha256':x['sha256'],'length':x['character_length'],'ranges':x['read_ranges']} for x in d['delivery_receipts']]))
result=[]
for task,report,receipts in jobs:
 agent,records=outputs(task);verified=[]
 for r in receipts:
  f=Path(r['path']);text=f.read_text();assert len(text)==r['length'];assert hashlib.sha256(f.read_bytes()).hexdigest()==r['sha256'];end0=0;chunks=[]
  for start,end in r['ranges']:
   assert start==end0 and 0<end-start<=5000;end0=end
   matches=[o for o,t in records if text[start:end] in t];assert matches,(task,r['path'],start,end)
   chunks.append({'start':start,'end':end,'runtime_output_record_ordinals':matches,'exact_expected_text_found':True})
  assert end0==len(text),(task,r['path'],end0,len(text));verified.append({'path':r['path'],'sha256':r['sha256'],'characters':len(text),'complete_contiguous':True,'slices':chunks})
 result.append({'task':agent['task'],'report':str(report.resolve()),'actual_model_confirmed':agent['confirmed'],'runtime_source_path':agent['runtime_source_path'],'verified_text_inputs':verified})
(P/'actual-reviewer-input-delivery-validation.json').write_text(json.dumps({'method':'Every exact declared text slice independently located in original model-visible runtime tool outputs after decoding JSON wrappers; no internal metadata copied. Native image views are evidenced separately by source reports/image receipts and runtime hashes.','reviewers':result},indent=2)+'\n')
print('Independently verified complete actual delivery:',[(x['task'],len(x['verified_text_inputs'])) for x in result])
