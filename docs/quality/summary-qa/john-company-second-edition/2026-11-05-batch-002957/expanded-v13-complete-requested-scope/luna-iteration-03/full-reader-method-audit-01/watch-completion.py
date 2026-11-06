import sys
sys.dont_write_bytecode=True
import pathlib,json,hashlib,datetime,time
O=pathlib.Path(__file__).parent;I=O.parent
H=lambda b:hashlib.sha256(b).hexdigest()
deadline=datetime.datetime.fromisoformat('2026-11-06T13:33:57+00:00')
previous={};seen=set()
while datetime.datetime.now(datetime.timezone.utc)<deadline:
 for role in 'ab':
  path=I/f'reader-{role}-draft.json'
  try:raw=path.read_bytes();data=json.loads(raw)
  except (OSError,ValueError):continue
  n=len(data.get('answers',[]));fp=I/f'reader-{role}.json';exists=fp.exists();state=(n,exists)
  now=datetime.datetime.now(datetime.timezone.utc).isoformat()
  if n==116 and role not in seen:
   dest=O/f'first-observed-complete-{role}-draft.json'
   if not dest.exists():dest.write_bytes(raw)
   record={'at_utc':now,'role':role,'count':n,'bytes':len(raw),'sha256':H(raw),'path':str(dest),'qualification':'First observed complete draft in this watcher; actual first-N write must be bound through the runtime and any authorized parent copy.'}
   (O/f'first-observed-complete-{role}-draft-binding.json').write_text(json.dumps(record,indent=2)+'\n');seen.add(role)
   print(json.dumps({'event':'first_observed_complete_draft',**record}),flush=True)
  if previous.get(role)!=state:
   record={'at_utc':now,'role':role,'count':n,'final_present':exists,'draft_sha256':H(raw)}
   with (O/'completion-watch-observations.jsonl').open('a')as out:out.write(json.dumps(record)+'\n')
   print(json.dumps(record),flush=True);previous[role]=state
 time.sleep(15)
print(json.dumps({'event':'bounded_watch_ended','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}),flush=True)
