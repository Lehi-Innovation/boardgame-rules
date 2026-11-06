"""Audit model-visible tool-output text; missing matches require inspection, never factual reader feedback."""
from pathlib import Path
import collections,datetime,hashlib,json,re,sys
R=Path(__file__).resolve().parent
D=R/sys.argv[1]
provenance=json.loads((R/sys.argv[2]).read_text())
trial=int(D.name.rsplit('-',1)[1])
def norm(s):return re.sub(r'\s+',' ',s).strip()
def texts(value):
    if isinstance(value,list):
        for x in value:yield from texts(x)
    elif isinstance(value,dict):
        for x in value.values():yield from texts(x)
    elif isinstance(value,str):
        yield value
        try:p=json.loads(value)
        except ValueError:p=None
        if p is not None and p!=value:yield from texts(p)
summary=(D/'summary-snapshot.md').read_text()
lines=[(i,s) for i,s in enumerate(summary.splitlines(),1) if s.strip()]
questions=json.loads((D/'questions.json').read_text())['questions']
records=[]
for side in 'ab':
    name='/root/source_continuation_reader'+str(trial)+'_'+side
    meta=next(x for x in provenance['records'] if x['agent_path']==name)
    visible=[];outer=collections.Counter();nested=collections.Counter();contacts=[];outputs=0
    with Path(meta['runtime_log']).open() as f:
        for line in f:
            try:o=json.loads(line)
            except ValueError:continue
            p=o.get('payload',{})
            if o.get('type')!='response_item':continue
            if p.get('type') in ['custom_tool_call','function_call']:outer[p.get('name')]+=1
            if p.get('type')=='custom_tool_call':nested.update(re.findall(r'tools\.([A-Za-z_0-9]+)',p.get('input','')))
            if p.get('type')=='function_call' and p.get('name')=='send_message':
                a=json.loads(p['arguments']) if isinstance(p['arguments'],str) else p['arguments']
                contacts.append({'timestamp':o.get('timestamp'),'target':a.get('target'),'body_runtime_opaque':True})
            if p.get('type')=='custom_tool_call_output':
                outputs+=1
                visible.extend(texts(p.get('output')))
    extra=[]
    for text in visible:
        for match in re.finditer(r'"(?:[^"\\]|\\.)*"',text):
            try:v=json.loads(match.group())
            except ValueError:continue
            if isinstance(v,str):extra.append(v)
    corpus=norm('\n'.join(visible+extra))
    missing_lines=[i for i,s in lines if norm(s) not in corpus]
    missing_questions=[q['id'] for q in questions if norm(q['question']) not in corpus]
    records.append({'reader':side,'runtime_log':meta['runtime_log'],'tool_output_blocks':outputs,'nonblank_summary_lines':len(lines),'summary_lines_matched':len(lines)-len(missing_lines),'missing_summary_line_numbers':missing_lines,'questions_matched':len(questions)-len(missing_questions),'missing_question_ids':missing_questions,'all_summary_lines_and_questions_visible_by_exact_normalized_text':not missing_lines and not missing_questions,'outer_tools':dict(outer),'nested_tools':dict(nested),'outbound_contacts':contacts,'cross_reader_contact_observed_in_direct_tools':any(x['target']!='/root' for x in contacts),'actual_model_settings_confirmed':meta['requested_model_high_forknone_confirmed']})
report={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checkpoint':sys.argv[4] if len(sys.argv)>4 else 'Completed reader sessions','trial':D.name,'summary_sha256':hashlib.sha256((D/'summary-snapshot.md').read_bytes()).hexdigest(),'question_sha256':hashlib.sha256((D/'questions.json').read_bytes()).hexdigest(),'method':'Union of actual custom-tool-output text across both reader contexts; normalize whitespace and decode JSON string literals. Match every nonblank frozen Summary line and every complete question. No task/system/reasoning body inspection or decryption.','limits':'Text visibility is not attention, factual completion or grade. Missing matches need raw-output inspection for formatting/truncation before conclusions. Own draft output may repeat source text; this audit reports visible text, not provenance of every repetition. It does not fully audit shell file/network access. No missing-ID/fact feedback to readers.','readers':records,'no_zero_communication_claim':True}
with (R/sys.argv[3]).open('x') as f:json.dump(report,f,indent=2);f.write('\n')
print(json.dumps([{k:x[k] for k in ['reader','summary_lines_matched','nonblank_summary_lines','questions_matched','missing_question_ids','all_summary_lines_and_questions_visible_by_exact_normalized_text']} for x in records]))
