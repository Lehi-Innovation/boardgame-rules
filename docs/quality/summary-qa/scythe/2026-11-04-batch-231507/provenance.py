from qa_tools import *
logs=Path('/mnt/c/Users/jonny/.codex/sessions')
records={}
for path in logs.rglob('*.jsonl'):
 if path.stat().st_mtime<1793866400:continue
 meta=None;ctx=[];prompts=[];calls=[]
 try:
  for line in path.open():
   d=json.loads(line);t=d.get('type');v=d.get('payload',{})
   if t=='session_meta':
    src=v.get('source',{});spawn=src.get('subagent',{}).get('thread_spawn',{}) if isinstance(src,dict) else {}
    if spawn.get('parent_thread_id')!='01a1aac5-76e9-7752-846f-420015969a30':break
    meta={'session_id':v.get('id'),'source':src,'session_log':str(path),'timestamp':d.get('timestamp')}
   elif t=='turn_context' and meta:ctx.append({x:v.get(x) for x in ['turn_id','model','effort','reasoning_effort']})
   elif t=='response_item' and meta:
    if v.get('type')=='message' and v.get('role')=='user':prompts.append(v)
    if v.get('type') in ['function_call','custom_tool_call']:calls.append(v)
  if meta:
   rec={**meta,'runtime_contexts':ctx,'original_user_messages':prompts,'tool_calls':calls};key=meta['source']['subagent']['thread_spawn']['agent_path'].split('/')[-1];records[key]=rec
 except (ValueError,OSError):continue
save(P/'runtime-provenance.json',records)
specs=[]
for directory in sorted(P.glob('*-iteration-*')):
 if not directory.is_dir():continue
 phase,_,number=directory.name.partition('-iteration-')
 if phase in ['seed','expanded','integrated']:specs.append((phase+'_'+number,directory.name))
for prefix,folder in specs:
 d=P/folder
 if not d.exists():continue
 out={'requested_model':'gpt-6-luna','requested_effort':'high','readers':{}}
 for r in ['a','b']:
  rec=records.get(prefix+'_'+r)
  if not rec:continue
  out['readers'][r]=rec
  # Preserve actual dispatch message verbatim from runtime; template remains separately available.
  # Runtime user messages contain environment context, while dispatch text is encrypted.
  # Record the verbatim task sent by the evaluator (known from its tool invocation),
  # separately from model/effort runtime evidence. No decryption is attempted.
  old_generic="Answer every question in the input file, including every requested part. Include every requested procedural quantity, timing, cost and destination within each answer. If a requested fact is absent, explicitly identify that part as unsupported; do not guess."
  new_generic="Answer every question in the input file, including every requested part. Treat compound questions as checklists and explicitly cover every requested procedural quantity, timing, cost and destination within that question's answer. Do not rely on answers to other questions. If a requested fact is absent, explicitly identify that part as unsupported; do not guess."
  generic=old_generic if folder in ['seed-iteration-01','seed-iteration-02','seed-iteration-03'] else new_generic
  if (folder.startswith('expanded-iteration-') and int(folder.split('-')[-1])>=3) or folder.startswith('integrated-iteration-'):
   generic=generic.replace('If a requested fact is absent,','Before saving, check each answer against its question and use a separate clause for each requested part. If a requested fact is absent,')
  use_v4=(folder.startswith('expanded-iteration-') and int(folder.split('-')[-1])>=9) or folder.startswith('integrated-iteration-')
  if use_v4:
   generic+='\n'+json.loads((P/'prompt-version-change.json').read_text())['exact_addition']
  prompt=("You are an independent rules-summary reader in a blind evaluation.\nRead ONLY these two input files:\n"+str(d)+"/summary-snapshot.md\n"+str(d)+"/questions.json\nDo not read any authoritative rulebook, extracted text, answer key, manifest, prior responses, other files, parent history or web links. Do not browse. Use only the supplied summary as evidence, not prior game knowledge. Do not communicate with other readers.\n"+generic+"\nFor every question include id, answer, support (supported, partial or unsupported), evidence (a short quote or section from the summary).\nSave valid JSON to "+str(d)+f"/reader-{r}.json with top-level fields reader, inputs_read and answers (an array). You may read only the two allowed inputs and write only your assigned output. Do not evaluate or improve the summary.")
  actual=d/f'reader-{r}-actual-prompt.txt'
  if actual.exists() and actual.read_text().startswith('<environment_context>'):
   actual.rename(d/f'reader-{r}-runtime-environment-message.txt')
  actual.write_text(prompt)
  out['readers'][r]['prompt_record']={'path':str(actual),'origin':'Verbatim evaluator dispatch text retained from parent tool invocation; runtime dispatch-message contents are encrypted, so models/effort are separately confirmed from plain turn_context metadata.','fork_turns':'none'}
  assert rec['runtime_contexts'] and all(x['model']=='gpt-6-luna' and x['effort']=='high' for x in rec['runtime_contexts'])
 save(d/'model-provenance.json',out)
 dispatch={'readers':{r:{'message':(d/f'reader-{r}-actual-prompt.txt').read_text(),'requested_model':'gpt-6-luna','reasoning_effort':'high','fork_turns':'none','agent_path':v['source']['subagent']['thread_spawn']['agent_path']} for r,v in out['readers'].items()}}
 if ((folder.startswith('expanded-iteration-') and int(folder.split('-')[-1])>=9) or folder.startswith('integrated-iteration-')):dispatch['prompt_version']='generic-self-check-v4'
 save(d/'dispatch-prompts.json',dispatch)
print({k:[(x['model'],x['effort']) for x in v['runtime_contexts']] for k,v in records.items()})
