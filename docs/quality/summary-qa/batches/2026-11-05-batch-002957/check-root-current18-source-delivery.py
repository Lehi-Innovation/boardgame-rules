"""Verify fresh Root source audit: complete meaning, native text, images, lineage."""
from pathlib import Path
from datetime import datetime,timezone
import ast,base64,json,hashlib
import fitz
B=Path(__file__).resolve().parent;ROOT=B.parents[4]
V=ROOT/'docs/quality/summary-qa/root'/B.name/'current-snapshot-revalidation-2026-11-07';A=V/'source-only-audit'
J=lambda p:json.loads(p.read_text());HB=lambda b:hashlib.sha256(b).hexdigest();H=lambda p:HB(p.read_bytes())
audit_path=A/'source-audit.json';audit=J(audit_path);index=J(V/'source-delivery-serialized-metadata/source-delivery-audit.json')
assert audit['verdict']=='PASS' and not audit['findings'] and not audit['authority_conflicts'] and index['status']=='PASS'
for name,receipt in audit['input_hashes'].items():assert H(Path(name))==receipt['sha256']
assert H(ROOT/'rules/root.md')==H(V/'iteration-01/summary-snapshot.md')=='da0b6b08fda1d3e1775a8ef813e31535ac35375399b061efe255690d09ad1aeb'
actor='01a1b63c-1b8f-7a12-918c-9170edda1718';runtime=next(Path('/mnt/c/Users/jonny/.codex/sessions/2026/11/07').glob('*'+actor+'.jsonl'))
tree=ast.parse((B/'check-spirit-source09-delivery.py').read_text());fn=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='strings');ns={'json':json};exec(compile(ast.Module(body=[fn],type_ignores=[]),'<strings>','exec'),ns)
outputs=[];images=[];contexts=[];terminals=[];calls=[]
for n,line in enumerate(runtime.open('rb'),1):
    row=json.loads(line);p=row.get('payload',{})
    if row.get('type')=='turn_context':contexts.append({'record':n,'model':p.get('model'),'effort':p.get('effort')})
    if row.get('type')=='event_msg' and p.get('type')=='task_complete':terminals.append(n)
    if row.get('type')=='event_msg' and p.get('type')=='item_completed':
        item=p.get('item',{})
        if item.get('type')=='CommandExecution':outputs.append((n,HB(line),list(ns['strings'](item.get('aggregated_output','')))))
    if row.get('type')!='response_item':continue
    if p.get('type') in ['function_call','custom_tool_call']:
        text=p.get('input',p.get('arguments',''))
        assert not any(x in text for x in ['questions.json','answer-key.json','grading-scope-policy','reader-a.json','reader-b.json','get_agent_info','list_agents','read_thread','wait_threads'])
        calls.append({'record':n,'name':p.get('name'),'record_sha256':HB(line)})
    if p.get('type') in ['function_call_output','custom_tool_call_output']:
        out=p.get('output');outputs.append((n,HB(line),list(ns['strings'](out))))
        if isinstance(out,list):
            for k,item in enumerate(out):
                if not isinstance(item,dict) or item.get('type')!='input_image':continue
                url=item.get('image_url');url=url.get('url') if isinstance(url,dict) else url
                data=base64.b64decode(url.split(';base64,',1)[1],validate=True)
                images.append({'record':n,'record_sha256':HB(line),'block':k,'bytes':len(data),'payload_sha256':HB(data),'actual_detail':item.get('detail')})
assert terminals and contexts and all(x['model']=='gpt-6.1-sol' and x['effort']=='high' for x in contexts)
upper=max(terminals)
def matches(text):
    found=[{'record':n,'record_sha256':h,'actual_output_value_characters':max(len(v) for v in vals)} for n,h,vals in outputs if n<upper and any(text in v.replace('\r\n','\n') for v in vals)]
    assert found
    return found
whole=[]
for f in index['inputs']:
    p=Path(f['path']);source=p.read_text().splitlines(keepends=True);assert H(p)==f['sha256'] and len(source)==f['total_lines'];cursor=0;parts=[]
    if p.name=='summary-snapshot.md':declared_ranges=[(1,200),(201,len(source))]
    elif p.name=='root-rules.txt':declared_ranges=audit['inspection']['extracted_law']['ranges']
    elif p.name=='publisher-rules-library-p16.txt':declared_ranges=audit['inspection']['publisher_rendered_text']['ranges']
    else:raise AssertionError(str(p))
    for a,z in declared_ranges:
        z=min(z,len(source));assert a==cursor+1 and a<=z<=len(source);text=''.join(source[a-1:z])
        parts.append({'line_start_1based':a,'line_end_inclusive':z,'slice_sha256':HB(text.encode()),'actual_outputs':matches(text)});cursor=z
    assert cursor==len(source);whole.append({'path':str(p),'sha256':H(p),'parts':parts})
