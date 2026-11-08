"""Neutral complete-draft deviation fixtures; no production data/runtime IO."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import unittest
import test_staged_workflow as base
from bind_terminal_draft_deviation import bind_terminal_deviation
from snapshot_stage import snapshot
from staged_common import checked_archives, closed_draft, load, sha
from validate_staged_history import validate_history
from verify_review_payloads import verify_payloads


class TerminalDeviationTests(base.StagedTests):
    def terminal_deviation(self, mutate=None, append_pool=False):
        base.save(self.ctx.work('a', 'draft'), self.document('a', 'input', 0))
        snapshot(self.root, 'a', 'input')
        for count in (10, 20):
            base.save(self.ctx.work('a', 'draft'), self.document('a', 'draft', count))
            self.assertTrue(snapshot(self.root, 'a', 'draft')['pass'])
        terminal = self.document('a', 'draft', 23)
        terminal['answers'][0]['answer'] = 'Neutral terminal self-revision.'
        terminal['answers'][0]['evidence_refs'] = ['7']
        if append_pool:
            terminal['evidence_units']['new-final-unit'] = {'text': 'Neutral appended complete unit.'}
            terminal['answers'][-1]['evidence_refs'] = ['new-final-unit']
        if mutate:
            mutate(terminal)
        base.save(self.ctx.work('a', 'draft'), terminal)
        report = snapshot(self.root, 'a', 'draft')
        self.assertFalse(report['pass'])
        self.original_answers = copy.deepcopy(terminal['answers'])
        self.pool = copy.deepcopy(terminal['evidence_units'])
        return terminal, report

    def finish_review(self):
        runtime, prefix = self.fence()
        self.review()
        self.draft('b')
        self.fence('b')
        self.review('b')
        return runtime, prefix

    def test_complete_terminal_selfrevision_content_true_workflow_false(self):
        terminal, failed = self.terminal_deviation(append_pool=True)
        original = self.root / 'reader-a-draft-batch-03.json'
        report_path = self.root / 'reader-a-draft-batch-03-structure.json'
        preserved = (original.read_bytes(), report_path.read_bytes())
        with self.assertRaises(ValueError):
            closed_draft(self.ctx, 'a')
        bound = bind_terminal_deviation(self.root, 'a')
        self.assertTrue(bound['binding_verified'])
        self.assertFalse(bound['immutable_prefix_pass'])
        self.assertFalse(bound['workflow_conformance_pass'])
        self.assertFalse(bound['original_structure_pass'])
        self.assertEqual(bound['question_count'], 23)
        self.assertEqual(bound['appended_evidence_paths'], ['/evidence_units/new-final-unit'])
        self.assertEqual(bound['earlier_answer_values_changed_ids'], [self.questions[0]['id']])
        self.assertEqual(len(bound['preserved_prior_drafts']), 2)
        self.assertTrue(bound['earlier_answer_differences'][0]['changed_paths_and_hashes'])
        path, draft = closed_draft(self.ctx, 'a')
        self.assertEqual(path, original)
        self.assertEqual(draft, terminal)
        runtime, prefix = self.finish_review()
        start = load(self.root / 'reader-a-review-start.json')
        self.assertEqual(start['draft_sha256'], sha(original.read_bytes()))
        self.assertFalse(start['draft_workflow_conformance_pass'])
        self.assertFalse(start['draft_immutable_prefix_pass'])
        self.assertEqual(start['draft_deviation_binding']['sha256'], sha((self.root / 'reader-a-terminal-draft-deviation.json').read_bytes()))
        history = validate_history(self.root)
        self.assertTrue(history['content_completion_pass'], history)
        self.assertFalse(history['workflow_conformance_pass'])
        self.assertFalse(history['pass'])
        self.assertFalse(history['overall_technical_pass'])
        self.assertEqual(history['factual_grading_question_count'], 23)
        self.assertFalse(history['workflow_deviation_factual_grade_cap'])
        draft_stage = history['readers'][0]['stages']['draft'][-1]
        self.assertFalse(draft_stage['reported_pass'])
        self.assertFalse(draft_stage['effective_pass'])
        self.assertTrue(draft_stage['content_integrity_pass'])
        self.assertFalse(draft_stage['workflow_conformance_pass'])
        self.assertEqual(draft_stage['original_errors'], ['Earlier completed values changed within stage'])
        proof = verify_payloads(self.ctx, 'a', runtime, prefix + self.payload_outputs())
        self.assertTrue(proof['payload_delivery_pass'], proof)
        self.assertFalse(proof['workflow_conformance_pass'])
        self.assertFalse(proof['pass'])
        self.assertEqual(preserved, (original.read_bytes(), report_path.read_bytes()))

    def test_pool_source_receipt_and_unknown_metadata_changes_rejected(self):
        mutations = [lambda d: d['evidence_units']['7'].update(text='Changed earlier unit.'),
                     lambda d: d['inputs_read'][0].update(sha256='0' * 64),
                     lambda d: d['instructions_read'].update(extra=True),
                     lambda d: d['unknown_output'].update(extra=True)]
        # Independent subfixtures, confined to the permitted tool directory.
        for mutate in mutations:
            fixture = TerminalDeviationTests('test_unbound_terminal_deviation_stays_rejected')
            fixture.setUp()
            try:
                fixture.terminal_deviation(mutate)
                with self.assertRaises(ValueError):
                    bind_terminal_deviation(fixture.root, 'a')
            finally:
                fixture.doCleanups()

    def test_unbound_terminal_deviation_stays_rejected(self):
        self.terminal_deviation()
        _, errors = checked_archives(self.ctx, 'a', 'draft')
        self.assertTrue(errors)
        with self.assertRaises(ValueError):
            closed_draft(self.ctx, 'a')

    def test_nonterminal_closure_rejected(self):
        base.save(self.ctx.work('a', 'draft'), self.document('a', 'input', 0))
        snapshot(self.root, 'a', 'input')
        base.save(self.ctx.work('a', 'draft'), self.document('a', 'draft', 10))
        snapshot(self.root, 'a', 'draft')
        doc = self.document('a', 'draft', 20)
        doc['answers'][0]['answer'] = 'Earlier neutral change.'
        base.save(self.ctx.work('a', 'draft'), doc)
        snapshot(self.root, 'a', 'draft')
        with self.assertRaises(ValueError):
            bind_terminal_deviation(self.root, 'a')

    def test_missing_records_and_unresolved_references_rejected(self):
        self.terminal_deviation(lambda d: d['answers'].pop())
        with self.assertRaises(ValueError):
            bind_terminal_deviation(self.root, 'a')

    def test_unresolved_explicit_reference_rejected(self):
        self.terminal_deviation(lambda d: d['answers'][0].update(evidence_refs=['missing-neutral-unit']))
        with self.assertRaises(ValueError):
            bind_terminal_deviation(self.root, 'a')

    def test_mutable_closed_draft_or_binding_rejected(self):
        self.terminal_deviation()
        bind_terminal_deviation(self.root, 'a')
        live = self.ctx.work('a', 'draft')
        original = live.read_bytes()
        live.write_bytes(original + b' ')
        with self.assertRaises(ValueError):
            closed_draft(self.ctx, 'a')
        live.write_bytes(original)
        binding = self.root / 'reader-a-terminal-draft-deviation.json'
        doc = load(binding)
        doc['workflow_conformance_pass'] = True
        base.save(binding, doc)
        with self.assertRaises(ValueError):
            closed_draft(self.ctx, 'a')

    def test_bound_draft_does_not_relax_review_prefix_immutability(self):
        self.terminal_deviation()
        bind_terminal_deviation(self.root, 'a')
        self.fence()
        base.save(self.ctx.work('a', 'final'), self.document('a', 'review', 20))
        self.assertTrue(snapshot(self.root, 'a', 'review')['pass'])
        doc = self.document('a', 'review', 23)
        doc['answers'][0]['answer'] = 'Illicit second review-prefix mutation.'
        base.save(self.ctx.work('a', 'final'), doc)
        report = snapshot(self.root, 'a', 'review')
        self.assertFalse(report['pass'])
        self.assertIn('Earlier completed values changed within stage', report['errors'])
        self.assertTrue(checked_archives(self.ctx, 'a', 'review')[1])

    def test_binding_cli_and_no_overwrite(self):
        self.terminal_deviation()
        run = subprocess.run([sys.executable, '-B', str(Path(__file__).with_name('bind_terminal_draft_deviation.py')),
                              str(self.root), 'a'], text=True, capture_output=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertFalse(json.loads(run.stdout)['workflow_conformance_pass'])
        before = (self.root / 'reader-a-terminal-draft-deviation.json').read_bytes()
        with self.assertRaises(FileExistsError):
            bind_terminal_deviation(self.root, 'a')
        self.assertEqual(before, (self.root / 'reader-a-terminal-draft-deviation.json').read_bytes())

    def test_review_fence_must_disclose_exact_binding(self):
        self.terminal_deviation()
        bind_terminal_deviation(self.root, 'a')
        self.fence()
        fence = self.root / 'reader-a-review-start.json'
        value = load(fence)
        del value['draft_deviation_binding']
        base.save(fence, value)
        base.save(self.ctx.work('a', 'final'), self.document('a', 'review', 20))
        self.assertFalse(snapshot(self.root, 'a', 'review')['pass'])


def load_tests(loader, tests, pattern):
    return unittest.TestSuite(TerminalDeviationTests(name) for name in TerminalDeviationTests.__dict__
                              if name.startswith('test_'))


if __name__ == '__main__':
    unittest.main()
