"""Reproduce the immutable adjudication transport proof after later working turns append."""
from pathlib import Path
import hashlib
import json

B=Path(__file__).resolve().parent
S=B/'novelty-adjudication-18'
load=lambda p:json.loads(p.read_text())
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
boundary=load(S/'completed-runtime-boundary.json')
adoption=load(S/'adoption.json')
original=B/'verify_novelty18_actual_delivery.py'
assert H(original)==adoption['actual_delivery_validator_sha256']
with Path(boundary['session_path']).open('rb') as stream:
    assert hashlib.sha256(stream.read(boundary['prefix_bytes'])).hexdigest()==boundary['prefix_sha256']
source=original.read_text()
needle="for ordinal, line in enumerate(Path(profile['session_path']).open('rb')):\n"
assert source.count(needle)==1
source=source.replace(needle,needle+f"    if ordinal >= {boundary['record_count']}:\n        break\n")
destination="dest = B / 'novelty-adjudication-18/actual-delivery-validation.json'"
assert source.count(destination)==1
source=source.replace(destination,"dest = B / 'novelty-adjudication-18/bounded-replay-validation.json'")
# Only a record-boundary guard and new derived-output destination differ.
# No runtime payload is copied; the original public-source matcher runs in memory.
exec(compile(source,str(original),'exec'),{'__file__':str(original),'__name__':'__main__'})
replay=S/'bounded-replay-validation.json'
assert replay.read_bytes()==(S/'actual-delivery-validation.json').read_bytes()
proof={'exact_original_proof_bytes_reproduced':True,'original_proof_sha256':H(S/'actual-delivery-validation.json'),'bounded_replay_sha256':H(replay),'boundary_sha256':H(S/'completed-runtime-boundary.json'),'opaque_completed_prefix_records':boundary['record_count'],'source_matcher_sha256':H(original),'no_private_runtime_bodies_copied':True,'method':'Original source matcher unchanged on disk; in-memory cutoff at captured completed record count plus a new derived output filename. Later working evidence cannot affect the original adjudication.'}
(S/'bounded-replay-method.json').write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps(proof))
