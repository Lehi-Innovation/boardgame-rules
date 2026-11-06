from pathlib import Path
import json,hashlib,shutil,difflib
P=Path(__file__).parent.resolve(); ROOT=P.parents[4]
def sha(f):return hashlib.sha256(Path(f).read_bytes()).hexdigest()
def dump(f,x):Path(f).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def provenance():
 out=[];parent_calls={};parent_path=next(Path('/mnt/c/Users/jonny/.codex/sessions/2026/11/05').glob('*01a1aa94-b6a2-7823-9d8b-2b4a666d8223.jsonl'))
 for li,line in enumerate(parent_path.open(),1):
  rec=json.loads(line);pay=rec.get('payload',{})
  if rec.get('type')=='response_item' and pay.get('name')=='spawn_agent':
   args=json.loads(pay['arguments']);task='/root/'+args['task_name'];settings={'record_line':li,'task':task,'fork_turns':args.get('fork_turns'),'model':args.get('model'),'reasoning_effort':args.get('reasoning_effort'),'task_payload':'encrypted; not inspected or decrypted'};parent_calls.setdefault(task,[]).append(settings)
 dump(P/'parent-spawn-settings.json',{'parent_runtime_path':str(parent_path),'method':'Read unencrypted spawn settings only, without task-payload inspection or decryption. Repeated identical settings can include a failed concurrency-limit attempt; actual child session metadata establishes successful readers.','spawn_calls':[v for vs in parent_calls.values() for v in vs]})
 for f in Path('/mnt/c/Users/jonny/.codex/sessions/2026/11/05').glob('*.jsonl'):
  try:
   lines=f.read_text().splitlines();m=json.loads(lines[0])['payload']; s=m.get('source',{}); spawn=s.get('subagent',{}).get('thread_spawn',{}) if isinstance(s,dict) else {}
   if spawn.get('parent_thread_id')!='01a1aa94-b6a2-7823-9d8b-2b4a666d8223':continue
   ctx=[];prompts=[]
   for i,l in enumerate(lines,1):
    r=json.loads(l)
    if r['type']=='turn_context':ctx.append({'line':i,'model':r['payload'].get('model'),'effort':r['payload'].get('effort')})
    if r['type']=='response_item' and r['payload'].get('type')=='message' and r['payload'].get('role')=='user':
     prompts.append(r['payload'].get('content'))
   out.append({'task':spawn['agent_path'],'session_id':m['id'],'parent_thread_id':spawn['parent_thread_id'],'runtime_path':str(f),'contexts':ctx,'source_metadata':spawn,'parent_spawn_settings':parent_calls.get(spawn['agent_path'],[]),'visible_environment_user_messages':prompts,'task_prompt_inspection':'NEW_TASK/spawn task message payloads are encrypted in runtime logs; not decrypted or recovered. Visible user-role messages are environment context only. reader-*-prompt.txt records the full intended task prompt, not a runtime-recovered delivered body.'})
  except Exception:raise
 dump(P/'model-provenance.json',out);return out

def freeze(name,bank):
 I=P/name;I.mkdir(); b=P/bank
 shutil.copy2(ROOT/'rules/obsession.md',I/'summary-snapshot.md');shutil.copy2(b/'questions.json',I/'questions.json')
 files=[I/'summary-snapshot.md',I/'questions.json',b/'answer-key.json',P/'baseline/obsession-rules.txt',P/'baseline/obsession-universal-rules.pdf',P/'baseline/obsession-corrigendum-1.0.pdf']
 if (P/'publisher-fr-base-rules.pdf').exists():files += [P/'publisher-fr-base-rules.pdf',P/'publisher-fr-base-rules.txt']
 dump(I/'input-manifest.json',{'inputs':[{'path':str(f),'sha256':sha(f)} for f in files],'requested_model':'gpt-6-luna','requested_effort':'high','benchmark':bank,'reader_prompt_version':'v2-generic-pre-submission-completeness-check','prompt_change_authority':'Coordinator game-specific instruction on November5,2026; applies only to pairs dispatched after iteration10.'})
 prev=P/'baseline/obsession.md'
 (I/'summary-changes.patch').write_text(''.join(difflib.unified_diff(prev.read_text().splitlines(True),(I/'summary-snapshot.md').read_text().splitlines(True),fromfile='baseline',tofile=name)))
 for who in ['a','b']:
  prompt=f'''You are an independent rules-summary reader in a blind evaluation.
Read ONLY these two input files:
{I}/summary-snapshot.md
{I}/questions.json
Do not read any authoritative rulebook, extracted text, answer key, manifest, prior responses, other files, parent history or web links. Do not browse. Use only the supplied summary as evidence, not prior game knowledge. Do not communicate with other readers.
Answer every question, including every requested part. Include all requested procedural quantities, timing, costs and destinations in each answer. If a requested fact is absent, explicitly identify that part as unsupported; do not guess.
For every question include id, answer, support (supported, partial or unsupported), and evidence (short quote or section from summary).
Before writing your final JSON, reread each question and review its draft answer on its own. Check that every requested part is explicitly resolved from the supplied summary, including any requested quantities, timing, costs, destinations and exceptions. Do not rely on another answer to fill a gap. If the summary does not resolve a requested part, identify it as unsupported rather than guessing. Check volunteered statements for contradictions with the summary.
Save valid JSON to {I}/reader-{who}.json with top-level fields reader, inputs_read and answers (an array). You may read only the two allowed inputs and write only your assigned output. Do not evaluate or improve the summary.'''
  (I/f'reader-{who}-prompt.txt').write_text(prompt)
 return I
if __name__=='__main__':provenance()
