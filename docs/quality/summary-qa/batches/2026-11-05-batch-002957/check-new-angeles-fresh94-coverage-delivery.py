"""Verify fresh94 review's six whole texts, native67 delivery and pixel lineage."""
from pathlib import Path
from datetime import datetime,timezone
import ast,base64,hashlib,json,re
import fitz
from PIL import Image

B=Path(__file__).resolve().parent;ROOT=B.parents[4]
G=ROOT/'docs/quality/summary-qa/new-angeles'/B.name;A=G/'coverage-fresh-final-94'
load=lambda p:json.loads(p.read_text());HB=lambda b:hashlib.sha256(b).hexdigest();H=lambda p:HB(p.read_bytes())
def resolve(p):return (ROOT/p).resolve()
manifest=load(A/'input-manifest.json');native=load(A/'native-manifest.json');report=load(A/'coverage-review.json');validation=load(A/'all94-scope-key-source-validation.json')
assert len(manifest)==6 and len(native)==67 and validation['count']==94
questions=load(G/'expanded-supported-bank-v11/questions.json')['questions'];scope=load(G/'expanded-supported-bank-v11/asked-clause-map.json')
assert [x['id'] for x in validation['questions']]==[x['id'] for x in questions]
assert [x['literal_question'] for x in validation['questions']]==[x['question'] for x in questions]
for x,s in zip(validation['questions'],scope):
    assert [f['literal_scope_fact'] for f in x['asked_clause_validation']]==s['asked_facts']
    assert all(f['source_supported'] for f in x['asked_clause_validation'])
    assert x['key_status']=='no_material_false_outcome_found'
assert report['verdict']['accepted_new_mechanism_gaps']==report['verdict']['material_false_key_defects']==0
expected=[]
for f in manifest:
    p=resolve(f['file']);text=p.read_text();assert H(p)==f['sha256'] and len(text)==f['unicode_chars'];cursor=0
    for a,z in f['ranges']:
        assert a==cursor and a<z<=len(text) and z-a<=5500
        expected.append({'path':str(p),'start':a,'end':z,'source_sha256':H(p),'slice_sha256':HB(text[a:z].encode()),'text':text[a:z]});cursor=z
    assert cursor==len(text)
assert len(expected)==61
actor='01a1b5b3-519b-74c0-81b5-4f04552311d0';parent='01a1b3fc-466c-7322-8413-9e59ff041286'
rt=next(Path('/mnt/c/Users/jonny/.codex/sessions/2026/11/07').glob('*'+actor+'.jsonl'))
tree=ast.parse((B/'check-spirit-source09-delivery.py').read_text());fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='strings');ns={'json':json};exec(compile(ast.Module(body=[fn],type_ignores=[]),'<public-string-walker>','exec'),ns)
matches=[[] for _ in expected];images=[];ends=[];contexts=[];calls=[];flags=[]
for n,line in enumerate(rt.open(),1):
    o=json.loads(line);v=o.get('payload',{})
    if o.get('type')=='session_meta':assert v['id']==actor and v['parent_thread_id']==parent and v['agent_path']=='/root/coverage_fresh_final_94'
    elif o.get('type')=='turn_context':contexts.append({'record':n,'model':v.get('model'),'effort':v.get('effort')})
    elif o.get('type')=='event_msg' and v.get('type')=='task_complete':ends.append(n)
    elif o.get('type')=='response_item':
        if v.get('type') in ('function_call','custom_tool_call'):
            text=v.get('input',v.get('arguments',''));name=v.get('name','')
            assert not re.search(r'(?:spawn_agent|list_agents|get_agent_info|read_thread|wait_threads|send_message_to_thread|web__run)',name+' '+text)
            if any(t in text for t in ['summary-snapshot.md','rules/new-angeles.md','reader-a.json','reader-b.json','/grading/','coverage-unexposed-signoff/','/sessions/']):flags.append({'record':n,'public_call_sha256':HB(line.encode())})
            calls.append({'record':n,'name':name,'raw_record_sha256':HB(line.encode())})
        elif v.get('type') in ('function_call_output','custom_tool_call_output'):
            out=v.get('output');values=list(ns['strings'](out))
            for i,e in enumerate(expected):
                if any(e['text'] in t or json.dumps(e['text'],ensure_ascii=False)[1:-1] in t for t in values):matches[i].append({'record':n,'raw_record_sha256':HB(line.encode())})
            if isinstance(out,list):
                for index,x in enumerate(out):
                    if not isinstance(x,dict) or x.get('type')!='input_image':continue
                    url=x.get('image_url');url=url.get('url') if isinstance(url,dict) else url
                    assert isinstance(url,str) and url.startswith('data:') and ';base64,' in url
                    b=base64.b64decode(url.split(';base64,',1)[1],validate=True)
                    images.append({'record':n,'block':index,'sha256':HB(b),'bytes':len(b),'detail':x.get('detail'),'raw_record_sha256':HB(line.encode())})
