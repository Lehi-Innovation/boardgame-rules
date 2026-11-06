#!/usr/bin/env python3
"""Evidence validation only: no semantic or novelty adjudication.

Read-only machine parsing of the four bound v19 source-bank files is authorized
for this validation. It is not retrospective model delivery of their text.
"""
import hashlib
import json
from pathlib import Path

from PIL import Image

B = Path(__file__).resolve().parent
OUTPUT = B / "novelty14-delivery-validation.json"
EXPECTED = {
    "working-novelty-adjudication-14.json": "5961ebea73fd8ef155ecf678a3e02ac7f167f005dd9bbcaed4efa66513ac5fe4",
    "working-novelty-adjudication-14-read-ledger.json": "de8ae70a3da95f8a9f405d396c3c62308ce39643c9b77431f76e86957ef7f047",
    "working-novelty14-input.json": "ed119d9de1a40b91ac48ed9cf957105377cc5ad8acacd3160a14d7f81e0b64a6",
    "novelty14-all170-actual-asks.jsonl": "306177be61f49eb8aaa921d77511aafc577a95a5e89886d0afea795d7602f2e7",
    "coverage-novelty-adjudication-11-read-ledger.json": "eca65d91d99ba2a1934cc6e35bed43a7de60e627335a24cf99178bd65c77a546",
    "native-panel-novelty-adjudication-12-read-ledger.json": "9d4b6b6324a31ab12ad2a6dd0ad582a8bfad2bf3ca725f046d03c8b9adf36ff3",
}
checks = []
snapshots = {}
counts = {}
machine_only_bank_access = []
transcription_digests = []


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def utf8hash(text):
    return digest(text.encode("utf-8"))


def raw(path):
    path = Path(path)
    value = path.read_bytes()
    snapshots.setdefault(str(path), digest(value))
    return value


def obj(path):
    return json.loads(raw(path))


def check(name, condition, kind="filesystem", detail=None):
    result = {"check": name, "kind": kind, "ok": bool(condition)}
    if detail is not None:
        result["detail"] = detail
    checks.append(result)


def slice_checks(path, text, part, label):
    a, z = part["range"]
    check(label + ":bounds", 0 <= a < z <= len(text) and z - a <= 6000)
    check(label + ":utf8_slice_hash", utf8hash(text[a:z]) == part["slice_utf8_sha256"])
    check(label + ":recorded_output_cap", part["output_cap_tokens"] >= 4000,
          "recorded_tool_attestation", "Recorded cap only; historical transport not replayed.")
    check(label + ":recorded_no_truncation", part["truncated"] is False,
          "recorded_tool_attestation", "Recorded truncation flag only; no independent transport receipt is available to this filesystem validator.")


def complete_text(row, label):
    data = raw(row["path"])
    text = data.decode("utf-8")
    check(label + ":original_byte_hash", digest(data) == row["original_byte_sha256"])
    check(label + ":unicode_length", len(text) == row["character_length"])
    end = 0
    for index, part in enumerate(row["slices"]):
        check(f"{label}:slice{index}:contiguous", part["range"][0] == end)
        slice_checks(row["path"], text, part, f"{label}:slice{index}")
        end = part["range"][1]
    check(label + ":complete_range", end == len(text))
    check(label + ":complete_flag", row["contiguous_complete"] is True, "recorded_tool_attestation")
    return len(row["slices"])


