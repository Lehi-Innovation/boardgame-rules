"""Bind fresh source13 audit to original public deliveries and source lineage."""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import base64
import hashlib
import json
import re
import subprocess
from PIL import Image

B = Path(__file__).resolve().parent
R = B.parents[4]
G = R / 'docs/quality/summary-qa/spirit-island' / B.name
def read(p): return json.loads(p.read_text())
def digest(b): return hashlib.sha256(b).hexdigest()
def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024), b''): h.update(b)
    return h.hexdigest()
def resolve(p): return (R / p).resolve()
def strings(v, depth=0):
    if depth > 9: return
    if isinstance(v,str):
        yield v
        try: child=json.loads(v)
        except (TypeError,ValueError): return
        if child != v: yield from strings(child,depth+1)
    elif isinstance(v,dict):
        if v.get('type') in ('input_image','image'): return
        for x in v.values(): yield from strings(x,depth+1)
    elif isinstance(v,list):
        for x in v: yield from strings(x,depth+1)

ap=G/'source-audit-final-13.json'
audit=read(ap)
ledger=read(G/'source-audit-final-13-read-ledger.json')
visual=read(G/'source-audit-final-13-visual-manifest.json')
candidate=resolve(audit['candidate_path'])
assert audit['verdict']=='PASS' and not audit['findings'] and audit['unresolved_findings']==0
assert sha(candidate)==audit['candidate_sha256']==audit['expected_candidate_sha256']
rows=ledger['deliveries']
fields=['path','start','end','source_sha256','slice_sha256','truncated']
assert [[e[k] for k in fields] for e in rows]==[[e[k] for k in fields] for e in audit['source_delivery']]
expected=[]; ranges={}; lengths={}
for e in rows:
    p=resolve(e['path']); assert sha(p)==e['source_sha256']
    choices=[p.read_bytes().decode('utf-8'),p.read_text()]
    choices=[t for t in choices if len(t)==e['character_length'] and digest(t[e['start']:e['end']].encode())==e['slice_sha256']]
    assert choices and e['truncated'] is False and e['output_cap']>=4000
    t=choices[0]; assert 0<=e['start']<e['end']<=len(t) and e['end']-e['start']<=6000
    expected.append(t[e['start']:e['end']]); ranges.setdefault(str(p),[]).append((e['start'],e['end'])); lengths[str(p)]=len(t)
for p,spans in ranges.items():
    cursor=0
    for start,end in sorted(spans):
        assert start<=cursor; cursor=max(cursor,end)
    assert cursor==lengths[p]
assert set(ranges)=={str(resolve(x['path'])) for x in ledger['source_files']}

actor='01a1b516-c016-78c0-b83a-c04a30719e71'
parent='01a1ac01-c763-7bb1-901e-7458891630b8'
paths=subprocess.run(['rg','--files','/mnt/c/Users/jonny/.codex/sessions'],check=True,capture_output=True,text=True).stdout.splitlines()
def runtime(ident):
    p=[Path(p) for p in paths if p.endswith(ident+'.jsonl')]; assert len(p)==1; return p[0]
