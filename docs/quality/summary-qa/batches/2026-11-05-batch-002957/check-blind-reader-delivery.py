"""Check actual blind-reader input delivery for a frozen game iteration."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import ast
import hashlib
import json
import re
import subprocess

p = argparse.ArgumentParser()
p.add_argument('--slug', required=True)
p.add_argument('--iteration', required=True)
p.add_argument('--reader-a', required=True)
p.add_argument('--reader-b', required=True)
p.add_argument('--reader-a-output', help='Preserved complete same-reader output filename, if an unfinished artifact also exists')
p.add_argument('--reader-b-output', help='Preserved complete same-reader output filename, if an unfinished artifact also exists')
p.add_argument('--allow-historical-snapshot', action='store_true')
p.add_argument('--manifest', help='Input manifest path relative to the iteration, for a nested revalidation directory')
args = p.parse_args()
B = Path(__file__).resolve().parent
REPO = B.parents[4]
R = REPO / 'docs/quality/summary-qa' / args.slug / B.name
D = R / args.iteration
assert D.resolve().is_relative_to(R.resolve()) and D != R and D.is_dir()
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
HB = lambda b: hashlib.sha256(b).hexdigest()
load = lambda p: json.loads(p.read_text())
manifest_path = (D / (args.manifest or 'input-manifest.json')).resolve()
assert manifest_path.is_relative_to(R.resolve())
m = load(manifest_path)
for name, digest in m.get('inputs', m.get('hashes', m.get('sha256', {}))).items():
    # Some manifests bind each hash together with its character count.
    digest = digest['sha256'] if isinstance(digest, dict) else digest
    assert H(D / name) == digest, name
summary = D / 'summary-snapshot.md'
canonical_body_matches = summary.read_bytes() == (REPO / 'rules' / (args.slug + '.md')).read_bytes()
assert canonical_body_matches or args.allow_historical_snapshot
questions = load(D / 'questions.json')['questions']
ids = [x['id'] for x in questions]
assert len(ids) == len(set(ids))
tree = ast.parse((B / 'check-spirit-source09-delivery.py').read_text())
fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'strings')
ns = {'json': json}
exec(compile(ast.Module(body=[fn], type_ignores=[]), '<literal-string-walker>', 'exec'), ns)
strings = ns['strings']
runtime_paths = subprocess.run(['rg', '--files', '/mnt/c/Users/jonny/.codex/sessions'], check=True, capture_output=True, text=True).stdout.splitlines()
manifest = load(B / 'manifest.json')
game = next(x for x in manifest['games'] if x['slug'] == args.slug)
results = []
for who, ident in [('a', args.reader_a), ('b', args.reader_b)]:
    raw_path = D / (getattr(args, 'reader_' + who + '_output') or ('reader-' + who + '.json'))
    assert raw_path.resolve().parent == D.resolve()
    raw_answers = load(raw_path)
    answers = raw_answers['answers']
    assert [x['id'] for x in answers] == ids
    runtime = next(Path(x) for x in runtime_paths if x.endswith(ident + '.jsonl'))
    records = runtime.read_bytes().splitlines(keepends=True)
    rows = {i: json.loads(v) for i, v in enumerate(records, 1)}
    contexts, outputs, calls, writes = [], [], [], []
    for n, row in rows.items():
        d = row.get('payload', {})
        if row.get('type') == 'session_meta':
            assert d['id'] == ident and d['parent_thread_id'] == game['thread_id']
        if row.get('type') == 'turn_context':
            contexts.append({'record': n, 'model': d.get('model'), 'effort': d.get('effort')})
        if row.get('type') != 'response_item':
            continue
        if d.get('type') in ('custom_tool_call', 'function_call'):
            t = d.get('input', d.get('arguments', ''))
            assert isinstance(t, str)
            assert not any(x in t for x in ('answer-key.json', 'grading-key.json', 'scope-map.json',
                'asked-facts.json', 'source-audit', 'source_pdfs/', 'extracted/', 'list_agents',
                'read_thread', 'wait_threads', 'search_query', 'web__', 'reader-' + ('b' if who == 'a' else 'a') + '.json'))
            calls.append({'record': n, 'name': d.get('name'), 'input_sha256': HB(t.encode())})
            if raw_path.name in t and any(x in t for x in ('write_text', 'writeFile', 'apply_patch')):
                writes.append(n)
        elif d.get('type') in ('function_call_output', 'custom_tool_call_output'):
            outputs.append((n, list(strings(d.get('output')))))
    assert contexts and all(x['model'] == 'gpt-6-luna' and x['effort'] == 'high' for x in contexts)
    assert writes
    boundary = min(writes)
    receipt = raw_answers.get('delivery_receipt', raw_answers.get('inputs_read'))
    assert receipt is not None
    if isinstance(receipt, list):
        if receipt and (any(k in receipt[0] for k in ['char_start', 'character_start'])
                        or 'start' in receipt[0] and 'end' in receipt[0] and 'total' in receipt[0]):
            grouped = {}
            for c in receipt:
                named = c['path']
                total = c.get('char_total', c.get('character_total', c.get('total')))
                f = grouped.setdefault(named, {'path': named, 'total_characters': total,
                    'sha256': c['utf8_file_sha256'], 'chunks': []})
                assert f['total_characters'] == total and f['sha256'] == c['utf8_file_sha256']
                f['chunks'].append({'start': c.get('char_start', c.get('character_start', c.get('start'))),
                    'end': c.get('char_end', c.get('character_end', c.get('end'))), 'sha256': c['chunk_sha256']})
            files = list(grouped.values())
        else:
            files = receipt
    else:
        files = receipt.get('files')
        if files is None:
            if 'range_receipts' in receipt:
                def receipt_path(value):
                    path = Path(value)
                    return (path if path.is_absolute() else REPO / path).resolve()
                files = []
                for label, metadata in receipt.items():
                    if label == 'range_receipts':
                        continue
                    assert isinstance(metadata, dict) and 'path' in metadata
                    chunks = [c for c in receipt['range_receipts']
                              if receipt_path(c['path']) == receipt_path(metadata['path'])]
                    files.append(dict(metadata, chunks=chunks))
                assert sum(len(f['chunks']) for f in files) == len(receipt['range_receipts'])
            elif 'summary_chunks' in receipt and 'questions_chunks' in receipt:
                files = [{'path': str(D / name), 'chunks': receipt[label],
                          'total_characters': len((D / name).read_text()),
                          'sha256': H(D / name), 'raw_file_hash_supplied': False}
                         for name, label in [('summary-snapshot.md', 'summary_chunks'), ('questions.json', 'questions_chunks')]]
            else:
                files = [dict(v, path=str(D / name), chunks=v['ranges']) for name, v in receipt.items()]
    text_checks = []
    for f in files:
        named = f.get('path', f.get('filename'))
        fp = Path(named) if named else D / f['file']
        fp = fp if fp.is_absolute() else REPO / fp
        t = fp.read_text(); cursor = 0; parts = []
        file_digest = next((f[k] for k in ['sha256', 'file_sha256', 'file_sha256_utf8', 'sha256_utf8', 'file_bytes_sha256', 'utf8_file_sha256'] if k in f), None)
        total_characters = next((f[k] for k in ['total_characters', 'total_unicode_characters', 'char_total', 'total_chars', 'character_length', 'characters'] if k in f), None)
        # Missing receipt metadata is distinct from actual missing delivery:
        # frozen hashes and literal original payloads are still checked below.
        assert (file_digest is None or H(fp) == file_digest) and len(t) == total_characters
        # Some readers print explicit byte-offset headers but describe their
        # ranges as characters in the final receipt. Rebind to the actual
        # original byte headers and literal decoded output, preserving that
        # metadata diagnostic instead of inventing missing input.
        data = fp.read_bytes()
        byte_parts = {}
        header = re.compile(r'filename=([^\n]+)\nstart=(\d+) end=(\d+) total=(\d+)\nsha256=([a-f0-9]{64})\n---CHUNK---\n')
        for n, vals in outputs:
            if n >= boundary:
                continue
            for value in vals:
                for match in header.finditer(value):
                    named_path = Path(match[1].strip())
                    named_path = named_path if named_path.is_absolute() else REPO / named_path
                    if named_path != fp or int(match[4]) != len(data):
                        continue
                    a, z = int(match[2]), int(match[3])
                    if not 0 <= a < z <= len(data) or HB(data[a:z]) != match[5]:
                        continue
                    try:
                        chunk = data[a:z].decode('utf-8')
                    except UnicodeDecodeError:
                        continue
                    if value[match.end():match.end()+len(chunk)] == chunk:
                        byte_parts.setdefault((a, z), set()).add(n)
        if byte_parts:
            byte_cursor = 0
            for (a, z), records_seen in sorted(byte_parts.items()):
                assert a == byte_cursor
                parts.append({'start': a, 'end': z, 'slice_sha256': HB(data[a:z]),
                    'actual_output_records': sorted(records_seen)})
                byte_cursor = z
            assert byte_cursor == len(data)
            text_checks.append({'path': str(fp), 'sha256': H(fp), 'complete': True,
                'offset_unit': 'bytes; exact contiguous UTF8-decodable original chunks',
                'raw_receipt_metadata_preserved': f,
                'metadata_qualification': 'Actual original tool headers identify byte offsets. Final reader receipt labels/ends are metadata only; all bytes through actual EOF were independently visible before answer writing.',
                'parts': parts})
            continue
        for chunk_index, c in enumerate(f.get('chunks', f.get('contiguous_ranges', f.get('ranges', f.get('read_ranges'))))):
            c = {'start': c[0], 'end': c[1]} if isinstance(c, list) else c
            a = c.get('start', c.get('start_character', c.get('char_start')))
            declared_end = c.get('end', c.get('end_character', c.get('char_end')))
            z = min(declared_end, len(t))
            digest = c.get('sha256', c.get('chunk_sha256', c.get('chunk_sha256_utf8')))
            if digest is None and isinstance(f.get('chunk_sha256_utf8'), list):
                digest = f['chunk_sha256_utf8'][chunk_index]
            if digest is None and isinstance(f.get('range_sha256'), list):
                digest = f['range_sha256'][chunk_index]
            actual_digest = HB(t[a:z].encode())
            assert a == cursor and a < z <= len(t)
            assert digest is None or actual_digest == digest
            matches = [n for n, vals in outputs if n < boundary and any(t[a:z] in x or json.dumps(t[a:z], ensure_ascii=False)[1:-1] in x for x in vals)]
            assert matches, (who, str(fp), a, z)
            parts.append({'start': a, 'end': z, 'declared_end': declared_end,
                'metadata_endpoint_clamped_to_actual_eof': declared_end != z,
                'slice_sha256': actual_digest, 'raw_slice_hash_supplied': digest is not None,
                'actual_output_records': matches})
            cursor = z
        assert cursor == len(t)
        text_checks.append({'path': str(fp), 'sha256': H(fp), 'complete': True,
            'raw_file_hash_supplied': f.get('raw_file_hash_supplied', file_digest is not None),
            'offset_unit': 'Unicode characters', 'parts': parts})
    assert len(text_checks) == 2
    assert sum(Path(x['path']).resolve() == summary.resolve() for x in text_checks) == 1
    delivered_questions = [Path(x['path']) for x in text_checks if Path(x['path']).resolve() != summary.resolve()]
    assert len(delivered_questions) == 1 and delivered_questions[0].resolve().parent == D.resolve()
    assert load(delivered_questions[0])['questions'] == questions
    results.append({'reader': who, 'id': ident, 'raw_path': str(raw_path), 'raw_sha256': H(raw_path),
        'runtime_path': str(runtime), 'runtime_sha256_at_check': H(runtime), 'contexts': contexts,
        'conservative_answer_writer_boundary': boundary, 'text_checks': text_checks, 'calls': calls})
result = {'verified': True, 'checked_at_utc': datetime.now(timezone.utc).isoformat(),
    'slug': args.slug, 'iteration': args.iteration, 'N': len(ids), 'summary_sha256': H(summary),
    'canonical_body_matches_at_check': canonical_body_matches,
    'historical_snapshot_check_explicitly_requested': args.allow_historical_snapshot,
    'input_manifest_path': str(manifest_path), 'input_manifest_sha256': H(manifest_path), 'readers': results,
    'limits': 'Actual whole frozen summary/question delivery, exact saved raw IDs and blind source-access trace checked. Current canonical equality is reported separately; a historical-snapshot check cannot approve newer body bytes. Explicit fresh-context dispatch is checked separately from original parent metadata. This does not grade answers or approve source/coverage/publication. No plaintext-to-ciphertext equality is claimed.'}
target = B / 'coordinator-checks' / (args.slug + '-' + args.iteration.replace('/', '-') + '-blind-inputs-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f') + '.json')
target.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'verified': True, 'N': len(ids), 'readers': len(results), 'report': str(target)}))
