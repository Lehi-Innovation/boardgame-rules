"""Independent verification implementation: verify exact, same-entry reference joins and raw bytes."""
import copy
import hashlib
import json
import sys
from pathlib import Path

R = Path(__file__).parent.resolve()
IT = (R / sys.argv[1]).resolve()
assert IT.is_relative_to(R)
expected_entry_count = 2 * len(json.loads((IT / 'questions.json').read_bytes())['questions'])
block_count = len(json.loads((IT / 'grading-inputs-v2/manifest.json').read_bytes())['blocks'])


def digest(b):
    return hashlib.sha256(b).hexdigest()


def normalized(x):
    return digest(json.dumps(x, sort_keys=True, ensure_ascii=False,
                             separators=(',', ':')).encode())


def pointer(x, p):
    for k in p.split('/')[1:]:
        k = k.replace('~1', '/').replace('~0', '~')
        x = x[int(k)] if isinstance(x, list) else x[k]
    return x


def refs(x, p=''):
    result = []
    if isinstance(x, dict):
        for k, v in x.items():
            q = p + '/' + k.replace('~', '~0').replace('/', '~1')
            if k in ('evidence', 'evidence_refs', 'evidence_ids') and isinstance(v, list):
                result += [(a, q + '/' + str(i)) for i, a in enumerate(v)
                           if isinstance(a, (str, int))]
            result += refs(v, q)
    elif isinstance(x, list):
        for i, v in enumerate(x):
            result += refs(v, p + '/' + str(i))
    return result


raw = {c: (IT / f'reader-{c}.json').read_bytes() for c in 'ab'}
docs = {c: json.loads(b) for c, b in raw.items()}
summary = (IT / 'summary-snapshot.md').read_text()
checks = []
for n in range(1, block_count + 1):
    filename = f'block-{n:02}.json'
    old = json.loads((IT / 'grading-inputs' / filename).read_bytes())
    new = json.loads((IT / 'grading-inputs-v2' / filename).read_bytes())
    stripped = copy.deepcopy(new)
    for k in ('reference_resolution_policy', 'original_bundle_path', 'original_bundle_sha256'):
        stripped.pop(k)
    for entry, stripped_entry in zip(new['entries'], stripped['entries']):
        for c, wrapper in entry['readers'].items():
            stripped_entry['readers'][c].pop('explicitly_referenced_shared_evidence')
            original = next(a for a in docs[c]['answers'] if a['id'] == entry['id'])
            assert wrapper['complete_original_entry'] == original
            assert digest(raw[c]) == wrapper['raw_file_sha256']
            piece = raw[c][wrapper['start_byte']:wrapper['end_byte']]
            assert json.loads(piece) == original
            assert digest(piece) == wrapper['raw_entry_sha256']
            assert normalized(original) == wrapper['normalized_entry_sha256']
            joined = wrapper['explicitly_referenced_shared_evidence']
            assert joined['raw_reader_sha256'] == digest(raw[c])
            pool = docs[c].get('evidence_units', [])
            assert normalized(pool) == joined['complete_pool_normalized_sha256']
            expected = refs(original) if pool else []
            by_number = pool if isinstance(pool, dict) else {u.get('number', u.get('id')): u for u in pool}
            assert len(by_number) == len(pool)
            actual = joined['resolved_units']
            assert [u.get('original_entry_reference_value', u['reference']) for u in actual] == list(dict.fromkeys(a for a, _ in expected))
            for u in actual:
                number = u['reference']
                unit = u['original_unit']
                assert unit == by_number[number]
                assert normalized(unit) == u['original_unit_sha256']
                s = u['original_raw_unit_span']
                assert pointer(docs[c], s['json_pointer']) == unit
                raw_unit = raw[c][s['start_byte']:s['end_byte']]
                assert json.loads(raw_unit) == unit
                assert digest(raw_unit) == s['raw_sha256']
                decoded = raw[c].decode()
                assert decoded[s['start_char']:s['end_char']].encode() == raw_unit
                assert normalized(unit) == s['normalized_sha256']
                original_reference = u.get('original_entry_reference_value', number)
                expected_paths = [p for a, p in expected if a == original_reference]
                assert u['explicit_reference_paths_in_original_entry'] == expected_paths
                assert all(pointer(original, p) == original_reference for p in expected_paths)
                # Source correctness is assessed by graders; preserve wrong original evidence.
                # Exact original referent bytes and same-entry links remain mandatory.
            checks.append({'reader': c, 'id': entry['id'], 'raw_entry_sha256': digest(piece),
                           'explicit_reference_occurrences': len(expected),
                           'resolved_unit_count': len(actual), 'pass': True})
    assert stripped == old, 'A field other than explicit reference metadata changed'

assert len(checks) == expected_entry_count
report = {'pass': True, 'implementation': 'Separate verification without importing materializer',
          'unchanged_original_bundles_except_reference_metadata': True,
          'all_original_raw_entry_byte_spans_verified': True,
          'raw_entry_count': expected_entry_count,
          'all_referents_exact_original_same_entry_references': True,
          'all_referent_raw_bytes_and_json_pointers_verified': True,
          'source_quote_correctness_not_assumed_or_used_to_filter_original_evidence': True,
          'raw_reader_sha256': {c: digest(b) for c, b in raw.items()},
          'pool_counts': {c: len(docs[c].get('evidence_units', [])) for c in 'ab'},
          'checks': checks}
dest = IT / 'materialized-reference-integrity-validation.json'
assert not dest.exists()
dest.write_text(json.dumps(report, indent=2) + '\n')
print('PASS:', expected_entry_count, 'original raw byte spans; exact explicit same-entry reference joins')
