"""Independent coordinator checks for a saved reader iteration; does not grade rules."""
from collections import Counter
from pathlib import Path
import argparse
import hashlib
import json

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("iteration", type=Path)
parser.add_argument("--canonical", type=Path)
args = parser.parse_args()
iteration = args.iteration.resolve()
questions = json.loads((iteration / "questions.json").read_text())["questions"]
results = json.loads((iteration / "results.json").read_text())
expected_ids = [str(item["id"]) for item in questions]
checks = {"question_ids_unique": len(expected_ids) == len(set(expected_ids))}
details = {}

for label, result in results["readers"].items():
    reader_name = label.lower().removeprefix("reader-").removeprefix("reader_")
    reader = json.loads((iteration / f"reader-{reader_name}.json").read_text())
    answers = reader["answers"]
    grades = result["grades"]
    answer_map = {str(item["id"]): item for item in answers}
    checks[f"{label}_answer_ids_exactly_once"] = Counter(str(item["id"]) for item in answers) == Counter(expected_ids)
    checks[f"{label}_grade_ids_exactly_once"] = Counter(str(item["id"]) for item in grades) == Counter(expected_ids)
    tallies = Counter(item["grade"].lower() for item in grades)
    totals = result.get("counts", result.get("totals", {key: result.get(key) for key in ("correct", "partial", "incorrect")}))
    checks[f"{label}_totals_match_saved_grades"] = all(tallies[key] == totals.get(key, 0) for key in ("correct", "partial", "incorrect"))
    checks[f"{label}_all_correct"] = tallies["correct"] == len(expected_ids) and len(tallies) == 1
    observed_matches = []
    for grade in grades:
        observed_key = next((key for key in ("observed_answer", "observed", "actual_answer") if key in grade), None)
        if observed_key is None:
            continue
        observed = grade[observed_key]
        answer = answer_map.get(str(grade["id"]))
        observed_matches.append(observed == answer if isinstance(observed, dict) else answer is not None and observed == answer["answer"])
    checks[f"{label}_saved_observed_answers_match_raw"] = all(observed_matches) and len(observed_matches) == len(expected_ids)
    unsupported = [item["id"] for item in grades if item.get("unsupported_guess") or item.get("unsupported_correct_guess")]
    checks[f"{label}_no_flagged_unsupported_guesses"] = not unsupported and not result.get("unsupported_guesses", 0)
    details[label] = {"grades": dict(tallies), "unsupported_guess_ids": unsupported, "inputs_read": reader.get("inputs_read")}

manifest = json.loads((iteration / "input-manifest.json").read_text())
hashes = manifest.get("hashes", manifest.get("sha256", manifest.get("files", {})))
if not hashes and isinstance(manifest.get("inputs"), list):
    hashes = {entry["path"]: entry["sha256"] for entry in manifest["inputs"]}
elif not hashes and isinstance(manifest.get("inputs"), dict):
    hashes = manifest["inputs"]
hash_details = {}
for name, value in hashes.items():
    expected = value.get("sha256") if isinstance(value, dict) else value
    file_path = Path(value.get("path", name) if isinstance(value, dict) else name)
    if not file_path.is_absolute():
        local_input = iteration / file_path
        file_path = local_input if local_input.exists() else Path.cwd() / file_path
    if not file_path.exists():
        hash_details[name] = "missing"
        continue
    actual = hashlib.sha256(file_path.read_bytes()).hexdigest()
    hash_details[name] = actual == expected
checks["frozen_input_hashes_match"] = bool(hash_details) and all(value is True for value in hash_details.values())
if args.canonical:
    checks["canonical_matches_snapshot"] = args.canonical.read_bytes() == (iteration / "summary-snapshot.md").read_bytes()

output = {"iteration": str(iteration), "question_count": len(expected_ids), "checks": checks, "reader_details": details, "input_hash_checks": hash_details, "mechanical_checks_pass": all(checks.values()), "scope": "Mechanical evidence integrity only. Source/key accuracy, grading semantics, context isolation, coverage saturation, and runtime model provenance require separate evidence review."}
print(json.dumps(output, indent=2))
