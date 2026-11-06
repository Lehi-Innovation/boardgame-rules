from pathlib import Path
import json,hashlib,sys
ROOT=Path(__file__).resolve().parent
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def aggregate(it):
 d=ROOT/it;assert not (d/'results.json').exists(),'Refusing historical results overwrite';k=json.loads((d/'answer-key.json').read_text())['answers'];expected={q['id']:{f['id'] for f in q['required_facts']} for q in k};out={'iteration':it,'readers':{'a':[],'b':[]},'block_reports':[]}
 for p in sorted(d.glob('grades-block-*.json')):
  x=json.loads(p.read_text());out['block_reports'].append({'path':str(p),'sha256':h(p)})
  for reader,body in x['readers'].items():
   name='a' if reader in ['a','reader_a','reader-a'] else 'b' if reader in ['b','reader_b','reader-b'] else None;assert name
   rows=body.get('results',body.get('entries',body.get('grades',[])))
   for row in rows:
    facts=row.get('required_facts',row.get('fact_checks',[]));assert {f['id'] for f in facts}==expected[row['id']],(row['id'],'missing/duplicate facts')
    assert len(facts)==len(expected[row['id']]);assert row['grade'].lower()!='correct' or all(f.get('match') is True for f in facts),(row['id'],'Correct requires every required fact true');out['readers'][name].append({'id':row['id'],'grade':row['grade'].lower(),'original_grade_record':row,'block_report':p.name})
 for name,rows in out['readers'].items():
  assert len(rows)==len(expected) and len({r['id'] for r in rows})==len(expected) and {r['id'] for r in rows}==set(expected)
  rows.sort(key=lambda r:r['id']);out.setdefault('reader_scores',{})[name]={g:sum(r['grade']==g for r in rows) for g in ['correct','partial','incorrect']}
 out['totals']={g:sum(v[g] for v in out['reader_scores'].values()) for g in ['correct','partial','incorrect']};out['validation']={'every_expected_id_once_per_reader':True,'every_expected_fact_once_per_reader':True,'required_fact_count_per_reader':sum(map(len,expected.values())),'all_original_grade_fields_retained':True};out['PASS']=out['totals']=={'correct':2*len(expected),'partial':0,'incorrect':0}
 (d/'results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(it,out['reader_scores'],out['PASS'])
if __name__=='__main__':aggregate(sys.argv[1])
