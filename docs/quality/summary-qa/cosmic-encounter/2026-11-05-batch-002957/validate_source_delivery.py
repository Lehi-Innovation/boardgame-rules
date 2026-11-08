"""Compare saved source delivery declarations to actual model-visible runtime output.

Only hashes, paths, input ranges, image dimensions and runtime ordinals are saved.
No session instructions, account configuration or image base64 is copied.
"""
from pathlib import Path
import base64
import hashlib
import json
import sys
import argparse

R=Path(__file__).parent.resolve()
def sha(b): return hashlib.sha256(b).hexdigest()
def texts(x):
    if isinstance(x,str):
        yield x
        try:
            y=json.loads(x)
            if isinstance(y,(list,dict)):
                yield from texts(y)
                return
        except ValueError: pass
        # A capped outer response can preserve complete JSON lines around its
        # missing middle. Decode only lines that independently parse in full.
        if '\n' in x:
            for line in x.splitlines():
                if not line.startswith(('{','[')): continue
                try: y=json.loads(line)
                except ValueError: continue
                if isinstance(y,(list,dict)): yield from texts(y)
    elif isinstance(x,list):
        for item in x: yield from texts(item)
    elif isinstance(x,dict):
        for value in x.values(): yield from texts(value)
def jpeg_dimensions(data):
    assert data[:2]==b'\xff\xd8'
    i=2
    while i<len(data):
        while data[i]==255: i+=1
        marker=data[i];i+=1
        if marker in [0x01,0xd8,0xd9] or 0xd0<=marker<=0xd7: continue
        size=int.from_bytes(data[i:i+2],'big')
        if marker in [0xc0,0xc1,0xc2,0xc3,0xc5,0xc6,0xc7,0xc9,0xca,0xcb,0xcd,0xce,0xcf]:
            return [int.from_bytes(data[i+5:i+7],'big'),int.from_bytes(data[i+3:i+5],'big')]
        i+=size
    raise ValueError('No JPEG frame')

parser=argparse.ArgumentParser()
parser.add_argument('task')
parser.add_argument('receipt_name')
parser.add_argument('out_name')
parser.add_argument('--native-mode',choices=['fifty','none','selected'],default='fifty')
parser.add_argument('--native-source',action='append',default=[])
parser.add_argument('--text-mode',choices=['full','selected'],default='full')
parser.add_argument('--require-file',action='append',default=[])
args=parser.parse_args()
assert args.native_mode!='selected' or args.native_source
task,receipt_name,out_name=args.task,args.receipt_name,args.out_name
provenance=json.loads((R/'model-provenance.json').read_text())
agent=next(a for a in provenance['agents'] if a['task']==task)
receipt_path=R/receipt_name
receipt=json.loads(receipt_path.read_text())
records=[];images=[]
for index,raw in enumerate(Path(agent['runtime_source_path']).open()):
    row=json.loads(raw);p=row.get('payload',{})
    if p.get('type')!='custom_tool_call_output': continue
    ordinal=row.get('ordinal',index)
    proof={'record_ordinal':ordinal,'record_sha256':sha(raw.encode())}
    output=p.get('output')
    records.append((proof,list(texts(output))))
    if isinstance(output,list):
        for item in output:
            if not isinstance(item,dict) or item.get('type')!='input_image': continue
            url=item.get('image_url','')
            if not isinstance(url,str) or not url.startswith('data:image/jpeg;base64,'): continue
            data=base64.b64decode(url.split(',',1)[1],validate=True)
            images.append({**proof,'sha256':sha(data),'bytes':len(data),'dimensions':jpeg_dimensions(data),'forward_detail':item.get('detail')})

