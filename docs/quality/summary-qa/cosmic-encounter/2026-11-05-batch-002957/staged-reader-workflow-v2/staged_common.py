"""Generic stage metadata. No answer generation, routing, or factual grading."""
import hashlib
import json
import re
from pathlib import Path


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(',', ':'), allow_nan=False).encode('utf-8')


def same(a, b):
    return encoded(a) == encoded(b)


def load(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('Duplicate JSON object key')
            result[key] = value
        return result
    def invalid(value):
        raise ValueError('Non-finite JSON value')
    return json.loads(Path(path).read_bytes(), object_pairs_hook=unique,
                      parse_constant=invalid)


def write_new(path, value):
    with Path(path).open('x', encoding='utf-8') as handle:
        handle.write(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n')


class Context:
    def __init__(self, iteration):
        self.root = Path(iteration).resolve()
        self.manifest_path = self.root / 'input-manifest-final.json'
        self.manifest = load(self.manifest_path)
        self.questions_path = self.root / 'questions.json'
        self.document = load(self.questions_path)
        self.code_path = self.root / 'generic-method-code.py'
        raw = self.code_path.read_bytes()
        if sha(raw) != self.manifest['generic_code_sha256']:
            raise ValueError('Generic method hash mismatch')
        # This is the predeclared trusted generic copy, never a reader output.
        self.method = {'__name__': 'staged_trusted_generic_method'}
        exec(compile(raw, str(self.code_path), 'exec'), self.method)
        self.questions = self.method['question_records'](self.document)
        self.n = len(self.questions)
        if self.n < 1 or type(self.manifest['question_count']) is not int or self.n != self.manifest['question_count']:
            raise ValueError('Frozen question count mismatch or empty bank')
        self.schedule = self.manifest['stage_schedule']
        if self.schedule != {'draft_batch_size': 10, 'review_batch_size': 20}:
            raise ValueError('Expected predeclared draft=10, review=20 schedule')
        files = self.manifest['sole_game_data_files']
        if not isinstance(files, list) or len(files) != 2 or not all(isinstance(p, str) and Path(p).is_absolute() for p in files) or len(set(files)) != 2:
            raise ValueError('Two distinct absolute game-data paths required')
        self.reader_questions_path = self.root / 'reader-questions-final.json'
        if str(self.reader_questions_path) not in files or str(self.questions_path) in files:
            raise ValueError('Reader data must contain reader-questions-final.json, not grading questions.json')
        self.reader_document = load(self.reader_questions_path)
        reader_questions = self.method['question_records'](self.reader_document)
        if not same(reader_questions, self.questions):
            raise ValueError('Embedded reader questions differ from the frozen grading bank')
        for label in ('a', 'b'):
            if self.manifest['reader_tasks'][label] != '/root/expanded6_reader_' + label:
                raise ValueError('Unexpected predeclared reader task')
            paths = self.manifest['reader_work_paths'][label]
            if any(not isinstance(paths.get(k), str) or not Path(paths[k]).is_absolute() for k in ('draft', 'final')) or paths['draft'] == paths['final']:
                raise ValueError('Distinct absolute draft/final paths required')
        all_paths = [self.work(label, kind) for label in ('a', 'b') for kind in ('draft', 'final')]
        if len(set(all_paths)) != 4:
            raise ValueError('Each reader must have separate work files')

    def work(self, label, kind):
        if label not in ('a', 'b'):
            raise ValueError('Reader label must be a or b')
        return Path(self.manifest['reader_work_paths'][label][kind]).resolve()

    def frozen(self):
        return {'manifest_sha256': sha(self.manifest_path.read_bytes()),
                'questions_sha256': sha(self.questions_path.read_bytes()),
                'reader_questions_sha256': sha(self.reader_questions_path.read_bytes()),
                'generic_code_sha256': sha(self.code_path.read_bytes())}


def archives(ctx, label, stage):
    term = {'input': 'input-ready', 'draft': 'draft-batch', 'review': 'review-batch'}[stage]
    prefix = 'reader-' + label + '-' + term + '-'
    found = []
    for path in ctx.root.glob(prefix + '*.json'):
        match = re.fullmatch(re.escape(prefix) + r'(\d+)\.json', path.name)
        if match:
            found.append((int(match[1]), path))
    return sorted(found)


def report_path(path):
    return path.with_name(path.stem + '-structure.json')


def metadata_changes(old, new):
    return [key for key in ('inputs_read', 'instructions_read', 'method_code_sha256')
            if key not in old or key not in new or not same(old[key], new[key])]


def pool_values(doc):
    pool = doc.get('evidence_units', {})
    if isinstance(pool, dict):
        return {'/evidence_units/' + str(key).replace('~', '~0').replace('/', '~1'): value
                for key, value in pool.items()}
    if isinstance(pool, list):
        return {'/evidence_units/' + str(i): value for i, value in enumerate(pool)}
    raise ValueError('Shared evidence pool must be an object or array')


def changes(old, new):
    answers = new.get('answers', [])
    changed = [a.get('id') for index, a in enumerate(old.get('answers', []))
               if index >= len(answers) or not same(a, answers[index])]
    old_pool, new_pool = pool_values(old), pool_values(new)
    pool_changed = [key for key, value in old_pool.items()
                    if key not in new_pool or not same(value, new_pool[key])]
    return changed, pool_changed


def check_doc(ctx, label, stage, doc, expected):
    errors = []
    if not isinstance(doc, dict):
        return ['Output must be an object']
    answers = doc.get('answers')
    if not isinstance(answers, list):
        return ['answers must be an array']
    if len(answers) != expected:
        errors.append('Wrong scheduled prefix length')
    try:
        ctx.method['validate_question_bindings'](ctx.document, answers, complete=expected == ctx.n)
        if stage != 'input':
            ctx.method['validate_clause_bindings'](ctx.document, answers, complete=expected == ctx.n)
        pool_values(doc)
    except (ValueError, KeyError, TypeError, AttributeError) as exc:
        errors.append('Literal/question/clause/evidence structure: ' + str(exc))
    required_stage = ('inputs_ready' if stage == 'input' else
                      ('draft_complete' if expected == ctx.n else 'drafting') if stage == 'draft' else
                      ('review_complete' if expected == ctx.n else 'reviewing'))
    if doc.get('stage') != required_stage:
        errors.append('Incorrect stage label')
    if doc.get('reader') != label:
        errors.append('Incorrect reader label')
    if doc.get('method_code_sha256') != ctx.manifest['generic_code_sha256']:
        errors.append('Incorrect method hash')
    if not isinstance(doc.get('instructions_read'), dict):
        errors.append('Missing process receipt object')
    inputs = doc.get('inputs_read')
    if not isinstance(inputs, list) or len(inputs) != 2 or not all(isinstance(item, dict) for item in inputs):
        errors.append('Two original input receipts required')
    elif sorted(item.get('path', '') for item in inputs) != sorted(ctx.manifest['sole_game_data_files']):
        errors.append('Input receipt paths differ from declared data files')
    else:
        for item in inputs:
            last = 0
            chunks = item.get('chunks')
            valid = (item.get('complete') is True and type(item.get('bytes')) is int and item['bytes'] >= 0
                     and type(item.get('characters')) is int and item['characters'] > 0
                     and isinstance(item.get('sha256'), str) and len(item['sha256']) == 64
                     and isinstance(chunks, list) and bool(chunks))
            for chunk in chunks if isinstance(chunks, list) else []:
                if not isinstance(chunk, dict):
                    valid = False
                    continue
                start, end = chunk.get('start'), chunk.get('end')
                if type(start) is not int or type(end) is not int or start != last or not 0 < end - start <= 2900:
                    valid = False
                if not isinstance(chunk.get('sha256'), str) or not re.fullmatch(r'[0-9a-f]{64}', chunk['sha256']):
                    valid = False
                last = end
            if not valid or last != item.get('characters'):
                errors.append('Incomplete/bounded input receipt declaration')
    continuation = doc.get('continuation', {})
    if not isinstance(continuation, dict) or any(not same(continuation.get(key), value) for key, value in
            [('completed_count', expected), ('next_record_index_zero_based', expected), ('bank_complete', expected == ctx.n)]):
        errors.append('Incorrect continuation metadata')
    if stage == 'input' and doc.get('evidence_units') != {}:
        errors.append('Input readiness requires an empty evidence dictionary')
    if stage == 'review':
        review = doc.get('self_review', {})
        if not isinstance(review, dict) or any(not same(review.get(key), value) for key, value in
                [('reviewed_count', expected), ('next_record_index_zero_based', expected), ('complete', expected == ctx.n)]):
            errors.append('Incorrect own-review prefix metadata')
        receipts = review.get('receipts') if isinstance(review, dict) else None
        if not isinstance(receipts, list) or [r.get('id') if isinstance(r, dict) else None for r in receipts] != [q['id'] for q in ctx.questions[:expected]]:
            errors.append('Review receipts must follow the actual reviewed question prefix')
    return errors


def checked_archives(ctx, label, stage, before_number=None):
    items, errors, previous = [], [], None
    history = archives(ctx, label, stage)
    for index, (number, path) in enumerate(history, 1):
        if before_number is not None and number >= before_number:
            break
        if number != index:
            errors.append('Archive numbering gap: ' + path.name)
        raw = path.read_bytes()
        try:
            doc, report = load(path), load(report_path(path))
            expected = 0 if stage == 'input' else min(index * (10 if stage == 'draft' else 20), ctx.n)
            diagnostics = []
            if report.get('raw_snapshot_sha256') != sha(raw) or report.get('frozen_inputs') != ctx.frozen():
                diagnostics.append('Archive hash/frozen inputs mismatch')
            if report.get('stage') != stage or report.get('reader') != label or report.get('sequence') != number:
                diagnostics.append('Archive report association mismatch')
            effective_path = path
            if stage in ('draft', 'review'):
                from correct_stage_metadata import resolve_archive
                (effective_path, doc, report), resolution_errors = resolve_archive(
                    ctx, label, stage, number, path, doc, report, previous)
                diagnostics.extend(resolution_errors)
            diagnostics.extend(check_doc(ctx, label, stage, doc, expected))
            if previous is not None and stage != 'input':
                changed, pool_changed = changes(previous, doc)
                if changed or pool_changed or metadata_changes(previous, doc):
                    diagnostics.append('Previously completed stage values changed')
            if not report.get('pass') or diagnostics:
                errors.append({'archive': path.name, 'diagnostics': diagnostics or report.get('errors', [])})
            items.append((effective_path, doc, report))
            previous = doc
        except (ValueError, KeyError, TypeError, AttributeError, OSError) as exc:
            errors.append({'archive': path.name, 'diagnostics': [str(exc)]})
    return items, errors


def closed_draft(ctx, label):
    items, errors = checked_archives(ctx, label, 'draft')
    required = (ctx.n + 9) // 10
    if len(items) != required or errors:
        raise ValueError('A structurally valid complete immutable draft history is required')
    path, doc, _ = items[-1]
    if ctx.work(label, 'draft').read_bytes() != path.read_bytes():
        raise ValueError('Closed live draft differs from its final archived bytes')
    ready, ready_errors = input_history(ctx, label)
    if ready is None or ready_errors or metadata_changes(ready, doc):
        raise ValueError('Complete unchanged input-readiness metadata required')
    return path, doc


def input_history(ctx, label):
    """Keep failed readiness attempts; only the last attempt authorizes drafting."""
    history, errors, latest = archives(ctx, label, 'input'), [], None
    for index, (number, path) in enumerate(history, 1):
        try:
            report = load(report_path(path))
            if number != index or report.get('raw_snapshot_sha256') != sha(path.read_bytes()) or report.get('frozen_inputs') != ctx.frozen():
                errors.append('Input archive hash/number/frozen binding mismatch')
            if index == len(history):
                latest = load(path)
                if not report.get('pass') or check_doc(ctx, label, 'input', latest, 0):
                    errors.append('Latest readiness attempt must pass structural checks')
        except (ValueError, KeyError, TypeError, AttributeError, OSError) as exc:
            errors.append(str(exc))
    if not history:
        errors.append('No readiness attempts archived')
    return latest, errors


def runtime_provenance_path(ctx):
    path = Path(ctx.manifest.get('model_provenance_path', str(ctx.root / 'model-provenance.json')))
    if not path.is_absolute():
        raise ValueError('Explicit model provenance path must be absolute')
    return path.resolve()


def locate_runtime(ctx, label):
    """Production entry points only; never called by synthetic tests."""
    provenance_path = runtime_provenance_path(ctx)
    provenance = load(provenance_path)
    task = ctx.manifest['reader_tasks'][label]
    agents = [agent for agent in provenance['agents'] if agent.get('task') == task]
    if len(agents) != 1:
        raise ValueError('Exactly one runtime for the predeclared reader is required')
    path = Path(agents[0]['runtime_source_path'])
    if not path.is_absolute():
        raise ValueError('Runtime path must be absolute')
    return path.resolve(), {'task': task, 'provenance_path': str(provenance_path),
                            'provenance_sha256': sha(provenance_path.read_bytes())}


def runtime_records(raw):
    result, last = [], -1
    for index, line in enumerate(raw.splitlines(keepends=True)):
        if not line.strip():
            raise ValueError('Blank runtime record')
        row = json.loads(line)
        ordinal = row.get('ordinal', index)
        if type(ordinal) is not int or ordinal <= last:
            raise ValueError('Runtime ordinals must strictly increase')
        result.append((ordinal, line, row))
        last = ordinal
    if raw and not raw.endswith(b'\n'):
        raise ValueError('Runtime must end at a complete JSONL record boundary')
    return result
