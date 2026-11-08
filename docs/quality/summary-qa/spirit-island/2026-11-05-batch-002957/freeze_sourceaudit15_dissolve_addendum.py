"""Freeze the same auditor's new own-source addendum before parent interpretation."""
from pathlib import Path
import datetime
import hashlib
import json

B = Path(__file__).resolve().parent
load = lambda p: json.loads(p.read_text())
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
main = B / 'source-audit15-own-source-dissolve-addendum.json'
assert main.is_file()
files = sorted(B.glob('source-audit15-own-source-dissolve*.json'))
assert main in files
dest = B / 'source-audit15-own-source-addendum-original-completed'
receipt = B / 'source-audit15-own-source-addendum-original-freeze.json'
assert not dest.exists() and not receipt.exists()
original = load(B / 'source-audit15-original-freeze.json')
for name, row in original['files'].items():
    assert H(B / name) == row['sha256'] == H(Path(row['original_completed_copy']))
assert H(B / 'source-candidate-26.md') == H(B.parents[4] / 'rules/spirit-island.md') == 'ce8f1d645f466686ae2e75fcd29130fa89cbb1c4963d981090e3768a526a6fd1'
raw = {p.name: p.read_bytes() for p in files}
boundary = load(B / 'source-audit15-original-completed-runtime-boundary.json')
prefix = hashlib.sha256()
new = hashlib.sha256()
total = hashlib.sha256()
size = count = prefix_size = 0
with Path(boundary['session_path']).open('rb') as stream:
    for ordinal, line in enumerate(stream):
        assert line.endswith(b'\n'), 'Wait for the auditor to report completion.'
        total.update(line)
        size += len(line)
        count += 1
        if ordinal < boundary['record_count']:
            prefix.update(line)
            prefix_size += len(line)
        else:
            new.update(line)
assert prefix.hexdigest() == boundary['prefix_sha256'] and prefix_size == boundary['prefix_bytes']
assert count > boundary['record_count']
new_boundary = {
    'session_path': boundary['session_path'], 'record_count': count,
    'prefix_bytes': size, 'prefix_sha256': total.hexdigest(),
    'new_record_start_inclusive': boundary['record_count'],
    'new_record_end_exclusive': count, 'new_records_sha256': new.hexdigest(),
    'original_653_record_boundary_unchanged': True,
    'no_original_delivery_borrowed_to_prove_new_reinspection': True,
    'captured_after_auditor_reported_completion': True,
    'before_parent_semantic_review': True, 'no_runtime_bodies_copied': True,
}
bp = B / 'source-audit15-own-source-addendum-completed-runtime-boundary.json'
assert not bp.exists()
bp.write_text(json.dumps(new_boundary, indent=2) + '\n')
dest.mkdir()
rows = {}
for name, data in raw.items():
    (dest / name).write_bytes(data)
    assert (dest / name).read_bytes() == (B / name).read_bytes()
    rows[name] = {'sha256': H(B / name), 'bytes': len(data), 'immutable_copy': str(dest / name)}
receipt.write_text(json.dumps({
    'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'files': rows, 'runtime_boundary': str(bp), 'runtime_boundary_sha256': H(bp),
    'before_parent_semantic_review': True, 'all_three_original_audit_files_unchanged': True,
    'canonical_C26_unchanged': True, 'same_original_auditor_own_source_continuation': True,
    'not_new_fresh_source_vote': True,
}, indent=2) + '\n')
print(json.dumps({'new_addendum_originals_frozen': True, 'files': rows, 'new_runtime_record_range': [boundary['record_count'], count], 'freeze_sha256': H(receipt)}))
