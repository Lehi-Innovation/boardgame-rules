"""Neutral later-lookup transport regression; no game facts or answer hints."""
import sys
sys.dont_write_bytecode = True
import unittest
from source_units import unit_display_blocks, extract_unit


class UnitDisplayTests(unittest.TestCase):
    def test_long_complete_unit_is_displayed_without_oversized_remainder(self):
        text = 'x' * 13750
        blocks = list(unit_display_blocks({'unit': {'start': 200, 'text': text}}))
        self.assertEqual([b['characters'] for b in blocks], [5800, 5800, 2150])
        self.assertEqual(''.join(b['text'] for b in blocks), text)
        self.assertEqual([(b['source_start'], b['source_end']) for b in blocks],
                         [(200, 6000), (6000, 11800), (11800, 13950)])

    def test_table_intro_header_and_row_are_all_displayed(self):
        text = '## Records\n\nShared convention.\n\n| Name | Value |\n|---|---|\n| Alpha | Detail |\n'
        record = extract_unit(text, text.index('Alpha'))
        blocks = list(unit_display_blocks(record))
        self.assertEqual([b['piece_of'] for b in blocks], ['introduction', 'header', 'row'])
        for block in blocks:
            self.assertEqual(text[block['source_start']:block['source_end']], block['text'])

    def test_invalid_display_bounds_and_absent_text_rejected(self):
        with self.assertRaises(ValueError):
            list(unit_display_blocks({'text': 'neutral'}, 6001))
        with self.assertRaises(ValueError):
            list(unit_display_blocks({'kind': 'unknown'}))


if __name__ == '__main__':
    unittest.main()
