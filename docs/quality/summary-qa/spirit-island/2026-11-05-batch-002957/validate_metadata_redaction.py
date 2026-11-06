"""Verify redaction lineage and actual model records without emitting payloads."""
from pathlib import Path
import json,sys
from provenance_runtime import digest,reconstruct,validate_projection
B=Path(__file__).parent.resolve();m=json.loads((B/'provenance-metadata-redaction-manifest.json').read_text());chainpath=B/'provenance-metadata-update-chain.json';chain=json.loads(chainpath.read_text())['updates'] if chainpath.exists() else []
assert m['operation_completed'] and m['protected_gameplay_unchanged_at_redaction']
for x in m['files']:
 restored=(json.dumps(reconstruct(x['legacy_reconstruction_recipe']),indent=x['legacy_serialization']['indent'],ensure_ascii=x['legacy_serialization']['ensure_ascii'])+'\n').encode();assert digest(restored)==x['before_sha256']
 current=digest(Path(x['path']).read_bytes());reachable={x['after_sha256']}
 for edge in chain:
  if edge['path']==x['path'] and edge['before_sha256'] in reachable:reachable.add(edge['after_sha256'])
 assert current in reachable
for p in B.rglob('*-metadata.json'):
 d=json.loads(p.read_text());assert d['schema']=='minimal-runtime-metadata-v1'
 assert all(validate_projection(x) for x in [d['session_meta']]+d['turn_contexts'])
 if 'requested_spawn' in d:assert validate_projection(d['requested_spawn'])
 assert d['confirmed_settings']==[{'model':x['fields'].get('model'),'effort':x['fields'].get('effort')} for x in d['turn_contexts']]
 forbidden={'base_instructions','creator_account_id','creator_user_id','approval_policy','approvals_reviewer','sandbox_policy','permission_profile','active_permission_profile','file_system_sandbox_policy','network_sandbox_policy','permissions','account'}
 def inspect(v):
  if isinstance(v,dict):
   assert not set(v).intersection(forbidden)
   for a in v.values():inspect(a)
  elif isinstance(v,list):
   for a in v:inspect(a)
 inspect(d)
protected_current=None
if '--check-protected-current' in sys.argv:
 protected_current=all(digest(Path(x['path']).read_bytes())==x['after_sha256'] for x in m['protected_gameplay_files']);assert protected_current
out={'all_passed':True,'legacy_files_reconstructable':len(m['files']),'minimal_metadata_files_verified':len(list(B.rglob('*-metadata.json'))),'all_original_external_record_hashes_verified':True,'privileged_field_keys_remaining':False,'protected_gameplay_unchanged_at_redaction':m['protected_gameplay_unchanged_at_redaction'],'protected_current_rechecked':'--check-protected-current' in sys.argv,'current_protected_bytes_unchanged':protected_current,'metadata_update_chain_edges':len(chain),'note':'External original records are reconstructed only in memory for hashing. No privileged payload is printed or copied.'}
(B/'metadata-redaction-validation.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
