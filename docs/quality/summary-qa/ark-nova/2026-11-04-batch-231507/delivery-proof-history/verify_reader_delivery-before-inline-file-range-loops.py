from pathlib import Path
import hashlib,json,re,sys
D=Path(__file__).resolve().parent
iteration,agent_prefix=sys.argv[1:3]
t=D/iteration
runtime=json.loads((D/'runtime-provenance.json').read_text())
h=lambda b:hashlib.sha256(b).hexdigest()
checks={}
for side in 'ab':
    rt=next(x for x in runtime if x['session_meta']['agent_path']==f'/root/{agent_prefix}_{side}')
    calls={x.get('call_id'):x for x in rt['tool_calls'] if 'arguments' in x}
    observed={x['call_id']:x for x in rt['tool_calls'] if x.get('type')=='tool_output_access_summary'}
    outputs={}
    for line in Path(rt['session_log_path']).read_text().splitlines():
        z=json.loads(line).get('payload',{})
        if z.get('type')=='custom_tool_call_output':
            outputs[z['call_id']]=''.join(c.get('text','') for c in z.get('output',[]) if isinstance(c,dict))
    covered={f:set() for f in ['summary-snapshot.md','questions.json']}
    reads=[];trace=[]
    for cid,c in calls.items():
        matches=[(int(m[1]),int(m[2]),m[3]) for m in re.finditer(r"sed -n '([0-9]+),([0-9]+)p'[^\n]*?(summary-snapshot\.md|questions\.json)",c['arguments'])]
        loop=re.search(r'const ranges\s*=\s*(\[\[.*?\]\]);',c['arguments'])
        loop_file=re.search(r"sed -n '\$\{a\},\$\{b\}p'[^\n]*?(summary-snapshot\.md|questions\.json)",c['arguments'])
        if loop and loop_file and re.search(r'for\s*\(const\s*\[a,b\]\s*of\s*ranges\)',c['arguments']):
            for start,end in json.loads(loop[1]):
                assert isinstance(start,int) and isinstance(end,int) and 0<start<=end
                matches.append((start,end,loop_file[1]))
        string_loop=re.search(r'const ranges\s*=\s*(\["[^;\n]*?"\]);',c['arguments'])
        string_file=re.search(r"sed -n '\$\{range\}p'[^\n]*?(summary-snapshot\.md|questions\.json)",c['arguments'])
        if string_loop and string_file and re.search(r'for\s*\(const\s*range\s*of\s*ranges\)',c['arguments']):
            for value in json.loads(string_loop[1]):
                assert re.fullmatch(r'[0-9]+,[0-9]+',value)
                start,end=map(int,value.split(','));assert 0<start<=end
                matches.append((start,end,string_file[1]))
        if not matches:continue
        output=outputs.get(cid,'')
        trace.append({'call_id':cid,'actual_tool_input':c['arguments'],'actual_visible_tool_output':output,'aggregate_truncation_notice':observed.get(cid,{}).get('truncation_notice')})
        for start,end,f in matches:
            lines=(t/f).read_text().splitlines(keepends=True);end=min(end,len(lines));expected=''.join(lines[start-1:end]);full=bool(expected) and expected in output
            reads.append({'call_id':cid,'file':f,'start':start,'end':end,'aggregate_truncation_notice':observed.get(cid,{}).get('truncation_notice'),'full_exact_requested_text_in_actual_visible_output':full,'visible_output_sha256':h(output.encode())})
            if full:covered[f].update(range(start,end+1))
    supplements=t/f'reader-{side}-visible-range-supplements.json'
    if supplements.exists():
        for s in json.loads(supplements.read_text()):
            cid=s['call_id'];f=s['file'];start=s['start'];end=s['end']
            assert any(r['call_id']==cid and r['file']==f and r['start']<=start<=end<=r['end'] for r in reads), 'Supplement must be a subrange of an actual input-reading command'
            expected=''.join((t/f).read_text().splitlines(keepends=True)[start-1:end]);output=outputs[cid]
            assert expected and expected in output, 'Supplement must match the exact complete visible source text'
            reads.append({'call_id':cid,'file':f,'start':start,'end':end,'aggregate_truncation_notice':observed.get(cid,{}).get('truncation_notice'),'full_exact_requested_text_in_actual_visible_output':True,'visible_subrange_of_larger_requested_chunk':True,'visible_output_sha256':h(output.encode()),'supplement_record':supplements.name})
            covered[f].update(range(start,end+1))
    missing={f:sorted(set(range(1,len((t/f).read_text().splitlines())+1))-v) for f,v in covered.items()}
    complete=not any(missing.values())
    forbidden=['SC01 size bands','SC02 mandatory','source-correction','baseline_benchmark','answer-key.json','material-requested-facts.json','independent-grade','grading-request-scope']
    exposures=[{'call_id':cid,'term':s} for cid,o in outputs.items() for s in forbidden if s in o]
    assert not exposures,exposures
    assert all(x['model']=='gpt-6-luna' and x['effort']=='high' for x in rt['turn_contexts'])
    (t/f'reader-{side}-actual-input-output-trace.json').write_text(json.dumps({'agent_path':rt['session_meta']['agent_path'],'session_log_path':rt['session_log_path'],'reads':trace},indent=2)+'\n')
    checks[side]={'actual_model_effort':rt['turn_contexts'],'session_log_path':rt['session_log_path'],'verified_read_calls':reads,'missing_lines':missing,'complete_exact_visible_text_proved':complete,'truncation_recovery_verified':complete,'forbidden_feedback_metadata_exposure_events':exposures,'input_output_trace':f'reader-{side}-actual-input-output-trace.json','other_commands_review':'Evaluator must separately inspect every non-sed tool input for unauthorized knowledge access; this helper establishes exact delivered text, not arbitrary command semantics.'}
q=json.loads((t/'questions.json').read_text());manifest=json.loads((t/'input-manifest.json').read_text());accepted=json.loads((D/manifest['benchmark']/'questions.json').read_text());assert q['questions']==accepted['questions'];assert set(q)=={'game','scope','version','questions'};assert re.fullmatch(r'r\d\d',q['version'])
(t/'input-access-validation.json').write_text(json.dumps({'verdict':'COMPLETE_AUTHORIZED_INPUTS_CONFIRMED' if all(c['complete_exact_visible_text_proved'] for c in checks.values()) else 'INCOMPLETE_AUTHORIZED_INPUT_DELIVERY','summary_lines':len((t/'summary-snapshot.md').read_text().splitlines()),'questions_lines':len((t/'questions.json').read_text().splitlines()),'reader_checks':checks},indent=2)+'\n')
(t/'reader-boundary-validation.json').write_text(json.dumps({'verdict':'CLEAN_READER_ONLY_DELIVERY_CONFIRMED','question_count':len(q['questions']),'all_question_objects_exact_accepted_bank':True,'delivery_copy_exact':(t/'questions.json').read_bytes()==Path(manifest['reader_question_payload']['path']).read_bytes(),'metadata':{k:v for k,v in q.items() if k!='questions'},'actual_public_tool_outputs_checked_both_readers':True,'feedback_metadata_exposure_events':{'a':[],'b':[]},'input_read_proof':'input-access-validation.json'},indent=2)+'\n')
print(iteration,{side:{'complete':c['complete_exact_visible_text_proved'],'missing_counts':{f:len(v) for f,v in c['missing_lines'].items()}} for side,c in checks.items()},'clean metadata confirmed; inspect non-reading calls separately')
