"""Verify frozen reader quotations; never assign or repair semantic grades.

Usage: python3 finalize_reader_quotes.py expanded-iteration-16
       python3 finalize_reader_quotes.py expanded-iteration-16 \
         --primary-review-declaration-file /absolute/path/root-review.json

The optional JSON declaration must contain reviewer='/root', iteration,
declaration (nonempty text), all_answers_reviewed=true, answers_reviewed=2*N,
quote_selection_review_complete=true, no_material_or_unresolved_findings=true,
quote_selection_findings=[] (or closed nonmaterial findings), and hashes binding
the summary, both raw readers, independent-grades.json, results.json and any
existing primary-review-log.json. Each
closed finding needs reader ('a'/'b'), id, optional passage_index (omit for an
answer-wide selection caveat), status='resolved',
material=false and a nonempty disposition. The file is an attributed primary
review attestation, not a review performed by this script.

Outputs are immutable: all prospective outputs are checked before any is
written; a different existing proof is never replaced. No questions or keys are
graded, and answer-key contents are never parsed.
"""
from collections import Counter
from pathlib import Path
import argparse
import hashlib
import json
import math
import re
import sys

R = Path(__file__).resolve().parent
ROOT = Path('/home/jonny/projects/boardgame-rules')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def encoded(value):
    return json.dumps(value, indent=2) + '\n'


def load(path):
    return json.loads(path.read_text())


def resolve(path):
    p = Path(path)
    return p.resolve() if p.is_absolute() else (ROOT / p).resolve()


def verify_ids(rows, expected):
    ids = [x.get('id') for x in rows if isinstance(x, dict)]
    return len(ids) == len(rows) == len(expected) and Counter(ids) == Counter(expected)


def manifest_hashes(value):
    """Yield declared file hashes, including nested path/sha256 bindings."""
    if isinstance(value, dict):
        for key in ('hashes', 'prompt_hashes'):
            for p, digest in value.get(key, {}).items():
                if isinstance(digest, str):
                    yield p, digest
        if isinstance(value.get('path'), str) and isinstance(value.get('sha256'), str):
            yield value['path'], value['sha256']
        for key, child in value.items():
            if key not in ('hashes', 'prompt_hashes'):
                yield from manifest_hashes(child)
    elif isinstance(value, list):
        for child in value:
            yield from manifest_hashes(child)


def audit_quotes(side, raw, summary, summary_sha):
    passages, errors = [], []
    for answer in raw['answers']:
        sources = answer.get('source_passages')
        if not isinstance(sources, list) or not sources:
            errors.append({'reader': side, 'id': answer.get('id'), 'error': 'No nonempty source_passages array'})
            continue
        for index, passage in enumerate(sources, 1):
            q = passage.get('quotation') if isinstance(passage, dict) else None
            valid_string = isinstance(q, str)
            empty = not valid_string or not q.strip()
            literal = valid_string and not empty and q in summary
            row = {'id': answer.get('id'), 'passage_index': index, 'section': passage.get('section') if isinstance(passage, dict) else None, 'characters': len(q) if valid_string else 0, 'empty': empty, 'sha256': hashlib.sha256(q.encode()).hexdigest() if valid_string else None, 'verbatim_substring': literal, 'summary_start_line': summary[:summary.index(q)].count('\n') + 1 if literal else None}
            passages.append(row)
            if not literal:
                errors.append({'reader': side, 'id': answer.get('id'), 'passage_index': index, 'error': 'Empty/non-string quotation' if empty else 'Not an exact nonempty substring'})
    result = {'reader': side, 'raw_sha256': None, 'summary_sha256': summary_sha, 'question_count': len(raw['answers']), 'method': 'Exact nonempty contiguous substring comparison only. Section relevance, requested facts and complete same-question response require separately attributed semantic review.', 'passages': passages, 'literal_count': sum(x['verbatim_substring'] for x in passages), 'empty_count': sum(x['empty'] for x in passages), 'total_count': len(passages)}
    return result, errors


