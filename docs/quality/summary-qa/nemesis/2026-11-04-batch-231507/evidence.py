from pathlib import Path
import json,hashlib,sys,shutil,difflib
R=Path(__file__).resolve().parent;C=Path('/home/jonny/projects/boardgame-rules/rules/nemesis.md');S=Path('/home/jonny/projects/boardgame-rules/extracted/nemesis-rules.txt')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def freeze(name,bank):
 d=R/name;d.mkdir(exist_ok=False)
 shutil.copyfile(C,d/'summary-snapshot.md');shutil.copyfile(R/bank/'questions.json',d/'questions.json')
 write(d/'input-manifest.json',{'benchmark_version':bank,'hashes':{str(p):sha(p) for p in [d/'summary-snapshot.md',d/'questions.json',R/bank/'answer-key.json',S,R/'nemesis-original-rules.pdf',R/'nemesis-current-official-faq.pdf',R/'current-official-faq-extraction.txt']},'requested_model':'gpt-6-luna','requested_effort':'high'})
 (d/'summary-changes.patch').write_text(''.join(difflib.unified_diff((R/'original-summary.md').read_text().splitlines(True),C.read_text().splitlines(True),fromfile='original-summary.md',tofile='summary-snapshot.md')))
 print(d)
def provenance():
 items=[]
 for p in Path('/mnt/c/Users/jonny/.codex/sessions').rglob('*.jsonl'):
  try:
   first=json.loads(p.open().readline());x=first.get('payload',{});parent=x.get('source',{})
   if not isinstance(parent,dict):continue
   spawn=parent.get('subagent',{}).get('thread_spawn',{})
   if spawn.get('parent_thread_id')!='01a1aa59-7f47-7aa0-b41e-cdb1bdbea5fa':continue
   turns=[]
   for line in p.open():
    obj=json.loads(line)
    if obj.get('type')=='turn_context':turns.append({'timestamp':obj.get('timestamp'),'model':obj['payload'].get('model'),'effort':obj['payload'].get('effort')})
   items.append({'session_id':x.get('id'),'agent_path':spawn.get('agent_path'),'runtime_log':str(p),'session_meta':first,'turn_contexts':turns})
  except (OSError,json.JSONDecodeError):continue
 write(R/'model-provenance.json',{'isolation':'Fresh fork_turns=none contexts with instructions allowing only frozen files; filesystem access not sandbox-isolated','records':items});print([(i['agent_path'],i['turn_contexts'][:1]) for i in items])
if __name__=='__main__':
 if sys.argv[1]=='freeze':freeze(*sys.argv[2:])
 elif sys.argv[1]=='provenance':provenance()
