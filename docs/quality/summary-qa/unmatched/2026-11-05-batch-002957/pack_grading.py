from pathlib import Path
import sys,json,hashlib
P=Path(__file__).resolve().parent;I=P/sys.argv[1];B=P/sys.argv[2];G=I/'grading';G.mkdir(exist_ok=False)
def read(p):return json.loads(p.read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def entry_hash(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
q=read(I/'questions.json')['questions'];k=read(B/'answer-key.json')['answers'];s=read(B/'scope-map.json')['questions'];raw={r:read(I/f'reader-{r}.json')['answers'] for r in ['a','b']};ids=[x['id'] for x in q]
assert ids==[x['id'] for x in k]==[x['id'] for x in s]
assert all(ids==[x['id'] for x in raw[r]] for r in raw)
assert len(ids)>=51
bounds=[(0,17),(17,34),(34,50),(50,len(ids))];receipts=[];allids=[]
for num,(start,end) in enumerate(bounds,1):
 rows=[]
 for j in range(start,end):
  row={'question':q[j],'fixed_key':k[j],'frozen_scope':s[j],'raw_reader_entries':{r:raw[r][j] for r in ['a','b']},'raw_entry_canonical_sha256':{r:entry_hash(raw[r][j]) for r in ['a','b']}}
  for r in raw:assert row['raw_reader_entries'][r]==raw[r][j]
  rows.append(row);allids.append(ids[j])
 pack={'benchmark':read(B/'questions.json')['benchmark_version'],'block':num,'ids':ids[start:end],'summary_path':str((I/'summary-snapshot.md').resolve()),'original_raw_file_sha256':{r:digest(I/f'reader-{r}.json') for r in ['a','b']},'entry_hash_definition':'SHA256 of lossless parsed entry reserialization with ensure_ascii=False,sort_keys=True,separators comma/colon. Every original entry field retained.','records':rows}
 f=G/f'block-{num:02d}-inputs.json';f.write_text(json.dumps(pack,ensure_ascii=False,indent=2)+'\n');receipts.append({'block':num,'path':str(f),'ids':ids[start:end],'sha256':digest(f),'question_count':end-start,'required_fact_count':sum(len(s[j]['required_answer_facts']) for j in range(start,end))})
assert allids==ids and len(set(allids))==len(ids)
(G/'input-manifest.json').write_text(json.dumps({'summary_sha256':digest(I/'summary-snapshot.md'),'questions_sha256':digest(I/'questions.json'),'key_sha256':digest(B/'answer-key.json'),'scope_sha256':digest(B/'scope-map.json'),'raw_file_sha256':{r:digest(I/f'reader-{r}.json') for r in ['a','b']},'blocks':receipts,'complete_disjoint_ids':True,'lossless_raw_entry_reconstruction':True},indent=2)+'\n')
print([(r['block'],r['question_count'],r['required_fact_count']) for r in receipts])
