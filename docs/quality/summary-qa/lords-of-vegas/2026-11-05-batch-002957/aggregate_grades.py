import json,hashlib,collections,sys
from pathlib import Path
R=Path(__file__).parent;D=R/(sys.argv[1] if len(sys.argv)>1 else 'expanded-iteration-03');load=lambda p:json.loads(p.read_text());hashv=lambda v:hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
q=load(D/'questions.json')['questions'];scope={x['id']:x for x in load(D/'scope-map.json')['entries']};keys={x['id']:x for x in load(D/'grading-key.json')['answers']};raw={l:{x['id']:x for x in load(D/f'reader-{l}.json')['answers']} for l in 'ab'}
result={'grading_standard':'Independent Sol/high disjoint blocks; every actually asked fact checked once per reader. All substantive fields of same raw entry assessed; no borrowing across questions; contextual key background is separate. Original grader findings retained without overwrite.','readers':{}};proof={'ids':{},'facts':{},'reconstruction':True,'grader_paths':[]}
for l in 'ab':
 grades=[];factpairs=[]
 for n in [1,2]:
  path=D/f'grader-block-{n}-results.json';obj=load(path);records=obj['readers'][l]['grades'];records=list(records.values()) if isinstance(records,dict) else records;proof['grader_paths'].append(str(path.resolve()))
  for original in records:
   ident=original['id'];entry=raw[l][ident];facts=original.get('required_facts',original.get('required_answer_facts'));indexes=[f['index'] for f in facts];count=len(scope[ident]['required_answer_facts']);zero_based=sorted(indexes)==list(range(count));assert zero_based or sorted(indexes)==list(range(1,count+1)),(ident,indexes)
   for f in facts:
    canonical_index=f['index']+1 if zero_based else f['index']
    assert f.get('required_fact',f.get('required_answer_fact',f.get('exact_fixed_required_fact')))==scope[ident]['required_answer_facts'][canonical_index-1],(ident,f)
    factpairs.append((ident,canonical_index))
   g={**original,'reason':original.get('whole_answer_reason',original.get('reason')),'question':next(x['question'] for x in q if x['id']==ident),'effective_fixed_key':keys[ident],'observed_raw_entry':entry,'observed_entry_canonical_sha256':hashv(entry),'grading_report':str(path.resolve()),'original_fact_index_base':0 if zero_based else 1,'fact_index_handling':'Original report indexes retained verbatim; only proof pairs normalize to one-based after exact fixed-text correspondence.'}
   if original.get('original_entry_canonical_sha256'):assert original['original_entry_canonical_sha256']==hashv(entry)
   grades.append(g)
 counts={k:sum(x['grade']==k for x in grades) for k in ['correct','partial','incorrect']};ids=[x['id'] for x in grades];assert collections.Counter(ids)==collections.Counter(x['id'] for x in q)
 assert len(factpairs)==len(set(factpairs))==sum(len(x['required_answer_facts']) for x in scope.values())
 result['readers'][l]={'counts':counts,'unresolved':counts['partial'],'unsupported_guesses':[x['id'] for x in grades if x.get('unsupported_guess')],'raw_sha256':hashlib.sha256((D/f'reader-{l}.json').read_bytes()).hexdigest(),'grades':sorted(grades,key=lambda x:x['id'])};proof['ids'][l]={'expected':len(q),'observed':len(ids),'unique':len(set(ids)),'all_expected_once':True};proof['facts'][l]={'expected':sum(len(x['required_answer_facts']) for x in scope.values()),'observed':len(factpairs),'unique':len(set(factpairs)),'all_expected_once':True}
(D/'results.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');(D/'grading-validation.json').write_text(json.dumps(proof,indent=2)+'\n');print({l:r['counts'] for l,r in result['readers'].items()})
