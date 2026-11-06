from pathlib import Path
import json,hashlib,sys,shutil
B=Path(__file__).parent.resolve();D=B/sys.argv[1];names=dict(zip('ab',sys.argv[2:4]));assert len(names)==2
load=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();M=load(D/'input-manifest.json')
pa=(D/'reader-a-prompt.txt').read_text();pb=(D/'reader-b-prompt.txt').read_text();same=pa.replace(str(D/'reader-a.json'),'<OUTPUT>')==pb.replace(str(D/'reader-b.json'),'<OUTPUT>');assert same
proof={'requested_model':'gpt-6-luna','requested_effort':'high','actual_settings_verified':True,'fork_turns_requested_none_verified':True,'prepared_prompts_identical_apart_from_output_path':same,'prompt_evidence_note':'Exact submitted instructions were preserved before dispatch and used verbatim in spawn requests. Local task text is encrypted, so prepared prompt equality is separate from independently verifiable model/effort/fork projections. Minimal metadata references external original records by path/ordinal/hash.','readers':[]};dest=D/'runtime';dest.mkdir(exist_ok=True)
for r,name in names.items():
 meta=load(B/f'runtime/{name}-metadata.json');assert meta['schema']=='minimal-runtime-metadata-v1';settings=meta['confirmed_settings'];assert settings and all(x=={'model':'gpt-6-luna','effort':'high'} for x in settings)
 spawn=meta['requested_spawn'];args=spawn['fields'];assert args['fork_turns']=='none' and args['model']=='gpt-6-luna' and args['reasoning_effort']=='high';assert H(D/f'reader-{r}-prompt.txt')==M['reader_prompt_sha256'][r];raw=load(D/f'reader-{r}.json')
 for suffix in ['metadata','tool-transcript','prompts','task-messages']:
  src=B/f'runtime/{name}-{suffix}.json';out=dest/src.name
  if out.exists():assert out.read_bytes()==src.read_bytes()
  else:shutil.copyfile(src,out)
 transcript=(dest/f'{name}-tool-transcript.json').read_text();warnings=[x for x in ['Warning: truncated output','Output exceeded available model context','output was truncated'] if x.lower() in transcript.lower()]
 proof['readers'].append({'reader':r,'agent':'/root/'+name,'agent_thread_id':meta['thread_id'],'actual_model':settings,'metadata_proof':str(dest/f'{name}-metadata.json'),'delivery_transcript':str(dest/f'{name}-tool-transcript.json'),'task_message_record':str(dest/f'{name}-task-messages.json'),'requested_fork_and_model_proof':spawn,'truncation_warnings':warnings,'inputs_read':raw['inputs_read'],'prompt_sha256':H(D/f'reader-{r}-prompt.txt'),'raw_response_sha256':H(D/f'reader-{r}.json')})
assert len({x['agent_thread_id'] for x in proof['readers']})==2;p=D/'model-provenance.json';assert not p.exists();p.write_text(json.dumps(proof,indent=2,ensure_ascii=False)+'\n');print(json.dumps({'actual_settings_verified':True,'prepared_prompts_equal_except_output':same,'truncation_warnings':{x['reader']:x['truncation_warnings'] for x in proof['readers']}},indent=2))
