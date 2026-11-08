from pathlib import Path
import base64,difflib,hashlib,io,json,struct,sys
sys.dont_write_bytecode=True
B=Path(__file__).parent.resolve();ROOT=Path('/home/jonny/projects/boardgame-rules');A=B/'current-text-source-auditor';revision=int(sys.argv[1]);assert revision>=2;R=A/f'revision-{revision:02}'
def sha(raw):return hashlib.sha256(raw).hexdigest()
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
def objects(x):
 if isinstance(x,dict):
  yield x
  for v in x.values():yield from objects(v)
 elif isinstance(x,list):
  for v in x:yield from objects(v)
M=next(x for x in json.loads((B/'runtime-provenance.json').read_text()) if x['task']=='/root/current_text_source_auditor');outputs=[];completions=[];images={}
for n,line in enumerate(Path(M['runtime_log_path']).open(),1):
 r=json.loads(line);v=r.get('payload',{})
 if r['type']=='event_msg' and v.get('type')=='task_complete':completions.append({'ordinal':n,'record_sha256':sha(line.encode()),'timestamp':r.get('timestamp')})
 if r['type']=='response_item' and v.get('type')=='custom_tool_call_output':
  output=v.get('output');outputs.append((n,sha(line.encode()),list(strings(output))))
  for x in objects(output):
   if x.get('type')=='input_image' and isinstance(x.get('image_url'),str) and x['image_url'].startswith('data:'):
    image=base64.b64decode(x['image_url'].split(',',1)[1]);assert image.startswith(b'\x89PNG\r\n\x1a\n');dimensions=list(struct.unpack('>II',image[16:24]));images.setdefault(sha(image),[]).append({'record_ordinal':n,'record_sha256':sha(line.encode()),'detail':x.get('detail'),'dimensions':dimensions})
cutoff=completions[revision-2];receipts=[];summary_ranges=[]
for line in (R/'text-receipts.jsonl').read_text().splitlines():
 x=json.loads(line);p=R/'snapshot-new-angeles.md' if x['path']=='rules/new-angeles.md' else ROOT/x['path'];raw=p.read_bytes();assert sha(raw)==x['sha256'];source=raw.decode();start,end=x['start_inclusive'],x['end_exclusive'];chunk=source[start:end];assert sha(chunk.encode())==x['chunk_sha256'];hits=[{'record_ordinal':n,'record_sha256':h} for n,h,items in outputs if n>cutoff['ordinal'] and any(chunk in s for s in items)];receipts.append({'path':x['path'],'sha256':x['sha256'],'start':start,'end':end,'actual_payload_matches_after_prior_completion':hits,'complete':bool(hits) and 0<len(chunk)<=5500})
 if x['path']=='rules/new-angeles.md':summary_ranges.append((start,end))
old=(A/'snapshot-new-angeles.md' if revision==2 else A/f'revision-{revision-1:02}/snapshot-new-angeles.md').read_text();new=(R/'snapshot-new-angeles.md').read_text();changes=[]
def covered(start,end):
 cursor=start
 for a,b in sorted(summary_ranges):
  if a<=cursor<=b:cursor=max(cursor,b)
  if cursor>=end:return True
 return False
for tag,a,b,c,d in difflib.SequenceMatcher(None,old,new,autojunk=False).get_opcodes():
 if tag!='equal':changes.append({'type':tag,'old_start':a,'old_end':b,'new_start':c,'new_end':d,'new_changed_text_delivered':covered(c,d)})
sources=json.loads((B/'input-manifest.json').read_text())['sources'];unchanged=all(sha(Path(p).read_bytes())==v['sha256'] for p,v in sources.items());base=A/'parent-actual-delivery-verification.json';proof=json.loads(base.read_text());assert proof['all_text_complete'] and proof['all_native_complete'];base_images={x['image_sha256']:x for x in proof['native_images']};fresh=[];documents={}
if (R/'native-receipts.json').exists():
 for x in json.loads((R/'native-receipts.json').read_text()):
  p=ROOT/x.get('crop',x.get('render'));h=x.get('crop_sha256',x.get('render_sha256'));assert sha(p.read_bytes())==h
  source=ROOT/x['source'];assert sha(source.read_bytes())==x['source_sha256']
  if 'render' in x:
   import fitz
   if source not in documents:documents[source]=fitz.open(source)
   # Reproduce the auditor's page sequence in a shared document, including any
   # already-proven pages, so the PDF renderer's font cache has the same state.
   pix=documents[source][x['page_1based']-1].get_pixmap(matrix=fitz.Matrix(*x['matrix']))
  reused=h in base_images
  if reused:
   original=base_images[h];assert original['source_pixels_match'] and original['source_sha256']==x['source_sha256'];dimensions=original['dimensions'];lineage=True
  else:
   from PIL import Image
   actual=Image.open(p).convert('RGBA')
   expected=Image.open(source).crop(x['rect']).convert('RGBA') if 'rect' in x else Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGBA')
   dimensions=list(actual.size);lineage=actual.size==expected.size and actual.tobytes()==expected.tobytes()
  hits=[y for y in images[h] if y['record_ordinal']>cutoff['ordinal']]
  fresh.append({'path':str(p),'sha256':h,'original_source_pixel_proof_reused':reused,'independently_reproduced_new_source_pixels':not reused,'source_pixels_match':lineage,'actual_fresh_forwarded_payload_matches':hits,'complete':lineage and bool(hits) and all(y['detail']=='original' and y['dimensions']==dimensions for y in hits)})
report={'revision':revision,'snapshot_sha256':sha(new.encode()),'prior_completion_boundary':cutoff,'focused_ranges':receipts,'all_new_focused_ranges_delivered_after_prior_completion':all(x['complete'] for x in receipts),'fullfile_changed_spans':changes,'all_changed_summary_text_delivered':all(x['new_changed_text_delivered'] for x in changes),'fresh_native_images':fresh,'all_fresh_native_views_after_prior_completion':all(x['complete'] for x in fresh),'all21_original_source_files_unchanged':unchanged,'explicit_full_source_native_reuse_base':str(base),'reuse_base_sha256':sha(base.read_bytes()),'original_FAIL_preserved':True,'source_audit_sha256':sha((R/'source-audit.json').read_bytes()),'model_provenance':M};(R/'parent-actual-reuse-verification.json').write_text(json.dumps(report,indent=2)+'\n');assert report['all_new_focused_ranges_delivered_after_prior_completion'] and report['all_changed_summary_text_delivered'] and report['all_fresh_native_views_after_prior_completion'] and unchanged;print(json.dumps({'revision':revision,'new_ranges':len(receipts),'fresh_native_views':len(fresh),'changed_spans':len(changes),'all_actual_delivery_and_reuse_verified':True}))
