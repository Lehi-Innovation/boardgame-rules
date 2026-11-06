"""Restore missing owned /tmp reading derivatives from pinned evidence bytes.

This is preservation/replay support only, never a new model-delivery claim.
Existing temporary files are verified and never overwritten.
"""
from pathlib import Path
import hashlib,json
B=Path(__file__).parent.resolve();D=B/'preserved-derived-inputs';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();m=json.loads((D/'manifest.json').read_text());restored=[]
for x in m['copies']:
 p=Path(x['original_delivered_path']);q=Path(x['preserved_exact_copy']);assert p.is_absolute() and p.is_relative_to('/tmp') and not p.is_symlink();assert q.resolve().is_relative_to(D) and H(q)==x['sha256']
 if p.exists():assert p.is_file() and H(p)==x['sha256']
 else:
  p.parent.mkdir(parents=True,exist_ok=True)
  with p.open('xb') as f:f.write(q.read_bytes())
  restored.append(str(p))
print(json.dumps({'preserved_input_copies_verified':len(m['copies']),'restored_missing_paths':restored,'new_model_delivery_claim':False}))
