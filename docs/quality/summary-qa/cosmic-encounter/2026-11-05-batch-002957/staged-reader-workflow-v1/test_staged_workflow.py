"""Neutral synthetic fixtures only. Never opens production provenance/runtime."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

from begin_review import make_start
from snapshot_stage import snapshot
from staged_common import Context, closed_draft, encoded, load, runtime_provenance_path, sha
from validate_staged_history import validate_history
from verify_review_payloads import verify_payloads

HERE = Path(__file__).resolve().parent
GENERIC = HERE.parent / 'reader-method-v15' / 'source_units.py'


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def line(ordinal, output=None, kind='custom_tool_call_output'):
    return (json.dumps({'ordinal': ordinal, 'payload': {'type': kind, 'output': output}}, ensure_ascii=False) + '\n').encode()


class StagedTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='.synthetic-', dir=HERE)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.code = GENERIC.read_bytes()
        (self.root / 'generic-method-code.py').write_bytes(self.code)
        self.questions = [{'id': 'neutral/' + str(i * 7 + 3), 'question': 'Record label ' + str(i) + '?',
                           'unknown_question': ['雪', i, False]} for i in range(23)]
        save(self.root / 'questions.json', {'questions': self.questions, 'unknown_document': None})
        save(self.root / 'reader-questions-final.json', {'questions': self.questions,
                                                       'reader_process': {'neutral_instruction': 'Fixture metadata.'}})
        (self.root / 'summary-snapshot.md').write_text('Neutral fixture text.\n', encoding='utf-8')
        self.manifest = {'question_count': 23, 'generic_code_sha256': sha(self.code),
                         'sole_game_data_files': [str(self.root / 'summary-snapshot.md'), str(self.root / 'reader-questions-final.json')],
                         'reader_tasks': {c: '/root/expanded6_reader_' + c for c in 'ab'},
                         'reader_work_paths': {c: {k: str(self.root / (c + '-' + k + '.json')) for k in ('draft', 'final')} for c in 'ab'},
                         'stage_schedule': {'draft_batch_size': 10, 'review_batch_size': 20},
                         'model_provenance_path': str(self.root.parent / 'neutral-parent-provenance-not-opened.json'),
                         'unknown_manifest_field': {'preserve': True}}
        save(self.root / 'input-manifest-final.json', self.manifest)
        self.ctx = Context(self.root)
        self.inputs = []
        for path in self.manifest['sole_game_data_files']:
            raw = Path(path).read_bytes()
            text = raw.decode()
            self.inputs.append({'path': path, 'bytes': len(raw), 'characters': len(text),
                                'sha256': sha(raw), 'complete': True,
                                'chunks': [{'start': i, 'end': min(i + 2900, len(text)),
                                            'sha256': sha(text[i:i + 2900].encode())} for i in range(0, len(text), 2900)]})
        self.original_answers = []
        for i, q in enumerate(self.questions):
            answer = self.ctx.method['new_answer_record'](q)
            answer.update({'clauses': [self.ctx.method['new_clause_record'](answer, 0, len(q['question']))],
                           'answer': 'Neutral unchecked label.', 'evidence_refs': [7, '7'],
                           'unknown_answer': '雪é📄' * 1100 if i == 0 else {'index': i, 'flag': False}})
            self.original_answers.append(answer)
        self.pool = {'7': {'text': 'Neutral complete shared unit.', 'extra': ['Ω', None]},
                     'unused': {'text': 'Unlinked fixture material.'}}

    def document(self, label, stage, count, revised=True):
        answers = copy.deepcopy(self.original_answers[:count])
        if stage == 'review' and revised and answers:
            answers[0]['answer'] = 'Neutral revised label.'
        doc = {'reader': label, 'stage': ('inputs_ready' if stage == 'input' else
                                         ('draft_complete' if count == 23 else 'drafting') if stage == 'draft' else
                                         ('review_complete' if count == 23 else 'reviewing')),
               'inputs_read': self.inputs, 'instructions_read': {'neutral_process_receipt': True},
               'method_code_sha256': sha(self.code), 'answers': answers,
               'evidence_units': {} if stage == 'input' else copy.deepcopy(self.pool),
               'continuation': {'completed_count': count, 'next_record_index_zero_based': count, 'bank_complete': count == 23},
               'unknown_output': {'keep': ['雪', None, 1.5, False]}}
        if stage == 'review':
            doc['self_review'] = {'reviewed_count': count, 'next_record_index_zero_based': count,
                                  'complete': count == 23, 'revised_ids': [self.questions[0]['id']] if revised else [],
                                  'receipts': self.receipts()[:count]}
        return doc

    def receipts(self):
        receipts = []
        for question, answer in zip(self.questions, self.original_answers):
            display = self.ctx.method['review_display_record'](question, answer, self.pool)
            chunks = list(self.ctx.method['unit_display_blocks'](display, limit=2900))
            receipts.append({'id': question['id'], 'payload_sha256': display['sha256'],
                             'chunks': [{'start': c['start'], 'end': c['end'], 'sha256': c['sha256']} for c in chunks]})
        return receipts

    def payload_outputs(self, first=20, whole=False, revised=False, kind='custom_tool_call_output'):
        rows, ordinal = [], first
        for i, (question, answer) in enumerate(zip(self.questions, self.original_answers)):
            answer = copy.deepcopy(answer)
            if revised and i == 0:
                answer['answer'] = 'Neutral revised label.'
            display = self.ctx.method['review_display_record'](question, answer, self.pool)
            pieces = [display['text']] if whole else [c['text'] for c in self.ctx.method['unit_display_blocks'](display, limit=2900)]
            for piece in pieces:
                rows.append(line(ordinal, [{'type': 'text', 'text': piece}], kind))
                ordinal += 1
        return b''.join(rows)

    def draft(self, label='a'):
        save(self.ctx.work(label, 'draft'), self.document(label, 'input', 0))
        self.assertTrue(snapshot(self.root, label, 'input')['pass'])
        for count in (10, 20, 23):
            save(self.ctx.work(label, 'draft'), self.document(label, 'draft', count))
            self.assertTrue(snapshot(self.root, label, 'draft')['pass'])

    def fence(self, label='a', prefix=None):
        raw = prefix if prefix is not None else line(4, 'Neutral pre-review public output.')
        path = self.root / (label + '-synthetic-runtime.jsonl')
        path.write_bytes(raw)
        make_start(self.ctx, label, path, raw)
        return path, raw

    def review(self, label='a'):
        for count in (20, 23):
            save(self.ctx.work(label, 'final'), self.document(label, 'review', count))
            self.assertTrue(snapshot(self.root, label, 'review')['pass'])

    def complete(self):
        self.draft()
        path, prefix = self.fence()
        self.review()
        return path, prefix

    def test_full_two_reader_history_original_refs_unknown_fields_and_corrections(self):
        for label in 'ab':
            self.draft(label)
            path, prefix = self.fence(label)
            self.review(label)
            result = verify_payloads(self.ctx, label, path, prefix + self.payload_outputs())
            self.assertTrue(result['pass'], result)
            self.assertEqual(len(result['payloads']), 23)
            self.assertEqual(result['payloads'][0]['explicit_shared_unit_count'], 1)
            self.assertEqual(len(result['payloads'][0]['chunks']), 2)
            draft_path, draft = closed_draft(self.ctx, label)
            self.assertEqual(draft['answers'], self.original_answers)
            self.assertEqual(draft['unknown_output'], self.document(label, 'draft', 23)['unknown_output'])
            report = load(self.root / ('reader-' + label + '-review-batch-02-structure.json'))
            self.assertEqual(report['draft_to_review_diff']['changed_answer_ids'], [self.questions[0]['id']])
            self.assertEqual(report['draft_to_review_diff']['answers'][0]['changes'][0]['path'], '/answer')
            unit = self.ctx.method['review_display_record'](self.questions[0], draft['answers'][0], draft['evidence_units'])['payload']['explicitly_referenced_shared_evidence'][0]
            self.assertEqual([x['value'] for x in unit['references']], [7, '7'])
            self.assertNotIn('Unlinked fixture material.', json.dumps(unit))
        self.assertTrue(validate_history(self.root)['pass'])

    def test_computed_only_receipts_are_not_actual_presence(self):
        path, prefix = self.complete()
        result = verify_payloads(self.ctx, 'a', path, prefix + line(6, 'Only a hash was computed.'))
        self.assertFalse(result['pass'])
        self.assertFalse(result['payloads'][0]['pass'])

    def test_pre_fence_delivery_and_other_private_messages_rejected(self):
        self.draft()
        path, prefix = self.fence(prefix=self.payload_outputs(first=0))
        self.review()
        self.assertFalse(verify_payloads(self.ctx, 'a', path, prefix)['pass'])
        private = self.payload_outputs(first=100, kind='hidden_message')
        self.assertFalse(verify_payloads(self.ctx, 'a', path, prefix + private)['pass'])

    def test_cannot_subdivide_large_actual_payload_or_display_revised_instead(self):
        path, prefix = self.complete()
        for output in (self.payload_outputs(whole=True), self.payload_outputs(revised=True)):
            with self.subTest(output_sha=sha(output)):
                self.assertFalse(verify_payloads(self.ctx, 'a', path, prefix + output)['pass'])

    def test_runtime_identity_prefix_hash_and_ordinal_fences(self):
        path, prefix = self.complete()
        self.assertFalse(verify_payloads(self.ctx, 'a', self.root / 'other-runtime.jsonl', prefix + self.payload_outputs())['pass'])
        self.assertFalse(verify_payloads(self.ctx, 'a', path, line(4, 'Changed prefix') + self.payload_outputs())['pass'])
        self.assertFalse(verify_payloads(self.ctx, 'a', path, prefix + line(4, 'Duplicate ordinal.'))['pass'])

    def test_archives_malformed_bytes_before_diagnostics_and_preserves_attempts(self):
        path = self.ctx.work('a', 'draft')
        raw = b'{"answers": [INVALID, "neutral"]}\n'
        path.write_bytes(raw)
        result = snapshot(self.root, 'a', 'input')
        self.assertFalse(result['pass'])
        self.assertEqual((self.root / 'reader-a-input-ready-01.json').read_bytes(), raw)
        self.draft()
        self.assertTrue((self.root / 'reader-a-input-ready-02.json').exists())
        closed_draft(self.ctx, 'a')

    def test_wrong_order_and_literal_are_structural_diagnostics(self):
        save(self.ctx.work('a', 'draft'), self.document('a', 'input', 0))
        snapshot(self.root, 'a', 'input')
        doc = self.document('a', 'draft', 10)
        doc['answers'][0], doc['answers'][1] = doc['answers'][1], doc['answers'][0]
        doc['answers'][1]['literal_question'] += ' '
        save(self.ctx.work('a', 'draft'), doc)
        result = snapshot(self.root, 'a', 'draft')
        self.assertFalse(result['pass'])
        self.assertFalse(result['factual_grades_or_automatic_caps'])
        self.assertEqual(load(self.root / 'reader-a-draft-batch-01.json'), doc)

    def test_earlier_answers_and_evidence_cannot_change_within_drafting(self):
        save(self.ctx.work('a', 'draft'), self.document('a', 'input', 0))
        snapshot(self.root, 'a', 'input')
        save(self.ctx.work('a', 'draft'), self.document('a', 'draft', 10))
        snapshot(self.root, 'a', 'draft')
        doc = self.document('a', 'draft', 20)
        doc['answers'][0]['unknown_answer'] = 'Changed earlier unknown value.'
        doc['evidence_units']['7']['extra'] = []
        save(self.ctx.work('a', 'draft'), doc)
        result = snapshot(self.root, 'a', 'draft')
        self.assertFalse(result['pass'])
        self.assertEqual(result['earlier_answer_values_changed_ids'], [self.questions[0]['id']])
        self.assertEqual(result['earlier_evidence_values_changed_paths'], ['/evidence_units/7'])

    def test_closed_draft_work_bytes_and_final_work_bytes_must_match_archives(self):
        path, prefix = self.complete()
        original = self.ctx.work('a', 'draft').read_bytes()
        self.ctx.work('a', 'draft').write_bytes(original + b' ')
        with self.assertRaises(ValueError):
            closed_draft(self.ctx, 'a')
        self.ctx.work('a', 'draft').write_bytes(original)
        final = self.ctx.work('a', 'final')
        final.write_bytes(final.read_bytes() + b' ')
        self.assertFalse(verify_payloads(self.ctx, 'a', path, prefix + self.payload_outputs())['pass'])

    def test_review_fence_and_archives_are_never_overwritten(self):
        self.draft()
        path, prefix = self.fence()
        start_path = self.root / 'reader-a-review-start.json'
        before = start_path.read_bytes()
        with self.assertRaises(FileExistsError):
            make_start(self.ctx, 'a', path, prefix)
        self.assertEqual(start_path.read_bytes(), before)

    def test_earlier_review_answer_evidence_and_receipt_hash_rejected(self):
        self.draft()
        path, prefix = self.fence()
        save(self.ctx.work('a', 'final'), self.document('a', 'review', 20))
        snapshot(self.root, 'a', 'review')
        doc = self.document('a', 'review', 23)
        doc['answers'][0]['answer'] = 'Second change to completed reviewed entry.'
        doc['evidence_units']['7']['text'] = 'Changed completed referent.'
        doc['self_review']['receipts'][0]['chunks'][0]['sha256'] = '0' * 64
        save(self.ctx.work('a', 'final'), doc)
        self.assertFalse(snapshot(self.root, 'a', 'review')['pass'])
        self.assertFalse(verify_payloads(self.ctx, 'a', path, prefix + self.payload_outputs())['pass'])

    def test_partial_review_cannot_be_certified_complete(self):
        self.draft()
        path, prefix = self.fence()
        save(self.ctx.work('a', 'final'), self.document('a', 'review', 20))
        snapshot(self.root, 'a', 'review')
        self.assertFalse(verify_payloads(self.ctx, 'a', path, prefix + self.payload_outputs())['pass'])

    def test_distinct_reader_question_bank_and_explicit_parent_provenance_path_roles(self):
        self.assertNotIn(str(self.root / 'questions.json'), self.manifest['sole_game_data_files'])
        self.assertIn(str(self.root / 'reader-questions-final.json'), self.manifest['sole_game_data_files'])
        self.assertEqual(runtime_provenance_path(self.ctx), self.root.parent / 'neutral-parent-provenance-not-opened.json')
        self.assertFalse(runtime_provenance_path(self.ctx).exists())
        reader_doc = load(self.root / 'reader-questions-final.json')
        reader_doc['questions'][0]['unknown_question'].append('Changed frozen record.')
        save(self.root / 'reader-questions-final.json', reader_doc)
        with self.assertRaisesRegex(ValueError, 'differ from the frozen'):
            Context(self.root)


if __name__ == '__main__':
    unittest.main()
