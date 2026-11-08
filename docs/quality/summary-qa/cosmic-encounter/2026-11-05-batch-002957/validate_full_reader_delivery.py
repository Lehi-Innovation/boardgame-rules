"""Validate a future full-bank pair using explicit dispatch bindings and runtime data."""
from pathlib import Path
import hashlib
import json
import sys

R=Path(__file__).parent.resolve()
def sha(b): return hashlib.sha256(b).hexdigest()
def read(p): return json.loads(p.read_text())
def texts(value):
    if isinstance(value,str):
        yield value
        try:
            parsed=json.loads(value)
            if isinstance(parsed,(dict,list)):
                yield from texts(parsed)
                return
        except ValueError: pass
        if '\n' in value:
            for line in value.splitlines():
                if not line.startswith(('{','[')): continue
                try: parsed=json.loads(line)
                except ValueError: continue
                if isinstance(parsed,(dict,list)): yield from texts(parsed)
    elif isinstance(value,list):
        for item in value: yield from texts(item)
    elif isinstance(value,dict):
        for key in ['output','text','content']:
            if key in value: yield from texts(value[key])

it=(R/sys.argv[1]).resolve()
assert it.is_relative_to(R)
dest=it/'delivery-validation.json'
assert not dest.exists(),'Never overwrite an earlier delivery report'
manifest=read(it/'input-manifest.json')
assert manifest.get('full_bank_freeze_authorized') is True
bindings=read(it/'dispatch-bindings.json')['readers']
assert {x['label'] for x in bindings}=={'a','b'} and len(bindings)==2
provenance=read(R/'model-provenance.json')
expected=[x['id'] for x in read(it/'questions.json')['questions']]
allowed={(it/'summary-snapshot.md').resolve(),(it/'questions.json').resolve()}
reports=[];normalized_prompts=[]
for binding in bindings:
    agent=next(x for x in provenance['agents'] if x['task']==binding['task'])
    path=Path(binding['output_path']);assert path==it/f"reader-{binding['label']}.json"
    prompt_path=Path(binding['prompt_path']);prompt=prompt_path.read_text()
    assert sha(prompt_path.read_bytes())==binding['submitted_prompt_sha256']
    normalized_prompts.append(prompt.replace(str(path),'OUTPUT_PATH'))
    output=read(path);records=[]
    for index,raw in enumerate(Path(agent['runtime_source_path']).open()):
        row=json.loads(raw);p=row.get('payload',{})
        if p.get('type')=='custom_tool_call_output':
            records.append(({'ordinal':row.get('ordinal',index),'record_sha256':sha(raw.encode())},list(texts(p.get('output')))))
    files=[]
    for declared in output['inputs_read']:
        input_path=Path(declared['path']).resolve();assert input_path in allowed
        value=input_path.read_text();last=0;chunks=[]
        for c in declared['chunks']:
            start,end=c['start'],c['end'];chunk=value[start:end]
            proof=[p for p,contents in records if any(chunk in t for t in contents)]
            chunks.append({'start':start,'end':end,'contiguous':start==last,'bounded':0<end-start<=6000,'sha256':sha(chunk.encode()),'declared_hash_matches':c['sha256']==sha(chunk.encode()),'exact_actual_model_visible_delivery':bool(proof),'runtime_proof':proof})
            last=end
        result={'path':str(input_path),'sha256':sha(input_path.read_bytes()),'frozen_hash_matches':manifest['sha256'][str(input_path)]==sha(input_path.read_bytes()),'declared_full_hash_matches':declared['sha256']==sha(input_path.read_bytes()),'full_contiguous_coverage':last==len(value) and all(c['contiguous'] for c in chunks),'chunks':chunks}
        result['pass']=result['frozen_hash_matches'] and result['declared_full_hash_matches'] and result['full_contiguous_coverage'] and all(c['bounded'] and c['declared_hash_matches'] and c['exact_actual_model_visible_delivery'] for c in chunks)
        files.append(result)
    actual=[x['id'] for x in output['answers']]
    rr={'reader':binding['label'],'identity':agent['identity'],'task':binding['task'],'raw_output_sha256':sha(path.read_bytes()),'submitted_prompt_sha256':binding['submitted_prompt_sha256'],'actual_model_and_effort_verified':agent['settings_verified'],'actual_settings':agent['turn_records'],'fresh_context_request':binding['fork_turns'],'runtime_fork_setting':None,'context_limit':'Explicit fork_turns:none submitted request; external runtime identity metadata does not expose a separate fork-turns field.','runtime_prompt_body_verification':None,'prompt_limit':'Runtime task body is encrypted; submitted literal prompt and hash are preserved. No encrypted instructions copied.','ids_exactly_once_in_order':actual==expected and len(set(actual))==len(expected),'files':files}
    rr['pass']=rr['actual_model_and_effort_verified'] and binding['fork_turns']=='none' and rr['ids_exactly_once_in_order'] and len(files)==2 and {x['path'] for x in files}=={str(p) for p in allowed} and all(x['pass'] for x in files)
    reports.append(rr)
same=normalized_prompts[0]==normalized_prompts[1]
report={'iteration':it.name,'reader_count':2,'identical_submitted_protocol_except_output_path':same,'readers':reports,'pass':same and all(x['pass'] for x in reports),'method':'Complete actual model-visible text is checked independently from declared receipts; requested settings are distinguished from runtime-verified model/effort and unavailable prompt/fork metadata.'}
dest.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print(it.name,report['pass'])
