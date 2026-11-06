"""Synthetic neutral Markdown only; no evaluation data or game facts."""
import sys
sys.dont_write_bytecode = True
import unittest
from source_units import (table_units, validate_table_unit, paragraph_unit,
                          list_item_unit, validate_text_unit)


class SourceUnitsTests(unittest.TestCase):
    def test_long_complete_table_row_and_header(self):
        row = "| Entry Alpha | Team Blue | " + "neutral detail " * 25 + "|"
        text = "Shared context.\n\n| Label | Owner | Notes |\n|---|:---:|---:|\n" + row + "\n| Entry Beta | Team Red | short |\n"
        got = table_units(text, text.index("Entry Alpha"))
        self.assertEqual(got["row"]["text"], row)
        self.assertEqual(got["header"]["text"], "| Label | Owner | Notes |")
        self.assertEqual(got["cell_count"], 3)
        bad = dict(got["row"], end=got["row"]["end"] - 8,
                   text=got["row"]["text"][:-8])
        with self.assertRaises(ValueError):
            validate_table_unit(text, bad, got["header"])

    def test_escaped_pipe_unicode_and_crlf(self):
        text = "📄 note\r\n\r\n| Label | Notes |\r\n|---|---|\r\n  | Café | left \\| right |  \r\n"
        got = table_units(text, text.index("Café"))
        self.assertEqual(got["cell_count"], 2)
        self.assertEqual(got["row"]["text"], "| Café | left \\| right |")
        self.assertEqual(text[got["row"]["start"]:got["row"]["end"]], got["row"]["text"])

    def test_bad_column_count_rejected(self):
        text = "| Label | Notes |\n|---|---|\n| Alpha | detail | extra |\n"
        with self.assertRaises(ValueError):
            table_units(text, text.index("Alpha"))

    def test_optional_labels_do_not_change_boundary_validation(self):
        text = "| Label | Notes |\n|---|---|\n| Alpha | detail |\n"
        got = table_units(text, text.index("Alpha"))
        row = dict(got["row"], unit_id="neutral-id", kind="optional label")
        self.assertTrue(validate_table_unit(text, row, got["header"]))
        paragraph = "A neutral paragraph.\n\nAnother paragraph."
        item = dict(paragraph_unit(paragraph, 0), unit_id="another-id")
        self.assertTrue(validate_text_unit(paragraph, item, "paragraph"))

    def test_complete_multiline_paragraph(self):
        text = "Title\n\nFirst sentence continues\non another line with a condition.\n\nNext paragraph.\n"
        got = paragraph_unit(text, text.index("another"))
        self.assertEqual(got["text"], "First sentence continues\non another line with a condition.")
        self.assertTrue(validate_text_unit(text, got, "paragraph"))
        bad = dict(got, end=got["end"] - 11, text=got["text"][:-11])
        with self.assertRaises(ValueError):
            validate_text_unit(text, bad, "paragraph")

    def test_nested_item_and_indented_continuation(self):
        text = "- Parent item.\n  Continued text.\n  - Child item.\n\n    Continued child paragraph.\n- Next item.\n\nOutside paragraph.\n"
        parent = list_item_unit(text, text.index("Parent"))
        child = list_item_unit(text, text.index("Child"))
        self.assertEqual(parent["text"], text[:text.index("- Next")].rstrip())
        self.assertIn("Continued child paragraph.", child["text"])
        self.assertNotIn("Next item", child["text"])
        self.assertTrue(validate_text_unit(text, parent, "list_item"))
        self.assertTrue(validate_text_unit(text, child, "list_item"))


if __name__ == "__main__":
    unittest.main()
