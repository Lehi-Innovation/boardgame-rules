"""Bind the single neutral06 review to actual whole inputs and original entries."""
import ast, hashlib, json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

B=Path(__file__).resolve().parent
R=B.parents[4]
D=R/'docs/quality/summary-qa/spirit-island'/B.name/'expanded-iteration-06'
J=lambda p:json.loads(p.read_text())
H=lambda b:hashlib.sha256(b).hexdigest()
tree=ast.parse((B/'check-spirit-source09-delivery.py').read_text())
fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='strings')
ns={'json':json};exec(compile(ast.Module(body=[fn],type_ignores=[]),'<strings>','exec'),ns)
strings=ns['strings']
paths=[]
for p in Path('/mnt/c/Users/jonny/.codex/sessions/2026/11/07').glob('*.jsonl'):
    with p.open() as f:meta=json.loads(next(f)).get('payload',{})
    if meta.get('parent_thread_id')=='01a1ac01-c763-7bb1-901e-7458891630b8' and meta.get('agent_path')=='/root/expanded6_adjudication_01':paths.append(p)
assert len(paths)==1
runtime=paths[0]; outputs=[]; contexts=[]; writes=[]
for n,line in enumerate(runtime.open(),1):
    row=json.loads(line);p=row.get('payload',{})
    if row.get('type')=='turn_context':contexts.append((p.get('model'),p.get('effort')))
    if row.get('type')=='response_item':
        if p.get('type') in ['function_call_output','custom_tool_call_output']:
            outputs.append((n,H(line.encode()),list(strings(p.get('output')))))
        if p.get('type') in ['function_call','custom_tool_call']:
            t=p.get('input',p.get('arguments',''))
            if 'adjudication.json' in t and any(s in t for s in ['write_text','writeFile','apply_patch',".open('x')"]):writes.append(n)
    if row.get('type')=='event_msg' and p.get('type')=='item_completed':
        item=p.get('item',{})
        if item.get('type')=='CommandExecution':outputs.append((n,H(line.encode()),list(strings(item.get('aggregated_output','')))))
assert contexts and all(x==('gpt-6.1-sol','high') for x in contexts) and writes
boundary=min(writes)
report_path=D/'adjudication-01/adjudication-original-completed.json'
report=J(report_path);assert H(report_path.read_bytes())==H((D/'adjudication-01/adjudication.json').read_bytes())
manifest=J(D/'adjudication-01/input-manifest.json')
reads=[]
for receipt in report['inputs_read']:
    p=Path(receipt['path']);text=p.read_text();binding=manifest['inputs'][str(p)]
    assert H(p.read_bytes())==binding['sha256']==receipt['sha256']
    assert len(text)==binding['characters']==receipt['unicode_character_length'] and receipt.get('complete',receipt.get('complete_contiguous_read'))
    cursor=0;parts=[]
    for c in receipt['read_ranges']:
        a,z=c['start'],c.get('end_exclusive',c.get('end'));assert a==cursor and a<z<=len(text)
        seen=[{'record':n,'record_sha256':h} for n,h,values in outputs if n<boundary and any(text[a:z] in v or json.dumps(text[a:z],ensure_ascii=False)[1:-1] in v for v in values)]
        assert seen,(str(p),a,z)
        parts.append({'start':a,'end':z,'sha256':H(text[a:z].encode()),'actual_outputs':seen});cursor=z
    assert cursor==len(text)
    reads.append({'path':str(p),'sha256':H(p.read_bytes()),'ranges':parts})
assert {x['path'] for x in reads}==set(manifest['inputs'])
packet=J(D/'adjudication-01/raw-cases.json')
full={w:{x['id']:x for x in J(D/(w+'.json'))['answers']} for w in ['reader-a','reader-b']}
for w in full:
    assert all(x==full[w][x['id']] for x in packet['readers'][w]['answers'])
def pointer(v,path):
    for bit in path.split('/')[1:]:
        bit=bit.replace('~1','/').replace('~0','~');v=v[int(bit)] if isinstance(v,list) else v[bit]
    return v
refs=[]
def walk(v,who,ident):
    if isinstance(v,dict):
        if v.get('path','').endswith('/raw-cases.json') and 'json_pointer' in v and ('quotation' in v or 'quote' in v):
            path=v['json_pointer']; quote=v.get('quotation',v.get('quote')); index=int(path.split('/')[4])
            assert path.startswith('/readers/'+who+'/answers/') and packet['readers'][who]['answers'][index]['id']==ident
            assert quote in pointer(packet,path)
            refs.append({'reader':who,'id':ident,**v})
        if v.get('path','').endswith('/summary-snapshot.md') and 'unicode_character_range' in v:
            a,z=v['unicode_character_range']; assert (D/'summary-snapshot.md').read_text()[a:z]==v['quotation']
        for child in v.values():walk(child,who,ident)
    elif isinstance(v,list):
        for child in v:walk(child,who,ident)
totals={w:Counter() for w in full};original={}
for p in sorted((D/'grading').glob('block-*/grades-original-completed.json')):
    for x in J(p)['grades']:original[x['reader'],x['id']]=x['grade'];totals[x['reader']][x['grade']]+=1
seen=set()
for x in report['adjudications']:
    pair=x['reader'],x['id'];assert pair not in seen and x['original_grade']==original[pair]
    seen.add(pair);walk(x,*pair)
    if x['contradictions']:assert x['adjudicated_grade']=='incorrect'
    totals[pair[0]][original[pair]]-=1;totals[pair[0]][x['adjudicated_grade']]+=1
assert seen=={(x['reader'],x['id']) for x in manifest['requested_cases']} and len(seen)==6
effective={w:{k:v[k] for k in ['correct','partial','incorrect']} for w,v in totals.items()}
assert effective=={'reader-a':{'correct':172,'partial':0,'incorrect':1},'reader-b':{'correct':171,'partial':1,'incorrect':1}}
assert {w:x['totals'] for w,x in J(D/'results-adjudicated.json')['readers'].items()}==effective
proof={'verified':True,'checked_at_utc':datetime.now(timezone.utc).isoformat(),'runtime':str(runtime),'runtime_sha256':H(runtime.read_bytes()),'report':str(report_path),'report_sha256':H(report_path.read_bytes()),'first_writer_record':boundary,'actual_full_input_checks':reads,'exact_same_entry_references':refs,'case_count':6,'effective_scores':effective,'semantic_acceptance':{'A_Q46':'Explicitly denies choosing the winning land first despite the operative rule allowing chosen Ravage land order; material false ruling remains Incorrect.','B_Q13':'Two Presence less one leaves one; explicit claim that two remain contradicts the requested state despite correct general quote.','B_Q37':'Growth play and no automatic play supplied, but separately requested immediate resolution outcome is genuinely absent from all same-entry fields.','Q81_both':'Nearest legal land, classifications and no-legal-land supply return all supplied. Unasked judgment/physical-distance detail is not required.','B_Q30':'Asked survivor effects, card destination and track Elements supplied. Unasked card-Element expiry is not an extra required answer.'},'limits':['One neutral only; all primary originals preserved.','No format/receipt/epistemic cap; same-entry operative quotations count.','Historical failed pair06 only; next C26/source/publication gates remain separate.']}
out=B/'coordinator-checks/spirit-expanded06-one-neutral-acceptance.json';assert not out.exists();out.write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps({'verified':True,'cases':len(seen),'whole_input_ranges':sum(len(x['ranges']) for x in reads),'same_entry_refs':len(refs),'effective':effective,'proof':str(out)}))
