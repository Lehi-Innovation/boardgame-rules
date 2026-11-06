import sys
sys.dont_write_bytecode=True
from pathlib import Path
import json,hashlib
O=Path(__file__).parent;F=O.parent;sha=lambda b:hashlib.sha256(b).hexdigest();manifest=json.loads((F/'grading-reader-b/packet-manifest.json').read_text());aggregate=json.loads((F/'reader-b-grading-results.json').read_text());agg={e['id']:e for e in aggregate['grades']};a=json.loads((O/'audit.json').read_text());assert a['all_six_technical_audit_complete'];actors={f'/root/v13_stamped_i1_grade_b_{i:02d}' for i in range(1,7)};filtered=[]
def walk(x):
 if isinstance(x,dict):
  if x.get('agent',x.get('actor')) in actors:filtered.append(x)
  else:
   for v in x.values():walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
walk(json.loads((F/'grading-b-terminal-runtime-provenance-01.json').read_text()));assert len(filtered)==6;(O/'six-B-terminal-provenance.json').write_text(json.dumps(filtered,indent=2)+'\n')
proofs={n:json.loads((F/n).read_text()) for n in ['grading-reader-b-input-delivery-proof.json','grading-reader-b-js-format-proposal-proof.json']}
def falses(x,path='',out=None):
 out=[] if out is None else out
 if isinstance(x,dict):
  for k,v in x.items():
   if v is False:out.append(path+'/'+k)
   elif isinstance(v,(dict,list)) and k!='first_possible_artifact_write_boundary':falses(v,path+'/'+k,out)
 elif isinstance(x,list):
  for i,v in enumerate(x):falses(v,path+'/'+str(i),out)
 return out
for block in manifest['blocks']:
 nn=block['block_id'][-2:];d=F/'grading-reader-b'/block['block_id'];packet=json.loads((d/'packet.json').read_text());report=json.loads((d/'grades-same-entry.json').read_text());integrity=json.loads((d/'parent-grade-integrity.json').read_text());hash_=sha((d/'grades-same-entry.json').read_bytes());assert hash_==integrity['original_grade_report_sha256']==aggregate['grade_report_hashes'][str(d/'grades-same-entry.json')];assert sha((d/'packet.json').read_bytes())==block['packet_sha256'];assert [g['id'] for g in report['readers']['reader-b']['grades']]==block['ids']==integrity['complete_ids']
 for e,g in zip(packet['entries'],report['readers']['reader-b']['grades']):
  assert sha(json.dumps(e['reader_b_entry'],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())==block['complete_raw_entry_sha256s'][e['id']]
  assert [x['requirement'] for x in g['material_parts']]==e['requested_fact_scope_entry']['material_requested_facts']
  r=e['reader_b_entry'];texts=[r['answer']]+r.get('case_conclusions',[])+[v.get('quote','') for v in r.get('evidence',[])]+[v.get('supported_fact_or_case_result','') for v in r.get('clause_ledger',[])]
  assert all(isinstance(q,str) and any(isinstance(t,str) and q in t for t in texts) for part in g['material_parts'] for q in part['reader_quotes'])
  row=agg[g['id']];assert {k:v for k,v in row.items() if k!='original_independent_grade_report'}==g and row['original_independent_grade_report']==str(d/'grades-same-entry.json')
 p=json.loads((O/f'{nn}-runtime-projection.json').read_text());raw=Path(p['original_runtime_path']).read_bytes();assert sha(raw[:p['prefix_bytes']])==p['prefix_sha256'];item=next(x for x in filtered if x.get('agent',x.get('actor'))==f'/root/v13_stamped_i1_grade_b_{nn}');assert item['runtime_source']==p['original_runtime_path'];assert sha(raw[:item['runtime_snapshot_bytes']])==item['runtime_snapshot_sha256']
 physical=raw[:p['prefix_bytes']].splitlines(keepends=True);assert len(physical)==len(p['physical_records'])
 for n,(line,b) in enumerate(zip(physical,p['physical_records']),1):
  x=json.loads(line);q=x.get('payload',{});assert b==dict(physical_record=n,ordinal=n-1,sha256=sha(line),bytes=len(line),type=x.get('type'),payload_type=q.get('type') if isinstance(q,dict) else None)
 for c in p['tool_calls']:
  q=json.loads(physical[c['physical_record']-1])['payload'];assert c['name']==q['name'] and c['call_id']==q['call_id'] and c['input']==q.get('input',q.get('arguments'))
 for out in p['tool_outputs']:
  q=json.loads(physical[out['physical_record']-1])['payload'];v=q['output'];texts=[v] if isinstance(v,str) else [part['text'] for part in v if part.get('type') in ['text','input_text']];assert out['call_id']==q['call_id'] and out['text_blocks']==texts
 run=a['runs'][block['block_id']];run['all_physical_original_record_tool_call_output_and_terminal_provenance_bindings_verified']=True;run['independent_packet_raw_entry_atom_quote_parent_integrity_aggregate_transport_verified']=True;run['supplied_proof_false_paths_preserved']={n:falses(v[block['block_id']]) for n,v in proofs.items()};run['original_strict_delivery_flag']=proofs['grading-reader-b-input-delivery-proof.json'][block['block_id']]['complete_input_delivery_confirmed'];run['normalized_delivery_flag']=proofs['grading-reader-b-js-format-proposal-proof.json'][block['block_id']]['complete_input_delivery_confirmed']
assert len(agg)==116
a['staging']={'stage_01':'Five terminal report inputs frozen; sixth only initial active trace projection.','stage_02':'Sixth terminal trace/report, final aggregate, separate strict/normalized proofs and terminal provenance frozen after actual availability.','sixth_initial_prefix_preserved':True};a['dispatch_qualification']={'b06_actual_vs_template':'Exactly one harmless duplicated followed word; replacing followed followed by with followed by makes the saved texts identical.','incoming_private_plaintext_not_independently_certified':True};a['no_factual_format_or_process_score_caps']=True;a['source_or_report_changes']=False
for n,v in json.loads((O/'freeze-manifest.json').read_text())['input_file_bindings'].items():b=(F/n).read_bytes();assert len(b)==v['bytes'] and sha(b)==v['sha256']
(O/'audit.json').write_text(json.dumps(a,indent=2)+'\n');print(json.dumps({'all_six_complete':True,'all_original_bindings_and_aggregate_verified':True,'input_freezes_unchanged':True,'strict_vs_normalized_flags':{k:[v['original_strict_delivery_flag'],v['normalized_delivery_flag']] for k,v in a['runs'].items()}}))
