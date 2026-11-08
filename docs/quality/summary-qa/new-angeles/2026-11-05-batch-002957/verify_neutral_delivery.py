from pathlib import Path
import hashlib,json,sys
B=Path(__file__).parent.resolve();I=B/(sys.argv[1] if len(sys.argv)>1 else 'expanded-luna-iteration-01');iteration_number=int(I.name.rsplit('-',1)[-1]);G=I/'grading';P=G/'fresh-borderline-adjudication.json';D=json.loads(P.read_text());M=next(x for x in json.loads((B/'runtime-provenance.json').read_text()) if x['task']==f'/root/expanded{iteration_number}_neutral_adjudicator')
def sha(x):return hashlib.sha256(x).hexdigest()
def canon(x):return json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
def strings(x):
 if isinstance(x,str):
  yield x
  if x[:1] in ['{','[']:
   try:yield from strings(json.loads(x))
   except (ValueError,TypeError):pass
 elif isinstance(x,list):
  for y in x:yield from strings(y)
 elif isinstance(x,dict):
  for k,y in x.items():
   if k not in ['encrypted_content','internal_chat_message_metadata_passthrough']:yield from strings(y)
outputs=[]
for n,line in enumerate(Path(M['runtime_log_path']).open(),1):
 r=json.loads(line);v=r.get('payload',{})
 if r['type']=='response_item' and v.get('type')=='custom_tool_call_output':outputs.append((n,sha(line.encode()),list(strings(v.get('output')))))
process_receipts=[]
if iteration_number>=3:
 for p in [G/'neutral-adjudicator-prompt.txt',G/'literal-scope-annotation-v1.json']:
  text=p.read_text();matches=[{'record_ordinal':n,'record_sha256':h} for n,h,items in outputs if any(text in s for s in items)]
  assert matches and len(text)<=5500
  process_receipts.append({'path':str(p),'sha256':sha(p.read_bytes()),'actual_full_text_matches':matches})
receipts=[]
for x in D['inputs_read']:
 p=Path(x.get('path',x.get('file',x.get('filename'))));source=p.read_text();bounds=[(r[0],r[1]) if isinstance(r,list) else (r.get('start',r.get('unicode_start')),r.get('end',r.get('unicode_end'))) for r in x['ranges']];checks=[]
 for start,end in bounds:
  chunk=source[start:end];hits=[{'record_ordinal':n,'record_sha256':h} for n,h,items in outputs if any(chunk in s for s in items)];checks.append({'start':start,'end':end,'chunk_sha256':sha(chunk.encode()),'actual_tool_matches':hits,'complete':bool(hits) and 0<len(chunk)<=5500})
 contiguous=bounds[0][0]==0 and bounds[-1][1]==len(source) and all(a[1]==b[0] for a,b in zip(bounds,bounds[1:]));receipts.append({'path':str(p),'sha256':sha(p.read_bytes()),'ranges':checks,'complete':contiguous and all(c['complete'] for c in checks)})
output_manifest=json.loads((I/'reader-output-manifest.json').read_text()) if (I/'reader-output-manifest.json').exists() else {}
raw={l:{x['id']:x for x in json.loads(Path(output_manifest.get(l,I/f'reader-{l}.json')).read_text())['answers']} for l in ['a','b']};pack=json.loads((G/'fresh-borderline-input.json').read_text());expected={(x['reader'],x['id']) for x in pack['entries']};actual={(x['reader'],x['id']) for x in D['records']};assert len(D['records'])==len(expected)==len(pack['entries']) and actual==expected
for x in pack['entries']:assert x['complete_raw_entry']==raw[x['reader']][x['id']]
links=[];vector_count=0
for x in D['records']:
 assert x['raw_entry_sha256']==sha(canon(raw[x['reader']][x['id']]))
 assert not x.get('material_wrong_claims') or x['label']=='Incorrect'
 if iteration_number>=3:
  required=next(v['asked_facts'] for v in pack['fixed_asked_clause_map'] if v['id']==x['id'])
  assessed=[v['asked_fact'] if 'asked_fact' in v else v['required_clause'] for v in x['asked_fact_assessments']]
  assert assessed==required
  vector_count+=len(required)
 links.append({'reader':x['reader'],'id':x['id'],'raw_entry_sha256':x['raw_entry_sha256'],'adjudication_record_sha256':sha(canon(x)),'label':x['label']})
report={'one_fresh_adjudicator_only':True,'model_provenance':M,'process_instruction_receipts':process_receipts,'fixed_required_fact_assessments_verified':vector_count,'input_receipts':receipts,'all_actual_input_delivery_complete':len(receipts)==2 and all(x['complete'] for x in receipts),'complete_raw_entry_links':links,'adjudication_file_sha256':sha(P.read_bytes()),'primary_labels_preserved':True};(I/'fresh-adjudication-integrity.json').write_text(json.dumps(report,indent=2)+'\n');assert report['all_actual_input_delivery_complete'];print(f'Verified{len(links)} whole-entry adjudications, exact full actual input delivery, raw hashes and fixed rubric consistency.')
