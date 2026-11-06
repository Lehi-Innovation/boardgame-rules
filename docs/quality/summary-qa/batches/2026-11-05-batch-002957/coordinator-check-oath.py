"""Independently check Oath's exact candidate, complete grading and provenance."""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from collections import Counter
import argparse
import copy
import hashlib
import json
import re
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--iteration', required=True)
parser.add_argument('--runtime-proof', required=True)
parser.add_argument('--phase', choices=['pre-stamp', 'complete'], required=True)
parser.add_argument('--auditor-task')
args = parser.parse_args()
base = Path(__file__).resolve().parent
repo = base.parents[4]
run = repo / 'docs/quality/summary-qa/oath-chronicles-of-empire-and-exile' / base.name
iteration = run / args.iteration
assert iteration.parent == run
tag = f"{int(iteration.name.rsplit('-', 1)[1]):02d}"
read = lambda p: json.loads(p.read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
checked_hashes = []

def path_of(value):
    p = Path(value)
    return p if p.is_absolute() else repo / p

def check_hashes(values):
    if isinstance(values, list):
        converted = {v['path']: v['sha256'] for v in values}
        assert len(converted) == len(values)
        values = converted
    for name, expected in values.items():
        expected = expected['sha256'] if isinstance(expected, dict) else expected
        assert sha(path_of(name)) == expected, name
        checked_hashes.append(str(path_of(name)))

manifest = read(base / 'manifest.json')
game = next(x for x in manifest['games'] if x['slug'] == 'oath-chronicles-of-empire-and-exile')
frozen = read(iteration / 'input-manifest.json')
check_hashes(frozen['hashes'])
bank = run / frozen['benchmark_version']
questions = read(iteration / 'questions.json')['questions']
assert questions == read(bank / 'questions.json')['questions']
ids = [q['id'] for q in questions]
n = len(ids)
assert n >= 20 and len(set(ids)) == n
assert questions[:20] == read(run / 'seed-v1/questions.json')['questions']
qmap = {q['id']: q for q in questions}
key_entries = read(bank / 'answer-key.json')['answers']
assert [k['id'] for k in key_entries] == ids
key = {k['id']: k for k in key_entries}
previous = None
for history_bank in [run / 'seed-v1'] + sorted(run.glob('expanded-v*'), key=lambda p: int(p.name.rsplit('v', 1)[1])):
    if not (history_bank / 'questions.json').exists():
        continue
    old_questions = read(history_bank / 'questions.json')['questions']
    if previous is not None:
        assert old_questions[:len(previous)] == previous
    previous = old_questions
    for filename, expected in read(history_bank / 'input-manifest.json').items():
        assert sha(history_bank / filename) == expected
        checked_hashes.append(str(history_bank / filename))

canonical = Path(game['summary_path'])
snapshot = iteration / 'summary-snapshot.md'
assert canonical.read_bytes() == snapshot.read_bytes()
summary = snapshot.read_text()
scope_path = run / 'grading-scope-v12/grading-scope.json'
scope = {q['id']: q for q in read(scope_path)['questions']}
assert list(scope) == ids
check_hashes(read(run / 'grading-scope-v12/freeze-manifest.json')['files'])
facts_per_reader = sum(len(scope[i]['required_facts']) for i in ids)
raw = {}
for who in ['reader-a', 'reader-b']:
    document = read(iteration / (who + '.json'))
    entries = document['answers']
    assert Counter(e['id'] for e in entries) == Counter(ids)
    raw[who] = {e['id']: e for e in entries}
    declared = document['inputs']
    if isinstance(declared, dict):
        declared = list(declared.values())
    assert {str(path_of(v['path']).resolve()) for v in declared} == {str(snapshot.resolve()), str((iteration / 'questions.json').resolve())}
    check_hashes(declared)
    assert all(e.get('support', e.get('support_label')) == 'supported' for e in entries)
    fmt = read(iteration / (who + '.section-format-validation.json'))
    assert fmt['status'] == 'PASS' and not fmt['errors'] and fmt['raw_sha256'] == sha(iteration / (who + '.json'))

def unpack_block(packet):
    pool = packet['shared_values']
    def expand(value):
        if isinstance(value, dict) and set(value) == {'$ref'}:
            assert isinstance(value['$ref'], int) and 0 <= value['$ref'] < len(pool)
            return copy.deepcopy(pool[value['$ref']])
        if isinstance(value, dict):
            return {k: expand(v) for k, v in value.items()}
        if isinstance(value, list):
            return [expand(v) for v in value]
        return value
    return expand({k: v for k, v in packet.items() if k != 'shared_values'})

def restore_entry(entry, table):
    restored = copy.deepcopy(entry)
    for encoded, original in [('attached_verbatim_passage_spans_ids', 'verbatim_passages'), ('answer_quotation_spans_ids', 'answer_quotations')]:
        quotes = []
        for index in restored.pop(encoded):
            start, end, kind, metadata = table[index]
            assert 0 <= start <= end <= len(summary)
            text = summary[start:end]
            if kind == 'object':
                value = copy.deepcopy(metadata)
                field = value.pop('__transport_text_field__', 'text')
                value[field] = text
            else:
                assert kind == 'string'
                value = text
            quotes.append(value)
        restored[original] = quotes
    if 'answer_transport' in restored:
        transport = restored.pop('answer_transport')
        assert transport['mode'] == 'join_answer_quotations'
        restored['answer'] = transport['separator'].join(v.get('text', v.get('verbatim')) if isinstance(v, dict) else v for v in restored['answer_quotations'])
    return restored

block_manifest = read(iteration / 'grading-block-manifest.json')
assert block_manifest['summary_sha256'] == sha(snapshot)
assert [i for b in block_manifest['blocks'] for i in b['question_ids']] == ids
assert sum(b['required_fact_groups_per_reader'] for b in block_manifest['blocks']) == facts_per_reader
check_hashes(block_manifest['original_input_hashes'])
primary_grades = {'reader-a': {}, 'reader-b': {}}
grading_tasks = []
for block in block_manifest['blocks']:
    directory = Path(block['directory'])
    packet_path = Path(block['packet_path'])
    assert sha(packet_path) == block['packet_sha256']
    checked_hashes.append(str(packet_path))
    packet = unpack_block(read(packet_path))
    assert [q['id'] for q in packet['questions']] == block['question_ids']
    check_hashes(packet['inputs'])
    for question in packet['questions']:
        ident = question['id']
        assert question['question'] == qmap[ident]['question']
        assert question['fixed_expected_answer'] == key[ident]['expected_answer']
        expected_facts = [{'fact_id': f['fact_id'], 'expected_fact': f['expected_fact']} for f in scope[ident]['required_facts']]
        assert question['required_facts'] == expected_facts
        for who, entry in question['readers'].items():
            assert restore_entry(entry, packet['quote_span_table']) == raw[who][ident]
    graded = read(directory / 'results.json')
    for reader in graded['readers']:
        who = reader['reader']
        for grade in reader['questions']:
            assert grade['id'] not in primary_grades[who]
            primary_grades[who][grade['id']] = grade
    validation = read(directory / 'grading-validation.json')
    assert validation['status'] in ['PASS', 'passed', 'complete'] and not validation.get('errors')
    grading_tasks.append(block['agent_name'])

results = read(iteration / 'results.json')
check_hashes(results['inputhashes'])
assert results['questions_graded'] == 2 * n and results['fact_assessments'] == 2 * facts_per_reader
assert not results.get('gold_or_scope_defects')
scores = {}
assert {r['reader'] for r in results['readers']} == {'reader-a', 'reader-b'}
for reader in results['readers']:
    who = reader['reader']
    grades = reader['questions']
    assert Counter(g['id'] for g in grades) == Counter(ids)
    assert set(primary_grades[who]) == set(ids)
    assert reader['totals'] == {'correct': n, 'partial': 0, 'incorrect': 0}
    for grade in grades:
        ident = grade['id']
        assert grade == primary_grades[who][ident]
        assert grade['grade'] == 'correct'
        assert grade['question'] == qmap[ident]['question']
        assert grade['expected_answer_from_fixed_key'] == key[ident]['expected_answer']
        assert grade['observed_answer'] == raw[who][ident]['answer']
        actual = grade['fact_checks']
        expected = scope[ident]['required_facts']
        assert [(f['fact_id'], f['expected_fact']) for f in actual] == [(f['fact_id'], f['expected_fact']) for f in expected]
        assert all(f['status'] == 'satisfied' and f['evidence'] for f in actual)
    scores[who] = {'correct': n, 'partial': 0, 'incorrect': 0, 'unresolved': 0, 'unsupported_guesses': 0}

audit_path = iteration / 'source-audit.json'
audit = read(audit_path)
assert audit['status'] == 'PASS' and not audit['findings']
assert audit['candidate']['sha256'] == sha(snapshot)
audit_sources = audit.get('sources', audit.get('sourcehashes'))
if audit_sources is None:
    receipts = audit['text_read_receipts']
    native = audit['native_pdf_inspection']
    assert receipts['all_characters_read_into_actual_model_visible_output']
    assert not receipts['truncated_chunks']
    assert all(f['complete_contiguous_model_visible_read'] for f in receipts['files'])
    assert native['all_applicable_pages_inspected']
    assert audit['input_discipline']['only_permitted_content_inputs_used']
    assert not audit['input_discipline']['prohibited_inputs_used']
    audit_sources = receipts['files'] + native['sources']
check_hashes(audit_sources)
source_representation = json.dumps(audit_sources)
for source in game['source_paths']:
    assert sha(Path(source)) in source_representation
models = read(Path(args.runtime_proof))
assert models['verified'] and models['slug'] == game['slug'] and models['game_chat_id'] == game['thread_id']
records = models['records']
readers = [r for r in records if r['role'] == 'reader']
auditors = [r for r in records if r['role'] == 'source-auditor']
assert len(readers) == 2 and len(auditors) == 1
reader_ids = {r['session_id'] for r in readers}
assert len(reader_ids) == 2
auditor_task = args.auditor_task or 'final_source_auditor_' + tag
assert auditors[0]['identity']['agent_path'].endswith('/' + auditor_task)
actor_tasks = [r['identity']['agent_path'].rsplit('/', 1)[1] for r in records]
required_tasks = ['expanded' + tag + '_reader_a', 'expanded' + tag + '_reader_b', auditor_task, 'coverage_challenge_10', 'scope_adjudicator_09'] + grading_tasks
assert set(required_tasks).issubset(actor_tasks)
for task in required_tasks:
    proof = read(run / 'delivery-audit' / (task + '.verified-delivery.json'))
    assert proof['status'] == 'PASS'

coverage = read(run / 'coverage-review-10.json')
assert coverage['verdict'] == 'PASS_WORKING_SATURATION' and not coverage['material_gaps'] and not coverage['new_questions_required']
coverage_delivery = read(run / 'delivery-audit/coverage_challenge_10.verified-delivery.json')
reviewed_inputs = coverage_delivery['coverage']
assert coverage_delivery['status'] == 'PASS' and all(v['complete'] and not v['gaps'] for v in reviewed_inputs)
check_hashes(reviewed_inputs)
reviewed_hashes = {str(path_of(v['path']).resolve()): v['sha256'] for v in reviewed_inputs}
assert reviewed_hashes[str((bank / 'questions.json').resolve())] == sha(bank / 'questions.json')
assert reviewed_hashes[str((bank / 'answer-key.json').resolve())] == sha(bank / 'answer-key.json')
assert coverage['q104_novelty_adjudication']['novelty_credit'] == 0
assert coverage['historical_overlap_credit']['novelty_credit_each'] == 0
ledger = read(run / 'coverage-ledger.json')
assert len(ledger['passes']) >= 2 and all(p['count'] == 0 for p in ledger['passes'][-2:])
assert ledger['stopping_rule']['consecutive_zero_addition_passes'] >= 2
assert ledger['stopping_rule']['all_core_procedural_passages_mapped']
assert all(set(re.findall(r'Q\d{3}', json.dumps(v))) & set(ids) for v in ledger['coverage_map'].values())
certificate = read(run / 'final-certificate.json')
assert certificate['status'] == 'READY_FOR_COORDINATOR' and certificate['summary_sha256'] == sha(snapshot)
assert all(v['pass'] for v in certificate['gates'].values())
integrity = read(run / 'validation-in-progress.json')
assert integrity['status'] == 'PASS' and not integrity['errors']
sys.path.insert(0, str(repo))
from scripts.validate import validate_rules_file
assert not validate_rules_file(str(canonical))

approval_path = base / 'coordinator-approvals.json'
before = approval_path.read_text()
approvals = json.loads(before)
prior = approvals.get(game['slug'])
if args.phase == 'complete' and prior:
    if prior['summary_sha256'] != sha(snapshot):
        assert not reader_ids.intersection(prior['reader_session_ids'])
    assert auditors[0]['session_id'] != prior['source_auditor_session_id']
now = datetime.now(ZoneInfo('America/Phoenix'))
report = {'game': game['game'], 'checked_at': now.isoformat(), 'approved': True, 'phase': args.phase, 'question_count': n,
          'final_reader_scores': scores, 'summary_sha256': sha(snapshot), 'final_snapshot_path': str(snapshot),
          'source_audit_verdict': 'PASS', 'source_audit_path': str(audit_path), 'reader_session_ids': sorted(reader_ids),
          'source_auditor_session_id': auditors[0]['session_id'], 'independent_runtime_proof': args.runtime_proof,
          'complete_lossless_original_entries_checked': 2 * n, 'required_fact_assessments_checked': 2 * facts_per_reader,
          'primary_block_grades_equal_aggregate': True, 'all_requested_facts_supported_with_evidence': True,
          'original_twenty_and_historical_question_prefixes_retained': True, 'frozen_hash_checks': len(checked_hashes),
          'coverage_working_saturation_checked': True, 'Q104_novelty_credit': 0, 'canonical_equals_tested_and_audited_bytes': True,
          'publication_gate': 'Coordinator audit recording, stamp and targeted catalog publication remain. Changed stamp bytes require a new full pair and fresh source auditor.'}
target = base / 'coordinator-checks' / ('oath-' + args.phase + '-' + now.strftime('%Y%m%dT%H%M%S%f') + '.json')
target.write_text(json.dumps(report, indent=2) + '\n')
report['coordinator_validation_path'] = str(target)
approvals[game['slug']] = report
assert approval_path.read_text() == before
approval_path.write_text(json.dumps(approvals, indent=2) + '\n')
print(json.dumps({'approved': True, 'phase': args.phase, 'question_count': n, 'summary_sha256': sha(snapshot), 'report': str(target)}))
