#!/usr/bin/env python3
"""Validate adjudication15 evidence and equivalence; do not reassess novelty."""
import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
OUTPUT = B / "novelty15-delivery-validation.json"
EXPECTED = {
    "working-novelty-adjudication-15.json": "fa3712d95582a2749dbe91fc0c27aaf4e3da3bcd150959fec83926f009920b83",
    "working-novelty-adjudication-15-read-ledger.json": "ead18d716f80666343968cf9819e86c294066271bcc7f475b8beb969801270e6",
    "working-novelty15-input.json": "9a319c7caa97caef6a8010acc3ac7f45e94e1aa10ad59945c1636fd001b86d13",
    "novelty15-all171-actual-asks.jsonl": "b7151bcffcaad7ea978f9e8593f085bccfbc50f48396208063ae447fae9d93d8",
    "coverage-novelty-adjudication-11-read-ledger.json": "eca65d91d99ba2a1934cc6e35bed43a7de60e627335a24cf99178bd65c77a546",
}
checks = []
snapshots = {}
counts = {}
bank_access = []


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def hs(text):
    return digest(text.encode("utf-8"))


def raw(path):
    path = Path(path)
    value = path.read_bytes()
    snapshots.setdefault(str(path), digest(value))
    return value


def obj(path):
    return json.loads(raw(path))


def check(name, condition, kind="filesystem", detail=None):
    row = {"check": name, "kind": kind, "ok": bool(condition)}
    if detail is not None:
        row["detail"] = detail
    checks.append(row)


def check_slice(text, part, label):
    a, z = part["range"]
    check(label + ":bounds", 0 <= a < z <= len(text) and z - a <= 6000)
    check(label + ":utf8_slice_hash", hs(text[a:z]) == part["slice_utf8_sha256"])
    check(label + ":recorded_cap", part["output_cap_tokens"] >= 4000, "historical_tool_attestation")
    check(label + ":recorded_no_truncation", part["truncated"] is False, "historical_tool_attestation")


