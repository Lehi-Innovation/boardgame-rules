"""Verify pure15's new full policy/body/publisher reading and nativep16."""
from pathlib import Path
from datetime import datetime,timezone
import ast,base64,hashlib,json,re
import fitz
from PIL import Image

B=Path(__file__).resolve().parent;ROOT=B.parents[4]
A=ROOT/'docs/quality/summary-qa/cosmic-encounter'/B.name/'source-review'
load=lambda p:json.loads(p.read_text());HB=lambda b:hashlib.sha256(b).hexdigest();H=lambda p:HB(p.read_bytes())
prior_path=B/'coordinator-checks/cosmic-source15-freeze14-actual-addendum.json';prior=load(prior_path)
base_path=Path(prior['prior_verified_union']);base=load(base_path)
assert H(base_path)==prior['prior_verified_union_sha256']
assert H(Path(base['audit_path']))==base['audit_sha256']
assert H(Path(prior['audit_path']))==prior['audit_sha256']
ap=A/'source-only-audit-15-freeze16.json';rp=A/'source-only-delivery-15-freeze16.json';np=A/'source-only-delivery-15-freeze16-normalized.json'
audit=load(ap);receipt=load(rp);normalized=load(np)
assert audit['source_verdict']=='PASS' and not audit['demonstrated_errors'] and not audit['omissions'] and not audit['new_findings']
assert len(audit['unresolved_sources'])==1 and audit['unresolved_sources'][0]['id']=='G15-02'
assert audit['continuation_and_isolation']['fresh_independent_vote'] is False
assert H(Path(audit['summary']['path']))==audit['summary']['sha256']==H(ROOT/'rules/cosmic-encounter.md')=='ce1f935e05a5e497fea24af7eea3598186dfb04e762000a79a4437e048b48dee'
for f in base['full_text_inputs']:assert H(Path(f['path']))==f['sha256']
for f in base['original_native_alien_images']:assert H(Path(f['path']))==f['sha256']
for f in base['independently_reproduced_native_pdf_text_views']:assert H(Path(f['path']))==f['pdf_sha256']
assert H(Path(prior['new_full_summary_path']))==prior['new_full_summary_sha256']
runtime=Path(prior['runtime']);lines=runtime.read_bytes().splitlines(keepends=True)
old_records=[]
for f in base['full_text_inputs']:
    for p in f['parts']:old_records.extend(p['actual_output_records'])
for f in base['original_native_alien_images']:old_records.extend({'record':x['record'],'sha256':x['record_sha256']} for x in f['actual_deliveries'])
for f in base['independently_reproduced_native_pdf_text_views']:
    for p in f['parts']:old_records.extend(p['actual_output_records'])
for f in prior['new_full_summary_parts']:old_records.extend(f['actual_records'])
for f in prior['new_native_pdf_text_views']:old_records.extend(f['actual_records'])
for x in old_records:assert HB(lines[x['record']-1])==x['sha256']
tree=ast.parse((B/'check-spirit-source09-delivery.py').read_text());fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='strings');ns={'json':json};exec(compile(ast.Module(body=[fn],type_ignores=[]),'<public-string-walker>','exec'),ns)
lower=prior['current_completion_record'];outputs=[];images=[];terminals=[];contexts=[];calls=[]
for n,line in enumerate(lines,1):
    if n<=lower and b'"turn_context"' not in line:continue
    row=json.loads(line);v=row.get('payload',{})
    if row.get('type')=='turn_context':contexts.append({'record':n,'model':v.get('model'),'effort':v.get('effort')})
    if n<=lower:continue
    if row.get('type')=='event_msg' and v.get('type')=='task_complete':terminals.append(n)
    if row.get('type')!='response_item':continue
    if v.get('type') in ['function_call_output','custom_tool_call_output']:
        out=v.get('output');outputs.append((n,list(ns['strings'](out))))
        if isinstance(out,list):
            for index,x in enumerate(out):
                if not isinstance(x,dict) or x.get('type')!='input_image':continue
                url=x.get('image_url');url=url.get('url') if isinstance(url,dict) else url
                assert isinstance(url,str) and url.startswith('data:') and ';base64,' in url
                data=base64.b64decode(url.split(';base64,',1)[1],validate=True)
                images.append({'record':n,'raw_record_sha256':HB(line),'block':index,'bytes':len(data),'sha256':HB(data),'detail':x.get('detail')})
    elif v.get('type') in ['function_call','custom_tool_call']:
        text=v.get('input',v.get('arguments',''))
        assert not re.search(r'(?:get_agent_info|list_agents|read_thread|wait_threads|web__run)\s*\(',text)
        assert not any(s in text for s in ['questions.json','answer-key.json','reader-a.json','reader-b.json','actual-question-scope.json','source-corrections-16.json','applicability-review.json','coordinator-checks/'])
        calls.append({'record':n,'name':v.get('name'),'raw_record_sha256':HB(line)})
