"""Accept the original pure source15 audit with its preserved own-source correction."""
import ast
import base64
import hashlib
import io
import json
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image

B=Path(__file__).resolve().parent; R=B.parents[4]
G=R/'docs/quality/summary-qa/spirit-island'/B.name
J=lambda p:json.loads(p.read_text())
HB=lambda b:hashlib.sha256(b).hexdigest()
H=lambda p:HB(p.read_bytes())
resolve=lambda p:(R/p).resolve()
tree=ast.parse((B/'check-spirit-source09-delivery.py').read_text())
fn=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='strings')
ns={'json':json};exec(compile(ast.Module(body=[fn],type_ignores=[]),'<strings>','exec'),ns)
a=J(G/'source-audit-final-15.json');v=J(G/'source-audit-final-15-visual-manifest.json')
original=J(G/'source-audit15-original-freeze.json')
addpath=G/'source-audit15-own-source-dissolve-addendum.json';add=J(addpath)
ledgerpath=G/'source-audit15-own-source-dissolve-addendum-read-view-ledger.json';ledger=J(ledgerpath)
freeze=J(G/'source-audit15-own-source-addendum-original-freeze.json')
delivery=J(B/'coordinator-checks/spirit-source-audit-final-15-actual-delivery.json')
assert delivery['verified'] and a['verdict']=='PASS' and not a['findings'] and not a['unresolved_findings']
assert H(G/'source-candidate-26.md')==a['candidate_sha256']==H(R/'rules/spirit-island.md')=='ce8f1d645f466686ae2e75fcd29130fa89cbb1c4963d981090e3768a526a6fd1'
for name,x in original['files'].items():
    assert H(G/name)==x['sha256']==H(Path(x['original_completed_copy']))==add['artifact_preservation']['original_hashes'][name]
for name,x in freeze['files'].items():
    assert H(G/name)==x['sha256']==H(Path(x['immutable_copy']))
assert add['reconciliation_status']=='CORRECTED_OWN_OBSERVATION'
assert add['precise_printed_replacements']==[
    {'source_piece':'City','source_count':1,'destination_piece':'Explorer','destination_count':2},
    {'source_piece':'Town','source_count':1,'destination_piece':'Explorer','destination_count':1},
    {'source_piece':'Dahan','source_count':1,'destination_piece':'Explorer','destination_count':1}]
boundary=J(G/'source-audit15-original-completed-runtime-boundary.json')
runtime=Path(boundary['session_path'])
with runtime.open('rb') as stream:
    old=stream.read(boundary['prefix_bytes']);assert HB(old)==boundary['prefix_sha256']
    newlines=stream.read().splitlines(keepends=True)
outputs=[];images=[];contexts=[];writes=[];ends=[];calls=[]
for n,line in enumerate(newlines,boundary['record_count']+1):
    row=json.loads(line);p=row.get('payload',{})
    if row.get('type')=='turn_context':contexts.append((p.get('model'),p.get('effort')))
    if row.get('type')=='event_msg' and p.get('type')=='task_complete':ends.append(n)
    if row.get('type')=='event_msg' and p.get('type')=='item_completed':
        item=p.get('item',{})
        if item.get('type')=='CommandExecution':outputs.append((n,HB(line),list(ns['strings'](item.get('aggregated_output','')))))
    if row.get('type')!='response_item':continue
    typ=p.get('type')
    if typ in ['function_call','custom_tool_call']:
        code=p.get('input',p.get('arguments',''))
        assert not any(s in code for s in ['questions.json','answer-key.json','asked-fact-map.json','coverage-review','reader-a.json','reader-b.json','/sessions/'])
        calls.append({'record':n,'name':p.get('name'),'record_sha256':HB(line)})
        if addpath.name in code and 'write_text' in code:writes.append(n)
    if typ in ['function_call_output','custom_tool_call_output']:
        outputs.append((n,HB(line),list(ns['strings'](p.get('output')))))
        if isinstance(p.get('output'),list):
            for x in p['output']:
                if not isinstance(x,dict) or x.get('type')!='input_image':continue
                url=x['image_url'];url=url.get('url') if isinstance(url,dict) else url
                data=base64.b64decode(url.split(';base64,',1)[1],validate=True)
                images.append({'record':n,'record_sha256':HB(line),'sha256':HB(data),'detail':x.get('detail'),'data':data})
