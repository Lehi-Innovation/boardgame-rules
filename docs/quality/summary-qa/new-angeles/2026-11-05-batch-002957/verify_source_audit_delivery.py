"""Independently verify exact text and actual native image payload delivery."""
from pathlib import Path
import base64, hashlib, io, json, sys
sys.dont_write_bytecode=True
from PIL import Image
import fitz
B=Path(__file__).parent.resolve();ROOT=Path('/home/jonny/projects/boardgame-rules')
A=B/'current-text-source-auditor'
meta=next(x for x in json.loads((B/'runtime-provenance.json').read_text()) if x['task']=='/root/current_text_source_auditor')
def sha(raw):return hashlib.sha256(raw).hexdigest()
def walk(x):
    if isinstance(x,dict):
        yield x
        for v in x.values():yield from walk(v)
    elif isinstance(x,list):
        for v in x:yield from walk(v)
def strings(x):
    if isinstance(x,str):
        yield x
        if x[:1] in ['{','[']:
            try:yield from strings(json.loads(x))
            except (ValueError,TypeError):pass
    elif isinstance(x,list):
        for y in x:yield from strings(y)
    elif isinstance(x,dict):
        for k,y in x.items():
            if k not in ['encrypted_content','internal_chat_message_metadata_passthrough']:yield from strings(y)
texts=[];images={}
for ordinal,line in enumerate(Path(meta['runtime_log_path']).open(),1):
    r=json.loads(line);v=r.get('payload',{})
    if r['type']!='response_item' or v.get('type')!='custom_tool_call_output':continue
    output=v.get('output');record={'record_ordinal':ordinal,'record_sha256':sha(line.encode())}
    texts.append((record,list(strings(output))))
    for x in walk(output):
        if x.get('type')=='input_image' and isinstance(x.get('image_url'),str) and x['image_url'].startswith('data:'):
            raw=base64.b64decode(x['image_url'].split(',',1)[1]);im=Image.open(io.BytesIO(raw))
            images.setdefault(sha(raw),[]).append({**record,'detail':x.get('detail'),'dimensions':list(im.size)})
text_checks=[]
for line in (A/'text-receipts.jsonl').read_text().splitlines():
    x=json.loads(line);p=ROOT/x['path']
    if x['path']=='rules/new-angeles.md':p=A/'snapshot-new-angeles.md'
    raw=p.read_bytes();assert sha(raw)==x['sha256'];text=raw.decode();start,end=x['start_inclusive'],x['end_exclusive'];chunk=text[start:end]
    assert sha(chunk.encode())==x['chunk_sha256']
    matches=[r for r,items in texts if any(chunk in s for s in items)]
    text_checks.append({'path':x['path'],'source_sha256':x['sha256'],'start':start,'end':end,'chars':len(chunk),'matches':matches,'complete':bool(matches) and len(chunk)<=5500})
native_checks=[];pdf_documents={}
for x in json.loads((A/'native-receipts.json').read_text()):
    source=Path(x['source']);source=source if source.is_absolute() else ROOT/source
    assert sha(source.read_bytes())==x['source_sha256']
    target=ROOT/x.get('crop',x.get('render'));raw=target.read_bytes();expected=x.get('crop_sha256',x.get('render_sha256'));assert sha(raw)==expected
    actual=Image.open(target).convert('RGBA')
    if 'rect' in x:
        original=Image.open(source).crop(x['rect']).convert('RGBA')
    else:
        if source not in pdf_documents:pdf_documents[source]=fitz.open(source)
        doc=pdf_documents[source];pix=doc[x['page_1based']-1].get_pixmap(matrix=fitz.Matrix(*x['matrix']),alpha=False);original=Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGBA')
    lineage=actual.size==original.size and actual.tobytes()==original.tobytes();matches=images.get(expected,[])
    native_checks.append({'source':str(source),'source_sha256':x['source_sha256'],'image_path':str(target),'image_sha256':expected,'dimensions':list(actual.size),'source_pixels_match':lineage,'actual_forwarded_image_matches':matches,'complete':lineage and bool(matches) and all(m['detail']=='original' and m['dimensions']==list(actual.size) for m in matches)})
report={'task':meta['task'],'runtime_log_path':meta['runtime_log_path'],'audited_snapshot_sha256':sha((A/'snapshot-new-angeles.md').read_bytes()),'text_chunks':text_checks,'native_images':native_checks,'all_text_complete':all(x['complete'] for x in text_checks),'all_native_complete':all(x['complete'] for x in native_checks),'runtime_objects_copied':False,'pdf_render_method':'Reuse each PDF document and original page-render sequence, matching auditor batch. Opening each page in a fresh document changed746 antialiasing pixels on LTPp14; original sequence reproduces exact pixels. Actual delivered image hash already matched throughout.'}
(A/'parent-actual-delivery-verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'text_chunks':len(text_checks),'native_images':len(native_checks),'text_complete':report['all_text_complete'],'native_complete':report['all_native_complete']}))
assert report['all_text_complete'] and report['all_native_complete']
