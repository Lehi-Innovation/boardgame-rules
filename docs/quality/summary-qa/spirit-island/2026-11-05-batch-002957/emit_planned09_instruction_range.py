"""Emit one literal predeclared instruction range; no reading/grade feedback."""
from pathlib import Path
import hashlib
import json
import sys

B = Path(__file__).resolve().parent
p = (B / sys.argv[1]).resolve()
assert p.is_relative_to(B)
assert p.parent.name in ['expanded09-planned-reader-prompts-v15', 'expanded09-planned-grader-prompts-v2'] or p.name == 'expanded09-adjudicator-protocol-template-v2.txt'
s = p.read_text()
a, z = map(int, sys.argv[2:4])
assert 0 <= a < z <= len(s) and z - a <= 6000
t = s[a:z]
print(json.dumps({'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest(),
                  'unicode_character_length': len(s), 'range': [a, z],
                  'slice_sha256': hashlib.sha256(t.encode()).hexdigest(),
                  'output_cap_tokens': 4000, 'truncated': False, 'text': t}, ensure_ascii=False))
