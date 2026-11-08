from pathlib import Path
import json,sys,hashlib
ROOT=Path(__file__).resolve().parent
iteration,filename=sys.argv[1:];D=ROOT/iteration;dest=D/filename;assert not dest.exists()
read=lambda p:json.loads(Path(p).read_text())
coverage=read(D/"output-diagnostic-coverage.json")["claims"];expected={(x["reader"],x["id"],x["raw_field_path"]):x["value"] for x in coverage};assert len(expected)==len(coverage)
observed={};checks=[]
for p in sorted(D.glob("grades-block-??.json")):
 for who,body in read(p)["readers"].items():
  for row in body["results"]:
   for item in row.get("output_level_diagnostic_checks",[]):
    key=(who,row["id"],item["raw_field_path"]);assert key in expected and key not in observed,(key,"unexpected/duplicate diagnostic check")
    assert item["value"]==expected[key] and isinstance(item.get("match"),bool);observed[key]=item
    checks.append({"reader":who,"id":row["id"],"raw_field_path":item["raw_field_path"],"original_value":expected[key],"match":item["match"],"reason":item.get("reason"),"grade_report":p.name,"grade_report_sha256":hashlib.sha256(p.read_bytes()).hexdigest()})
assert set(observed)==set(expected),("Missing supplemental factual assessments",set(expected)-set(observed))
passed=all(x["match"] for x in checks);dest.write_text(json.dumps({"status":"PASS" if passed else "FAIL","all_present_output_level_game_numeric_claims_assessed":True,"claim_count":len(checks),"checks":checks,"separate_from_entry_grades":True,"metadata_cannot_heal_missing_entry_results":True,"missing_diagnostics_not_an_omission_gate":True},indent=2)+"\n");print("Supplemental output diagnostics", "PASS" if passed else "FAIL",len(checks),"claims")
