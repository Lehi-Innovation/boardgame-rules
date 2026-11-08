"""Bind current C29 source signoff to original pure15 and new current-body deliveries."""
import ast,difflib,hashlib,json
from datetime import datetime,timezone
from pathlib import Path
B=Path(__file__).resolve().parent;R=B.parents[4]
G=R/'docs/quality/summary-qa/spirit-island'/B.name
J=lambda p:json.loads(p.read_text());HB=lambda b:hashlib.sha256(b).hexdigest();H=lambda p:HB(p.read_bytes())
resolve=lambda p:(R/p).resolve()
ap=G/'source-audit15-current-body-C29-followup.json';lp=G/'source-audit15-current-body-C29-followup-read-view-ledger.json'
a=J(ap);ledger=J(lp);freeze=J(G/'source-audit15-C29-followup-original-completed/original-freeze.json')
assert a['verdict']=='PASS' and not a['findings'] and not a['unresolved_current_guide_findings'] and not a['unverified_current_guide_concerns']
for row in freeze['originals']:
    assert H(Path(row['path']))==row['sha256']==H(Path(row['immutable_copy']))==row['immutable_copy_sha256']
candidate=resolve(a['candidate_path']);prior=resolve(a['prior_candidate_path'])
assert H(candidate)==a['candidate_sha256']==H(R/'rules/spirit-island.md')=='98863278049dd9af7bf5953ac092b6e2e176f1ec75f33bb48159ed9e63509968'
assert H(prior)==a['prior_candidate_sha256']=='8f17f3ce025a16045709c4302e1c2e46d9da22c1e705fc4db28d8b7182985e5c'
base=J(B/'coordinator-checks/spirit-source-audit-final-15-actual-delivery.json')
correction=J(B/'coordinator-checks/spirit-C26-source15-own-correction-and-semantic-acceptance.json')
assert base['verified'] and correction['verified']
for row in ledger['reused_own_evidence_artifacts']:assert H(resolve(row['path']))==row['source_sha256']
assert len(ledger['reused_complete_text_perceptions'])==16 and len(ledger['reused_visual_perceptions'])==57
oldviews={resolve(x['path']):x['sha256'] for x in base['individually_bound_native_images']}
for row in ledger['reused_visual_perceptions']:
    path=resolve(row['path']);assert H(path)==row['source_sha256']==oldviews[path]
for row in ledger['reused_complete_text_perceptions']:assert H(resolve(row['path']))==row['source_sha256']
assert len(ledger['reused_source_manifest_and_supplement_reconciliation'])==79
for row in ledger['reused_source_manifest_and_supplement_reconciliation']:assert H(resolve(row['path']))==row['source_sha256']
rows=ledger['actual_new_text_deliveries'];assert rows==a['new_source_delivery'] and rows
tree=ast.parse((B/'check-spirit-source09-delivery.py').read_text());fn=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='strings');ns={'json':json};exec(compile(ast.Module(body=[fn],type_ignores=[]),'<strings>','exec'),ns)
runtime=Path(freeze['external_runtime_path']);oldbound=J(G/'source-audit15-C28-followup-original-completed/original-freeze.json')
prior_count=oldbound['runtime_records_at_completed_freeze']
assert prior_count==freeze['prior_completed_records_excluded_from_new_delivery_claim']
oldhash=hashlib.sha256();frozenhash=hashlib.sha256();received=[];contexts=[];ends=[];writers=[];calls=[]
for n,line in enumerate(runtime.open('rb'),1):
    if n<=prior_count:oldhash.update(line)
    if n<=freeze['runtime_records_at_completed_freeze']:frozenhash.update(line)
    if n<=prior_count or n>freeze['runtime_records_at_completed_freeze']:continue
    row=json.loads(line);p=row.get('payload',{})
    if row.get('type')=='turn_context':contexts.append((p.get('model'),p.get('effort')))
    if row.get('type')=='event_msg' and p.get('type')=='task_complete':ends.append(n)
    if row.get('type')=='event_msg' and p.get('type')=='item_completed':
        item=p.get('item',{})
        if item.get('type')=='CommandExecution':received.append((n,HB(line),list(ns['strings'](item.get('aggregated_output','')))))
    if row.get('type')!='response_item':continue
    typ=p.get('type')
    if typ in ['function_call_output','custom_tool_call_output']:received.append((n,HB(line),list(ns['strings'](p.get('output')))))
    if typ in ['function_call','custom_tool_call']:
        code=p.get('input',p.get('arguments',''))
        assert not any(x in code for x in ['questions.json','answer-key.json','asked-fact-map.json','coverage-review','reader-a.json','reader-b.json','/sessions/','source-audit-final-16.json'])
        calls.append({'record':n,'name':p.get('name'),'record_sha256':HB(line)})
        if ap.name in code and any(x in code for x in ['write_text','json.dump','writeFile','apply_patch']):writers.append(n)
