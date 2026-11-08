"""Verify actual full-size pixels and original detail in same-origin continuation."""
from pathlib import Path
import base64
import hashlib
import io
import json
import re
from PIL import Image
from collections import defaultdict
from verify_runtime_delivery import log_for

ROOT=Path(__file__).resolve().parent
D=ROOT/'source-audit-09'
def sha(b):return hashlib.sha256(b).hexdigest()
def pixel_identity(image):
    im=image.convert('RGBA')
    return (im.size,sha(im.tobytes()))
inp=json.loads((D/'source-only-original-image-completion-input.json').read_text())
report=D/'source-audit-completed.json'
x=json.loads(report.read_text())
assert len(inp['images'])==41
assert sha(Path(inp['summary_path']).read_bytes())==inp['summary_sha256']
assert sha(Path(inp['source_manifest_path']).read_bytes())==inp['source_manifest_sha256']
expected=[]
for r in inp['images']:
    p=Path(r['image_path']);b=p.read_bytes();im=Image.open(io.BytesIO(b))
    assert sha(b)==r['image_sha256'] and list(im.size)==r['original_dimensions']
    assert sha(Path(r['source_path']).read_bytes())==r['source_sha256']
    expected.append((r,pixel_identity(im)))
log=log_for('/root/pure_source_auditor_09');calls={};frames=[];initial=[];completed=[];contexts=[];text_outputs=[]
for n,line in enumerate(log.open(),1):
    rec=json.loads(line);p=rec.get('payload',{});typ=p.get('type');rh=sha(line.encode())
    if rec.get('type')=='turn_context':
        contexts.append({'ordinal':n,'actual_model':p.get('model'),'actual_effort':p.get('effort'),'record_sha256':rh})
    if typ in ['custom_tool_call','function_call']:
        code=p.get('input',p.get('arguments',''))
        calls[p.get('call_id')]={'ordinal':n,'code':code,'record_sha256':rh}
        if ('write_text' in code or 'writeFile' in code):
            if 'source-audit-completed.json' in code:completed.append(n)
            elif 'source-audit.json' in code:initial.append(n)
    if typ in ['custom_tool_call_output','function_call_output'] and isinstance(p.get('output'),list):
        for index,v in enumerate(p['output']):
            if isinstance(v,dict) and v.get('type')=='input_image':
                b=base64.b64decode(v['image_url'].split(',',1)[1]);im=Image.open(io.BytesIO(b))
                frames.append({'ordinal':n,'call_id':p.get('call_id'),'output_index':index,'record_sha256':rh,'detail':v.get('detail'),'dimensions':list(im.size),'encoded_image_sha256':sha(b),'pixel_identity':pixel_identity(im)})
    if typ in ['custom_tool_call_output','function_call_output']:
        output=p.get('output')
        if isinstance(output,str):text_outputs.append((n,output,rh))
        elif isinstance(output,list):
            text_outputs.extend((n,v['text'],rh) for v in output if isinstance(v,dict) and isinstance(v.get('text'),str))
assert initial and completed
start=min(initial);cut=min(completed)
actual=[f for f in frames if start<f['ordinal']<cut]
assert len(actual)==45,len(actual)
assert contexts and all(r['actual_model']=='gpt-6.1-sol' and r['actual_effort']=='high' for r in contexts)
assert x['verdict']=='PASS' and x['findings']==[]
assert x['summary_snapshot_sha256']==inp['summary_sha256']
assert x['source_manifest_sha256']==inp['source_manifest_sha256']
assert x['independent_input_declaration']['source_only'] is True
assert x['independent_input_declaration']['same_initially_fresh_auditor']=='/root/pure_source_auditor_09'
assert x['independent_input_declaration']['no_question_bank_maps_readers_grades_peer_qa_history_web_or_other_agent_status'] is True
assert x['initial_reading_reuse']['disclosed'] is True
assert x['initial_reading_reuse']['preserved_initial_report_sha256']==sha((D/'source-audit.json').read_bytes())
assert len(x['native_view_receipts'])==41
receipts={r['image_path']:r for r in x['native_view_receipts']}
assert set(receipts)=={r['image_path'] for r in inp['images']}
bindings=[];used=set();capped=[]
def bind_frame(r,identity):
    matches=[(i,f) for i,f in enumerate(actual) if f['pixel_identity']==identity]
    assert len(matches)==1,(r['image_path'],len(matches))
    index,frame=matches[0];assert index not in used;used.add(index)
    assert frame['detail']=='original',(r['image_path'],frame['detail'])
    assert frame['dimensions']==r['original_dimensions']
    call=calls[frame['call_id']]
    assert call['ordinal']<frame['ordinal']<cut
    assert 'tools.view_image' in call['code']
    assert re.search(r'image\([^;]*?,\s*[\'\"]original[\'\"]\s*\)',call['code']),call['ordinal']
    return {**r,'actual_image':{k:v for k,v in frame.items() if k!='pixel_identity'},'full_decoded_RGBA_pixels_identical':True,'decoded_pixel_sha256':identity[1],'actual_call_ordinal':call['ordinal'],'actual_call_record_sha256':call['record_sha256']}
