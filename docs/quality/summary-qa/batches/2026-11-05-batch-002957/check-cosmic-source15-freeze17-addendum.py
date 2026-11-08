"""Verify own-source full freeze17 continuation and exact primary FAQ spot."""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,re
B=Path(__file__).resolve().parent;ROOT=B.parents[4]
A=ROOT/'docs/quality/summary-qa/cosmic-encounter'/B.name/'source-review'
J=lambda p:json.loads(p.read_text());HB=lambda b:hashlib.sha256(b).hexdigest();H=lambda p:HB(p.read_bytes())
prior_path=B/'coordinator-checks/cosmic-source15-freeze16-actual-addendum.json';prior=J(prior_path)
old14_path=Path(prior['prior_verified_union']);old14=J(old14_path)
base_path=Path(old14['prior_verified_union']);base=J(base_path)
assert H(base_path)==old14['prior_verified_union_sha256'] and H(old14_path)==prior['prior_verified_union_sha256']
for proof in [base,old14,prior]:assert H(Path(proof['audit_path']))==proof['audit_sha256']
ap=A/'source-only-audit-15-freeze17.json';rp=A/'source-only-delivery-15-freeze17.json';np=A/'source15-freeze17-normalized-delivery.json'
audit=J(ap);receipt=J(rp);normalized=J(np)
assert audit['source_verdict']=='PASS' and not audit['demonstrated_errors'] and not audit['omissions'] and not audit['new_findings']
assert audit['isolation']['fresh_independent_vote'] is False
candidate=Path(audit['summary']['path']);assert H(candidate)==audit['summary']['sha256']=='787b88677123fc93751d1605a99e4c724faadaa891f1b0c103bcb296075952b9'
for f in base['full_text_inputs']:assert H(Path(f['path']))==f['sha256']
for f in base['original_native_alien_images']:assert H(Path(f['path']))==f['sha256']
for f in base['independently_reproduced_native_pdf_text_views']:assert H(Path(f['path']))==f['pdf_sha256']
for f in prior['new_complete_text_inputs']:assert H(Path(f['path']))==f['sha256']
runtime=Path(prior['runtime']);lines=runtime.read_bytes().splitlines(keepends=True);old_records=[]
for f in base['full_text_inputs']:
    for p in f['parts']:old_records.extend(p['actual_output_records'])
for f in base['original_native_alien_images']:old_records.extend({'record':x['record'],'sha256':x['record_sha256']} for x in f['actual_deliveries'])
for f in base['independently_reproduced_native_pdf_text_views']:
    for p in f['parts']:old_records.extend(p['actual_output_records'])
for f in old14['new_full_summary_parts']:old_records.extend(f['actual_records'])
for f in old14['new_native_pdf_text_views']:old_records.extend(f['actual_records'])
for f in prior['new_complete_text_inputs']:
    for p in f['parts']:old_records.extend(p['actual_records'])
old_records.extend(prior['new_native_publisher_page16']['actual_records'])
old_records.extend({'record':x['record'],'sha256':x['raw_record_sha256']} for x in prior['new_original_detail_page16']['actual_payloads'])
for r in old_records:assert HB(lines[r['record']-1])==r['sha256']
tree=ast.parse((B/'check-spirit-source09-delivery.py').read_text());fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='strings');ns={'json':json};exec(compile(ast.Module(body=[fn],type_ignores=[]),'<strings>','exec'),ns)
lower=prior['current_completion_record'];outputs=[];contexts=[];ends=[];calls=[]
for n,line in enumerate(lines,1):
    if n<=lower and b'"turn_context"' not in line:continue
    row=json.loads(line);p=row.get('payload',{})
    if row.get('type')=='turn_context':contexts.append({'record':n,'model':p.get('model'),'effort':p.get('effort')})
    if n<=lower:continue
    if row.get('type')=='event_msg' and p.get('type')=='task_complete':ends.append(n)
    if row.get('type')!='response_item':continue
    if p.get('type') in ['function_call_output','custom_tool_call_output']:outputs.append((n,list(ns['strings'](p.get('output')))))
    if p.get('type') in ['function_call','custom_tool_call']:
        text=p.get('input',p.get('arguments',''))
        assert not re.search(r'(?:get_agent_info|list_agents|read_thread|wait_threads|web__run)\s*\(',text)
        assert not any(x in text for x in ['questions.json','answer-key.json','reader-a.json','reader-b.json','actual-question-scope.json','source-corrections-17.json','coordinator-checks/'])
        calls.append({'record':n,'name':p.get('name'),'raw_record_sha256':HB(line)})
