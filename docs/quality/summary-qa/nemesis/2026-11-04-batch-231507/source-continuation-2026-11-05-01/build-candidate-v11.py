"""One-shot, append-only evidence construction after the 119-question challenge."""
import copy
import datetime
import difflib
import hashlib
import json
from pathlib import Path

R = Path(__file__).resolve().parent
ROOT = R.parents[5]
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()

def read(name):
    return json.loads((R / name).read_text())

def write(name, obj):
    p = R / name
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('x') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write('\n')

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

review = read('coverage119-independent-final.json')
q = read('benchmark-v10/questions.json')
k = read('benchmark-v10/answer-key.json')
oldq, oldk = copy.deepcopy(q), copy.deepcopy(k)
q['benchmark_version'] = k['benchmark_version'] = 'benchmark-v11'
for x in k['answers']:
    if x['id'] == 'Q117':
        x['expected_answer'] = review['corrections'][0]['corrected_expected_answer']
        x['source_references'] = review['corrections'][0]['sources']
for x in review['accepted_additions']:
    q['questions'].append({'id': x['proposed_id'], 'question': x['question']})
    k['answers'].append({'id': x['proposed_id'], 'expected_answer': x['expected_answer'],
                         'source_references': x['sources'], 'topic': x['topic']})
assert q['questions'][:119] == oldq['questions']
assert len(q['questions']) == 122
assert len({x['id'] for x in q['questions']}) == 122
assert 'Q109' not in {x['id'] for x in q['questions']}
write('benchmark-v11/questions.json', q)
write('benchmark-v11/answer-key.json', k)
write('benchmark-v11/draft-status.json', {'created_utc': NOW, 'candidate': True,
      'final_readers_dispatched': False, 'coverage_closure_pending': True,
      'based_on': 'coverage119-independent-final.json', 'question_count': 122})
bank = '# Nemesis — benchmark-v11 candidate\n\n' + q['scope'] + '\n\n'
bank += '\n\n'.join('**' + x['id'] + '.** ' + x['question'] for x in q['questions']) + '\n'
with (R/'benchmark-v11/question-bank.md').open('x') as f:
    f.write(bank)
write('benchmark-v11-changes.json', {'created_utc': NOW,
      'prior_benchmark': 'benchmark-v10', 'question_count_before': 119, 'question_count_after': 122,
      'all_existing119_question_objects_unchanged': True, 'original108_unchanged': True,
      'changed_existing_key_ids': ['Q117'], 'key_correction': review['corrections'][0],
      'accepted_additions': review['accepted_additions'], 'retired_id': 'Q109',
      'request_scope': 'Source-backed key context does not become a requirement when unasked by a stem.'})
rubric = read('grading-rubric-v10.json')
rubric['benchmark_version'] = 'benchmark-v11'
rubric['fixed_before_v11_readers'] = NOW
write('grading-rubric-v11.json', rubric)
src = read('source-version-04.json')
src.update({'version': 'source-version-05-english-illustrations-corrected', 'created_utc': NOW,
            'prior_source_version': 'source-version-04.json',
            'new_source_bytes': False,
            'accepted_primary_corrections': ['Energy Charge has no Combat restriction icon',
               'Remove unsupported occupied-Pod qualifier on Evacuation Key',
               'Remove unsupported Chemicals reload cross-reference',
               'Include English p13 readable card effects and p19 Scientist Pistol exception'],
            'coverage_limit': 'Selected examples, not a complete original card corpus. Unreadable Grenade/component-card clauses deferred to actual cards.',
            'independent_reviews': ['coverage119-independent-final.json', 'source-candidate-08/source-audit.json']})
write('source-version-05.json', src)
before = (R/'source-candidate-08/summary-snapshot.md').read_text()
current = (ROOT/'rules/nemesis.md').read_text()
with (R/'summary-coverage119-repairs.patch').open('x') as f:
    f.write(''.join(difflib.unified_diff(before.splitlines(True), current.splitlines(True),
                                       fromfile='source-candidate-08/summary-snapshot.md', tofile='rules/nemesis.md')))
candidate = R/'source-candidate-09'
candidate.mkdir()
(candidate/'summary-snapshot.md').write_text(current)
m = read('source-candidate-08/input-manifest.json')
m['summary_file'] = str(candidate/'summary-snapshot.md')
m['summary_sha256'] = sha(candidate/'summary-snapshot.md')
write('source-candidate-09/input-manifest.json', m)
write('source-candidate-09/repair-record.json', {'created_utc': NOW,
      'prior_candidate': 'source-candidate-08', 'prior_sha256': sha(R/'source-candidate-08/summary-snapshot.md'),
      'sha256': m['summary_sha256'], 'prior_findings_addressed': ['F01', 'F02', 'F03', 'C01', 'C02'],
      'C01': 'Added readable p13 effects and explicitly selected-example scope; not a complete card catalog.',
      'C02': 'Explicit actual-card lookup limitation; no complete Grenade rule inferred from tiny source image.'})
print(json.dumps({'questions': len(q['questions']), 'canonical_sha256': m['summary_sha256'],
                  'existing_question_objects_preserved': True}))
