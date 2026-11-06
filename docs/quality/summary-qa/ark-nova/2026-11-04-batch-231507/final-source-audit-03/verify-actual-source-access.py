from pathlib import Path
import json,hashlib
Q=Path('docs/quality/summary-qa/ark-nova/2026-11-04-batch-231507');O=Q/'final-source-audit-03';R=json.loads((O/'report.json').read_text());RT=next(x for x in json.loads((Q/'runtime-provenance.json').read_text()) if x['session_meta']['agent_path']=='/root/final_source_audit03');H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();calls={};rawblocks={};visible={};imageblocks={}
for line in Path(RT['session_log_path']).read_text().splitlines():
 z=json.loads(line).get('payload',{})
 if z.get('type') in ['custom_tool_call','function_call']:calls[z['call_id']]=z.get('arguments') or z.get('input') or ''
 if z.get('type')=='custom_tool_call_output':
  blocks=[x for x in z.get('output',[]) if isinstance(x,dict)];texts=[x.get('text','') for x in blocks if x.get('type') in ['input_text','text']];rawblocks[z['call_id']]=texts;vals=texts.copy()
  for txt in texts:
   for row in txt.splitlines():
    try:a=json.loads(row)
    except json.JSONDecodeError:continue
    if isinstance(a,dict) and isinstance(a.get('output'),str):vals.append(a['output'])
  visible[z['call_id']]=vals
  imgs=[x for x in blocks if x.get('type') not in ['input_text','text']]
  if imgs:imageblocks[z['call_id']]=[{'type':x.get('type'),'keys':list(x),'content_sha256':hashlib.sha256(json.dumps(x,sort_keys=True).encode()).hexdigest()} for x in imgs]
checks=[]
def numbered(p,a,b,cid,label):
 ls=Path(p).read_text().splitlines();b=min(b,len(ls));expected='\n'.join(f'{i}: {ls[i-1]}' for i in range(a,b+1))+'\n';ok=any(expected in s for s in visible[cid]);checks.append({'input':label,'path':str(Path(p).resolve()),'start':a,'end':b,'call_id':cid,'exact_complete_numbered_text_visible':ok});return ok
snap=Q/'expanded-iteration-19/summary-snapshot.md';manifest=Q/'neutral-source-manifest.json';raw=Path('extracted/ark-nova-rules.txt')
manifest_ok=any(manifest.read_text() in s for s in visible['call_wBLCp35yDKJnCYP01OFpq0us'])
for a,b,cid in [(1,100,'call_nCXkYSlsdkb1Ao5F55T03lZ5'),(101,164,'call_nCXkYSlsdkb1Ao5F55T03lZ5'),(165,280,'call_fgsM5ZLwHinOpgcuB7dQMF2m'),(281,360,'call_nCXkYSlsdkb1Ao5F55T03lZ5'),(361,480,'call_u1BFR0iwNeeWZXIP7OyLzt1P'),(481,600,'call_12U1I8NZoybj8Et9Gkqypukf'),(601,717,'call_12U1I8NZoybj8Et9Gkqypukf')]:numbered(snap,a,b,cid,'summary')
for a,b,cid in [(1,230,'call_lYxwiFH2cqa0kszWXBv6ceNv'),(231,460,'call_Z9v6wvNha49uNtkhiBSxEBUQ'),(461,700,'call_tCJYosVRxhHSm8YoPjggH2G0'),(701,930,'call_4pBoLX94MF4Eg12zHXNG31Yw'),(931,1160,'call_LhpGnYb8nzv4btN0xVx9R7CR'),(1161,1370,'call_Wa8CgbFJfMPQiMeKuJpQzZkh'),(1371,1535,'call_FzpYOGhBnrpBjp1zTeLWt2DZ'),(1536,1735,'call_LIH6BWGnBPA5MkNBoZWlKlmD'),(1736,1898,'call_m6Pu98JEBhpyKML7FJSEJTfO')]:numbered(raw,a,b,cid,'raw source')
pdfgroups=[('ark-nova-rules',1,5,'call_nScq2kpNWRe6IeSAyKZHIYYB'),('ark-nova-rules',6,9,'call_tX950ogFEDrIzSoHgSvrgU8k'),('ark-nova-rules',10,13,'call_O0b1kRzJ81IEZFZdzB2hq1OL'),('ark-nova-rules',14,17,'call_rQmGzA3r8YUZbIbQMm5XjaSH'),('ark-nova-rules',18,20,'call_paEeIO4rNhpJOuPfui6VYp1b'),('ark-nova-glossary-rules',1,3,'call_mAViIOiwAFK16JyFFoZGYa7r'),('ark-nova-glossary-rules',4,6,'call_1vIN9Txo8YcdyfiIKyoWTW3V'),('ark-nova-glossary-rules',7,8,'call_DkmtIOg6UyObFZa6tsPSOo77'),('ark-nova-faq-rules',1,3,'call_DkmtIOg6UyObFZa6tsPSOo77'),('capstone-icon-overview',1,2,'call_kPZpdns6oGVMSGsNc9xzTbCq')]
for stem,a,b,cid in pdfgroups:
 for n in range(a,b+1):
  p=O/f'{stem}-p{n:02}.txt';numbered(p,1,len(p.read_text().splitlines()),cid,f'{stem} page{n} text')
