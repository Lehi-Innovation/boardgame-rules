"""Synthetic own-record transport tests; no source facts or semantic results."""
import sys
sys.dont_write_bytecode = True
import hashlib
import json
import unittest
from source_units import review_display_record, unit_display_blocks


class ReviewDisplayTests(unittest.TestCase):
    def setUp(self):
        self.question = {'id': 'record/雪~é', 'question': 'Which label is recorded?',
                         'unknown_question_field': {'labels': ['Ω', None, False]}}
        self.answer = {'id': self.question['id'], 'literal_question': self.question['question'],
                       'answer': 'Unchecked text.', 'unknown_answer_field': {'x': [1, 2.5, True]}}

    def render(self, pool=None):
        return review_display_record(self.question, self.answer, pool)

    def test_complete_records_unknown_fields_and_independent_snapshots(self):
        self.answer['clauses'] = [{'arbitrary': {'note': 'Preserve every character.\r\n'}}]
        got = self.render()
        self.assertEqual(got['payload']['complete_original_question'], self.question)
        self.assertEqual(got['payload']['complete_original_answer'], self.answer)
        self.assertEqual(got['payload']['explicitly_referenced_shared_evidence'], [])
        self.answer['unknown_answer_field']['x'].append('later mutation')
        self.question['unknown_question_field']['labels'].append('later mutation')
        self.assertNotEqual(got['payload']['complete_original_answer'], self.answer)
        self.assertNotEqual(got['payload']['complete_original_question'], self.question)
        self.assertEqual(json.loads(got['text']), got['payload'])

    def test_id_and_literal_association_are_exact(self):
        for field, replacement in [('id', 'record/雪~e'),
                                   ('literal_question', 'Which label is recorded? ')]:
            with self.subTest(field=field):
                answer = dict(self.answer, **{field: replacement})
                with self.assertRaises(ValueError):
                    review_display_record(self.question, answer)
        with self.assertRaises(ValueError):
            review_display_record(self.question, [])

    def test_dictionary_numeric_and_unicode_ids_keep_reference_types_and_paths(self):
        self.answer['evidence_refs'] = [7, '7', '雪/~é']
        self.answer['clauses'] = [{'field/~雪': {'evidence_ids': [7]}}]
        pool = {'7': {'text': 'Full first unit.', 'unknown': {'x': [None, False]}},
                '雪/~é': {'text': 'Full second unit.'}, 'unlinked': {'text': 'Other unit.'}}
        original_pool = json.loads(json.dumps(pool))
        units = self.render(pool)['payload']['explicitly_referenced_shared_evidence']
        by_key = {u['pool_reference']: u for u in units}
        self.assertEqual(set(by_key), {'7', '雪/~é'})
        self.assertEqual(by_key['7']['original_unit'], pool['7'])
        self.assertEqual(by_key['7']['references'], [
            {'value': 7, 'path': '/clauses/0/field~1~0雪/evidence_ids/0'},
            {'value': 7, 'path': '/evidence_refs/0'},
            {'value': '7', 'path': '/evidence_refs/1'}])
        self.assertEqual(by_key['雪/~é']['pool_path'], '/evidence_units/雪~1~0é')
        self.assertEqual(by_key['雪/~é']['references'],
                         [{'value': '雪/~é', 'path': '/evidence_refs/2'}])
        self.assertEqual(pool, original_pool)

    def test_list_pool_uses_number_or_id_and_retains_every_field(self):
        self.answer['evidence'] = ['12', 'Δ/entry', 2.5]
        pool = [{'number': 12, 'id': 'secondary-label', 'text': 'Numeric unit.', 'extra': [False]},
                {'id': 'Δ/entry', 'text': 'Unicode unit.'},
                {'number': '2.5', 'text': 'Fractional unit.'},
                {'number': 99, 'text': 'Unreferenced unit.'}]
        got = self.render(pool)
        units = got['payload']['explicitly_referenced_shared_evidence']
        self.assertEqual([u['original_unit'] for u in units], pool[:3])
        self.assertEqual([u['pool_reference'] for u in units], [12, 'Δ/entry', '2.5'])
        self.assertEqual([u['pool_path'] for u in units],
                         ['/evidence_units/0', '/evidence_units/1', '/evidence_units/2'])
        self.assertEqual([u['references'][0]['value'] for u in units], ['12', 'Δ/entry', 2.5])

    def test_numeric_dictionary_keys_are_preserved_without_rewriting(self):
        self.answer['evidence_refs'] = ['8', 8]
        unit = self.render({8: {'text': 'Complete unit.'}})['payload'][
            'explicitly_referenced_shared_evidence'][0]
        self.assertEqual(unit['pool_reference'], 8)
        self.assertIs(type(unit['pool_reference']), int)
        self.assertEqual([ref['value'] for ref in unit['references']], ['8', 8])

    def test_no_unreferenced_units_or_other_records_are_attached(self):
        pool = {'alpha': {'text': 'Other record material.'}, 'beta': {'text': 'Unused unit.'}}
        self.assertEqual(self.render(pool)['payload']['explicitly_referenced_shared_evidence'], [])
        self.answer['evidence_ids'] = ['beta']
        got = self.render(pool)
        self.assertEqual([u['original_unit'] for u in got['payload'][
            'explicitly_referenced_shared_evidence']], [pool['beta']])
        self.assertNotIn('Other record material.', got['text'])

    def test_missing_explicit_references_fail_with_or_without_pool(self):
        for field in ('evidence_refs', 'evidence_ids', 'evidence'):
            for pool in (None, {}, [], {'other': {'text': 'Unused.'}}):
                with self.subTest(field=field, pool=pool):
                    self.answer[field] = ['not-present']
                    with self.assertRaises(ValueError):
                        self.render(pool)
                    del self.answer[field]

    def test_ambiguous_normalized_dictionary_or_list_references_fail(self):
        self.answer['evidence_refs'] = ['4']
        for pool in ({4: {'text': 'One.'}, '4': {'text': 'Two.'}},
                     [{'number': 4, 'text': 'One.'}, {'id': '4', 'text': 'Two.'}]):
            with self.subTest(pool=pool):
                with self.assertRaises(ValueError):
                    self.render(pool)

    def test_inline_literals_are_preserved_without_unmarked_reference_inference(self):
        self.answer['evidence'] = [{'id': 'not-a-ref', 'text': 'Literal content.',
                                    'source': {'number': 123, 'quote': 'Original quotation.'}}]
        self.answer['id_like_text'] = 'not-a-ref'
        got = self.render()
        self.assertEqual(got['payload']['complete_original_answer'], self.answer)
        self.assertEqual(got['payload']['explicitly_referenced_shared_evidence'], [])

    def test_nested_explicit_ref_inside_inline_material_is_still_resolved(self):
        self.answer['evidence'] = [{'text': 'Literal content.', 'evidence_refs': ['linked']}]
        unit = self.render({'linked': {'text': 'Full unit.'}})['payload'][
            'explicitly_referenced_shared_evidence'][0]
        self.assertEqual(unit['references'],
                         [{'value': 'linked', 'path': '/evidence/0/evidence_refs/0'}])

    def test_intentionally_false_text_and_wrong_spans_are_preserved(self):
        self.answer['answer'] = 'The deliberately false claim is that two plus two equals five.'
        self.answer['evidence_refs'] = ['wrong-text']
        pool = {'wrong-text': {'text': 'A deliberately incorrect quotation: five equals six.',
                               'source_span': {'start': -19, 'end': -2},
                               'unverified': True}}
        got = self.render(pool)
        self.assertEqual(got['payload']['complete_original_answer'], self.answer)
        self.assertEqual(got['payload']['explicitly_referenced_shared_evidence'][0][
            'original_unit'], pool['wrong-text'])
        self.assertNotIn('correct', set(got))

    def test_canonical_utf8_hash_counts_and_complete_bounded_display(self):
        self.answer['long_unknown_field'] = '雪é📄' * 3100
        got = self.render()
        expected = json.dumps(got['payload'], ensure_ascii=False, sort_keys=True,
                              separators=(',', ':'), allow_nan=False)
        self.assertEqual(got['text'], expected)
        self.assertIn('雪é📄', got['text'])
        self.assertEqual(got['characters'], len(expected))
        self.assertEqual(got['utf8_bytes'], len(expected.encode('utf-8')))
        self.assertEqual(got['sha256'], hashlib.sha256(expected.encode('utf-8')).hexdigest())
        blocks = list(unit_display_blocks(got, limit=2900))
        self.assertTrue(all(0 < block['characters'] <= 2900 for block in blocks))
        self.assertEqual(''.join(block['text'] for block in blocks), expected)
        self.assertTrue(all(block['source_start'] is None for block in blocks))

    def test_non_json_values_and_malformed_explicit_reference_fields_are_rejected(self):
        for invalid in (float('nan'), ('tuple',), {3: 'non-string object key'}):
            with self.subTest(invalid=invalid):
                self.answer['unknown_answer_field'] = invalid
                with self.assertRaises(ValueError):
                    self.render()
        self.answer['unknown_answer_field'] = None
        for invalid in ('scalar-ref', [True], [None], [{'id': 'object-ref'}]):
            with self.subTest(invalid=invalid):
                self.answer['evidence_refs'] = invalid
                with self.assertRaises(ValueError):
                    self.render()


if __name__ == '__main__':
    unittest.main()