def image_checks(row, label, fresh=False):
    data = raw(row["path"])
    check(label + ":native_byte_hash", digest(data) == row["original_byte_sha256"])
    with Image.open(row["path"]) as image:
        w, h = image.size
    check(label + ":native_dimensions", [w, h] == row["dimensions"])
    region = row.get("viewed_region_xyxy", row.get("viewed_region"))
    check(label + ":recorded_full_view_bounds", region == [0, 0, w, h])
    if "relevant_region_xyxy" in row:
        a, b, c, d = row["relevant_region_xyxy"]
        check(label + ":relevant_bounds", 0 <= a < c <= w and 0 <= b < d <= h)
    flag = row.get("full_native_view", row.get("fully_viewed"))
    check(label + ":historical_view_attested", flag is True, "recorded_tool_attestation",
          "Does not prove that an image tool ran or that the printed glyphs were perceived correctly.")
    if fresh:
        if "complete_native_transcription" in row:
            check(label + ":native_transcription_utf8_hash",
                  utf8hash(row["complete_native_transcription"]) == row["transcription_sha256"])
        else:
            text = json.dumps(row["complete_Growth_band_transcription"], ensure_ascii=False, separators=(",", ":"))
            transcription_digests.append({"path": row["path"], "representation": "canonical JSON of complete_Growth_band_transcription", "sha256": utf8hash(text)})
        check(label + ":visual_transcription_attestation_present",
              bool(row.get("complete_native_transcription", row.get("complete_Growth_band_transcription"))),
              "recorded_perception_attestation", "Text-to-pixels correctness belongs to the original adjudication; not OCR-verified here.")


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
        check("immutable_hash:" + filename, digest(raw(B / filename)) == expected)
    report = obj(B / "working-novelty-adjudication-14.json")
    ledger = obj(B / "working-novelty-adjudication-14-read-ledger.json")
    packet = obj(B / "working-novelty14-input.json")
    prior11 = obj(B / "coverage-novelty-adjudication-11-read-ledger.json")
    prior12 = obj(B / "native-panel-novelty-adjudication-12-read-ledger.json")
    check("report_ledger_link", report["read_ledger_path"] == str(B / "working-novelty-adjudication-14-read-ledger.json"))
    check("report_packet_binding", report["input_packet"]["sha256"] == EXPECTED["working-novelty14-input.json"])

    new_slices = sum(complete_text(row, "new:" + row["path"]) for row in ledger["new_complete_text_inputs"])
    counts["new_complete_text_files"] = len(ledger["new_complete_text_inputs"])
    counts["new_complete_text_slices"] = new_slices
    check("new_complete_input_set_exact", {Path(x["path"]).name for x in ledger["new_complete_text_inputs"]} == {"working-novelty14-input.json", "novelty14-all170-actual-asks.jsonl", "scope-reachability-steering-2026-11-05.txt"})

    reused_slices = 0
    reused_by_path = {}
    for index, reuse in enumerate(ledger["own_prior_complete_primary_text_delivery_reuse"]):
        row = reuse["original_complete_delivery_row"]
        check(f"reuse{index}:original_ledger_path", reuse["original_ledger_path"] == str(B / "coverage-novelty-adjudication-11-read-ledger.json"))
        check(f"reuse{index}:original_ledger_hash", reuse["original_ledger_sha256"] == EXPECTED["coverage-novelty-adjudication-11-read-ledger.json"])
        check(f"reuse{index}:exact_full_original_row", row in prior11["text_files"])
        reused_slices += complete_text(row, "reused:" + row["path"])
        reused_by_path[row["path"]] = row
    counts["reused_complete_source_files"] = len(reused_by_path)
    counts["reused_complete_source_slices"] = reused_slices

    intervals = {}
    for index, row in enumerate(ledger["targeted_primary_rereads"]):
        data = raw(row["path"])
        text = data.decode()
        check(f"targeted{index}:full_source_hash", digest(data) == row["original_byte_sha256"])
        check(f"targeted{index}:full_source_length", len(text) == row["character_length"])
        check(f"targeted{index}:complete_source_reuse_bound", row["path"] in reused_by_path and reused_by_path[row["path"]]["original_byte_sha256"] == row["original_byte_sha256"])
        slice_checks(row["path"], text, row, f"targeted{index}")
        intervals.setdefault(row["path"], []).append(row["range"])
    counts["new_targeted_primary_slices"] = len(ledger["targeted_primary_rereads"])
    counts["all_new_recorded_slices"] = new_slices + counts["new_targeted_primary_slices"]
    check("all28_slices_accounted", counts["all_new_recorded_slices"] == ledger["successful_text_slice_count"] == report["input_delivery"]["successful_slice_count"] == 28)

    for index, entry in enumerate(ledger["source_passages"]):
        text = raw(entry["path"]).decode()
        a, z = entry["character_range"]
        check(f"operative{index}:source_hash", digest(raw(entry["path"])) == entry["original_byte_sha256"])
        check(f"operative{index}:range_text_hash", 0 <= a < z <= len(text) and text[a:z] == entry["complete_operative_passage"] and utf8hash(text[a:z]) == entry["passage_utf8_sha256"])
        check(f"operative{index}:fresh_range_coverage", covered(a, z, intervals[entry["path"]]))
    counts["operative_source_entries"] = len(ledger["source_passages"])

    for index, reuse in enumerate(ledger["own_prior_original_panel_identity_reuse"]):
        check(f"panel_reuse{index}:ledger_hash", reuse["original_ledger_path"] == str(B / "native-panel-novelty-adjudication-12-read-ledger.json") and reuse["original_ledger_sha256"] == EXPECTED["native-panel-novelty-adjudication-12-read-ledger.json"])
        check(f"panel_reuse{index}:exact_original_row", reuse["original_image_delivery_row"] in prior12["image_files"])
        image_checks(reuse["original_image_delivery_row"], f"panel_reuse{index}")
    counts["reused_panel_photo_records"] = len(ledger["own_prior_original_panel_identity_reuse"])
    cards = ledger["own_prior_card_identity_rows"]
    check("card_reuse_ledger_hash", cards["original_ledger_path"] == str(B / "coverage-novelty-adjudication-11-read-ledger.json") and cards["original_ledger_sha256"] == EXPECTED["coverage-novelty-adjudication-11-read-ledger.json"])
    for index, row in enumerate(cards["rows"]):
        check(f"card_reuse{index}:exact_original_row", row in prior11["image_files"])
        image_checks(row, f"card_reuse{index}")
    counts["reused_card_legend_records"] = len(cards["rows"])
    for index, row in enumerate(ledger["fresh_full_native_views"]):
        image_checks(row, f"fresh{index}", True)
        prior = [x["original_image_delivery_row"] for x in ledger["own_prior_original_panel_identity_reuse"]] + cards["rows"]
        check(f"fresh{index}:previous_source_image_binding", any(x["path"] == row["path"] and x["original_byte_sha256"] == row["original_byte_sha256"] and x["dimensions"] == row["dimensions"] for x in prior))
    counts["fresh_native_full_view_records"] = len(ledger["fresh_full_native_views"])
    check("ten_fresh_records", counts["fresh_native_full_view_records"] == report["input_delivery"]["fresh_native_full_views"] == 10)

    # Authorized validation-only parsing; never print/review whole bank prose.
    bank = {}
    for path, expected in packet["current_bank_bindings"].items():
        path = Path(path)
        data = raw(path)
        check("bound_bank_hash:" + path.name, digest(data) == expected)
        bank[path.name] = json.loads(data)
        machine_only_bank_access.append({"path": str(path), "sha256": digest(data), "access": "Read-only validation-only machine parsing/hashing; no whole-file model-delivery claim."})
    questions = bank["questions.json"]["questions"]
    maps = bank["asked-fact-map.json"]["questions"]
    keys = bank["answer-key.json"]["answers"]
    credits = bank["core-scope-credit.json"]["questions"]
    q_by_id = {x["id"]: x for x in questions}
    m_by_id = {x["id"]: x for x in maps}
    k_by_id = {x["id"]: x for x in keys}
    c_by_id = {x["id"]: x for x in credits}
    check("all170_unique_ordered_IDs", len(q_by_id) == len(m_by_id) == len(k_by_id) == 170 and [x["id"] for x in questions] == [f"Q{i:02d}" for i in range(1, 171)] == [x["id"] for x in maps] == [x["id"] for x in keys])
    reconstructed = []
    for question in questions:
        mapped = m_by_id[question["id"]]
        check("literal_map_question_match:" + question["id"], question["question"] == mapped["question"])
        reconstructed.append({"id": question["id"], "literal_question": question["question"], "all_asked_facts": [f for c in mapped["requested_clauses"] for f in c["required_facts"]]})
    ask_path = B / "novelty14-all170-actual-asks.jsonl"
    ask_text = raw(ask_path).decode()
    ask_objects = [json.loads(line) for line in ask_text.splitlines() if line.strip()]
    check("all170_all505_exact_projection_reconstruction", ask_objects == reconstructed)
    trailing_newlines = len(ask_text) - len(ask_text.rstrip("\n"))
    reconstructed_text = "\n".join(json.dumps(x, ensure_ascii=False) for x in reconstructed) + "\n" * trailing_newlines
    check("all170_projection_exact_serialized_bytes", reconstructed_text.encode() == raw(ask_path))
    counts["projection_trailing_newlines"] = trailing_newlines
    counts["current_questions"] = len(reconstructed)
    counts["current_asked_facts"] = sum(len(x["all_asked_facts"]) for x in reconstructed)
    check("170_505_count", counts["current_questions"] == 170 and counts["current_asked_facts"] == bank["asked-fact-map.json"]["required_fact_count"] == 505)
    for selected in packet["complete_selected_current_entries"]:
        ident = selected["question"]["id"]
        check("selected_question_exact:" + ident, selected["question"] == q_by_id[ident])
        check("selected_key_exact:" + ident, selected["key"] == k_by_id[ident])
        check("selected_full_map_exact:" + ident, selected["asked_map"] == m_by_id[ident])
    counts["selected_current_entries"] = len(packet["complete_selected_current_entries"])
    check("complete_Q36_scope_exact", packet["complete_Q36_current_scope_credit"] == c_by_id["Q36"])

    gap = report["coverage_decisions"][0]
    scope = report["scope_decisions"][0]
    check("all170_compared_ID_record", gap["all170_coverage_comparison"]["all_IDs_compared"] == [x["id"] for x in reconstructed])
    check("retained_gap_exact_packet", gap["original_proposal"] == packet["complete_retained_set"]["remaining_gaps"][0])
    check("scope_finding_exact_packet", scope["original_finding"] == packet["complete_retained_set"]["scope_findings"][0])
    check("Q36_old_scope_exact", scope["complete_old_scope_entry"] == c_by_id["Q36"])
    check("Q36_preserved_full_question_key_map", scope["complete_Q36_question_key_map"] == next(x for x in packet["complete_selected_current_entries"] if x["question"]["id"] == "Q36"))
    check("Q36_split_preserves_four_facts", [scope["unsupported_clause"]["exact_asked_fact"]] + scope["supported_clauses"] == reconstructed[35]["all_asked_facts"] and len(reconstructed[35]["all_asked_facts"]) == 4)

    for index, correction in enumerate(report["source_transcription_decisions"]):
        finding = packet["complete_retained_set"]["source_evidence_findings"][index]
        check(f"correction{index}:exact_packet_finding", correction["original_finding"] == finding)
        check(f"correction{index}:old_fragment_exact", correction["exact_old_fragment"] == finding["exact_old_text"])
        for prefix, text_key, hash_key in [
            ("old_fragment", "exact_old_fragment", "old_fragment_utf8_sha256"),
            ("new_fragment", "exact_corrected_fragment", "corrected_fragment_utf8_sha256"),
        ]:
            check(f"correction{index}:{prefix}_hash", utf8hash(correction[text_key]) == correction[hash_key])
        owned = correction["own_prior_transcription_correction"]
        old_row = owned["original_image_row"]
        check(f"correction{index}:exact_own_original_image_row", old_row in prior11["image_files"])
        check(f"correction{index}:original_ledger_hash", owned["original_ledger_path"] == str(B / "coverage-novelty-adjudication-11-read-ledger.json") and owned["original_ledger_sha256"] == EXPECTED["coverage-novelty-adjudication-11-read-ledger.json"])
        check(f"correction{index}:old_full_exact", owned["exact_old_full_transcription"] == old_row["transcription"])
        check(f"correction{index}:old_full_hash", utf8hash(owned["exact_old_full_transcription"]) == owned["old_full_transcription_utf8_sha256"])
        check(f"correction{index}:new_full_hash", utf8hash(owned["exact_proposed_corrected_full_transcription"]) == owned["corrected_full_transcription_utf8_sha256"])
        old, new = ("Cost 4", "Cost 3") if index == 0 else ("Threshold 3 Moon", "Threshold 3 Animal")
        check(f"correction{index}:only_specified_fragment_replacement", correction["exact_old_fragment"].replace(old, new) == correction["exact_corrected_fragment"])
        check(f"correction{index}:only_specified_full_replacement", owned["exact_old_full_transcription"].replace(old, new) == owned["exact_proposed_corrected_full_transcription"])
        check(f"correction{index}:fresh_native_row_exact", correction["native_source"] in ledger["fresh_full_native_views"])
        check(f"correction{index}:same_native_file_binding", old_row["path"] == correction["native_source"]["path"] and old_row["original_byte_sha256"] == correction["native_source"]["original_byte_sha256"])
        check(f"correction{index}:actual_ask_exact", correction["actual_current_ask"] == next(x for x in reconstructed if x["id"] == correction["actual_current_ask"]["id"]))
    counts["explicit_transcription_corrections"] = len(report["source_transcription_decisions"])

    # Every report copy of an operative passage/native row must bind the same evidence.
    known_passages = ledger["source_passages"]
    known_images = ledger["fresh_full_native_views"]
    copies = {"passages": 0, "native_rows": 0}
    def walk(value):
        if isinstance(value, dict):
            if "complete_operative_passage" in value:
                copies["passages"] += 1
                check(f"report_passage_copy{copies['passages']}", value in known_passages)
            if value.get("full_native_view") is True:
                copies["native_rows"] += 1
                check(f"report_native_copy{copies['native_rows']}", value in known_images)
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)
    walk(report)
    counts["report_operative_passage_copies"] = copies["passages"]
    counts["report_native_row_copies"] = copies["native_rows"]
    new_facts = [f for c in gap["minimal_asked_only_map"]["requested_clauses"] for f in c["required_facts"]]
    check("one_minimal_new_fact_exact", new_facts == gap["minimum_new_required_facts"] and len(new_facts) == gap["minimum_new_required_fact_count"] == 1)
    accounting = report["required_fact_accounting"]
    check("accounting_170_505_to171_506", accounting["current_questions"] == 170 and accounting["current_required_facts"] == 505 and accounting["new_distinct_coverage_questions"] == 1 and accounting["new_distinct_required_facts"] == 1 and accounting["proposed_questions_if_consolidated"] == 171 and accounting["proposed_required_facts_if_consolidated"] == 506)