rt=runtime(actor); matches=[[] for _ in rows]; image_outputs=[]; contexts=[]; terminal=[]; calls={}; names=Counter(); suspicious=[]
for n,line in enumerate(rt.open(),1):
    o=json.loads(line); v=o.get('payload',{})
    if not isinstance(v,dict): continue
    if o.get('type')=='session_meta': identity={k:v.get(k) for k in ['id','parent_thread_id','agent_path']}
    elif o.get('type')=='turn_context': contexts.append({'ordinal':n,'model':v.get('model'),'effort':v.get('effort')})
    elif o.get('type')=='event_msg' and v.get('type')=='task_complete': terminal.append(n)
    elif o.get('type')=='event_msg' and v.get('type')=='item_completed':
        it=v.get('item',{})
        if it.get('type')=='CommandExecution':
            out=it.get('aggregated_output','')
            if out:
                values=list(strings(out))
                for i,part in enumerate(expected):
                    if any(part in x for x in values): matches[i].append({'raw_runtime_ordinal':n,'raw_record_sha256':digest(line.encode()),'public_output_sha256':digest(out.encode()),'exit_code':it.get('exit_code')})
            command=it.get('command',[]); command='\n'.join(command) if isinstance(command,list) else str(command)
            for ln in command.splitlines():
                if re.search(r'questions\.json|answer-key\.json|reader-[ab]\.json|coverage-review|grading-block|/sessions/',ln) and re.search(r'read_text|read_bytes|open\(|\b(?:cat|sed|rg)\s',ln): suspicious.append({'ordinal':n,'line_sha256':digest(ln.encode())})
    elif o.get('type')=='response_item':
        typ=v.get('type')
        if typ in ('function_call','custom_tool_call'):
            name=v.get('name',''); names[name]+=1
            body=v.get('arguments',v.get('input','')); body=body if isinstance(body,str) else json.dumps(body)
            calls[v.get('call_id')]={'ordinal':n,'name':name,'body_sha256':digest(body.encode())}
            assert not re.search(r'(?:collaboration\.|spawn_agent|read_thread|send_message_to_thread)',name)
        elif typ in ('function_call_output','custom_tool_call_output') and isinstance(v.get('output'),list):
            for idx,x in enumerate(v['output']):
                if not isinstance(x,dict) or x.get('type')!='input_image': continue
                url=x.get('image_url'); url=url.get('url') if isinstance(url,dict) else url
                assert isinstance(url,str) and url.startswith('data:') and ';base64,' in url
                data=base64.b64decode(url.split(';base64,',1)[1],validate=True)
                image_outputs.append({'raw_runtime_ordinal':n,'block_index':idx,'bytes_sha256':digest(data),'bytes':len(data),'detail':x.get('detail'),'call_id':v.get('call_id')})
assert identity=={'id':actor,'parent_thread_id':parent,'agent_path':'/root/final_source_audit_13'}
assert contexts and all(x['model']=='gpt-6.1-sol' and x['effort']=='high' for x in contexts)
assert terminal and all(matches) and not suspicious,suspicious
end=max(terminal); assert all(any(x['raw_runtime_ordinal']<end for x in m) for m in matches)
dispatch=[]; parent_contexts=[]
for n,line in enumerate(runtime(parent).open('rb'),1):
    if b'final_source_audit_13' not in line and b'"turn_context"' not in line: continue
    o=json.loads(line); v=o.get('payload',{})
    if o.get('type')=='turn_context':
        parent_contexts.append({'ordinal':n,'model':v.get('model'),'effort':v.get('effort'),'turn_id':v.get('turn_id')}); continue
    if o.get('type')!='response_item' or not isinstance(v,dict) or v.get('type')!='function_call' or not v.get('name','').endswith('spawn_agent'): continue
    opts=v['arguments']; opts=json.loads(opts) if isinstance(opts,str) else opts
    if opts.get('task_name')!='final_source_audit_13': continue
    dispatch.append({'ordinal':n,'raw_record_sha256':digest(line),**{k:opts.get(k) for k in ['task_name','model','reasoning_effort','fork_turns']}})
assert len(dispatch)==1 and dispatch[0]['model']=='gpt-6.1-sol' and dispatch[0]['reasoning_effort']=='high' and dispatch[0]['fork_turns']=='none'
assert parent_contexts[-1]['model']=='gpt-6.1-sol' and parent_contexts[-1]['effort']=='high'
native=[]
for e in visual['visual_sources']:
    p=resolve(e['path']); h=sha(p); assert h==e.get('source_sha256',e.get('sha256'))
    with Image.open(p) as im: assert list(im.size)==e['dimensions']
    delivered=[x for x in image_outputs if x['bytes_sha256']==h and x['raw_runtime_ordinal']<end and x['detail']=='original']
    assert delivered,str(p)
    native.append({'path':str(p),'sha256':h,'dimensions':e['dimensions'],'actual_original_byte_deliveries':delivered})
