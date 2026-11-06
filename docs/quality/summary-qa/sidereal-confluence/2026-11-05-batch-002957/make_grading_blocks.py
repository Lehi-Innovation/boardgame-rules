from pathlib import Path
import json,hashlib,sys
ROOT=Path(__file__).resolve().parent
def sh(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical_hash(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def make(it,size):
 d=ROOT/it; assert not (d/'grading-block-manifest.json').exists(),'Refusing historical block overwrite'; q=json.loads((d/'questions.json').read_text())['questions'];k=json.loads((d/'answer-key.json').read_text())['answers'];f=json.loads((d/'asked-facts.json').read_text())['questions'];a=json.loads((d/'reader-a.json').read_text())['answers'];b=json.loads((d/'reader-b.json').read_text())['answers']
 def index(rows):
  assert len({x['id'] for x in rows})==len(rows);return {x['id']:x for x in rows}
 ki,fi,ai,bi=map(index,[k,f,a,b]);expected=[x['id'] for x in q];assert all(set(t)==set(expected) for t in [ki,fi,ai,bi])
 paths=[]
 for start in range(0,len(q),size):
  rows=[]
  for question in q[start:start+size]:
   i=question['id'];rows.append({'id':i,'question':question,'key':ki[i],'asked_scope':fi[i],'reader_a_original_entry':ai[i],'reader_b_original_entry':bi[i],'original_entry_canonical_hashes':{'a':canonical_hash(ai[i]),'b':canonical_hash(bi[i])}})
  dest=d/f'grading-block-{1+start//size:02}.json';assert not dest.exists();dest.write_text(json.dumps({'iteration':it,'scope':'Disjoint full original-entry grading; no dropped fields, no quotation substitutions, all same-entry substantive fields assessed.','source_raw_hashes':{n:sh(d/n) for n in ['summary-snapshot.md','questions.json','answer-key.json','asked-facts.json','reader-a.json','reader-b.json']},'records':rows},ensure_ascii=False,indent=2)+'\n');paths.append({'path':str(dest),'sha256':sh(dest),'ids':[x['id'] for x in rows]})
 (d/'grading-block-manifest.json').write_text(json.dumps({'blocks':paths,'expected_ids':expected,'every_expected_id_once_in_blocks':len([i for p in paths for i in p['ids']])==len(set(expected)),'original_entries_exactly_reconstructed':True,'per_reader_expected_fact_count':sum(len(x['required_facts']) for x in k)},indent=2)+'\n');print(paths)
if __name__=='__main__':make(sys.argv[1],int(sys.argv[2]))
