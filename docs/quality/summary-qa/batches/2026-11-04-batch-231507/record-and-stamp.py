"""Record one reviewed independent verdict through the audit workflow; stamp only its game."""
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from zoneinfo import ZoneInfo
import argparse
import hashlib
import json
import os
import re
import shutil
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[5]))
import yaml
from scripts import audit
from scripts.stamp_verification import load_audit_results, stamp_file

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("slug")
parser.add_argument("--audit", required=True, type=Path)
parser.add_argument("--summary-sha256", required=True)
parser.add_argument("--coordinator-check", required=True, type=Path)
parser.add_argument("--resolve-verification-date", action="store_true", help="Resolve the sole nonmaterial META-01 stale verification_date finding by this stamp; exact stamped retesting remains mandatory")
args = parser.parse_args()
base = Path(__file__).parent
manifest_path = base / "manifest.json"
manifest = json.loads(manifest_path.read_text())
game = next(game for game in manifest["games"] if game["slug"] == args.slug)
worker = json.loads((Path(game["output_directory"]) / "game-status.json").read_text())
assert worker["status"] == "ready-for-coordinator", "Worker is not ready for recording/stamping"
check = json.loads(args.coordinator_check.read_text())
assert check["mechanical_checks_pass"], "Coordinator iteration-integrity checks failed"
assert check["question_count"] == worker["question_count"], "Final full-bank count differs"
source_audit = json.loads(args.audit.read_text())
assert source_audit["verdict"] == "PASS" and not source_audit.get("material_findings"), "Independent audit must pass with no material findings"
date_findings = source_audit.get("findings", [])
if date_findings:
    assert args.resolve_verification_date and len(date_findings) == 1, "Unresolved findings require review; only the sole stale-date metadata fix is supported"
    finding = date_findings[0]
    assert finding.get("id") == "META-01" and finding.get("type") == "metadata" and finding.get("material") is False and "verification_date" in finding.get("location", ""), "Only a nonmaterial verification_date finding may be resolved by stamping"
elif args.resolve_verification_date:
    raise AssertionError("No stale-date finding exists to resolve")
summary = Path(game["summary_path"])
before = summary.read_bytes()
assert hashlib.sha256(before).hexdigest() == args.summary_sha256, "Summary changed after evidence review"
assert before == Path(worker["final_snapshot_path"]).read_bytes(), "Canonical no longer matches tested snapshot"

output = base / "recording" / (args.slug + "-" + datetime.now(ZoneInfo("America/Phoenix")).strftime("%Y%m%d-%H%M%S"))
output.mkdir(parents=True, exist_ok=False)
tracker_path = Path("docs/quality/semantic-audit-results.yaml")
audit_manifest_path = Path("docs/quality/semantic-audit-manifest.json")
shutil.copy2(tracker_path, output / "before-results.yaml")
shutil.copy2(audit_manifest_path, output / "before-manifest.json")
(output / "summary-before.md").write_bytes(before)
finding_note = "zero material findings; sole META-01 stale verification_date must be resolved by the associated stamp before final acceptance" if date_findings else "zero findings"
reason = f"Independent final source audit PASS, {finding_note}: {args.audit.as_posix()}; audited/tested canonical SHA-256 {args.summary_sha256}."
result_path = output / "audit-result.txt"
result_path.write_text(f"RESULT|{args.slug}|PASS|{reason}\n")

# Exercise the repository recording workflow on snapshots. Merge only this
# verdict into the latest live tracker, without marking unrelated audit batches.
audit.RESULTS_PATH = str(output / "recorded-results.yaml")
audit.MANIFEST_PATH = str(output / "recorded-manifest.json")
shutil.copy2(tracker_path, audit.RESULTS_PATH)
shutil.copy2(audit_manifest_path, audit.MANIFEST_PATH)
audit.cmd_record(SimpleNamespace(results_file=str(result_path), batch_ids=[]))
record = yaml.safe_load(Path(audit.RESULTS_PATH).read_text())[args.slug]
live_text = tracker_path.read_text()
live = yaml.safe_load(live_text)
replacement = yaml.safe_dump({args.slug: record}, sort_keys=True, allow_unicode=True, width=120)
pattern = re.compile(rf"(?ms)^{re.escape(args.slug)}:\n.*?(?=^\S|\Z)")
if pattern.search(live_text):
    updated_text = pattern.sub(lambda match: replacement, live_text, count=1)
else:
    updated_text = live_text.rstrip() + "\n" + replacement
updated = yaml.safe_load(updated_text)
assert {k: v for k, v in updated.items() if k != args.slug} == {k: v for k, v in live.items() if k != args.slug}
assert tracker_path.read_text() == live_text, "Audit tracker changed concurrently"
staging = tracker_path.with_suffix(".yaml.summary-qa-tmp")
staging.write_text(updated_text)
os.replace(staging, tracker_path)

stamp_date = datetime.now(ZoneInfo("America/Phoenix")).date().isoformat()
stamp_file(str(summary), load_audit_results(), stamp_date=stamp_date)
after = summary.read_bytes()
if date_findings:
    metadata = yaml.safe_load(after.decode().split("---", 2)[1])
    assert str(metadata["verification_date"]) == stamp_date and metadata["verification"] == "verified", "Stamp did not resolve the audited stale verification date"
(output / "summary-after.md").write_bytes(after)
result = {"game": args.slug, "independent_audit": str(args.audit.resolve()), "recorded_verdict": record, "unrelated_audit_verdicts_preserved": True, "global_audit_manifest_unchanged": audit_manifest_path.read_bytes() == (output / "before-manifest.json").read_bytes(), "summary_sha256_before": hashlib.sha256(before).hexdigest(), "summary_sha256_after": hashlib.sha256(after).hexdigest(), "stamping_changed_tested_bytes": before != after, "requires_full_bank_retest": before != after}
result["resolved_metadata_finding_ids"] = [finding["id"] for finding in date_findings]
(output / "validation.json").write_text(json.dumps(result, indent=2) + "\n")
game.update(status="stamped-retest-required" if before != after else "ready-for-publication", recording_evidence=str(output.resolve()), source_audit={"verdict": "PASS", "path": str(args.audit.resolve())})
manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
print(json.dumps(result, indent=2))
