from pathlib import Path
import json,sys
from verify_runtime_delivery import strings,sha
ROOT=Path(__file__).resolve().parent
iteration,reader=sys.argv[1:];d=ROOT/iteration
raw=json.loads((d/f"reader-{reader}.json").read_text());rules=json.loads((d/f"reader-{reader}-runtime-delivery.json").read_text());source=d/f"reader-{reader}-prompt.txt";content=source.read_text();frozen=json.loads((d/"prompt-binding.json").read_text());assert sha(source.read_bytes())==frozen["prompt_hashes"][reader]
receipts=raw.get("process_instruction_receipts")
if receipts is None and isinstance(raw.get("inputs_read"),dict):receipts=raw["inputs_read"].get("process_instruction_receipts")
if receipts is None and isinstance(raw.get("delivery_receipts"),dict):receipts=raw["delivery_receipts"].get("process_instruction_receipts")
assert isinstance(receipts,list) and len(receipts)==1
receipt=receipts[0];assert Path(receipt.get("path",receipt.get("file"))).name==source.name
ranges=receipt.get("ranges",receipt.get("slices",receipt.get("read_spans",receipt.get("read_as_complete_contiguous_slices",receipt.get("read_as_contiguous_slices")))));assert ranges
ranges=[[x["start"],x["end"]] if isinstance(x,dict) else x for x in ranges]
assert ranges[0][0]==0 and ranges[-1][1]==len(content)
outputs=[]
for n,line in enumerate(Path(rules["runtime_source_path"]).open(),1):
 p=json.loads(line).get("payload",{})
 if p.get("type") in ["custom_tool_call_output","function_call_output"]:outputs.append({"ordinal":n,"record_sha256":sha(line.encode()),"text":list(strings(p.get("output")))})
checked=[]
for i,(a,b) in enumerate(ranges):
 assert 0<=a<b<=len(content) and b-a<=6000
 if i:assert a==ranges[i-1][1]
 found=[{k:o[k] for k in ["ordinal","record_sha256"]} for o in outputs if o["ordinal"]<rules["first_answer_file_write_record_ordinal"] and any(content[a:b] in t for t in o["text"])]
 assert found,(a,b,"No complete literal process slice before first answer write")
 checked.append({"start":a,"end":b,"slice_sha256":sha(content[a:b].encode()),"matching_runtime_outputs":found})
other=(d/f"reader-{'b' if reader=='a' else 'a'}-prompt.txt").read_text();assert content.replace(f"reader-{reader}.json","reader-X.json")==other.replace(f"reader-{'b' if reader=='a' else 'a'}.json","reader-X.json")
output=d/f"reader-{reader}-process-instruction-delivery.json";assert not output.exists();output.write_text(json.dumps({"validation":"PASS","reader":reader,"process_instruction_path":str(source),"process_instruction_sha256":sha(source.read_bytes()),"characters":len(content),"complete_bounded_ranges":checked,"all_process_text_before_first_answer_write":True,"same_frozen_instructions_except_output":True,"boundary":"Actual full model-visible process text proved from tool outputs; initial parent dispatch plaintext remains opaque. Generic instructions/helper are authorized process metadata, not additional rules DATA."},indent=2)+"\n");print(reader,"complete actual process-instruction delivery and equality PASS")
