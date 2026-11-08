"""Neutral record-association guard; no game facts, keys or expected answers."""
import sys
sys.dont_write_bytecode = True
import unittest
from source_units import question_batch, new_answer_record, validate_question_bindings


class QuestionBindingTests(unittest.TestCase):
    def setUp(self):
        self.doc = {'questions': [
            {'id': 'T001', 'question': 'What happens in the north room?'},
            {'id': 'T004', 'question': 'When does the south gate open?'},
            {'id': 'T009', 'question': 'Who owns the east ledger?'}]}

    def test_actual_record_order_survives_id_gaps(self):
        batch = question_batch(self.doc, 1, 2)
        self.assertEqual([q['id'] for q in batch], ['T004', 'T009'])
        self.assertEqual(batch[0]['question'], self.doc['questions'][1]['question'])

    def test_literal_binding_catches_right_id_wrong_ask(self):
        first = new_answer_record(self.doc['questions'][0])
        first['literal_question'] = self.doc['questions'][1]['question']
        with self.assertRaises(ValueError):
            validate_question_bindings(self.doc, [first])

    def test_literal_binding_catches_swapped_records(self):
        entries = [new_answer_record(q) for q in self.doc['questions']]
        entries[0], entries[1] = entries[1], entries[0]
        with self.assertRaises(ValueError):
            validate_question_bindings(self.doc, entries, complete=True)

    def test_no_answer_or_semantic_result_is_generated(self):
        first = new_answer_record(self.doc['questions'][0])
        self.assertEqual(set(first), {'id', 'literal_question'})
        first['answer'] = 'A deliberately unchecked semantic result.'
        self.assertTrue(validate_question_bindings(self.doc, [first]))
        with self.assertRaises(ValueError):
            validate_question_bindings(self.doc, [first], complete=True)

    def test_final_short_batch_and_invalid_prefix(self):
        self.assertEqual(len(question_batch(self.doc, 2, 10)), 1)
        self.assertEqual(question_batch(self.doc, 3, 10), [])
        with self.assertRaises(ValueError):
            question_batch(self.doc, 4)


if __name__ == '__main__':
    unittest.main()
