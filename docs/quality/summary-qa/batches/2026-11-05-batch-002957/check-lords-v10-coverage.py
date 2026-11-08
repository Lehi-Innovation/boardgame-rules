"""Verify current39 coverage, declared source limits, and original-source reuse."""
from pathlib import Path
from datetime import datetime, timezone
import ast
import base64
import hashlib
import json
import re
import fitz

B = Path(__file__).resolve().parent
REPO = B.parents[4]
R = REPO / 'docs/quality/summary-qa/lords-of-vegas' / B.name
load = lambda p: json.loads(p.read_text())
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
HB = lambda b: hashlib.sha256(b).hexdigest()
AP = R / 'source-key-v10-review.json'
d, old = load(AP), load(R / 'source-key-v9-review.json')
assert d['verdict'] == 'PASS_FOR_DECLARED_EXPANDED_V10_SOURCE_LIMITS_BENCHMARK'
assert old['verdict'] == 'NOT_PASS_UNQUALIFIED_STRICT_SOURCE_BENCHMARK'
assert d['coverage_stopping_rule']['accepted_remaining_distinct_source_supported_gap_count'] == 0
assert d['Q39_determination']['verdict'] == 'SUPPORTED_AND_COVERS_THE_ACCEPTED_ACTOR_GAP'
rp = Path('/mnt/c/Users/jonny/.codex/sessions/2026/11/06/rollout-2026-11-06T16-31-02-01a1b333-8d3b-7002-acbd-35553310a62a.jsonl')
tree = ast.parse((B / 'check-spirit-source09-delivery.py').read_text())
functions = [x for x in tree.body if isinstance(x, ast.FunctionDef) and x.name in ('strings', 'literal_image_paths')]
ns = {'json': json, 're': re, 'resolve': lambda p: Path(p) if Path(p).is_absolute() else REPO / p}
exec(compile(ast.Module(body=functions, type_ignores=[]), '<literal-data-parsers>', 'exec'), ns)
raw = rp.read_bytes().splitlines(keepends=True)
calls, outputs, contexts, old_writers, writers = {}, [], [], [], []
for n, line in enumerate(raw, 1):
    row = json.loads(line); p = row.get('payload', {})
    if row.get('type') == 'session_meta':
        assert p['id'] == '01a1b333-8d3b-7002-acbd-35553310a62a' and p['parent_thread_id'] == '01a1b2c1-d5d1-7333-8948-72708b3d1f3e'
        assert p['agent_path'] == '/root/source_key_v9_review'
    if row.get('type') == 'turn_context':
        contexts.append({'record': n, 'model': p.get('model'), 'effort': p.get('effort')})
    if row.get('type') != 'response_item':
        continue
    if p.get('type') in ('custom_tool_call', 'function_call'):
        t = p.get('input', p.get('arguments', ''))
        assert isinstance(t, str)
        assert not any(x in t for x in ('rules/lords-of-vegas.md', 'summary-snapshot.md', 'reader-a.json', 'reader-b.json',
            'results.json', 'source-audit.json', 'tie-actor-source-review.json', 'source-only-v8-review.json',
            'list_agents', 'read_thread', 'wait_threads'))
        calls[p['call_id']] = (n, t)
        write = any(x in t for x in ('write_text', 'writeFile', 'apply_patch', 'json.dump(', '.write('))
        if 'source-key-v9-review.json' in t and write:
            old_writers.append(n)
        if AP.name in t and write:
            writers.append(n)
    elif p.get('type') in ('custom_tool_call_output', 'function_call_output'):
        outputs.append((n, p, list(ns['strings'](p.get('output')))))
assert contexts and all(x['model'] == 'gpt-6.1-sol' and x['effort'] == 'high' for x in contexts)
assert old_writers and writers
old_boundary, boundary = min(old_writers), min(writers)
assert old_boundary < boundary


def check_text(f, first, last):
    p = Path(f['path']); t = p.read_text(); cursor = 0; parts = []
    assert H(p) == f['byteSHA256'] and len(t) == f['character_count']
    for c in f['receipts']:
        a, z = c['start'], c['end']
        assert a == cursor and a < z <= len(t) and t[a:z] == c['exact_text']
        assert HB(t[a:z].encode()) == c['chunkSHA256']
        matches = [n for n, _, vals in outputs if first <= n < last and any(t[a:z] in v or json.dumps(t[a:z], ensure_ascii=False)[1:-1] in v for v in vals)]
        assert matches, (str(p), a, z)
        parts.append({'start': a, 'end': z, 'slice_sha256': c['chunkSHA256'], 'actual_output_records': matches})
        cursor = z
    assert cursor == len(t)
    return {'path': str(p), 'sha256': H(p), 'complete': True, 'parts': parts}


sources = [check_text(f, 0, old_boundary) for f in old['full_read_receipts'][:2]]
assert len(sources) == 2
for x in d['authority_hashes_and_reused_full_read_receipt_hashes']:
    assert H(Path(x['path'])) == x['byteSHA256']
    if 'previously_read_receipt_hashes' in x:
        p = Path(x['path']); t = p.read_text(); original = next(v for v in sources if v['path'] == str(p))
        assert [(c['start'], c['end'], c['chunkSHA256']) for c in x['previously_read_receipt_hashes']] == [(c['start'], c['end'], c['slice_sha256']) for c in original['parts']]
