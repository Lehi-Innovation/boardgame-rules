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

ip=B/'coordinator-checks/spirit-source-audit-final-12-actual-delivery.json'
initial=read(ip);assert initial['verified']
ap=G/'source-audit12-own-correction-addendum.json'
lp=G/'source-audit12-correction-read-ledger.json'
a,l=read(ap),read(lp)
resolve=lambda p:(R/p).resolve()
for e in a['original_artifacts']:assert sha(resolve(e['path']))==e['sha256']
old=read(G/'source-audit-final-12.json');new=read(G/'source-audit-final-12-corrected.json')
ov=read(G/'source-audit-final-12-visual-manifest.json');nv=read(G/'source-audit-final-12-corrected-visual-manifest.json')
assert new['verdict']=='PASS' and not new['findings'] and not a['new_candidate_findings']
assert new['candidate_sha256']==a['candidate_sha256']==initial['summary_sha256']
assert sha(resolve(new['candidate']))==sha(R/'rules/spirit-island.md')==new['candidate_sha256']
assert new['source_delivery']==old['source_delivery'] and len(new['source_delivery'])==94
assert new['source_delivery_summary']==old['source_delivery_summary']
assert new['read_ledger']==old['read_ledger']
expected_report={p for e in a['changes'] for p in e['report_json_pointers']}|{'/visual_manifest','/source_delivery_provenance','/correction_phase'}
expected_visual={p for e in a['changes'] for p in e['visual_manifest_json_pointers']}|{'/correction_phase'}
rd,vd=changes(old,new),changes(ov,nv)
assert set(rd)==expected_report,(rd,expected_report)
assert set(vd)==expected_visual,(vd,expected_visual)
for e in a['changes']:
    assert sha(resolve(e['source_path']))==e['source_sha256']
    assert e['candidate_comparison']['actual_candidate_finding'] is False
    ce=e['candidate_comparison']['candidate_evidence'];t=resolve(ce['path']).read_text()
    assert t[ce['start']:ce['end']]==ce['passage']
original_ledger=read(G/'source-audit-final-12-read-ledger.json')
assert a['original_source_reuse']['original_ledger_sha256']==sha(G/'source-audit-final-12-read-ledger.json')
original_inputs={e['path']:e['source_sha256'] for e in original_ledger['entries']}
expected,rows,complete_groups=[],l['new_text_deliveries'],{}
for e in rows:
    p=resolve(e['path']);assert sha(p)==e['source_sha256']
    t=p.read_text();assert len(t)==e['character_length']
    part=t[e['start']:e['end']]
    assert e['end']-e['start']<=6000 and e['truncated'] is False and e['output_cap']>=4000
    assert digest(part.encode())==e['slice_sha256']
    expected.append(part)
    if p==resolve('docs/quality/summary-qa/batches/'+B.name+'/source-preflight/spirit-island/living-faq-core-game.txt'):
        assert original_inputs[e['path']]==e['source_sha256']
    else:complete_groups.setdefault(str(p),[]).append((e['start'],e['end']))
assert len(rows)==51 and len(complete_groups)==3
for p,spans in complete_groups.items():
    cursor=0
    for start,end in sorted(spans):assert start<=cursor;cursor=max(cursor,end)
    assert cursor==len(Path(p).read_text())
views=l['new_card_views']+[l['additional_native_panel_view']]
assert len(l['new_card_views'])==33 and len(views)==34
assert len({e['source_sha256'] for e in views})==34
rt=Path(initial['runtime_path']);boundary=max(initial['actual_terminal_event_ordinals'])
matches=[[] for _ in rows];images=[];contexts=[];terminals=[];forbidden=[]
import re
marker=re.compile(r'get_agent_info|list_agents|read_thread|list_threads|send_message_to_thread|tools\.(?:web__run|web\.run)')
for n,line in enumerate(rt.open(),1):
    o=json.loads(line);v=o.get('payload',{})
    if not isinstance(v,dict):continue
    if o.get('type')=='turn_context':contexts.append({'ordinal':n,'model':v.get('model'),'effort':v.get('effort')})
    elif o.get('type')=='event_msg' and v.get('type')=='task_complete':terminals.append(n)
    elif n>boundary and o.get('type')=='event_msg' and v.get('type')=='item_completed':
        it=v.get('item',{})
        if it.get('type')=='CommandExecution':
            out=it.get('aggregated_output','');vals=list(strings(out))
            for i,part in enumerate(expected):
                if any(part in s for s in vals):matches[i].append({'ordinal':n,'record_sha256':digest(line.encode()),'exit_code':it.get('exit_code')})
    elif o.get('type')=='response_item':
        if v.get('type') in ('function_call','custom_tool_call'):
            s=str(v.get('name',''))+' '+str(v.get('input',v.get('arguments','')))
            if marker.search(s):forbidden.append({'ordinal':n,'markers':sorted(set(marker.findall(s)))})
        elif n>boundary and v.get('type') in ('function_call_output','custom_tool_call_output') and isinstance(v.get('output'),list):
            for i,z in enumerate(v['output']):
                if not isinstance(z,dict) or z.get('type')!='input_image':continue
                url=z.get('image_url');url=url.get('url') if isinstance(url,dict) else url
                data=base64.b64decode(url.split(';base64,',1)[1],validate=True)
                images.append({'ordinal':n,'block':i,'sha256':digest(data),'detail':z.get('detail')})
