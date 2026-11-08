"""Verify the pure auditor's original-image completion without exporting private context."""
from pathlib import Path
from datetime import datetime, timezone
import base64
import hashlib
import io
import json
from PIL import Image

B=Path(__file__).resolve().parent
REPO=B.parents[4]
R=REPO/'docs/quality/summary-qa/sidereal-confluence'/B.name
D=R/'source-audit-09'
def load(p):return json.loads(p.read_text())
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for x in iter(lambda:f.read(1024*1024),b''):h.update(x)
    return h.hexdigest()
def digest(b):return hashlib.sha256(b).hexdigest()

prior_path=B/'coordinator-checks/sidereal-source-audit-09-actual-delivery.json'
prior=load(prior_path)
assert prior['verified']
assert sha(Path(prior['audit_path']))==prior['audit_sha256'],'Preserve the original audit report'
report_path=D/'source-audit-completed.json'
report=load(report_path)
assert report['verdict']=='PASS' and not report['findings']
current=sha(REPO/'rules/sidereal-confluence.md')
assert current==prior['summary_sha256']=='eb091e5288b379afe914cb89f64d9590c6c9242f05e0843d34cd347311fe348f'
summary_claims=[report.get(k) for k in ['summary_snapshot_sha256','summary_sha256','candidate_sha256'] if report.get(k)]
assert summary_claims and all(x==current for x in summary_claims)
assert (R/'full-iteration-09/summary-snapshot.md').read_bytes()==(REPO/'rules/sidereal-confluence.md').read_bytes()
for x in prior['text_checks']:assert sha(Path(x['path']))==x['sha256']
for x in prior['source_hashes']:assert sha(Path(x['path']))==x['sha256']
expected={}
for x in prior['native_checks']:
    p=Path(x['path']);assert sha(p)==x['sha256']
    with Image.open(p) as im:size=list(im.size)
    expected.setdefault(x['sha256'],[]).append({'path':str(p),'sha256':x['sha256'],'dimensions':size})
assert sum(map(len,expected.values()))==41
source_images=expected.copy()
tile_groups={}
for x in report.get('supplemental_full_resolution_tile_receipts',[]):
    source=Path(x['source_path']);tile=Path(x['image_path'])
    assert sha(source)==x['source_sha256'] and sha(tile)==x['sha256']
    assert x['source_sha256'] in source_images
    box=x['source_pixel_bbox']
    with Image.open(source) as original,Image.open(tile) as part:
        cropped=original.crop(box)
        assert cropped.mode==part.mode and cropped.size==part.size and cropped.tobytes()==part.tobytes()
        assert list(part.size)==x['original_dimensions']
    tile_groups.setdefault(x['source_sha256'],[]).append(x)
    expected.setdefault(x['sha256'],[]).append({'path':str(tile),'sha256':x['sha256'],'dimensions':x['original_dimensions'],
        'source_parent':str(source),'source_parent_sha256':x['source_sha256'],'exact_original_pixel_bbox':box})
for parent_hash,tiles in tile_groups.items():
    width,height=source_images[parent_hash][0]['dimensions'];cursor=0
    for x in sorted(tiles,key=lambda x:x['source_pixel_bbox'][1]):
        left,top,right,bottom=x['source_pixel_bbox']
        assert left==0 and right==width and top==cursor and top<bottom<=height
        cursor=bottom
    assert cursor==height
    # The two oversized complete frames hit an actual transport cap. Their
    # exact nonoverlapping raster tiles deliver every original source pixel.
    del expected[parent_hash]
