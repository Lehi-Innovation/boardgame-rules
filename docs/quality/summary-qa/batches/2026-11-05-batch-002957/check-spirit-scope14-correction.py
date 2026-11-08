"""Verify the same-origin review correction, preserving its initial evidence."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import base64
from PIL import Image

B=Path(__file__).resolve().parent
R=B.parents[4]
G=R/'docs/quality/summary-qa/spirit-island'/B.name
def read(p):return json.loads(p.read_text())
def digest(b):return hashlib.sha256(b).hexdigest()
def sha(p):return digest(p.read_bytes())
def strings(v,depth=0):
    if depth>9:return
    if isinstance(v,str):
        yield v
        try:j=json.loads(v)
        except (ValueError,TypeError):return
        if j!=v:yield from strings(j,depth+1)
    elif isinstance(v,dict):
        if v.get('type') in ('input_image','image'):return
        for x in v.values():yield from strings(x,depth+1)
    elif isinstance(v,list):
        for x in v:yield from strings(x,depth+1)
def changes(a,b,p=''):
    if type(a)!=type(b):return [p]
    if isinstance(a,dict):
        out=[]
        for k in sorted(a.keys()|b.keys()):
            pp=p+'/'+str(k).replace('~','~0').replace('/','~1')
            out+=changes(a[k],b[k],pp) if k in a and k in b else [pp]
        return out
    if isinstance(a,list):
        if len(a)!=len(b):return [p]
        return [z for i,(x,y) in enumerate(zip(a,b)) for z in changes(x,y,p+'/'+str(i))]
    return [] if a==b else [p]

ip=B/'coordinator-checks/spirit-scope14-initial-actual-delivery.json'
initial=read(ip);assert initial['verified_delivery_only']
ap=G/'scope14-own-correction-addendum.json'
lp=G/'scope14-correction-read-ledger.json'
a,l=read(ap),read(lp)
for p,h in a['original_artifact_bindings'].items():assert sha(Path(p))==h
for p,h in a['corrected_output_bindings'].items():assert sha(Path(p))==h
assert a['read_evidence']['sha256']==sha(lp)
assert a['verdict']==a['fixed_key_verdict']==a['asked_fact_mapping_verdict']==a['scope_verdict']==a['coverage_verdict']==a['stopping_verdict']=='PASS'
assert a['checked_question_count']==173 and a['checked_required_grading_fact_count']==506
assert a['remaining_gap_count']==0 and not a['remaining_gaps']
actual_changes={}
for name,expected in a['field_changes_by_artifact'].items():
    original=G/name.replace('-corrected','')
    corrected=G/name
    actual=changes(read(original),read(corrected))
    assert sorted(actual)==sorted(expected),(name,actual,expected)
    actual_changes[name]=actual
for stem in ['question-key-scope-review-14','coverage-review-14']:
    old,new=read(G/(stem+'.json')),read(G/(stem+'-corrected.json'))
    for f in ['per_question_checks','checked_question_ids','input_hashes','asked_fact_map_sha256','scope_credit_validation']:
        assert old[f]==new[f],f
    for p,h in new['input_hashes'].items():assert sha(Path(p))==h
assert read(G/'scope-coverage-14-read-ledger.json')['text_inputs']==read(G/'scope-coverage-14-read-ledger-corrected.json')['text_inputs']
original_inputs={e['path']:e['source_sha256'] for e in initial['actual_complete_text_delivery']}
reused={e['path']:e['sha256'] for e in l['reused_complete_primary_deliveries']}
assert reused==original_inputs
expected,rows=[],[]
for e in l['new_text_reads']:
    p=Path(e['path']);assert sha(p)==e['full_byte_sha256']
    t=p.read_text();assert len(t)==e['character_length']
    cursor=0
    for z in sorted(e['slices'],key=lambda z:(z['start'],z['end'])):
        part=t[z['start']:z['end']]
        assert z['end']-z['start']<=6000 and z['truncated'] is False
        assert digest(part.encode())==z['slice_utf8_sha256']
        if e['complete_new_delivery']:
            assert z['start']<=cursor;cursor=max(cursor,z['end'])
        expected.append(part);rows.append({'path':str(p),'source_sha256':e['full_byte_sha256'],'start':z['start'],'end':z['end'],'slice_sha256':z['slice_utf8_sha256'],'complete_new_file_delivery':e['complete_new_delivery']})
    if e['complete_new_delivery']:assert cursor==len(t)
    else:assert original_inputs.get(str(p))==e['full_byte_sha256']
views=l['new_card_views'];assert len(views)==33 and l['new_card_view_count']==33
assert len({x['full_byte_sha256'] for x in views})==33
rt=Path(initial['runtime_path']);matches=[[] for _ in rows];image_outputs=[];contexts=[];terminals=[]
boundary=initial['original_terminal_ordinal']
for n,line in enumerate(rt.open(),1):
    j=json.loads(line);v=j.get('payload',{})
    if not isinstance(v,dict):continue
    if j.get('type')=='turn_context':contexts.append({'ordinal':n,'model':v.get('model'),'effort':v.get('effort')})
    elif j.get('type')=='event_msg' and v.get('type')=='task_complete':terminals.append(n)
    elif n>boundary and j.get('type')=='event_msg' and v.get('type')=='item_completed':
        it=v.get('item',{})
        if it.get('type')=='CommandExecution':
            out=it.get('aggregated_output','');vals=list(strings(out))
            for i,part in enumerate(expected):
                if any(part in s for s in vals):matches[i].append({'ordinal':n,'record_sha256':digest(line.encode()),'exit_code':it.get('exit_code')})
    elif n>boundary and j.get('type')=='response_item' and v.get('type') in ('function_call_output','custom_tool_call_output') and isinstance(v.get('output'),list):
        for i,z in enumerate(v['output']):
            if not isinstance(z,dict) or z.get('type')!='input_image':continue
            url=z.get('image_url');url=url.get('url') if isinstance(url,dict) else url
            data=base64.b64decode(url.split(';base64,',1)[1],validate=True)
            image_outputs.append({'ordinal':n,'block':i,'sha256':digest(data),'detail':z.get('detail')})
assert contexts and all(x['model']=='gpt-6.1-sol' and x['effort']=='high' for x in contexts)
assert len(terminals)>=2 and boundary==min(terminals)
end=max(terminals)
assert all(matches) and all(any(x['ordinal']<end for x in mm) for mm in matches)
bound=[]
for e in views:
    p=Path(e['path']);h=sha(p);assert h==e['full_byte_sha256']
    with Image.open(p) as im:assert list(im.size)==e['dimensions'] and e['viewed_region_xyxy']==[0,0,*list(im.size)]
    delivered=[x for x in image_outputs if x['sha256']==h and x['detail']=='original' and x['ordinal']<end]
    assert delivered,str(p)
    bound.append({'path':str(p),'sha256':h,'dimensions':e['dimensions'],'actual_new_native_deliveries':delivered})
proof={'verified':True,'checked_at_utc':datetime.now(timezone.utc).isoformat(),'checker_sha256':sha(Path(__file__)),'initial_delivery_proof':str(ip),'initial_delivery_proof_sha256':sha(ip),'same_initially_fresh_author':initial['actor'],'actual_initial_spawn':initial['actual_initial_spawn'],'runtime_path':str(rt),'runtime_sha256_at_check':sha(rt),'all_actual_contexts_minimal':contexts,'original_terminal_ordinal':boundary,'corrected_terminal_ordinal':end,'original_artifacts_unchanged':a['original_artifact_bindings'],'corrected_outputs_verified':a['corrected_output_bindings'],'own_correction_addendum':str(ap),'own_correction_addendum_sha256':sha(ap),'all_and_only_declared_field_changes':actual_changes,'all173_question_checks_and506_required_facts_unchanged':True,'all22_earlier_complete_text_deliveries_reused_with_exact_bindings':True,'new_text_inputs':len(l['new_text_reads']),'new_text_slices':len(rows),'new_actual_text_deliveries':[dict(e,actual_public_output_records=mm) for e,mm in zip(rows,matches)],'new_full_original_card_faces':bound,'new33_full_faces_verified':True,'N':173,'required_facts':506,'corrected_coverage_report':str(G/'coverage-review-14-corrected.json'),'corrected_coverage_report_sha256':sha(G/'coverage-review-14-corrected.json'),'corrected_key_scope_report':str(G/'question-key-scope-review-14-corrected.json'),'source_only_followup_prompt':str(G/'scope14-own-card-observation-correction-prompt.txt'),'source_only_followup_prompt_sha256':sha(G/'scope14-own-card-observation-correction-prompt.txt'),'verdict':'PASS','remaining_gaps':0,'limits':['This is a versioned correction by the same initially fresh source-only coverage reviewer, not another independent vote.','Three own original reports were newly reread completely; six focused primary/key/map reopens supplement their already-verified unchanged complete original delivery.','Source and bank hashes, all173 per-question checks and506 required facts remain unchanged. Corrected evidence notes do not independently imply a summary or key defect.','New literal readings and33 newly delivered native full faces precede the corrected terminal; no unverified first-draft write-boundary claim.','Coverage/key/scope evidence only: no reader, pure-source-audit, stamp, publication or game completion approval.']}
out=B/'coordinator-checks/spirit-scope14-corrected-actual-delivery.json';assert not out.exists();out.write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps({'verified':True,'N':173,'facts':506,'new_text_slices':len(rows),'new_native_faces':len(bound),'exact_declared_field_changes':True,'proof':str(out)},indent=2))
