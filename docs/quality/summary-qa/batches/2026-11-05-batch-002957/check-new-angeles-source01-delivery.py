"""Verify public delivered input bytes; this does not resolve pending source scope."""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import base64
import hashlib
import json
from PIL import Image

B = Path(__file__).resolve().parent
R = B.parents[4]
G = R / 'docs/quality/summary-qa/new-angeles' / B.name
A = G / 'source-auditor'
RT = Path('/mnt/c/Users/jonny/.codex/sessions/2026/11/06/rollout-2026-11-06T20-50-22-01a1b420-fb9a-7502-a0a5-075546f28c41.jsonl')
PARENT = Path('/mnt/c/Users/jonny/.codex/sessions/2026/11/06/rollout-2026-11-06T20-10-17-01a1b3fc-466c-7322-8413-9e59ff041286.jsonl')

def digest(data): return hashlib.sha256(data).hexdigest()
def sha(p): return digest(p.read_bytes())
def read(p): return json.loads(p.read_text())
def rows(p): return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]
def strings(v, depth=0):
    if depth > 9: return
    if isinstance(v, str):
        yield v
        try: j = json.loads(v)
        except (ValueError, TypeError): return
        if j != v: yield from strings(j, depth+1)
    elif isinstance(v, dict):
        if v.get('type') in ('input_image', 'image'): return
        for x in v.values(): yield from strings(x, depth+1)
    elif isinstance(v, list):
        for x in v: yield from strings(x, depth+1)

audit = read(A/'source-audit.json')
assert audit['verdict'] == 'PASS' and not audit['findings']
assert sha(Path(audit['summary']['path'])) == audit['summary']['sha256']
for s in audit['sources']: assert sha(Path(s['path'])) == s['sha256']
text = rows(A/'text-delivery-receipts.jsonl')
images = rows(A/'image-delivery-receipts.jsonl')
crops = read(A/'native-crop-manifest.json')
expected, spans = [], {}
for e in text:
    p = Path(e['source']); t = p.read_text()
    assert sha(p) == e['source_sha256'] and len(t) == e['total_chars']
    part = t[e['start_char']:e['end_char_exclusive']]
    assert digest(part.encode()) == e['chunk_sha256_utf8']
    expected.append(part)
    spans.setdefault(str(p), []).append((e['start_char'],e['end_char_exclusive']))
for p, ranges in spans.items():
    cursor = 0
    for start, end in sorted(ranges):
        assert start <= cursor; cursor = max(cursor,end)
    assert cursor == len(Path(p).read_text())
assert set(spans) == {audit['summary']['path']} | {e['path'] for e in audit['sources'] if e['path'].endswith('.txt')}

matches = [[] for _ in expected]
delivered, contexts, terminal, names = [], [], [], Counter()
for n, line in enumerate(RT.open(),1):
    j = json.loads(line); q = j.get('payload',{})
    if not isinstance(q,dict): continue
    if j.get('type') == 'session_meta':
        identity = {k:q.get(k) for k in ['id','parent_thread_id','agent_path']}
    elif j.get('type') == 'turn_context':
        contexts.append({'ordinal':n,'model':q.get('model'),'effort':q.get('effort')})
    elif j.get('type') == 'event_msg' and q.get('type') == 'task_complete': terminal.append(n)
    elif j.get('type') == 'event_msg' and q.get('type') == 'item_completed':
        it = q.get('item',{})
        if it.get('type') == 'CommandExecution':
            output = it.get('aggregated_output','')
            values = list(strings(output))
            for i, part in enumerate(expected):
                if any(part in v for v in values):
                    matches[i].append({'ordinal':n,'record_sha256':digest(line.encode()),'exit_code':it.get('exit_code')})
    elif j.get('type') == 'response_item':
        if q.get('type') in ('function_call','custom_tool_call'): names[q.get('name')] += 1
        elif q.get('type') in ('function_call_output','custom_tool_call_output') and isinstance(q.get('output'),list):
            for i, v in enumerate(q['output']):
                if not isinstance(v,dict) or v.get('type') != 'input_image': continue
                url = v.get('image_url'); url = url.get('url') if isinstance(url,dict) else url
                assert isinstance(url,str) and ';base64,' in url
                data = base64.b64decode(url.split(';base64,',1)[1],validate=True)
                delivered.append({'ordinal':n,'block':i,'bytes_sha256':digest(data),'detail':v.get('detail'),'record_sha256':digest(line.encode())})
