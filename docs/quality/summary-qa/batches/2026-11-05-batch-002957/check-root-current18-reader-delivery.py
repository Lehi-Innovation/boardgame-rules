"""Independently bind complete current81 inputs despite filename-only raw receipts."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,hashlib
B=Path(__file__).resolve().parent;ROOT=B.parents[4]
G=ROOT/'docs/quality/summary-qa/root'/B.name;V=G/'current-snapshot-revalidation-2026-11-07';D=V/'iteration-01'
J=lambda p:json.loads(p.read_text());HB=lambda b:hashlib.sha256(b).hexdigest();H=lambda p:HB(p.read_bytes())
tree=ast.parse((B/'check-spirit-source09-delivery.py').read_text());fn=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='strings');ns={'json':json};exec(compile(ast.Module(body=[fn],type_ignores=[]),'<strings>','exec'),ns)
ids=[x['id'] for x in J(D/'questions.json')['questions']];assert len(ids)==81
actors={'a':'01a1b63b-4bd2-7d91-b408-6bd669a728ab','b':'01a1b63b-9a73-7760-ac27-6b5999854e0e'};checks=[]
for who,actor in actors.items():
    raw=D/('reader-'+who+'.json');output=J(raw);assert [x['id'] for x in output['answers']]==ids
    runtime=next(Path('/mnt/c/Users/jonny/.codex/sessions/2026/11/07').glob('*'+actor+'.jsonl'));lines=runtime.read_bytes().splitlines(keepends=True)
    rows={n:json.loads(line) for n,line in enumerate(lines,1)};writes=[];terminals=[];contexts=[];calls=[]
    for n,row in rows.items():
        p=row.get('payload',{})
        if row.get('type')=='session_meta':assert p['id']==actor and p['parent_thread_id']=='01a1aa9d-614e-7493-a3f2-715a8c52e03d'
        if row.get('type')=='turn_context':contexts.append({'record':n,'model':p.get('model'),'effort':p.get('effort')})
        if row.get('type')=='event_msg' and p.get('type')=='task_complete':terminals.append(n)
        if row.get('type')=='response_item' and p.get('type') in ['function_call','custom_tool_call']:
            text=p.get('input',p.get('arguments',''))
            assert not any(x in text for x in ['answer-key.json','grading-scope-policy','/benchmark-v10/','/source-only-audit/','extracted/','source_pdfs/','read_thread','list_agents','get_agent_info','web__run','reader-'+('b' if who=='a' else 'a')+'.json'])
            if raw.name in text and any(x in text for x in ['write_text','writeFile','apply_patch',"open('w')",'open(\"w\")']):writes.append(n)
            calls.append({'record':n,'name':p.get('name'),'record_sha256':HB(lines[n-1])})
    assert writes and terminals and max(terminals)>max(writes)
    assert contexts and all(x['model']=='gpt-6-luna' and x['effort']=='high' for x in contexts)
    boundary=min(writes);audit_path=D/('reader-'+who+'-delivery-initial/delivery-audit.json');audit=J(audit_path)
    assert Path(audit['runtime_path'])==runtime
    call_index={x['read_index']:x for x in audit['read_calls']};files=[];received=[]
    for ordinal,row in rows.items():
        payload=row.get('payload',{})
        if row.get('type')=='response_item' and payload.get('type') in ['function_call_output','custom_tool_call_output']:
            received.append((ordinal,list(ns['strings'](payload.get('output')))))
        if row.get('type')=='event_msg' and payload.get('type')=='item_completed':
            item=payload.get('item',{})
            if item.get('type')=='CommandExecution':received.append((ordinal,list(ns['strings'](item.get('aggregated_output','')))))
    for f in audit['inputs']:
        path=Path(f['path']);assert path in [D/'summary-snapshot.md',D/'questions.json'] and H(path)==f['sha256']
        source=path.read_text().splitlines(keepends=True);cursor=0;parts=[]
        assert len(source)==f['total_lines']
        for span in f['ordered_exact_matching_ranges']:
            a,z=span['source_lines'];assert a==cursor+1 and a<=z<=len(source)
            call=call_index[span['read_index']]
            part=''.join(source[a-1:z])
            matched=[{'raw_record':n,'raw_record_sha256':HB(lines[n-1])} for n,values in received if n<boundary and any(part in value.replace('\r\n','\n') for value in values)]
            assert matched,(who,str(path),a,z)
            parts.append({'line_start_1based':a,'line_end_inclusive':z,'unicode_characters':len(part),'slice_sha256':HB(part.encode()),'actual_output_records':matched,'parent_normalized_call_index':call});cursor=z
        assert cursor==len(source)
        files.append({'path':str(path),'sha256':H(path),'complete_literal_input_including_blank_lines':True,'parts':parts})
    assert len(files)==2
    checks.append({'reader':who,'actor':actor,'runtime':str(runtime),'runtime_sha256':H(runtime),'raw_sha256':H(raw),'original_raw_inputs_read_metadata':output['inputs_read'],'receipt_qualification':'Original output lists only filenames. Actual full text including blank lines is independently bound to original runtime before first writer; no metadata omission penalty.','first_writer_record':boundary,'last_completed_turn_record':max(terminals),'contexts':contexts,'input_files':files,'public_call_trace':calls,'parent_initial_delivery_index_sha256':H(audit_path)})
proof={'verified':True,'checked_at_utc':datetime.now(timezone.utc).isoformat(),'N':81,'summary_sha256':H(D/'summary-snapshot.md'),'canonical_matches':H(D/'summary-snapshot.md')==H(ROOT/'rules/root.md'),'readers':checks,'limits':['Exact initial full two-file logical UTF8 text and original81 IDs checked; CRLF transport is normalized only for comparison, pinned file hashes preserve exact originals.','Model/fresh-spawn requests verified separately. Parent prefixgrading chronology recorded separately, never relayed as readerfeedback.','No grade/source/publication/goal-complete approval.']}
out=B/'coordinator-checks/root-current18-complete-reader-actual-delivery.json';assert not out.exists();out.write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps({'verified':True,'N':81,'readers':2,'actual_full_input_ranges':sum(len(f['parts']) for x in checks for f in x['input_files']),'proof':str(out)}))
