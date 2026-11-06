from pathlib import Path
import json,hashlib,shutil
P=Path(__file__).parent;D=P/'expanded-iteration-05'
# Verbatim transcription of the visible spawn_agent message in this chat.
# Runtime logs encrypt the message field; do not claim decrypted runtime text.
records={}
root_calls={}
for f in Path('/mnt/c/Users/jonny/.codex/sessions/2026/11').rglob('*01a1aa59-bae3-71a3-afd7-182f8b7a1490.jsonl'):
 for line in f.open():
  x=json.loads(line);y=x.get('payload',{})
  if y.get('type')!='function_call' or y.get('name')!='spawn_agent':continue
  a=json.loads(y['arguments'])
  if a.get('task_name') in ['expanded_certify_a','expanded_certify_b']:
   root_calls[a['task_name']]={'runtime_path':str(f),'timestamp':x.get('timestamp'),'ordinal':x.get('ordinal'),'call_id':y.get('call_id'),'requested_model':a['model'],'reasoning_effort':a['reasoning_effort'],'fork_turns':a['fork_turns'],'message_encrypted_in_runtime_log':True}
for who in ['a','b']:
 prompt=f'''You are an independent rules-summary reader in a blind evaluation.
Read ONLY these two input files:
{D.resolve()}/summary-snapshot.md
{D.resolve()}/questions.json
Do not read any authoritative rulebook, extracted text, answer key, manifest, prior responses, grading/material-facts files, audit findings, other files, parent history or web links. Do not browse or follow links. Use only supplied summary as evidence, not prior game knowledge. Do not communicate with other readers.
Answer every question in the input file, including every requested part. If a requested fact is absent, explicitly identify that part as unsupported; do not guess. For each question include id, answer, support (supported, partial or unsupported), evidence (short quote or section from summary).
Save valid JSON to {D.resolve()}/reader-{who}.json with top-level reader, inputs_read and answers (array). You may read only the two allowed inputs and write only your assigned output. Do not evaluate or improve the summary. Use python3 if needed.'''
 f=D/f'reader-{who}-prompt.txt';assert not f.exists();f.write_text(prompt)
 actor='expanded_certify_'+who;settings=root_calls[actor];assert settings['requested_model']=='gpt-6-luna' and settings['reasoning_effort']=='high' and settings['fork_turns']=='none'
 records[who]={'actor':actor,'prompt_path':f.name,'prompt_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'dispatch_runtime_evidence':settings,'actual_model_provenance':'model-provenance.json'}
(D/'reader-prompt-record.json').write_text(json.dumps({'record_type':'Exact final reader dispatch prompts','plaintext_provenance':'Verbatim transcription of the visible collaboration.spawn_agent messages in this chat. Runtime logs retain encrypted message fields; plaintext was not decrypted or claimed to be independently recovered from those encrypted fields.','historical_boundary':'This record covers expanded-iteration-05 only. It does not imply identical wording for earlier reader prompts.','readers':records},indent=2)+'\n')
old=P/'evidence-hashes.json';backup=P/'evidence-hashes.pre-prompt-record.json';assert not backup.exists();shutil.copyfile(old,backup);inventory=json.loads(old.read_text())
for f in [D/'reader-a-prompt.txt',D/'reader-b-prompt.txt',D/'reader-prompt-record.json']:inventory[str(f.relative_to(P))]=hashlib.sha256(f.read_bytes()).hexdigest()
old.write_text(json.dumps(dict(sorted(inventory.items())),indent=2)+'\n');print('Recorded two exact final prompts;',len(inventory),'evidence hashes; original100 hashes preserved.')
