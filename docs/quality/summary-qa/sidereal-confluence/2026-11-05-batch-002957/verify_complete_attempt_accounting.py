from pathlib import Path
import json,hashlib,datetime
ROOT=Path(__file__).resolve().parent
D=ROOT/"complete-attempt-accounting-01"
def read(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def canonical(z):return hashlib.sha256(json.dumps(z,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
dest=D/"validation.json";assert not dest.exists()
attempts=read(D/"attempts.json")["attempts"];questions=read(D/"questions.json")["questions"];keys=read(D/"answer-key.json")["answers"];scopes=read(D/"asked-facts.json")["questions"];ids=[q["id"] for q in questions]
assert len(ids)==86;qi={q["id"]:q for q in questions};ki={q["id"]:q for q in keys};si={q["id"]:q for q in scopes};facts=sum(len(q["required_facts"]) for q in keys);assert facts==256
raw={}
for who,spec in attempts.items():
 assert sha(spec["original_raw_path"])==sha(D/f"attempt-{who}-original.json")==spec["raw_sha256"]
 assert sha(D/f"summary-{who}.md")==sha(ROOT/spec["round"]/"summary-snapshot.md")==spec["summary_sha256"]
 for name in ["questions.json","answer-key.json","asked-facts.json"]:assert (D/name).read_bytes()==(ROOT/spec["round"]/name).read_bytes()
 answers=read(D/f"attempt-{who}-original.json")["answers"];assert len(answers)==len({a["id"] for a in answers})==86 and {a["id"] for a in answers}==set(ids);raw[who]={a["id"]:a for a in answers}
results=read(D/"results.json");assert len(results["readers"]["a"])==len(results["readers"]["b"])==86;assert sum(results["totals"].values())==172;assert not results["missing_unsupported_guessing_assessments"]
blocks=sorted(D.glob("grading-block-??.json"));grades=sorted(D.glob("grades-block-??.json"));assert len(blocks)==len(grades)==5
seen=[]
for block in blocks:
 b=read(block)
 for who in ["a","b"]:
  binding=b["reader_summary_bindings"][who];assert binding["path"]==str(D/f"summary-{who}.md") and binding["sha256"]==sha(binding["path"])
 for name,h in b["source_raw_hashes"].items():assert sha(D/name)==h
 for entry in b["records"]:
  i=entry["id"];seen.append(i);assert entry["question"]==qi[i] and entry["key"]==ki[i] and entry["asked_scope"]==si[i]
  for who in ["a","b"]:assert entry[f"reader_{who}_original_entry"]==raw[who][i] and entry["original_entry_canonical_hashes"][who]==canonical(raw[who][i])
assert len(seen)==len(set(seen))==86 and set(seen)==set(ids)
proofs=[]
for grade in grades:
 report=read(grade);proof=read(D/(grade.stem+"-runtime-delivery.json"));assert proof["validation"]=="PASS" and proof["report_sha256"]==sha(grade) and proof["all_text_inputs_before_first_report_write"]
 assert {Path(x["file"]).name for x in proof["input_delivery"]}=={"summary-a.md","summary-b.md",grade.name.replace("grades-block-","grading-block-")}
 assert len(proof["input_delivery"])==3 and proof["model_records"] and all(x["actual_model"]=="gpt-6.1-sol" and x["actual_effort"]=="high" for x in proof["model_records"])
 for f in proof["input_delivery"]:assert sha(f["file"])==f["sha256"]
 for who in ["a","b"]:
  body=report["readers"][who];assert Path(body["bound_summary"]).name==f"summary-{who}.md"
  aggregated={x["id"]:x for x in results["readers"][who]}
  for row in body["results"]:
   assert aggregated[row["id"]]["original_grade_record"]==row
   assert isinstance(row.get("unsupported_guessing"),bool)
   fs=row["required_facts"];assert len(fs)==len({f["id"] for f in fs})==len(ki[row["id"]]["required_facts"]) and {f["id"] for f in fs}=={f["id"] for f in ki[row["id"]]["required_facts"]}
   assert all(isinstance(f["match"],bool) for f in fs)
   if row["grade"].lower()=="correct":assert all(f["match"] for f in fs) and row["unsupported_guessing"] is False
 proofs.append({"report":str(grade),"report_sha256":sha(grade),"runtime_delivery_proof":str(D/(grade.stem+"-runtime-delivery.json")),"all_three_inputs_before_first_report_write":True})
runtime=read(ROOT/"runtime-provenance.json");models=[]
for i in range(1,6):
 task=f"/root/historical_output_grader_{i:02}";record=next(z for z in runtime["records"] if z["task"]==task)
 assert record["request"]["requested_model"]=="gpt-6.1-sol" and record["request"]["requested_effort"]=="high" and record["request"]["requested_fork_turns"]=="none"
 assert record["turn_context_records"] and all(z["actual_model"]=="gpt-6.1-sol" and z["actual_effort"]=="high" for z in record["turn_context_records"]);models.append({"task":task,"actual_model":"gpt-6.1-sol","actual_effort":"high","fork_none_requested":True})
prior=read(ROOT/"completed-output-grade-inventory-before-accounting.json");inventory=[]
for row in prior["already_graded_complete_outputs"]:
 assert sha(row["path"])==row["sha256"] and sha(row["grade_authority"])==row["grade_authority_sha256"];inventory.append({**row,"factual_grades_recorded":True})
for who,spec in attempts.items():
 old=next(z for z in prior["additional_complete_outputs_pending_factual_grades"] if z["path"]==spec["original_raw_path"]);assert old["sha256"]==sha(old["path"])
 inventory.append({**old,"grade_authority":str(D/"results.json"),"grade_authority_sha256":sha(D/"results.json"),"accounting_reader_key":who,"own_frozen_summary":str(D/f"summary-{who}.md"),"own_frozen_summary_sha256":spec["summary_sha256"],"scores":results["reader_scores"][who],"graded_ids_exactly_once":True,"all_original_frozen_fact_atoms_graded":True,"factual_grades_recorded":True,"process_deviation_recorded_separately":True})
assert len(inventory)==24 and sum(z["entries"] for z in inventory)==1648 and len({z["path"] for z in inventory})==24
out_inventory=ROOT/"completed-output-grade-inventory.json";assert not out_inventory.exists();out_inventory.write_text(json.dumps({"status":"ALL_COMPLETE_OUTPUTS_HAVE_FACTUAL_GRADES","complete_outputs":24,"complete_entry_records":1648,"outputs":inventory,"historical_targets_preserved":True,"no_process_label_used_as_factual_grade":True},indent=2)+"\n")
selected=read(ROOT/"full-iteration-08/results.json");assert selected["PASS"] and selected["reader_scores"]=={"a":{"correct":86,"partial":0,"incorrect":0},"b":{"correct":86,"partial":0,"incorrect":0}}
current_sha=sha(Path("/home/jonny/projects/boardgame-rules/rules/sidereal-confluence.md"));selected_validation=read(ROOT/"validation.json")
out={"status":"COMPLETE_FACTUAL_ACCOUNTING_PASS","checked_at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"accounting_scope":"Two historical complete outputs graded against their own original frozen summaries/key/scope. Not a new candidate pair.","additional_completed_outputs":2,"additional_whole_entries":172,"additional_required_fact_checks":512,"attempt_scores":{who:{"original_round":s["round"],"original_task":s["task"],"raw_sha256":s["raw_sha256"],"own_summary_sha256":s["summary_sha256"],"scores":results["reader_scores"][who]} for who,s in attempts.items()},"all_complete_reader_outputs_with_factual_grades":24,"all_complete_entry_records_with_factual_grades":1648,"inventory_path":str(out_inventory),"inventory_sha256":sha(out_inventory),"grader_input_proofs":proofs,"actual_model_checks":models,"selected_full8_pair_unchanged":"Both86Correct0Partial0Incorrect0unsupportedguessing","current_canonical_sha256":current_sha,"current_canonical_matches_selected_validation":current_sha==selected_validation["canonical_sha256"],"historical_grades_and_targets_not_revised":True,"no_raw_answers_rewritten":True,"goal":"ACTIVE pending coordinator exact-byte stamping verification and explicit authorization"};dest.write_text(json.dumps(out,indent=2)+"\n");print("Complete factual accounting PASS:24 complete outputs/1648 entries; two additional172-entry/512-fact grade sets recorded.")
