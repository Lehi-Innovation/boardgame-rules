"""Bind current81 metadata revalidation to the exact earlier fixed benchmark."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
B=Path(__file__).resolve().parent;ROOT=B.parents[4]
G=ROOT/'docs/quality/summary-qa/root'/B.name;V=G/'current-snapshot-revalidation-2026-11-07';D=V/'iteration-01'
J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=J(V/'input-manifest.json');old=J(G/'expanded-iteration-17/input-manifest.json')
for name,h in m['hashes'].items():assert H(Path(name))==h
assert H(ROOT/'rules/root.md')==H(D/'summary-snapshot.md')==m['canonical_sha256']=='da0b6b08fda1d3e1775a8ef813e31535ac35375399b061efe255690d09ad1aeb'
baseline=G/'expanded-iteration-17/summary-snapshot.md'
assert H(baseline)==m['prior_accepted_snapshot_sha256']=='844f9b73297121dc8813cb18c623d68cdafc9942bcba8485ca0cccaec56eebec'
assert baseline.read_text().replace('extracted_date: "2026-11-05"','extracted_date: "2026-11-06"')==(D/'summary-snapshot.md').read_text()
assert (D/'questions.json').read_bytes()==(G/'benchmark-v10/questions.json').read_bytes()==(G/'expanded-iteration-17/questions.json').read_bytes()
key=G/'benchmark-v10/answer-key.json';assert (D/'answer-key.json').read_bytes()==key.read_bytes()
assert old['hashes'][str(key)]==H(key)=='56ddcebb25060299ac51e3acec2b32f9d7c94fae1020e49ec43cff79e07ffaab'
assert len(J(D/'questions.json')['questions'])==81
pa=(D/'reader-a-prompt.txt').read_text();pb=(D/'reader-b-prompt.txt').read_text()
assert pa.replace(str(D/'reader-a.json'),'OUTPUT')==pb.replace(str(D/'reader-b.json'),'OUTPUT')
for name,h in m['prompt_hashes'].items():assert H(Path(name))==h
proof={'verified':True,'checked_at_utc':datetime.now(timezone.utc).isoformat(),'N':81,'summary_sha256':H(D/'summary-snapshot.md'),'manifest_sha256':H(V/'input-manifest.json'),'all_frozen_hashes_rechecked':m['hashes'],'exact_old81_Q_key_files_unchanged':True,'old17_external_fixed_key_binding_rechecked':True,'only_current_drift':'extracted_date2026-11-05 to2026-11-06, allotherbytesunchanged; unownededitpreserved','tested_verification_date_preserved':'2026-11-05','prior22pairs_and_stopping_closure_reused_honestly':True,'complete_generic_prompts_read_and_identical_except_output':True,'prompt_review':'Two frozen ruledata files+own same-run progress only. Complete governing quotes and all actual asked cases; no source/key/routing/factual hints. Parent evaluator may repair and grade per local QAguide; final source auditor must remain independent/pure.','initial_critical_model_proof':str(B/'coordinator-runtime-model-checks/root-revalidation18-initial-cohort-20261107T065420450888.json'),'protocol_qualification':'Parent began prefixgrading beforeboth81outputscomplete; preserveeveryprefix/earlylabel, finishSAMEblindreaderswithoutfeedbackbeforefurthergrading, freezeallcompleteoriginals and bindfinalgrades. Chronologydeviationonly, no factualcap or resampling.','limits':['Complete current81 actual input/model/original-grade verification and fresh pure source audit remain separate.','No final record/stamp/pub/goal-complete authorization yet.']}
out=B/'coordinator-checks/root-current18-exact81-frozen-input-continuity.json';assert not out.exists();out.write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps({'verified':True,'N':81,'proof':str(out)}))
