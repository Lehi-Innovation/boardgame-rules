"""Bind a completed game goal to the original host mutation after authorization."""
from pathlib import Path
from datetime import datetime,timezone
import argparse
import hashlib
import json
import subprocess

ap=argparse.ArgumentParser();ap.add_argument('--slug',required=True);args=ap.parse_args()
B=Path(__file__).resolve().parent
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def hb(b):return hashlib.sha256(b).hexdigest()
manifest=load(B/'manifest.json');g=next(x for x in manifest['games'] if x['slug']==args.slug)
assert args.slug=='root'
auth_path=B/'coordinator-checks/root-current19-final-completion-authorization.json'
auth=load(auth_path);assert auth['authorized'] is True
after=datetime.fromisoformat(auth['created_at_utc'])
paths=subprocess.run(['rg','--files','/mnt/c/Users/jonny/.codex/sessions'],check=True,capture_output=True,text=True).stdout.splitlines()
rt=[Path(p) for p in paths if p.endswith(g['thread_id']+'.jsonl')];assert len(rt)==1;rt=rt[0]
def objects(v,depth=0):
    if depth>10:return
    if isinstance(v,dict):
        yield v
        for x in v.values():yield from objects(x,depth+1)
    elif isinstance(v,list):
        for x in v:yield from objects(x,depth+1)
    elif isinstance(v,str):
        try:d=json.loads(v)
        except (ValueError,TypeError):return
        if d!=v:yield from objects(d,depth+1)
calls={};bindings=[];identity=None
for n,line in enumerate(rt.open('rb'),1):
    o=json.loads(line);p=o.get('payload',{})
    if not isinstance(p,dict):continue
    if o.get('type')=='session_meta':identity={k:p.get(k) for k in ['id','parent_thread_id','agent_path']}
    if o.get('type')!='response_item':continue
    typ=p.get('type')
    if typ in ['function_call','custom_tool_call']:
        body=p.get('input',p.get('arguments',''));body=body if isinstance(body,str) else json.dumps(body)
        if 'update_goal' not in p.get('name','') and 'tools.update_goal' not in body:continue
        if datetime.fromisoformat(o['timestamp'].replace('Z','+00:00'))<after:continue
        calls[p['call_id']]={'record':n,'record_sha256':hb(line),'timestamp':o['timestamp'],'input_sha256':hb(body.encode())}
    elif typ in ['function_call_output','custom_tool_call_output'] and p.get('call_id') in calls:
        goals=[x['goal'] for x in objects(p.get('output')) if isinstance(x.get('goal'),dict) and x['goal'].get('status')=='complete']
        for goal in goals:
            assert goal.get('threadId',g['thread_id'])==g['thread_id']
            bindings.append({'call':calls[p['call_id']],'output_record':n,'output_record_sha256':hb(line),'actual_status':'complete','goal_thread_id':goal.get('threadId'),'goal_id':goal.get('id'),'token_budget':goal.get('tokenBudget',goal.get('token_budget'))})
assert identity and identity['id']==g['thread_id'] and identity['parent_thread_id'] is None
if not bindings:
    print(json.dumps({'verified':False,'status':'awaiting-original-host-goal-completion','slug':args.slug}));raise SystemExit(0)
out=B/'coordinator-checks'/'root-current19-original-goal-completion.json'
assert not out.exists(),'Preserve prior proof; do not overwrite'
out.write_text(json.dumps({'verified':True,'checked_at_utc':datetime.now(timezone.utc).isoformat(),'slug':args.slug,'original_runtime_path':str(rt),'identity':identity,'actual_goal_status':'complete','completion_authorization_path':str(auth_path),'completion_authorization_sha256':sha(auth_path),'original_goal_tool_binding':bindings[-1],'limits':'Actual original goal-tool mutation result after coordinator publication authorization verified. UI completion/inactivity must also be checked before releasing the active chat slot.'},indent=2)+'\n')
print(json.dumps({'verified':True,'status':'complete','proof':str(out)}))
