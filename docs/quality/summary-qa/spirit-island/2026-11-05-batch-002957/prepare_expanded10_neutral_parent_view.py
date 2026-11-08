"""Prepare a lossless parent view; only technical input-delivery metadata moves."""
from pathlib import Path
import copy, hashlib, json
B=Path(__file__).resolve().parent
A=B/'expanded-iteration-10/adjudication-01'
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda p:json.loads(p.read_text())
raw=A/'adjudication.json'
assert H(raw)==H(A/'adjudication-original-completed.json')==load(A/'adjudication-original-freeze.json')['sha256']
original=load(raw)
semantic=copy.deepcopy(original)
technical={'inputs_read':semantic.pop('inputs_read')}
reconstructed={**semantic,**technical}
assert reconstructed==original
view={'original_output_sha256':H(raw),'all_original_human_adjudication_fields':semantic}
v=A/'parent-complete-semantic-view.json'
s=A/'parent-technical-input-delivery-sidecar.json'
r=A/'parent-view-reconstruction-validation.json'
assert not any(p.exists() for p in [v,s,r])
v.write_text(json.dumps(view,ensure_ascii=False,separators=(',',':'))+'\n')
s.write_text(json.dumps(technical,ensure_ascii=False,separators=(',',':'))+'\n')
r.write_text(json.dumps({'parent_view_sha256':H(v),'technical_sidecar_sha256':H(s),'entire_original_output_sha256':H(raw),'exact_object_reconstruction_verified':True,'only_technical_inputs_read_metadata_moved_to_sidecar':True,'all_original_human_fields_retained_without_deduplication':True,'not_an_input_to_any_evaluator':True},indent=2)+'\n')
assert {**load(v)['all_original_human_adjudication_fields'],**load(s)}==original
print(json.dumps({'human_view_characters':len(v.read_text()),'human_view_sha256':H(v),'all_original_human_fields_retained':True,'parent_human_read_not_yet_claimed':True}))
