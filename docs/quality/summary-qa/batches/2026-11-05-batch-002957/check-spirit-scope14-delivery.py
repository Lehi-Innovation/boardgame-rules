"""Bind the initial independent coverage review to actual public input delivery.

The review's own card-observation correction remains separate from this proof.
"""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import hashlib
import json
import base64
from PIL import Image

B=Path(__file__).resolve().parent
R=B.parents[4]
G=R/'docs/quality/summary-qa/spirit-island'/B.name
def read(p): return json.loads(p.read_text())
def digest(b): return hashlib.sha256(b).hexdigest()
def sha(p): return digest(p.read_bytes())
def resolve(p): return (R/p).resolve()
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

cp=G/'coverage-review-14.json'
kp=G/'question-key-scope-review-14.json'
lp=G/'scope-coverage-14-read-ledger.json'
c,k,l=read(cp),read(kp),read(lp)
q=read(G/'expanded-v24/questions.json')['questions']
ids=[e['id'] for e in q]
factmap=read(G/'expanded-v24/asked-fact-map.json')
assert len(ids)==len(set(ids))==173 and factmap['required_fact_count']==506
for a in [c,k]:
    assert a['checked_question_ids']==ids and a['checked_question_count']==173
    assert a['checked_required_grading_fact_count']==506
    assert all(a[f]=='PASS' for f in ['verdict','fixed_key_verdict','asked_fact_mapping_verdict'])
    for f in ['fixed_key_findings','asked_fact_mapping_findings','missing_truly_asked_facts_in_map','missing_truly_asked_facts_in_fixed_key','scope_credit_findings','unresolved_relevant_findings']:assert not a[f]
    for p,h in a['input_hashes'].items():assert sha(resolve(p))==h,(p,h)
assert c['coverage_verdict']==c['stopping_verdict']=='PASS'
assert c['remaining_gap_count']==0 and not c['remaining_gaps']
assert c['complete_independent_challenge'] is True
expected,rows=[],[]
for e in l['text_inputs']:
    p=resolve(e['path']);assert sha(p)==e['full_byte_sha256']
    t=p.read_text();assert len(t)==e['character_length']
    cursor=0
    for z in sorted(e['slices'],key=lambda z:(z['start'],z['end'])):
        assert z['start']<=cursor and z['end']-z['start']<=6000 and z['truncated'] is False
        cursor=max(cursor,z['end'])
        part=t[z['start']:z['end']];assert digest(part.encode())==z['slice_utf8_sha256']
        expected.append(part)
        rows.append({'path':str(p),'source_sha256':e['full_byte_sha256'],'start':z['start'],'end':z['end'],'slice_sha256':z['slice_utf8_sha256'],'source_character_length':len(t),'declared_slice_character_cap':z['cap']})
    assert cursor==len(t)
assert len(l['text_inputs'])==22
assert not any(Path(e['path']).name.startswith(('source-candidate','summary-snapshot','reader-a','reader-b')) or e['path']==str(R/'rules/spirit-island.md') for e in rows)

projection=read(G/'runtime/scope_and_coverage_14-initial-projection.json')
actor=projection['thread_id'];rt=Path(projection['session_path'])
parent=Path(projection['requested_spawn']['source_record']['runtime_path'])
matches=[[] for _ in rows];images=[];contexts=[];terminal=[];names=Counter()
for n,line in enumerate(rt.open(),1):
    o=json.loads(line);v=o.get('payload',{})
    if not isinstance(v,dict):continue
    if o.get('type')=='session_meta':identity={f:v.get(f) for f in ['id','parent_thread_id','agent_path']}
    elif o.get('type')=='turn_context':contexts.append({'ordinal':n,'model':v.get('model'),'effort':v.get('effort')})
    elif o.get('type')=='event_msg' and v.get('type')=='task_complete':terminal.append(n)
    elif o.get('type')=='event_msg' and v.get('type')=='item_completed':
        it=v.get('item',{})
        if it.get('type')=='CommandExecution':
            out=it.get('aggregated_output','');values=list(strings(out))
            for i,part in enumerate(expected):
                if any(part in s for s in values):matches[i].append({'ordinal':n,'record_sha256':digest(line.encode()),'public_output_sha256':digest(out.encode()),'exit_code':it.get('exit_code')})
    elif o.get('type')=='response_item':
        if v.get('type') in ('function_call','custom_tool_call'):names[v.get('name')]+=1
        elif v.get('type') in ('function_call_output','custom_tool_call_output') and isinstance(v.get('output'),list):
            for i,z in enumerate(v['output']):
                if not isinstance(z,dict) or z.get('type')!='input_image':continue
                url=z.get('image_url');url=url.get('url') if isinstance(url,dict) else url
                assert isinstance(url,str) and ';base64,' in url
                data=base64.b64decode(url.split(';base64,',1)[1],validate=True)
                images.append({'ordinal':n,'block_index':i,'bytes_sha256':digest(data),'detail':z.get('detail')})
