"""Neutral characterization probes; accepted unsafe cases are findings, not approvals."""
import hashlib
import json
from pathlib import Path

from source_units import (unit, lines, cells, table_units, validate_table_unit,
                          paragraph_unit, list_item_unit, validate_text_unit)

CASES = []


def probe(name, claim, fn, expect, finding=None):
    try:
        value = fn()
        observed = {"status": "returned", "value": value}
    except Exception as exc:
        observed = {"status": "raised", "type": type(exc).__name__, "message": str(exc)}
    matched = expect(observed)
    CASES.append({"name": name, "claim": claim, "observed": observed,
                  "characterization_matched": matched, "finding": finding})


def returned(value=None):
    return lambda x: x["status"] == "returned" and (value is None or x["value"] == value)


def raised(kind="ValueError"):
    return lambda x: x["status"] == "raised" and x["type"] == kind


T = "| A | B |\n|---|---|\n| one | two |\n"
R = table_units(T, T.index("one"))
probe("unicode_codepoints_crlf", "Original Python Unicode offsets survive emoji, combining marks, CRLF and trimming.",
      lambda: table_units("😀 e\u0301\r\n\r\n" + T.replace("\n", "\r\n"), 35), returned({"header": {"start": 8, "end": 17, "text": "| A | B |"}, "row": {"start": 30, "end": 43, "text": "| one | two |"}, "cell_count": 2}), "S1")
probe("exact_trim_contract", "unit strips all Python isspace at both ends, including NBSP and em-space.",
      lambda: unit("\u00a0\u2003alpha\u2003\n", 0, 9), returned({"start": 2, "end": 7, "text": "alpha"}), "L1")
probe("invalid_unit_negative", "Negative unit bounds are checked after trimming/indexing.",
      lambda: unit("abc", -1, 2), raised(), "F5")
probe("invalid_unit_oversize", "Oversized end can leak IndexError instead of ValueError.",
      lambda: unit("abc", 0, 10), raised("IndexError"), "F5")
probe("table_negative_offset", "High-level table rejects negative offset.", lambda: table_units(T, -1), raised(), "S1")
probe("table_end_offset", "High-level table rejects offset equal to len(text).", lambda: table_units(T, len(T)), raised(), "S1")
probe("paragraph_negative_offset", "Paragraph rejects negative offset.", lambda: paragraph_unit(T, -1), raised(), "S1")
probe("list_end_offset", "List rejects out-of-range offset.", lambda: list_item_unit("- alpha\n", 8), raised(), "S1")
probe("cropped_row", "Row cropped but exact to its substring fails complete-line validation.",
      lambda: validate_table_unit(T, dict(R["row"], end=R["row"]["end"] - 1, text=R["row"]["text"][:-1])), raised(), "S1")
probe("partial_header_accepted", "A header substring with fewer source columns can pass if it matches row column count.",
      lambda: validate_table_unit("| A | B | C |\n|---|---|\n| one | two |\n", {"start": 24, "end": 37, "text": "| one | two |"}, {"start": 0, "end": 9, "text": "| A | B |"}), returned(True), "F1")
probe("unrelated_header_accepted", "Low-level header can come from an unrelated distant table.",
      lambda: validate_table_unit(T + "\n| X | Y |\n", R["row"], {"start": len(T) + 1, "end": len(T) + 10, "text": "| X | Y |"}), returned(True), "F1")
probe("same_count_wrong_header_accepted", "Low-level validator accepts a data row as the claimed header.",
      lambda: validate_table_unit(T, R["row"], R["row"]), returned(True), "F1")
probe("separator_as_row_accepted", "Low-level row validator does not reject separator lines.",
      lambda: validate_table_unit(T, unit(T, 10, 20)), returned(True), "F1")
probe("header_negative_offsets_accepted", "Header offsets may use Python negative indexing and still validate.",
      lambda: validate_table_unit(T + "| X | Y |", R["row"], {"start": -9, "end": len(T)+9, "text": "| X | Y |"}), returned(True), "F1")