current = [check_text(f, old_boundary, boundary) for f in d['new_input_full_read_receipts']]
assert len(current) == 5
native, inline = [], []
pdf_path = B / 'source-preflight/lords-of-vegas/unified-2022/mayfair-unified-rulebook.pdf'
pdf = fitz.open(pdf_path)
for n, p, vals in outputs:
    out = p.get('output')
    if n >= old_boundary or not isinstance(out, list):
        continue
    images = [x for x in out if isinstance(x, dict) and x.get('type') == 'input_image']
    if not images:
        continue
    cn, t = calls[p['call_id']]
    if 'view_image' in t:
        paths = ns['literal_image_paths'](t)
        assert len(paths) == len(images)
        native.extend({'path': path, 'sha256': H(Path(path)), 'call_record': cn, 'output_record': n} for path in sorted(paths))
    else:
        assert 'mayfair-unified-rulebook.pdf' in t and 'fitz.open(p)' in t and 'get_pixmap' in t
        if 'Matrix(1.8,1.8)' in t:
            assert 'd[8]' in t
            pages, scale = [9], 1.8
        else:
            assert 'for(const page of [11,13,15,16])' in t and 'Matrix(1.5,1.5)' in t and '${page-1}' in t
            pages, scale = [11, 13, 15, 16], 1.5
        assert len(pages) == len(images)
        for page, block in zip(pages, images):
            data = block['image_url']; data = data['url'] if isinstance(data, dict) else data
            assert data.startswith('data:image/png;base64,')
            payload = base64.b64decode(data.split(',', 1)[1])
            reproduced = pdf[page-1].get_pixmap(matrix=fitz.Matrix(scale, scale)).tobytes('png')
            assert payload == reproduced
            inline.append({'source_pdf': str(pdf_path), 'source_sha256': H(pdf_path), 'physical_page': page,
                'scale': scale, 'actual_model_png_sha256': HB(payload), 'independent_rerender_byte_identical': True,
                'call_record': cn, 'output_record': n})
assert len(native) == 4 and len(inline) == 5
v = R / 'expanded-v10'
qs = load(v / 'questions.json')['questions']; ks = load(v / 'grading-key.json')['answers']; ss = load(v / 'scope-map.json')['entries']
assert len(qs) == len(ks) == len(ss) == len(d['per_question_checks']) == 39
assert qs[:38] == load(R / 'expanded-v8/questions.json')['questions']
current_baseline = load(v / 'answer-key.json')['answers'][:38]
old_baseline = load(R / 'expanded-v8/answer-key.json')['answers']
assert [x['id'] for x, y in zip(current_baseline, old_baseline) if x != y] == ['Q27']
correction_path = R / 'expanded-v9/source-key-correction.json'
assert correction_path.is_file()
for q, k, s, review in zip(qs, ks, ss, d['per_question_checks']):
    assert q['id'] == k['id'] == s['id'] == review['id']
    assert q['question'] == k['asked_question'] == s['asked_question'] == review['actual_asked_question']
    assert k['required_answer_facts'] == s['required_answer_facts']
    assert [x['fact'] for x in review['required_fact_checks']] == k['required_answer_facts']
    assert all(x['verdict'].startswith('SUPPORTED') for x in review['required_fact_checks'])
result = {'verified': True, 'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'N': 39,
    'required_facts': sum(len(x['required_answer_facts']) for x in ks),
    'coverage_report_path': str(AP), 'coverage_report_sha256': H(AP), 'coverage_verdict': d['verdict'],
    'qualification': d['qualification'], 'original_v9_NOT_PASS_preserved': H(R / 'source-key-v9-review.json'),
    'runtime_path': str(rp), 'runtime_sha256_at_check': H(rp), 'actual_contexts': contexts,
    'initial_source_and_native_report_boundary': old_boundary, 'current_report_boundary': boundary,
    'actual_initial_complete_primary_texts': sources, 'current_complete_bank_inputs': current,
    'original_native_views': native, 'original_pdf_native_views_independently_rerendered': inline,
    'stopping_rule': d['coverage_stopping_rule'],
    'current_bank_hashes': {n: H(v / n) for n in ('questions.json', 'grading-key.json', 'scope-map.json', 'answer-key.json')},
    'original38_questions_and_other37_baseline_answers_preserved': True,
    'Q27_genuine_versioned_source_key_correction': {'path': str(correction_path), 'sha256': H(correction_path),
        'old_v8_record_preserved_in_old_benchmark': True, 'only_existing_baseline_answer_record_changed': 'Q27'},
    'limits': 'Same initially fresh source-only reviewer completed its own source-limits/added-Q39 challenge. Source reads and9 original native views are verified own-history reuse, not new deliveries. Current39 bank fully delivered. This is qualified source-knowledge coverage, not a recovered mandatory physical tie-roller ruling, blind-reader acceptance or publication approval.'}
out = B / 'coordinator-checks/lords-v10-current39-coverage.json'
assert not out.exists()
out.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'verified': True, 'N': 39, 'facts': result['required_facts'], 'original_complete_primary_texts': 2,
    'current_full_inputs': 5, 'original_native_views': len(native)+len(inline), 'pdf_pixel_reproductions': len(inline), 'report': str(out)}))