try:
    run()
except Exception as error:
    check("validator_runtime_exception", False, detail=f"{type(error).__name__}: {error}")
for path, before in list(snapshots.items()):
    check("input_preserved:" + path, digest(Path(path).read_bytes()) == before)
failures = [x for x in checks if not x["ok"]]
filesystem = [x for x in checks if x["kind"] == "filesystem"]
attestations = [x for x in checks if x["kind"] != "filesystem"]
result = {
    "task": "Novelty14 evidence validation only; no semantic re-review or coverage verdict",
    "status": "VALID_FOR_RECORDED_EVIDENCE" if not failures else "EVIDENCE_FAILURES",
    "validator": str(Path(__file__).resolve()),
    "validator_sha256": digest(Path(__file__).read_bytes()),
    "check_count": len(checks),
    "filesystem_check_count": len(filesystem),
    "recorded_attestation_check_count": len(attestations),
    "counts": counts,
    "immutable_expected_sha256": EXPECTED,
    "authorized_validation_only_machine_bank_access": machine_only_bank_access,
    "access_history_boundary": "These four bank-file accesses occur only in this later authorized validation. They do not change adjudication14's earlier access history, become fresh model text delivery, or alter the preserved report/ledger.",
    "proof_boundaries": {
        "filesystem_proven": "Exact bytes/hashes, Unicode ranges, slice content, contiguity, entry equality, source/image binding, dimensions/bounds, all170/all505 reconstruction, transcription before/after arithmetic and unchanged inputs.",
        "tool_attestations_only": "Output caps, no-truncation flags and historical full-view flags are checked as recorded attestations; filesystem evidence alone cannot prove actual historical tool delivery.",
        "perception_attestations_only": "Native Growth-band transcription and reading Cost3/3Animal were performed in the original adjudication. This validator checks text/image bindings and hashes, and does not OCR, replay views or newly judge those perceptions.",
    },
    "exceptions": failures,
    "derived_growth_transcription_hashes": transcription_digests,
    "checks": checks,
}
OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"status": result["status"], "checks": len(checks), "filesystem_checks": len(filesystem), "attestation_checks": len(attestations), "exceptions": len(failures), "counts": counts, "output": str(OUTPUT), "output_sha256": digest(OUTPUT.read_bytes()), "validator_sha256": result["validator_sha256"]}))
raise SystemExit(0 if not failures else 1)
