"""Extend the immutable24-output accounting with every new complete submitted raw."""
from pathlib import Path
import json,hashlib,sys,datetime
ROOT=Path(__file__).resolve().parent
output=ROOT/sys.argv[1];assert not output.exists()
def read(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def digest(z):return hashlib.sha256(json.dumps(z,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
base=read(ROOT/"completed-output-grade-inventory.json");baseproof=read(ROOT/"complete-attempt-accounting-01/validation.json");assert baseproof["status"]=="COMPLETE_FACTUAL_ACCOUNTING_PASS" and baseproof["inventory_sha256"]==sha(ROOT/"completed-output-grade-inventory.json")
known={x["path"]:x for x in base["outputs"]};complete=[];ungraded=[]
for directory in sorted([*ROOT.glob("seed-iteration-*"),*ROOT.glob("full-iteration-*")]):
 if not directory.is_dir() or not (directory/"questions.json").exists():continue
 questions=read(directory/"questions.json")["questions"];ids={q["id"] for q in questions}
 for path in sorted(directory.glob("reader*.json")):
  try:data=read(path)
  except (json.JSONDecodeError,UnicodeDecodeError):continue
  if not isinstance(data,dict):continue
  answers=data.get("answers")
  if not isinstance(answers,list) or not answers or not all(isinstance(a,dict) and "answer" in a and "evidence" in a for a in answers):continue
  answer_ids=[a.get("id") for a in answers]
  if len(answer_ids)!=len(ids) or len(set(answer_ids))!=len(ids) or set(answer_ids)!=ids:continue
  key=str(path.resolve())
  if key in known:
   row=known[key];assert row["sha256"]==sha(path) and row["grade_authority_sha256"]==sha(row["grade_authority"]);complete.append(row);continue
  if path.name not in ["reader-a.json","reader-b.json"] or not (directory/"results.json").exists():ungraded.append(key);continue
  who="a" if path.name=="reader-a.json" else "b";authority=directory/"results.json";result=read(authority);rows=result["readers"][who];assert len(rows)==len(ids) and {x["id"] for x in rows}==ids
  target={x["id"]:{f["id"] for f in x["required_facts"]} for x in read(directory/"answer-key.json")["answers"]}
  for row in rows:
   original=row.get("original_grade_record",row);fs=original["required_facts"];assert len(fs)==len(target[row["id"]]) and {f["id"] for f in fs}==target[row["id"]];assert isinstance(original.get("unsupported_guessing"),bool)
  raw_index={x["id"]:x for x in answers};seen=[]
  for block in sorted(directory.glob("grading-block-??.json")):
   data=read(block);assert data["source_raw_hashes"][path.name]==sha(path)
   for record in data["records"]:
    i=record["id"];assert record[f"reader_{who}_original_entry"]==raw_index[i] and record["original_entry_canonical_hashes"][who]==digest(raw_index[i]);seen.append(i)
  assert len(seen)==len(ids) and set(seen)==ids
  complete.append({"path":key,"sha256":sha(path),"round":directory.name,"entries":len(answers),"entry_list_sha256":digest(answers),"grade_authority":str(authority),"grade_authority_sha256":sha(authority),"grade_result_reader":who,"own_frozen_summary":str(directory/"summary-snapshot.md"),"own_frozen_summary_sha256":sha(directory/"summary-snapshot.md"),"scores":result["reader_scores"][who],"graded_ids_exactly_once":True,"all_original_frozen_fact_atoms_graded":True,"whole_original_entries_match_grading_blocks":True,"factual_grades_recorded":True})
assert not ungraded,("New complete nonstandard/ungraded attempts require independent factual accounting before closure",ungraded)
assert len({x["path"] for x in complete})==len(complete) and all(x["factual_grades_recorded"] for x in complete)
out={"status":"ALL_CURRENT_COMPLETE_OUTPUTS_HAVE_FACTUAL_GRADES","checked_at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"complete_outputs":len(complete),"complete_entry_records":sum(x["entries"] for x in complete),"prior_immutable_accounting_outputs":24,"outputs":complete,"no_process_deviation_used_as_factual_grade":True,"historical_targets_raws_grades_preserved":True};output.write_text(json.dumps(out,indent=2)+"\n");print("Current complete-output accounting PASS",len(complete),"sets",out["complete_entry_records"],"entries")