views={}
def view(cid,paths):
 assert len(imageblocks.get(cid,[]))==len(paths),(cid,len(imageblocks.get(cid,[])),len(paths));views[cid]={'actual_image_blocks':len(imageblocks[cid]),'paths':[str(Path(p).resolve()) for p in paths],'image_hashes':[H(p) for p in paths],'actual_command_sha256':hashlib.sha256(calls[cid].encode()).hexdigest()}
for a,b,cid in [(1,4,'call_ybdPPa7NuT4T5UCCrxleXpcC'),(5,8,'call_I3l8vOjT28KZSh6IUfB4TWwk'),(9,12,'call_labC2iuLSW4Cgay0j1ugDQn9'),(13,16,'call_qxM6vqve3grbllbKqVZzCy97'),(17,20,'call_HxWmrTKkqqDeEVA2vTDTBQhh')]:view(cid,[O/f'ark-nova-rules-p{i:02}.png' for i in range(a,b+1)])
for a,b,cid in [(1,4,'call_rH7PjbmzcAmqm9OlySKkZA7A'),(5,8,'call_ytzKvk1ft26toeSR9YWUs1wq')]:view(cid,[O/f'ark-nova-glossary-rules-p{i:02}.png' for i in range(a,b+1)])
view('call_ZXTaNwQCHXc7VBgOb79zdkrA',[O/f'ark-nova-faq-rules-p{i:02}.png' for i in range(1,4)]+[O/f'capstone-icon-overview-p{i:02}.png' for i in range(1,3)])
view('call_XmVeeop9GWPjrsZrP6wyvCzP',[Q/'table-source-check/Spielzene.jpg',Q/'table-source-check/Back_arche_nova.jpg'])
view('call_fdwxZU4hx5hsZb5MAjTvF38X',[O/f'{x}.png' for x in ['photo-action-II','photo-action-I','photo-tracks','main-p15-projects','main-p02-final-card','main-p09-reputation']]);view('call_54R3YteNkdHLGiyxMyVwHnmE',[O/f'{x}.png' for x in ['main-p02-cards-II','main-p06-map-A','main-p05-association','main-p04-track']])
expected={str(snap.resolve()):H(snap),str(manifest.resolve()):H(manifest)};expected.update({x['path']:x['sha256'] for x in json.loads(manifest.read_text())['sources']});reported={x['path']:x for x in R['allowed_inputs']};assert set(reported)==set(expected)
for p,sha in expected.items():
 assert H(p)==sha
 shas=[v for k,v in reported[p].items() if 'sha256' in k and isinstance(v,str)];assert shas and all(v==sha for v in shas),(p,shas)
