"""Independent exact-byte, full-answer, model and actual-delivery checks."""
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
import argparse
import hashlib
import json
import re

ap = argparse.ArgumentParser()
ap.add_argument('--iteration', required=True)
ap.add_argument('--audit', required=True)
ap.add_argument('--runtime-proof', required=True)
args = ap.parse_args()
base = Path(__file__).resolve().parent
repo = base.parents[4]
run = repo / 'docs/quality/summary-qa/unmatched' / base.name
it = run / args.iteration
assert it.parent == run
read = lambda p: json.loads(p.read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
entry_sha = lambda v: hashlib.sha256(json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
checked = set()

def hashes(values, relative=repo):
    if isinstance(values, list):
        values = {x['path']: x['sha256'] for x in values}
    for name, expected in values.items():
        p = Path(name)
        p = p if p.is_absolute() else relative / p
        expected = expected['sha256'] if isinstance(expected, dict) else expected
        assert sha(p) == expected, str(p)
        checked.add(str(p))

manifest = read(base / 'manifest.json')
game = next(g for g in manifest['games'] if g['slug'] == 'unmatched')
hashes(game['source_hashes'])
frozen = read(it / 'input-manifest.json')
for field in ['hashes', 'prompt_hashes', 'authoritative_source_hashes']:
    hashes(frozen[field])
bank = run / frozen['benchmark']
hashes(read(bank / 'input-manifest.json')['hashes'], bank)
questions = read(it / 'questions.json')['questions']
assert questions == read(bank / 'questions.json')['questions']
ids = [q['id'] for q in questions]
assert len(ids) == 67 and len(set(ids)) == 67
seed = read(run / 'benchmark-v1/questions.json')['questions']
assert questions[:20] == seed
previous_questions = []
historical_banks = []
for old_bank in sorted(run.glob('benchmark-v*'), key=lambda p: int(p.name.rsplit('v', 1)[1])):
    hashes(read(old_bank / 'input-manifest.json')['hashes'], old_bank)
    old_questions = read(old_bank / 'questions.json')['questions']
    assert old_questions[:len(previous_questions)] == previous_questions
    assert old_questions[:20] == seed
    previous_questions = old_questions
    historical_banks.append({'bank': str(old_bank), 'questions': len(old_questions), 'frozen_hashes_preserved': True})
qmap = {q['id']: q for q in questions}
key = {x['id']: x for x in read(bank / 'answer-key.json')['answers']}
scope = {x['id']: x for x in read(bank / 'scope-map.json')['questions']}
assert list(key) == list(scope) == ids
facts = sum(len(scope[i]['required_answer_facts']) for i in ids)
assert facts == 216
snapshot = it / 'summary-snapshot.md'
assert Path(game['summary_path']).read_bytes() == snapshot.read_bytes()
summary = snapshot.read_text()
raw = {}
for who in ['a', 'b']:
    doc = read(it / f'reader-{who}.json')
    entries = doc['answers']
    assert [a['id'] for a in entries] == ids
    raw[who] = {a['id']: a for a in entries}
    for entry in entries:
        for quote in entry['evidence']:
            assert 0 <= quote['start'] < quote['end'] <= len(summary)
            assert quote['text'] == summary[quote['start']:quote['end']]

results = read(it / 'results.json')
assert results['summary_sha256'] == sha(snapshot)
primary = {'a': {}, 'b': {}}
for block in range(1, 5):
    packet_path = it / f'grading/block-{block:02d}-inputs.json'
    packet = read(packet_path)
    grades_path = it / f'grading/block-{block:02d}-grades.json'
    grades = read(grades_path)
    assert grades['block'] == packet['block'] == block
    gh = grades['input_hashes']
    # Independent reports may name the same exact input hash by path or label.
    summary_hashes = [gh[k] for k in ('summary_sha256', 'summary_snapshot_sha256', 'summary', str(snapshot)) if k in gh]
    packet_hashes = [gh[k] for k in ('input_pack_sha256', 'lossless_input_pack_sha256', 'pack', str(packet_path)) if k in gh]
    assert summary_hashes and all(value == sha(snapshot) for value in summary_hashes)
    assert packet_hashes and all(value == sha(packet_path) for value in packet_hashes)
    assert [r['question']['id'] for r in packet['records']] == packet['ids']
    for record in packet['records']:
        ident = record['question']['id']
        assert record['question'] == qmap[ident]
        assert record['fixed_key'] == key[ident]
        assert record['frozen_scope'] == scope[ident]
        for who in ['a', 'b']:
            assert record['raw_reader_entries'][who] == raw[who][ident]
            assert record['raw_entry_canonical_sha256'][who] == entry_sha(raw[who][ident])
    for who in ['a', 'b']:
        assert grades['readers'][who]['scores'] == {'correct': len(packet['ids']), 'partial': 0, 'incorrect': 0}
        for grade in grades['readers'][who]['grades']:
            assert grade['id'] not in primary[who]
            primary[who][grade['id']] = grade
for who in ['a', 'b']:
    result = results['readers'][who]
    assert result['scores'] == {'correct': 67, 'partial': 0, 'incorrect': 0}
    assert result['required_fact_count'] == facts and result['unresolved_asked_facts'] == 0
    assert not result['unsupported_correct_guesses']
    assert result['raw_file_sha256'] == sha(it / f'reader-{who}.json')
    assert [g['id'] for g in result['grades']] == ids
    assert set(primary[who]) == set(ids)
    for grade in result['grades']:
        ident = grade['id']
        expected_grade = dict(primary[who][ident], raw_entry_canonical_sha256=entry_sha(raw[who][ident]))
        assert grade == expected_grade
        assert grade['grade'] == 'correct' and grade['reason']
        assert not grade['unsupported_correct_guess'] and not grade['extra_unsupported_claims']
        assert [f['fact_index'] for f in grade['facts']] == list(range(len(scope[ident]['required_answer_facts'])))
        assert all(f['assessment'] == 'satisfied' and f['reader_evidence'] and f['summary_support'] and f['reason'] for f in grade['facts'])
assert results['both_full_bank_pass'] and results['both_full_bank_semantic_pass']

audit_path = run / args.audit / 'source-audit.json'
audit = read(audit_path)
assert audit['verdict'] == 'PASS' and not audit['findings']
assert audit['summary_sha256'] == sha(snapshot)
assert Path(audit['summary_path']).read_bytes() == snapshot.read_bytes()
assert not audit['candidate_modified'] and not audit['canonical_modified']
hashes(audit['input_hashes'])
source_delivery = read(base / f'coordinator-checks/unmatched-{args.audit}-actual-delivery.json')
assert source_delivery['verified'] and source_delivery['audit_sha256'] == sha(audit_path)
assert source_delivery['expected_native_image_outputs'] >= 48
images = audit['image_receipts']
cell_count = (images['total_inspected_action_cells'] if isinstance(images, dict)
              else sum(len(x.get('cells', [])) for x in images))
assert len(audit['card_checks']) == 58 and cell_count == 120

coverage_path = run / 'current-v9-final-review/coverage-key-scope.json'
coverage = read(coverage_path)
assert coverage['verdict'] == 'PASS' and all(v == 'PASS' for v in coverage['verdicts'].values())
assert not any(coverage['findings'][x] for x in ['key_corrections', 'scope_corrections', 'source_corrections', 'coverage_additions', 'remaining_supported_procedural_gaps'])
assert [x['id'] for x in coverage['all_67_id_checks']] == ids
assert all(x['verdict'] == 'PASS' for x in coverage['all_67_id_checks'])
ledger = read(run / 'coverage-ledger-v9.json')
assert ledger['stopping_rule']['zero_addition_passes'] == [15, 16]
assert ledger['stopping_rule']['all_core_procedural_passages_mapped']

models = read(Path(args.runtime_proof))
assert models['verified'] and models['slug'] == 'unmatched' and models['game_chat_id'] == game['thread_id']
assert len([r for r in models['records'] if r['role'] == 'reader']) == 2
agents = read(run / 'model-provenance.json')['agents']
actors = {a['task']: a for a in agents}
reader_proofs = [x for x in read(run / 'actual-input-delivery-validation.json')['readers'] if x['iteration'] == args.iteration]
grader_proofs = read(it / 'grading/actual-input-delivery-validation.json')['graders']
review_proofs = read(run / 'actual-reviewer-input-delivery-validation.json')['reviewers']
selected_reviews = [x for x in review_proofs if x['task'].endswith('/current_v9_final_challenge') or x['task'].endswith('/current_source_audit_' + args.audit.rsplit('-', 1)[1])]
assert len(reader_proofs) == 2 and len(grader_proofs) == 4 and len(selected_reviews) == 2
adjudication_path = it / 'adjudication/q63-b-assessment.json'
if adjudication_path.exists():
    pack_path = it / 'adjudication/q63-b-inputs.json'
    pack, adjudication = read(pack_path), read(adjudication_path)
    assert set(pack) == {'summary_path', 'question', 'fixed_key', 'frozen_scope', 'reader', 'original_raw_file_sha256', 'raw_entry_canonical_sha256', 'raw_reader_entry'}
    assert pack['question'] == qmap['Q63'] and pack['fixed_key'] == key['Q63'] and pack['frozen_scope'] == scope['Q63']
    assert pack['reader'] == 'b' and pack['raw_reader_entry'] == raw['b']['Q63']
    assert pack['original_raw_file_sha256'] == adjudication['original_raw_file_sha256'] == sha(it / 'reader-b.json')
    assert pack['raw_entry_canonical_sha256'] == adjudication['raw_entry_canonical_sha256'] == entry_sha(raw['b']['Q63'])
    assert adjudication['input_hashes'] == {'summary_sha256': sha(snapshot), 'pack_sha256': sha(pack_path)}
    assert adjudication['grade'] == 'correct' and not adjudication['unsupported_correct_guess'] and not adjudication['extra_unsupported_claims']
    assert [f['fact_index'] for f in adjudication['facts']] == list(range(len(scope['Q63']['required_answer_facts'])))
    assert all(f['assessment'] == 'satisfied' and f['reason'] and f['reader_evidence'] and f['summary_support'] for f in adjudication['facts'])
    extra_reviews = [x for x in review_proofs if x['task'].endswith('/expanded11_whole_entry_adjudicator')]
    assert len(extra_reviews) == 1
    selected_reviews += extra_reviews

def strings(value, depth=0):
    if depth > 8:
        return
    if isinstance(value, str):
        yield value
        try:
            parsed = json.loads(value)
        except (ValueError, TypeError):
            return
        if parsed != value:
            yield from strings(parsed, depth + 1)
    elif isinstance(value, dict):
        for v in value.values():
            yield from strings(v, depth + 1)
    elif isinstance(value, list):
        for v in value:
            yield from strings(v, depth + 1)

deliveries = []
for proof in reader_proofs + grader_proofs + selected_reviews:
    actor = actors[proof['task']]
    runtime_path = Path(actor['runtime_source_path'])
    records = [json.loads(line) for line in runtime_path.open()]
    outputs, calls, write_cutoffs = [], {}, []
    is_reader = proof in reader_proofs
    is_grader = proof in grader_proofs
    for ordinal, record in enumerate(records):
        if not isinstance(record, dict) or record.get('type') != 'response_item':
            continue
        payload = record.get('payload')
        if not isinstance(payload, dict):
            continue
        typ = payload.get('type')
        if typ in ('custom_tool_call', 'function_call'):
            body = payload.get('input', payload.get('arguments', ''))
            calls[payload.get('call_id')] = ordinal
            if not isinstance(body, str):
                continue
            writing = ('write_text' in body or 'writeFile' in body or 'apply_patch' in body
                       or re.search(r"open\([^\n)]*,\s*['\"](?:w|a|x)", body))
            factual = is_reader or is_grader or (('source-audit.json' in body or 'coverage-key-scope.json' in body) and 'verdict' in body) or ('q63-b-assessment.json' in body and 'grade' in body)
            if writing and factual:
                write_cutoffs.append(ordinal)
        elif typ in ('custom_tool_call_output', 'function_call_output'):
            outputs.append((ordinal, payload.get('call_id'), list(strings(payload.get('output')))))
    assert write_cutoffs, actor['task']
    cutoff = min(write_cutoffs)
    receipts = proof.get('receipts', proof.get('verified_inputs', proof.get('verified_text_inputs')))
    receipts = list(receipts.values()) if isinstance(receipts, dict) else receipts
    verified_files = []
    for receipt in receipts:
        path = Path(receipt['path'])
        assert sha(path) == receipt['sha256']
        text = path.read_text()
        cursor = 0
        verified_slices = []
        for part in sorted(receipt['slices'], key=lambda x: x['start']):
            start, end = part['start'], part['end']
            # Repeated bounded reads are retained; coverage may overlap but cannot have gaps.
            assert 0 <= start <= cursor and start < end <= len(text)
            expected = text[start:end]
            matches = [(o, call) for o, call, values in outputs if o < cutoff and any(expected in v for v in values)]
            assert matches, (actor['task'], str(path), start, end, cutoff)
            assert any(call in calls and calls[call] < o for o, call in matches)
            verified_slices.append({'start': start, 'end': end, 'runtime_ordinals': [o for o, _ in matches]})
            cursor = max(cursor, end)
        assert cursor == len(text), (actor['task'], path)
        verified_files.append({'path': str(path), 'sha256': sha(path), 'characters': len(text), 'slices': verified_slices})
    deliveries.append({'actor_id': actor['identity'], 'task': actor['task'], 'runtime_path': str(runtime_path), 'runtime_sha256': sha(runtime_path), 'first_factual_write_ordinal': cutoff, 'all_inputs_delivered_before_first_factual_write': True, 'files': verified_files})

validation = read(run / 'validation.json')
assert validation['canonical_sha256'] == sha(snapshot) and validation['final_iteration'] == args.iteration
assert all(validation['gates'].values())
result = {'verified': True, 'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'checker_script_sha256': sha(Path(__file__)), 'slug': 'unmatched', 'iteration': args.iteration, 'summary_sha256': sha(snapshot), 'questions_per_reader': 67, 'required_facts_per_reader': facts, 'whole_raw_entries_preserved_and_every_fact_satisfied': True, 'historical_banks': historical_banks, 'source_audit': str(audit_path), 'source_audit_sha256': sha(audit_path), 'source_audit_verdict': 'PASS', 'coverage_review': str(coverage_path), 'runtime_model_proof': str(Path(args.runtime_proof)), 'actual_pre_answer_pre_grade_pre_audit_delivery': deliveries, 'checked_hash_paths': sorted(checked), 'technical_deviations': validation.get('technical_delivery_deviations'), 'limits': validation['limitations']}
target = base / 'coordinator-checks' / ('unmatched-' + args.iteration + '-acceptance.json')
target.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'verified': True, 'proof': str(target), 'questions': 67, 'facts': 2*facts, 'actors_with_actual_prewrite_delivery': len(deliveries)}))
