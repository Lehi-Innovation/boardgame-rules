from pathlib import Path
import json,hashlib,sys
B=Path(__file__).parent.resolve();D=B/(sys.argv[1] if len(sys.argv)>1 else 'expanded-iteration-01');M=json.loads((D/'input-manifest.json').read_text());bank=B/M['benchmark_version'];Q=json.loads((D/'questions.json').read_text());K=json.loads((bank/'answer-key.json').read_text());R={r:json.loads((D/f'reader-{r}.json').read_text()) for r in 'ab'};H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();ids=[x['id'] for x in Q['questions']]
F=json.loads((D/'asked-fact-map.json').read_text());assert [x['id'] for x in F['questions']]==ids
for r,raw in R.items():assert len(raw['answers'])==len(ids) and len({x['id'] for x in raw['answers']})==len(ids) and {x['id'] for x in raw['answers']}==set(ids)
boundary=json.loads((D/'operative-unit-boundary-validation.json').read_text());assert boundary['all_passed'], 'Preserve outputs and resolve failed operative-unit boundary gate before grading'
assert boundary['summary_sha256']==H(D/'summary-snapshot.md')
for r in boundary['checks']:assert r['raw_output_sha256']==H(D/(r['reader']+'.json'))
base=D/'grading';base.mkdir(exist_ok=True);manifest=[];template=(B/'grader-protocol-template.txt').read_text();allids=[]
block_count=(len(ids)+19)//20
sizes=[len(ids)//block_count+(i<len(ids)%block_count) for i in range(block_count)]
assert all(15<=size<=20 for size in sizes),sizes
start=0
for n,size in enumerate(sizes,1):
 blockids=ids[start:start+size];d=base/f'block-{n:02}';d.mkdir(exist_ok=True);allids+=blockids
 q={**Q,'full_bank_question_count':len(ids),'questions':[x for x in Q['questions'] if x['id'] in blockids]};k={**K,'full_bank_question_count':len(ids),'answers':[x for x in K['answers'] if x['id'] in blockids]};raw={'full_bank_question_count':len(ids),'expected_ids':blockids,'readers':{f'reader-{r}':{'reader_metadata':R[r].get('reader'),'answers':[x for x in R[r]['answers'] if x['id'] in blockids]} for r in 'ab'},'full_raw_output_hashes':{r:H(D/f'reader-{r}.json') for r in 'ab'}}
 facts={**F,'full_bank_question_count':len(ids),'questions':[x for x in F['questions'] if x['id'] in blockids]}
 for filename,value in [('questions.json',q),('answer-key.json',k),('asked-facts.json',facts),('raw-answers.json',raw)]:
  p=d/filename
  if p.exists():assert json.loads(p.read_text())==value
  else:p.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
 # Reversible delivery proof: every original question, key and entire raw entry preserved exactly, no quote deduplication.
 for r in 'ab':
  rb={x['id']:x for x in R[r]['answers']};assert all(x==rb[x['id']] for x in raw['readers'][f'reader-{r}']['answers'])
 assert q['questions']==Q['questions'][start:start+size] and k['answers']==K['answers'][start:start+size]
 assert facts['questions']==F['questions'][start:start+size]
 prompt=template.format(summary=(D/'summary-snapshot.md'),questions=d/'questions.json',key=d/'answer-key.json',asked_facts=d/'asked-facts.json',answers=d/'raw-answers.json',output=d/'grades.json');(d/'grader-prompt.txt').write_text(prompt)
 bm={'expected_ids':blockids,'question_count':len(blockids),'reader_answer_count':2*len(blockids),'all_subset_entries_equal_originals':True,'quote_deduplication':False,'requested_model':'gpt-6.1-sol','requested_effort':'high','full_bank_hashes':{'questions':H(D/'questions.json'),'key':H(bank/'answer-key.json'),'reader_a':H(D/'reader-a.json'),'reader_b':H(D/'reader-b.json')},'inputs':{str(p):{'sha256':H(p),'characters':len(p.read_text())} for p in [D/'summary-snapshot.md',d/'questions.json',d/'answer-key.json',d/'raw-answers.json']}}
 bm['full_bank_hashes']['asked_facts']=H(D/'asked-fact-map.json');bm['inputs'][str(d/'asked-facts.json')]={'sha256':H(d/'asked-facts.json'),'characters':len((d/'asked-facts.json').read_text())}
 (d/'input-manifest.json').write_text(json.dumps(bm,indent=2)+'\n');manifest.append({'block':n,'path':str(d),'ids':blockids,'input_manifest_sha256':H(d/'input-manifest.json')})
 start+=size
assert allids==ids and len(allids)==len(set(allids))
(base/'blocks-manifest.json').write_text(json.dumps({'iteration':D.name,'benchmark':M['benchmark_version'],'question_count':len(ids),'blocks':manifest,'all_ids_once_per_reader':True},indent=2)+'\n');print(json.dumps({'blocks':len(manifest),'questions':len(ids),'answers':2*len(ids),'all_original_entry_equality_checks':True}))
