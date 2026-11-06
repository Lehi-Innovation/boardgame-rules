"""Refresh the coordinator manifest/report from worker-owned progress files."""
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import json

base = Path(__file__).parent
path = base / "manifest.json"
manifest = json.loads(path.read_text())
for game in manifest["games"]:
    status_path = Path(game["output_directory"]) / "game-status.json"
    if status_path.exists():
        state = json.loads(status_path.read_text())
        game["worker_progress"] = state
        for key in ("question_count", "iterations", "final_reader_scores", "source_audit", "report_path", "blocking_reason"):
            if key == "source_audit" and game.get("status") == "complete":
                # Keep the coordinator's accepted exact-byte audit/path after closure.
                continue
            if state.get(key) is not None:
                game[key] = state[key]
        if game.get("coordinator_completion_scores"):
            game["final_reader_scores"] = game["coordinator_completion_scores"]
        game["worker_status"] = state.get("status")
        if game.get("status") != "complete":
            game["phase"] = state.get("phase")
        # Count actual reader trials, not prepared directories or worker list length.
        def has_responses(p):
            try:
                data = json.loads(p.read_text())
                return bool(data.get("answers", [])) if isinstance(data, dict) else bool(data)
            except (OSError, ValueError):
                return False

        trials = sorted({p.parent for name in ("reader-a.json", "reader-b.json",
                                               "reader-a-draft*.json", "reader-b-draft*.json")
                         for p in Path(game["output_directory"]).rglob(name)
                         if (p.parent / "summary-snapshot.md").exists() and has_responses(p)})
        game["iteration_inventory"] = {
            "executed_trials": len(trials),
            "complete_pairs": sum(all(has_responses(p / name) for name in
                                      ("reader-a.json", "reader-b.json")) for p in trials),
            "trials": [{"name": p.name,
                        "reader_a": has_responses(p / "reader-a.json"),
                        "reader_b": has_responses(p / "reader-b.json"),
                        "reader_a_draft": any(has_responses(f) for f in p.glob("reader-a-draft*.json")),
                        "reader_b_draft": any(has_responses(f) for f in p.glob("reader-b-draft*.json")),
                        "invalid_model_gate_diagnostic": (p / "invalid-model-gate-diagnostic.json").exists(),
                        "graded_export": (p / "results.json").exists()} for p in trials],
        }
manifest["updated_at"] = datetime.now(ZoneInfo("America/Phoenix")).isoformat()
path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")

rows = []
for game in manifest["games"]:
    title = game.get("chat_title", game["game"])
    chat = f'[{title}](codex://threads/{game["thread_id"]})' if game.get("thread_id") else "Queued"
    report_path = game.get("report_path")
    if report_path:
        report_target = Path(report_path)
        if not report_target.is_absolute():
            report_target = Path.cwd() / report_target
        report = f'[Report]({report_target})'
    else:
        report = "Pending"
    scores = game.get("final_reader_scores")
    if isinstance(scores, dict) and any(key in scores for key in ("a", "reader_a")):
        size = scores.get("out_of", game.get("question_count"))
        parts = []
        for letter in ("a", "b"):
            value = scores.get(letter, scores.get("reader_" + letter))
            correct = value.get("correct") if isinstance(value, dict) else value
            parts.append(f'{letter.upper()}: {correct}/{size}')
        scores = "; ".join(parts)
    elif scores is not None:
        scores = json.dumps(scores, ensure_ascii=False)
    progress = game.get("worker_progress", {})
    if scores and game["status"] not in ("complete", "awaiting-source"):
        final_path = progress.get("final_snapshot_path")
        matches = False
        if final_path:
            try:
                matches = Path(final_path).read_bytes() == Path(game["summary_path"]).read_bytes()
            except OSError:
                pass
        if progress.get("status") != "ready-for-coordinator" or not matches:
            scores = "Pending exact final text"
    inventory = game.get("iteration_inventory", {})
    iterations = inventory.get("executed_trials", game.get("iterations"))
    if isinstance(iterations, list):
        iterations = len(iterations)
    if inventory.get("complete_pairs", iterations) != iterations:
        iterations = f'{iterations} trials ({inventory["complete_pairs"]} pairs)'
    audit = game.get("source_audit") or "Pending"
    if isinstance(audit, dict):
        if audit.get("complete_core") == "NOT_ESTABLISHED" or "fidelity only" in str(audit.get("verdict_scope", "")).lower() or "fidelity only" in str(audit.get("scope", "")).lower():
            audit = str(audit.get("verdict")) + " (source fidelity only)"
        else:
            audit = audit.get("verdict", str(audit))
    if game["status"] not in ("complete", "awaiting-source") and progress:
        if progress.get("status") != "ready-for-coordinator":
            audit = "Pending final text"
    status = game["status"]
    if status != "complete":
        status += ": " + (game.get("phase") or game.get("worker_status") or "")
    rows.append(f'| {game["game"]} | {game.get("question_count") or "—"} | {iterations or "—"} | {scores or "—"} | {audit} | {status} | {chat} | {report} |')