def check_semantic_records(independent, results, raws, expected):
    """Validate existing grade records and their bindings; do not grade answers."""
    errors = []
    count = len(expected)
    for side in 'ab':
        original = independent.get('readers', {}).get('reader-' + side, {})
        imported = results.get(side, {})
        for name, record in [('independent', original), ('results', imported)]:
            grades = record.get('grades', [])
            if not verify_ids(grades, expected):
                errors.append(f'{side}: {name} grade IDs incomplete/duplicated/unexpected')
                continue
            if record.get('totals') != {'correct': count, 'partial': 0, 'incorrect': 0}:
                errors.append(f'{side}: {name} totals are not full correct')
            for row in grades:
                if row.get('grade') != 'correct' or row.get('unsupported_guess') is not False:
                    errors.append(f'{side} {row["id"]}: {name} grade is not explicit correct/no-guess')
                if row.get('summary_support', {}).get('status') != 'supported':
                    errors.append(f'{side} {row["id"]}: {name} summary support is not explicit supported')
                checklist = row.get('requested_fact_checklist')
                if not isinstance(checklist, list) or not checklist or any(not isinstance(x, dict) or x.get('status') not in ('satisfied', 'context_not_requested') for x in checklist):
                    errors.append(f'{side} {row["id"]}: {name} requested-fact checklist is not complete/satisfied')
        originals = {x['id']: x for x in original.get('grades', []) if isinstance(x, dict) and 'id' in x}
        actual = {x['id']: x for x in raws[side]['answers']}
        for row in imported.get('grades', []):
            if not isinstance(row, dict) or row.get('id') not in actual:
                continue
            qid = row['id']
            if row.get('observed') != actual[qid]:
                errors.append(f'{side} {qid}: results observed response differs from frozen raw')
            source = originals.get(qid, {})
            for field in ('grade', 'unsupported_guess', 'summary_support', 'requested_fact_checklist'):
                if row.get(field) != source.get(field):
                    errors.append(f'{side} {qid}: results {field} differs from independent record')
        for row in raws[side]['answers']:
            if row.get('support') != 'supported':
                errors.append(f'{side} {row["id"]}: raw reader support is not explicit supported')
    return errors


def check_primary_review(review, iteration, count, required_hashes, quote_rows, logged_findings=()):
    errors = []
    requirements = {'reviewer': '/root', 'iteration': iteration, 'all_answers_reviewed': True, 'answers_reviewed': 2 * count, 'quote_selection_review_complete': True, 'no_material_or_unresolved_findings': True}
    for key, expected in requirements.items():
        actual = review.get(key)
        if actual != expected or (isinstance(expected, bool) and actual is not expected):
            errors.append(f'Primary declaration {key} does not explicitly match required value')
    if not isinstance(review.get('declaration'), str) or not review['declaration'].strip():
        errors.append('Primary review declaration text missing')
    hashes = review.get('hashes', {})
    for path, digest in required_hashes.items():
        if hashes.get(path) != digest:
            errors.append(f'Primary declaration does not bind exact file hash: {path}')
    findings = review.get('quote_selection_findings')
    if not isinstance(findings, list):
        errors.append('Primary declaration must explicitly list quote_selection_findings')
        findings = []
    seen = set()
    for finding in findings:
        if not isinstance(finding, dict):
            errors.append('Malformed quote-selection finding')
            continue
        identity = (finding.get('reader'), finding.get('id'), finding.get('passage_index'))
        known_identity = identity in quote_rows or (identity[2] is None and any(row[:2] == identity[:2] for row in quote_rows))
        if identity in seen or not known_identity:
            errors.append('Duplicate or nonexistent quote-selection finding identity')
        seen.add(identity)
        if finding.get('status') != 'resolved' or finding.get('material') is not False or not isinstance(finding.get('disposition'), str) or not finding['disposition'].strip():
            errors.append('Quote-selection finding is material, unresolved, or lacks its disposition')
    for finding in logged_findings:
        if not any(x.get('reader') == finding.get('reader') and x.get('id') == finding.get('id') for x in findings if isinstance(x, dict)):
            errors.append(f'Logged quote-selection finding has no explicit final disposition: {finding.get("reader")} {finding.get("id")}')
    return errors, findings


