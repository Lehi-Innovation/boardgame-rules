"""Reversible parent-only review encoding; original grader/reader inputs never touched."""
from pathlib import Path
import copy,hashlib,json
B=Path(__file__).resolve().parent;load=lambda p:json.loads(p.read_text());H=lambda data:hashlib.sha256(data).hexdigest();k=load(B/'question-key-scope-review-14.json');c=load(B/'coverage-review-14.json');l=load(B/'scope-coverage-14-read-ledger.json');q={x['id']:x for x in load(B/'expanded-v24/questions.json')['questions']};a={x['id']:x for x in load(B/'expanded-v24/answer-key.json')['answers']};m={x['id']:x for x in load(B/'expanded-v24/asked-fact-map.json')['questions']};s={x['id']:x for x in load(B/'expanded-v24/core-scope-credit.json')['questions']};assert k['per_question_checks']==c['per_question_checks'];side=[]
def stash(obj,label):
 i=len(side);side.append(copy.deepcopy(obj));return {'$technical':i,'label':label}
rows=[];hashes={};assessment=k['per_question_checks'][0]['assessment']
for row in k['per_question_checks']:
 ident=row['id'];facts=[f for cl in m[ident]['requested_clauses'] for f in cl['required_facts']]
 assert row['literal_question_sha256']==H(q[ident]['question'].encode())
 assert row['fixed_key_answer_sha256']==H(a[ident]['answer'].encode())
 assert row['required_fact_entries_sha256']==H(json.dumps(facts,ensure_ascii=False,separators=(',',':')).encode())
 assert row['required_fact_count']==len(facts) and row['scope_result']==s[ident]['scope_result']
 assert row['literal_ask_checked'] is True and row['every_required_fact_checked'] is True and row['fixed_key_verdict']==row['asked_fact_mapping_verdict']=='PASS' and row['assessment']==assessment
 rows.append([ident,len(facts),row['scope_result'],row['source_family_checks']]);hashes[ident]={name:row[name] for name in ['literal_question_sha256','fixed_key_answer_sha256','required_fact_entries_sha256']}
assert len(rows)==173 and sum(x[1] for x in rows)==506
base=copy.deepcopy(k);original_rows=base['per_question_checks'];base['per_question_checks']={'$uniform_question_checks':rows,'uniform_template':{'literal_ask_checked':True,'every_required_fact_checked':True,'fixed_key_verdict':'PASS','asked_fact_mapping_verdict':'PASS','assessment':assessment},'exact_hashes':stash(hashes,'All173 exact current input question/key/flat-fact-list hashes verified')}
extras={name:value for name,value in c.items() if name not in k or k[name]!=value};deleted=[name for name in k if name not in c]
for name in ['input_hashes','read_evidence']:base[name]=stash(base[name],'exact '+name)
ledger=copy.deepcopy(l);inventory=[{'source_filename':Path(f['path']).name,'character_length':f['character_length'],'recorded_ranges':len(f['slices']),'complete_contiguous_delivery':f['complete_contiguous_delivery']} for f in ledger['text_inputs']];ledger['text_inputs']=stash(ledger['text_inputs'],'Exact22 input inventories/all245 recorded range rows retained')
obj={'key_report':base,'coverage_derivation':{'all_other_fields_exactly_equal_key_report':True,'deleted_fields':deleted,'different_or_added_fields':extras},'ledger':ledger,'derived_text_input_inventory':inventory}
# Do not suppress human observations or substantive judgments; only mechanical identity fields move.
def encode(x):
 if isinstance(x,dict):
  if '$technical' in x:return x
  tech={name:value for name,value in x.items() if name in ['path','full_byte_sha256','dimensions','viewed_region_xyxy']}
  result={name:encode(value) for name,value in x.items() if name not in tech}
  if tech:
   result['$metadata']=stash(tech,'exact source identity metadata')
   if 'path' in tech:result['source_filename']=Path(tech['path']).name
  return result
 if isinstance(x,list):return [encode(y) for y in x]
 return x
projection=encode(obj)
def restore(x):
 if isinstance(x,dict):
  if '$technical' in x:return copy.deepcopy(side[x['$technical']])
  result={name:restore(value) for name,value in x.items() if name not in ['$metadata','source_filename']}
  if '$metadata' in x:result.update(restore(x['$metadata']))
  # Inventory has only derived source filenames; restore is compared without it below.
  return result
 if isinstance(x,list):return [restore(y) for y in x]
 return x
restored=restore(projection);rk=restored['key_report'];codec=rk['per_question_checks'];full=[]
for ident,count,scope,families in codec['$uniform_question_checks']:
 row={'id':ident,**hashes[ident],'required_fact_count':count,**codec['uniform_template'],'scope_result':scope,'source_family_checks':families};full.append(row)
rk['per_question_checks']=full;assert rk==k
rc=copy.deepcopy(rk)
for name in deleted:del rc[name]
rc.update(restored['coverage_derivation']['different_or_added_fields']);assert rc==c;assert restored['ledger']==l
for name,value in [('scope14-root-semantic-projection.json',projection),('scope14-root-technical-sidecar.json',side)]:
 p=B/name;assert not p.exists();p.write_text(json.dumps(value,ensure_ascii=False,separators=(',',':'))+'\n');print(json.dumps({'path':str(p),'characters':len(p.read_text()),'sha256':H(p.read_bytes())}))
print(json.dumps({'exact_original_reconstruction':True,'current_questions':len(rows),'all_current_fact_entries_verified':sum(x[1] for x in rows),'source_inventory_entries':len(inventory)}))
