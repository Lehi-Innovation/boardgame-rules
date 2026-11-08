"""Synthetic neutral lookup cases; no game facts or question routing."""
import sys
sys.dont_write_bytecode = True
import unittest
from source_units import extract_heading_unit, heading_paths, validate_record


class HeadingLookupTests(unittest.TestCase):
    def test_earlier_prose_mention_is_not_selected(self):
        text = '## Introduction\n\nHarbor is mentioned here.\n\n## Harbor\n\nThe complete operation.\n\nException applies.\n'
        got = extract_heading_unit(text, 'harbor')
        self.assertTrue(got['unit']['text'].startswith('## Harbor'))
        self.assertIn('Exception applies.', got['unit']['text'])
        self.assertNotIn('Introduction', got['unit']['text'])
        self.assertTrue(validate_record(text, got))

    def test_duplicate_titles_require_full_path(self):
        text = '## North\n\n### Port\n\nFirst operation.\n\n## South\n\n### Port\n\nSecond operation.\n'
        with self.assertRaises(ValueError):
            extract_heading_unit(text, 'Port')
        got = extract_heading_unit(text, 'Port', ['South', 'Port'])
        self.assertIn('Second operation.', got['unit']['text'])
        self.assertNotIn('First operation.', got['unit']['text'])

    def test_substring_is_not_exact_title(self):
        text = '## Long Harbor\n\nComplete operation.\n'
        with self.assertRaises(ValueError):
            extract_heading_unit(text, 'Harbor')

    def test_numbered_governing_procedure_remains_complete(self):
        text = '## Procedure\n\n1. Begin.\n\n### Review\n\nCheck details.\n\n### End\n\nFinish.\n'
        got = extract_heading_unit(text, 'Review')
        self.assertIn('1. Begin.', got['unit']['text'])
        self.assertIn('Finish.', got['unit']['text'])

    def test_bare_title_cannot_supply_evidence(self):
        with self.assertRaises(ValueError):
            extract_heading_unit('## Harbor\n', 'Harbor')

    def test_deep_path_index_and_whitespace_case(self):
        text = '## Catalog\n\n### Group\n\n#### Entry A\n\nComplete body.\n'
        self.assertEqual(heading_paths(text)[-1]['path'], ['Catalog', 'Group', 'Entry A'])
        got = extract_heading_unit(text, ' entry  a ')
        self.assertIn('Complete body.', got['unit']['text'])


if __name__ == '__main__':
    unittest.main()
