#!/usr/bin/env python3
"""Independent initial transport audit; reads no key or factual findings.
Answers/evidence are opaque: only whole-file hashes, receipts and continuation metadata
are examined. Never converts an oversized payload into bounded deliveries.
"""
from pathlib import Path
import collections, datetime, hashlib, json, re
IT=Path(__file__).resolve().parent
ROOT=IT.parent
FILES={}; CHECKS=collections.Counter(); ERRORS=[]
def sha(x):return hashlib.sha256(x.encode() if isinstance(x,str) else x).hexdigest()
def read(p):
 p=Path(p).resolve();b=p.read_bytes();FILES[str(p)]={'bytes':len(b),'sha256':sha(b)};return b
def ck(ok,name,ctx=None):
 CHECKS[name]+=1
 if not ok:ERRORS.append({'check':name,'context':ctx})
 return bool(ok)
def public_text(x,depth=0):
 if depth>10:return []
 if isinstance(x,list):return [t for a in x for t in public_text(a,depth+1)]
 if isinstance(x,dict):return [t for k,v in x.items() if k in ['text','output','content','value'] for t in public_text(v,depth+1)]
 if not isinstance(x,str):return []
 choices=[x.strip()]+[x.split(m,1)[1].strip() for m in ['Output:\n\n','Output:\n'] if m in x]
 for s in choices:
  if s.startswith(('{','[')):
   try:
    decoded=public_text(json.loads(s),depth+1)
    if decoded:return decoded
   except ValueError:pass
 return [x]
def runtime(path):
 b=Path(path).read_bytes();lines=b.splitlines(keepends=True)
 return {'path':str(path),'bytes':len(b),'observed_prefix_sha256':sha(b),'lines':lines,'rows':[json.loads(l) for l in lines]}
def proof(rt,i):return {'runtime_path':rt['path'],'record_ordinal_zero_based':i,'timestamp':rt['rows'][i].get('timestamp'),'record_sha256_including_lf':sha(rt['lines'][i])}
def outs(rt):return [(i,public_text(o['payload'].get('output'))) for i,o in enumerate(rt['rows']) if o.get('payload',{}).get('type') in ['custom_tool_call_output','function_call_output']]
def pointer(v,p):
 for k in p.split('/')[1:]:v=v[int(k)] if isinstance(v,list) else v[k.replace('~1','/').replace('~0','~')]
 return v
def merged(ranges):
 result=[]
 for a,b in sorted(ranges):
  if a==b:continue
  if result and a<=result[-1][1]:result[-1][1]=max(result[-1][1],b)
  else:result.append([a,b])
 return result
def missing(ranges,n):
 result=[];at=0
 for a,b in merged(ranges):
  if a>at:result.append([at,a])
  at=max(at,b)
 if at<n:result.append([at,n])
 return result

data={n:read(IT/n) for n in ['summary-snapshot.md','reader-questions-final.json']}
qdoc=json.loads(data['reader-questions-final.json']);process=qdoc['reader_process']
process_hash=sha(process['instructions'])
ck(process_hash==process['instructions_sha256'],'embedded_instruction_digest')
# The opaque serialized question records are not interpreted or assessed.
original_question_records=qdoc.pop('questions')
provenance=json.loads(read(ROOT/'model-provenance.json'));agents={a['task']:a for a in provenance['agents']}
rootrt=runtime(agents['/root']['runtime_source_path']);spawn={};followups=collections.defaultdict(list);messages=collections.defaultdict(list)
for i,o in enumerate(rootrt['rows']):
 p=o.get('payload',{})
 if p.get('type') not in ['function_call','custom_tool_call']:continue
 name=p.get('name')
 if name not in ['spawn_agent','followup_task','send_message']:continue
 try:args=json.loads(p.get('arguments',p.get('input','')))
 except ValueError:continue
 if name=='spawn_agent' and args.get('task_name') in ['expanded5_reader_a','expanded5_reader_b']:
  spawn['/root/'+args['task_name']]=dict(proof(rootrt,i),settings={k:v for k,v in args.items() if k!='message'})
 elif args.get('target','').removeprefix('/root/') in ['expanded5_reader_a','expanded5_reader_b']:
  target='/root/'+args['target'].removeprefix('/root/')
  (followups if name=='followup_task' else messages)[target].append(proof(rootrt,i))