assert contexts and all(x['model']=='gpt-6.1-sol' and x['effort']=='high' for x in contexts)
assert not forbidden,forbidden
assert len(terminals)>=2,'The corrected audit has not yet reached its actual completed terminal.'
assert min(terminals)==boundary;end=max(terminals)
assert all(matches) and all(any(x['ordinal']<end for x in mm) for mm in matches)
bound=[]
for e in views:
    p=resolve(e['path']);h=sha(p);assert h==e['source_sha256']
    with Image.open(p) as im:assert list(im.size)==e['dimensions']
    assert e['detail_requested']==e['detail_forwarded']=='original' and e['resized'] is False and e['cropped'] is False
    actual=[x for x in images if x['sha256']==h and x['detail']=='original' and x['ordinal']<end]
    assert actual,str(p)
    bound.append({'path':str(p),'sha256':h,'dimensions':e['dimensions'],'actual_new_original_deliveries':actual})
supp=read(G/'supplemental-source-manifest-v4.json')
assert all(sha(resolve(e['path']))==e['sha256'] for e in supp['source_records'])
assert all(sha(resolve(p))==h for p,h in read(G/'source-manifest.json')['paths_and_sha256'].items())
proof={'verified':True,'checked_at_utc':datetime.now(timezone.utc).isoformat(),'checker_sha256':sha(Path(__file__)),'initial_delivery_proof':str(ip),'initial_delivery_proof_sha256':sha(ip),'same_initially_fresh_auditor':initial['auditor'],'actual_initial_spawn':initial['actual_initial_spawn'],'runtime_path':str(rt),'runtime_sha256_at_check':sha(rt),'all_actual_contexts_minimal':contexts,'original_terminal_ordinal':boundary,'corrected_terminal_ordinal':end,'audit_path':str(G/'source-audit-final-12-corrected.json'),'audit_sha256':sha(G/'source-audit-final-12-corrected.json'),'summary_sha256':new['candidate_sha256'],'current_canonical_matches':True,'original_artifacts_preserved':a['original_artifacts'],'exact_declared_main_report_changes':rd,'exact_declared_visual_manifest_changes':vd,'all94_original_source_delivery_rows_retained_exactly':True,'new_complete_own_artifact_files':3,'new_complete_own_artifact_ranges':49,'new_focused_FAQ_ranges':2,'new_actual_text_deliveries':[dict(e,actual_public_output_records=mm) for e,mm in zip(rows,matches)],'new33_complete_card_faces_and1_full_panel':bound,'all72_supplementals_and7_original_source_hashes_current':True,'source_only_followup_prompt':str(G/'source-audit12-own-card-observation-correction-prompt.txt'),'source_only_followup_prompt_sha256':sha(G/'source-audit12-own-card-observation-correction-prompt.txt'),'forbidden_agent_status_or_peer_thread_tool_markers':forbidden,'own_correction_addendum':str(ap),'own_correction_addendum_sha256':sha(ap),'corrected_visual_manifest':str(G/'source-audit-final-12-corrected-visual-manifest.json'),'corrected_visual_manifest_sha256':sha(G/'source-audit-final-12-corrected-visual-manifest.json'),'verdict':'PASS','findings':[],'limits':['Same initially fresh pure source auditor corrects own evidence notes, not another independent vote. Root read the full initial and source-only continuation prompts; no questions, keys, reader data or peer results were authorized.','All17 complete original text inputs94ranges and57 original images remain bound by the initial Root proof. Three own artifacts were newly reread completely49ranges; two focused FAQ entries supplement its previously complete file delivery.','All33 newly delivered complete native faces plus one2697x1797 Shadows front occur after the original audit terminal and before corrected terminal. No unverified first-draft chronology claim.','Current canonical is unchangedC23. Source and coverage acceptance do not replace the required first full173-question pair or later exact stamped-byte recheck.','No blind-reader, stamping, publication or game-goal completion approval.']}
out=B/'coordinator-checks/spirit-source12-corrected-actual-delivery.json';assert not out.exists();out.write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps({'verified':True,'texts':51,'new_card_faces':33,'new_full_panel':1,'current_body':new['candidate_sha256'],'verdict':'PASS','proof':str(out)},indent=2))
