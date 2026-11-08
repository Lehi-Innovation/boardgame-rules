"""Prepare a fixed current-bank test only after explicit pre-reader gates.

This neither launches readers nor declares complete-source/final readiness.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil

R = Path(__file__).parent.resolve()
WORK = R.parents[4]


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


decision_path = R / 'pre-reader-gate-decision-01.json'
decision = read(decision_path)
assert decision['may_dispatch_full_current_bank'] is True
assert decision['pending_dependent_source_choices'] == []
assert decision['independent_actual_scope_validated'] is True
scope_path = Path(decision['scope_map_path'])
assert scope_path.is_relative_to(R)
assert sha(scope_path) == decision['scope_map_sha256']
assert read(Path(decision['scope_delivery_validation_path']))['pass'] is True
assert decision['current_source_strata_reviewed'] is True
assert decision['final_scope_readiness_claimed'] is False

bank = (R / decision['bank_version']).resolve()
snapshot = Path(decision['snapshot_path']).resolve()
assert bank.is_relative_to(R) and snapshot.is_relative_to(R)
assert snapshot.read_bytes() == (WORK / 'rules/cosmic-encounter.md').read_bytes()
assert sha(snapshot) == decision['snapshot_sha256']
questions = read(bank / 'questions.json')['questions']
key = read(bank / 'answer-key.json')['answers']
scope = read(scope_path)['questions']
ids = [q['id'] for q in questions]
count = len(ids)
fact_count = sum(len(a['required_facts']) for a in key)
assert count == len(set(ids)) == decision['question_count']
assert count >= len(read(R / 'seed-v1/questions.json')['questions'])
assert [a['id'] for a in key] == ids
assert {q['id'] for q in scope} == set(ids) and len(scope) == count
assert fact_count == decision['raw_key_fact_count']
assert questions[:20] == read(R / 'seed-v1/questions.json')['questions']
assert key[:20] == read(R / 'seed-v1/answer-key.json')['answers']

it = R / 'expanded-iteration-01'
assert not it.exists(), 'Never replace any frozen iteration'
it.mkdir()
for source, name in [
    (snapshot, 'summary-snapshot.md'),
    (bank / 'questions.json', 'questions.json'),
    (bank / 'answer-key.json', 'answer-key.json'),
    (scope_path, 'actual-question-scope.json'),
    (decision_path, 'pre-reader-gate-decision.json'),
]:
    shutil.copyfile(source, it / name)

template = (R / 'full-bank-reader-protocol-template-v2.txt').read_text()
for letter in ['a', 'b']:
    prompt = (template.replace('SUMMARY_PATH', str(it / 'summary-snapshot.md'))
              .replace('QUESTIONS_PATH', str(it / 'questions.json'))
              .replace('OUTPUT_PATH', str(it / f'reader-{letter}.json')))
    (it / f'reader-{letter}-prompt.txt').write_text(prompt)
assert ((it / 'reader-a-prompt.txt').read_text().replace(str(it / 'reader-a.json'), 'OUTPUT_PATH')
        == (it / 'reader-b-prompt.txt').read_text().replace(str(it / 'reader-b.json'), 'OUTPUT_PATH'))
frozen = [p for p in it.iterdir() if p.is_file()]
manifest = {
    'created_at_utc': datetime.now(timezone.utc).isoformat(),
    'purpose': 'Preliminary complete current-bank source-resolvable regression; final authority scope remains pending.',
    'full_bank_freeze_authorized': True,
    'freeze_authorization_scope': 'Every question in the unchanged frozen current bank; no final complete-source readiness claim.',
    'independent_actual_scope_validated': True,
    'pending_dependent_source_choices': [],
    'unresolved_global_authority_topics': decision['unresolved_global_authority_topics'],
    'final_scope_freeze': False,
    'completion_readiness': False,
    'question_count': count,
    'raw_key_fact_count': fact_count,
    'bank_version': bank.name,
    'expected_ids': ids,
    'original_twenty_preserved_verbatim': True,
    'reader_protocol_version': 2,
    'reader_models': 'gpt-6-luna/high, two NEW fork_turns:none identities',
    'sha256': {str(p): sha(p) for p in frozen},
    'no_reader_dispatched_by_this_script': True,
}
(it / 'input-manifest.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')
print('Frozen preliminary current bank:', count, 'questions;', fact_count,
      'raw records. No readers dispatched or final readiness claimed.')
