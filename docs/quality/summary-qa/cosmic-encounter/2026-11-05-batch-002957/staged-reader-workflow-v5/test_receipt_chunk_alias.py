"""Neutral faithful alias tests; actual-presence matching remains unchanged."""
import copy
import json
from pathlib import Path
import unittest
import test_staged_workflow as base
from snapshot_stage import snapshot
from verify_review_payloads import declared_receipt_chunks, verify_payloads


class ReceiptAliasTests(base.StagedTests):
    def receipts(self):
        receipts = base.StagedTests.receipts(self)
        mode = getattr(self, 'receipt_mode', 'alias')
        for index, receipt in enumerate(receipts):
            if mode == 'alias' or mode == 'mixed' and index % 2 == 0:
                receipt['displayed_chunks'] = receipt.pop('chunks')
            elif mode == 'equal_both':
                receipt['displayed_chunks'] = copy.deepcopy(receipt['chunks'])
            elif mode == 'conflicting_both':
                receipt['displayed_chunks'] = copy.deepcopy(receipt['chunks'])
                receipt['displayed_chunks'][0]['sha256'] = '0' * 64
            elif mode == 'wrong_hash':
                receipt['displayed_chunks'] = receipt.pop('chunks')
                receipt['displayed_chunks'][0]['sha256'] = '0' * 64
        return receipts

    def test_displayed_chunks_alias_exact_ranges_original_key_and_visibility(self):
        runtime, prefix = self.complete()
        before = self.ctx.work('a', 'final').read_bytes()
        result = verify_payloads(self.ctx, 'a', runtime, prefix + self.payload_outputs())
        self.assertTrue(result['payload_delivery_pass'], result)
        declared = json.loads(before)['self_review']['receipts']
        for record, receipt in zip(result['payloads'], declared):
            self.assertEqual(record['original_receipt_key'], 'displayed_chunks')
            self.assertEqual(record['original_receipt_keys_present'], ['displayed_chunks'])
            self.assertEqual([{key: chunk[key] for key in ('start', 'end', 'sha256')} for chunk in record['chunks']],
                             receipt['displayed_chunks'])
        self.assertEqual(len(result['payloads'][0]['chunks']), 2)
        self.assertEqual(before, self.ctx.work('a', 'final').read_bytes())

    def test_identical_simultaneous_declarations_accepted_without_rewrite(self):
        self.receipt_mode = 'equal_both'
        runtime, prefix = self.complete()
        result = verify_payloads(self.ctx, 'a', runtime, prefix + self.payload_outputs())
        self.assertTrue(result['payload_delivery_pass'], result)
        self.assertEqual(result['payloads'][0]['original_receipt_key'], 'chunks')
        self.assertEqual(result['payloads'][0]['original_receipt_keys_present'], ['chunks', 'displayed_chunks'])

    def test_conflicting_simultaneous_declarations_rejected(self):
        self.receipt_mode = 'conflicting_both'
        runtime, prefix = self.complete()
        result = verify_payloads(self.ctx, 'a', runtime, prefix + self.payload_outputs())
        self.assertFalse(result['payload_delivery_pass'])
        self.assertIn('Conflicting chunks and displayed_chunks declarations', result['payloads'][0]['errors'])
        self.assertEqual(result['payloads'][0]['original_receipt_keys_present'], ['chunks', 'displayed_chunks'])

    def test_alias_hash_mismatch_not_excused_by_actual_visible_text(self):
        self.receipt_mode = 'wrong_hash'
        runtime, prefix = self.complete()
        result = verify_payloads(self.ctx, 'a', runtime, prefix + self.payload_outputs())
        self.assertFalse(result['payload_delivery_pass'])
        self.assertIn('Chunk hash mismatch', result['payloads'][0]['errors'])

    def test_computed_only_and_pre_fence_alias_receipts_still_fail_visibility(self):
        runtime, prefix = self.complete()
        self.assertFalse(verify_payloads(self.ctx, 'a', runtime, prefix)['payload_delivery_pass'])
        # Same exact payloads before the fence do not become later delivery.
        other = ReceiptAliasTests('test_displayed_chunks_alias_exact_ranges_original_key_and_visibility')
        other.setUp()
        try:
            other.draft()
            runtime, prefix = other.fence(prefix=other.payload_outputs(first=0))
            other.review()
            self.assertFalse(verify_payloads(other.ctx, 'a', runtime, prefix)['payload_delivery_pass'])
        finally:
            other.doCleanups()

    def test_alias_does_not_relax_whole_display_or_bank_order(self):
        runtime, prefix = self.complete()
        self.assertFalse(verify_payloads(self.ctx, 'a', runtime, prefix + self.payload_outputs(whole=True))['payload_delivery_pass'])
        rows = [json.loads(row) for row in self.payload_outputs().splitlines()]
        outputs = [row['payload']['output'] for row in reversed(rows)]
        reordered = b''.join(base.line(20 + index, output) for index, output in enumerate(outputs))
        self.assertFalse(verify_payloads(self.ctx, 'a', runtime, prefix + reordered)['payload_delivery_pass'])

    def test_selection_preserves_list_identity_types_unknown_fields_and_no_fallback(self):
        chunks = [{'start': 0, 'end': 3, 'sha256': 'a' * 64, 'unknown': ['雪', False]}]
        key, selected = declared_receipt_chunks({'displayed_chunks': chunks})
        self.assertEqual(key, 'displayed_chunks')
        self.assertIs(selected, chunks)
        with self.assertRaises(ValueError):
            declared_receipt_chunks({'chunks': None, 'displayed_chunks': chunks})
        different_type = copy.deepcopy(chunks)
        different_type[0]['start'] = 0.0
        with self.assertRaises(ValueError):
            declared_receipt_chunks({'chunks': chunks, 'displayed_chunks': different_type})
        different_unknown = copy.deepcopy(chunks)
        different_unknown[0]['unknown'].append(None)
        with self.assertRaises(ValueError):
            declared_receipt_chunks({'chunks': chunks, 'displayed_chunks': different_unknown})

    def test_mixed_original_receipt_keys_are_recorded_per_entry(self):
        self.receipt_mode = 'mixed'
        runtime, prefix = self.complete()
        result = verify_payloads(self.ctx, 'a', runtime, prefix + self.payload_outputs())
        self.assertTrue(result['payload_delivery_pass'], result)
        self.assertEqual([record['original_receipt_key'] for record in result['payloads']],
                         ['displayed_chunks' if index % 2 == 0 else 'chunks' for index in range(23)])

    def test_full_chunk_validation_and_matching_block_byte_identical_to_v4(self):
        current = Path(__file__).with_name('verify_review_payloads.py').read_text()
        previous = (Path(__file__).resolve().parent.parent / 'staged-reader-workflow-v4' / 'verify_review_payloads.py').read_text()
        start = '            if not isinstance(chunks, list) or not chunks:\n'
        end = '        except (ValueError, KeyError, TypeError, AttributeError) as exc:\n'
        current_block = current[current.index(start):current.index(end, current.index(start))]
        previous_block = previous[previous.index(start):previous.index(end, previous.index(start))]
        self.assertEqual(current_block, previous_block)


def load_tests(loader, tests, pattern):
    return unittest.TestSuite(ReceiptAliasTests(name) for name in ReceiptAliasTests.__dict__
                              if name.startswith('test_'))


if __name__ == '__main__':
    unittest.main()
