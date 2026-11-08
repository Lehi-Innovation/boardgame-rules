"""Neutral wrong-record clause regressions; no game rules or expected answers."""
import sys
sys.dont_write_bytecode = True
import unittest
from source_units import new_answer_record, new_clause_record, validate_clause_bindings


class ClauseBindingTests(unittest.TestCase):
    def setUp(self):
        self.doc = {'questions': [
            {'id': 'R002', 'question': 'For Áster, name the Orbit trigger; then state its timing.'},
            {'id': 'R007', 'question': 'For Birch, name the Drift trigger; then state its timing.'}]}

    def make_answer(self, index):
        answer = new_answer_record(self.doc['questions'][index])
        split = answer['literal_question'].index(';')
        answer['clauses'] = [new_clause_record(answer, 0, split),
                             new_clause_record(answer, split + 2, len(answer['literal_question']))]
        return answer

    def test_exact_unicode_spans_and_gapped_records(self):
        answers = [self.make_answer(i) for i in range(2)]
        self.assertTrue(validate_clause_bindings(self.doc, answers, complete=True))
        first = answers[0]['clauses'][0]
        self.assertEqual(first['literal_ask'], 'For Áster, name the Orbit trigger')
        self.assertEqual(set(first), {'literal_ask', 'question_start', 'question_end'})

    def test_correct_outer_record_does_not_hide_borrowed_clause(self):
        answer = self.make_answer(0)
        answer['clauses'][0] = self.make_answer(1)['clauses'][0]
        with self.assertRaises(ValueError):
            validate_clause_bindings(self.doc, [answer])

    def test_missing_altered_and_invalid_spans_are_rejected(self):
        for mutation in ('missing', 'paraphrase', 'range', 'boolean'):
            with self.subTest(mutation=mutation):
                answer = self.make_answer(0)
                if mutation == 'missing':
                    answer['clauses'] = []
                elif mutation == 'paraphrase':
                    answer['clauses'][0]['literal_ask'] = 'A different paraphrased ask'
                elif mutation == 'range':
                    answer['clauses'][0]['question_end'] = 1000
                else:
                    answer['clauses'][0]['question_start'] = False
                with self.assertRaises(ValueError):
                    validate_clause_bindings(self.doc, [answer])

    def test_bindings_do_not_generate_or_grade_semantic_answers(self):
        answer = self.make_answer(0)
        answer['answer'] = 'A deliberately unchecked semantic result.'
        self.assertTrue(validate_clause_bindings(self.doc, [answer]))
        with self.assertRaises(ValueError):
            validate_clause_bindings(self.doc, [answer], complete=True)


if __name__ == '__main__':
    unittest.main()
