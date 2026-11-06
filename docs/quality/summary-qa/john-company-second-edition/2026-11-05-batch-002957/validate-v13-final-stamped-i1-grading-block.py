"""Intermediate block integrity; final unchanged role/paired validators still apply."""
from pathlib import Path
from collections import Counter
import datetime
import hashlib
import importlib.util
import json
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('single', ROOT / 'single-reader-grading-tools.py')
single = importlib.util.module_from_spec(spec)
spec.loader.exec_module(single)
role, block_id = sys.argv[1:]
bank, run, questions, ids, key_path, scope_path, keys, scopes, raw = single.context(
    'expanded-v13-complete-requested-scope', 'luna-final-stamped-iteration-01', role)
base = single.base
manifest = base.read(run / f'grading-reader-{role}/packet-manifest.json')
block = next(block for block in manifest['blocks'] if block['block_id'] == block_id)
folder = run / f'grading-reader-{role}' / block_id
assert base.sha(folder / 'packet.json') == block['packet_sha256']
assert all(base.sha(Path(path)) == digest for path, digest in manifest['input_hashes'].items())
packet = base.read(folder / 'packet.json')
report_path = folder / 'grades-same-entry.json'
report = base.read(report_path)
assert report['block_id'] == block_id and set(report['readers']) == {f'reader-{role}'}
grades = report['readers'][f'reader-{role}']['grades']
assert [entry['id'] for entry in packet['entries']] == block['ids']
assert [grade['id'] for grade in grades] == block['ids']
atoms = 0
for entry, grade in zip(packet['entries'], grades):
    qid = grade['id']
    assert entry[f'reader_{role}_entry'] == raw[qid]
    assert base.entry_sha(raw[qid]) == block['complete_raw_entry_sha256s'][qid]
    assert entry['key_entry'] == keys[qid] and entry['requested_fact_scope_entry'] == scopes[qid]
    assert grade['grade'] in ['Correct', 'Partial', 'Incorrect']
    assert isinstance(grade['reason'], str) and grade['reason'].strip()
    assert Counter(part['requirement'] for part in grade['material_parts']) == Counter(scopes[qid]['material_requested_facts'])
    substantive = base.substantive_strings(raw[qid])
    for part in grade['material_parts']:
        assert part['status'].lower() in ['covered', 'omitted', 'contradicted']
        quotes = part.get('reader_quotes', [])
        assert isinstance(quotes, list) and all(isinstance(q, str) and q.strip() for q in quotes)
        assert all(any(q in text for text in substantive) for q in quotes)
        if part['status'].lower() == 'covered':
            assert quotes
    if grade['grade'] == 'Correct':
        assert all(part['status'].lower() == 'covered' for part in grade['material_parts'])
        assert not grade.get('unsupported_guesses')
    atoms += len(grade['material_parts'])
counts = dict(Counter(grade['grade'] for grade in grades))
result = dict(at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    reader_role=f'reader-{role}', block_id=block_id, complete_ids=block['ids'],
    counts={name: counts.get(name, 0) for name in ['Correct', 'Partial', 'Incorrect']},
    material_parts_checked=atoms, all_required_atoms_once=True,
    all_reader_quotes_literal_in_original_substantive_fields=True,
    all_original_packet_raw_entries_and_frozen_hashes_match=True,
    original_grade_report_sha256=base.sha(report_path),
    limits='Schema, frozen raw-entry/atom transport and quote integrity only. Actual delivery/model/path proof and substantive judgment remain separate. Original reports unchanged; final reviewed role and paired validators remain mandatory.')
with (folder / 'parent-grade-integrity.json').open('x') as handle:
    json.dump(result, handle, ensure_ascii=False, indent=2)
    handle.write('\n')
print(json.dumps(dict(reader=f'reader-{role}', block=block_id, counts=result['counts'], atoms=atoms)))