for r,identity in expected:
    receipt=receipts[r['image_path']]
    assert receipt['image_sha256']==r['image_sha256'] and receipt['original_dimensions']==r['original_dimensions']
    if receipt.get('whole_image_transport_cap'):
        capped.append(r);continue
    bindings.append(bind_frame(r,identity))
assert len(bindings)==39 and len(capped)==2
tile_groups=defaultdict(list);tile_bindings=[]
assert len(x['supplemental_full_resolution_tile_receipts'])==4
for r in x['supplemental_full_resolution_tile_receipts']:
    p=Path(r['image_path']);source=Path(r['source_path']);tile=Image.open(p);source_image=Image.open(source)
    assert sha(p.read_bytes())==r['sha256'] and sha(source.read_bytes())==r['source_sha256']
    assert list(tile.size)==r['original_dimensions']
    assert pixel_identity(source_image.crop(r['source_pixel_bbox']))==pixel_identity(tile)
    tile_groups[str(source)].append(r['source_pixel_bbox'])
    tile_bindings.append(bind_frame(r,pixel_identity(tile)))
for r in capped:
    width,height=r['original_dimensions'];boxes=tile_groups[r['image_path']]
    # Exact full-width contiguous partition proves no source pixel is absent.
    assert len(boxes)==2
    ordered=sorted(boxes,key=lambda b:b[1]);assert ordered[0][1]==0 and ordered[-1][3]==height
    assert all(b[0]==0 and b[2]==width for b in boxes)
    assert ordered[0][3]==ordered[1][1]
    receipt=receipts[r['image_path']]
    matches=[(i,f) for i,f in enumerate(actual) if i not in used and f['dimensions']==receipt['transport_delivered_dimensions']]
    assert len(matches)==1
    index,frame=matches[0];used.add(index);call=calls[frame['call_id']]
    assert Path(r['image_path']).name in call['code']
    assert frame['detail']=='original' and 'tools.view_image' in call['code']
    assert re.search(r'image\([^;]*?,\s*[\'\"]original[\'\"]\s*\)',call['code'])
assert len(used)==len(actual)==45
source_input=D/'source-only-original-image-completion-input.json'
text=source_input.read_text();receipt=x['completion_input']
assert receipt['sha256']==sha(source_input.read_bytes()) and receipt['character_count']==len(text)
cursor=0;delivery=[]
for a,b in receipt['ranges']:
    assert a==cursor and 0<b-a<=6000;cursor=b;s=text[a:b]
    matches=[]
    for ordinal,output,rh in text_outputs:
        if not start<ordinal<cut:continue
        transport='literal' if s in output else None
        encoded=json.dumps(s,ensure_ascii=False)[1:-1]
        if not transport and encoded in output and json.loads('"'+encoded+'"')==s:transport='complete_JSON_escaped_literal'
        if transport:matches.append({'ordinal':ordinal,'record_sha256':rh,'transport':transport})
    assert matches,(a,b)
    delivery.append({'range':[a,b],'slice_sha256':sha(s.encode()),'actual_outputs':matches})
assert cursor==len(text)
out={'validation':'PASS','report_path':str(report),'report_sha256':sha(report.read_bytes()),'runtime_source':str(log),'task':'/root/pure_source_auditor_09','actual_model_records':contexts,'initial_report_first_write_ordinal':start,'completed_report_first_write_ordinal':cut,'fresh_native_deliveries':45,'original_detail_whole_image_payloads':41,'full_size_pixel_identical_whole_images':39,'capped_whole_image_overviews':2,'full_resolution_pixel_identical_tiles':4,'all_9_species_fronts_and_faderan_reverse_whole_original_pixels':True,'all_45_image_payloads_original_detail':True,'every_mandatory_original_pixel_delivered_before_completed_report':True,'capped_image_coverage':'Two exact full-width contiguous lossless tiles per capped source; all source pixels and dimensions checked independently','source_input_path':str(source_input),'source_input_sha256':sha(source_input.read_bytes()),'new_complete_input_actual_delivery':delivery,'bindings':bindings,'tile_bindings':tile_bindings,'limits':'Proves actual original-detail image payload dimensions and full decoded pixel equality for39 whole source/render images and four tiles covering every pixel of the other two sources. The two capped whole-image overviews are not claimed full size. Initial report/images remain historical; prior hash-identical text-reading reuse disclosed separately. No private session objects copied.'}
dest=D/'runtime-original-resolution-completion.json';assert not dest.exists();dest.write_text(json.dumps(out,indent=2)+'\n')
print('Source09 same-origin completion:39 full-size whole images +4 lossless tiles cover all41 mandatory originals;45 original-detail deliveries PASS')
