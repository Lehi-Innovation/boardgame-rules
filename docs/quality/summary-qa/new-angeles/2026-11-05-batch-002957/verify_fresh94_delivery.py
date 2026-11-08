"""Parent verification of actual fresh-review delivery and native pixel lineage."""
from pathlib import Path
import base64, hashlib, io, json, sys
sys.dont_write_bytecode = True
from PIL import Image
import fitz
B = Path(__file__).parent.resolve()
ROOT = Path('/home/jonny/projects/boardgame-rules')
A = B / 'coverage-fresh-final-94'
meta = next(x for x in json.loads((B/'runtime-provenance.json').read_text()) if x['task']=='/root/coverage_fresh_final_94')
def sha(raw): return hashlib.sha256(raw).hexdigest()
def walk(x):
    if isinstance(x,dict):
        yield x
        for k,v in x.items():
            if k not in ['encrypted_content','internal_chat_message_metadata_passthrough']: yield from walk(v)
    elif isinstance(x,list):
        for v in x: yield from walk(v)
def strings(x):
    if isinstance(x,str):
        yield x
        if x[:1] in ['{','[']:
            try: yield from strings(json.loads(x))
            except (ValueError,TypeError): pass
    elif isinstance(x,list):
        for v in x: yield from strings(v)
    elif isinstance(x,dict):
        for k,v in x.items():
            if k not in ['encrypted_content','internal_chat_message_metadata_passthrough']: yield from strings(v)
texts=[]; images={}; calls=[]
for ordinal,line in enumerate(Path(meta['runtime_log_path']).open(),1):
    r=json.loads(line);v=r.get('payload',{})
    receipt={'record_ordinal':ordinal,'record_sha256':sha(line.encode())}
    if r['type']=='response_item' and v.get('type') in ['function_call','custom_tool_call']:
        calls.append((receipt,v.get('name'),v.get('input',v.get('arguments',''))))
    if r['type']!='response_item' or v.get('type')!='custom_tool_call_output': continue
    output=v.get('output'); texts.append((receipt,list(strings(output))))
    for x in walk(output):
        if x.get('type')=='input_image' and isinstance(x.get('image_url'),str) and x['image_url'].startswith('data:'):
            raw=base64.b64decode(x['image_url'].split(',',1)[1]);im=Image.open(io.BytesIO(raw))
            images.setdefault(sha(raw),[]).append({**receipt,'detail':x.get('detail'),'dimensions':list(im.size)})
checks=[]
for line in (A/'unicode-range-receipts.jsonl').read_text().splitlines():
    x=json.loads(line);p=ROOT/x['file'];chunk=p.read_text()[x['start']:x['end']]
    assert sha(chunk.encode())==x['sha256_utf8']
    matches=[r for r,items in texts if any(chunk in s for s in items)]
    checks.append({**x,'actual_matches':matches,'verified':bool(matches) and len(chunk)<=5500})
inputs=json.loads((A/'input-manifest.json').read_text())
for x in inputs:
    assert sha((ROOT/x['file']).read_bytes())==x['sha256']
    ranges=sorted((c['start'],c['end']) for c in checks if c['file']==x['file'])
    assert ranges==[tuple(r) for r in x['ranges']]
    assert ranges[0][0]==0 and ranges[-1][1]==x['unicode_chars']
    assert all(l[1]==r[0] for l,r in zip(ranges,ranges[1:]))
native=[];docs={}
for x in json.loads((A/'native-manifest.json').read_text()):
    source=Path(x['source']);target=Path(x['output']);actual=Image.open(target).convert('RGB')
    assert sha(source.read_bytes())==x['source_sha256']
    assert sha(target.read_bytes())==x['output_sha256']
    if 'rectangles' in x:
        original=Image.new('RGB',tuple(x['output_dimensions'])); src=Image.open(source)
        for rect in x['rectangles']:
            crop=src.crop(rect['rect']);assert list(crop.size)==[rect['output_rect'][2]-rect['output_rect'][0],rect['output_rect'][3]-rect['output_rect'][1]]
            original.paste(crop,tuple(rect['output_rect'][:2]))
    else:
        if source not in docs: docs[source]=fitz.open(source)
        pix=docs[source][x['page_one_based']-1].get_pixmap(matrix=fitz.Matrix(x['scale'],x['scale']))
        original=Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB')
    lineage=actual.size==original.size and actual.tobytes()==original.tobytes()
    matches=images.get(x['output_sha256'],[])
    native.append({'id':x['id'],'source':str(source),'source_sha256':x['source_sha256'],'image_sha256':x['output_sha256'],'dimensions':list(actual.size),'source_pixels_match':lineage,'actual_matches':matches,'verified':lineage and bool(matches) and all(m['detail']=='original' and m['dimensions']==list(actual.size) for m in matches)})
# Inspect actual call text for evidence of forbidden channels. This negative scan
# supports the recorded tool boundary; it is not a semantic proof by itself.
forbidden=['list_agents','send_message_to_thread','read_thread','runtime-provenance','/sessions/','summary-snapshot','rules/new-angeles.md','expanded-luna-iteration','grading/','reader-a.json','reader-b.json']
boundary=[{'literal':s,'matches':[r for r,name,code in calls if s in code]} for s in forbidden]
report={'task':meta['task'],'model_provenance':meta,'text_ranges':checks,'native_images':native,'all_text_complete':len(checks)==61 and all(x['verified'] for x in checks),'all_native_complete':len(native)==67 and all(x['verified'] for x in native),'all16_original_atlases_used':len({x['source'] for x in native if not x['source'].endswith('.pdf')})==16,'tool_names':sorted(set(n for r,n,c in calls)),'forbidden_channel_literal_scan':boundary,'no_forbidden_channel_literal_matches':all(not x['matches'] for x in boundary),'runtime_objects_copied':False,'qualification':'Negative literal scan is corroborating boundary evidence; no raw session objects, instructions or image base64 are copied. Source authority limits remain open.'}
(A/'parent-actual-delivery-verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['all_text_complete','all_native_complete','all16_original_atlases_used','no_forbidden_channel_literal_matches']}))
assert report['all_text_complete'] and report['all_native_complete'] and report['all16_original_atlases_used'] and report['no_forbidden_channel_literal_matches']
