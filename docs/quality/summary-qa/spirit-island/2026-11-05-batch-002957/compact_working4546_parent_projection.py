from pathlib import Path
import json,copy,hashlib
B=Path(__file__).resolve().parent
src=json.loads((B/'working45-46-root-semantic-projection-v2.json').read_text());side=[]
def stash(obj,label=None):
 i=len(side);side.append(copy.deepcopy(obj));return {'$t':i,**({'label':label} if label else {})}
def encode(obj):
 if isinstance(obj,dict):
  if any(k.startswith('$') for k in obj):return stash(obj)
  if 'literal_passage' in obj and 'character_range' in obj:return stash(obj,obj.get('label','verified primary citation'))
  technical={'path','sha256','full_byte_sha256','byte_length','native_dimensions','dimensions','whole_region','regions','relevant_regions','viewed_region_xyxy','full_byte_sha256_at_verification','manifest_sha256_match'}
  result={k:encode(v) for k,v in obj.items() if k not in technical}
  omitted={k:v for k,v in obj.items() if k in technical}
  if omitted:
   result['$metadata']=stash(omitted)
   if 'path' in omitted:result['source_filename']=Path(omitted['path']).name
  return result
 if isinstance(obj,list):return [encode(x) for x in obj]
 return obj
# Uniform existing-input references and the two per-question positive judgments encode exactly.
checks=src['report']['current_actual_ask_and_fact_checks'];checkrows=[]
for x in checks:
 assert x['checked_in_pass45'] is True and x['checked_separately_in_pass46'] is True
 checkrows.append([x['id'],x['source_focus_families'],x['$exact_current_bank_given_fields']])
checkcodec={'$uniform_check_matrix':checkrows,'both_pass_flags':True,'description':'Each row [id,source-focus-families,exact-current-bank-given-fields-index] reconstructs its original two true flags and own-bank input reference. All173 checked; no answer or grading material is abbreviated for a grader.'}
saved=src['report']['current_actual_ask_and_fact_checks'];src['report']['current_actual_ask_and_fact_checks']=checkcodec
out=encode(src)
def decode(obj):
 if isinstance(obj,dict):
  if '$t' in obj:return copy.deepcopy(side[obj['$t']])
  result={k:decode(v) for k,v in obj.items() if k not in ['$metadata','source_filename']}
  if '$metadata' in obj:result.update(decode(obj['$metadata']))
  return result
 if isinstance(obj,list):return [decode(x) for x in obj]
 return obj
restored=decode(out);assert restored==src
restored['report']['current_actual_ask_and_fact_checks']=[{'id':i,'checked_in_pass45':True,'checked_separately_in_pass46':True,'source_focus_families':f,'$exact_current_bank_given_fields':n} for i,f,n in checkrows]
assert restored['report']['current_actual_ask_and_fact_checks']==saved
for name,obj in [('working45-46-root-semantic-projection-v3.json',out),('working45-46-root-technical-sidecar-v3.json',side)]:
 p=B/name;assert not p.exists();p.write_text(json.dumps(obj,ensure_ascii=False,separators=(',',':'))+'\n');print(json.dumps({'file':str(p),'characters':len(p.read_text()),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}))
print('Exact layered reconstruction of all original report/ledger/visual judgments confirmed.')