assert ends and writes and contexts and all(x==('gpt-6.1-sol','high') for x in contexts)
cutoff=min(writes);reads=[];cursor=0
for e in ledger['source_delivery']:
    path=resolve(e['path']);text=path.read_bytes().decode('utf-8');a0,z=e['start'],e['end']
    assert H(path)==e['source_sha256'] and a0==cursor and a0<z<=len(text) and HB(text[a0:z].encode())==e['slice_sha256']
    matched=[{'record':n,'record_sha256':h} for n,h,vals in outputs if n<cutoff and any(text[a0:z] in s for s in vals)]
    assert matched
    reads.append(dict(e,actual_outputs=matched));cursor=z
assert cursor==ledger['source_completion']['character_length']
views=[]
for e in ledger['image_delivery']:
    path=resolve(e['path']);assert H(path)==e['source_sha256']
    hits=[x for x in images if x['sha256']==H(path) and x['record']<cutoff and x['detail']=='original'];assert hits
    views.append({'path':str(path),'sha256':H(path),'actual_original_deliveries':[{k:v for k,v in x.items() if k!='data'} for x in hits]})
primary=resolve(add['primary_source']['path'])
assert H(primary)==add['primary_source']['source_sha256']=='92a29d653e305f8fa839c822d8b92b1298298f721c4de787ca9a017d399cedd9'
with Image.open(primary) as im:
    expected=im.resize((1800,2520),Image.Resampling.NEAREST)
    diagnostic=next(x for x in images if x['sha256']==ledger['image_delivery'][1]['source_sha256'])
    with Image.open(io.BytesIO(diagnostic['data'])) as got:assert expected.mode==got.mode and expected.size==got.size and expected.tobytes()==got.tobytes()
refs=[];nativepaths={resolve(x['path']) for x in v['images']}
for group in a['checked_groups']:
    assert group['result']=='consistent'
    for q in group['sources']:
        path=resolve(q['path']);assert H(path)==q['source_sha256']
        if all(k in q for k in ['start','end','passage']):
            texts=[path.read_bytes().decode('utf-8'),path.read_text()]
            assert any(t[q['start']:q['end']]==q['passage'] for t in texts)
            refs.append({'path':str(path),'sha256':H(path),'start':q['start'],'end':q['end']})
    for q in group['visual_sources']:
        assert resolve(q['path']) in nativepaths and H(resolve(q['path']))==q['source_sha256']
pins=J(G/'supplemental-source-manifest-v4.json')['source_records']
assert len(pins)==len(a['supplemental_record_reconciliation'])==72
for row in a['supplemental_record_reconciliation']:
    pin=pins[row['record_index']];assert resolve(row['path'])==resolve(pin['path']) and row['source_sha256']==pin['sha256']
proof={'verified':True,'checked_at_utc':datetime.now(timezone.utc).isoformat(),'summary_sha256':H(G/'source-candidate-26.md'),'original_audit_sha256':H(G/'source-audit-final-15.json'),'original_three_file_freeze_rechecked':True,'addendum_path':str(addpath),'addendum_sha256':H(addpath),'addendum_original_freeze_rechecked':True,'same_original_auditor':delivery['auditor'],'new_actual_text_ranges':reads,'new_original_and_diagnostic_views':views,'diagnostic_pixels_independently_reproduced_6x_nearest':True,'actual_new_contexts':contexts,'actual_new_completed_turn_records':ends,'new_public_call_trace':calls,'all23_groups_and57_original_visual_notes_read':True,'exact_primary_checked_group_passages':refs,'all72_exact_supplemental_members_reconciled':True,'semantic_acceptance':'Original pure15 PASS accepted with explicit evidentiary correction of image41. Printed mappings are City2Explorers/Town1Explorer/Dahan1Explorer. Candidate asserts neither wrong mapping; its actual Push distribution and pre-Push simultaneous threshold procedure remain accurate. Original mistake is preserved, corrected by the same auditor from primary pixels, and qualified in the Core card group; no new vote, guide change, question or coverage quota.','verdict':'PASS','limits':['Exact C26 source accuracy only; full173 blind trials and actual stamping/publication remain separate.','Original full candidate/source reading is reused honestly for the narrow own-source continuation; only seven own-note ranges and two views are new.','No questions, keys, maps, readers, grades or peer QA were supplied to this initially fresh pure auditor.']}
out=B/'coordinator-checks/spirit-C26-source15-own-correction-and-semantic-acceptance.json';assert not out.exists();out.write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps({'verified':True,'groups':len(a['checked_groups']),'exact_primary_passages':len(refs),'new_ranges':len(reads),'new_views':len(views),'proof':str(out)}))