assert identity=={'id':actor,'parent_thread_id':'01a1ac01-c763-7bb1-901e-7458891630b8','agent_path':'/root/scope_and_coverage_14'}
assert contexts and all(z['model']=='gpt-6.1-sol' and z['effort']=='high' for z in contexts)
assert terminal and all(matches)
end=min(terminal)
assert all(any(z['ordinal']<end for z in mm) for mm in matches)
spawns=[]
for n,line in enumerate(parent.open(),1):
    if 'scope_and_coverage_14' not in line:continue
    o=json.loads(line);v=o.get('payload',{})
    if o.get('type')!='response_item' or v.get('type')!='function_call' or not v.get('name','').endswith('spawn_agent'):continue
    a=v.get('arguments');a=json.loads(a) if isinstance(a,str) else a
    if a.get('task_name')=='scope_and_coverage_14':spawns.append({'ordinal':n,'raw_record_sha256':digest(line.encode()),**{f:a.get(f) for f in ['task_name','model','reasoning_effort','fork_turns']}})
assert len(spawns)==1 and spawns[0]['model']=='gpt-6.1-sol' and spawns[0]['reasoning_effort']=='high' and spawns[0]['fork_turns']=='none'
native=[]
for e in l['images']:
    p=resolve(e['path']);h=sha(p);assert h==e['full_byte_sha256']
    with Image.open(p) as im:assert list(im.size)==e['dimensions'] and e['viewed_region_xyxy']==[0,0,*list(im.size)]
    received=[z for z in images if z['bytes_sha256']==h and z['detail']=='original' and z['ordinal']<end]
    assert received,str(p)
    native.append({'path':str(p),'sha256':h,'dimensions':e['dimensions'],'actual_original_byte_deliveries':received})
assert len(native)==54
prior=read(B/'coordinator-checks/spirit-source-audit-final-12-actual-delivery.json')
mandatory={e['sha256'] for e in prior['individually_bound_native_images'] if '/pdf-inspection/' not in e['path']}
assert len(mandatory)==53 and mandatory<={e['sha256'] for e in native}
prior_native={e['sha256'] for e in prior['individually_bound_native_images']}
extra_images=[e for e in native if e['sha256'] not in prior_native]
assert len(extra_images)==1
assert extra_images[0]['sha256']=='5f8f518b428a008bbe31b59a886dbea941b4555a01d42cc65ac25e1b996068e1'
assert Path(extra_images[0]['path']).name=='all-named-card-title-corner-strips.jpg'
prior_text={e['source_sha256'] for e in prior['complete_actual_source_delivery']}
prior_text.discard(prior['summary_sha256'])
current_text={e['source_sha256'] for e in rows}
# The physical-image BGG provenance metadata entries need not be reread when
# their complete original photo provenance plus native images are inspected.
optional_metadata={sha(resolve(e['path'])) for e in read(G/'source-audit-final-12-read-ledger.json')['coverage'] if Path(e['path']).name in ['bgg-all-original-spirits-image3635658-metadata.json','bgg-river-image4421052-metadata.json']}
assert prior_text-optional_metadata<=current_text
assert '73e15164ca9975c3ce8ed36d3a58174d61f545bd3e5156dfd3b8c92ec87b957a' in current_text
proof={'verified_delivery_only':True,'checked_at_utc':datetime.now(timezone.utc).isoformat(),'checker_sha256':sha(Path(__file__)),'coverage_report':str(cp),'coverage_report_sha256':sha(cp),'key_scope_report':str(kp),'key_scope_report_sha256':sha(kp),'read_ledger':str(lp),'read_ledger_sha256':sha(lp),'N':173,'required_fact_count':506,'actor':identity,'actual_initial_spawn':spawns[0],'runtime_path':str(rt),'runtime_sha256_at_check':sha(rt),'actual_contexts_minimal':contexts,'original_terminal_ordinal':end,'complete_text_inputs':22,'text_slices_including_rereads':len(rows),'actual_complete_text_delivery':[dict(e,actual_public_output_records=mm) for e,mm in zip(rows,matches)],'native_unique':len(native),'actual_original_images':native,'all53_required_nonPDF_images_preserved':True,'primary_text_corpus_preserved_except_optional_BGG_locator_metadata':True,'additional_CORE_image_already_independently_reproduced':True,'public_tool_names':dict(names),'limits':['Initial delivery proof only. Own Dissolve card observation reverses the printed Dahan/Explorer direction and requires versioned source-only correction; this proof grants no semantic coverage acceptance.','Actual initial model/freshness and full public source/bank/map deliveries precede the original terminal event. It does not prove cognition or exhaustive coverage.','Known fixed bank plus scoped conditional regressions; zero current-base novelty credit does not relax any existing asked grading requirement.','No blind reader, source-audit, stamp, publication or final completion approval.']}
proof.pop('additional_CORE_image_already_independently_reproduced')
proof['additional_membership_composite_aid']=dict(extra_images[0],role='Supplementary title/corner comparison only; all33 full faces were separately delivered. A copied full-face phrase in its pertinent-region metadata is not treated as a claim that this strip composite contains every rule.')
out=B/'coordinator-checks/spirit-scope14-initial-actual-delivery.json';assert not out.exists();out.write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps({f:proof[f] for f in ['verified_delivery_only','N','required_fact_count','complete_text_inputs','text_slices_including_rereads','native_unique']},indent=2))
