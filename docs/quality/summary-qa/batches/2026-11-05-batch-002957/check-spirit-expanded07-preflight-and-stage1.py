"""Bind unchanged173 inputs, generic prompts, and actual empty-stage input deliveries."""
import ast,hashlib,json
from datetime import datetime,timezone
from pathlib import Path
B=Path(__file__).resolve().parent;R=B.parents[4]
G=R/'docs/quality/summary-qa/spirit-island'/B.name;D=G/'expanded-iteration-07'
J=lambda p:json.loads(p.read_text());HB=lambda b:hashlib.sha256(b).hexdigest();H=lambda p:HB(p.read_bytes())
m=J(D/'input-manifest.json');old=G/'expanded-iteration-06';bindings=[]
for path,metadata in m['inputs'].items():
    p=Path(path);assert H(p)==metadata['sha256'] and len(p.read_text())==metadata['characters'];bindings.append({'path':path,'sha256':H(p)})
assert H(D/'summary-snapshot.md')==H(R/'rules/spirit-island.md')=='ce8f1d645f466686ae2e75fcd29130fa89cbb1c4963d981090e3768a526a6fd1'
assert (D/'questions.json').read_bytes()==(old/'questions.json').read_bytes()
assert (D/'asked-fact-map.json').read_bytes()==(old/'asked-fact-map.json').read_bytes()
assert m['inputs'][m['key_path']]['sha256']==J(old/'input-manifest.json')['inputs'][m['key_path']]['sha256']
assert m['source_hashes']==J(old/'input-manifest.json')['source_hashes']
assert len(J(D/'questions.json')['questions'])==m['question_count']==173
for path,h in m['source_hashes'].items():assert H(Path(path))==h
template=Path(m['reader_protocol']['template_path']).read_text()
assert H(Path(m['reader_protocol']['template_path']))==m['reader_protocol']['template_sha256']=='62a935cc6e0aba9c9b9cb23a69520c772adedcb5e212994c13412c1c8731783b'
prompts={}
for who in 'ab':
    p=D/f'reader-{who}-prompt.txt';native=p.read_text()
    assert H(p)==m['reader_prompt_sha256'][who]
    assert p.read_bytes()==(G/'expanded07-planned-reader-instructions'/p.name).read_bytes()
    rendered=template.format(summary=str(D/'summary-snapshot.md'),questions=str(D/'questions.json'),output=str(D/f'reader-{who}.json'))
    assert native.startswith(rendered)
    code=native.split('```python\n',1)[1].rsplit('\n```',1)[0]
    assert m['reader_protocol']['embedded_generic_method_sha256'] in [HB(code.encode()),HB((code+'\n').encode())]
    prompts[who]=native.replace(str(D/f'reader-{who}.json'),'OUTPUT')
