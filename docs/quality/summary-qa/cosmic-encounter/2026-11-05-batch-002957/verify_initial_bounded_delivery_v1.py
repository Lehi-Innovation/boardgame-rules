"""Additive actual transport proof; no factual grading or retrospective gate claim."""
from pathlib import Path
import hashlib,json,sys
R=Path(__file__).parent.resolve()
it=Path(sys.argv[1]).resolve();label=sys.argv[2]
assert it.is_relative_to(R) and label in ('a','b')
def sha(b):return hashlib.sha256(b).hexdigest()
def strings(value):
    if isinstance(value,str):
        yield value
        try:parsed=json.loads(value)
        except ValueError:return
        if isinstance(parsed,(dict,list)):yield from strings(parsed)
    elif isinstance(value,dict):
        for v in value.values():yield from strings(v)
    elif isinstance(value,list):
        for v in value:yield from strings(v)
gates=sorted(it.glob(f'reader-{label}-input-gate-[0-9][0-9].json'));gate=json.loads(gates[-1].read_text())
receipt=json.loads(Path(gate['actual_delivery_validation']).read_text())
prov=json.loads((R/'model-provenance.json').read_text())
agent=next(a for a in prov['agents'] if a['identity']==gate['identity'])
outputs=[]
for index,raw in enumerate(Path(agent['runtime_source_path']).open()):
    row=json.loads(raw);ordinal=row.get('ordinal',index);payload=row.get('payload',{})
    if ordinal<=gate['after_ordinal'] and payload.get('type')=='custom_tool_call_output':
        outputs.append((ordinal,sha(raw.encode()),list(set(strings(payload.get('output'))))))
used=set();files=[]
for source in receipt['text_files']:
    text=Path(source['path']).read_text();checks=[];last=-1
    for chunk in source['chunks']:
        begin,end=chunk['start'],chunk['end'];piece=text[begin:end];found=[];oversized=[]
        for ordinal,digest,values in outputs:
            for value in values:
                where=value.find(piece)
                if where<0:continue
                left,right=begin,end;start,stop=where,where+len(piece)
                while left>0 and start>0 and text[left-1]==value[start-1]:left-=1;start-=1
                while right<len(text) and stop<len(value) and text[right]==value[stop]:right+=1;stop+=1
                if right-left>2900:oversized.append({'ordinal':ordinal,'source_start':left,'source_end':right})
                if left==begin and right==end:found.append({'ordinal':ordinal,'record_sha256':digest})
        available=[f for f in found if f['ordinal']>last and f['ordinal'] not in used]
        selected=min(available,key=lambda x:x['ordinal']) if available else None
        if selected:last=selected['ordinal'];used.add(last)
        checks.append({'start':begin,'end':end,'sha256':sha(piece.encode()),'bounded':0<end-begin<=2900,
                       'distinct_in_order_whole_payload':selected,'oversized_actual_source_matches':oversized,
                       'pass':bool(selected) and 0<end-begin<=2900 and not oversized})
    files.append({'path':source['path'],'chunks':checks,'pass':all(c['pass'] for c in checks)})
report={'reader':label,'identity':agent['identity'],'initial_gate_path':str(gates[-1]),
        'actual_outputs_limited_through_original_gate_ordinal':gate['after_ordinal'],
        'files':files,'pass':len(files)==2 and all(x['pass'] for x in files),
        'limit':'Additive later validation of original pre-draft public payloads; original gate only checked actual availability and declared bounds. This proof separately verifies whole bounded distinct actual outputs. No factual grade/cap or semantic comprehension claim.'}
out=it/f'reader-{label}-initial-bounded-actual-validation-01.json'
with out.open('x') as f:json.dump(report,f,indent=2);f.write('\n')
print({'reader':label,'pass':report['pass'],'actual_distinct_records':len(used),'chunks':sum(len(f['chunks']) for f in files)})