assert ends and contexts and all(c['model']=='gpt-6.1-sol' and c['effort']=='high' for c in contexts)
assert not flags,flags
assert all(any(m['record']<max(ends) for m in match) for match in matches)
pixel_checks=[];pdfs={}
for e in native:
    source=Path(e['source']);out=Path(e['output']);assert H(source)==e['source_sha256'] and H(out)==e['output_sha256']
    with Image.open(out) as output:
        assert list(output.size)==e['output_dimensions']
        if source.suffix=='.pdf':
            doc=pdfs.setdefault(str(source),fitz.open(source));page=doc[e['page_one_based']-1]
            assert list(page.rect)==e['page_rect'];pix=page.get_pixmap(matrix=fitz.Matrix(e['scale'],e['scale']),alpha=False)
            reconstructed=Image.frombytes('RGB',(pix.width,pix.height),pix.samples).convert(output.mode)
        else:
            with Image.open(source) as im:
                assert list(im.size)==e['source_dimensions'];im=im.convert(output.mode);reconstructed=Image.new(output.mode,tuple(e['output_dimensions']))
                for r in e['rectangles']:
                    rect=r['rect'];dest=r['output_rect'];assert rect[2]-rect[0]==dest[2]-dest[0] and rect[3]-rect[1]==dest[3]-dest[1]
                    reconstructed.paste(im.crop(rect),tuple(dest[:2]))
        assert output.size==reconstructed.size and output.tobytes()==reconstructed.tobytes(),e['id']
    delivered=[x for x in images if x['record']<max(ends) and x['sha256']==e['output_sha256'] and x['detail']=='original'];assert delivered,e['id']
    pixel_checks.append({'id':e['id'],'path':str(out),'sha256':H(out),'source':str(source),'source_sha256':H(source),'independently_pixel_equal':True,'native_pdf':source.suffix=='.pdf','actual_original_payloads':delivered})
proof={'verified':True,'checked_at_utc':datetime.now(timezone.utc).isoformat(),'actor':actor,'runtime_path':str(rt),'runtime_sha256_at_check':H(rt),'all_actual_contexts':contexts,'whole_text_file_count':6,'whole_text_ranges':61,'actual_complete_text_deliveries':[dict({k:v for k,v in e.items() if k!='text'},actual_public_outputs=match) for e,match in zip(expected,matches)],'native_derivative_count':67,'actual_original_image_payload_count':len(images),'native_pixel_lineages':pixel_checks,'all94_literal_questions_and_272_asked_vectors_bound':True,'fresh_supported_scope_saturation':report['verdict'],'authority_limits':load(A/'source-limits.json')['authority_limits'],'report_path':str(A/'coverage-review.json'),'report_sha256':H(A/'coverage-review.json'),'validation_sha256':H(A/'all94-scope-key-source-validation.json'),'public_tool_calls':calls,'flagged_forbidden_reads':flags,'limits':['A genuinely new independent source/key/coverage challenge; no guide, readers, grades or old review maps/ledgers supplied. Initialactualfork settings checked separately from originalParent rawspawn.','Native67 derivative views all exactly match assigned original pixels or independently reproducedFitz2.0PDFpages; this does not make community module scripts authority.','Zero newdistinctmechanism proposals supports working saturation within the explicit supported scope, not all conceivable instances/combinations.','Arrestpriority/impossibleplacement remain unresolved; specificinvestmentreadings and no generic stack/revival claims remain qualified. No unqualifiedcompletecore/reader/stamp/publication approval.']}
out=B/'coordinator-checks/new-angeles-fresh94-coverage-actual-delivery-and-scope-acceptance.json';assert not out.exists();out.write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps({'verified':True,'whole_text_files':6,'ranges':61,'native_pixels_and_actual_payloads':67,'pdf_views':sum(x['native_pdf'] for x in pixel_checks),'N':94,'proof':str(out)}))