derived=[]
for doc in R['complete_read_evidence']['pdfs']:
 for pg in doc['pages']:
  assert H(pg['text'])==pg['text_sha256'] and H(pg['image'])==pg['image_sha256'];derived.extend([{'path':pg['text'],'sha256':pg['text_sha256']},{'path':pg['image'],'sha256':pg['image_sha256']}])
for x in R['complete_read_evidence']['additional_image_inspection_assets']:
 assert H(x['path'])==x['sha256'];derived.append({'path':x['path'],'sha256':x['sha256']})
assert len(derived)==76 and len(expected)==9
assert all(x['model']=='gpt-6.1-sol' and x['effort']=='high' for x in RT['turn_contexts']);assert R['exact_intended_prompt'].strip()==(O/'intended-prompt.txt').read_text().strip();assert R['verdict']=='PASS' and R['unresolved_material_count']==R['unresolved_minor_rules_count']==0 and R['snapshot_sha256']==H(snap)
assert manifest_ok and all(c['exact_complete_numbered_text_visible'] for c in checks),[c for c in checks if not c['exact_complete_numbered_text_visible']]
inventory='\n'.join(visible['call_XmVeeop9GWPjrsZrP6wyvCzP']);prompt_count_lines=[s for s in inventory.splitlines() if s.startswith('intended-prompt.txt')]
proof={'verdict':'PASS_ACTUAL_COMPLETE_SOURCE_ACCESS_AND_FRESH_INDEPENDENCE','snapshot_sha256':H(snap),'runtime':RT['turn_contexts'],'session_log':RT['session_log_path'],'requested_model_effort_fork':'Sol/high/none; originalrootspawn recorded, no parent history supplied','actual_dispatch_plaintext_recovery_not_claimed':True,'intended_prompt_exact_report_match':True,'authorized_input_hashes':expected,'all9input_and76derived_hashes_verified':True,'derived_hashes':derived,'text_checks':checks,'manifest_full_text_visible':manifest_ok,'all717summary_lines_visible':True,'all1898raw_logical_lines_true_EOF_visible':True,'all33PDF_page_texts_visible':True,'actual_image_view_calls':views,'actual_image_block_count':sum(v['actual_image_blocks'] for v in views.values()),'coverage':'33fullPDFpageimages+2originalphotos+10source-onlyzoomcrops','all37executable_calls_inspected':True,'metadata_only_duplicate_instruction_event':{'call_id':'call_XmVeeop9GWPjrsZrP6wyvCzP','operation':"Directory *.txt inventory used f.read_text() twice to compute lengths, including intended-prompt.txt.",'actual_returned_lines':prompt_count_lines,'contents_returned':False,'identity':'Exactsame task instructions already supplied; no outside rule, key, prior finding, grade, history or other-candidate content entered.','description_qualification':'Auditor says contents not read; at byte-operation level it decoded the duplicate prompt for counts. This distinction is recorded explicitly. Root independently accepted this as metadata-only, no outside rule-input leak.','future_prevention':'Keep any future auditor intended-prompt artifact outside its derivative/output directory.'},'other_access':'Named nine inputs, own source-only derivates/metadata/report, cwdidentity, plus disclosed duplicate-task metadata count. No network/otheragent/canonical/priorreport/key/reader access.','source_only_gate_accepted_by_coordinator':True,'finding_counts':{'material':0,'credible_minor_rules_omissions':0}}
(O/'runtime-and-input-validation.json').write_text(json.dumps(proof,indent=2)+'\n');(O/'actual-text-output-trace.json').write_text(json.dumps({'raw_visible_text_blocks':rawblocks,'image_return_metadata':imageblocks},indent=2)+'\n');print(json.dumps({'verdict':proof['verdict'],'source_text_checks':len(checks),'actual_images':proof['actual_image_block_count'],'authorized_plus_derived_hashes':len(expected)+len(derived),'snapshot_sha256':H(snap),'metadata_only_prompt_count_disclosed':True},indent=2))
