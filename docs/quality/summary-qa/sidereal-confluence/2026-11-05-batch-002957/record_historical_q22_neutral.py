"""Record the one authorized neutral decision without overwriting primary history."""
from pathlib import Path
import copy
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'historical-full5-q22-neutral-01'
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):
    return json.loads(p.read_text())
def bind(p):
    return {'path': str(p), 'sha256': sha(p)}
def write(name, value):
    p = OUT / name
    assert not p.exists(), p
    p.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')

packet = read(OUT / 'neutral-input-packet.json')
report = read(OUT / 'adjudication.json')
manifest = read(OUT / 'input-manifest.json')
primary_path = ROOT / 'full-iteration-05/results.json'
primary = read(primary_path)
primary_hash = sha(primary_path)
canonical = ROOT.parents[4] / 'rules/sidereal-confluence.md'
assert sha(canonical) == 'eb091e5288b379afe914cb89f64d9590c6c9242f05e0843d34cd347311fe348f'
assert report['packet_sha256'] == sha(OUT / 'neutral-input-packet.json') == manifest['neutral_packet_sha256']
assert sha(Path(report['packet_path'])) == report['packet_sha256']
assert sha(Path(report['frozen_summary_path'])) == report['frozen_summary_sha256'] == packet['summary_sha256']
assert report['key_or_scope_correction_needed'] is True
assert read(OUT / 'runtime-text-delivery.json')['validation'] == 'PASS'
assert read(OUT / 'runtime-native-delivery.json')['validation'] == 'PASS'
assert read(OUT / 'runtime-native-delivery.json')['native_view_count'] == 4
assert read(OUT / 'runtime-text-delivery.json')['report_sha256'] == sha(OUT / 'adjudication.json')
assert read(OUT / 'runtime-native-delivery.json')['report_sha256'] == sha(OUT / 'adjudication.json')
for source in manifest['original_authorities']:
    assert sha(Path(source['path'])) == source['sha256']

scope_path = ROOT / 'full-iteration-05/asked-facts.json'
scope = read(scope_path)
q = next(q for q in scope['questions'] if q['id'] == 'Q22')
assert q == packet['asked_fact_map']
effective_q = copy.deepcopy(q)
facts = {f['id']: f for f in effective_q['required_facts']}
facts['Q22.F01']['fact'] = 'Select the complete six-player colony-track configuration because Kjas counts twice only there; six spots is an equivalent explanatory description.'
facts['Q22.F02']['fact'] = 'Select the complete five-player research-track configuration and six Confluence cards appropriate to the actual five players; five research spots is an equivalent explanatory description.'
scope_correction = {
    'version': 'historical-full5-q22-effective-scope-v1',
    'type': 'Source-correct selection-label equivalence; no separate printed-space tally omission gate',
    'decision': bind(OUT / 'adjudication.json'),
    'primary_scope_file': bind(scope_path),
    'primary_Q22': q,
    'effective_Q22': effective_q,
    'literal_question_unchanged': True,
    'required_fact_ids_and_count_unchanged': True,
    'fixed_answer_key_unchanged': True,
    'source_rules_unchanged': True,
    'basis': report['key_or_scope_correction'],
    'application': 'Historical full05 effective accounting only. All frozen banks, primary grades, keys, raw outputs and the selected full09 grades remain unchanged. This version records the genuine interpretive correction rather than silently editing a frozen bank. Any future use of Q22 should attach this explicit interpretation or prospectively ask for bid-space counts if intended.',
    'no_scope_resampling_or_additional_neutral_decision': True,
}
write('scope-correction-v1.json', scope_correction)
effective = copy.deepcopy(primary)
effective['primary_results'] = bind(primary_path)
effective['effective_adjudication'] = bind(OUT / 'adjudication.json')
effective['effective_scope'] = bind(OUT / 'scope-correction-v1.json')
effective['effective_version'] = 'historical-full5-q22-neutral-v1'
for side, rows in effective['readers'].items():
    original = read(ROOT / f'full-iteration-05/reader-{side}.json')
    entry = next(e for e in original['answers'] if e['id'] == 'Q22')
    assert entry == packet['complete_original_entries'][side]
    row = next(r for r in rows if r['id'] == 'Q22')
    assert row['grade'] == 'partial'
    neutral = report['independent_grades'][side]
    assert neutral['grade'] == 'Correct'
    assert len(neutral['per_asked_fact']) == 5
    assert all(f['grade'] == 'Correct' for f in neutral['per_asked_fact'])
    row['primary_grade'] = row['grade']
    row['grade'] = 'correct'
    row['effective_grade_record'] = neutral
    row['effective_grade_authority'] = bind(OUT / 'adjudication.json')
    row['original_grade_record_preserved'] = True
effective['reader_scores'] = {s: {g: Counter(r['grade'] for r in rows)[g] for g in ['correct','partial','incorrect']} for s, rows in effective['readers'].items()}
effective['totals'] = {g: sum(v[g] for v in effective['reader_scores'].values()) for g in ['correct','partial','incorrect']}
effective['PASS'] = all(v['correct'] == 86 for v in effective['reader_scores'].values())
assert effective['reader_scores'] == {'a': {'correct':86,'partial':0,'incorrect':0}, 'b': {'correct':85,'partial':0,'incorrect':1}}
assert effective['PASS'] is False
for side in ['a','b']:
    for before, after in zip(primary['readers'][side], effective['readers'][side]):
        if before['id'] != 'Q22':
            assert before == after
        else:
            assert before['original_grade_record'] == after['original_grade_record']
write('effective-results-v1.json', effective)
assert sha(primary_path) == primary_hash
validation = {
    'status': 'ONE_NEUTRAL_HISTORICAL_SCOPE_AND_WHOLE_ENTRY_DECISION_PASS',
    'created_at_utc': datetime.now(timezone.utc).isoformat(),
    'canonical_sha256_unchanged': sha(canonical),
    'clean_packet': bind(OUT / 'neutral-input-packet.json'),
    'neutral_report': bind(OUT / 'adjudication.json'),
    'actual_text_delivery': bind(OUT / 'runtime-text-delivery.json'),
    'actual_native_delivery': bind(OUT / 'runtime-native-delivery.json'),
    'text_files': 3, 'bounded_text_slices': 14, 'native_views': 4,
    'primary_results_unchanged': bind(primary_path),
    'scope_correction': bind(OUT / 'scope-correction-v1.json'),
    'effective_results': bind(OUT / 'effective-results-v1.json'),
    'primary_scores': primary['reader_scores'],
    'effective_scores': effective['reader_scores'],
    'historical_pair_still_fails': True,
    'remaining_historical_failure': 'Reader b Q63; unchanged primary Incorrect/unsupported-guess assessment',
    'selected_final_pair': 'full09 a/b, unchanged 86/86 each; no cross-round substitution',
    'all_primary_raw_key_grade_and_frozen_bank_files_preserved': True,
    'only_Q22_effective_decisions_changed': True,
    'unsupported_guessing_in_neutral_Q22': False,
    'only_one_fresh_neutral_decision': True,
    'final_coordinator_signoff_and_completion_authorization': 'PENDING',
}
write('validation.json', validation)
print(json.dumps({'status':validation['status'],'effective_scores':effective['reader_scores'],'canonical_sha256':sha(canonical)}))
