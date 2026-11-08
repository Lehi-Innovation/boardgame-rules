"""Preserve raw entries while losslessly resolving their explicit shared evidence."""
from pathlib import Path
import copy
import hashlib
import json
import re
import sys

R = Path(__file__).parent.resolve()
IT = (R / sys.argv[1]).resolve()
assert IT.is_relative_to(R)
DEST = IT / 'grading-inputs-v2'
assert not DEST.exists()


def sha(value):
    return hashlib.sha256(value).hexdigest()


def objsha(value):
    return sha(json.dumps(value, sort_keys=True, ensure_ascii=False,
                          separators=(',', ':')).encode())


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate JSON key: ' + key)
        result[key] = value
    return result


def read(path):
    return json.loads(path.read_text(), object_pairs_hook=unique)


def collection_spans(path, field):
    text = path.read_text()
    doc = read(path)
    decoder = json.JSONDecoder(object_pairs_hook=unique)
    candidates = []
    for match in re.finditer('"' + re.escape(field) + r'"\s*:\s*([\[{])', text):
        start = match.end() - 1
        try:
            value, stop = decoder.raw_decode(text, start)
        except ValueError:
            continue
        if value == doc[field]:
            candidates.append((start, stop))
    assert len(candidates) == 1
    start, stop = candidates[0]
    pos, spans = start + 1, []
    dictionary = isinstance(doc[field], dict)
    expected = list(doc[field].items()) if dictionary else list(enumerate(doc[field]))
    while pos < stop:
        while text[pos].isspace() or text[pos] == ',':
            pos += 1
        if text[pos] in ']}':
            break
        if dictionary:
            key, pos = decoder.raw_decode(text, pos)
            while text[pos].isspace():
                pos += 1
            assert text[pos] == ':'
            pos += 1
            while text[pos].isspace():
                pos += 1
        else:
            key = len(spans)
        value, end = decoder.raw_decode(text, pos)
        assert (key, value) == expected[len(spans)]
        escaped = str(key).replace('~', '~0').replace('/', '~1')
        spans.append({'collection_key': key,
                      'json_pointer': f'/{field}/{escaped}',
                      'start_char': pos, 'end_char': end,
                      'start_byte': len(text[:pos].encode()),
                      'end_byte': len(text[:end].encode()),
                      'raw_sha256': sha(text[pos:end].encode()),
                      'normalized_sha256': objsha(value)})
        pos = end
    assert len(spans) == len(doc[field])
    return spans


def evidence_refs(value, pointer=''):
    if isinstance(value, dict):
        for key, item in value.items():
            child = pointer + '/' + key.replace('~', '~0').replace('/', '~1')
            if key in ['evidence', 'evidence_refs', 'evidence_ids'] and isinstance(item, list):
                for index, ref in enumerate(item):
                    if isinstance(ref, (str, int)):
                        yield ref, child + '/' + str(index)
            yield from evidence_refs(item, child)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from evidence_refs(item, pointer + '/' + str(index))


summary = (IT / 'summary-snapshot.md').read_text()
readers = {c: read(IT / f'reader-{c}.json') for c in ['a', 'b']}
pools = {}
for label, doc in readers.items():
    path = IT / f'reader-{label}.json'
    units = doc.get('evidence_units', [])
    spans = collection_spans(path, 'evidence_units') if units else []
    dictionary = isinstance(units, dict)
    values = list(units.values()) if dictionary else units
    pool = {}
    for unit, span in zip(values, spans):
        number = span['collection_key'] if dictionary else unit.get('number', unit.get('id'))
        assert number is not None and number not in pool
        source_span = unit.get('source_span', unit) if isinstance(unit, dict) else {}
        text = unit.get('text') if isinstance(unit, dict) else None
        literal_match = text in summary if isinstance(text, str) else None
        span_match = (summary[source_span['start']:source_span['end']] == text
                      if isinstance(text, str) and isinstance(source_span.get('start'), int)
                      and isinstance(source_span.get('end'), int) else None)
        pool[number] = {'reference': number, 'original_unit': unit,
                        'original_unit_sha256': objsha(unit),
                        'original_raw_unit_span': span,
                        'unit_text_matches_frozen_summary': literal_match,
                        'declared_source_span_matches_text': span_match,
                        'source_diagnostic_policy': 'Preserve all original evidence even if quote/span is wrong; graders assess substantive errors. No filtering or automatic grade cap.'}

    pools[label] = pool

