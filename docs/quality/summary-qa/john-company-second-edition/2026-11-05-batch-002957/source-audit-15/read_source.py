from pathlib import Path
import json,hashlib,sys,datetime
ROOT=Path('/home/jonny/projects/boardgame-rules')
OUT=ROOT/'docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/source-audit-15'
def read(path,start=1,end=None):
 p=Path(path);p=p if p.is_absolute() else ROOT/p
 data=p.read_bytes();lines=data.decode('utf-8',errors='replace').splitlines();end=min(end or len(lines),len(lines))
 chosen='\n'.join(f'{i}: {lines[i-1]}' for i in range(start,end+1))
 if len(chosen)>23000: raise ValueError('read exceeds safe output size; reduce chunk')
 logp=OUT/'source-read-record.json';log=json.loads(logp.read_text()) if logp.exists() else {'policy':'Allowed original sources only; reads capped at 23,000 characters and tool output at a safe token cap. No output truncations to date.','reads':[],'truncations':[]}
 log['reads'].append({'path':str(p),'sha256':hashlib.sha256(data).hexdigest(),'start_line':start,'end_line':end,'source_line_count':len(lines),'read_type':'text','truncated':False})
 logp.write_text(json.dumps(log,indent=2)+'\n')
 print(str(p)+f' [{start}-{end} of {len(lines)}]');print(chosen)
if __name__=='__main__': read(sys.argv[1],int(sys.argv[2]) if len(sys.argv)>2 else 1,int(sys.argv[3]) if len(sys.argv)>3 else None)