assert ends and contexts and all(x['model']=='gpt-6.1-sol' and x['effort']=='high' for x in contexts)
upper=max(ends)
def actual(text):
    found=[n for n,values in outputs if n<upper and any(text in v or json.dumps(text,ensure_ascii=False)[1:-1] in v for v in values)]
    assert found
    return [{'record':n,'sha256':HB(lines[n-1])} for n in found]
whole=[]
for f in normalized['text_input_proofs']:
    p=Path(f['path']);text=p.read_text();assert H(p)==f['full_file_sha256'];cursor=0;parts=[]
    for c in f['chunks']:
        a,z=c['start_char'],c['end_char_exclusive'];assert a==cursor and a<z<=len(text) and z-a<=6000 and HB(text[a:z].encode())==c['utf8_chunk_sha256']
        parts.append({'start':a,'end':z,'sha256':c['utf8_chunk_sha256'],'actual_records':actual(text[a:z])});cursor=z
    assert cursor==len(text);whole.append({'path':str(p),'sha256':H(p),'characters':len(text),'parts':parts})
assert len(whole)==2 and sorted(x['characters'] for x in whole)==[4735,59002]
spots=[]
for f in receipt['new_primary_text_spot_checks']:
    p=Path(f['path']);text=p.read_text();a,z=f['start'],f['end'];part=text[a:z]
    assert H(p)==f['source_sha256'] and HB(part.encode())==f['chunk_sha256'] and len(part)==f['chars']
    spots.append({'path':str(p),'sha256':H(p),'start':a,'end':z,'slice_sha256':f['chunk_sha256'],'actual_records':actual(part)})
assert len(spots)==1
change=audit['current_claim_checks'][0];assert change['current_quote'] in candidate.read_text()
assert change['primary_exact_quote'] in Path(spots[0]['path']).read_text()[spots[0]['start']:spots[0]['end']]
assert [x['id'] for x in audit['authority_limits'] if x['id']=='G15-02']==['G15-02']
proof={'verified_delivery_only':True,'checked_at_utc':datetime.now(timezone.utc).isoformat(),'auditor':prior['auditor'],'runtime':str(runtime),'runtime_sha256_at_check':H(runtime),'actual_contexts':contexts,'prior_verified_union':str(prior_path),'prior_verified_union_sha256':H(prior_path),'old_actual_public_record_bindings_rechecked':len(old_records),'old_source_and_original50_native_hashes_current':True,'new_complete_text_inputs':whole,'new_primary_FAQ_spot':spots,'prior_completion_record':lower,'current_completion_record':upper,'new_public_tool_call_trace':calls,'audit_path':str(ap),'audit_sha256':H(ap),'receipt_sha256':H(rp),'normalized_receipt_sha256':H(np),'summary_sha256':H(candidate),'current_canonical_matches_at_check':H(candidate)==H(ROOT/'rules/cosmic-encounter.md'),'semantic_acceptance':'Only new Void Super ally-use sentence is directly supported by the explicit original-base FAQ parenthetical. Prior168 question/coverage procedure remains applicable. All source claim checks and the sole body delta reviewed. Attributed later setup remains narrowly scoped. One essential reinforcement/Negotiate FAQ conflict persists; optional preferences are not automatically additional essential blockers.','limits':['Initially fresh pure15 own-source continuation, not new vote. Whole4735policy and59002candidate in11 fresh full ranges plus164-character originalFAQ spot; prior wholecorpus/50native views explicitly reused with actual record bindings checked.','No new native image view is claimed for freeze17; clear originalFAQ text spot suffices. Parent-created repair17 image is not attributed to this auditor.','No new pair, global scope/readiness, stamp or publication approval.']}
out=B/'coordinator-checks/cosmic-source15-freeze17-actual-addendum.json';assert not out.exists();out.write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps({'verified_delivery_only':True,'old_actual_records':len(old_records),'new_whole_ranges':sum(len(x['parts']) for x in whole),'new_FAQ_spots':len(spots),'current_canonical_matches':proof['current_canonical_matches_at_check'],'proof':str(out)}))