assert len(whole)==3
prov=A/'source-provenance.json';provenance={'path':str(prov),'sha256':H(prov),'actual_outputs':matches(prov.read_text())}
pub=index['publisher_representation'];jp=Path(pub['raw_json_path']);raw=J(jp);txt=Path(next(f['path'] for f in index['inputs'] if f['path'].endswith('publisher-rules-library-p16.txt')))
assert H(jp)==pub['raw_json_sha256'] and raw['results'][0]['text']+'\n'==txt.read_text()
jsonlines=jp.read_text().splitlines(keepends=True);omitted=pub['long_escaped_text_property_line'];assert omitted==9
nontext=[];covered=set()
for a,z in audit['inspection']['publisher_structure']['complete_nontext_raw_ranges']:
    assert not a<=omitted<=z
    text=''.join(jsonlines[a-1:z]);nontext.append({'line_start_1based':a,'line_end_inclusive':z,'slice_sha256':HB(text.encode()),'actual_outputs':matches(text)});covered.update(range(a,z+1))
assert covered==set(range(1,len(jsonlines)+1))-{omitted}
manifest_path=A/'native-render-manifest.json';manifest=J(manifest_path);pdf=ROOT/'source_pdfs/root-recovery.pdf'
assert H(pdf)==manifest['pdf_sha256'];native_text=[];native_images=[];page_map={x['physical_page']:x for x in manifest['pages']}
with fitz.open(pdf) as doc:
    assert len(doc)==manifest['page_count']==32
    for rec in manifest['all_native_page_texts']:
        page=rec['physical_page'];p=Path(rec['derived_text_file']);text=doc[page-1].get_text()
        assert HB(text.encode())==H(p)==rec['sha256'] and p.read_text()==text
        native_text.append({'page':page,'path':str(p),'sha256':H(p),'actual_outputs':matches(text)})
    for page in [1,5,9,10,24,27,28,32]:
        rec=page_map[page];data=doc[page-1].get_pixmap(matrix=fitz.Matrix(2,2)).tobytes('png');assert HB(data)==H(Path(rec['render']))==rec['png_sha256']
with fitz.open(pdf) as doc:
    for page in [2,3,4,6,7,8,25,26]:
        rec=page_map[page];data=doc[page-1].get_pixmap(matrix=fitz.Matrix(2,2)).tobytes('png');assert HB(data)==H(Path(rec['render']))==rec['png_sha256']
for page,rec in sorted(page_map.items()):
    delivered=[x for x in images if x['record']<upper and x['payload_sha256']==rec['png_sha256']];assert delivered
    native_images.append({'page':page,'path':rec['render'],'sha256':rec['png_sha256'],'dimensions':[rec['pixel_width'],rec['pixel_height']],'independently_byte_equal_native_pdf_2x':True,'actual_payloads':delivered})
assert len(native_text)==32 and len(native_images)==16
proof={'verified':True,'checked_at_utc':datetime.now(timezone.utc).isoformat(),'summary_sha256':H(V/'iteration-01/summary-snapshot.md'),'auditor':actor,'runtime_path':str(runtime),'runtime_sha256':H(runtime),'actual_contexts':contexts,'audit_path':str(audit_path),'audit_sha256':H(audit_path),'complete_actual_primary_texts':whole,'own_source_only_provenance':provenance,'publisher_json':{'path':str(jp),'sha256':H(jp),'complete_decoded_text_byte_equal_TXT_except_declared_final_newline':True,'all_nontext_raw_lines_actually_received':nontext,'all814_links_and_remaining_metadata_covered':True,'long_escaped_line_literal_delivery_claimed':False},'all32_native_PDF_page_texts_reproduced_and_actually_received':native_text,'all16_native_PDF_images_reproduced_and_actually_received':native_images,'public_tool_trace':calls,'current_canonical_matches':True,'verdict':'PASS','limits':['Fresh pure actor/fork model metadata verified separately. No Q/key/reader/priorQA/status access in public calls.','Large raw JSON escaped text line originally truncated and NOT claimed as literal full delivery; its complete decoded value was actually read in full TXT, with exact byte equivalence proved. All remaining raw JSON/link/metadata lines actually read. Earlier partial technical index remains preserved.','Text range membership is mapped into actual unsplit tool envelopes; no smaller fabricated source deliveries or pre-first-draft chronology claimed.','Accuracy PASS exactda0 only. Failed current18 A79/B81 and NEW current19 performance remain separate; no publication/goal approval.']}
out=B/'coordinator-checks/root-current18-fresh-source-actual-delivery-and-native-lineage.json';assert not out.exists();out.write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps({'verified':True,'full_primary_texts':len(whole),'native_text_pages':len(native_text),'native_image_pages':len(native_images),'actual_image_payloads':len(images),'proof':str(out)}))