assert prompts['a']==prompts['b']
tree=ast.parse((B/'check-spirit-source09-delivery.py').read_text());fn=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='strings');ns={'json':json};exec(compile(ast.Module(body=[fn],type_ignores=[]),'<strings>','exec'),ns)
actors={'a':'01a1b6a1-e9e8-7892-b1fe-1ebe5290d359','b':'01a1b6a3-692e-7b31-8bc5-25d3e6a9b3be'};readers=[]
for who,actor in actors.items():
    ready=D/'pre-authoring-attempt-01-originals'/f'reader-{who}-delivery-ready.json';data=J(ready);freeze=J(D/'pre-authoring-attempt-01-originals'/f'reader-{who}-delivery-ready-freeze.json')
    assert H(ready)==freeze['sha256'] and data['stage']=='delivery_ready' and data['answers']==[]
    runtime=next(Path('/mnt/c/Users/jonny/.codex/sessions/2026/11/07').glob('*'+actor+'.jsonl'))
    lines=runtime.read_bytes().splitlines(keepends=True);received=[];writes=[];contexts=[];ends=[]
    for n,line in enumerate(lines,1):
        row=json.loads(line);p=row.get('payload',{})
        if row.get('type')=='session_meta':assert p['id']==actor and p['parent_thread_id']=='01a1ac01-c763-7bb1-901e-7458891630b8'
        if row.get('type')=='turn_context':contexts.append((p.get('model'),p.get('effort')))
        if row.get('type')=='event_msg' and p.get('type')=='task_complete':ends.append(n)
        if row.get('type')=='response_item':
            if p.get('type') in ['function_call','custom_tool_call']:
                code=p.get('input',p.get('arguments',''))
                assert not any(x in code for x in ['answer-key.json','asked-fact-map.json','source-audit-final','extracted/','source_pdfs/','read_thread','list_agents','web__run',f'reader-{"b" if who=="a" else "a"}.json'])
                if f'reader-{who}.json' in code and any(x in code for x in ['write_text','writeFile','apply_patch','json.dump',"open('w')",'open("w")']):writes.append(n)
            if p.get('type') in ['function_call_output','custom_tool_call_output']:received.append((n,HB(line),list(ns['strings'](p.get('output')))))
        if row.get('type')=='event_msg' and p.get('type')=='item_completed':
            item=p.get('item',{})
            if item.get('type')=='CommandExecution':received.append((n,HB(line),list(ns['strings'](item.get('aggregated_output','')))))
    assert contexts and all(x==('gpt-6-luna','high') for x in contexts) and writes,(who,contexts,writes,ends)
    checks=[]
    for f in data['inputs_read']:
        path=Path(f['path']);assert path in [D/'summary-snapshot.md',D/'questions.json'];text=path.read_text()
        assert H(path)==f['sha256'] and len(text)==f.get('characters',f.get('character_length')) and f['output_cap_tokens']>=4000
        cursor=0;parts=[]
        for a,z in f['read_ranges']:
            assert a==cursor and a<z<=len(text) and z-a<=6000
            hits=[{'record':n,'record_sha256':h} for n,h,values in received if n<min(writes) and any(text[a:z] in v for v in values)]
            assert hits,(who,path.name,a,z)
            parts.append({'start':a,'end':z,'sha256':HB(text[a:z].encode()),'actual_outputs':hits});cursor=z
        assert cursor==len(text)
        checks.append({'path':str(path),'sha256':H(path),'parts':parts})
    assert len(checks)==2
    readers.append({'actor':actor,'reader':who,'runtime':str(runtime),'runtime_sha256':H(runtime),'empty_readiness_sha256':H(ready),'first_readiness_writer_record':min(writes),'actual_inputs':checks})
proof={'verified':True,'checked_at_utc':datetime.now(timezone.utc).isoformat(),'N':173,'bank':'expanded-v24','bound_inputs':bindings,'all79_source_hashes_current':True,'literal_Q_key_and_fact_map_unchanged_from06':True,'native_prompts_exact_planned_and_same_except_output':True,'generic_template_sha256':m['reader_protocol']['template_sha256'],'unchanged_inline_helper_sha256':m['reader_protocol']['embedded_generic_method_sha256'],'readers':readers,'parallel_source_status_at_dispatch_honestly_pending':m['independent_source_audit']['own_note_correction_pending'],'current_source_semantic_acceptance':'spirit-C26-source15-own-correction-and-semantic-acceptance.json','limits':['Both preserved original readiness files have zero answers. Actual complete two-file inputs precede first saved readiness output; no private cognition claim. B initially combined the last two guide slices in one6517-character output, explicitly preserved in pre-authoring-first-actual-source-match-diagnostic.json. Later same-reader separate retransmission is a technical-only check before authoring, not a factual cap or a new reader trial.','Fresh spawn requests/model cohort verified separately. Same original staged tasks continue without factual feedback; drafts and final originals must be preserved.','No factual grades, source/publication stamping or final completion claimed.']}
out=B/'coordinator-checks/spirit-expanded07-C26-fixed173-generic-method-and-stage1.json';assert not out.exists();out.write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps({'verified':True,'N':173,'readers':2,'actual_full_input_ranges':sum(len(f['parts']) for r in readers for f in r['actual_inputs']),'proof':str(out)}))
