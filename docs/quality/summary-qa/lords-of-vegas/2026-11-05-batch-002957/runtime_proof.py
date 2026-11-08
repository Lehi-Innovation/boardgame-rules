import json,hashlib,sys
from datetime import datetime
from pathlib import Path
R=Path(__file__).parent.resolve(); parent='01a1b2c1-d5d1-7333-8948-72708b3d1f3e'
h=lambda b:hashlib.sha256(b).hexdigest()
def decode_texts(v):
 out=[]
 if isinstance(v,str):
  out.append(v)
  try:
   z=json.loads(v)
   if isinstance(z,(dict,list)):out += decode_texts(z)
  except (ValueError,TypeError):pass
 elif isinstance(v,list):
  for z in v:out += decode_texts(z)
 elif isinstance(v,dict):
  # Losslessly decode semantic strings in arbitrary structured tool-result fields,
  # including exact_full_chunk/chunk/text wrappers. Persist no wrapper contents.
  for value in v.values():out += decode_texts(value)
 return out
records=[]
for p in [p for day in ['06','07'] for p in Path(f'/mnt/c/Users/jonny/.codex/sessions/2026/11/{day}').glob('*.jsonl')]:
 try:
  with p.open('rb') as f:first=f.readline()
  meta=json.loads(first); m=meta['payload']
 except:continue
 spawn=m.get('source',{}); spawn=spawn.get('subagent',{}).get('thread_spawn',{}) if isinstance(spawn,dict) else {}
 if m.get('id')!=parent and spawn.get('parent_thread_id')!=parent:continue
 lines=p.read_bytes().splitlines()
 contexts=[]; outputs=[]; output_timestamps={}
 for i,l in enumerate(lines):
  o=json.loads(l);x=o.get('payload',{})
  if o['type']=='turn_context':contexts.append({'record_ordinal_zero_based':i,'record_sha256':h(l),'actual_model':x.get('model'),'actual_effort':x.get('effort'),'timestamp':o.get('timestamp')})
  if o['type']=='response_item' and x.get('type') in ['function_call_output','custom_tool_call_output']:
   v='\n'.join(decode_texts(x.get('output','')))
   outputs.append((i,v,h(l))); output_timestamps[i]=o.get('timestamp')
 task=spawn.get('agent_path','/root'); request_model='gpt-6-luna' if 'reader' in task else 'gpt-6.1-sol'
 rec={'identity':m.get('id'),'parent':spawn.get('parent_thread_id'),'task':task,'fork_context':'none' if spawn else 'root','requested_model':request_model,'requested_effort':'high','runtime_source_path':str(p),'identity_record_ordinal_zero_based':0,'identity_record_sha256':h(lines[0]),'identity_timestamp':meta.get('timestamp'),'turn_contexts':contexts}
 # Verify exact known input chunks appeared in model-visible tool outputs.
 bindings=[]
 if 'reader' in task:
  iteration=next(it for prefix,it in [('expanded_reader10','stamped-iteration-02'),('expanded_reader9','stamped-iteration-01'),('expanded_reader8','expanded-iteration-13'),('expanded_reader7','expanded-iteration-11'),('expanded_reader6','expanded-iteration-10'),('expanded_reader5','expanded-iteration-09'),('expanded_reader4','expanded-iteration-08'),('expanded_reader3','expanded-iteration-06'),('expanded_reader2','expanded-iteration-05'),('expanded_reader','expanded-iteration-03'),('seed_reader2','seed-iteration-02'),('seed_reader','seed-iteration-01')] if task.rsplit('/',1)[-1].startswith(prefix))
  allowed=[R/iteration/'summary-snapshot.md',R/iteration/'questions.json']
 elif 'coverage_challenge' in task:
  allowed=[Path('extracted/lords-of-vegas-rules.txt').resolve(),Path('docs/quality/summary-qa/batches/2026-11-05-batch-002957/source-preflight/lords-of-vegas/unified-2022/mayfair-unified-rulebook.txt').resolve(),R/'expanded-v1/questions.json',R/'expanded-v1/answer-key.json',R/'expanded-v1/scope-map.json',R/'coverage-ledger.json']
 elif 'final_scope_coverage' in task:
  allowed=[Path('extracted/lords-of-vegas-rules.txt').resolve(),Path('docs/quality/summary-qa/batches/2026-11-05-batch-002957/source-preflight/lords-of-vegas/unified-2022/mayfair-unified-rulebook.txt').resolve(),R/'expanded-v2/questions.json',R/'expanded-v2/grading-key.json',R/'expanded-v2/scope-map.json',R/'coverage-ledger-v2.json',R/'expanded-v4/questions.json',R/'expanded-v4/grading-key.json',R/'expanded-v4/scope-map.json',R/'coverage-ledger-v4.json']
 elif 'final_grader' in task and 'block' in task:
  block=task[-1]; iteration=next(it for prefix,it in [('final_grader10','stamped-iteration-02'),('final_grader9','stamped-iteration-01'),('final_grader8','expanded-iteration-13'),('final_grader7','expanded-iteration-11'),('final_grader6','expanded-iteration-10'),('final_grader5','expanded-iteration-09'),('final_grader4','expanded-iteration-08'),('final_grader3','expanded-iteration-06'),('final_grader2','expanded-iteration-05'),('final_grader','expanded-iteration-03')] if task.rsplit('/',1)[-1].startswith(prefix));allowed=[R/iteration/'summary-snapshot.md',R/iteration/f'grader-block-{block}.json']
 elif 'coverage_reopen' in task:
  allowed=[Path('extracted/lords-of-vegas-rules.txt').resolve(),Path('docs/quality/summary-qa/batches/2026-11-05-batch-002957/source-preflight/lords-of-vegas/unified-2022/mayfair-unified-rulebook.txt').resolve(),R/'expanded-v4/questions.json',R/'expanded-v4/scope-map.json',R/'coverage-reopen-candidates.json',R/'expanded-v5/questions.json',R/'expanded-v5/grading-key.json',R/'expanded-v5/scope-map.json',R/'coverage-ledger-v5.json']
 elif 'clean_final_coverage' in task:
  allowed=[Path('extracted/lords-of-vegas-rules.txt').resolve(),Path('docs/quality/summary-qa/batches/2026-11-05-batch-002957/source-preflight/lords-of-vegas/unified-2022/mayfair-unified-rulebook.txt').resolve(),R/'expanded-v6/questions.json',R/'expanded-v6/grading-key.json',R/'expanded-v6/scope-map.json',R/'expanded-v6/bank-freeze-manifest.json',R/'coverage-ledger-v6.json']
 elif 'tie_actor_source_review' in task:
  allowed=[Path('extracted/lords-of-vegas-rules.txt').resolve(),Path('docs/quality/summary-qa/batches/2026-11-05-batch-002957/source-preflight/lords-of-vegas/unified-2022/mayfair-unified-rulebook.txt').resolve()]
 elif 'source_key_v9_review' in task:
  allowed=[Path('extracted/lords-of-vegas-rules.txt').resolve(),Path('docs/quality/summary-qa/batches/2026-11-05-batch-002957/source-preflight/lords-of-vegas/unified-2022/mayfair-unified-rulebook.txt').resolve(),R/'expanded-v9/questions.json',R/'expanded-v9/grading-key.json',R/'expanded-v9/scope-map.json',R/'expanded-v9/bank-freeze-manifest.json',R/'coverage-ledger-v9.json',R/'expanded-v10/questions.json',R/'expanded-v10/grading-key.json',R/'expanded-v10/scope-map.json',R/'expanded-v10/bank-freeze-manifest.json',R/'coverage-ledger-v10.json']
 elif 'source_only_v8_review' in task:
  allowed=[Path('extracted/lords-of-vegas-rules.txt').resolve(),Path('docs/quality/summary-qa/batches/2026-11-05-batch-002957/source-preflight/lords-of-vegas/unified-2022/mayfair-unified-rulebook.txt').resolve(),R/'expanded-v8/questions.json',R/'expanded-v8/grading-key.json',R/'expanded-v8/scope-map.json',R/'expanded-v8/bank-freeze-manifest.json',R/'coverage-ledger-v8.json']
 elif 'source_audit' in task:
  audit_iter='stamped-iteration-01' if 'stamped1' in task else ('expanded-iteration-11' if 'revision3' in task else ('expanded-iteration-07' if 'revision2' in task else 'expanded-iteration-01'))
  allowed=[R/audit_iter/'summary-snapshot.md',Path('extracted/lords-of-vegas-rules.txt').resolve(),Path('docs/quality/summary-qa/batches/2026-11-05-batch-002957/source-preflight/lords-of-vegas/unified-2022/mayfair-unified-rulebook.txt').resolve()]
 elif 'stamped_q27_neutral' in task:
  allowed=[R/'stamped-iteration-01/summary-snapshot.md',Path('docs/quality/summary-qa/batches/2026-11-05-batch-002957/coordinator-checks/lords-stamped01-q27-neutral-packet.json').resolve()]
 else:allowed=[]
 for fp in allowed:
  if not fp.exists():continue
  t=fp.read_text(); spans=[]
  # Testing per-character covered by exact known substrings, including slice boundaries; larger original chunks can contain many slices.
  coverage=[False]*len(t)
  candidate_ranges=set()
  for size in [5000,4999,4800,4500,4000,3000]:
   candidate_ranges.update((start,min(start+size,len(t))) for start in range(0,len(t),size))
  # Some historical readers sliced UTF-8 bytes despite labeling counts as characters.
  # Map only valid complete UTF-8 chunks to exact character spans, then still require
  # the literal decoded substring in a pre-save model-visible tool output.
  encoded=t.encode('utf-8')
  for size in [5000,4800,4500,4000]:
   for start in range(0,len(encoded),size):
    end=min(start+size,len(encoded))
    try:
     cs=len(encoded[:start].decode('utf-8'));ce=len(encoded[:end].decode('utf-8'))
    except UnicodeDecodeError:continue
    candidate_ranges.add((cs,ce))
  if 'reader' in task:
   label=task[-1]
   raw_path=fp.parent/f'reader-{label}.json'
   if raw_path.exists():
    def collect_ranges(v):
     if isinstance(v,dict):
      if v.get('total_characters')==len(t) and isinstance(v.get('chunks'),list):
       for c in v['chunks']:
        if isinstance(c,dict) and 'start' in c and 'end' in c:candidate_ranges.add((c['start'],c['end']))
      for x in v.values():collect_ranges(x)
     elif isinstance(v,list):
      for x in v:collect_ranges(x)
    collect_ranges(json.loads(raw_path.read_text()).get('delivery_receipt',{}))
  if ('final_grader' in task and 'block' in task) or 'stamped_q27_neutral' in task:
   grade_path=R/'stamped-iteration-01/q27-neutral-adjudication.json' if 'stamped_q27_neutral' in task else fp.parent/f'grader-block-{task[-1]}-results.json'
   if grade_path.exists():
    def collect_grader_ranges(v,inherited_path=None):
     if isinstance(v,dict):
      path=v.get('path',v.get('file_path',v.get('filename',inherited_path)))
      if path:
       pp=Path(path);pp=pp if pp.is_absolute() or pp.exists() else fp.parent/pp
       start,end=v.get('start'),v.get('end')
       if pp.resolve()==fp.resolve() and isinstance(start,int) and isinstance(end,int) and 0<=start<end<=len(t):candidate_ranges.add((start,end))
      for x in v.values():collect_grader_ranges(x,path)
     elif isinstance(v,list):
      for x in v:collect_grader_ranges(x,inherited_path)
    report=json.loads(grade_path.read_text());collect_grader_ranges(report.get('delivery_receipts',report.get('delivery_receipt',report.get('complete_delivery_receipts',{}))))
  raw_mtime=None
  if 'reader' in task and (fp.parent/f'reader-{task[-1]}.json').exists():raw_mtime=(fp.parent/f'reader-{task[-1]}.json').stat().st_mtime
  if 'final_grader' in task and 'block' in task and (fp.parent/f'grader-block-{task[-1]}-results.json').exists():raw_mtime=(fp.parent/f'grader-block-{task[-1]}-results.json').stat().st_mtime
  if 'stamped_q27_neutral' in task and (R/'stamped-iteration-01/q27-neutral-adjudication.json').exists():raw_mtime=(R/'stamped-iteration-01/q27-neutral-adjudication.json').stat().st_mtime
  def before_saved(ordinal):
   ts=output_timestamps.get(ordinal)
   return raw_mtime is None or (ts is not None and datetime.fromisoformat(ts.replace('Z','+00:00')).timestamp()<=raw_mtime)
  for start,end in sorted(candidate_ranges):
   part=t[start:end]
   matches=[(ordinal,rh) for ordinal,v,rh in outputs if part in v and before_saved(ordinal)]
   if matches:
    for j in range(start,end):coverage[j]=True
    spans.append({'start':start,'end':end,'substring_sha256':h(part.encode()),'runtime_records':[{'ordinal':o,'record_sha256':rh,'timestamp':output_timestamps.get(o)} for o,rh in matches]})
  bindings.append({'path':str(fp),'sha256':h(fp.read_bytes()),'characters':len(t),'response_output_mtime_utc_epoch':raw_mtime,'delivery_restricted_to_pre_save_outputs':raw_mtime is not None,'all_character_slices_seen':all(coverage),'missing_slices':[i for i in range(0,len(t),500) if not all(coverage[i:i+500])],'exact_model_visible_slice_proof':spans})
 rec['content_delivery_proof']=bindings
 records.append(rec)
(R/'runtime-provenance.json').write_text(json.dumps({'delivery_encoding':'Exact source substrings verified after lossless JSON decoding of nested tool output wrappers; unmodified runtime records remain authority.', 'hygiene':'Only identity, requested/actual settings, task,parent,timestamps,runtime locations/ordinals and opaque record hashes plus exact delivery-range evidence. External runtime logs remain untouched.','agents':records},indent=2)+'\n')
print(json.dumps({'agents':len(records),'models_and_efforts_verified':all(r['turn_contexts'] and all(c['actual_model']==r['requested_model'] and c['actual_effort']=='high' for c in r['turn_contexts']) for r in records),'incomplete_delivery':[r['task']+':'+x['path'] for r in records for x in r['content_delivery_proof'] if not x['all_character_slices_seen']]},indent=2))
