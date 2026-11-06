import json,pathlib,hashlib,collections,copy
p=pathlib.Path('/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/oath-chronicles-of-empire-and-exile/2026-11-05-batch-002957');d=p/'expanded-iteration-07';a=p/'delivery-audit'
g=json.loads((d/'grading-input.json').read_text());res=json.loads((d/'results.json').read_text());s=(d/'summary-snapshot.md').read_text();scope=json.loads((p/'expanded-v11/grading-scope.json').read_text());key=json.loads((p/'expanded-v11/answer-key.json').read_text());checks={};errors=[]
def check(name,condition):
 checks[name]=bool(condition)
 if not condition:errors.append(name)
check('all_original_input_hashes',all(hashlib.sha256(pathlib.Path(x['path']).read_bytes()).hexdigest()==x['sha256'] for x in g['inputs']))
check('packet_hash',hashlib.sha256((d/'grading-input.json').read_bytes()).hexdigest()=='d1de1d1197ee15c3da6d3e2d03851279a4af5a286403c464e3dd338e21a26b3a')
check('snapshot_hash',hashlib.sha256((d/'summary-snapshot.md').read_bytes()).hexdigest()=='cf1df544f9eb4b20cafbddd1200c237387b7361bef456e38e1a035e5fcd07e07')
ks={x['id']:x for x in key['answers']};ss={x['id']:x for x in scope['questions']}
check('fixed_key_expected_answers_exact',all(ks[q['id']]['expected_answer']==q['fixed_expected_answer'] for q in g['questions']))
check('scope_question_fact_text_and_ids_exact',all([(f['fact_id'],f['expected_fact']) for f in q['required_facts']]==[(f['fact_id'],f['expected_fact']) for f in ss[q['id']]['required_facts']] and q['question']==ss[q['id']]['question'] for q in g['questions']))
check('scope_exclusions_and_semantic_notes_exact',all(q['contextual_exclusions']==ss[q['id']]['contextual_exclusions'] and q['semantic_notes']==ss[q['id']]['semantic_notes'] for q in g['questions']))
count=0;quotes=0;evidencecount=0
for r in res['readers']:
 rid=r['reader'];raw=json.loads((d/(rid+'.json')).read_text());rawmap={x['id']:x for x in raw['answers']};ct=collections.Counter();ft=collections.Counter()
 check(rid+'_question_ids_order_exact',[x['id'] for x in r['questions']]==[x['id'] for x in g['questions']])
 for q,z in zip(g['questions'],r['questions']):
  e=q['readers'][rid];reconstructed=copy.deepcopy(e);spans=reconstructed.pop('attached_verbatim_passage_spans');vp=[]
  for sp in spans:
   t=s[sp['start']:sp['end']];check(rid+'_'+q['id']+'_quote_'+str(quotes),hashlib.sha256(t.encode()).hexdigest()==sp['sha256_utf8']);quotes+=1
   if sp['original_quote_type']=='string':vp.append(t)
   else:vp.append({**sp['original_quote_metadata'],'text':t})
  reconstructed['verbatim_passages']=vp
  check(rid+'_'+q['id']+'_raw_entry_lossless',reconstructed==rawmap[q['id']])
  check(rid+'_'+q['id']+'_observed_entry_exact',e==z['observed_answer'])
  check(rid+'_'+q['id']+'_fact_ids_text_exact',[(f['fact_id'],f['expected_fact']) for f in z['fact_checks']]==[(f['fact_id'],f['expected_fact']) for f in q['required_facts']])
  for f in z['fact_checks']:
   ft[f['status']]+=1;count+=1
   check(rid+'_'+f['fact_id']+'_nonempty_evidence',bool(f['evidence']))
   for ev in f['evidence']:
    evidencecount+=1;loc=ev['location']
    if 'span_if_quote' in ev:
     sp=ev['span_if_quote'];i=int(loc.rsplit('/',1)[1]);owner=spans[i]
     good=owner['start']<=sp['start']<=sp['end']<=owner['end'] and s[sp['start']:sp['end']]==ev['excerpt'] and hashlib.sha256(ev['excerpt'].encode()).hexdigest()==sp['sha256_utf8']
    elif loc.endswith('/answer'):good=ev['excerpt'] in e['answer']
    elif loc.endswith('/scenario'):good=ev['excerpt']==(json.dumps(e['scenario'],ensure_ascii=False) if isinstance(e['scenario'],dict) else e['scenario'])
    else:good=False
    check(f'evidence_{evidencecount}_literal_same_entry',good and loc.startswith(rid+'/'+q['id']+'/'))
  ct[z['grade']]+=1
  statuses=[f['status'] for f in z['fact_checks']];expectedgrade='incorrect' if 'contradiction' in statuses else 'partial' if 'missing' in statuses else 'correct'
  check(rid+'_'+q['id']+'_grade_derivation',z['grade']==expectedgrade)
 check(rid+'_totals',sum(ct.values())==104 and all(r['totals'][k]==ct[k] for k in ['correct','partial','incorrect']))
 check(rid+'_fact_totals',sum(ft.values())==328 and all(r['fact_totals'][k]==ft[k] for k in ['satisfied','missing','contradiction']))
check('208_entries_656_facts',sum(len(r['questions']) for r in res['readers'])==208 and count==656)
check('301_attached_quotes',quotes==301)
receipt=json.loads((a/'grader07-receipts.json').read_text());chunks=receipt['chunks'];check('73_delivery_chunks',len(chunks)==73)
for f in ['grading-input.json','summary-snapshot.md']:
 cc=[x for x in chunks if x['filename']==f];txt=(d/f).read_text();check(f+'_delivery_contiguous_complete',cc[0]['start']==0 and cc[-1]['end']==len(txt) and all(x['end']==y['start'] for x,y in zip(cc,cc[1:])))
 check(f+'_delivery_chunks_bounded_and_hashes',all(x['end']-x['start']<=5000 and hashlib.sha256(txt[x['start']:x['end']].encode()).hexdigest()==x['chunk_sha256_utf8'] for x in cc))
v={'status':'pass' if not errors else 'fail','questions_graded':208,'fact_assessments':count,'attached_quotes_verified':quotes,'literal_same_entry_evidence_checks':evidencecount,'checks_passed':sum(checks.values()),'checks_total':len(checks),'errors':errors,'checks':checks,'external_primary_rule_lookups':[],'limitations':'Semantic grades are human-model judgments; mechanical checks verify identity, ownership, literal evidence, complete counts, and derivation, not semantic truth.'}
(d/'grading-validation.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n');print({k:v[k] for k in ['status','checks_passed','checks_total','errors','fact_assessments','attached_quotes_verified']})