report = "# Multi-game rules-summary QA batch\n\n"
report += f'Run `{manifest["run_id"]}`. Updated {manifest["updated_at"]}.\n\n'
report += "At most three game chats run concurrently, in the existing local checkout. Game evaluators/reviewers use gpt-6.1-sol/high; blind readers use gpt-6-luna/high. No commits or pushes are authorized.\n\n"
report += "| Game | Questions | Iterations | Final reader scores | Source audit | Status | Chat | Evidence |\n|---|---:|---:|---|---|---|---|---|\n"
report += "\n".join(rows) + "\n\n"
report += "Iterations count trials with actual saved reader responses, including stopped partial drafts; prepared but undispatched candidates and copies of an existing pair are excluded. Complete pairs are identified separately when a trial is partial. Historical invalid or nonpassing trials remain in the count and evidence.\n\n"
blockers = [game for game in manifest["games"] if game.get("blocking_reason") and game["status"] != "complete"]
if blockers:
    report += "## Outstanding external inputs\n\n"
    for game in blockers:
        report += f'- **{game["game"]}:** {game["blocking_reason"]}\n'
    report += "\n"
if any(game.get("coordinator_completion_scores") for game in manifest["games"]):
    report += "Rows with source-unresolved questions use the coordinator’s strict resolved-answer counts: an unresolved requested ruling is partial even when a response correctly describes the source limitation. Original factual-key-match grades and raw responses are retained; see [Nemesis completion grading](nemesis-coordinator-completion-results.json) and [incomplete review](nemesis-coordinator-incomplete-review.json).\n\n"
report += "Completion requires working coverage saturation in the documented source/scope, a resolved independent coverage challenge, two fresh full-bank Luna N/N results, independent source-audit PASS, verified model/input integrity, exact canonical snapshot equality, and repository checks. A partial result remains incomplete. This does not prove every conceivable scenario is covered.\n\n"
if any(game.get("source_gap_reporting_question_ids") for game in manifest["games"]):
    report += "Dead Last’s 27/27 figures are factual quiz results including Q26, which correctly reports that the booklet omits a multiway Showdown procedure. That answer does not resolve the missing gameplay ruling; full-core completion remains awaiting-source.\n\n"
report += "See [manifest](manifest.json), [identity/source decisions](identity-and-source-decisions.md), [initial checkout status](initial-git-status.txt), and [initial catalog check](initial-catalog-check.txt). Shared-file baseline copies are in `baseline-shared/`; worker assignments and historical failed iterations must remain intact.\n"
(base / "README.md").write_text(report)
print(json.dumps([{k: game.get(k) for k in ("slug", "status", "phase", "question_count", "worker_status")} for game in manifest["games"]], indent=2))
