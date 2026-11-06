from pathlib import Path
import sys,json,hashlib,shutil
P=Path(__file__).resolve().parent;I=P/sys.argv[1];ids=[x['id'] for x in json.loads((I/'questions.json').read_text())['questions']];rows=[]
for who in ['a','b']:
 f=I/f'reader-{who}.json'
 if not f.exists():rows.append({'reader':who,'count':0,'status':'output_not_yet_written'});continue
 d=json.loads(f.read_text());answers=d['answers'];assert [x['id'] for x in answers]==ids[:len(answers)]
 D=I/f'reader-{who}-batches';D.mkdir(exist_ok=True);old=sorted(D.glob('count-*.json'));unchanged=True
 if old:
  previous=json.loads(old[-1].read_text())['answers'];unchanged=answers[:len(previous)]==previous;assert unchanged,'Previously answered entries changed'
 target=D/f'count-{len(answers):03d}.json'
 if not target.exists():shutil.copyfile(f,target)
 else:assert json.loads(target.read_text())['answers']==answers
 rows.append({'reader':who,'count':len(answers),'expected':len(ids),'prefix_ids_once':True,'earlier_entries_unchanged':unchanged,'raw_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'checkpoint_path':str(target.resolve())})
(I/'assembly-progress.json').write_text(json.dumps({'mode':'Technical answer assembly only; no answers graded or factual/grade feedback given','readers':rows},indent=2)+'\n');print(rows)
