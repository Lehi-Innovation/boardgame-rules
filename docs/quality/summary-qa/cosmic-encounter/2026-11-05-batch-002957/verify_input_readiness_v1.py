"""Verify whole actual two-file delivery while the reader still has zero answers."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
from reader_receipt_offsets_v1 import normalize_offset_receipts

R=Path(__file__).parent.resolve()
it=Path(sys.argv[1]).resolve()
label=sys.argv[2]
assert it.is_relative_to(R) and label in ('a','b')
manifest=json.loads((it/'input-manifest-final.json').read_text())
# Archive first, including any malformed raw work; no replacement of old attempts.
subprocess.run([sys.executable,'-B',str(R/'staged-reader-workflow-v1/snapshot_stage.py'),str(it),label,'input'],check=True)
archives=sorted(it.glob(f'reader-{label}-input-ready-[0-9][0-9].json'))
archive=archives[-1]
attempt=archive.stem.rsplit('-',1)[1]
doc=json.loads(archive.read_text())
assert doc['answers']==[] and doc['evidence_units']=={} and doc['stage']=='inputs_ready'
assert not Path(manifest['reader_work_paths'][label]['final']).exists()
assert [x['path'] for x in doc['inputs_read']]==manifest['sole_game_data_files'] or set(x['path'] for x in doc['inputs_read'])==set(manifest['sole_game_data_files'])
receipt={'text_input_proofs':[],'coordinate_bindings':[]}
for source in doc['inputs_read']:
    path=Path(source['path']);text=path.read_text()
    assert source['characters']==len(text) and source['bytes']==len(path.read_bytes())
    assert source['sha256']==hashlib.sha256(path.read_bytes()).hexdigest()
    converted=normalize_offset_receipts(text,source['chunks'])
    assert all(0<c['end']-c['start']<=2900 for c in converted['chunks'])
    receipt['coordinate_bindings'].append({'path':str(path),**converted})
    receipt['text_input_proofs'].append({'path':str(path),'full_file_sha256':source['sha256'],
       'chunks':[{'start_char':c['start'],'end_char_exclusive':c['end'],'utf8_chunk_sha256':c['sha256']} for c in converted['chunks']]})
normalized=it/f'reader-{label}-input-normalized-{attempt}.json'
with normalized.open('x') as f: json.dump(receipt,f,indent=2);f.write('\n')
output=it/f'reader-{label}-input-actual-validation-{attempt}.json'
cmd=[sys.executable,'-B',str(R/'validate_source_delivery.py'),manifest['reader_tasks'][label],str(normalized),str(output),'--native-mode','none']
for path in manifest['sole_game_data_files']:cmd+=['--require-file',path]
subprocess.run(cmd,check=True)
actual=json.loads(output.read_text())
assert actual['pass']
provenance=json.loads(Path(manifest['model_provenance_path']).read_text())
agent=next(x for x in provenance['agents'] if x['task']==manifest['reader_tasks'][label])
raw=Path(agent['runtime_source_path']).read_bytes()
# Save only opaque runtime-prefix metadata. No encrypted argument or instruction text.
ordinals=[json.loads(line).get('ordinal',i) for i,line in enumerate(raw.splitlines())]
gate={'pass':True,'reader':label,'identity':agent['identity'],'zero_answers_at_gate':True,
      'initial_readiness_archive':str(archive),'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),
      'actual_delivery_validation':str(output),'runtime_prefix_bytes':len(raw),
      'runtime_prefix_sha256':hashlib.sha256(raw).hexdigest(),'after_ordinal':max(ordinals),
      'draft_continuation_authorized_only_after_this_gate':True,
      'limit':'Complete actual input availability while zero answers are saved; semantic comprehension and future answer correctness are separate. No hidden instruction or encrypted text copied.'}
with (it/f'reader-{label}-input-gate-{attempt}.json').open('x') as f:json.dump(gate,f,indent=2);f.write('\n')
print({'reader':label,'input_gate_pass':True,'actual_chunks':sum(len(x['chunks']) for x in receipt['text_input_proofs'])})