READERS=[];NORMALIZED=[]
for label in 'ab':
 task='/root/expanded5_reader_'+label
 # JSON parsing is mechanical. Only declared transport/process metadata is retained;
 # semantic answers and evidence are neither inspected, printed nor graded.
 raw=read(IT/f'reader-{label}.json');snap=read(IT/f'reader-{label}-batch-01.json')
 current=json.loads(raw)
 current_continuation=current.get('continuation')
 del current
 saved=json.loads(snap);metadata={k:saved[k] for k in ['reader','instructions_read','inputs_read','method_code_sha256','continuation']}
 del saved
 ck(metadata['continuation']=={'completed_count':10,'next_record_index_zero_based':10,'bank_complete':False},'initial_fixed_boundary_metadata',label)
 ck(metadata['method_code_sha256']==process['method_code_sha256'],'declared_embedded_method_hash',label)
 instructions=metadata['instructions_read']
 if isinstance(instructions,dict):irecs=[instructions['question_file_process_metadata']];external=instructions.get('no_external_instruction_file') is True
 else:irecs=[x for x in instructions if isinstance(x,dict)];external='no_external_instruction_file' in instructions
 ck(external,'no_external_instruction_metadata',label)
 imeta=[]
 for rec in irecs:
  target=pointer(qdoc,rec['json_pointer']);declared=rec.get('instructions_sha256',rec.get('sha256'))
  # A digest-valued method-code pointer labels the code digest, not a hash of the
  # hexadecimal digest string. Both readers use the valid sha256 metadata alias.
  actual=sha(target) if rec['json_pointer'].endswith('/instructions') else target
  ck(rec['path']==str(IT/'reader-questions-final.json') and declared==actual,'instruction_receipt_alias_digest',{'reader':label,'pointer':rec['json_pointer']})
  imeta.append({'json_pointer':rec['json_pointer'],'sha256_alias':declared,'matches_target_digest':declared==actual})
 rt=runtime(agents[task]['runtime_source_path']);outputs=outs(rt)
 allcontexts=[(i,o) for i,o in enumerate(rt['rows']) if o.get('type')=='turn_context']
 first_attempt=min(i for i,o in enumerate(rt['rows']) if o.get('payload',{}).get('type') in ['custom_tool_call','function_call'] and any(w in o.get('payload',{}).get('input',o.get('payload',{}).get('arguments','')) for w in ['write_text(','write_bytes(']))
 contexts=[(i,o) for i,o in allcontexts if i<first_attempt]
 ck(len(contexts)==1,'actual_initial_reader_turn_count',task)
 for i,o in contexts:ck(o['payload'].get('model')=='gpt-6-luna' and o['payload'].get('effort')=='high','actual_initial_reader_model_effort',task)
 meta=rt['rows'][0]['payload'];ck(meta.get('id')==agents[task]['identity'] and meta.get('agent_path')==task,'actual_reader_identity',task)
 ck(meta.get('parent_thread_id')==agents['/root']['identity'],'actual_reader_parent',task)
 ck(spawn[task]['settings'].get('fork_turns')=='none' and spawn[task]['settings'].get('model')=='gpt-6-luna' and spawn[task]['settings'].get('reasoning_effort')=='high','actual_requested_reader_spawn',task)
 ck(not [x for x in followups[task] if x['timestamp']<rt['rows'][first_attempt]['timestamp']],'no_root_continuation_before_initial_write_attempt',task)
 attempts=[]
 for i,o in enumerate(rt['rows']):
  p=o.get('payload',{});text=p.get('input',p.get('arguments',''))
  if p.get('type') in ['custom_tool_call','function_call'] and isinstance(text,str) and any(w in text for w in ['write_text(','write_bytes(']):attempts.append(i)
 ck(bool(attempts),'write_containing_initial_call_present',task)
 cutoff=min(attempts)
 # This conservative cutoff precedes the first attempted reader-output-producing
 # code. Failed attempts and later saves are separately recorded, never backdated.
 files=[];allbounded=True;allactual=True;diagnostics=[]
 for i,ts in outputs:
  trunc=any('Warning: truncated output' in t or re.search(r'\d+ tokens truncated',t) for t in ts)
  if trunc or any('Traceback (most recent call last):' in t for t in ts) or any(len(t)>6500 for t in ts):
   diagnostics.append(dict(proof(rt,i),before_conservative_write_cutoff=i<cutoff,truncated=bool(trunc),traceback=any('Traceback (most recent call last):' in t for t in ts),maximum_actual_public_text_characters=max(map(len,ts),default=0)))
 for rec in metadata['inputs_read']:
  name=Path(rec['path']).name;b=data[name];s=b.decode();ctx={'reader':label,'file':name}
  ck(rec['path']==str(IT/name),'sole_frozen_input_path',ctx)
  ck(rec['bytes']==len(b) and rec['characters']==len(s) and rec['sha256']==sha(b),'declared_input_sizes_full_hash',ctx)
  charmatches=[];bytematches=[]
  for c in rec['chunks']:
   a,z=c['start'],c['end'];h=c.get('sha256',c.get('utf8_chunk_sha256'))
   charmatches.append(0<=a<z<=len(s) and sha(s[a:z])==h)
   bytematches.append(0<=a<z<=len(b) and sha(b[a:z])==h)
  mode='unicode_characters' if all(charmatches) else ('utf8_bytes' if all(bytematches) else 'inconsistent')
  ck(mode!='inconsistent','receipt_unit_consistent_interpretation',ctx)
  ranges=[];bounded_ranges=[];blocks=[];declared_pos=0
  for c in rec['chunks']:
   a,z=c['start'],c['end'];h=c['sha256']
   ck(a==declared_pos,'declared_ranges_contiguous_in_actual_unit',dict(ctx,start=a,end=z));declared_pos=z
   if mode=='utf8_bytes':
    text=b[a:z].decode('utf-8');uc_a=len(b[:a].decode('utf-8'));uc_z=len(b[:z].decode('utf-8'));byte_a,byte_z=a,z
   else:
    text=s[a:z];uc_a,uc_z=a,z;byte_a=len(s[:a].encode());byte_z=len(s[:z].encode())
   ck(h==sha(text),'original_receipt_chunk_hash_in_proven_offset_unit',dict(ctx,start=a,end=z,unit=mode))
   found=[i for i,ts in outputs if i<cutoff and any(text in t for t in ts)]
   # Exact original result sizes establish compliant delivery. Do not take an
   # oversized/truncated result and split its remaining text into new blocks.
   bounded=[i for i,ts in outputs if i<cutoff and any(text in t and len(t)<=6500 and 'Warning: truncated output' not in t and not re.search(r'\d+ tokens truncated',t) for t in ts) and len(text)<=5800]
   if found:ranges.append([uc_a,uc_z])
   if bounded:bounded_ranges.append([uc_a,uc_z])
   allactual=allactual and bool(found);allbounded=allbounded and bool(bounded)
   blocks.append({'original_receipt':c,'inferred_original_offset_unit':mode,'start_char':uc_a,'end_char':uc_z,'start_byte':byte_a,'end_byte':byte_z,'unicode_characters':len(text),'utf8_sha256':sha(text),'declared_hash_matches':h==sha(text),'actual_public_matches_before_cutoff':[proof(rt,i) for i in found],'bounded_original_delivery_matches_before_cutoff':[proof(rt,i) for i in bounded]})
   if bounded:NORMALIZED.append({'reader':label,'path':str(IT/name),'original_unit':mode,'original_start':a,'original_end':z,'start_char':uc_a,'end_char_exclusive':uc_z,'start_byte':byte_a,'end_byte_exclusive':byte_z,'utf8_chunk_sha256':sha(text),'unicode_characters':len(text),'runtime_proofs':[proof(rt,i) for i in bounded]})
  ck(declared_pos==(len(b) if mode=='utf8_bytes' else len(s)),'declared_receipt_eof_in_actual_unit',ctx)
  files.append({'path':str(IT/name),'bytes':len(b),'unicode_characters':len(s),'sha256':sha(b),'inferred_receipt_offset_unit':mode,'declared_chunk_count':len(blocks),'declared_chunk_hashes_matching_unicode_interpretation':sum(charmatches),'declared_chunk_hashes_matching_byte_interpretation':sum(bytematches),'complete_declared_chunks_visible_before_cutoff':sum(bool(x['actual_public_matches_before_cutoff']) for x in blocks),'complete_declared_chunks_bounded_before_cutoff':sum(bool(x['bounded_original_delivery_matches_before_cutoff']) for x in blocks),'complete_declared_chunk_visibility_char_ranges':merged(ranges),'bounded_proven_char_ranges':merged(bounded_ranges),'missing_bounded_char_ranges':missing(bounded_ranges,len(s)),'chunks':blocks})
 # Independently measure contiguous surviving prefix/suffix from the single
 # oversized result; these are visibility observations, never bounded receipt repair.
 oversized_survivors=[]
 for i,ts in outputs:
  if i>=cutoff:continue
  for text in ts:
   if len(text)<=6500:continue
   for name,b in data.items():
    s=b.decode();prefix=text.find(s[:200]);suffix=text.find(s[-200:]);observed=[]
    if prefix>=0:
     n=0
     while n<len(s) and prefix+n<len(text) and s[n]==text[prefix+n]:n+=1
     if n>=200:observed.append({'start_char':0,'end_char':n,'payload_start_char':prefix,'payload_end_char':prefix+n,'kind':'exact_surviving_prefix'})
    if suffix>=0:
     end=suffix+200;n=0
     while n<len(s) and end-n-1>=0 and s[len(s)-n-1]==text[end-n-1]:n+=1
     if n>=200:observed.append({'start_char':len(s)-n,'end_char':len(s),'payload_start_char':end-n,'payload_end_char':end,'kind':'exact_surviving_suffix'})
    for hit in observed:oversized_survivors.append(dict(proof(rt,i),path=str(IT/name),**hit,qualifies_as_bounded_delivery=False))
 for f in files:
  extra=[[x['start_char'],x['end_char']] for x in oversized_survivors if x['path']==f['path']]
  f['measured_raw_source_visible_ranges_including_oversized_survivors']=merged(f['complete_declared_chunk_visibility_char_ranges']+extra)
  f['missing_raw_source_char_ranges_after_measured_survivors']=missing(f['measured_raw_source_visible_ranges_including_oversized_survivors'],f['unicode_characters'])
 # A's decoded first/last process excerpts do not establish whole question-file coverage.
 proc_observations=[];question_excerpt_observations=[]
 for i,ts in outputs:
  if i>=cutoff:continue
  for t in ts:
   candidate=t.lstrip()
   if candidate.startswith('['):
    try:
     decoded,end=json.JSONDecoder().raw_decode(candidate)
     if isinstance(decoded,list) and decoded and decoded==original_question_records[:len(decoded)]:
      question_excerpt_observations.append(dict(proof(rt,i),original_record_index_start=0,original_record_index_end_exclusive=len(decoded),exact_question_records=True,establishes_entire_file=False))
    except ValueError:pass
  for a,z in [(0,1500),(len(process['instructions'])-2500,len(process['instructions']))]:
   if any(process['instructions'][a:z] in t for t in ts):proc_observations.append(dict(proof(rt,i),decoded_process_start_char=a,decoded_process_end_char=z,establishes_entire_file=False))
 READERS.append({'reader':label,'task':task,'identity':agents[task]['identity'],'runtime_path':rt['path'],'runtime_observed_prefix_sha256':rt['observed_prefix_sha256'],'runtime_bytes_observed':rt['bytes'],'session_record':proof(rt,0),'initial_prewrite_turn_contexts':[dict(proof(rt,i),model=o['payload'].get('model'),effort=o['payload'].get('effort')) for i,o in contexts],'later_turn_contexts_excluded_from_initial_proof':[dict(proof(rt,i),model=o['payload'].get('model'),effort=o['payload'].get('effort')) for i,o in allcontexts if i>=cutoff],'root_spawn':spawn[task],'root_continuations':followups[task],'root_messages_to_reader':messages[task],'raw_snapshot_sha256':sha(snap),'raw_output_sha256':sha(raw),'raw_snapshot_equals_current_output':raw==snap,'later_current_output_continuation_metadata':current_continuation,'snapshot_authority_policy':'batch-01 is the authoritative unchanged initial snapshot; a later cumulative output may legitimately differ and is excluded from initial input proof','continuation_metadata':metadata['continuation'],'raw_instruction_receipt':instructions,'instruction_receipt_alias_verification':imeta,'conservative_first_write_containing_call':proof(rt,cutoff),'write_containing_call_ordinals':attempts,'all_declared_chunks_actually_visible_before_cutoff':bool(allactual),'complete_bounded_initial_delivery_verified_before_cutoff':bool(allbounded),'technical_transport_verdict':'PASS_WITH_BYTE_OFFSET_METADATA_NORMALIZATION' if allbounded and all(f['inferred_receipt_offset_unit']=='utf8_bytes' for f in files) else ('PASS' if allbounded else 'FAIL_INCOMPLETE_PREWRITE_BOUNDED_DELIVERY'),'files':files,'oversized_surviving_source_fragments':oversized_survivors,'decoded_process_excerpt_observations':proc_observations,'decoded_question_record_excerpt_observations':question_excerpt_observations,'transport_diagnostics':diagnostics})

