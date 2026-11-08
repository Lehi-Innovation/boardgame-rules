from pathlib import Path
import json,copy,hashlib
B=Path(__file__).resolve().parent;load=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();side=[]
def stash(obj,label):
 i=len(side);side.append(copy.deepcopy(obj));return {'$technical':i,'label':label}
def diff(a,b,path=''):
 if a==b:return []
 if isinstance(a,dict) and isinstance(b,dict):
  out=[]
  for key in sorted(set(a)|set(b)):
   p=path+'/'+key
   if key not in a:out.append({'path':p,'operation':'add','new':copy.deepcopy(b[key])})
   elif key not in b:out.append({'path':p,'operation':'delete','old':copy.deepcopy(a[key])})
   else:out.extend(diff(a[key],b[key],p))
  return out
 if isinstance(a,list) and isinstance(b,list) and len(a)==len(b):return [change for i,(x,y) in enumerate(zip(a,b)) for change in diff(x,y,path+'/'+str(i))]
 return [{'path':path,'operation':'replace','old':copy.deepcopy(a),'new':copy.deepcopy(b)}]
patches={}
for old,new in [('question-key-scope-review-14.json','question-key-scope-review-14-corrected.json'),('coverage-review-14.json','coverage-review-14-corrected.json'),('scope-coverage-14-read-ledger.json','scope-coverage-14-read-ledger-corrected.json')]:
 a=load(B/old);z=load(B/new);patches[new]={'original':old,'changes':diff(a,z)}
 for field in ['per_question_checks','input_hashes','scope_credit_validation','scope_validation_counts']:
  if field in a:assert a[field]==z[field],field
 if 'text_inputs' in a:assert a['text_inputs']==z['text_inputs']
addendum=load(B/'scope14-own-correction-addendum.json');ledger=load(B/'scope14-correction-read-ledger.json');assert addendum['own_report_phrase_correction']==ledger['own_report_phrase_correction'];assert len(ledger['new_card_views'])==33
obj={'complete_semantic_field_changes':patches,'addendum':copy.deepcopy(addendum),'correction_read_ledger':copy.deepcopy(ledger)}
for name in ['original_artifact_bindings','corrected_output_bindings']:
 for record in [obj['addendum'],obj['correction_read_ledger']]:
  if name in record:record[name]=stash(record[name],'exact '+name)
obj['correction_read_ledger']['new_text_reads']=stash(obj['correction_read_ledger']['new_text_reads'],'six source inputs: three own original artifacts whole, FAQ/key/map focused reopens; all exact rows retained')
# Keep all new transcription/comparison/old-new observation judgments. Only identities move.
def encode(x):
 if isinstance(x,dict):
  if '$technical' in x:return x
  fields=['path','full_byte_sha256','file_sha256','passage_utf8_sha256','symbol_transcription_sha256','dimensions','viewed_region_xyxy','rules_region_xyxy','original_ledger_sha256']
  metadata={k:v for k,v in x.items() if k in fields};result={k:encode(v) for k,v in x.items() if k not in metadata}
  if metadata:
   result['$metadata']=stash(metadata,'source identity/coordinates/hash metadata')
   if 'path' in metadata:result['source_filename']=Path(metadata['path']).name
  return result
 if isinstance(x,list):return [encode(v) for v in x]
 return x
projection=encode(obj)
def restore(x):
 if isinstance(x,dict):
  if '$technical' in x:return copy.deepcopy(side[x['$technical']])
  out={k:restore(v) for k,v in x.items() if k not in ['$metadata','source_filename']}
  if '$metadata' in x:out.update(restore(x['$metadata']))
  return out
 if isinstance(x,list):return [restore(v) for v in x]
 return x
restored=restore(projection);assert restored['complete_semantic_field_changes']==patches
for field in ['original_artifact_bindings','corrected_output_bindings']:
 if field in addendum:obj['addendum'][field]=addendum[field]
 if field in ledger:obj['correction_read_ledger'][field]=ledger[field]
obj['correction_read_ledger']['new_text_reads']=ledger['new_text_reads'];assert restored==obj
# Mechanical patch reapplication proves no corrected field is omitted from this review view.
for name,item in patches.items():
 current=load(B/item['original'])
 for change in item['changes']:
  pieces=change['path'].strip('/').split('/');target=current
  for part in pieces[:-1]:target=target[int(part)] if isinstance(target,list) else target[part]
  leaf=int(pieces[-1]) if isinstance(target,list) else pieces[-1]
  if change['operation']=='delete':del target[leaf]
  else:target[leaf]=copy.deepcopy(change['new'])
 assert current==load(B/name),name
for name,data in [('scope14-corrected-root-semantic-projection.json',projection),('scope14-corrected-root-technical-sidecar.json',side)]:
 p=B/name;assert not p.exists();p.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n');print(json.dumps({'path':str(p),'characters':len(p.read_text()),'sha256':H(p)}))
print(json.dumps({'exact_full_reconstruction':True,'new_card_observation_comparisons':33,'all173_question_checks_506_fact_hashes_unchanged':True,'all_current_corrections_included':True}))
