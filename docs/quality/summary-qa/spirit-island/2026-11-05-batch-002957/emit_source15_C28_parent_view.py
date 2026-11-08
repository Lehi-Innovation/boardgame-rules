from pathlib import Path
import hashlib
import json
import sys
B = Path(__file__).resolve().parent
p = B / 'source-audit15-C28-parent-current-human-semantic-view.json'
s = p.read_text()
a, z = map(int, sys.argv[1:3])
assert 0 <= a < z <= len(s) and z-a <= 6000
t = s[a:z]
print(json.dumps({'path':str(p), 'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
                  'characters':len(s), 'range':[a,z], 'slice_sha256':hashlib.sha256(t.encode()).hexdigest(),
                  'output_cap_tokens':4000, 'truncated':False, 'text':t}, ensure_ascii=False))