assert identity == {'id':'01a1b420-fb9a-7502-a0a5-075546f28c41','parent_thread_id':'01a1b3fc-466c-7322-8413-9e59ff041286','agent_path':'/root/source_auditor'}
assert contexts and all(c['model']=='gpt-6.1-sol' and c['effort']=='high' for c in contexts)
assert terminal and all(matches)
end = max(terminal)
assert all(any(m['ordinal']<end for m in mm) for mm in matches)
initial = []
for n,line in enumerate(PARENT.open(),1):
    if 'source_auditor' not in line: continue
    j=json.loads(line);q=j.get('payload',{})
    if j.get('type')!='response_item' or q.get('type')!='function_call' or not q.get('name','').endswith('spawn_agent'):continue
    a=q.get('arguments');a=json.loads(a) if isinstance(a,str) else a
    if a.get('task_name')=='source_auditor':
        initial.append({'ordinal':n,'raw_record_sha256':digest(line.encode()),**{k:a.get(k) for k in ['task_name','model','reasoning_effort','fork_turns']}})
assert len(initial)==1 and initial[0]['model']=='gpt-6.1-sol' and initial[0]['reasoning_effort']=='high' and initial[0]['fork_turns']=='none'

bound_images=[]
for e in images:
    p=Path(e['path']);h=sha(p)
    assert h==e['runtime_image_block_bytes_sha256']
    with Image.open(p) as im:
        assert list(im.size)==e['source_dimensions']==e['runtime_decoded_dimensions']
        assert digest(im.convert('RGB').tobytes())==e['source_decoded_rgb_sha256']==e['runtime_decoded_rgb_sha256']
    found=[d for d in delivered if d['bytes_sha256']==h and d['detail']=='original' and d['ordinal']<end]
    assert found,str(p)
    bound_images.append({'path':str(p),'sha256':h,'dimensions':e['source_dimensions'],'actual_deliveries':found})
crop_groups={}
for e in crops:
    p=Path(e['path']); parent=Path(e['parent'])
    assert sha(p)==e['file_sha256'] and sha(parent)==e['parent_sha256']
    with Image.open(parent) as source, Image.open(p) as crop:
        assert list(source.size)==e['parent_dimensions'] and list(crop.size)==e['dimensions']
        assert source.convert('RGB').crop(tuple(e['rectangle'])).tobytes()==crop.convert('RGB').tobytes()
    assert any(i['path']==str(p) for i in bound_images)
    crop_groups.setdefault(str(parent),[]).append(e)
used_cells = {p:sorted({c for e in group for c in e['cells']})
              for p,group in crop_groups.items()}
# Semantic crops may overlap (for example an overview plus named regions).
# Exact native crop equality matters; overlapping source views are legitimate.

proof={'verified_delivery_only':True,'checked_at_utc':datetime.now(timezone.utc).isoformat(),'checker_sha256':sha(Path(__file__)),'audit_path':str(A/'source-audit.json'),'audit_sha256':sha(A/'source-audit.json'),'summary_sha256':audit['summary']['sha256'],'auditor':identity,'actual_initial_spawn':initial[0],'actual_contexts_minimal':contexts,'runtime_path':str(RT),'runtime_sha256_at_check':sha(RT),'terminal_ordinals':terminal,'complete_text_files':len(spans),'text_slices':len(text),'text_delivery':[dict(e,actual_public_output_records=mm) for e,mm in zip(text,matches)],'original_image_count':len(bound_images),'original_image_deliveries':bound_images,'native_crop_count':len(crops),'native_crop_parents':len(crop_groups),'native_crop_pixel_equality':True,'public_tool_names':dict(names),'limits':['Delivery verification only. Pending Arrest Orders scope interpretation and final full-bank/source acceptance are not resolved by this proof.','The same fresh-origin source auditor reads only source/summary and its own delivery/provenance material according to its report; this proof verifies actual model/freshness and delivered public bytes, not cognition.','Atlas semantic used-cell coverage and source exclusions remain exactly as the audit reports. No claim is made that all unused cells or every card-instance value was audited.','Inputs precede the completed terminal event; no unverified first-draft chronology claim is made.','No blind reader, publication or final completion approval is granted.']}
proof['actual_native_crop_used_cells_by_parent'] = used_cells
out=B/'coordinator-checks/new-angeles-source01-actual-delivery.json'
assert not out.exists(),'Version a new proof rather than overwriting'
out.write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps({k:proof[k] for k in ['verified_delivery_only','complete_text_files','text_slices','original_image_count','native_crop_count','native_crop_parents']},indent=2))
