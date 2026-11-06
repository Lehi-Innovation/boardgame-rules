from pathlib import Path
import json,hashlib,collections
ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'manifest.json').read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def load_tool_evidence(path):
 # Original ordinals, not projected line numbers, remain the historical citation keys.
 rows=[json.loads(x) for x in Path(path).read_bytes().splitlines()]
 return [(r['original_record_ordinal'],r['event']) for r in rows[1:] if r['retention']=='tool_evidence']
checks=[]
for c in manifest['changes']:
 p=Path(c['path']);projection=Path(c['projection_file']);pb=projection.read_bytes();assert sha(pb)==c['projection_sha256'];assert sha(p.read_bytes())==c['new_stub_sha256'];stub=json.loads(p.read_bytes());assert stub['type']=='qa_runtime_raw_copy_superseded_v1'
 with Path(c['original_runtime_path']).open('rb') as h:original=h.read(c['old_bytes'])
 assert sha(original)==c['old_sha256'];lines=original.splitlines(keepends=True);rows=[json.loads(x) for x in pb.splitlines()];assert len(rows)==len(lines)+1;counts=collections.Counter()
 for ordinal,(raw,row) in enumerate(zip(lines,rows[1:]),1):
  assert row['original_record_ordinal']==ordinal and row['original_record_sha256']==sha(raw)
  assert original[row['original_record_byte_start']:row['original_record_byte_start']+row['original_record_byte_length']]==raw
  event=json.loads(raw);payload=event.get('payload',{}) if isinstance(event,dict) else {};counts[row['retention']]+=1
  if row['retention']=='tool_evidence':
   assert row['event']['type']==event['type'];q=row['event']['payload'];assert set(q)<={'type','call_id','name','input','arguments','output','output_hash_only'}
   for key,value in q.items():assert value==payload[key]
  elif row['retention']=='allowlisted_actual_metadata':
   assert set(row['metadata'])<=set(manifest['allowlist']['metadata']);assert 'event' not in row and 'payload' not in row
   if event['type']=='turn_context':
    for k,v in row['metadata'].items():assert payload[k]==v
  else:assert 'event' not in row and 'payload' not in row and 'metadata' not in row
 assert dict(counts)==c['retained_counts']
 # These private instruction wrappers do not occur in retained tool evidence.
 marker_hits={marker:pb.count(marker.encode()) for marker in ['<app-context>','<permissions instructions>','<environment_context>','You are Codex, an agent']}
 assert not any(marker_hits.values())
 checks.append(dict(path=c['path'],projection=c['projection_file'],record_count=len(lines),all_record_hashes_and_offsets_verified=True,all_retained_tool_fields_exact=True,allowlisted_context_metadata_verified=True,private_instruction_wrapper_hits=0))
print(json.dumps({'verified_files':len(checks),'verified_original_records':sum(x['record_count'] for x in checks),'all_pass':True}))
with (ROOT/'verification.json').open('x') as f:json.dump({'checks':checks,'all_pass':True},f,indent=2);f.write('\n')
