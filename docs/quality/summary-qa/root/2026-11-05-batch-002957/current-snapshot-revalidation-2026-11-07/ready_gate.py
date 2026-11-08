"""Concrete current-byte handoff gate; no publication or shared writes."""
from evidence import *
import re
import subprocess

def main():
    directory = N / 'iteration-02'
    checks = []
    def check(name, condition, detail=None):
        checks.append({'check': name, 'passed': bool(condition), 'detail': detail})
    check('Canonical exact authorized current SHA', sha(ROOT / 'rules/root.md') == 'da0b6b08fda1d3e1775a8ef813e31535ac35375399b061efe255690d09ad1aeb')
    check('Final snapshot exact current canonical bytes', (directory / 'summary-snapshot.md').read_bytes() == (ROOT / 'rules/root.md').read_bytes())
    for name in ('validation.json', 'protocol-validation.json'):
        report = json.loads((directory / name).read_text())
        check('Final ' + name + ' PASS', report['status'] == 'PASS')
    result = json.loads((directory / 'results.json').read_text())
    originals = json.loads((directory / 'raw-output-manifest.json').read_text())
    declaration = json.loads((directory / 'primary-review-declaration.json').read_text())
    check('All162 complete original entries substantively reviewed', declaration['complete_entries_reviewed'] == 162 and declaration['all_substantive_fields_reviewed'] and declaration['all_requested_material_facts_resolved'])
    check('Primary review declaration binds all current inputs/outputs', all(sha(path) == expected for path, expected in declaration['hashes'].items()))
    check('Both final full originals precede any semantic grading', originals['existing_primary_count'] == 0)
    for side in 'ab':
        row = result['readers'][side]
        check('Reader' + side + ' final81/0/0', row['totals'] == {'correct': 81, 'partial': 0, 'incorrect': 0})
        check('Reader' + side + ' zero unresolved facts/unsupported guesses', all(g['grade'] == 'correct' and g['unresolved_requested_fact'] is False and g['unsupported_guess'] is False for g in row['grades']))
        for name in (f'reader-{side}-input-before-first-save/delivery-audit.json', f'reader-{side}-delivery-completed/delivery-audit.json'):
            report = json.loads((directory / name).read_text())
            check(side + ' ' + name + ' PASS', report['status'] == 'PASS')
        check('Reader' + side + ' immutable exact full original', sha(directory / f'reader-{side}.json') == originals['readers'][side]['sha256'])
        frozen = datetime.datetime.fromisoformat(originals['frozen_at_utc']).timestamp()
        check('Reader' + side + ' every primary grade written after both full originals frozen', all(p.stat().st_mtime >= frozen for p in (directory / 'primary-grades').glob(side + '-*.json')))
    old_result = json.loads((N / 'iteration-01/results.json').read_text())
    check('Genuine first-attempt failures retained', old_result['readers']['a']['totals'] == {'correct': 79, 'partial': 2, 'incorrect': 0} and old_result['readers']['b']['totals'] == {'correct': 81, 'partial': 0, 'incorrect': 0})
    old_primary = json.loads((N / 'iteration-01/results-primary.json').read_text())
    check('Original two semantic borderline labels retained', old_primary['readers']['a']['totals']['borderline'] == old_primary['readers']['b']['totals']['borderline'] == 1)
    check('Original grading chronology deviation retained', (N / 'iteration-01/grading-chronology-deviation.json').is_file())
    check('Nonfactual actual B restriction repetition disclosed', (directory / 'prompt-repetition-disclosure.json').is_file())
    provenance = json.loads((directory / 'protocol-validation.json').read_text())
    final_ids = {x['session_id'] for x in provenance['actors']}
    previous_ids = set()
    for p in R.glob('*-iteration-*/model-provenance.json'):
        raw = json.loads(p.read_text())
        for row in raw.get('readers', []):
            if row.get('session_id'):
                previous_ids.add(row['session_id'])
    previous_ids.update(x['session_id'] for x in json.loads((N / 'iteration-01/protocol-validation.json').read_text())['actors'])
    check('Final two identities new versus all old readers', len(final_ids) == 2 and not final_ids.intersection(previous_ids))
    audit = N / 'source-only-audit/source-audit.json'
    source = json.loads(audit.read_text())
    check('New pure source audit PASS with no findings', source['verdict'] == 'PASS' and source['findings'] == [])
    check('New pure audit exact tested bytes', source['input_hashes'][str((N / 'iteration-01/summary-snapshot.md').resolve())]['sha256'] == sha(directory / 'summary-snapshot.md'))
    proof = json.loads((N / 'source-delivery-serialized-metadata/source-delivery-audit.json').read_text())
    check('Complete actual source union/native imagery PASS', proof['status'] == 'PASS' and proof['image_delivery']['status'] == 'PASS' and len(proof['pdf_pages']) == 32)
    check('Source proof original audit bytes bound', proof['completed_source_audit']['sha256'] == sha(audit))
    check('Final coverage ledger unchanged', sha(R / 'coverage-ledger.json') == '1d8e969840696732b73bc081ac0fa97e7ba7c4a28e960a4202205aac1bfe27b5')
    check('Reused independent source/FAQ coverage review unchanged', sha(R / 'publisher-faq-coverage-review-02.json') == '5c9a9acef26430a98f43e1c54eb21942907fbcb9ca8c8c0fe8c3deef844b1d59')
    links = []
    for report in [R / 'README.md', N / 'README.md', N / 'previous-complete-report-linked.md', N / 'iteration-01/report.md', directory / 'report.md']:
        for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', report.read_text()):
            if target.startswith(('https:', 'http:', 'mailto:', '#')):
                continue
            target = target.split('#')[0].strip('<>')
            path = Path(target) if target.startswith('/') else report.parent / target
            links.append({'report': str(report), 'target': target, 'resolved': str(path.resolve()), 'exists': path.exists()})
    check('Every current report link resolves', all(x['exists'] for x in links), [x for x in links if not x['exists']])
    scope = subprocess.run(['git', 'diff', '--check', '--', 'rules/root.md', str(R.relative_to(ROOT))], cwd=ROOT, capture_output=True, text=True)
    check('Scoped git diff whitespace check', scope.returncode == 0, scope.stdout + scope.stderr)
    result = {'status': 'PASS' if all(x['passed'] for x in checks) else 'FAIL', 'passed': sum(x['passed'] for x in checks), 'total': len(checks), 'checks': checks, 'report_link_count': len(links), 'report_links': links, 'coordinator_acceptance': 'Still required. This gate does not record, stamp, publish or complete the actual goal.'}
    save(N / 'ready-validation.json', result)
    print(json.dumps({'status': result['status'], 'passed': result['passed'], 'total': result['total'], 'links': len(links), 'failures': [x for x in checks if not x['passed']]}))

if __name__ == '__main__':
    main()
