"""Neutral continuation-only repair fixtures; no production files or runtimes."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import unittest
import test_staged_workflow as base
from correct_stage_metadata import correct_metadata
from snapshot_stage import snapshot
from staged_common import archives, checked_archives, closed_draft, load, sha
from validate_staged_history import validate_history
from verify_review_payloads import verify_payloads


class MetadataCorrectionTests(base.StagedTests):
    def failed_review(self, count=20, keep_unknown=False):
        self.draft()
        path, prefix = self.fence()
        if count == 23:
            base.save(self.ctx.work('a', 'final'), self.document('a', 'review', 20))
            self.assertTrue(snapshot(self.root, 'a', 'review')['pass'])
        good = self.document('a', 'review', count)
        original = copy.deepcopy(good)
        if keep_unknown:
            original['continuation'] = {'unknown_metadata': {'flag': False, 'typed': [1, '1']}}
            good['continuation']['unknown_metadata'] = copy.deepcopy(original['continuation']['unknown_metadata'])
        else:
            del original['continuation']
        base.save(self.ctx.work('a', 'final'), original)
        failed = snapshot(self.root, 'a', 'review')
        self.assertFalse(failed['pass'])
        self.assertEqual(failed['errors'], ['Incorrect continuation metadata'])
        number = 1 if count == 20 else 2
        original_path = self.root / ('reader-a-review-batch-' + format(number, '02') + '.json')
        structure_path = original_path.with_name(original_path.stem + '-structure.json')
        return good, original_path, structure_path, path, prefix

    def test_missing_continuation_resolution_and_next_batch_uses_effective_prior(self):
        good, original, structure, runtime, prefix = self.failed_review()
        raw_before, report_before = original.read_bytes(), structure.read_bytes()
        base.save(self.ctx.work('a', 'final'), good)
        resolution = correct_metadata(self.root, 'a', 'review', 1)
        self.assertTrue(resolution['pass'], resolution)
        self.assertTrue(resolution['no_factual_changes'])
        self.assertEqual(resolution['original_failed_report_sha256'], sha(report_before))
        items, errors = checked_archives(self.ctx, 'a', 'review')
        self.assertFalse(errors)
        self.assertEqual(items[0][0].name, 'reader-a-review-batch-01-metadata-corrected-01.json')
        self.assertFalse(items[0][2]['_original_structure_pass'])
        self.assertEqual(items[0][2]['_metadata_resolution_status'], 'continuation_metadata_only_resolved')
        base.save(self.ctx.work('a', 'final'), self.document('a', 'review', 23))
        next_batch = snapshot(self.root, 'a', 'review')
        self.assertTrue(next_batch['pass'], next_batch)
        self.assertEqual(next_batch['previous_effective_snapshot_path'], str(items[0][0]))
        self.assertEqual(len(archives(self.ctx, 'a', 'review')), 2)
        self.assertEqual(original.read_bytes(), raw_before)
        self.assertEqual(structure.read_bytes(), report_before)
        self.draft('b')
        self.fence('b')
        self.review('b')
        history = validate_history(self.root)
        self.assertTrue(history['pass'], history)
        stage = history['readers'][0]['stages']['review'][0]
        self.assertFalse(stage['reported_pass'])
        self.assertEqual(stage['original_errors'], ['Incorrect continuation metadata'])
        self.assertTrue(stage['effective_pass'])
        self.assertEqual(stage['path'], str(original))
        self.assertEqual(stage['original_structure_sha256'], sha(report_before))
        self.assertEqual(stage['metadata_correction_attempts'][0]['reported_pass'], True)
        self.assertTrue(verify_payloads(self.ctx, 'a', runtime, prefix + self.payload_outputs())['pass'])

    def test_terminal_review_corrected_bytes_and_hashes_are_explicit(self):
        good, original, structure, runtime, prefix = self.failed_review(count=23)
        base.save(self.ctx.work('a', 'final'), good)
        result = correct_metadata(self.root, 'a', 'review', 2)
        self.assertTrue(result['pass'], result)
        self.draft('b')
        self.fence('b')
        self.review('b')
        history = validate_history(self.root)
        self.assertTrue(history['pass'], history)
        terminal = history['readers'][0]['effective_terminals']['review']
        self.assertEqual(terminal['path'], result['corrected_snapshot_path'])
        self.assertEqual(terminal['sha256'], result['corrected_snapshot_sha256'])
        self.assertFalse(terminal['original_structure_pass'])
        self.assertEqual(terminal['metadata_resolution_status'], 'continuation_metadata_only_resolved')
        self.assertTrue(verify_payloads(self.ctx, 'a', runtime, prefix + self.payload_outputs())['pass'])
        final = self.ctx.work('a', 'final')
        final.write_bytes(final.read_bytes() + b' ')
        self.assertFalse(validate_history(self.root)['pass'])
        self.assertFalse(verify_payloads(self.ctx, 'a', runtime, prefix + self.payload_outputs())['pass'])

    def test_terminal_draft_correction_becomes_closed_draft_and_fence(self):
        base.save(self.ctx.work('a', 'draft'), self.document('a', 'input', 0))
        snapshot(self.root, 'a', 'input')
        for count in (10, 20):
            base.save(self.ctx.work('a', 'draft'), self.document('a', 'draft', count))
            snapshot(self.root, 'a', 'draft')
        good = self.document('a', 'draft', 23)
        broken = copy.deepcopy(good)
        del broken['continuation']
        base.save(self.ctx.work('a', 'draft'), broken)
        self.assertFalse(snapshot(self.root, 'a', 'draft')['pass'])
        base.save(self.ctx.work('a', 'draft'), good)
        result = correct_metadata(self.root, 'a', 'draft', 3)
        self.assertTrue(result['pass'], result)
        path, draft = closed_draft(self.ctx, 'a')
        self.assertEqual(str(path), result['corrected_snapshot_path'])
        runtime, prefix = self.fence()
        start = load(self.root / 'reader-a-review-start.json')
        self.assertEqual(start['draft_sha256'], sha(path.read_bytes()))
        self.review()
        self.assertTrue(verify_payloads(self.ctx, 'a', runtime, prefix + self.payload_outputs())['pass'])

    def test_answer_evidence_and_unknown_value_changes_rejected_and_preserved(self):
        good, original, structure, _, _ = self.failed_review()
        raw_before, report_before = original.read_bytes(), structure.read_bytes()
        mutations = [('answer', lambda d: d['answers'][0].update(answer='Illicit neutral answer change.')),
                     ('evidence', lambda d: d['evidence_units']['7'].update(text='Illicit neutral evidence change.')),
                     ('unknown', lambda d: d['unknown_output'].update(extra='Illicit unknown value.')),
                     ('receipts', lambda d: d['self_review']['receipts'][0].update(payload_sha256='0' * 64)),
                     ('instructions', lambda d: d['instructions_read'].update(extra='Illicit metadata.'))]
        for attempt, (name, mutate) in enumerate(mutations, 1):
            with self.subTest(name=name):
                proposed = copy.deepcopy(good)
                mutate(proposed)
                base.save(self.ctx.work('a', 'final'), proposed)
                result = correct_metadata(self.root, 'a', 'review', 1)
                self.assertFalse(result['pass'])
                self.assertFalse(result['no_factual_changes'])
                self.assertIn('Non-continuation JSON values changed', result['errors'])
                self.assertEqual(load(self.root / ('reader-a-review-batch-01-metadata-corrected-' + format(attempt, '02') + '.json')), proposed)
        base.save(self.ctx.work('a', 'final'), good)
        self.assertTrue(correct_metadata(self.root, 'a', 'review', 1)['pass'])
        items, errors = checked_archives(self.ctx, 'a', 'review')
        self.assertFalse(errors, errors)
        self.assertEqual(len(items[0][2]['_metadata_correction_attempts']), 6)
        self.assertEqual(original.read_bytes(), raw_before)
        self.assertEqual(structure.read_bytes(), report_before)

    def test_unknown_continuation_fields_retained_exactly_and_type_changes_rejected(self):
        good, _, _, _, _ = self.failed_review(keep_unknown=True)
        changed = copy.deepcopy(good)
        changed['continuation']['unknown_metadata']['typed'][0] = 1.0
        base.save(self.ctx.work('a', 'final'), changed)
        result = correct_metadata(self.root, 'a', 'review', 1)
        self.assertFalse(result['pass'])
        self.assertIn('Unknown continuation fields changed', result['errors'])
        base.save(self.ctx.work('a', 'final'), good)
        result = correct_metadata(self.root, 'a', 'review', 1)
        self.assertTrue(result['pass'], result)
        self.assertEqual(load(self.ctx.work('a', 'final'))['continuation']['unknown_metadata'], good['continuation']['unknown_metadata'])

    def test_malformed_correction_archived_before_inspection_then_valid_retry(self):
        good, _, _, _, _ = self.failed_review()
        raw = b'{INVALID neutral proposal}\n'
        self.ctx.work('a', 'final').write_bytes(raw)
        result = correct_metadata(self.root, 'a', 'review', 1)
        self.assertFalse(result['pass'])
        self.assertEqual((self.root / 'reader-a-review-batch-01-metadata-corrected-01.json').read_bytes(), raw)
        base.save(self.ctx.work('a', 'final'), good)
        self.assertTrue(correct_metadata(self.root, 'a', 'review', 1)['pass'])

    def test_correction_and_resolution_tampering_rejected(self):
        good, _, _, _, _ = self.failed_review()
        base.save(self.ctx.work('a', 'final'), good)
        result = correct_metadata(self.root, 'a', 'review', 1)
        corrected = self.root / 'reader-a-review-batch-01-metadata-corrected-01.json'
        raw = corrected.read_bytes()
        corrected.write_bytes(raw + b' ')
        self.assertTrue(checked_archives(self.ctx, 'a', 'review')[1])
        corrected.write_bytes(raw)
        resolution = self.root / 'reader-a-review-batch-01-metadata-resolution-01.json'
        changed = load(resolution)
        changed['no_factual_changes'] = False
        base.save(resolution, changed)
        self.assertTrue(checked_archives(self.ctx, 'a', 'review')[1])

    def test_successful_resolution_not_overwritten_and_no_resampling(self):
        good, _, _, _, _ = self.failed_review()
        base.save(self.ctx.work('a', 'final'), good)
        self.assertTrue(correct_metadata(self.root, 'a', 'review', 1)['pass'])
        paths = [self.root / 'reader-a-review-batch-01-metadata-corrected-01.json',
                 self.root / 'reader-a-review-batch-01-metadata-resolution-01.json']
        before = [p.read_bytes() for p in paths]
        with self.assertRaises(FileExistsError):
            correct_metadata(self.root, 'a', 'review', 1)
        self.assertEqual(before, [p.read_bytes() for p in paths])
        self.assertEqual(len(archives(self.ctx, 'a', 'review')), 1)

    def test_correction_cannot_clear_additional_original_structural_failure(self):
        self.draft()
        self.fence()
        doc = self.document('a', 'review', 20)
        doc['stage'] = 'wrong-stage'
        del doc['continuation']
        base.save(self.ctx.work('a', 'final'), doc)
        self.assertFalse(snapshot(self.root, 'a', 'review')['pass'])
        doc['continuation'] = {'completed_count': 20, 'next_record_index_zero_based': 20, 'bank_complete': False}
        base.save(self.ctx.work('a', 'final'), doc)
        result = correct_metadata(self.root, 'a', 'review', 1)
        self.assertFalse(result['pass'])
        self.assertIn('Original failure must concern continuation metadata only', result['errors'])

    def test_correction_cli_uses_same_neutral_verification(self):
        good, original, structure, _, _ = self.failed_review()
        base.save(self.ctx.work('a', 'final'), good)
        run = subprocess.run([sys.executable, '-B', str(Path(__file__).with_name('correct_stage_metadata.py')),
                              str(self.root), 'a', 'review', '1'], capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        result = json.loads(run.stdout)
        self.assertTrue(result['pass'])
        self.assertEqual(result['sequence'], 1)
        self.assertEqual(result['correction_attempt'], 1)
        self.assertTrue(original.exists())
        self.assertFalse(load(structure)['pass'])


def load_tests(loader, tests, pattern):
    # Reuse neutral fixture helpers, but run inherited v1 checks only once via
    # test_staged_workflow.py in the combined suite.
    return unittest.TestSuite(MetadataCorrectionTests(name) for name in MetadataCorrectionTests.__dict__
                              if name.startswith('test_'))


if __name__ == '__main__':
    unittest.main()