def complete(row, label):
    data = raw(row["path"])
    text = data.decode("utf-8")
    check(label + ":file_hash", digest(data) == row["original_byte_sha256"])
    check(label + ":unicode_length", len(text) == row["character_length"])
    end = 0
    for index, part in enumerate(row["slices"]):
        check(f"{label}:slice{index}:contiguous", part["range"][0] == end)
        check_slice(text, part, f"{label}:slice{index}")
        end = part["range"][1]
    check(label + ":complete_range", end == len(text))
    check(label + ":complete_delivery_flag", row["contiguous_complete"] is True, "historical_tool_attestation")
    return len(row["slices"])


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
    for name, expected in EXPECTED.items():
        check("immutable_expected_hash:" + name, digest(raw(B / name)) == expected)
    report = obj(B / "working-novelty-adjudication-15.json")
    ledger = obj(B / "working-novelty-adjudication-15-read-ledger.json")
    packet = obj(B / "working-novelty15-input.json")
    oldledger = obj(B / "coverage-novelty-adjudication-11-read-ledger.json")
    check("report_ledger_path", report["read_ledger_path"] == str(B / "working-novelty-adjudication-15-read-ledger.json"))
    check("report_packet_binding", report["input_packet"]["sha256"] == EXPECTED["working-novelty15-input.json"] and report["input_packet"]["character_length"] == 15656)

    new = ledger["new_complete_text_inputs"]
    counts["new_complete_input_files"] = len(new)
    counts["new_complete_input_slices"] = sum(complete(row, "new:" + row["path"]) for row in new)
    check("complete_input_set", {Path(row["path"]).name for row in new} == {"working-novelty15-input.json", "novelty15-all171-actual-asks.jsonl", "scope-reachability-steering-2026-11-05.txt"})
    reuse = ledger["own_exact_complete_primary_source_reuse"]
    check("reuse_original_ledger_exact", reuse["original_ledger_path"] == str(B / "coverage-novelty-adjudication-11-read-ledger.json") and reuse["original_ledger_sha256"] == EXPECTED["coverage-novelty-adjudication-11-read-ledger.json"])
    oldrow = reuse["original_complete_delivery_row"]
    check("reuse_exact_original_full_row", oldrow in oldledger["text_files"])
    counts["reused_complete_CORE_slices"] = complete(oldrow, "original_CORE")
    check("sixteen_reused_CORE_slices", counts["reused_complete_CORE_slices"] == 16)
    intervals = {}
    for index, row in enumerate(ledger["targeted_primary_rereads"]):
        data = raw(row["path"])
        text = data.decode()
        check(f"targeted{index}:original_file_binding", row["path"] == oldrow["path"] and digest(data) == row["original_byte_sha256"] == oldrow["original_byte_sha256"])
        check(f"targeted{index}:original_length", len(text) == row["character_length"] == oldrow["character_length"])
        check_slice(text, row, f"targeted{index}")
        intervals.setdefault(row["path"], []).append(row["range"])
    counts["new_targeted_primary_slices"] = len(ledger["targeted_primary_rereads"])
    counts["all_new_recorded_slices"] = counts["new_complete_input_slices"] + counts["new_targeted_primary_slices"]
    check("twenty_new_slices_exact", counts["all_new_recorded_slices"] == ledger["successful_new_text_slice_count"] == report["delivery_summary"]["successful_new_text_slice_count"] == 20)
    check("no_image_perception_claims", ledger["native_images_required_or_viewed"] == [])

    operative = ledger["primary_operative_passages"]
    for index, entry in enumerate(operative):
        data = raw(entry["path"])
        text = data.decode()
        a, z = entry["character_range"]
        check(f"operative{index}:original_source_hash", digest(data) == entry["original_byte_sha256"] == oldrow["original_byte_sha256"])
        check(f"operative{index}:exact_range_text_hash", 0 <= a < z <= len(text) and text[a:z] == entry["complete_operative_passage"] and hs(text[a:z]) == entry["passage_utf8_sha256"])
        check(f"operative{index}:fresh_reread_coverage", covered(a, z, intervals[entry["path"]]))
    counts["operative_primary_passages"] = len(operative)
    decision = report["decisions"][0]
    check("report_passage_copies_exact", decision["primary_sources"] == operative)
    urgency = operative[0]
    check("packet_primary_passage_exact", packet["complete_retained_set"][0]["primary_passage"] == urgency["complete_operative_passage"])
    printedref = packet["complete_retained_set"][0]["primary_sources"][0]
    check("packet_primary_reference_exact", printedref["path"] == urgency["path"] and printedref["sha256"] == urgency["original_byte_sha256"] and printedref["character_range"] == urgency["character_range"] and printedref["passage_sha256"] == urgency["passage_utf8_sha256"])
    keyref = decision["proposed_fixed_key"]["source_refs"][0]
    check("proposed_key_source_reference_exact", keyref == {"path": urgency["path"], "sha256": urgency["original_byte_sha256"], "character_range": urgency["character_range"], "passage_sha256": urgency["passage_utf8_sha256"]})

    # These four file accesses are authorized only for this later equivalence check.
    bank = {}
    bindings = packet["current_bank"]["hashes"]
    check("exact_four_authorized_bank_paths", set(bindings) == {str(B / "expanded-v20" / name) for name in ["questions.json", "answer-key.json", "asked-fact-map.json", "core-scope-credit.json"]})
    check("ledger_bank_bindings_exact_packet", ledger["current_bank_bindings_supplied_only"] == bindings)
    for path, expected in bindings.items():
        data = raw(path)
        check("authorized_bank_hash:" + Path(path).name, digest(data) == expected)
        bank[Path(path).name] = json.loads(data)
        bank_access.append({"path": path, "sha256": digest(data), "purpose": "Authorized later evidence-validation-only machine parsing/hashing; no model delivery of whole rule text."})
    questions = bank["questions.json"]["questions"]
    keys = bank["answer-key.json"]["answers"]
    maps = bank["asked-fact-map.json"]["questions"]
    qid = {x["id"]: x for x in questions}
    kid = {x["id"]: x for x in keys}
    mid = {x["id"]: x for x in maps}
    check("all171_unique_ordered_IDs", len(qid) == len(kid) == len(mid) == 171 and [x["id"] for x in questions] == [f"Q{i:02d}" for i in range(1, 172)] == [x["id"] for x in keys] == [x["id"] for x in maps])
    reconstructed = []
    for question in questions:
        mapping = mid[question["id"]]
        check("literal_question_map_equality:" + question["id"], question["question"] == mapping["question"])
        reconstructed.append({"id": question["id"], "literal_question": question["question"], "all_asked_facts": [f for c in mapping["requested_clauses"] for f in c["required_facts"]]})
    ask_path = B / "novelty15-all171-actual-asks.jsonl"
    ask_text = raw(ask_path).decode()
    actual = [json.loads(line) for line in ask_text.splitlines() if line.strip()]
    check("all171_all506_exact_projection_objects", actual == reconstructed)
    trailing_newlines = len(ask_text) - len(ask_text.rstrip("\n"))
    serialized = "\n".join(json.dumps(row, ensure_ascii=False) for row in reconstructed) + "\n" * trailing_newlines
    check("all171_projection_exact_serialized_bytes", serialized.encode() == raw(ask_path))
    counts["projection_trailing_newlines"] = trailing_newlines
    counts["current_questions"] = len(reconstructed)
    counts["current_asked_facts"] = sum(len(row["all_asked_facts"]) for row in reconstructed)
    check("171_questions506_facts", counts["current_questions"] == 171 and counts["current_asked_facts"] == bank["asked-fact-map.json"]["required_fact_count"] == 506)
    check("compared_ID_record_exact", decision["all171_actual_ask_comparison"]["all_IDs_compared"] == [x["id"] for x in reconstructed])
    selected = packet["complete_selected_nearest_entries"]
    check("selected_ID_set_exact", [x["question"]["id"] for x in selected] == ["Q55", "Q129", "Q134"])
    for row in selected:
        ident = row["question"]["id"]
        check("selected_question_exact:" + ident, row["question"] == qid[ident])
        check("selected_full_key_exact:" + ident, row["key"] == kid[ident])
        check("selected_full_map_exact:" + ident, row["asked_map"] == mid[ident])
    counts["selected_full_entries"] = len(selected)
    check("report_selected_full_entries_exact", [x["complete_current_question_key_map"] for x in decision["closest_existing_actual_ask_comparisons"]] == selected)
    check("original_proposal_exact_packet", decision["original_retained_proposal"] == packet["complete_retained_set"][0])
    check("literal_question_preserved", decision["literal_surviving_pretest_question"] == packet["complete_retained_set"][0]["proposed_question"])
    minimal = [f for c in decision["minimal_asked_only_map"]["requested_clauses"] for f in c["required_facts"]]
    check("one_minimal_required_fact_exact", minimal == decision["minimum_required_facts"] and len(minimal) == decision["minimum_required_fact_count"] == 1)
    check("single_complete_retained_set", len(report["decisions"]) == report["complete_retained_set_size"] == len(packet["complete_retained_set"]) == 1)
    accounting = report["required_fact_accounting"]
    check("one_fact172_507_arithmetic", accounting["current_questions"] == 171 and accounting["current_required_facts"] == 506 and accounting["new_questions"] == accounting["new_required_facts"] == 1 and accounting["proposed_questions_if_consolidated"] == 172 and accounting["proposed_required_facts_if_consolidated"] == 507)


