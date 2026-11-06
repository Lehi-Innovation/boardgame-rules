from pathlib import Path
import json,hashlib,collections,sys
B=Path(__file__).parent.resolve();D=B/sys.argv[1];load=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();M=load(D/'input-manifest.json');Q=load(D/'questions.json')['questions'];K=load(B/M['benchmark_version']/'answer-key.json')['answers'];ids=[x['id'] for x in Q];qby={x['id']:x for x in Q};kby={x['id']:x for x in K};R={f'reader-{r}':load(D/f'reader-{r}.json') for r in 'ab'};by={r:{x['id']:x for x in raw['answers']} for r,raw in R.items()};bm=load(D/'grading/blocks-manifest.json');res={'benchmark':M['benchmark_version'],'question_count':len(ids),'grading_basis':'Fresh independent Sol/high graders in disjoint balanced blocks. Each grader sees entire frozen summary, own exact fixed questions/key and complete original raw entries for both readers. No fields or quotes removed. Every actual requested part graded separately.','readers':{r:{'totals':{},'grades':[]} for r in R},'grading_blocks':[],'unresolved_adjudications':[]};seen=collections.Counter()
F=load(D/'asked-fact-map.json')['questions'];fby={x['id']:x for x in F}
for block in bm['blocks']:
 p=Path(block['path']);inp=load(p/'input-manifest.json');assert H(p/'input-manifest.json')==block['input_manifest_sha256'];assert all(H(Path(f))==v['sha256'] for f,v in inp['inputs'].items())
 q=load(p/'questions.json')['questions'];k=load(p/'answer-key.json')['answers'];raw=load(p/'raw-answers.json');assert q==[qby[i] for i in block['ids']] and k==[kby[i] for i in block['ids']]
 assert load(p/'asked-facts.json')['questions']==[fby[i] for i in block['ids']]
 for r in R:assert raw['readers'][r]['answers']==[by[r][i] for i in block['ids']]
 g=load(p/'grades.json');assert g['expected_ids']==block['ids'];entries=g['grades']
 # Schema accepts a flat list or explicit per-reader lists; no content changes.
 if isinstance(entries,dict):entries=[dict(x,reader=r) for r,arr in entries.items() for x in arr]
 count=collections.Counter((x['reader'],x['id']) for x in entries);assert set(count)=={(r,i) for r in R for i in block['ids']} and all(v==1 for v in count.values())
 for r in R:
  totals=collections.Counter(x['grade'] for x in entries if x['reader']==r)
  assert all(g['totals'][r][t]==totals[t] for t in ['correct','partial','incorrect']),g['totals']
 for x in entries:
  r=x['reader'];i=x['id'];assert x['grade'] in ['correct','partial','incorrect'];assert x['requested_part_assessment'];assert all(key in x for key in ['reason','missing_requested_material_facts','contradictions','unsupported_guesses','borderline_adjudication_needed']);seen[r,i]+=1
  assert isinstance(x['borderline_adjudication_needed'],bool) and all(isinstance(x[t],list) for t in ['missing_requested_material_facts','contradictions','unsupported_guesses'])
  clauses={c['clause_id']:c for c in fby[i]['requested_clauses']};parts=x['requested_part_assessment'];pc=collections.Counter(c['clause_id'] for c in parts)
  assert set(pc)==set(clauses) and all(v==1 for v in pc.values())
  for part in parts:
   expected_indices=set(range(1,len(clauses[part['clause_id']]['required_facts'])+1));fc=collections.Counter(f['fact_index'] for f in part['fact_assessments'])
   assert set(fc)==expected_indices and all(v==1 for v in fc.values())
   assert all(all(t in f for t in ['expected','observed','summary_support','outcome']) for f in part['fact_assessments'])
  item={'id':i,'question':qby[i]['question'],'expected':kby[i],'observed':by[r][i],**{a:v for a,v in x.items() if a not in ['id','reader']},'grader_output':str(p/'grades.json'),'grader_output_sha256':H(p/'grades.json')};res['readers'][r]['grades'].append(item)
  if x['borderline_adjudication_needed']:res['unresolved_adjudications'].append({'reader':r,'id':i,'source':str(p/'grades.json'),'detail':x['borderline_adjudication_needed']})
 res['unresolved_adjudications']+=g.get('unresolved_adjudications',[]);res['grading_blocks'].append({'path':str(p),'ids':block['ids'],'grades_sha256':H(p/'grades.json')})
assert set(seen)=={(r,i) for r in R for i in ids} and all(v==1 for v in seen.values())
for r,rr in res['readers'].items():
 rr['grades'].sort(key=lambda x:ids.index(x['id']));c=collections.Counter(x['grade'] for x in rr['grades']);rr['totals']={t:c[t] for t in ['correct','partial','incorrect']};rr['unsupported_guess_count']=sum(bool(x['unsupported_guesses']) for x in rr['grades'])
res['all_ids_once_per_reader']=True;res['all_inputs_exactly_preserved']=True;res['passes_full_bank']=not res['unresolved_adjudications'] and all(rr['totals']=={'correct':len(ids),'partial':0,'incorrect':0} and not rr['unsupported_guess_count'] and all(not x['missing_requested_material_facts'] and not x['contradictions'] for x in rr['grades']) for rr in res['readers'].values())
p=D/'results.json'
if p.exists():raise RuntimeError('Refuse overwrite frozen grading aggregation')
p.write_text(json.dumps(res,indent=2,ensure_ascii=False)+'\n');print(json.dumps({'question_count':len(ids),'totals':{r:rr['totals'] for r,rr in res['readers'].items()},'passes_full_bank':res['passes_full_bank'],'unresolved_adjudications':res['unresolved_adjudications']},indent=2))
