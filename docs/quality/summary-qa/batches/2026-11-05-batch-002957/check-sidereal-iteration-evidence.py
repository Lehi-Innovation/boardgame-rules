"""Check frozen Sidereal inputs, original runtime delivery and full-entry grading."""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import argparse
import hashlib
import json

parser = argparse.ArgumentParser()
parser.add_argument('--iteration', required=True)
parser.add_argument('--require-pass', action='store_true')
parser.add_argument('--allow-historical', action='store_true')
args = parser.parse_args()
assert not (args.require_pass and args.allow_historical)
B = Path(__file__).resolve().parent
REPO = B.parents[4]
R = REPO / 'docs/quality/summary-qa/sidereal-confluence' / B.name
D = R / args.iteration
assert D.parent == R and D.is_dir()
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
HB = lambda b: hashlib.sha256(b).hexdigest()
load = lambda p: json.loads(p.read_text())
m = load(D / 'input-manifest.json')
for name, digest in m['hashes'].items():
    assert H(D / name) == digest, name
s = (D / 'summary-snapshot.md').read_text()
canonical_matches = (D / 'summary-snapshot.md').read_bytes() == (REPO / 'rules/sidereal-confluence.md').read_bytes()
assert canonical_matches or args.allow_historical
qs = load(D / 'questions.json')['questions']
keys = load(D / 'answer-key.json')['answers']
scope = load(D / 'asked-facts.json')['questions']
ids = [x['id'] for x in qs]
assert len(ids) == len(set(ids)) == m['question_count']
assert [x['id'] for x in keys] == [x['id'] for x in scope] == ids
qmap, kmap, smap = ({x['id']: x for x in v} for v in (qs, keys, scope))
assert all(kmap[i]['required_facts'] == smap[i]['required_facts'] for i in ids)
nfacts = sum(len(x['required_facts']) for x in scope)
assert nfacts == m['required_facts_per_reader']


def strings(v):
    if isinstance(v, str):
        yield v
        try:
            w = json.loads(v)
        except ValueError:
            return
        if w != v:
            yield from strings(w)
    elif isinstance(v, dict):
        if v.get('type') in ('input_image', 'image'):
            return
        for x in v.values():
            yield from strings(x)
    elif isinstance(v, list):
        for x in v:
            yield from strings(x)


def bind_delivery(path, role):
    d = load(path); rp = Path(d['runtime_source_path'])
    raw = rp.read_bytes().splitlines(keepends=True)
    rows = {i: json.loads(v) for i, v in enumerate(raw, 1)}
    boundary = d['first_answer_file_write_record_ordinal'] if role == 'reader' else d['first_report_write_record_ordinal']
    inputs = []
    for f in d['input_delivery']:
        p = Path(f.get('source_path', f.get('file')))
        digest = f.get('source_sha256', f.get('sha256'))
        assert H(p) == digest
        t = p.read_text(); cursor = 0; parts = []
        for c in f.get('complete_nontruncated_ranges', f.get('ranges')):
            a, z = c['start'], c['end']
            assert a == cursor and a < z <= len(t)
            assert HB(t[a:z].encode()) == c.get('slice_sha256_utf8', c.get('sha256'))
            matches = c.get('matching_runtime_outputs', c.get('matching_runtime_outputs'))
            assert matches
            for v in matches:
                n = v['ordinal']
                assert n < boundary and HB(raw[n-1]) == v['record_sha256']
                pld = rows[n]['payload']
                assert pld['type'] in ('function_call_output', 'custom_tool_call_output')
                vals = list(strings(pld.get('output')))
                assert any(t[a:z] in x or json.dumps(t[a:z], ensure_ascii=False)[1:-1] in x for x in vals)
            parts.append({'start': a, 'end': z, 'actual_output_records': [v['ordinal'] for v in matches]})
            cursor = z
        assert cursor == len(t)
        inputs.append({'path': str(p), 'sha256': digest, 'complete': True, 'parts': parts})
    contexts, call_hashes = [], []
    for n, row in rows.items():
        p = row.get('payload', {})
        if row.get('type') == 'turn_context':
            contexts.append({'record': n, 'model': p.get('model'), 'effort': p.get('effort')})
        if row.get('type') == 'response_item' and p.get('type') in ('function_call', 'custom_tool_call'):
            t = p.get('input', p.get('arguments', ''))
            assert isinstance(t, str)
            if role == 'reader':
                assert not any(x in t for x in ('answer-key.json', 'asked-facts.json', 'grading-block-',
                    'grades-block-', 'source-audit', 'source_pdfs/', 'extracted/', 'list_agents',
                    'read_thread', 'wait_threads', 'web__', 'search_query'))
            call_hashes.append({'record': n, 'name': p.get('name'), 'input_sha256': HB(t.encode())})
    expected = 'gpt-6-luna' if role == 'reader' else 'gpt-6.1-sol'
    assert contexts and all(x['model'] == expected and x['effort'] == 'high' for x in contexts)
    return {'path': str(path), 'sha256': H(path), 'runtime_path': str(rp),
        'runtime_sha256_at_check': H(rp), 'identity': d['identity'], 'inputs': inputs,
        'contexts': contexts, 'first_write_record': boundary, 'calls': call_hashes}


