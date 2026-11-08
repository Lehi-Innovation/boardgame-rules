"""Neutral stage-label-only fixtures, including old report byte compatibility."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import unittest
import test_staged_workflow as base
import test_terminal_draft_deviation as deviation
from bind_terminal_draft_deviation import bind_terminal_deviation
from correct_stage_label import correct_stage_label
from correct_stage_metadata import build_resolution
from snapshot_stage import snapshot
from staged_common import checked_archives, closed_draft, load, sha
from validate_staged_history import validate_history
from verify_review_payloads import verify_payloads


class StageLabelCorrectionTests(deviation.TerminalDeviationTests):
    def wrong_review_label(self, count=23):
        self.draft()
        runtime, prefix = self.fence()
        if count == 23:
            base.save(self.ctx.work('a', 'final'), self.document('a', 'review', 20))
            self.assertTrue(snapshot(self.root, 'a', 'review')['pass'])
        good = self.document('a', 'review', count)
        bad = copy.deepcopy(good)
        bad['stage'] = 'reviewing' if count == 23 else 'review_complete'
        base.save(self.ctx.work('a', 'final'), bad)
        failure = snapshot(self.root, 'a', 'review')
        self.assertEqual(failure['errors'], ['Incorrect stage label'])
        number = 2 if count == 23 else 1
        original = self.root / ('reader-a-review-batch-' + format(number, '02') + '.json')
        structure = original.with_name(original.stem + '-structure.json')
        return good, original, structure, runtime, prefix

    def finish_other_reader(self):
        self.draft('b')
        self.fence('b')
        self.review('b')

    def test_terminal_label_only_resolution_full_history_and_delivery(self):
        good, original, structure, runtime, prefix = self.wrong_review_label()
        before = (original.read_bytes(), structure.read_bytes())
        base.save(self.ctx.work('a', 'final'), good)
        result = correct_stage_label(self.root, 'a', 'review', 2)
        self.assertTrue(result['pass'], result)
        self.assertTrue(result['no_factual_changes'])
        self.assertEqual(result['permitted_change_fields'], ['/stage'])
        self.assertEqual(result['expected_stage_label'], 'review_complete')
        self.assertEqual(result['original_failed_report_sha256'], sha(before[1]))
        self.finish_other_reader()
        history = validate_history(self.root)
        self.assertTrue(history['pass'], history)
        self.assertTrue(history['content_completion_pass'])
        record = history['readers'][0]['stages']['review'][-1]
        self.assertFalse(record['reported_pass'])
        self.assertEqual(record['original_errors'], ['Incorrect stage label'])
        self.assertEqual(record['metadata_resolution_status'], 'stage_label_only_resolved')
        self.assertEqual(record['stage_label_resolution_status'], 'stage_label_only_resolved')
        self.assertTrue(record['effective_pass'])
        self.assertEqual(record['effective_path'], result['corrected_snapshot_path'])
        terminal = history['readers'][0]['effective_terminals']['review']
        self.assertEqual(terminal['sha256'], result['corrected_snapshot_sha256'])
        self.assertEqual(terminal['stage_label_resolution_status'], 'stage_label_only_resolved')
        self.assertTrue(verify_payloads(self.ctx, 'a', runtime, prefix + self.payload_outputs())['payload_delivery_pass'])
        self.assertEqual(before, (original.read_bytes(), structure.read_bytes()))
        final = self.ctx.work('a', 'final')
        final.write_bytes(final.read_bytes() + b' ')
        self.assertFalse(validate_history(self.root)['content_completion_pass'])

    def test_next_batch_compares_effective_label_corrected_prior(self):
        good, original, structure, _, _ = self.wrong_review_label(count=20)
        base.save(self.ctx.work('a', 'final'), good)
        result = correct_stage_label(self.root, 'a', 'review', 1)
        self.assertTrue(result['pass'], result)
        base.save(self.ctx.work('a', 'final'), self.document('a', 'review', 23))
        next_batch = snapshot(self.root, 'a', 'review')
        self.assertTrue(next_batch['pass'], next_batch)
        self.assertEqual(next_batch['sequence'], 2)
        self.assertEqual(next_batch['previous_effective_snapshot_path'], result['corrected_snapshot_path'])
        self.assertEqual(next_batch['previous_metadata_resolution_status'], 'stage_label_only_resolved')
        self.assertFalse(load(structure)['pass'])
        self.finish_other_reader()
        self.assertTrue(validate_history(self.root)['content_completion_pass'])

    def test_reject_answer_evidence_receipt_and_unknown_changes(self):
        good, original, structure, _, _ = self.wrong_review_label()
        preserved = (original.read_bytes(), structure.read_bytes())
        mutations = [lambda d: d['answers'][0].update(answer='Illicit neutral value.'),
                     lambda d: d['evidence_units']['7'].update(text='Illicit neutral unit.'),
                     lambda d: d['unknown_output'].update(extra=False),
                     lambda d: d['self_review']['receipts'][0].update(payload_sha256='0' * 64),
                     lambda d: d['unknown_output']['keep'].__setitem__(3, 0)]
        for mutate in mutations:
            proposed = copy.deepcopy(good)
            mutate(proposed)
            base.save(self.ctx.work('a', 'final'), proposed)
            result = correct_stage_label(self.root, 'a', 'review', 2)
            self.assertFalse(result['pass'])
            self.assertIn('Non-stage JSON values changed', result['errors'])
            self.assertFalse(result['no_factual_changes'])
        base.save(self.ctx.work('a', 'final'), good)
        self.assertTrue(correct_stage_label(self.root, 'a', 'review', 2)['pass'])
        items, errors = checked_archives(self.ctx, 'a', 'review')
        self.assertFalse(errors, errors)
        self.assertEqual(len(items[-1][2]['_stage_label_correction_attempts']), 6)
        self.assertEqual(preserved, (original.read_bytes(), structure.read_bytes()))

    def test_label_fix_retains_bound_draft_workflow_failure(self):
        self.terminal_deviation()
        bind_terminal_deviation(self.root, 'a')
        runtime, prefix = self.fence()
        base.save(self.ctx.work('a', 'final'), self.document('a', 'review', 20))
        self.assertTrue(snapshot(self.root, 'a', 'review')['pass'])
        good = self.document('a', 'review', 23)
        bad = copy.deepcopy(good)
        bad['stage'] = 'reviewing'
        base.save(self.ctx.work('a', 'final'), bad)
        self.assertEqual(snapshot(self.root, 'a', 'review')['errors'], ['Incorrect stage label'])
        base.save(self.ctx.work('a', 'final'), good)
        self.assertTrue(correct_stage_label(self.root, 'a', 'review', 2)['pass'])
        self.finish_other_reader()
        history = validate_history(self.root)
        self.assertTrue(history['content_completion_pass'], history)
        self.assertFalse(history['workflow_conformance_pass'])
        self.assertFalse(history['pass'])
        self.assertFalse(history['workflow_deviation_factual_grade_cap'])
        proof = verify_payloads(self.ctx, 'a', runtime, prefix + self.payload_outputs())
        self.assertTrue(proof['payload_delivery_pass'], proof)
        self.assertFalse(proof['pass'])

    def test_terminal_draft_label_correction_closes_effective_bytes(self):
        base.save(self.ctx.work('a', 'draft'), self.document('a', 'input', 0))
        snapshot(self.root, 'a', 'input')
        for count in (10, 20):
            base.save(self.ctx.work('a', 'draft'), self.document('a', 'draft', count))
            snapshot(self.root, 'a', 'draft')
        good = self.document('a', 'draft', 23)
        bad = copy.deepcopy(good)
        bad['stage'] = 'drafting'
        base.save(self.ctx.work('a', 'draft'), bad)
        self.assertEqual(snapshot(self.root, 'a', 'draft')['errors'], ['Incorrect stage label'])
        base.save(self.ctx.work('a', 'draft'), good)
        result = correct_stage_label(self.root, 'a', 'draft', 3)
        self.assertTrue(result['pass'], result)
        path, draft = closed_draft(self.ctx, 'a')
        self.assertEqual(str(path), result['corrected_snapshot_path'])
        self.fence()
        self.review()
        self.finish_other_reader()
        self.assertTrue(validate_history(self.root)['content_completion_pass'])

    def test_old_v2_v3_continuation_reports_recompute_identically(self):
        for version in ('v2', 'v3'):
            fixture = StageLabelCorrectionTests('test_next_batch_compares_effective_label_corrected_prior')
            fixture.setUp()
            try:
                fixture.draft()
                fixture.fence()
                good = fixture.document('a', 'review', 20)
                bad = copy.deepcopy(good)
                del bad['continuation']
                base.save(fixture.ctx.work('a', 'final'), bad)
                self.assertEqual(snapshot(fixture.root, 'a', 'review')['errors'], ['Incorrect continuation metadata'])
                base.save(fixture.ctx.work('a', 'final'), good)
                old_script = Path(__file__).resolve().parent.parent / ('staged-reader-workflow-' + version) / 'correct_stage_metadata.py'
                run = subprocess.run([sys.executable, '-B', str(old_script), str(fixture.root), 'a', 'review', '1'],
                                     text=True, capture_output=True)
                self.assertEqual(run.returncode, 0, run.stderr)
                original = fixture.root / 'reader-a-review-batch-01.json'
                corrected = fixture.root / 'reader-a-review-batch-01-metadata-corrected-01.json'
                saved_report = fixture.root / 'reader-a-review-batch-01-metadata-resolution-01.json'
                saved_bytes = saved_report.read_bytes()
                recomputed = build_resolution(fixture.ctx, 'a', 'review', 1, original, corrected, 1)
                self.assertEqual(load(saved_report), recomputed)
                rendered = (json.dumps(recomputed, indent=2, ensure_ascii=False, allow_nan=False) + '\n').encode()
                self.assertEqual(saved_bytes, rendered)
                final = fixture.document('a', 'review', 23)
                wrong = copy.deepcopy(final)
                wrong['stage'] = 'reviewing'
                base.save(fixture.ctx.work('a', 'final'), wrong)
                self.assertEqual(snapshot(fixture.root, 'a', 'review')['errors'], ['Incorrect stage label'])
                base.save(fixture.ctx.work('a', 'final'), final)
                self.assertTrue(correct_stage_label(fixture.root, 'a', 'review', 2)['pass'])
                self.assertFalse(checked_archives(fixture.ctx, 'a', 'review')[1])
                self.assertEqual(saved_bytes, saved_report.read_bytes())
            finally:
                fixture.doCleanups()

    def test_only_stage_error_exact_label_and_success_immutable(self):
        good, original, structure, _, _ = self.wrong_review_label()
        wrong = copy.deepcopy(good)
        wrong['stage'] = 'draft_complete'
        base.save(self.ctx.work('a', 'final'), wrong)
        self.assertFalse(correct_stage_label(self.root, 'a', 'review', 2)['pass'])
        base.save(self.ctx.work('a', 'final'), good)
        result = correct_stage_label(self.root, 'a', 'review', 2)
        self.assertTrue(result['pass'])
        resolution = self.root / 'reader-a-review-batch-02-stage-label-resolution-02.json'
        before = resolution.read_bytes()
        with self.assertRaises(FileExistsError):
            correct_stage_label(self.root, 'a', 'review', 2)
        self.assertEqual(before, resolution.read_bytes())

    def test_malformed_proposal_archived_and_binding_tamper_rejected(self):
        good, original, structure, _, _ = self.wrong_review_label()
        raw = b'{INVALID neutral proposal}\n'
        self.ctx.work('a', 'final').write_bytes(raw)
        self.assertFalse(correct_stage_label(self.root, 'a', 'review', 2)['pass'])
        corrected = self.root / 'reader-a-review-batch-02-stage-label-corrected-01.json'
        self.assertEqual(corrected.read_bytes(), raw)
        base.save(self.ctx.work('a', 'final'), good)
        self.assertTrue(correct_stage_label(self.root, 'a', 'review', 2)['pass'])
        corrected = self.root / 'reader-a-review-batch-02-stage-label-corrected-02.json'
        corrected.write_bytes(corrected.read_bytes() + b' ')
        self.assertTrue(checked_archives(self.ctx, 'a', 'review')[1])

    def test_label_only_cli_and_original_failure_preserved(self):
        good, original, structure, _, _ = self.wrong_review_label()
        base.save(self.ctx.work('a', 'final'), good)
        run = subprocess.run([sys.executable, '-B', str(Path(__file__).with_name('correct_stage_label.py')),
                              str(self.root), 'a', 'review', '2'], text=True, capture_output=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertTrue(json.loads(run.stdout)['pass'])
        self.assertFalse(load(structure)['pass'])
        self.assertEqual(load(original)['stage'], 'reviewing')

    def test_label_fix_cannot_resolve_additional_original_error(self):
        self.draft()
        self.fence()
        good = self.document('a', 'review', 20)
        bad = copy.deepcopy(good)
        bad['stage'] = 'wrong'
        del bad['continuation']
        base.save(self.ctx.work('a', 'final'), bad)
        self.assertFalse(snapshot(self.root, 'a', 'review')['pass'])
        bad['stage'] = good['stage']
        base.save(self.ctx.work('a', 'final'), bad)
        result = correct_stage_label(self.root, 'a', 'review', 1)
        self.assertFalse(result['pass'])
        self.assertIn('Original failure must concern the stage label only', result['errors'])


def load_tests(loader, tests, pattern):
    return unittest.TestSuite(StageLabelCorrectionTests(name) for name in StageLabelCorrectionTests.__dict__
                              if name.startswith('test_'))


if __name__ == '__main__':
    unittest.main()
