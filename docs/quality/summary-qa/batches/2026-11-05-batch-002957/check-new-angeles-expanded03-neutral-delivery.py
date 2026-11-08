"""Bind one neutral's own whole-input deliveries and exact same-entry citations."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

B=Path(__file__).resolve().parent
R=B.parents[4]
D=R/'docs/quality/summary-qa/new-angeles'/B.name/'expanded-luna-iteration-03'
H=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_text())
report_path=D/'grading/fresh-borderline-adjudication.json'
report=load(report_path); packet=load(D/'grading/fresh-borderline-input.json')
actor='01a1b5ee-c30f-7042-b271-dcf54d5388e6'
runtime=next(Path('/mnt/c/Users/jonny/.codex/sessions/2026/11/07').glob('*'+actor+'.jsonl'))
def strings(v,depth=0):
    if depth>8:return
    if isinstance(v,str):
        yield v
        try:c=json.loads(v)
        except (ValueError,TypeError):return
        if c!=v:yield from strings(c,depth+1)
    elif isinstance(v,dict):
        if v.get('type') in ('input_image','image'):return
        for x in v.values():yield from strings(x,depth+1)
    elif isinstance(v,list):
        for x in v:yield from strings(x,depth+1)
outputs=[];ends=[];contexts=[]
for n,line in enumerate(runtime.open(),1):
    d=json.loads(line);v=d.get('payload',{})
    if d.get('type')=='turn_context':contexts.append((v.get('model'),v.get('effort')))
    elif d.get('type')=='event_msg' and v.get('type')=='task_complete':ends.append(n)
    elif d.get('type')=='event_msg' and v.get('type')=='item_completed':
        it=v.get('item',{})
        if it.get('type')=='CommandExecution': outputs.append((n,H(line.encode()),list(strings(it.get('aggregated_output','')))))
assert ends and contexts and all(c==('gpt-6.1-sol','high') for c in contexts)
reads=[]
for f in report['inputs_read']:
    p=Path(f['path']); t=p.read_text();assert H(p.read_bytes())==f['sha256'] and len(t)==f['unicode_characters'] and f['complete']
    cursor=0
    for c in f['ranges']:
        a,z=c['unicode_start'],c['unicode_end']; assert a==cursor and a<z<=len(t) and H(t[a:z].encode())==c['sha256']
        matches=[{'ordinal':n,'raw_record_sha256':h} for n,h,vals in outputs if n<max(ends) and any(t[a:z] in value for value in vals)]
        assert matches,(str(p),a,z)
        reads.append({'path':str(p),'start':a,'end':z,'slice_sha256':c['sha256'],'actual_public_outputs':matches});cursor=z
    assert cursor==len(t)
assert {Path(f['path']).resolve() for f in report['inputs_read']}=={(D/'summary-snapshot.md').resolve(),(D/'grading/fresh-borderline-input.json').resolve()}
def pointer(v,path):
    for part in path.split('/')[1:]:
        part=part.replace('~1','/').replace('~0','~');v=v[int(part)] if isinstance(v,list) else v[part]
    return v
refs=[]
def refs_in(v,entry,ident):
    if isinstance(v,dict):
        if 'json_pointer' in v and 'start' in v and 'end' in v and 'exact_text' in v:
            text=pointer(entry,v['json_pointer']);assert isinstance(text,str) and text[v['start']:v['end']]==v['exact_text']
            refs.append({'id':ident,**v})
        for child in v.values():refs_in(child,entry,ident)
    elif isinstance(v,list):
        for child in v:refs_in(child,entry,ident)
entries={(x['reader'],x['id']):x for x in packet['entries']}
for x in report['records']:refs_in(x,entries[x['reader'],x['id']],x['id'])
proof={'verified':True,'checked_at_utc':datetime.now(timezone.utc).isoformat(),'actor':actor,'runtime_path':str(runtime),'runtime_sha256':H(runtime.read_bytes()),'report_path':str(report_path),'report_sha256':H(report_path.read_bytes()),'actual_contiguous_reads':reads,'actual_same_entry_exact_references':refs,'semantic_acceptance':{'Q13_b':'Correct: same-entry disputed-status context and quotation supply the precise qualification without requiring extra agreement for ordinary immediate trades.','Q21_b':'Partial: android occupied-destination prohibition genuinely absent; development exclusion supplied by exhaustive mover list; unrest background not asked.','Q52_both':'Partial: general any-android-free-district ignoring-paths movement procedure genuinely absent; all illness and threat facts correct.'},'limits':['One neutral only; original scores unchanged.','No second vote or factual penalty for quoting irrelevant evidence when substantive answer is correct.','Historical failed full94 pair03 only; no current04 source-gap/publication approval.']}
out=B/'coordinator-checks/new-angeles-expanded03-one-neutral-actual-delivery-and-semantic-acceptance.json';assert not out.exists();out.write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps({'verified':True,'new_whole_input_slices':len(reads),'same_entry_exact_references':len(refs),'proof':str(out)}))
