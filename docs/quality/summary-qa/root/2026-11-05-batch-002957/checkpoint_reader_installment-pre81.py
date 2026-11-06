from build_evidence import *
import sys
I=R/sys.argv[1];who=sys.argv[2];path=I/f'reader-{who}.json'
raw=json.loads(path.read_text());ids=[x['id'] for x in raw['answers']]
assert ids==[f'Q{n:02}' for n in range(1,len(ids)+1)]
n=len(ids);dest=I/f'reader-{who}-installment-{n//5:02}.json'
if not dest.exists():shutil.copyfile(path,dest)
assert dest.read_bytes()==path.read_bytes()
note=I/f'reader-{who}-installment-manifest.json'
report=json.loads(note.read_text()) if note.exists() else {'status':'INCREMENTAL_ORIGINAL_BLIND_ASSIGNMENT','method':'Same fresh reader session, same two original factual inputs, no factual feedback; partial saved groups preserved before generic continuation. No installment separately graded or called a passing run.','checkpoints':[]}
if not any(x['answers']==n for x in report['checkpoints']):report['checkpoints'].append({'answers':n,'path':str(dest),'sha256':sha(dest)})
save(note,report)
print(json.dumps({'reader':who,'completed_answers':n,'checkpoints':len(report['checkpoints'])}))