assert len(tile_groups)==2 and len(report['supplemental_full_resolution_tile_receipts'])==4
runtime=Path(prior['runtime_path'])
matched={h:[] for h in expected};contexts=[];terminal=[];calls={};writer_candidates=[]
runtime_hash=hashlib.sha256()
for n,line in enumerate(runtime.open('rb'),1):
    runtime_hash.update(line)
    o=json.loads(line);p=o.get('payload',{})
    if not isinstance(p,dict):continue
    if o.get('type')=='session_meta':identity={k:p.get(k) for k in ['id','parent_thread_id','agent_path']}
    elif o.get('type')=='turn_context':contexts.append({'ordinal':n,'model':p.get('model'),'effort':p.get('effort')})
    elif o.get('type')=='event_msg' and p.get('type')=='task_complete':terminal.append(n)
    elif o.get('type')=='response_item':
        typ=p.get('type')
        if typ in ['function_call','custom_tool_call']:
            name=p.get('name','');body=p.get('input',p.get('arguments',''))
            assert isinstance(body,str)
            assert not any(x in body for x in ['questions.json','answer-key.json','asked-facts.json','reader-a.json','reader-b.json','grades-block-','results.json','source-audit-06/','source-audit-07/','source-audit-08/'])
            assert not any(x in name for x in ['collaboration','spawn_agent','read_thread','list_agents','wait_threads'])
            calls[p.get('call_id')]={'ordinal':n,'name':name,'body_sha256':digest(body.encode())}
            if 'source-audit-completed.json' in body and any(x in body for x in ['write_text','writeFile','apply_patch','json.dump']):writer_candidates.append(n)
        elif typ in ['function_call_output','custom_tool_call_output'] and isinstance(p.get('output'),list):
            for i,block in enumerate(p['output']):
                if not isinstance(block,dict) or block.get('type')!='input_image':continue
                url=block.get('image_url');url=url.get('url') if isinstance(url,dict) else url
                assert isinstance(url,str) and ';base64,' in url
                data=base64.b64decode(url.split(';base64,',1)[1],validate=True);h=digest(data)
                if h not in expected or n<=prior['first_report_write_record']:continue
                with Image.open(io.BytesIO(data)) as im:size=list(im.size)
                assert all(size==x['dimensions'] for x in expected[h])
                assert block.get('detail')=='original'
                call=calls[p['call_id']];assert call['ordinal']<n
                matched[h].append({'raw_runtime_ordinal':n,'block_index':i,'bytes_sha256':h,'bytes':len(data),'dimensions':size,'detail':block['detail'],'call':call})
assert identity=={'id':'01a1b3bc-f76d-7043-9e8b-fbc09eb8ba75','parent_thread_id':'01a1b0b3-0030-70b2-8947-7a940fdf364f','agent_path':'/root/pure_source_auditor_09'}
assert contexts and all(x['model']=='gpt-6.1-sol' and x['effort']=='high' for x in contexts)
assert all(matched.values()),[expected[h] for h,v in matched.items() if not v]
assert len(terminal)>=2,'The same-origin completion task has not finished'
completion=max(terminal)
assert all(any(x['raw_runtime_ordinal']<completion for x in v) for v in matched.values())
latest_inputs=max(min(x['raw_runtime_ordinal'] for x in v) for v in matched.values())
valid_writers=[n for n in writer_candidates if latest_inputs<n<completion]
assert valid_writers,'No completed-report write after all original-resolution images'
result={'verified':True,'checked_at_utc':datetime.now(timezone.utc).isoformat(),'checker_sha256':sha(Path(__file__)),'audit_path':str(report_path),'audit_sha256':sha(report_path),'summary_sha256':current,'verdict':'PASS','findings':[],'auditor':identity,'runtime_path':str(runtime),'runtime_sha256_at_check':runtime_hash.hexdigest(),'actual_turn_contexts_minimal':contexts,'initial_fresh_origin_model_fork_proof':prior['actual_initial_spawn'],'same_original_pure_auditor_source_only_continuation':True,'original_report_and_receipts_preserved':True,'prior_complete_text_and_source_delivery':{'path':str(prior_path),'sha256':sha(prior_path),'text_inputs':len(prior['text_checks']),'text_slices':sum(len(x['parts']) for x in prior['text_checks']),'all_sources_current_hashes_verified':True},'actual_original_image_deliveries':[dict(x,actual_original_deliveries=matched[h]) for h,paths in expected.items() for x in paths],'original_resolution_source_images':41,'direct_exact_original_file_deliveries':39,'oversized_source_files_completed_by_native_tiles':len(tile_groups),'native_tiles':4,'native_tile_pixel_unions_exactly_cover_sources':True,'native_tile_source_binding':tile_groups,'latest_required_original_image_output_ordinal':latest_inputs,'actual_completed_report_write_candidates_after_all_inputs':valid_writers,'actual_terminal_events':terminal,'limitations':['Prior original-resolution claims based only on named paths/counts are superseded by these exact decoded original-byte and dimension bindings.','Two oversized whole frames reached a transport cap even at original detail; their four exact raster tiles independently deliver every original pixel, with complete source coverage verified.','The same initially fresh source-only auditor reused its own unchanged complete text readings; this is a completion of one independent audit, not a second fresh context.','No reader score, question/key/map, coverage or publication approval follows from this transport proof alone.','No private runtime instruction, reasoning, profile, permission or account bodies were exported.']}
out=B/'coordinator-checks/sidereal-source09-completed-original-delivery.json'
assert not out.exists();out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'verified':True,'proof':str(out),'original_images':41,'text_files':len(prior['text_checks']),'source_only':True}))
