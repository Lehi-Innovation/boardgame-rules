"""Neutral byte/Unicode receipt regressions; no game data or expected answers."""
import sys
sys.dont_write_bytecode = True
import unittest
import hashlib
from reader_receipt_offsets_v1 import normalize_offset_receipts


def receipt(raw, start, end):
    return {'start': start, 'end': end, 'sha256': hashlib.sha256(raw[start:end]).hexdigest()}


class OffsetTests(unittest.TestCase):
    def test_unicode_character_ranges_remain_unchanged(self):
        text = 'café Ω / 漢字'
        pieces = [(0, 5), (5, len(text))]
        chunks = [{'start': a, 'end': b, 'sha256': hashlib.sha256(text[a:b].encode()).hexdigest()}
                  for a, b in pieces]
        result = normalize_offset_receipts(text, chunks)
        self.assertEqual(result['original_offset_unit'], 'unicode_characters')
        self.assertEqual([(c['start'], c['end']) for c in result['chunks']], pieces)

    def test_byte_ranges_map_one_to_one_to_actual_unicode_pieces(self):
        text = 'café Ω / 漢字'
        raw = text.encode()
        split = len('café '.encode())
        result = normalize_offset_receipts(text, [receipt(raw, 0, split), receipt(raw, split, len(raw))])
        self.assertEqual(result['original_offset_unit'], 'utf8_bytes')
        self.assertEqual([(c['start'], c['end']) for c in result['chunks']], [(0, 5), (5, len(text))])
        self.assertFalse(result['actual_visibility_or_pre_save_timing_certified'])

    def test_cut_utf8_character_cannot_be_relabelled_as_a_valid_payload(self):
        text = 'a漢b'
        raw = text.encode()
        with self.assertRaises(ValueError):
            normalize_offset_receipts(text, [receipt(raw, 0, 2), receipt(raw, 2, len(raw))])

    def test_gap_wrong_hash_and_incomplete_eof_are_rejected(self):
        text = 'plain text'
        raw = text.encode()
        for chunks in ([receipt(raw, 0, 4)],
                       [receipt(raw, 0, 4), receipt(raw, 5, len(raw))],
                       [{'start': 0, 'end': len(raw), 'sha256': '0' * 64}]):
            with self.subTest(chunks=chunks), self.assertRaises(ValueError):
                normalize_offset_receipts(text, chunks)


if __name__ == '__main__':
    unittest.main()