readers, delivery, quote_counts = {}, {}, {}
for who in ('a', 'b'):
    p = D / ('reader-' + who + '.json')
    d = load(p); entries = d['answers']
    assert [x['id'] for x in entries] == ids
    readers[who] = {x['id']: x for x in entries}
    receipt = load(D / ('reader-' + who + '-runtime-delivery.json'))
    assert receipt['raw_response_sha256'] == H(p)
    delivery[who] = bind_delivery(D / ('reader-' + who + '-runtime-delivery.json'), 'reader')
    assert {Path(x['path']).name for x in delivery[who]['inputs']} == {'summary-snapshot.md', 'questions.json'}
    count = [0]

    def check_units(v):
        if isinstance(v, dict):
            if {'start', 'end', 'text'} <= v.keys():
                a, z = v['start'], v['end']
                if isinstance(a, int) and isinstance(z, int):
                    assert s[a:z] == v['text']
                    count[0] += 1
            for x in v.values():
                check_units(x)
        elif isinstance(v, list):
            for x in v:
                check_units(x)
    for x in entries:
        if 'question' in x:
            assert x['question'] == qmap[x['id']]['question']
        check_units(x)
    quote_counts[who] = count[0]
packets = sorted(D.glob('grading-block-[0-9][0-9].json'))
assert packets
seen, grades, grader_delivery, findings = [], {'a': {}, 'b': {}}, [], []
for p in packets:
    packet = load(p); block = p.stem.rsplit('-', 1)[-1]
    ids_block = [x['id'] for x in packet['records']]
    seen.extend(ids_block)
    for x in packet['records']:
        i = x['id']
        assert x['question'] == qmap[i] and x['key'] == kmap[i] and x['asked_scope'] == smap[i]
        for who in ('a', 'b'):
            assert x['reader_' + who + '_original_entry'] == readers[who][i]
    report_path = D / ('grades-block-' + block + '.json')
    report = load(report_path)
    receipt_path = D / ('grades-block-' + block + '-runtime-delivery.json')
    assert load(receipt_path)['report_sha256'] == H(report_path)
    gd = bind_delivery(receipt_path, 'grader')
    assert {Path(x['path']).name for x in gd['inputs']} == {'summary-snapshot.md', p.name}
    grader_delivery.append(gd)
    for who in ('a', 'b'):
        results = report['readers'][who]['results']
        assert [x['id'] for x in results] == ids_block
        for x in results:
            i = x['id']; assert i not in grades[who]
            assert [f['id'] for f in x['required_facts']] == [f['id'] for f in smap[i]['required_facts']]
            if x['grade'] == 'Correct':
                assert all(f['match'] is True for f in x['required_facts'])
                assert not x.get('unsupported_guessing') and not x.get('material_concerns') and not x.get('asked_omissions')
            else:
                findings.append({'reader': who, 'id': i, 'grade': x['grade']})
            grades[who][i] = x
assert seen == ids
scores = {who: dict(Counter(x['grade'] for x in values.values())) for who, values in grades.items()}
assert all(len(v) == len(ids) for v in grades.values())
if args.require_pass:
    assert not findings and all(v == {'Correct': len(ids)} for v in scores.values()), scores
result = {'verified': True, 'checked_at_utc': datetime.now(timezone.utc).isoformat(),
    'iteration': args.iteration, 'N': len(ids), 'required_facts_per_reader': nfacts,
    'summary_sha256': H(D / 'summary-snapshot.md'), 'input_manifest_sha256': H(D / 'input-manifest.json'),
    'scores': scores, 'findings': findings, 'canonical_matches': canonical_matches,
    'historical_evidence_only': args.allow_historical, 'all_complete_original_entries_preserved': True,
    'literal_same_entry_source_units_checked': quote_counts, 'reader_delivery': delivery,
    'grader_delivery': grader_delivery,
    'limits': 'Original full-entry and input-delivery integrity verified. Factual rulings rely on independent whole-entry graders, with separate coordinator spot checks. Coverage, source audit, stamping and publication are separate gates. Runtime dispatch plaintext is not inferred from opaque hashes.'}
target = B / 'coordinator-checks' / ('sidereal-' + args.iteration + '-reader-evidence-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f') + '.json')
target.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'verified': True, 'N': len(ids), 'facts_per_reader': nfacts, 'scores': scores,
    'literal_units': quote_counts, 'report': str(target)}))
