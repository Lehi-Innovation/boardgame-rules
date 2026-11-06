#!/usr/bin/env python3
"""Validate recorded novelty13 delivery evidence without reviewing its verdict."""
import copy
import hashlib
import json
from pathlib import Path

from PIL import Image

B = Path(__file__).resolve().parent
OUT = B / "novelty13-delivery-validation.json"
EXPECTED = {
    "working-novelty-adjudication-13.json": "c543494c330ee64288ff592988bfcc050a3c8376a4f61ea25dbc4b5ca4f46493",
    "working-novelty-adjudication-13-read-ledger.json": "3455d5417b2517e5caa28810b761c5c7480ddbc311fb054dfb34be045ef49423",
    "native-panel-novelty-adjudication-12-read-ledger.json": "9d4b6b6324a31ab12ad2a6dd0ad582a8bfad2bf3ca725f046d03c8b9adf36ff3",
    "coverage-novelty-adjudication-11-read-ledger.json": "eca65d91d99ba2a1934cc6e35bed43a7de60e627335a24cf99178bd65c77a546",
}
checks = []
snapshots = {}
counts = {}


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def data(path):
    path = Path(path)
    raw = path.read_bytes()
    snapshots.setdefault(str(path), digest(raw))
    return raw


def obj(path):
    return json.loads(data(path))


def check(name, condition, detail=None):
    row = {"check": name, "ok": bool(condition)}
    if detail is not None:
        row["detail"] = detail
    checks.append(row)


def full_text(row, label):
    raw = data(row["path"])
    text = raw.decode("utf-8")
    check(label + ":file_hash", digest(raw) == row["original_byte_sha256"])
    check(label + ":unicode_length", len(text) == row["character_length"])
    end = 0
    for i, part in enumerate(row["slices"]):
        a, z = part["range"]
        tag = f"{label}:slice{i}"
        check(tag + ":contiguous_bounds", a == end and 0 <= a < z <= len(text) and z - a <= 6000)
        check(tag + ":utf8_hash", digest(text[a:z].encode()) == part["slice_utf8_sha256"])
        check(tag + ":cap_no_truncation", part["output_cap_tokens"] >= 4000 and part["truncated"] is False)
        end = z
    check(label + ":complete", end == len(text) and row["contiguous_complete"] is True)
    return len(row["slices"])


def image_row(row, label):
    raw = data(row["path"])
    check(label + ":hash", digest(raw) == row["original_byte_sha256"])
    with Image.open(row["path"]) as im:
        w, h = im.size
    check(label + ":dimensions", [w, h] == row["dimensions"])
    region = row.get("viewed_region_xyxy", row.get("viewed_region"))
    check(label + ":full_view", region == [0, 0, w, h] and row.get("full_native_view", row.get("fully_viewed")) is True)
    if "relevant_region_xyxy" in row:
        a, b, c, d = row["relevant_region_xyxy"]
        check(label + ":relevant_bounds", 0 <= a < c <= w and 0 <= b < d <= h)
    check(label + ":evidence_description", bool(row.get("printed_transcription", row.get("identity", row.get("observation", "")))))


def covered(a, z, intervals):
    end = a
    for lo, hi in sorted(intervals):
        if hi <= end:
            continue
        if lo > end:
            return False
        end = hi
        if end >= z:
            return True
    return False