probe("high_level_column_mismatch", "High-level rejects row/header/separator column mismatch.",
      lambda: table_units("| A | B |\n|---|---|\n| one | two | three |", 27), raised(), "S1")
probe("high_level_malformed_intervening_row", "High-level ignores malformed intervening pipe-start rows.",
      lambda: table_units("| A | B |\n|---|---|\n| broken\n| one | two |", 30), returned(), "F2")
probe("high_level_separator_as_header", "Consecutive separators cause nearest separator's preceding separator to be labeled header.",
      lambda: table_units("| A | B |\n|---|---|\n|---|---|\n| one | two |", 33), returned(), "F2")
probe("high_level_missing_outer_pipes", "Optional-outer-pipe Markdown tables are outside supported format.",
      lambda: table_units("A | B\n---|---\none | two\n", 15), raised(), "L2")
probe("escaped_pipe_odd", "Odd backslash run escapes a pipe without changing the original text.",
      lambda: cells(r"| a \| b | c |"), returned([r"a \| b", "c"]), "S1")
probe("escaped_pipe_even", "Even backslash run leaves the pipe a delimiter.",
      lambda: cells("| a " + chr(92) * 2 + "| b | c |"), returned(["a " + chr(92) * 2, "b", "c"]), "S1")
probe("escaped_final_outer_pipe", "An escaped final pipe is still treated as a complete outer boundary.",
      lambda: cells("| a | b \\|"), returned(), "F3")
probe("table_in_fence", "Table-like lines inside fenced code are accepted as a table.",
      lambda: table_units("```\n" + T + "```\n", 29), returned(), "L2")
probe("paragraph_heading_swallowed", "Paragraph helper groups ATX heading and following text without blank line.",
      lambda: paragraph_unit("# Section\nAlpha detail.\n", 12), returned({"start": 0, "end": 23, "text": "# Section\nAlpha detail."}), "L3")
probe("paragraph_cr_only", "CR-only paragraphs are not blank-line delimited by the LF regex.",
      lambda: paragraph_unit("Alpha\r\rBeta", 8), returned({"start": 0, "end": 11, "text": "Alpha\r\rBeta"}), "L3")
probe("paragraph_blank_offset", "Offset in LF blank separation rejects.", lambda: paragraph_unit("Alpha\n\nBeta", 6), raised(), "S1")
probe("paragraph_crlf", "CRLF blank separation works and trims line endings.",
      lambda: paragraph_unit("Alpha\r\n\r\nBeta\r\n", 10), returned({"start": 9, "end": 13, "text": "Beta"}), "S1")
probe("list_child_omits_parent", "Nested child selection contains no governing parent text.",
      lambda: list_item_unit("- Parent qualifier.\n  - Child detail.\n- Sibling.\n", 28), returned({"start": 22, "end": 37, "text": "- Child detail."}), "F4")
probe("list_indented_heading_swallowed", "Indented ATX heading without blank line does not terminate list selection.",
      lambda: list_item_unit("- Alpha.\n  # Next section\nOutside.\n", 3), returned(), "L4")
probe("list_setext_swallowed", "Setext heading without blank line does not terminate list selection.",
      lambda: list_item_unit("- Alpha.\nNext section\n============\nOutside.\n", 3), returned(), "L4")
probe("list_tab_nested_unsupported", "Tab-indented nested item is not recognized as a child item.",
      lambda: list_item_unit("- Parent.\n\t- Child.\n- Sibling.\n", 14), returned({"start": 0, "end": 19, "text": "- Parent.\n\t- Child."}), "L4")
probe("list_fenced_bullet_selected_as_child", "A bullet-like line inside an indented fenced block is selected as a nested child.",
      lambda: list_item_unit("- Parent.\n  ```\n  - literal code\n  ```\n  Parent tail.\n- Next.\n", 23), returned({"start": 18, "end": 53, "text": "- literal code\n  ```\n  Parent tail."}), "L4")
