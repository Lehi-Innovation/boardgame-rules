"""Bind fresh supplemental coverage20 to whole texts and exact selected records."""
from pathlib import Path
from datetime import datetime,timezone
import ast,base64,hashlib,json,re

B=Path(__file__).resolve().parent;ROOT=B.parents[4]
G=ROOT/'docs/quality/summary-qa/cosmic-encounter'/B.name;A=G/'source-review/supplement-coverage-20'
load=lambda p:json.loads(p.read_text());HB=lambda b:hashlib.sha256(b).hexdigest();H=lambda p:HB(p.read_bytes())
report=load(A/'coverage-challenge.json');receipt=load(A/'delivery-receipt.json')
assert report['bounded_verdict']['new_gap_count']==0 and not report['new_gaps'] and not report['independent_new_gaps']
assert report['bounded_verdict']['all_substantive_eligible_fields_actually_asked']
actor='01a1b5b3-b1e3-7812-8c9b-bfe998151b8a';rt=next(Path('/mnt/c/Users/jonny/.codex/sessions/2026/11/07').glob('*'+actor+'.jsonl'))
tree=ast.parse((B/'check-spirit-source09-delivery.py').read_text());fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='strings');ns={'json':json};exec(compile(ast.Module(body=[fn],type_ignores=[]),'<public-string-walker>','exec'),ns)
outputs=[];images=[];ends=[];contexts=[];calls=[]
for n,line in enumerate(rt.open(),1):
    d=json.loads(line);v=d.get('payload',{})
    if d.get('type')=='session_meta':assert v['id']==actor and v['parent_thread_id']=='01a1b3c7-0daa-70f1-9158-0e75d24cbb22' and v['agent_path']=='/root/supplement_source_coverage_20'
    elif d.get('type')=='turn_context':contexts.append({'record':n,'model':v.get('model'),'effort':v.get('effort')})
    elif d.get('type')=='event_msg' and v.get('type')=='task_complete':ends.append(n)
    elif d.get('type')=='response_item':
        if v.get('type') in ('function_call','custom_tool_call'):
            text=v.get('input',v.get('arguments',''));name=v.get('name','')
            assert not re.search(r'(?:spawn_agent|list_agents|get_agent_info|read_thread|wait_threads|send_message_to_thread|web__run)',name+' '+text)
            assert not any(t in text for t in ['rules/cosmic-encounter.md','summary-snapshot.md','repair-freeze-','reader-a.json','reader-b.json','source-only-audit','applicability-review.json','source-corrections-','/sessions/','coordinator-checks/'])
            calls.append({'record':n,'name':name,'raw_record_sha256':HB(line.encode())})
        elif v.get('type') in ('function_call_output','custom_tool_call_output'):
            out=v.get('output');outputs.append((n,HB(line.encode()),list(ns['strings'](out))))
            if isinstance(out,list):
                for ix,x in enumerate(out):
                    if not isinstance(x,dict) or x.get('type')!='input_image':continue
                    url=x.get('image_url');url=url.get('url') if isinstance(url,dict) else url
                    assert isinstance(url,str) and ';base64,' in url
                    raw=base64.b64decode(url.split(';base64,',1)[1],validate=True);images.append({'record':n,'raw_record_sha256':HB(line.encode()),'block':ix,'sha256':HB(raw),'bytes':len(raw),'detail':x.get('detail')})
assert ends and contexts and all(x['model']=='gpt-6.1-sol' and x['effort']=='high' for x in contexts)
def actual(text):
    m=[{'record':n,'raw_record_sha256':h} for n,h,values in outputs if n<max(ends) and any(text in v or json.dumps(text,ensure_ascii=False)[1:-1] in v for v in values)]
    assert m;return m
whole=[]
for f in receipt['complete_inputs_actually_delivered'].values():
    p=Path(f['path']);t=p.read_text();assert H(p)==f['sha256'] and len(t)==f['chars'];cursor=0;parts=[]
    for c in f['chunks']:
        a,z=c['start'],c['end'];assert a==cursor and a<z<=len(t) and z-a<=6000 and HB(t[a:z].encode())==c['utf8_sha256'];parts.append({'start':a,'end':z,'sha256':c['utf8_sha256'],'actual_outputs':actual(t[a:z])});cursor=z
    assert cursor==len(t);whole.append({'path':str(p),'sha256':H(p),'characters':len(t),'parts':parts})
