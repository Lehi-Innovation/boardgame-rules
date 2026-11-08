from pathlib import Path
import copy,hashlib,json
B=Path(__file__).resolve().parent;ROOT=B.parents[4];load=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();side=[];references=[]
def stash(x,label):
 i=len(side);side.append(copy.deepcopy(x));return {'$technical':i,'label':label}
def diff(a,b,path=''):
 if a==b:return []
 if isinstance(a,dict) and isinstance(b,dict):
  return [r for key in sorted(set(a)|set(b)) for r in ([{'path':path+'/'+key,'op':'add','new':copy.deepcopy(b[key])}] if key not in a else [{'path':path+'/'+key,'op':'delete','old':copy.deepcopy(a[key])}] if key not in b else diff(a[key],b[key],path+'/'+key))]
 if isinstance(a,list) and isinstance(b,list) and len(a)==len(b):return [r for i,(x,y) in enumerate(zip(a,b)) for r in diff(x,y,path+'/'+str(i))]
 return [{'path':path,'op':'replace','old':copy.deepcopy(a),'new':copy.deepcopy(b)}]
r=load(B/'source-audit-final-12-corrected.json');v=load(B/'source-audit-final-12-corrected-visual-manifest.json');a=load(B/'source-audit12-own-correction-addendum.json');l=load(B/'source-audit12-correction-read-ledger.json');oldr=load(B/'source-audit-final-12.json');oldv=load(B/'source-audit-final-12-visual-manifest.json');assert r['source_delivery']==oldr['source_delivery'];assert a['new_card_views']==l['new_card_views'];assert r['correction_phase']['observation_changes']==a['changes'];assert len(a['new_card_views'])==33
obj={'report_field_changes':diff(oldr,r),'visual_manifest_field_changes':diff(oldv,v),'addendum':copy.deepcopy(a),'correction_read_ledger':copy.deepcopy(l)}
aliases={'card_views':(a['new_card_views'],'/addendum/new_card_views'),'changes':(a['changes'],'/addendum/changes'),'original_reuse':(a['original_source_reuse'],'/addendum/original_source_reuse')}
def encode(x,path=''):
 if isinstance(x,(dict,list)):
  for name,(value,canonical_path) in aliases.items():
   if path!=canonical_path and x==value:return {'$identical_to_canonical_addendum_field':name}
 if isinstance(x,dict):
  if 'passage' in x and 'candidate_sha256' in x:
   source=ROOT/x['path'];start,end=x['start'],x['end'];assert H(source)==x['candidate_sha256'] and source.read_text()[start:end]==x['passage'];references.append({'path':x['path'],'range':[start,end],'sha256':hashlib.sha256(x['passage'].encode()).hexdigest()});return stash(x,'exact copied unchanged candidate passage; own earlier whole delivery bound')
  result={}
  for key,value in x.items():
   if key in ['candidate_prior_delivery_ranges','complete_FAQ_prior_delivery_ranges','original_delivery_bindings','new_text_deliveries']:
    result[key]=stash(value,'exact original/new source range metadata')
   elif key in ['path','source_path','source_sha256','dimensions','output_cap','original_ledger_sha256','source_sha256','candidate_sha256']:
    result[key]=stash(value,'source identity metadata')
    if key in ['path','source_path']:result['source_filename' if key=='path' else 'source_asset']=Path(value).name
   else:result[key]=encode(value,path+'/'+key)
  return result
 if isinstance(x,list):return [encode(value,path+'/'+str(i)) for i,value in enumerate(x)]
 return x
projection=encode(obj)
def restore(x):
 if isinstance(x,dict):
  if '$technical' in x:return copy.deepcopy(side[x['$technical']])
  if '$identical_to_canonical_addendum_field' in x:return copy.deepcopy(aliases[x['$identical_to_canonical_addendum_field']][0])
  return {key:restore(value) for key,value in x.items() if key not in ['source_filename','source_asset']}
 if isinstance(x,list):return [restore(value) for value in x]
 return x
assert restore(projection)==obj
for changes,base,target in [(obj['report_field_changes'],oldr,r),(obj['visual_manifest_field_changes'],oldv,v)]:
 current=copy.deepcopy(base)
 for item in changes:
  parts=item['path'].strip('/').split('/');parent=current
  for key in parts[:-1]:parent=parent[int(key)] if isinstance(parent,list) else parent[key]
  key=int(parts[-1]) if isinstance(parent,list) else parts[-1]
  if item['op']=='delete':del parent[key]
  else:parent[key]=copy.deepcopy(item['new'])
 assert current==target
for name,data in [('source-audit12-corrected-root-semantic-projection.json',projection),('source-audit12-corrected-root-technical-sidecar.json',side),('source-audit12-corrected-candidate-citations.json',references)]:
 p=B/name;assert not p.exists();p.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n');print(json.dumps({'file':str(p),'characters':len(p.read_text()),'sha256':H(p)}))
print(json.dumps({'exact_full_reconstruction':True,'all_changed_fields_preserved':True,'all33_new_card_observations_present_once_by_exact_alias':True,'copied_candidate_passages_verified':len(references)}))