live_hash_changes=[]
for path,meta in list(FILES.items()):
 if Path(path).name in ['reader-a.json','reader-b.json','model-provenance.json']:
  now=sha(Path(path).read_bytes())
  if now!=meta['sha256']:live_hash_changes.append({'path':path,'hash_when_read':meta['sha256'],'hash_at_final_check':now,'policy':'Live cumulative output or provenance changed externally; initial snapshots and frozen inputs remain authoritative.'})
 else:ck(sha(Path(path).read_bytes())==meta['sha256'],'all_initial_snapshots_and_frozen_inputs_unchanged_during_audit',path)
selftask='/root/expanded4_bookkeeping_auditor_23';selfmodel=[]
if selftask in agents:
 selfrt=runtime(agents[selftask]['runtime_source_path'])
 for i,o in enumerate(selfrt['rows']):
  if o.get('type')=='turn_context':
   selfmodel.append(dict(proof(selfrt,i),model=o['payload'].get('model'),effort=o['payload'].get('effort')))
   ck(o['payload'].get('model')=='gpt-6.1-sol' and o['payload'].get('effort')=='high','auditor_actual_model_effort_unchanged',i)
report={'audit':'Initial transport technical audit 23; continuation of own technical-only work','created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'iteration':str(IT),'scope':'Initial two-reader pre-save input transport only. No answer semantics, keys, factual findings, gameplay grades or source-authority judgment assessed.','technical_verdict':'FAIL_PAIR_INITIAL_DELIVERY; A incomplete, B independently normalized byte offsets prove complete bounded initial delivery','verification_script':{'path':str(Path(__file__).resolve()),'sha256':sha(Path(__file__).read_bytes())},'independent_check_count':sum(CHECKS.values()),'independent_checks_by_category':dict(CHECKS),'unexpected_verifier_failures':ERRORS,'reader_results':READERS,'normalized_actual_bounded_ranges':NORMALIZED,'auditor_actual_model_contexts':selfmodel,'observed_data_hashes':FILES,'live_cumulative_or_provenance_changes_during_audit':live_hash_changes,'important_limits':['Parent timing clarification says B resumed its fixed answer schedule and A received a transport-only continuation after the initial first10. These later turns/cumulative changes do not repair the historical initial proof.',
 'The parent initial validation result was not read or used as an oracle. All original raw snapshots, receipts and frozen data remain unchanged. Iteration04 report/script were untouched.','Receipt sha256 alias and UTF-8-byte start/end interpretation are technical metadata normalization only. B normalization maps each original actually delivered byte block to its exact Unicode boundaries; no extra blocks or saved-reader fields are invented.','A oversize/truncated result is retained as a diagnostic and its surviving prefix/suffix visibility is measured. It is never divided into artificial compliant blocks. Later decoded question/process excerpts do not establish complete original file visibility.','Delivery proof conservatively ends at the earliest write-containing call, even if that attempt fails before the actual reader-output file is written. Later successful saves and post-save tool reads are never counted as pre-save input delivery.','Later same-identity turn contexts are recorded but excluded from the original first-turn transport proof; no later output is used to repair initial visibility.',
 'Task message bodies are encrypted in external runtime logs. Actual root fork_turns:none requests and child identities/model contexts are observed separately; runtime fork field and saved-prompt plaintext equality are unavailable. No ciphertext is copied.','Input visibility is not semantic comprehension. This report does not alter grades, impose a gameplay cap, or certify global readiness. Root runtime hash describes its observed append-only prefix.']}
out=IT/'initial-transport-technical-audit-23.json';out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'output':str(out),'checks':sum(CHECKS.values()),'unexpected_failures':len(ERRORS),'readers':[{'reader':x['reader'],'verdict':x['technical_transport_verdict'],'cutoff':x['conservative_first_write_containing_call']['record_ordinal_zero_based'],'files':[{'file':Path(f['path']).name,'unit':f['inferred_receipt_offset_unit'],'bounded_chunks':f['complete_declared_chunks_bounded_before_cutoff'],'total_chunks':f['declared_chunk_count'],'bounded_missing':f['missing_bounded_char_ranges'],'observed_visible':f['measured_raw_source_visible_ranges_including_oversized_survivors'],'raw_missing':f['missing_raw_source_char_ranges_after_measured_survivors']} for f in x['files']]} for x in READERS]},ensure_ascii=False))
