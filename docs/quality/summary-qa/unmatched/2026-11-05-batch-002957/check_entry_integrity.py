from pathlib import Path
import json,hashlib,sys
P=Path(__file__).resolve().parent;I=P/sys.argv[1];s=(I/'summary-snapshot.md').read_text()
def read(f):return json.loads(f.read_text())
def digest(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def h(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
entries={r:read(I/f'reader-{r}.json')['answers'] for r in ['a','b']};ids=[x['id'] for x in read(I/'questions.json')['questions']]
result={'method':'Independent exact source-span and lossless whole-entry integrity check. Optional kind/header/unit-boundary findings remain separate and alone do not cap factual grades. All original fields retained; no raw or grader input rewritten.','summary_sha256':digest(I/'summary-snapshot.md'),'question_sha256':digest(I/'questions.json'),'raw_file_sha256':{r:digest(I/f'reader-{r}.json') for r in ['a','b']},'readers':{},'packs':[]}
for r,answers in entries.items():
 assert [a['id'] for a in answers]==ids;rows=[]
 for a in answers:
  spans=[]
  for e in a['evidence']:
   assert type(e['start']) is int and type(e['end']) is int and 0<=e['start']<e['end']<=len(s)
   assert e['text']==s[e['start']:e['end']]
   spans.append({'unit_id':e['unit_id'],'start':e['start'],'end':e['end'],'exact_original_source_span':True})
  rows.append({'id':a['id'],'raw_entry_sha256':h(a),'all_original_fields':list(a),'source_spans':spans})
 result['readers'][r]=rows
seen=[]
for f in sorted((I/'grading').glob('*inputs.json')):
 pack=read(f);count=0
 for row in pack['records']:
  qid=row['question']['id'];seen.append(qid)
  for r in ['a','b']:
   original=next(x for x in entries[r] if x['id']==qid)
   assert row['raw_reader_entries'][r]==original and row['raw_entry_canonical_sha256'][r]==h(original);count+=1
 result['packs'].append({'path':str(f.resolve()),'sha256':digest(f),'full_entry_pairs_verified':count//2,'every_field_preserved':True})
assert seen==ids and len(set(seen))==len(ids)
result['complete_disjoint_ids']=True;result['question_count']=len(ids)
(I/'whole-entry-source-integrity-validation.json').write_text(json.dumps(result,indent=2)+'\n')
print('Exact original source spans and all raw-entry fields verified for both',len(ids),'answer sets; no factual grades inferred.')