original = read(IT / 'grading-inputs/manifest.json')
DEST.mkdir()
blocks, checks = [], []
for block in original['blocks']:
    source_path = Path(block['path'])
    bundle = read(source_path)
    new = copy.deepcopy(bundle)
    for entry in new['entries']:
        for label, wrapper in entry['readers'].items():
            raw = wrapper['complete_original_entry']
            actual = next(a for a in readers[label]['answers'] if a['id'] == entry['id'])
            assert raw == actual
            assert wrapper['normalized_entry_sha256'] == objsha(actual)
            references = list(evidence_refs(raw)) if pools[label] else []
            resolved = []
            for reference in dict.fromkeys(ref for ref, _ in references):
                pool_key = reference if reference in pools[label] else str(reference)
                assert pool_key in pools[label], (label, entry['id'], reference)
                value = copy.deepcopy(pools[label][pool_key])
                value['original_entry_reference_value'] = reference
                value['explicit_reference_paths_in_original_entry'] = [p for ref, p in references if ref == reference]
                resolved.append(value)
            wrapper['explicitly_referenced_shared_evidence'] = {
                'raw_reader_path': str(IT / f'reader-{label}.json'),
                'raw_reader_sha256': sha((IT / f'reader-{label}.json').read_bytes()),
                'pool_field': '/evidence_units' if pools[label] else None,
                'complete_pool_normalized_sha256': objsha(readers[label].get('evidence_units', [])),
                'resolved_units': resolved,
                'no_unreferenced_units_added': True,
                'raw_entry_not_rewritten': True,
            }
            checks.append({'reader': label, 'id': entry['id'],
                           'original_raw_entry_sha256': wrapper['raw_entry_sha256'],
                           'normalized_raw_entry_unchanged': True,
                           'explicit_reference_occurrences': len(references),
                           'unique_resolved_unit_count': len(resolved),
                           'all_references_resolved': True,
                           'only_explicitly_referenced_units_attached': True})
    new['reference_resolution_policy'] = (
        'Complete original raw fields/spans/hashes are unchanged. An entry may '
        'explicitly reference a top-level shared evidence unit. Its exact full '
        'referent is attached under explicitly_referenced_shared_evidence with '
        'original JSON pointer/raw byte span/hash. Treat the referenced quote '
        'as evidence supplied for that entry; do not borrow unreferenced units '
        'or another answer. A reader format difference alone is not a factual '
        'failure; all substantive fields and material contradictions still count.')
    new['original_bundle_path'] = str(source_path)
    new['original_bundle_sha256'] = sha(source_path.read_bytes())
    path = DEST / source_path.name
    path.write_text(json.dumps(new, indent=2, ensure_ascii=False) + '\n')
    blocks.append({**block, 'path': str(path), 'sha256': sha(path.read_bytes())})
report = {**original, 'blocks': blocks,
          'original_manifest_path': str(IT / 'grading-inputs/manifest.json'),
          'reference_materializer_version': 2,
          'dictionary_and_array_pools_preserved': True,
          'invalid_reader_quotes_preserved_for_grading_not_dropped': True,
          'resolution_check_count': len(checks), 'resolution_checks': checks,
          'raw_reader_outputs_unchanged': True,
          'question_key_scope_unchanged': True,
          'all_original_raw_fields_and_exact_spans_preserved': True,
          'all_shared_referents_exact_and_explicit': True,
          'pool_unit_counts': {c: len(pool) for c, pool in pools.items()}}
assert len(checks) == 2 * original['question_count']
(DEST / 'manifest.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
print('Resolved', len(checks), 'whole entries without changing any raw answer; pool units', report['pool_unit_counts'])