assert len(whole)==3
f=receipt['source_scope_delivery'];policy=Path(f['path']);t=policy.read_text();assert H(policy)==f['sha256'] and len(t)==f['chars'];policy_actual=actual(t)
def pointer(v,path):
    for part in path.split('/')[1:]:
        part=part.replace('~1','/').replace('~0','~');v=v[int(part)] if isinstance(v,list) else v[part]
    return v
selected=[]
for f in receipt['selected_complete_record_deliveries']:
    p=Path(f['source_path']);obj=pointer(load(p),f['pointer']);t=json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':'))
    assert HB(t.encode())==f['canonical_sha256'] and len(t)==f['canonical_chars']
    embedded=report['selected_records_exact'][str(p)+'#'+f['pointer']]
    assert embedded['record_exact']==obj and embedded['canonical_sha256']==f['canonical_sha256']
    cursor=0;parts=[]
    for c in f['chunks']:
        a,z=c['start'],c['end'];assert a==cursor and a<z<=len(t) and z-a<=6000 and HB(t[a:z].encode())==c['utf8_sha256'];parts.append({'start':a,'end':z,'sha256':c['utf8_sha256'],'actual_outputs':actual(t[a:z])});cursor=z
    assert cursor==len(t);selected.append({'path':str(p),'file_sha256':H(p),'pointer':f['pointer'],'id':f['id'],'canonical_sha256':f['canonical_sha256'],'parts':parts})
assert len(selected)==6
image=report['image_evidence'];ip=Path(image['path']);ih=H(ip);assert ih==image['decoded_payload_sha256']=='0cb65b933b19c24ccc93d3c8326e78c34622cf9a7f55dfc00f5d6badcd293981'
payloads=[x for x in images if x['record']<max(ends) and x['sha256']==ih and x['detail']=='original'];assert payloads
lineage_path=B/'coordinator-checks/cosmic-source15-freeze16-actual-addendum.json';lineage=load(lineage_path);assert lineage['new_original_detail_page16']['sha256']==ih and lineage['new_original_detail_page16']['independently_byte_equal_Fitz1_5_native_pdf_render'];assert H(Path(lineage['new_native_publisher_page16']['path']))==lineage['new_native_publisher_page16']['pdf_sha256']
proof={'verified':True,'checked_at_utc':datetime.now(timezone.utc).isoformat(),'actor':actor,'runtime_path':str(rt),'runtime_sha256_at_check':H(rt),'all_actual_contexts':contexts,'complete_actual_text_inputs':whole,'normative_policy_actual_whole_delivery':policy_actual,'six_selected_exact_records':selected,'no_false_wholekey_or_wholescope_delivery_claim':True,'new_actual_native_page16_payloads':payloads,'independent_render_lineage_reused':{'path':str(lineage_path),'sha256':H(lineage_path),'same_pinned_pdf_and_png':True},'public_tool_calls':calls,'report_path':str(A/'coverage-challenge.json'),'report_sha256':H(A/'coverage-challenge.json'),'bounded_verdict':report['bounded_verdict'],'semantic_acceptance':'NewQ169actuallyasks all source-supported reveal relations. OldQ001/Q090/Q150/Q168 alone do not test the new timing. Threefixedfactscover prereqs,simultaneity,beforedeckandhands; documentaryattribution isgiven/background,notanotheranswergate. Zeroextraquestions justified for this one newsource stratum; unchanged original167/coreclosure remains historicalretainedproof, notnew50-alien audit.','limits':['Freshsource/key/coverage challenge of ONLY the new authorized supplementary stratum, no guide/readers/grades/peerQA supplied. Actual initialfork/spawn checked separately.','Three fulltextinputs +full4735policy and six WHOLEselectedrecords verified; no claimofcompletekey/scopefile delivery.','Whole168readerpair/currentfacts/FAQcoreauthoritygap/stamp/publication remain separate.']}
out=B/'coordinator-checks/cosmic-source20-fresh-supplement-coverage-actual-acceptance.json';assert not out.exists();out.write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps({'verified':True,'full_text_files':len(whole),'text_ranges':sum(len(x['parts']) for x in whole),'policy_files':1,'selected_records':len(selected),'native_images':len(payloads),'proof':str(out)}))
