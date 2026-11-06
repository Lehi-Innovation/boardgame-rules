import sys
sys.dont_write_bytecode = True
from pathlib import Path
import json, hashlib, base64, re

HERE = Path(__file__).resolve().parent
R = HERE.parent
A = R / 'final-stamped-source-audit-01'
F = R / 'expanded-v13-complete-requested-scope/luna-final-stamped-iteration-01'
RT = Path('/mnt/c/Users/jonny/.codex/sessions/2026/11/06/rollout-2026-11-06T08-33-02-01a1b17d-ec85-7a01-8175-22d4430ab94b.jsonl')
ACTOR = '/root/v13_stamped_i1_source_auditor'
PARENT = '01a1aaa2-7c89-7c92-bca8-a89efc3fe4d7'
def digest(b): return hashlib.sha256(b).hexdigest()
def save(name, obj):
    (HERE/name).write_text(json.dumps(obj, indent=2, ensure_ascii=False)+'\n')
def binding(p):
    b=Path(p).read_bytes()
    return {'path':str(p), 'bytes':len(b), 'sha256':digest(b)}

m = json.loads((A/'manifest.json').read_text())
rr = json.loads((A/'source-read-record.json').read_text())
dispatch = (R/'final-stamped-source-audit-01-dispatch.txt').read_text()
provenance_path = F/'source-auditor-terminal-runtime-provenance.json'
pv = json.loads(provenance_path.read_text())
target = [x for x in pv['records'] if x.get('agent')==ACTOR and x.get('runtime_source')==str(RT)]
assert len(target)==1
# Explicit projection; do not retain session IDs or other actors' metadata.
pv_target={k:target[0][k] for k in ['agent','runtime_source','parent_thread_id','settings','confirmed','all_contexts_at_snapshot','runtime_snapshot_bytes','runtime_snapshot_sha256','parse_issues']}
save('terminal-provenance-target.json', {'container_binding':binding(provenance_path),'target':pv_target})
files = [m['candidate']]+m['originals']+m['outputs']+[m['derivative_provenance_record']]
extra = [A/'manifest.json', A/'original-hashes.json',R/'final-stamped-source-audit-01-dispatch.txt',provenance_path]
unique = {x['path']:x for x in files}
checks=[]
for p,x in unique.items():
    actual=binding(p)
    checks.append({**actual,'expected_sha256':x['sha256'],'sha256_matches':actual['sha256']==x['sha256'], 'expected_bytes':x.get('bytes'),'bytes_match':x.get('bytes',actual['bytes'])==actual['bytes']})
before = {x['path']:x['sha256'] for x in checks}
before.update({str(p):binding(p)['sha256'] for p in extra})
save('file-hash-verification.json',checks)

raw=RT.read_bytes()
rtbind=binding(RT)
assert rtbind['sha256']==pv_target['runtime_snapshot_sha256'] and rtbind['bytes']==pv_target['runtime_snapshot_bytes']
projection=[]; outputs=[]; calls=[]; contexts=[]; images=[]; initial=[]; terminals=[]
offset=0
for ordinal,line in enumerate(raw.splitlines(keepends=True),1):
    d=json.loads(line); x=d.get('payload',{}); t=d.get('type')
    head={'record':ordinal,'byte_start_zero_based':offset,'record_bytes_including_lf':len(line),'record_sha256':digest(line)}
    offset+=len(line)
    if t=='session_meta':
        assert x.get('agent_path')==ACTOR and x.get('parent_thread_id')==PARENT
        projection.append({**head,'kind':'actor_parent_binding','actor':x.get('agent_path'),'parent':x.get('parent_thread_id')})
    elif t=='turn_context':
        context={**head,'kind':'model_effort','model':x.get('model'),'effort':x.get('effort')}
        contexts.append(context);projection.append(context)
    elif t=='response_item' and x.get('type')=='agent_message':
        texts=[c['text'] for c in x.get('content',[]) if c.get('type')=='input_text']
        item={**head,'kind':'initial_prompt_binding','author':x.get('author'),'recipient':x.get('recipient'),'opaque_encrypted_part_present':any(c.get('type')=='encrypted_content' for c in x.get('content',[])),'text_parts':[{'bytes':len(s.encode()),'sha256':digest(s.encode()),'contains_exact_dispatch':dispatch in s,'contains_dispatch_without_trailing_lf':dispatch.rstrip('\n') in s,'fresh_independent_instruction_present':'Fresh independent source auditor' in s} for s in texts]}
        initial.append(item);projection.append(item)
    elif t=='response_item' and x.get('type')=='custom_tool_call':
        item={**head,'kind':'tool_call','name':x.get('name'),'call_id':x.get('call_id'),'input':x.get('input','')}
        calls.append(item);projection.append(item)
    elif t=='response_item' and x.get('type')=='custom_tool_call_output':
        texts=[];imgs=[]
        for j,c in enumerate(x.get('output',[])):
            if c.get('type')=='input_text':texts.append({'content_index':j,'text':c['text']})
            elif c.get('type')=='input_image':
                url=c['image_url'];url=url.get('url') if isinstance(url,dict) else url
                match=re.fullmatch(r'data:([^;]+);base64,(.*)',url,re.S)
                assert match
                b=base64.b64decode(match.group(2),validate=True)
                receipt={**head,'content_index':j,'mime':match.group(1),'decoded_bytes':len(b),'decoded_sha256':digest(b),'call_id':x.get('call_id')}
                images.append(receipt);imgs.append(receipt)
        item={**head,'kind':'tool_output','call_id':x.get('call_id'),'texts':texts,'images':imgs}
        outputs.append(item);projection.append(item)
    elif t=='event_msg' and x.get('type')=='task_complete':
        msg=x.get('last_agent_message','')
        item={**head,'kind':'terminal_event','event':'task_complete','final_output_bytes':len(msg.encode()),'final_output_sha256':digest(msg.encode()),'reports_named':all(s in msg for s in ['source-audit.json','source-audit.md','manifest.json','source-read-record.json'])}
        terminals.append(item);projection.append(item)
