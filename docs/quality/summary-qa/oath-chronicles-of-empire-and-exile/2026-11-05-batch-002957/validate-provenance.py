"""Verify minimal metadata and redaction chains against untouched external runtime logs."""
from pathlib import Path
import hashlib,json
from provenance_runtime import digest,project
P=Path(__file__).resolve().parent
manifest=json.loads((P/'provenance-metadata-redaction-manifest.json').read_text())
chain=json.loads((P/'provenance-metadata-update-chain.json').read_text()) if (P/'provenance-metadata-update-chain.json').exists() else {'updates':[]}
checks={};errors=[];refs={};projections=[];minimal=[]
def check(name,value):
 checks[name]=bool(value)
 if not value:errors.append(name)
def walk(x):
 if isinstance(x,dict):
  if 'source_record' in x and 'fields' in x:projections.append(x);r=x['source_record'];refs[(r['runtime_path'],r['runtime_line_ordinal'])]=r
  if '$external_runtime_record' in x:r=x['$external_runtime_record'];refs[(r['runtime_path'],r['runtime_line_ordinal'])]=r
  if x.get('schema')=='minimal-runtime-provenance-v1':minimal.append(x)
  for v in x.values():walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
walk(manifest)
for f in P.rglob('*provenance*.json'):
 if f.name in ['provenance-metadata-redaction-manifest.json','provenance-metadata-validation.json']:continue
 walk(json.loads(f.read_text()))
byfile={}
for (path,n),ref in refs.items():byfile.setdefault(path,set()).add(n)
loaded={}
for path,wanted in byfile.items():
 with Path(path).open('rb') as h:
  for n,line in enumerate(h):
   if n not in wanted:continue
   ref=refs[(path,n)];check('external_record_hash:'+path+':'+str(n),digest(line)==ref['runtime_record_sha256']);loaded[(path,n)]=(json.loads(line),line)
   if all((path,i) in loaded for i in wanted):break
 check('all_external_ordinals:'+path,all((path,i) in loaded for i in wanted))
for n,p in enumerate(projections):
 r=p['source_record'];row,line=loaded[(r['runtime_path'],r['runtime_line_ordinal'])]
 if 'task_name' in p['fields']:
  a=row['payload'].get('arguments',{});a=json.loads(a) if isinstance(a,str) else a;expected={k:a[k] for k in ['task_name','fork_turns','model','reasoning_effort'] if k in a};check('spawn_fields:'+str(n),p['fields']==expected)
 else:check('projected_fields:'+str(n),project(Path(r['runtime_path']),r['runtime_line_ordinal'],row,line)==p)
def restore(x):
 if isinstance(x,dict) and '$external_runtime_record' in x:
  r=x['$external_runtime_record'];row=loaded[(r['runtime_path'],r['runtime_line_ordinal'])][0];return row if x['view']=='whole' else row['payload']
 if isinstance(x,dict):return {k:restore(v) for k,v in x.items()}
 if isinstance(x,list):return [restore(v) for v in x]
 return x
for item in manifest['files']:
 obj=restore(item['legacy_reconstruction_recipe']);fmt=item['legacy_serialization'];before=(json.dumps(obj,indent=fmt['indent'],ensure_ascii=fmt['ensure_ascii'])+('\n' if fmt['trailing_newline'] else '')).encode();check('before_hash_reconstructed_external:'+item['path'],digest(before)==item['before_sha256']);current=item['after_sha256']
 for u in chain['updates']:
  if u['path']==item['path'] and u['before_sha256']==current:current=u['after_sha256']
 check('after_redaction_chain:'+item['path'],digest(Path(item['path']).read_bytes())==current)
for r in minimal:
 fields=[p['fields'] for p in r['runtime_records'] if p['source_record']['runtime_record_type']=='turn_context'];check('actual_model_effort:'+r['session_path'],r['models']==list(dict.fromkeys(f.get('model') for f in fields)) and r['efforts']==list(dict.fromkeys(f.get('effort') for f in fields)) and r['model_confirmed']==bool(fields))
check('gameplay_unchanged_at_redaction',manifest['protected_gameplay_unchanged_at_redaction'] and all(x['before_sha256']==x['after_sha256'] for x in manifest['protected_gameplay_files']))
for x in manifest['protected_gameplay_files']:
 if x['frozen_live_check']:check('frozen_gameplay_exact:'+x['path'],digest(Path(x['path']).read_bytes())==x['after_sha256'])
# Scan dictionaries, not mere key names in reconstruction recipes, for copied private runtime payload fields.
badkeys={'base_instructions','creator_account_id','creator_user_id','permission_profile','active_permission_profile','sandbox_policy','runtime_workspace_roots','environment_context','developer_instructions'};found=[]
def privacy(x,path):
 if isinstance(x,dict):
  for k,v in x.items():
   if k in badkeys:found.append([path,k])
   privacy(v,path)
 elif isinstance(x,list):
  for v in x:privacy(v,path)
 elif isinstance(x,str) and '<environment_context>' in x:found.append([path,'environment_dump'])
for f in P.rglob('*.json'):privacy(json.loads(f.read_text()),str(f))
check('no_copied_private_runtime_payloads',not found)
out={'status':'PASS' if not errors else 'FAIL','affected_files':len(manifest['files']),'external_runtime_records_verified':len(refs),'minimal_model_records_verified':len(minimal),'before_hashes_reconstruct_from_external_logs':True if not any(k.startswith('before_hash') for k in errors) else False,'checks':checks,'errors':errors,'private_payload_findings':found,'limits':'Canonical equality at redaction is historical before/after proof; later authorized gameplay revisions use their own frozen-source gates. External originals were read only. No full-content backup copies were created.'}
(P/'provenance-metadata-validation.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'],'metadata files',out['affected_files'],'external records',len(refs),'errors',errors[:8])
if errors:raise SystemExit(1)
