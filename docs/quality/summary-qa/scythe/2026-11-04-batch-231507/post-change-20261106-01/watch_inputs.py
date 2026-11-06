from pathlib import Path
import json,hashlib,time,datetime,os
D=Path(__file__).resolve().parent
stamp=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def fingerprint(path):
 try:
  p=Path(path);s=p.stat();return {'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'size':s.st_size,'mtime_ns':s.st_mtime_ns}
 except OSError as e:return {'error':str(e)}
def event(value):
 with (D/'input-watch-events.jsonl').open('a') as f:f.write(json.dumps(value)+'\n')
 print(json.dumps(value),flush=True)
event({'event':'watch-started','at_utc':stamp(),'pid':os.getpid()})
last=None
while not (D/'STOP-WATCH').exists():
 config=json.loads((D/'input-manifest.json').read_text())['inputs']
 if (D/'additional-watched-inputs.json').exists():config.update(json.loads((D/'additional-watched-inputs.json').read_text()))
 current={name:fingerprint(name) for name in config};content_changes={name:{'expected':expected,'actual':current[name]} for name,expected in config.items() if current[name].get('sha256')!=expected['sha256']};metadata_changes={name:{'expected':expected,'actual':current[name]} for name,expected in config.items() if current[name]!=expected and name not in content_changes}
 state={'at_utc':stamp(),'pid':os.getpid(),'watched_count':len(config),'content_stable':not content_changes,'content_changes':content_changes,'metadata_changes':metadata_changes,'current':current}
 (D/'input-watch-state.json').write_text(json.dumps(state,indent=2)+'\n')
 signature=json.dumps([content_changes,metadata_changes],sort_keys=True)
 if signature!=last:
  event({'event':'input-observation','at_utc':state['at_utc'],'content_stable':state['content_stable'],'content_changes':content_changes,'metadata_changes':metadata_changes});last=signature
 if content_changes:(D/'INPUT-CHANGE-ALERT.json').write_text(json.dumps(state,indent=2)+'\n')
 time.sleep(15)
event({'event':'watch-stopped','at_utc':stamp(),'pid':os.getpid()})
