"""Normalize receipt field names only; never invent/repartition delivered ranges."""
from pathlib import Path
import hashlib
import json
import sys

R = Path(__file__).parent.resolve()
IT = (R / sys.argv[1]).resolve()
assert IT.is_relative_to(R)
tag = f'{int(sys.argv[2]):02}'
report = IT / f'grades-{tag}.json'
doc = json.loads(report.read_bytes())
sources = [doc['instructions_read']] + doc['inputs_read']
proofs = []
for source in sources:
    chunks = []
    declared_chunks = source.get('chunks', source.get('actual_delivered_chunks'))
    assert declared_chunks, 'A declared delivered chunk list is required'
    for c in declared_chunks:
        chunks.append({'start_char': c.get('start', c.get('start_char')),
                       'end_char_exclusive': c.get('end', c.get('end_char_exclusive', c.get('end_char'))),
                       'utf8_chunk_sha256': c.get('sha256', c.get('utf8_sha256', c.get('utf8_chunk_sha256')))})
    assert all(c['start_char'] is not None and c['end_char_exclusive'] is not None
               and c['utf8_chunk_sha256'] is not None for c in chunks)
    proofs.append({'path': source['path'], 'full_file_sha256': source['sha256'], 'chunks': chunks})
out = {'report_path': str(report), 'report_sha256': hashlib.sha256(report.read_bytes()).hexdigest(),
       'normalization': 'Receipt schema aliases only; all actual declared ranges/hashes unchanged.',
       'text_input_proofs': proofs}
path = IT / f'grader-{tag}-normalized-delivery.json'
assert not path.exists()
path.write_text(json.dumps(out, indent=2) + '\n')
print('Normalized original receipt:', tag, '; files:', len(proofs))
