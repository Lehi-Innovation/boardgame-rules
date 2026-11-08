"""Targeted read-only checks; writes only this continuation's evidence."""
from evidence import *
import collections
import re

def validate(pair='iteration-01'):
    directory = N / pair
    checks = []
    def check(label, condition, detail=None):
        checks.append({'check': label, 'passed': bool(condition), 'detail': detail})
    manifest = json.loads((N / 'input-manifest.json').read_text())
    for path, expected in manifest['hashes'].items():
        check('Original frozen binding: ' + path, Path(path).is_file() and sha(path) == expected)
    canonical = ROOT / 'rules/root.md'
    check('Canonical equals frozen current candidate', canonical.read_bytes() == (directory / 'summary-snapshot.md').read_bytes())
    check('Current candidate is requested exact SHA', sha(canonical) == 'da0b6b08fda1d3e1775a8ef813e31535ac35375399b061efe255690d09ad1aeb')
    old = R / 'expanded-iteration-17/summary-snapshot.md'
    check('Only accepted old-date-to-current-date metadata differs', canonical.read_text().replace('extracted_date: "2026-11-06"', 'extracted_date: "2026-11-05"') == old.read_text())
    check('Tested verification date remains November5', 'verification_date: "2026-11-05"' in canonical.read_text())
    guide = canonical.read_text()
    for field in ['title', 'bgg_id', 'player_count', 'play_time', 'designer', 'source_pdf', 'extracted_date', 'summarized_date', 'rulebook_version', 'verification', 'verification_date']:
        check('Required frontmatter field ' + field, bool(re.search(r'^' + field + ': .+', guide, re.M)))
    for heading in ['Overview', 'Components', 'Setup', 'Turn Structure', 'Actions', 'Scoring / Victory Conditions', 'Special Rules & Edge Cases', 'Player Reference']:
        check('Required section ' + heading, '\n## ' + heading + '\n' in guide)
    history = json.loads((N / 'preserved-historical-pairs.json').read_text())
    check('All22 old scored pairs retained', history['scored_pairs'] == len(history['pairs']) == 22)
    for item in history['pairs']:
        for path, expected in item['files'].items():
            check('Historical artifact unchanged: ' + path, Path(path).is_file() and sha(path) == expected)
    q = json.loads((directory / 'questions.json').read_text())['questions']
    k = json.loads((directory / 'answer-key.json').read_text())['answers']
    ids = [x['id'] for x in q]
    check('Exactly81 unique question IDs', len(ids) == len(set(ids)) == 81)
    check('Key IDs match question IDs', [x['id'] for x in k] == ids)
    for filename in ('questions.json', 'answer-key.json'):
        check('Unchanged expanded-v10 ' + filename, (directory / filename).read_bytes() == (R / 'benchmark-v10' / filename).read_bytes())
    initial = json.loads((R / 'benchmark-v1/questions.json').read_text())['questions']
    check('All original20 question IDs/wording retained', q[:20] == initial[:20])
    originals = json.loads((directory / 'raw-output-manifest.json').read_text())
    results = json.loads((directory / 'results.json').read_text())
    for side in 'ab':
        path = directory / f'reader-{side}.json'
        raw = json.loads(path.read_text())
        check('Reader' + side + ' full original bytes unchanged after freeze', sha(path) == originals['readers'][side]['sha256'])
        check('Reader' + side + ' all81 exact once/in-order', [x['id'] for x in raw['answers']] == ids)
        for cp in (directory / 'checkpoints').glob(f'reader-{side}-*.json'):
            prior = json.loads(cp.read_text())['answers']
            if len(prior) % 10 == 0 or len(prior) == 81:
                check('Completed-turn prefix unchanged: ' + cp.name, raw['answers'][:len(prior)] == prior)
        records = results['readers'][side]['grades']
        check('Reader' + side + ' all81 grades exact once', [x['id'] for x in records] == ids)
        counts = collections.Counter(g['grade'] for g in records)
        check('Reader' + side + ' totals equal per-entry grades', all(results['readers'][side]['totals'][g] == counts[g] for g in ('correct', 'partial', 'incorrect')))
        for question, key, entry, record in zip(q, k, raw['answers'], records):
            check('Grade exact question/key/original entry: ' + side + entry['id'], record['question'] == question and record['expected'] == key and record['observed_original_entry'] == entry and record['observed_entry_sha256'] == hashlib.sha256(js(entry).encode()).hexdigest())
            check('All substantive fields reviewed: ' + side + entry['id'], record['every_substantive_field_reviewed'] and record['whole_entry_policy'])
            for index, passage in enumerate(entry['source_passages']):
                check('Nonempty verbatim quotation: ' + side + entry['id'] + '/' + str(index), bool(passage['quotation']) and passage['quotation'] in guide)
    audit = N / 'source-only-audit/source-audit.json'
    report = json.loads(audit.read_text())
    check('New independent source-only audit PASS/no findings', report['verdict'] == 'PASS' and report['findings'] == [])
    check('New source audit binds exact current candidate', report['input_hashes'][str((N / 'iteration-01/summary-snapshot.md').resolve())]['sha256'] == sha(canonical))
    delivery = N / 'source-delivery-serialized-metadata/source-delivery-audit.json'
    proof = json.loads(delivery.read_text())
    check('Actual complete source/text/native-image delivery proof PASS', proof['status'] == 'PASS')
    check('Source proof binds original audit bytes', proof['completed_source_audit']['sha256'] == sha(audit))
    check('Source proof every raw actual pair intact', all(sha(x['raw_path']) == x['raw_sha256'] for x in proof['read_calls']))
    status = 'PASS' if all(x['passed'] for x in checks) else 'FAIL'
    result = {'status': status, 'checks_passed': sum(x['passed'] for x in checks), 'checks_total': len(checks), 'checks': checks, 'scope': 'Targeted current Root input/history/grade/delivery integrity; regression success separately equals both81/0/0. Does not run shared/global scripts, stamp, record or publish.'}
    save(directory / 'validation.json', result)
    print(json.dumps({'status': status, 'passed': result['checks_passed'], 'total': len(checks), 'failures': [x for x in checks if not x['passed']]}))

if __name__ == '__main__':
    validate(sys.argv[1] if len(sys.argv) > 1 else 'iteration-01')