try:
    run()
except Exception as error:
    check("validator_runtime_exception", False, detail=f"{type(error).__name__}: {error}")
for path, before in list(snapshots.items()):
    check("input_unchanged:" + path, digest(Path(path).read_bytes()) == before)
exceptions = [x for x in checks if not x["ok"]]
filesystem = [x for x in checks if x["kind"] == "filesystem"]
attestations = [x for x in checks if x["kind"] != "filesystem"]
result = {
    "task": "Evidence validation only; no new semantic adjudication, novelty review or global coverage verdict",
    "status": "VALID_FOR_RECORDED_EVIDENCE" if not exceptions else "EVIDENCE_FAILURES",
    "validator": str(Path(__file__).resolve()),
    "validator_sha256": digest(Path(__file__).read_bytes()),
    "check_count": len(checks),
    "filesystem_check_count": len(filesystem),
    "historical_attestation_check_count": len(attestations),
    "counts": counts,
    "immutable_expected_sha256": EXPECTED,
    "authorized_validation_only_machine_bank_access": bank_access,
    "access_history_boundary": "The four v20 bank files are accessed only for this subsequently authorized machine equivalence validation. This does not retroactively change adjudication15's earlier access history or constitute fresh whole-file model text delivery.",
    "proof_boundaries": {
        "filesystem": "Verifies exact original bytes/hashes, Unicode lengths/ranges, slice content and contiguity, original owned ledger rows, primary passage text/hashes, exact171/506 reconstruction, selected entries, declared fact-count arithmetic and input preservation.",
        "historical_tools": "Caps, no-truncation flags and complete-delivery flags are checked as recorded historical tool attestations. Filesystem evidence alone cannot independently prove historical transport or perception.",
        "perception": "No image views are claimed for adjudication15. Interpretation of the primary text and the novelty decision are preserved rather than semantically re-reviewed.",
    },
    "exceptions": exceptions,
    "checks": checks,
}
OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"status": result["status"], "checks": len(checks), "filesystem_checks": len(filesystem), "attestation_checks": len(attestations), "exceptions": len(exceptions), "counts": counts, "output": str(OUTPUT), "output_sha256": digest(OUTPUT.read_bytes()), "validator_sha256": result["validator_sha256"]}))
raise SystemExit(0 if not exceptions else 1)