probe("list_blank_then_outside", "Blank line followed by unindented prose terminates item.",
      lambda: list_item_unit("- Alpha.\n\nOutside.\n", 3), returned({"start": 0, "end": 8, "text": "- Alpha."}), "S1")
probe("text_validator_mirrors_extractor", "Text validator accepts the same heading-containing paragraph as its extractor.",
      lambda: validate_text_unit("# Section\nAlpha detail.\n", paragraph_unit("# Section\nAlpha detail.\n", 12), "paragraph"), returned(True), "L3")
probe("unicode_line_separators", "splitlines recognizes Unicode line separators although paragraph regex recognizes LF only.",
      lambda: lines("Alpha\u2028Beta"), returned([(0, 6, "Alpha\u2028"), (6, 10, "Beta")]), "L3")


probe("unit_negative_bounds_can_be_normalized", "Invalid negative start can be silently normalized when final character is whitespace.",
      lambda: unit("abc ", -1, 3), returned({"start": 0, "end": 3, "text": "abc"}), "F5")
probe("wrong_header_count_rejected", "Low-level count check catches a header with a different number of cells.",
      lambda: validate_table_unit(T + "| X |", R["row"], {"start": len(T), "end": len(T)+5, "text": "| X |"}), raised(), "S1")
probe("mutated_quote_rejected", "Exact span matching rejects changed row text.",
      lambda: validate_table_unit(T, dict(R["row"], text="| one | red |")), raised(), "S1")
probe("table_gap_blocks_unrelated_header", "Blank separation prevents high-level reuse of an earlier table header.",
      lambda: table_units(T + "\n| three | four |\n", len(T) + 3), raised(), "S1")
probe("table_newline_offset_returns_row", "A source offset on a row's newline selects the row even though trimmed span excludes offset.",
      lambda: table_units(T, len(T)-1), returned(R), "L1")
probe("paragraph_absorbs_adjacent_list", "Blank-line paragraph selection absorbs an adjacent list without blank separation.",
      lambda: paragraph_unit("Intro.\n- Alpha.\n- Beta.\n", 3), returned({"start": 0, "end": 23, "text": "Intro.\n- Alpha.\n- Beta."}), "L3")
probe("nested_parent_continuation_excluded_from_child", "A blank line and dedented parent continuation ends a child item, while parent retains it.",
      lambda: list_item_unit("- Parent.\n  - Child.\n\n  Parent continuation.\n- Next.\n", 15), returned({"start": 12, "end": 20, "text": "- Child."}), "S1")
probe("ordered_item_continuation", "Ordered items with parenthesized markers retain indented continuation and stop at sibling.",
      lambda: list_item_unit("1) Alpha.\n   Continued.\n2) Beta.\n", 5), returned({"start": 0, "end": 23, "text": "1) Alpha.\n   Continued."}), "S1")
probe("no_separator_rejected", "High-level extractor rejects pipe rows without a preceding separator.",
      lambda: table_units("| A | B |\n| one | two |\n", 15), raised(), "S1")
probe("high_level_separator_target_rejected", "High-level extractor rejects a separator as selected row.",
      lambda: table_units(T, 12), raised(), "S1")

if __name__ == "__main__":
    result = {"purpose": "Characterization only. Matching a known unsafe behavior is evidence of a limitation, not approval.",
              "cases": CASES, "count": len(CASES),
              "characterization_matches": sum(c["characterization_matched"] for c in CASES),
              "probe_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    Path("probe-results.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "cases"}, ensure_ascii=False))
    for case in CASES:
        if not case["characterization_matched"]:
            print(json.dumps(case, ensure_ascii=False))
    raise SystemExit(0 if result["characterization_matches"] == len(CASES) else 1)
