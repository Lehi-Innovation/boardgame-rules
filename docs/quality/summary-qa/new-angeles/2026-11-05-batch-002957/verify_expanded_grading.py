from pathlib import Path
import collections, hashlib, json, sys
B=Path(__file__).parent.resolve();I=B/(sys.argv[1] if len(sys.argv)>1 else 'expanded-luna-iteration-01');G=I/'grading';iteration_number=int(I.name.rsplit('-',1)[-1])
def sha(x):return hashlib.sha256(x).hexdigest()
def canon(x):return json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
def strings(x):
    if isinstance(x,str):
        yield x
        if x[:1] in ['{','[']:
            try:yield from strings(json.loads(x))
            except (ValueError,TypeError):pass
    elif isinstance(x,list):
        for y in x:yield from strings(y)
    elif isinstance(x,dict):
        for k,y in x.items():
            if k not in ['encrypted_content','internal_chat_message_metadata_passthrough']:yield from strings(y)
manifest=json.loads((G/'input-manifest.json').read_text());meta={x['task']:x for x in json.loads((B/'runtime-provenance.json').read_text())}
output_manifest=json.loads((I/'reader-output-manifest.json').read_text()) if (I/'reader-output-manifest.json').exists() else {}
raw={l:{x['id']:x for x in json.loads(Path(output_manifest.get(l,I/f'reader-{l}.json')).read_text())['answers']} for l in ['a','b']}
report={'status':'partial checkpoint','blocks':[],'raw_grade_links':[],'counts':{},'technical_diagnostics':[],'asked_fact_vector_checks':[]};totals=collections.Counter();all_pairs=[]
for block in manifest['blocks']:
    packpath=Path(block['pack']);assert sha(packpath.read_bytes())==block['pack_sha256'];pack=json.loads(packpath.read_text());promptpath=Path(block['prompt']);assert sha(promptpath.read_bytes())==block['prompt_sha256']
    for l,entries in pack['complete_raw_reader_entries'].items():assert entries==[raw[l][i] for i in block['ids']]
    output=Path(block['output'])
    if not output.exists():continue
    d=json.loads(output.read_text());entries=d.get('grades',d.get('records',d.get('entries',[])));expected={(l,i) for l in ['a','b'] for i in block['ids']}
    actual={(x['reader'].replace('reader_',''),x['id']) for x in entries};assert actual==expected and len(entries)==len(expected)
    task=f'/root/expanded{iteration_number}_grader_'+str(block['block']).zfill(2);m=meta[task];tool_outputs=[]
    for ordinal,line in enumerate(Path(m['runtime_log_path']).open(),1):
        r=json.loads(line);v=r.get('payload',{})
        if r['type']=='response_item' and v.get('type')=='custom_tool_call_output':tool_outputs.append((ordinal,sha(line.encode()),list(strings(v.get('output')))))
    prompt=promptpath.read_text();prompt_matches=[{'record_ordinal':n,'record_sha256':h} for n,h,items in tool_outputs if any(prompt in s for s in items)];assert prompt_matches and len(prompt)<=5500
    annotation=G/'literal-scope-annotation-v1.json';annotation_receipt=None
    if annotation.exists():
        text=annotation.read_text();hits=[{'record_ordinal':n,'record_sha256':h} for n,h,items in tool_outputs if any(text in s for s in items)]
        assert hits and len(text)<=5500
        annotation_receipt={'path':str(annotation),'sha256':sha(annotation.read_bytes()),'actual_full_text_matches':hits}
    receipts=[]
    for x in d['inputs_read']:
        p=Path(x.get('path',x.get('file',x.get('filename'))));source=p.read_text();ranges=x.get('ranges',x.get('ranges_read',x.get('unicode_ranges',x.get('chunks'))));assert ranges,'Missing actual ranges'
        bounds=[(r[0],r[1]) if isinstance(r,list) else (r.get('start',r.get('unicode_start',r.get('start_inclusive'))),r.get('end',r.get('unicode_end',r.get('end_exclusive')))) for r in ranges];matches=[]
        for start,end in bounds:
            chunk=source[start:end];hits=[{'record_ordinal':n,'record_sha256':h} for n,h,items in tool_outputs if any(chunk in s for s in items)]
            matches.append({'start':start,'end':end,'characters':len(chunk),'range_sha256':sha(chunk.encode()),'actual_tool_payload_matches':hits,'complete':bool(hits) and 0<len(chunk)<=5500})
        contiguous=bounds[0][0]==0 and bounds[-1][1]==len(source) and all(a[1]==b[0] for a,b in zip(bounds,bounds[1:]));receipts.append({'path':str(p),'sha256':sha(p.read_bytes()),'ranges':matches,'complete':contiguous and all(r['complete'] for r in matches)})
    required={str(I/'summary-snapshot.md'),str(packpath)};assert required.issubset({x['path'] for x in receipts});assert all(x['complete'] for x in receipts)
    for x in entries:
        l=x['reader'].replace('reader_','');i=x['id'];assert x['label'] in ['Correct','Partial','Incorrect'];assert x['raw_entry_sha256']==sha(canon(raw[l][i]));all_pairs.append((l,i));totals[(l,x['label'])]+=1
        if iteration_number>=3:
            required=next(v['asked_facts'] for v in pack['asked_clause_map'] if v['id']==i)
            assessed=[v['asked_fact'] if 'asked_fact' in v else v['required_clause'] for v in x['asked_fact_assessments']]
            assert assessed==required,('Asked-fact vector mismatch',l,i)
            report['asked_fact_vector_checks'].append({'reader':l,'id':i,'required_fact_count':len(required),'all_original_required_facts_assessed_in_order':True,'fixed_required_vector_sha256':sha(canon(required))})
        report['raw_grade_links'].append({'reader':l,'id':i,'raw_entry_sha256':x['raw_entry_sha256'],'grade_record_sha256':sha(canon(x)),'grade_file':str(output),'grade_file_sha256':sha(output.read_bytes())})
        if x.get('material_wrong_claims') and x['label']!='Incorrect':report['technical_diagnostics'].append({'reader':l,'id':i,'issue':'Nonempty material_wrong_claims with non-Incorrect label; semantic review required, no automatic label rewrite.'})
    report['blocks'].append({'block':block['block'],'actual_complete_input_delivery':True,'process_instruction_delivery':{'path':str(promptpath),'sha256':block['prompt_sha256'],'actual_full_text_matches':prompt_matches},'literal_scope_annotation_delivery':annotation_receipt,'receipts':receipts,'actual_model_effort_verified':m['model_effort_verified'],'fork_turns':m['fork_turns'],'records':len(entries),'grade_file_sha256':sha(output.read_bytes())})
assert len(all_pairs)==len(set(all_pairs));report['counts']={l:{label:totals[(l,label)] for label in ['Correct','Partial','Incorrect']} for l in ['a','b']};report['all_expected_records_present']=len(all_pairs)==manifest['expected_grade_records'];report['status']='all primary grades linked and delivered; semantic/adjudication gates separate' if report['all_expected_records_present'] else 'partial checkpoint'
report['original_required_fact_assessments_verified']=sum(x['required_fact_count'] for x in report['asked_fact_vector_checks'])
(I/'primary-grading-integrity.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'blocks_verified':len(report['blocks']),'records':len(all_pairs),'counts':report['counts'],'complete':report['all_expected_records_present'],'diagnostics':len(report['technical_diagnostics'])}))