supp=read(G/'supplemental-source-manifest-v4.json')
assert sha(G/'supplemental-source-manifest-v4.json')=='67934a634fb9032856cfc750bd279a6e2974fa75eee9694093325223e69ac1c2'
assert len(supp['source_records'])==len(audit['supplemental_record_reconciliation'])==72
assert all(sha(resolve(x['path']))==x['sha256'] for x in supp['source_records'])
original=read(G/'source-manifest.json'); assert all(sha(resolve(p))==h for p,h in original['paths_and_sha256'].items())
old=read(B/'coordinator-checks/spirit-source-audit-final-12-actual-delivery.json')
old_images={x['sha256'] for x in old['individually_bound_native_images'] if '/pdf-inspection/audit12/' not in x['path']}
assert old_images<={x['sha256'] for x in native}
lineage=read(B/'coordinator-checks/spirit-completed09-mandatory-inventory-and-render-lineage.json')
render_checks=[]
for x in lineage['independent_pdf_render_reproductions']:
    if not x['source_pdf'].endswith('spirit-island-rules.pdf'): continue
    h=sha(resolve(x['current_original_render']))
    m=[v for v in visual['visual_sources'] if v.get('sha256')==h and v.get('one_based_page')==x['page']]
    assert len(m)==1 and m[0]['original_pdf_sha256']==x['source_sha256'] and m[0]['matrix_scale']==x['matrix']
    assert sha(resolve(m[0]['original_pdf']))==x['source_sha256']
    render_checks.append({'path':m[0]['path'],'sha256':h,'page':x['page'],'pixel_and_byte_equal_independently_reproduced_prior_render':True})
assert [x['page'] for x in render_checks]==[6,7,17,32]
deriv=visual['publisher_html_derivation']; assert sha(resolve(deriv['visible_prose_derivative']))==deriv['derivative_sha256']=='73e15164ca9975c3ce8ed36d3a58174d61f545bd3e5156dfd3b8c92ec87b957a'
assert sha(resolve(deriv['source_path']))==deriv['source_sha256']
prompt=G/'final-source-audit-13-prompt.txt'; assert sha(prompt)=='e8ee12e3e1e938c50de6cee8f38be484f29947a45c8877c2c92900c6f5180d8e'
proof={'verified':True,'checked_at_utc':datetime.now(timezone.utc).isoformat(),'checker_sha256':sha(Path(__file__)),'audit_path':str(ap),'audit_sha256':sha(ap),'summary_sha256':sha(candidate),'current_canonical_matches':sha(R/'rules/spirit-island.md')==sha(candidate),'auditor':identity,'runtime_path':str(rt),'runtime_sha256_at_check':sha(rt),'actual_initial_spawn':dispatch[0],'actual_turn_contexts_minimal':contexts,'resumed_parent_latest_context':parent_contexts[-1],'actual_terminal_event_ordinals':terminal,'text_file_count':len(ranges),'text_slices':len(rows),'complete_actual_source_delivery':[dict(e,actual_public_output_records=m) for e,m in zip(rows,matches)],'native_unique_count':len(native),'actual_original_image_output_count':len(image_outputs),'individually_bound_native_images':native,'all_72_supplemental_source_hashes_current':True,'all_7_assigned_source_hashes_current':True,'old_mandatory_native_inventory_preserved':True,'core_render_lineage':render_checks,'publisher_prose_byte_equal_previously_independently_reproduced':True,'source_only_prompt_path':str(prompt),'source_only_prompt_sha256':sha(prompt),'public_tool_names':dict(names),'flagged_forbidden_reads':suspicious,'verdict':audit['verdict'],'findings':audit['findings'],'limits':['Original public deliveries precede the completed terminal event; no pre-first-draft chronology claim.','Original fresh source-only audit; no questions, keys, readers, grades or repair feedback supplied.','Delivery checks are separate from semantic review and are not an exhaustive cognition claim.','No reader-pair or publication approval.']}
out=B/'coordinator-checks/spirit-source-audit-final-13-actual-delivery.json'; assert not out.exists()
out.write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps({'verified':True,'proof':str(out),'text_files':len(ranges),'text_slices':len(rows),'native_unique':len(native),'image_deliveries':len(image_outputs),'current':proof['current_canonical_matches']}))
