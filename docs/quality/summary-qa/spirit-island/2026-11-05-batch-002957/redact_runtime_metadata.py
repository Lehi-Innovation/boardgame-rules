"""Narrow metadata-only redaction; never print or persist privileged payload copies."""
from pathlib import Path
import datetime,json,hashlib
from provenance_runtime import legacy_recipe,reconstruct,digest,load_selected,validate_projection
B=Path(__file__).parent.resolve();ROOT=B.parents[4];OUT=B/'provenance-metadata-redaction-manifest.json';assert not OUT.exists()
serial=lambda x:(json.dumps(x,indent=2,ensure_ascii=True)+'\n').encode()
targets=sorted(B.rglob('*-metadata.json'));plans=[]
for p in targets:
 before=p.read_bytes();old=json.loads(before)
 if old.get('schema')=='minimal-runtime-metadata-v1':continue
 recipe,projection=legacy_recipe(old)
 assert digest(serial(reconstruct(recipe)))==digest(before)
 assert all(validate_projection(x) for x in [projection['session_meta']]+projection['turn_contexts'])
 if 'requested_spawn' in projection:assert validate_projection(projection['requested_spawn'])
 plans.append({'path':str(p),'before_sha256':digest(before),'after_sha256':digest(serial(projection)),'legacy_reconstruction_recipe':recipe,'legacy_serialization':{'indent':2,'ensure_ascii':True,'trailing_newline':True},'correction':'Whitelist-only identity/model/fork projection; original full records remain in external logs.','projection':projection})
assert plans
# Protect all requested gameplay evidence and source bytes. No metadata payload is included.
protected={ROOT/'rules/spirit-island.md'}
protected.update(ROOT/x for x in json.loads((B/'source-manifest.json').read_text())['paths_and_sha256'])
protected.update(Path(x['path']) for x in json.loads((B/'supplemental-source-manifest-v2.json').read_text())['source_records'])
for pattern in ['source-candidate-*.md','**/questions.json','**/answer-key.json','**/reader-a.json','**/reader-b.json','**/results.json','**/grades.json','**/summary-snapshot.md','**/asked-fact-map*.json','coverage-review-??.json','source-audit*.json']:
 protected.update(B.glob(pattern))
protected=sorted(p for p in protected if p.is_file());before_protected={str(p):digest(p.read_bytes()) for p in protected}
external=[]
for s in sorted({x['projection']['session_path'] for x in plans}):
 p=Path(s);size=p.stat().st_size
 with p.open('rb') as h:sha=digest(h.read(size))
 external.append({'path':s,'prefix_byte_length':size,'sha256_before':sha})
references=[]
for p in B.rglob('*.json'):
 if p in targets or p==OUT:continue
 text=p.read_text()
 for entry in plans:
  if entry['before_sha256'] in text:references.append({'referencing_path':str(p),'metadata_path':entry['path'],'old_sha256':entry['before_sha256'],'projected_sha256':entry['after_sha256'],'adjustment':'Historical reference remains unchanged; use this redaction overlay or reconstruct the original bytes externally.'})
manifest={'schema':'provenance-metadata-redaction-v1','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'affected_file_count':len(plans),'scope':'Only owned *-metadata.json artifacts and their capture generator. External runtime logs are read-only. No full-content backup copies created.','files':[{k:v for k,v in x.items() if k!='projection'} for x in plans],'old_provenance_hash_references':references,'hash_chain_adjustments':[{'path':x['path'],'before_sha256':x['before_sha256'],'after_sha256':x['after_sha256'],'legacy_reconstruction_verified':True} for x in plans],'protected_gameplay_files':[{'path':p,'before_sha256':h} for p,h in before_protected.items()],'protected_gameplay_unchanged_at_redaction':False,'projection_policy':'Retain identity, parent/session/task, requested and actual model/effort, fork context, timestamps, external source paths/record ordinals and opaque original-record hashes only.','external_prefix_integrity':external,'operation_completed':False}
# Write safe recipes first so an interrupted narrow projection remains reconstructable.
OUT.write_bytes(serial(manifest))
for x in plans:
 p=Path(x['path']);assert digest(p.read_bytes())==x['before_sha256'];p.write_bytes(serial(x['projection']));assert digest(p.read_bytes())==x['after_sha256']
for x in manifest['protected_gameplay_files']:
 x['after_sha256']=digest(Path(x['path']).read_bytes());x['unchanged']=x['before_sha256']==x['after_sha256'];assert x['unchanged']
for x in manifest['external_prefix_integrity']:
 with Path(x['path']).open('rb') as h:x['sha256_after_same_length']=digest(h.read(x['prefix_byte_length']))
 x['unchanged']=x['sha256_before']==x['sha256_after_same_length'];assert x['unchanged']
manifest['protected_gameplay_unchanged_at_redaction']=True;manifest['operation_completed']=True;OUT.write_bytes(serial(manifest))
print(json.dumps({'metadata_files_projected':len(plans),'legacy_before_hashes_reconstructed':True,'protected_gameplay_files':len(protected),'all_protected_bytes_unchanged':True,'external_log_prefixes_unchanged':True,'existing_hash_references_preserved_through_overlay':len(references)}))
