"""Synthetic neutral Markdown only; no rules, questions, keys or reader data."""
import sys
sys.dont_write_bytecode = True
import unittest
from source_units import extract_unit, validate_record, heading_index


class GenericUnitsTests(unittest.TestCase):
    def test_optional_span_labels_do_not_change_validation(self):
        text = "## Records\n\n| Label | Notes |\n|---|---|\n| Alpha | detail |\n"
        got = extract_unit(text, text.index("Alpha"))
        got["row"]["unit_id"] = "neutral-row"
        got["header"]["kind"] = "optional-label"
        got["fields"][0]["source_id"] = "neutral-source"
        self.assertTrue(validate_record(text, got))

    def test_literal_table_fields_and_duplicate_names(self):
        text = "## Records\n\n| Label | Owner | Owner |\n|---|---|---|\n| Alpha | Blue | Red |\n"
        got = extract_unit(text, text.index("Alpha"))
        self.assertEqual([x["value"] for x in got["fields"]], ["Alpha", "Blue", "Red"])
        self.assertEqual([x["column"] for x in got["fields"]], ["Label", "Owner", "Owner"])
        self.assertIn("|---|---|---|", got["header"]["text"])
        self.assertTrue(validate_record(text, got))

    def test_long_row_is_never_fixed_length(self):
        row = "| Alpha | " + "neutral detail " * 50 + "|"
        text = "## Records\n\n| Label | Notes |\n|---|---|\n" + row + "\n"
        got = extract_unit(text, text.index("Alpha"))
        self.assertEqual(got["row"]["text"], row)
        bad = dict(got, row=dict(got["row"], end=got["row"]["end"] - 5,
                                text=got["row"]["text"][:-5]))
        with self.assertRaises(ValueError):
            validate_record(text, bad)

    def test_escaped_pipe_unicode_and_crlf(self):
        text = "## 📄 Notes\r\n\r\n| Label | Notes |\r\n|---|---|\r\n  | Café | left \\| right |  \r\n"
        got = extract_unit(text, text.index("Café"))
        self.assertEqual(got["fields"][1]["value"], "left \\| right")
        self.assertEqual(text[got["row"]["start"]:got["row"]["end"]], got["row"]["text"])

    def test_column_mismatch_is_rejected(self):
        text = "## Records\n\n| Label | Notes |\n|---|---|\n| Alpha | detail | extra |\n"
        with self.assertRaises(ValueError):
            extract_unit(text, text.index("Alpha"))

    def test_heading_match_includes_the_whole_procedure(self):
        text = "## Prepare\n\n1. Select a group.\n2. Load its records.\n\n### Details\n\nRetain the labels.\n\n## Finish\n\nClose the file.\n"
        got = extract_unit(text, text.index("## Prepare"))
        self.assertEqual(got["unit"]["text"], text[:text.index("## Finish")].rstrip())
        self.assertTrue(validate_record(text, got))

    def test_single_step_expands_to_all_peer_steps(self):
        text = "## Process\n\n1. Select the file.\n2. Review each entry.\n3. Save the result.\n\n## Next\n\nOther text.\n"
        got = extract_unit(text, text.index("Select the file"))
        self.assertIn("2. Review each entry.", got["unit"]["text"])
        self.assertIn("3. Save the result.", got["unit"]["text"])

    def test_context_paragraph_keeps_prior_steps(self):
        text = "## Process\n\n1. Select the file.\n2. Review each entry.\n\nAdditional restrictions apply to the review.\n\n## Next\n"
        got = extract_unit(text, text.index("Additional restrictions"))
        self.assertIn("1. Select the file.", got["unit"]["text"])
        self.assertIn("2. Review each entry.", got["unit"]["text"])

    def test_nested_detail_keeps_its_governing_procedure(self):
        text = "## Process\n\n### Prepare\n\n1. Select a group.\n\n#### Detail\n\nUse the matching label.\n\n### Continue\n\nNext operation.\n"
        got = extract_unit(text, text.index("Use the matching"))
        self.assertIn("1. Select a group.", got["unit"]["text"])
        self.assertNotIn("Next operation", got["unit"]["text"])

    def test_long_nonprocedural_catalog_uses_complete_paragraph(self):
        text = "## Catalog\n\nA complete short definition.\n\n" + ("Neutral description. " * 400)
        got = extract_unit(text, text.index("A complete"))
        self.assertEqual(got["kind"], "paragraph")
        self.assertEqual(got["unit"]["text"], "A complete short definition.")

    def test_no_bare_heading_from_long_catalog(self):
        text = "## Catalog\n\n" + ("Neutral description. " * 400)
        with self.assertRaises(ValueError):
            extract_unit(text, 0)

    def test_modified_procedure_record_is_rejected(self):
        text = "## Process\n\n1. Select a group.\n2. Load records.\n"
        got = extract_unit(text, text.index("Select"))
        got["unit"] = dict(got["unit"], end=got["unit"]["end"] - 5,
                           text=got["unit"]["text"][:-5])
        with self.assertRaises(ValueError):
            validate_record(text, got)

    def test_heading_index_has_unicode_codepoint_offsets(self):
        text = "📄 prefix\n\n## Group\n\nText.\n"
        got = heading_index(text)[0]
        self.assertEqual(got["start"], text.index("## Group"))


if __name__ == "__main__":
    unittest.main()