with (HERE/'runtime-allowlisted-projection.jsonl').open('w') as out:
    for item in projection:out.write(json.dumps(item,ensure_ascii=False)+'\n')
# Decode complete JSON representations recursively, without interpreting truncation as absent content.
leaves=[]
def leaf_strings(s, record, content_index, trail):
    leaves.append({'record':record,'content_index':content_index,'representation_path':trail,'text':s})
    try:obj=json.loads(s)
    except (ValueError,TypeError):return
    def walk(o,path):
        if isinstance(o,str):leaf_strings(o,record,content_index,path)
        elif isinstance(o,dict):
            for k,v in o.items():walk(v,path+'/'+str(k))
        elif isinstance(o,list):
            for i,v in enumerate(o):walk(v,path+'/'+str(i))
    walk(obj,trail+'/json')
for output in outputs:
    for c in output['texts']:leaf_strings(c['text'],output['record'],c['content_index'],'text')
boundary_candidates=[x for x in calls if 'source-audit.json' in x['input']]
boundary=boundary_candidates[0]['record']
receipts=[]
for read in rr['reads']:
    text=Path(read['path']).read_text(); lines=text.split('\n')
    start,end=read['start_lf'],read['end_lf']
    numbered='\n'.join(f'{i}: {lines[i-1]}' for i in range(start,end+1))
    matches=[]
    for leaf in leaves:
        if leaf['record']>=boundary:continue
        pos=leaf['text'].find(numbered)
        while pos>=0:
            finish=pos+len(numbered)
            if (pos==0 or leaf['text'][pos-1]=='\n') and (finish==len(leaf['text']) or leaf['text'][finish]=='\n'):
                matches.append({k:v for k,v in leaf.items() if k!='text'}|{'character_start':pos,'numbered_block_utf8_bytes':len(numbered.encode()),'numbered_block_sha256':digest(numbered.encode())})
            pos=leaf['text'].find(numbered,pos+1)
    receipts.append({**read,'actual_file_sha256':digest(Path(read['path']).read_bytes()),'actual_split_lf_pieces':len(lines),'complete_contiguous_visible_matches_before_verdict_writer':matches,'verified':bool(matches) and digest(Path(read['path']).read_bytes())==read['sha256']})
save('text-delivery-receipts.json',receipts)
image_matches=[]
call_by_id={x['call_id']:x for x in calls}
image_position_by_call={}
for receipt in images:
    matches=[x for x in rr['visual_inspections'] if x['derivative_sha256']==receipt['decoded_sha256']]
    call=call_by_id[receipt['call_id']]
    requested_paths=re.findall(r'tools\.view_image\(\{path:("(?:[^"\\]|\\.)*")\}',call['input'])
    requested_paths=[json.loads(p) for p in requested_paths]
    position=image_position_by_call.get(receipt['call_id'],0)
    image_position_by_call[receipt['call_id']]=position+1
    requested=requested_paths[position] if position<len(requested_paths) else None
    image_matches.append({**receipt,'view_image_call_record':call['record'],'view_image_sequence_zero_based':position,'requested_view_image_path':requested,'requested_path_matches_declared_derivative':len(matches)==1 and requested==matches[0]['derivative'],'matching_declared_visuals':matches,'before_verdict_writer':receipt['record']<boundary,'exact_derivative_bytes_match':len(matches)==1 and binding(matches[0]['derivative'])['sha256']==receipt['decoded_sha256']})
save('image-delivery-receipts.json',image_matches)
failure_markers=[]
for leaf in leaves:
    markers=[s for s in ['command not found','FileExistsError','No such file','Failed to establish','ERROR:','socket failed','truncated','Successfully installed'] if s in leaf['text']]
    if markers:failure_markers.append({k:v for k,v in leaf.items() if k!='text'}|{'markers':markers,'text_utf8_bytes':len(leaf['text'].encode()),'text_sha256':digest(leaf['text'].encode())})
save('runtime-summary.json',{'runtime':rtbind,'physical_records':ordinal,'contexts':contexts,'initial_prompt':initial,'terminal_events':terminals,'tool_calls':len(calls),'tool_output_records':len(outputs),'verdict_writer_call_record':boundary,'report_related_tool_calls':[{'record':x['record'],'input_utf8_bytes':len(x['input'].encode()),'input_sha256':digest(x['input'].encode())} for x in boundary_candidates],'text_reads_verified':sum(x['verified'] for x in receipts),'declared_reads':len(receipts),'actual_images':len(images),'image_matches':sum(x['exact_derivative_bytes_match'] for x in image_matches),'failure_and_setup_markers':failure_markers})
save('unchanged-baseline.json',before)
print(json.dumps({'all_hashes_match':all(x['sha256_matches'] and x['bytes_match'] for x in checks),'files_checked':len(checks),'text_receipts':len(receipts),'verified':sum(x['verified'] for x in receipts),'images':len(images),'matched':sum(x['exact_derivative_bytes_match'] for x in image_matches),'boundary':boundary,'prompt_binding':initial,'terminal':terminals},ensure_ascii=False))