def main():
    parser = argparse.ArgumentParser(__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('iteration', help='Batch-local iteration directory name, e.g. expanded-iteration-16')
    parser.add_argument('--primary-review-declaration-file', type=Path)
    args = parser.parse_args()
    if not re.fullmatch(r'(?:expanded|seed)-iteration-\d+', args.iteration):
        parser.error('Expected one batch-local iteration name')
    directory = R / args.iteration
    problems, checks, files = [], [], set()
    expected_files = [directory / n for n in ('summary-snapshot.md', 'questions.json', 'input-manifest.json', 'raw-output-manifest.json', 'reader-a.json', 'reader-b.json', 'reader-a-prompt.txt', 'reader-b-prompt.txt', 'reader-a-installment-manifest.json', 'reader-b-installment-manifest.json')]
    missing = [str(p) for p in expected_files if not p.is_file()]
    if missing:
        parser.error('Required completed/frozen inputs missing; no proof written: ' + ', '.join(missing))
    files.update(expected_files)
    summary = (directory / 'summary-snapshot.md').read_text()
    # Only question IDs are used. Questions are never graded and key contents are never parsed.
    questions = load(directory / 'questions.json')['questions']
    expected = [x['id'] for x in questions]
    if not expected or len(expected) != len(set(expected)):
        parser.error('Question IDs must be nonempty and unique')
    raws = {side: load(directory / f'reader-{side}.json') for side in 'ab'}
    input_manifest = load(directory / 'input-manifest.json')
    output_manifest = load(directory / 'raw-output-manifest.json')
    declared_input = {str(resolve(p)): h for p, h in manifest_hashes(input_manifest)}
    declared_output = {str(resolve(p)): h for p, h in manifest_hashes(output_manifest)}
    for name in ('summary-snapshot.md', 'questions.json', 'reader-a-prompt.txt', 'reader-b-prompt.txt'):
        if str(directory / name) not in declared_input:
            problems.append(f'Frozen input manifest lacks {name}')
    for side in 'ab':
        if str(directory / f'reader-{side}.json') not in declared_output:
            problems.append(f'Frozen output manifest lacks reader-{side}.json')
    manifests = [(directory / 'input-manifest.json', input_manifest), (directory / 'raw-output-manifest.json', output_manifest)]
    for side in 'ab':
        raw = raws[side]
        if not isinstance(raw.get('answers'), list) or not verify_ids(raw['answers'], expected):
            parser.error(f'Reader {side} must contain every expected ID exactly once; no final quote proof written')
        path = directory / f'reader-{side}-installment-manifest.json'
        manifest = load(path)
        manifests.append((path, manifest))
        checkpoints = manifest.get('checkpoints', [])
        counts = [x.get('answers') for x in checkpoints]
        scheduled = list(range(10, len(expected) + 1, 10))
        if len(expected) % 10:
            scheduled.append(len(expected))
        if counts != scheduled:
            problems.append(f'{side}: checkpoints do not cover the complete ten-question turn schedule')
        for checkpoint in checkpoints:
            p, n = resolve(checkpoint['path']), checkpoint['answers']
            if p.name != f'reader-{side}-installment-{math.ceil(n / 5):02}.json':
                problems.append(f'{side}: checkpoint group filename does not use ceil(answers/5): {p}')
            if not p.is_file():
                problems.append(f'{side}: checkpoint is missing: {p}')
                continue
            data = load(p)
            if data.get('answers') != raw['answers'][:n] or len(data.get('answers', [])) != n:
                problems.append(f'{side}: checkpoint is not an exact frozen raw prefix: {p}')
        if checkpoints and resolve(checkpoints[-1]['path']).is_file() and sha(resolve(checkpoints[-1]['path'])) != sha(directory / f'reader-{side}.json'):
            problems.append(f'{side}: final checkpoint bytes differ from completed raw')
    for manifest_path, value in manifests:
        for path_string, digest in manifest_hashes(value):
            path = resolve(path_string)
            actual = sha(path) if path.is_file() else None
            good = actual == digest
            checks.append({'manifest': str(manifest_path), 'path': str(path), 'expected_sha256': digest, 'actual_sha256': actual, 'matches': good})
            if path.is_file():
                files.add(path)
            if not good:
                problems.append(f'Frozen hash mismatch/missing file: {path}')
    outputs, audits, quote_errors = {}, {}, []
    for side in 'ab':
        audit, errors = audit_quotes(side, raws[side], summary, sha(directory / 'summary-snapshot.md'))
        audit['raw_sha256'] = sha(directory / f'reader-{side}.json')
        audits[side] = audit
        quote_errors.extend(errors)
        outputs[directory / f'reader-{side}-quote-audit.json'] = encoded(audit)
    semantic_paths = [directory / x for x in ('independent-grades.json', 'results.json')]
    semantic_present = all(p.is_file() for p in semantic_paths)
    semantic_errors = check_semantic_records(load(semantic_paths[0]), load(semantic_paths[1]), raws, expected) if semantic_present else ['Completed independent-grades.json and results.json are both required']
    files.update(p for p in semantic_paths if p.is_file())
    review_errors, findings, review = ['Explicit attributed primary review declaration is required'], [], None
    review_log_path = directory / 'primary-review-log.json'
    review_log = load(review_log_path) if review_log_path.is_file() else None
    logged_findings = review_log.get('selection_findings', []) if review_log else []
    if review_log:
        files.add(review_log_path)
    if args.primary_review_declaration_file is not None:
        review_path = args.primary_review_declaration_file.resolve()
        if not review_path.is_file():
            parser.error('Supplied primary review declaration file is missing')
        review = load(review_path)
        binding_files = [directory / 'summary-snapshot.md', directory / 'reader-a.json', directory / 'reader-b.json'] + semantic_paths + ([review_log_path] if review_log else [])
        required_hashes = {str(p): sha(p) for p in binding_files if p.is_file()}
        quote_rows = {(side, x['id'], x['passage_index']) for side in 'ab' for x in audits[side]['passages']}
        review_errors, findings = check_primary_review(review, args.iteration, len(expected), required_hashes, quote_rows, logged_findings)
        files.add(review_path)
    literal_ok = not problems and not quote_errors
    semantic_complete = semantic_present and not semantic_errors and review is not None and not review_errors
    passed = literal_ok and semantic_complete
    flag_count = len(quote_errors)
    hashes = {str(p): sha(p) for p in sorted(files)}
    hashes.update({str(p): hashlib.sha256(text.encode()).hexdigest() for p, text in outputs.items()})
    proof = {'status': 'PASS' if passed else ('EXACT_QUOTES_VERIFIED_PENDING_SEMANTIC_REVIEW' if literal_ok else 'QUOTE_VERIFICATION_FAILED'), 'scope': 'Literal quotations and frozen evidence integrity, with separately attributed completed semantic grade/review prerequisites when PASS. Literal matching does not establish that the selected quotation supplies its answer. Closed nonmaterial citation-selection caveats are retained without a format-only grade penalty. No source-correctness verdict, grade creation, key repair or cognitive-attention claim.', 'iteration': args.iteration, 'expected_answers_per_reader': len(expected), 'all_expected_ids_once': True, 'all_frozen_hashes_match': all(x['matches'] for x in checks), 'frozen_manifest_checks': checks, 'frozen_structure_findings': problems, 'all_quotes_exact_nonempty_substrings_of_frozen_summary': not quote_errors, 'flagged_blocks_expected': flag_count, 'flagged_blocks_independently_disposed': 0, 'no_material_or_unresolved_findings': passed, 'literal_quote_findings': quote_errors, 'quote_selection_findings': findings, 'primary_review_log_findings': logged_findings, 'readers': [{k: audits[side][k] for k in ('reader', 'question_count', 'literal_count', 'empty_count', 'total_count')} for side in 'ab'], 'total_exact_nonempty_quotes': sum(audits[side]['literal_count'] for side in 'ab'), 'independent_semantic_records_complete_full_correct_no_guesses': semantic_present and not semantic_errors, 'semantic_prerequisite_findings': semantic_errors, 'primary_review': {'provided': review is not None, 'attributed_reviewer': review.get('reviewer') if review else None, 'declaration': review.get('declaration') if review else None, 'declaration_file': str(args.primary_review_declaration_file.resolve()) if args.primary_review_declaration_file else None, 'declaration_validation_findings': review_errors, 'helper_review_scope': 'Programmatic quote/hash/record validation only. The script did not perform the primary semantic or quote-selection review.'}, 'hashes': hashes}
    outputs[directory / 'quotation-review-validation.json'] = encoded(proof)
    # Preflight all outputs so a conflicting historical proof cannot cause a partial rewrite.
    for path, text in outputs.items():
        if path.exists() and path.read_text() != text:
            parser.error(f'Refusing to overwrite different immutable evidence: {path}; preserve it before a separate finalization')
    for path, text in outputs.items():
        if not path.exists():
            path.write_text(text)
    print(json.dumps({'status': proof['status'], 'iteration': args.iteration, 'expected_answers_per_reader': len(expected), 'exact_nonempty_quotes': proof['total_exact_nonempty_quotes'], 'frozen_hash_checks': len(checks), 'proof_sha256': sha(directory / 'quotation-review-validation.json')}))
    return 0 if literal_ok else 2


if __name__ == '__main__':
    sys.exit(main())
