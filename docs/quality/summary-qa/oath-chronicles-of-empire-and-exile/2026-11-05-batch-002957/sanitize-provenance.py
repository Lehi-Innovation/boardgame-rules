"""Metadata-only in-place minimization. No full-content backups are made."""
from pathlib import Path
import datetime,hashlib,json
from provenance_runtime import load,captured_record,canonical_hash,digest
P=Path(__file__).resolve().parent
markers=['"base_instructions"','"permission_profile"','"creator_account_id"','<environment_context>']
targets=[f for f in P.rglob('*provenance*.json') if any(m in f.read_text() for m in markers)]
assert targets,'Nothing to sanitize; do not fabricate another redaction chain.'
before={str(f.resolve()):digest(f.read_bytes()) for f in targets}
# Hash-only protection of immutable gameplay evidence. Current unfinished grade blocks are not included.
protected={}
for f in P.rglob('*'):
 if not f.is_file() or f in targets:continue
 name=f.name
 frozen=(name in ['summary-snapshot.md','questions.json','answer-key.json','grading-scope.json','source-audit.json','results.json','grading-input.json','packet.json'] or (name.startswith('reader-') and name.endswith('.json') and not any(x in name for x in ['validation','provenance'])))
 if frozen and not ('expanded-iteration-13/grading-blocks/block-0' in str(f) and f.parent.name in ['block-04','block-05','block-06']):protected[str(f.resolve())]=digest(f.read_bytes())
canonical=P.parents[4]/'rules/oath-chronicles-of-empire-and-exile.md';protected[str(canonical)]=digest(canonical.read_bytes())
refs=[]
for f in P.rglob('*.json'):
 if f in targets:continue
 text=f.read_text()
 for path,h in before.items():
  if h in text:refs.append({'manifest_path':str(f.resolve()),'metadata_path':path,'expected_before_sha256':h})
def recipe(x,lookup):
 if isinstance(x,dict):
  key=canonical_hash(x)
  if key in lookup:
   pr,view=lookup[key];return {'$external_runtime_record':pr['source_record'],'view':view}
  return {k:recipe(v,lookup) for k,v in x.items()}
 if isinstance(x,list):return [recipe(v,lookup) for v in x]
 return x
def sanitize(j):
 if isinstance(j,list):
  out=[];lookup={}
  for r in j:
   data=load(r['session_path']);lookup.update(data['views']);out.append(captured_record(r))
  return out,recipe(j,lookup)
 if isinstance(j,dict) and 'session' in j and 'messages' in j:
  data=load(j['session']);projected=[]
  for message in j['messages']:
   key=canonical_hash(message);assert key in data['lookup'];projected.append(data['lookup'][key])
  identity=data['meta']['fields'];out={'schema':'minimal-dispatch-reference-v1','session_path':j['session'],'agent_path':identity.get('agent_path',identity.get('fork_context',{}).get('agent_path')),'runtime_records':[data['meta']]+projected,'limits':'Opaque runtime references and allowed identity fields only; no message content or plaintext-to-ciphertext equivalence claim.'}
  return out,recipe(j,data['views'])
 raise AssertionError(('Unsupported provenance shape',type(j).__name__))
entries=[]
for f in targets:
 original=f.read_bytes();j=json.loads(original);new,rec=sanitize(j)
 serial=None
 for ascii_mode in [True,False]:
  for newline in [True,False]:
   candidate=(json.dumps(j,indent=2,ensure_ascii=ascii_mode)+('\n' if newline else '')).encode()
   if digest(candidate)==digest(original):serial={'indent':2,'ensure_ascii':ascii_mode,'trailing_newline':newline};break
  if serial:break
 assert serial,(str(f),'unknown original serializer; do not replace without reconstructable before hash')
 data=(json.dumps(new,indent=2)+'\n').encode();f.write_bytes(data)
 entries.append({'path':str(f.resolve()),'before_sha256':digest(original),'after_sha256':digest(data),'legacy_reconstruction_recipe':rec,'legacy_serialization':serial,'correction':'Metadata-only projection; original source records remain in external authoritative runtime logs.'})
unchanged=[]
for path,h in protected.items():
 after=digest(Path(path).read_bytes());assert h==after,(path,'protected gameplay changed')
 unchanged.append({'path':path,'before_sha256':h,'after_sha256':after,'frozen_live_check':path!=str(canonical)})
manifest={'schema':'provenance-metadata-redaction-v1','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'affected_file_count':len(entries),'scope':'Only this game QA provenance. Full runtime logs outside repo unchanged; no full-content backup copies created. Legacy before hashes reconstruct in memory from external record references.','files':entries,'old_provenance_hash_references':refs,'protected_gameplay_files':unchanged,'protected_gameplay_unchanged_at_redaction':True,'projection_policy':'Retain identity, parent/agent path, turns/timestamps, actual models/efforts and fork-context fields only; each external original has source path, zero-based line ordinal and opaque raw-record SHA256.'}
(P/'provenance-metadata-redaction-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Sanitized',len(entries),'provenance files; protected',len(unchanged),'gameplay files unchanged; referenced prior hashes',len(refs))