def run():
    for filename, expected in EXPECTED.items():
        check("immutable_artifact_hash:" + filename, digest(data(B / filename)) == expected)
    report = obj(B / "working-novelty-adjudication-13.json")
    ledger = obj(B / "working-novelty-adjudication-13-read-ledger.json")
    prior12 = obj(B / "native-panel-novelty-adjudication-12-read-ledger.json")
    prior11 = obj(B / "coverage-novelty-adjudication-11-read-ledger.json")
    reuse = ledger["own_immutable_input_delivery_reuse"]
    check("own12_exact_reference", reuse["own_ledger_path"] == str(B / "native-panel-novelty-adjudication-12-read-ledger.json") and reuse["own_ledger_sha256"] == EXPECTED["native-panel-novelty-adjudication-12-read-ledger.json"])
    check("own11_exact_reference", reuse["prior11_ledger_path"] == str(B / "coverage-novelty-adjudication-11-read-ledger.json") and reuse["prior11_ledger_sha256"] == EXPECTED["coverage-novelty-adjudication-11-read-ledger.json"])
    check("report_ledger_reuse_identical", report["bank_validation"] == reuse)
    check("report_ledger_input_link", report["read_ledger_path"] == str(B / "working-novelty-adjudication-13-read-ledger.json"))

    new_slices = sum(full_text(f, "new:" + f["path"]) for f in ledger["new_complete_text_inputs"])
    counts["new_complete_text_files"] = len(ledger["new_complete_text_inputs"])
    counts["new_complete_text_slices"] = new_slices
    check("report_input_hashes_exact", report["input_hashes"] == {r["path"]: r["original_byte_sha256"] for r in ledger["new_complete_text_inputs"]})
    prior_rows = prior12["text_files"] + prior12["prior_immutable_delivery_reuse"]["text_files"]
    old_slices = 0
    base_keys = ["path", "original_byte_sha256", "character_length", "slices", "contiguous_complete"]
    for row in reuse["complete_immutable_text_deliveries"]:
        check("own_reuse_exact_row:" + row["path"], row in prior_rows)
        old_slices += full_text(row, "reused:" + row["path"])
        if "reused_from_ledger" in row:
            original = next(x for x in prior11["text_files"] if x["path"] == row["path"])
            check("own11_original_row:" + row["path"], all(row[k] == original[k] for k in base_keys))
            check("own11_original_row_hash_link:" + row["path"], row["reused_from_ledger"] == str(B / "coverage-novelty-adjudication-11-read-ledger.json") and row["reused_from_ledger_sha256"] == EXPECTED["coverage-novelty-adjudication-11-read-ledger.json"])
    counts["reused_complete_text_files"] = len(reuse["complete_immutable_text_deliveries"])
    counts["reused_complete_text_slices"] = old_slices

    intervals = {}
    for i, row in enumerate(ledger["targeted_primary_source_rereads"]):
        raw = data(row["path"])
        text = raw.decode()
        a, z = row["range"]
        intervals.setdefault(row["path"], []).append((a, z))
        check(f"targeted{i}:file", digest(raw) == row["original_byte_sha256"] and len(text) == row["character_length"])
        check(f"targeted{i}:bounds", 0 <= a < z <= len(text) and z - a <= 6000)
        check(f"targeted{i}:slice", digest(text[a:z].encode()) == row["slice_utf8_sha256"] and row["output_cap_tokens"] >= 4000 and row["truncated"] is False)
        check(f"targeted{i}:complete_original_reuse", any(x["path"] == row["path"] and x["original_byte_sha256"] == row["original_byte_sha256"] for x in reuse["complete_immutable_text_deliveries"]))
    operative = report["decisions"][0]["primary_sources"]["operative_text_entries"]
    for i, entry in enumerate(operative):
        raw = data(entry["path"])
        text = raw.decode()
        a, z = entry["character_range"]
        check(f"operative{i}:full_file_hash", digest(raw) == entry["original_byte_sha256"])
        check(f"operative{i}:range_text_hash", 0 <= a < z <= len(text) and text[a:z] == entry["complete_operative_passage"] and digest(text[a:z].encode()) == entry["passage_utf8_sha256"])
        check(f"operative{i}:covered_by_fresh_reread", covered(a, z, intervals[entry["path"]]))
    counts["targeted_primary_slices"] = len(ledger["targeted_primary_source_rereads"])
    counts["operative_primary_entries"] = len(operative)
    check("successful_slice_total", ledger["total_successful_slice_count"] == new_slices + counts["targeted_primary_slices"])

    for i, row in enumerate(ledger["fresh_native_image_views"]):
        image_row(row, f"fresh_image{i}")
    counts["fresh_native_images"] = len(ledger["fresh_native_image_views"])
    check("report_native_records_identical", report["decisions"][0]["primary_sources"]["native_images"] == ledger["fresh_native_image_views"])
    oldimages = ledger["prior_native_source_reuse"]
    check("prior_native_exact_rows", oldimages["images"] == prior12["image_files"])
    check("prior_native_exact_ledger", oldimages["own_ledger_sha256"] == EXPECTED["native-panel-novelty-adjudication-12-read-ledger.json"])
    for i, row in enumerate(oldimages["images"]):
        image_row(row, f"prior_image{i}")
    counts["reused_native_images"] = len(oldimages["images"])

    # Rebuild literal bank entries; do not assess answers or novelty conclusions.
    packet16 = obj(B / "panel-audit-bank-supplement-v16.json")
    corrections18 = obj(B / "expanded-v16/key-corrections.json")[0]
    packet18 = obj(B / "working-pass-v18-supplement.json")
    correction157 = packet18["inherited163_equivalence"]["Q157_explicit_correction"][0]
    current = {}
    for filename, field, supplement, replacement in [
        ("questions.json", "questions", "complete6_question_objects", "question"),
        ("answer-key.json", "answers", "complete6_key_objects", "key"),
        ("asked-fact-map.json", "questions", "complete6_asked_map_objects", "mapping"),
    ]:
        old = obj(B / "expanded-v16" / filename)
        oldhash = {"questions.json": "full_question_file_sha256", "answer-key.json": "full_key_file_sha256", "asked-fact-map.json": "full_asked_map_sha256"}[filename]
        check("v16_immutable:" + filename, digest(data(B / "expanded-v16" / filename)) == prior12["current_bank_comparison"][oldhash])
        entries = copy.deepcopy(old[field])
        i = next(i for i, row in enumerate(entries) if row["id"] == "Q157")
        check("Q157_old_exact:" + filename, entries[i] == correction157["old_" + replacement])
        entries[i] = correction157["new_" + replacement]
        entries += packet18[supplement]
        path = B / "expanded-v18" / filename
        final = obj(path)
        current[filename] = final
        check("all169_exact_reconstruction:" + filename, entries == final[field] and len(entries) == 169)
        check("full169_hash:" + filename, digest(data(path)) == packet18["full_bank_sha256"][filename] == reuse["new_v18_reconstruction"][filename]["sha256"])
    q15 = obj(B / "expanded-v15/questions.json")["questions"]
    k15 = obj(B / "expanded-v15/answer-key.json")["answers"]
    check("old154_questions_exact", q15 + packet16["questions"] == obj(B / "expanded-v16/questions.json")["questions"])
    old_i = next(i for i, row in enumerate(k15) if row["id"] == "Q18")
    check("old_Q18_key_exact", k15[old_i] == corrections18["old_key"])
    k15[old_i] = corrections18["new_key"]
    check("old154_keys_plus9_exact", k15 + packet16["answer_key"] == obj(B / "expanded-v16/answer-key.json")["answers"])
    check("nine_map_supplement_exact", packet16["asked_fact_entries"] == obj(B / "expanded-v16/asked-fact-map.json")["questions"][154:])
    maps = current["asked-fact-map.json"]["questions"]
    check("all169_map_question_texts_exact", [{"id": x["id"], "question": x["question"]} for x in maps] == current["questions.json"]["questions"])
    check("all169_unique_ordered_IDs", len({x["id"] for x in maps}) == 169 and [x["id"] for x in maps] == [x["id"] for x in current["answer-key.json"]["answers"]])
    expected_projection = "\n\n".join(row["id"] + " " + row["question"] + "\nRequired: " + " | ".join(f for c in row["requested_clauses"] for f in c["required_facts"]) for row in maps) + "\n"
    projection = reuse["full_new_asked_projection"]
    check("all169_projection_exact", data(projection["path"]).decode() == expected_projection and len(expected_projection) == projection["character_length"] and digest(expected_projection.encode()) == projection["sha256"])
    check("all169_projection_complete_delivery", any(row["path"] == projection["path"] and row["original_byte_sha256"] == projection["sha256"] for row in ledger["new_complete_text_inputs"]))
    facts = sum(len(c["required_facts"]) for row in maps for c in row["requested_clauses"])
    counts["current_questions"] = len(maps)
    counts["current_required_facts"] = facts
    check("current_count504", facts == 504 and current["asked-fact-map.json"]["required_fact_count"] == 504)
    check("all169_comparison_IDs_exact", [x["id"] for x in report["decisions"][0]["all169_actual_ask_comparison"]] == [x["id"] for x in maps])

    precision = report["Q84_precision_adjudication"]
    oldmap = precision["complete_old_map_entry"]
    newmap = precision["complete_proposed_new_map_entry"]
    check("Q84_old_map_exact_current", oldmap == next(row for row in maps if row["id"] == "Q84"))
    restored = copy.deepcopy(newmap)
    oldfacts = oldmap["requested_clauses"][0]["required_facts"]
    newfacts = newmap["requested_clauses"][0]["required_facts"]
    differences = [i for i, (a, z) in enumerate(zip(oldfacts, newfacts)) if a != z]
    restored["requested_clauses"][0]["required_facts"][:2] = oldfacts[:2]
    check("Q84_exactly_two_string_changes", differences == [0, 1] and len(oldfacts) == len(newfacts) == 4 and restored == oldmap)
    check("Q84_all_context_unchanged", oldmap["key_context_not_required"] == newmap["key_context_not_required"])
    check("Q84_key_unchanged_current", precision["complete_old_key"] == precision["complete_proposed_new_key"] == next(x for x in current["answer-key.json"]["answers"] if x["id"] == "Q84"))
    check("Q84_question_unchanged_current", precision["old_question"] == precision["proposed_question"] == next(x for x in current["questions.json"]["questions"] if x["id"] == "Q84"))
    check("Q84_zero_fact_delta", precision["required_fact_count_old"] == precision["required_fact_count_new"] == 4 and precision["count_delta"] == 0)
    decision = report["decisions"][0]
    minimal = sum(len(c["required_facts"]) for c in decision["minimal_asked_only_map"]["requested_clauses"])
    check("single_new_minimal_fact_exact", [f for c in decision["minimal_asked_only_map"]["requested_clauses"] for f in c["required_facts"]] == decision["minimum_required_facts"])
    accounting = report["required_fact_accounting"]
    check("delta1_and170_505", len(report["decisions"]) == 1 and minimal == decision["required_fact_count"] == len(decision["minimum_required_facts"]) == accounting["retained_new_question_required_facts"] == 1 and accounting["current169_required_facts"] == accounting["actual_bank_required_fact_count"] == 504 and accounting["Q84_precision_delta"] == 0 and accounting["proposed_total_if_explicitly_consolidated"] == 505 and accounting["proposed_question_count_if_consolidated"] == 170 and accounting["actual_bank_question_count"] == 169)


try:
    run()
except Exception as exc:
    check("validator_runtime_exception", False, f"{type(exc).__name__}: {exc}")
for path, before in list(snapshots.items()):
    check("input_preserved:" + path, digest(Path(path).read_bytes()) == before)
exceptions = [row for row in checks if not row["ok"]]
result = {
    "task": "Evidence-delivery validation only; no novelty review or global coverage verdict",
    "validator": str(Path(__file__).resolve()),
    "validator_sha256": digest(Path(__file__).read_bytes()),
    "status": "VALID" if not exceptions else "INVALID",
    "check_count": len(checks),
    "passed_check_count": len(checks) - len(exceptions),
    "counts": counts,
    "immutable_artifact_expected_sha256": EXPECTED,
    "exceptions": exceptions,
    "checks": checks,
    "scope": "Checks recorded delivery caps/truncation flags, exact bytes/ranges/rows, native dimensions, reconstruction, preservation and count arithmetic. Does not newly adjudicate game rules or novelty.",
}
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"status": result["status"], "checks": result["check_count"], "exceptions": len(exceptions), "counts": counts, "output": str(OUT), "output_sha256": digest(OUT.read_bytes()), "validator_sha256": result["validator_sha256"]}))
raise SystemExit(0 if not exceptions else 1)