assert oldhash.hexdigest()==oldbound['runtime_sha256_at_completed_freeze'] and frozenhash.hexdigest()==freeze['runtime_sha256_at_completed_freeze']
assert contexts and all(x==('gpt-6.1-sol','high') for x in contexts) and ends and writers
boundary=min(writers);checks=[];candidate_ranges=[]
for e in rows:
    path=resolve(e['path']);assert H(path)==e['source_sha256'] and not e['truncated'] and e['output_cap']>=4000
    texts=[path.read_bytes().decode('utf-8'),path.read_text()];a0,z=e['start'],e['end']
    text=next(t for t in texts if len(t)==e['character_length'] and HB(t[a0:z].encode())==e['slice_sha256'])
    assert 0<=a0<z<=len(text) and z-a0<=6000
    hits=[{'record':n,'record_sha256':h} for n,h,values in received if n<boundary and any(text[a0:z] in v for v in values)]
    assert hits,(path.name,a0,z)
    checks.append(dict(e,actual_new_output_records=hits))
    if path==candidate:candidate_ranges.append((a0,z))
cursor=0
for a0,z in sorted(candidate_ranges):assert a0==cursor;cursor=z
assert cursor==a['candidate_character_length']==len(candidate.read_text())
references=[]
def checkref(q):
    path=resolve(q['path']);assert H(path)==q['source_sha256']
    if all(k in q for k in ['start','end','passage']):
        assert any(t[q['start']:q['end']]==q['passage'] for t in [path.read_bytes().decode('utf-8'),path.read_text()])
        references.append({'path':str(path),'start':q['start'],'end':q['end'],'sha256':H(path)})
for item in a['changed_material']:
    if 'candidate_source_sha256' in item:assert item['candidate_source_sha256']==H(candidate)
    assert 0<=item['candidate_start']<item['candidate_end']<=len(candidate.read_text()) and not item['findings']
    for q in item['primary_citations']:checkref(q)
    for q in item['primary_visual_citations']:assert H(resolve(q['path']))==q['source_sha256']==oldviews[resolve(q['path'])]
for group in a['checked_current_scope']:
    for q in group['primary_sources']:checkref(q)
    for q in group['visual_source_references']:assert H(resolve(q['path']))==q['source_sha256']==oldviews[resolve(q['path'])]
oldtext=prior.read_text();newtext=candidate.read_text();oldlines=oldtext.splitlines(keepends=True);newlines=newtext.splitlines(keepends=True)
changes=[]
for kind,i,j,x,y in difflib.SequenceMatcher(a=oldlines,b=newlines,autojunk=False).get_opcodes():
    if kind=='equal':continue
    changes.append({'change':kind,'prior_start':sum(map(len,oldlines[:i])),'prior_end':sum(map(len,oldlines[:j])),'current_start':sum(map(len,newlines[:x])),'current_end':sum(map(len,newlines[:y])),'prior_text':''.join(oldlines[i:j]),'current_text':''.join(newlines[x:y])})
assert changes==a['comparison']['source_only_derived_diff']['changes'] and len(changes)==4 and len(newtext)-len(oldtext)==712
proof={'verified':True,'checked_at_utc':datetime.now(timezone.utc).isoformat(),'audit_path':str(ap),'audit_sha256':H(ap),'ledger_sha256':H(lp),'summary_sha256':H(candidate),'original_followup_copies_and_runtime_prefix_verified':True,'same_original_initially_pure_auditor':base['auditor'],'new_contexts':contexts,'new_completed_turn_records':ends,'first_original_report_writer_record':boundary,'actual_new_deliveries':checks,'whole_current_candidate_newly_received':True,'changed_primary_and_current_scope_exact_references':references,'all23_current_scope_groups':len(a['checked_current_scope']),'all79_reused_source_pins_and16_whole_texts57_native_views_rechecked':True,'exact4_block712_character_diff_independently_reproduced':True,'public_new_call_trace':calls,'semantic_acceptance_status':'PENDING_SEPARATE_COORDINATOR_REVIEW','verdict':'PASS','limits':['Source followup integrity only on exact 988632 C29; both173 reader results, actual stamping and exact-stamped-byte full173 validation remain separate.','No new whole-authority/native-image quota; source15 original complete evidence and correction remain independently bound.','No source16 final vote was discarded: its interrupted candidate/manifest-only partial work, no findings or completed three-file audit, is preserved separately.']}
out=B/'coordinator-checks/spirit-source15-C29-current-body-actual-followup-integrity.json';assert not out.exists();out.write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps({'verified':True,'new_ranges':len(checks),'current_candidate_ranges':len(candidate_ranges),'primary_references':len(references),'groups':len(a['checked_current_scope']),'proof':str(out)}))
