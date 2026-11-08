import json,hashlib,sys
from pathlib import Path
R=Path(__file__).parent;D=R/(sys.argv[1] if len(sys.argv)>1 else 'expanded-iteration-03');load=lambda p:json.loads(p.read_text());sh=lambda v:hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
raw={l:load(D/f'reader-{l}.json')['answers'] for l in 'ab'};questions=load(D/'questions.json')['questions'];scopes=load(D/'scope-map.json')['entries'];keys=load(D/'grading-key.json')['answers'];proof=[]
scope_mode=load(D/'grading-key.json').get('benchmark_scope_decision','Source-grounded actual-asked facts; no invented rule.')
for n,(first,last) in enumerate([(1,(len(questions)+1)//2),((len(questions)+1)//2+1,len(questions))],1):
 ids=[f'Q{i:02}' for i in range(first,last+1)];dictionary={};inverse={}
 def encode(v,in_quote=False):
  if isinstance(v,str) and in_quote:
   if v not in inverse:
    ident=f'U{len(dictionary)+1:03}';dictionary[ident]=v;inverse[v]=ident
   return {'__literal_quote__':inverse[v]}
  if isinstance(v,list):return [encode(x,in_quote) for x in v]
  if isinstance(v,dict):return {k:encode(x,in_quote or k=='operative_quotes') for k,x in v.items()}
  return v
 def decode(v):
  if isinstance(v,dict) and set(v)=={'__literal_quote__'}:return dictionary[v['__literal_quote__']]
  if isinstance(v,dict):return {k:decode(x) for k,x in v.items()}
  if isinstance(v,list):return [decode(x) for x in v]
  return v
 entries=[]
 for ident in ids:
  records={l:next(x for x in raw[l] if x['id']==ident) for l in 'ab'};encoded={l:encode(v) for l,v in records.items()};assert all(decode(encoded[l])==records[l] for l in 'ab')
  entries.append({'id':ident,'question':next(q for q in questions if q['id']==ident),'effective_fixed_key':next(k for k in keys if k['id']==ident),'asked_scope':next(s for s in scopes if s['id']==ident),'raw_entries':encoded,'original_entry_canonical_sha256':{l:sh(records[l]) for l in 'ab'}})
 obj={'benchmark_scope_decision':scope_mode,'protocol':'Reversible literal-quote dictionary only. Recursively replace a dictionary with sole key __literal_quote__ by dictionary[id]. Every original answer field including quote metadata, clause rulings, support,evidence and direct answer retained. Exact reconstruction and original record hashes checked. No answers or grades dropped.','ids':ids,'dictionary':dictionary,'entries':entries}
 p=D/f'grader-block-{n}.json';p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n');proof.append({'block':n,'ids':ids,'path':str(p.resolve()),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'all_raw_entries_exactly_reconstructed':True,'fact_count_per_reader':sum(len(e['asked_scope']['required_answer_facts']) for e in entries)})
(D/'grader-input-validation.json').write_text(json.dumps({'blocks':proof,'all_ids_once':len({x for p in proof for x in p['ids']})==len(questions),'all_raw_fields_preserved':True},indent=2)+'\n');print(proof)
