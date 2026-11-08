"""Lossless parent-only projection; never changes original evidence or grader inputs."""
from pathlib import Path
import copy,hashlib,json
B=Path(__file__).resolve().parent
load=lambda p:json.loads(p.read_text())
H=lambda x:hashlib.sha256(x).hexdigest()
r=load(B/'working-source-sweeps-45-46.json');l=load(B/'working-source-sweeps-45-46-read-ledger.json');v=load(B/'working-source-sweeps-45-46-visual-manifest.json')
q={x['id']:x for x in load(B/'expanded-v24/questions.json')['questions']};k={x['id']:x for x in load(B/'expanded-v24/answer-key.json')['answers']};m={x['id']:x for x in load(B/'expanded-v24/asked-fact-map.json')['questions']};s={x['id']:x for x in load(B/'expanded-v24/core-scope-credit.json')['questions']}
projection={'report':copy.deepcopy(r),'ledger':copy.deepcopy(l),'visual':copy.deepcopy(v)};side={};citations=[]
# Given input data are verified against the actual current immutable bank before encoding.
for i,row in enumerate(projection['report']['current_actual_ask_and_fact_checks']):
 ident=row['id'];expected={'literal_question':q[ident]['question'],'literal_requested_clauses_and_required_facts':m[ident]['requested_clauses'],'unasked_key_context_not_used_as_tested_coverage':m[ident]['key_context_not_required'],'predetermined_current_answer':k[ident]['answer'],'scope_classification':s[ident]['scope_result'],'scope_noncredited_clauses_retained':s[ident].get('noncredited_clauses',[])}
 for key,value in expected.items():
  assert row[key]==value,(ident,key)
  pointer=f'/report/current_actual_ask_and_fact_checks/{i}/{key}';side[pointer]=row.pop(key)
 row['$exact_current_bank_given_fields']=i
# Copies of the same72 dispositions are represented once, preserving every distinct judgment.
roles=projection['report']['source_corpus']['all72_supplemental_dispositions']
for obj,name in [(projection['ledger'],'ledger'),(projection['visual'],'visual')]:
 assert obj['supplemental_record_dispositions']==roles
 side[f'/{name}/supplemental_record_dispositions']=obj['supplemental_record_dispositions'];obj['supplemental_record_dispositions']={'$exact_report_roles':'/report/source_corpus/all72_supplemental_dispositions'}
# Eight already-reviewed own original-phase image records remain in technical sidecar after exact comparison.
old=load(B/'novelty-adjudication-18/visual-manifest.json')['images'];oldmap={x['path']:x for x in old}
for i,row in enumerate(projection['visual']['images']):
 if 'original_visual_manifest' not in row:continue
 original={key:value for key,value in row.items() if key not in ['disposition','original_visual_manifest','actual_delivery_proof']}
 assert original==oldmap[row['path']]
 pointer=f'/visual/images/{i}';side[pointer]=row;projection['visual']['images'][i]={'$previously_reviewed_own_image':pointer,'path':row['path'],'disposition':row['disposition']}
# Strip only copied primary literal passages after exact range/hash validation.
def walk(obj,path=''):
 if isinstance(obj,dict):
  if 'literal_passage' in obj:
   source=Path(obj['path']);data=source.read_bytes();text=data.decode();a,z=obj['character_range'];excerpt=text[a:z]
   assert H(data)==obj['full_byte_sha256'] and excerpt==obj['literal_passage'] and H(excerpt.encode())==obj['passage_utf8_sha256']
   key=path+'/literal_passage';side[key]=obj['literal_passage'];citations.append({'path':obj['path'],'range':[a,z],'sha256':H(excerpt.encode())});obj['literal_passage']={'$verified_primary_literal':key}
  for key,value in list(obj.items()):walk(value,path+'/'+key)
 elif isinstance(obj,list):
  for i,value in enumerate(obj):walk(value,path+'/'+str(i))
walk(projection)
# Technical-only hashes, delivery ranges and old own receipts are retained without claiming new semantic reading.
for name,keys in {'report':['input_bindings','artifacts'],'ledger':['input_bindings','new_delivered_text_files','own_hash_verified_complete_primary_text_reuse'],'visual':[]}.items():
 for key in keys:
  pointer=f'/{name}/{key}';side[pointer]=projection[name][key];projection[name][key]={'$technical_sidecar':pointer}
def restore(obj):
 if isinstance(obj,dict):
  if '$exact_current_bank_given_fields' in obj:
   idx=obj['$exact_current_bank_given_fields'];result={key:restore(value) for key,value in obj.items() if key!='$exact_current_bank_given_fields'}
   for field in ['literal_question','literal_requested_clauses_and_required_facts','unasked_key_context_not_used_as_tested_coverage','predetermined_current_answer','scope_classification','scope_noncredited_clauses_retained']:result[field]=copy.deepcopy(side[f'/report/current_actual_ask_and_fact_checks/{idx}/{field}'])
   return result
  for marker in ['$exact_current_bank_input','$previously_reviewed_own_image','$verified_primary_literal','$technical_sidecar']:
   if marker in obj:return copy.deepcopy(side[obj[marker]])
  if '$exact_report_roles' in obj:return copy.deepcopy(roles)
  return {key:restore(value) for key,value in obj.items()}
 if isinstance(obj,list):return [restore(x) for x in obj]
 return obj
assert restore(projection)=={'report':r,'ledger':l,'visual':v}
for name,obj in [('working45-46-root-semantic-projection-v2.json',projection),('working45-46-root-technical-sidecar-v2.json',side),('working45-46-verified-primary-citations-v2.json',citations)]:
 p=B/name;assert not p.exists();p.write_text(json.dumps(obj,ensure_ascii=False,separators=(',',':'))+'\n');print(json.dumps({'path':str(p),'characters':len(p.read_text()),'sha256':H(p.read_bytes())}))
print(json.dumps({'exact_reconstruction':True,'current_questions':len(q),'mapped_facts':sum(len(c['required_facts']) for x in m.values() for c in x['requested_clauses']),'validated_literal_primary_copies':len(citations)}))