assert contexts and all(c['model']=='gpt-6.1-sol' and c['effort']=='high' for c in contexts)
assert terminals;upper=max(terminals)
def actual(part):
    found=[n for n,values in outputs if n<upper and any(part in v or json.dumps(part,ensure_ascii=False)[1:-1] in v for v in values)]
    assert found
    return [{'record':n,'sha256':HB(lines[n-1])} for n in found]
new_text=[]
for f in normalized['text_input_proofs']:
    p=Path(f['path']);text=p.read_text();assert H(p)==f['full_file_sha256'];cursor=0;parts=[]
    for c in f['chunks']:
        a,z=c['start_char'],c['end_char_exclusive'];assert a==cursor and a<z<=len(text) and z-a<=6000 and HB(text[a:z].encode())==c['utf8_chunk_sha256']
        parts.append({'start':a,'end':z,'sha256':c['utf8_chunk_sha256'],'actual_records':actual(text[a:z])});cursor=z
    assert cursor==len(text);new_text.append({'path':str(p),'sha256':H(p),'characters':len(text),'parts':parts})
assert len(new_text)==3 and sorted(x['characters'] for x in new_text)==[4735,58939,75088]
native=receipt['new_native_pdf_text_delivery'];pdf=Path(native['path']);doc=fitz.open(pdf);text=doc[native['printed_page']-1].get_text()
assert len(doc)==20 and len(text)==native['chars'] and HB(text.encode())==native['sha256']
a,z=native['start'],native['end'];assert HB(text[a:z].encode())==native['chunk_sha256'];native_actual=actual(text[a:z])
payload=receipt['new_publisher_p16_payload'];image_path=Path(payload['path']);image_hash=H(image_path)
assert image_hash==payload['returned_decoded_sha256']==payload['expected_sha256']=='0cb65b933b19c24ccc93d3c8326e78c34622cf9a7f55dfc00f5d6badcd293981'
matches=[x for x in images if x['record']<upper and x['sha256']==image_hash and x['detail']=='original'];assert matches
with Image.open(image_path) as im:assert list(im.size)==payload['returned_dimensions']==[918,1188]
render=doc[15].get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False).tobytes('png');assert HB(render)==image_hash
result={'verified_delivery_only':True,'checked_at_utc':datetime.now(timezone.utc).isoformat(),'auditor':prior['auditor'],'runtime':str(runtime),'runtime_sha256_at_check':H(runtime),'all_actual_contexts':contexts,'prior_verified_union':str(prior_path),'prior_verified_union_sha256':H(prior_path),'old_actual_public_record_bindings_rechecked':len(old_records),'old_primary_and_original50_image_hashes_current':True,'new_complete_text_inputs':new_text,'new_native_publisher_page16':{'path':str(pdf),'pdf_sha256':H(pdf),'native_method':'PyMuPDF1.27.2 get_text, independently reproduced; not pypdf text ordering','characters':len(text),'native_text_sha256':HB(text.encode()),'actual_records':native_actual},'new_original_detail_page16':{'path':str(image_path),'sha256':image_hash,'dimensions':[918,1188],'actual_payloads':matches,'independently_byte_equal_Fitz1_5_native_pdf_render':True},'prior_completion_record':lower,'current_completion_record':upper,'new_public_tool_call_trace':calls,'audit_path':str(ap),'audit_sha256':H(ap),'receipt_path':str(rp),'receipt_sha256':H(rp),'normalized_receipt_sha256':H(np),'summary_sha256':audit['summary']['sha256'],'unresolved_authority_gaps':audit['unresolved_sources'],'limits':'Same initiallyfresh pure15 own-source continuation; explicitoldfullsource/50native reuse, notnewvote ornew50-image inspection. New full4735char cleanpolicy,58939charcurrentbody,75088charwhole20ppublishercontext24ranges plusnativep16textandoneactualoriginalp16image afterverifiedf14completion. ScopedsourceaccuracyPASS only; one essentialFAQconflict andunansweredhumanpreferences remain. No whole168reader/stamp/pub/goalapproval.'}
out=B/'coordinator-checks/cosmic-source15-freeze16-actual-addendum.json';assert not out.exists();out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'verified_delivery_only':True,'old_record_bindings':len(old_records),'new_text_files':len(new_text),'new_ranges':sum(len(x['parts']) for x in new_text),'new_native_text_pages':1,'new_original_image_payloads':len(matches),'proof':str(out)}))
