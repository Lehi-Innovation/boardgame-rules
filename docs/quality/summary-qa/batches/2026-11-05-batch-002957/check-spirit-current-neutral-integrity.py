"""Bind one current neutral review to actual whole inputs and original entries."""
import argparse, ast, hashlib, json, subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

B=Path(__file__).resolve().parent
R=B.parents[4]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--iteration',required=True,type=int)
parser.add_argument('--agent',required=True)
parser.add_argument('--proof-suffix',default='')
args=parser.parse_args()
assert args.iteration>=8
assert not args.proof_suffix or all(c.islower() or c.isdigit() or c in '_-' for c in args.proof_suffix)
label=f'{args.iteration:02d}'
D=R/'docs/quality/summary-qa/spirit-island'/B.name/('expanded-iteration-'+label)
J=lambda p:json.loads(p.read_text())
H=lambda b:hashlib.sha256(b).hexdigest()
tree=ast.parse((B/'check-spirit-source09-delivery.py').read_text())
fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='strings')
ns={'json':json};exec(compile(ast.Module(body=[fn],type_ignores=[]),'<strings>','exec'),ns)
strings=ns['strings']
paths=[Path(x) for x in subprocess.run(['rg','--files','/mnt/c/Users/jonny/.codex/sessions'],capture_output=True,text=True,check=True).stdout.splitlines() if x.endswith(args.agent+'.jsonl')]
assert len(paths)==1
with paths[0].open() as f:meta=json.loads(next(f))['payload']
assert meta['id']==args.agent and meta['parent_thread_id']=='01a1ac01-c763-7bb1-901e-7458891630b8'
assert meta['agent_path']==f'/root/expanded{args.iteration}_adjudication_01'
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
selected_ids={x['id'] for x in manifest['requested_cases']}
for filename,key,source in [('questions.json','questions',D/'questions.json'),('answer-key.json','answers',Path(J(D/'input-manifest.json')['key_path'])),('asked-facts.json','questions',D/'asked-fact-map.json')]:
    original={x['id']:x for x in J(source)[key]}; subset=J(D/'adjudication-01'/filename)[key]
    assert {x['id'] for x in subset}==selected_ids and all(x==original[x['id']] for x in subset)
reads=[]
for receipt in report['inputs_read']:
    p=Path(receipt['path']);text=p.read_text();binding=manifest['inputs'][str(p)]
    assert H(p.read_bytes())==binding['sha256']==receipt['sha256']
    assert len(text)==binding['characters']==receipt['unicode_character_length']
    assert not receipt.get('truncated_ranges_requiring_reread')
    cursor=0;parts=[]
    for c in receipt['read_ranges']:
        a,z=c.get('start',c.get('start_inclusive')),c.get('end_exclusive',c.get('end'));assert a==cursor and a<z<=len(text)
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
assert all({x['id'] for x in packet['readers'][w]['answers']}==selected_ids for w in full)
# The established neutral protocol preserves both original same-question entries.
# Only requested pairs are adjudicated; exact field pointers below prohibit borrowing.
def pointer(v,path):
    for bit in path.split('/')[1:]:
        bit=bit.replace('~1','/').replace('~0','~');v=v[int(bit)] if isinstance(v,list) else v[bit]
    return v
refs=[]
def walk(v,who,ident):
    if isinstance(v,dict):
        source=v.get('path',v.get('source',v.get('file','')))
        if source.endswith('/raw-cases.json') and 'json_pointer' in v:
            path=v['json_pointer']; quote=v.get('quotation',v.get('quote',v.get('text'))); index=int(path.split('/')[4])
            assert path.startswith('/readers/'+who+'/answers/') and packet['readers'][who]['answers'][index]['id']==ident
            value=pointer(packet,path)
            if quote is not None: assert isinstance(value,str) and quote in value
            refs.append({'reader':who,'id':ident,**v})
        if source.endswith('/summary-snapshot.md') and 'spans' in v:
            for span in v['spans']:
                a,z=span['unicode_range_start_inclusive_end_exclusive']
                assert (D/'summary-snapshot.md').read_text()[a:z]==span['text']
        if source.endswith('/summary-snapshot.md') and 'unicode_range' in v:
            bounds=v['unicode_range']
            if isinstance(bounds,dict):
                a,z=bounds['start'],bounds['end']
                assert bounds.get('interval','half-open')=='half-open'
            else:
                a,z=bounds
            assert (D/'summary-snapshot.md').read_text()[a:z]==v.get('quotation',v.get('quote',v.get('text')))
        if source.endswith('/summary-snapshot.md') and ('unicode_character_range' in v or 'range' in v or 'start' in v):
            a,z=v.get('unicode_character_range',v.get('range',[v.get('start'),v.get('end')]))
            assert (D/'summary-snapshot.md').read_text()[a:z]==v.get('quotation',v.get('quote',v.get('text')))
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
    clauses=next(v for v in J(D/'asked-fact-map.json')['questions'] if v['id']==pair[1])['requested_clauses']
    assessed=x['requested_part_assessment']
    assert [v['clause_id'] for v in assessed]==[v['clause_id'] for v in clauses]
    for required,assessment in zip(clauses,assessed):
        assert [v['fact_index'] for v in assessment['fact_assessments']]==list(range(1,len(required['required_facts'])+1))
    if x['contradictions']:assert x['adjudicated_grade']=='incorrect'
    totals[pair[0]][original[pair]]-=1;totals[pair[0]][x['adjudicated_grade']]+=1
assert seen=={(x['reader'],x['id']) for x in manifest['requested_cases']} and len(seen)==len(manifest['requested_cases'])
assert all(any((x['reader'],x['id'])==pair for x in refs) for pair in seen), 'Each case needs exact same-entry reference validation'
effective={w:{k:v[k] for k in ['correct','partial','incorrect']} for w,v in totals.items()}
parent_result_path=D/'results-adjudicated.json'
if parent_result_path.exists():
    assert {w:x['totals'] for w,x in J(parent_result_path)['readers'].items()}==effective
proof={'verified':True,'checked_at_utc':datetime.now(timezone.utc).isoformat(),'runtime':str(runtime),'runtime_sha256':H(runtime.read_bytes()),'report':str(report_path),'report_sha256':H(report_path.read_bytes()),'first_writer_record':boundary,'actual_full_input_checks':reads,'exact_same_entry_references':refs,'case_count':len(seen),'effective_scores':effective,'semantic_acceptance_status':'PENDING_SEPARATE_COORDINATOR_REVIEW','limits':['One neutral only; all primary originals preserved.','No format/receipt/epistemic cap; same-entry operative quotations count.','Current selected original neutral delivery/reference/arithmetic integrity only; no semantic upgrade or source/stamping/publication approval.']}
suffix=('-'+args.proof_suffix) if args.proof_suffix else ''
out=B/'coordinator-checks'/('spirit-expanded'+label+'-one-neutral-delivery-integrity'+suffix+'.json');assert not out.exists();out.write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps({'verified':True,'cases':len(seen),'whole_input_ranges':sum(len(x['ranges']) for x in reads),'same_entry_refs':len(refs),'effective':effective,'proof':str(out)}))