files=[]
declarations=receipt.get('text_input_proofs',receipt.get('text_receipts',receipt.get('inputs',receipt.get('source_text_delivery',{}).get('sources',[]))))
for declared in declarations:
    path=Path(declared.get('path',declared.get('file',declared.get('filepath'))));s=path.read_text();last=0;checks=[]
    for c in declared['chunks']:
        start,end=c.get('start_char',c.get('start_character',c.get('start'))),c.get('end_char_exclusive',c.get('end_character_exclusive',c.get('end_exclusive')));chunk=s[start:end]
        found=[proof for proof,contents in records if any(chunk in t for t in contents)]
        check={'start':start,'end':end,'characters':end-start,'contiguous':start==last,
               'bounded':0<end-start<=6000,'declared_hash_matches':c.get('utf8_chunk_sha256',c.get('utf8_sha256',c.get('sha256_utf8')))==sha(chunk.encode()),
               'exact_chunk_found_in_actual_model_visible_output':bool(found),'runtime_proof':found}
        checks.append(check);last=end
    result={'path':str(path),'sha256':sha(path.read_bytes()),'declared_full_hash_matches':declared.get('full_file_sha256',declared.get('full_sha256',declared.get('sha256')))==sha(path.read_bytes()),'characters':len(s),'complete':last==len(s) and all(c['contiguous'] for c in checks),'chunks':checks}
    result['assignment_text_mode']=args.text_mode
    result['pass']=(result['complete'] or args.text_mode=='selected') and result['declared_full_hash_matches'] and bool(checks) and all(c['bounded'] and c['declared_hash_matches'] and c['exact_chunk_found_in_actual_model_visible_output'] for c in checks)
    files.append(result)

manifest=R.parents[1]/'batches/2026-11-05-batch-002957/source-preflight/cosmic-encounter/original-alien-sheet-provenance.json'
assets=json.loads(manifest.read_text())['assets']
native=[]
assigned_assets=assets if args.native_mode=='fifty' else [a for a in assets if a['original_file'] in args.native_source] if args.native_mode=='selected' else []
if args.native_mode=='selected': assert len(assigned_assets)==len(set(args.native_source))
for a in assigned_assets:
    found=[x for x in images if x['sha256']==a['original_sha256'] and x['bytes']==a['expected_size'] and x['dimensions']==[a['width'],a['height']] and x['forward_detail']=='original']
    native.append({'alien':a['alien'],'source_path':a['original_file'],'pinned_sha256':a['original_sha256'],'pinned_bytes':a['expected_size'],'pinned_dimensions':[a['width'],a['height']],'matching_actual_model_visible_native_payloads':found,'pass':bool(found)})
report={'validator_version':4,'version_note':'Earlier versions preserved. Version4 adds explicit selected-range/selected-image assignments for narrow adjudications and own-review continuations. Defaults still require complete EOF delivery and all fifty native images; a selected-range proof never certifies full-file coverage. All exact chunks and assigned payloads must appear in actual runtime outputs.','task':task,'identity':agent['identity'],'actual_model_and_effort_verified':agent['settings_verified'],'receipt_path':str(receipt_path),'receipt_sha256':sha(receipt_path.read_bytes()),'native_manifest_sha256':sha(manifest.read_bytes()),'text_files':files,'native_original_images':native,'all_declared_text_delivery_verified':all(x['pass'] for x in files),'text_review_assignment':args.text_mode,'selected_range_limit':'Only explicit declared chunks are certified in selected mode; other keyword-hit/inspection claims and prior-reading reuse are assessed separately, not relabeled as new complete delivery.','native_review_assignment':args.native_mode,'all_fifty_native_images_verified':len(native)==50 and all(x['pass'] for x in native) if args.native_mode=='fifty' else None,'required_text_paths':args.require_file,'all_required_text_inputs_present':set(args.require_file).issubset({x['path'] for x in files}),'method':'Actual input_text and decoded input_image payloads in external runtime custom_tool_call_output; exact complete text chunks and assigned original JPEG hashes/bytes/dimensions/detail. Narrow specialists explicitly make no unassigned source/image claim. No hidden instructions or image bytes copied. Delivery establishes input availability, not semantic signoff.'}
report['all_assigned_native_images_verified']=len(native)==len(assigned_assets) and all(x['pass'] for x in native)
report['nonvacuous_input_proof']=bool(files) or bool(assigned_assets)
report['pass']=report['nonvacuous_input_proof'] and report['actual_model_and_effort_verified'] and report['all_declared_text_delivery_verified'] and report['all_required_text_inputs_present'] and report['all_assigned_native_images_verified']
dest=R/out_name
assert not dest.exists(),'Never replace historical validation'
dest.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print({'task':task,'text_files':len(files),'text_chunks':sum(len(x['chunks']) for x in files),'native_images':len(native),'pass':report['pass']})
