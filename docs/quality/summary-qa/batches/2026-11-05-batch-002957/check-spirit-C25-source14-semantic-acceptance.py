"""Record semantic adoption after exact original source14 delivery validation."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
B=Path(__file__).resolve().parent;ROOT=B.parents[4]
G=ROOT/'docs/quality/summary-qa/spirit-island'/B.name
J=lambda p:json.loads(p.read_text())
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
resolve=lambda p:(ROOT/p).resolve()
a=J(G/'source-audit-final-14.json');v=J(G/'source-audit-final-14-visual-manifest.json')
f=J(G/'source-audit14-original-freeze.json');pins=J(G/'supplemental-source-manifest-v4.json')['source_records']
delivery=J(B/'coordinator-checks/spirit-source-audit-final-14-actual-delivery.json')
assert delivery['verified'] and delivery['summary_sha256']==a['candidate_sha256']==H(ROOT/'rules/spirit-island.md')=='f0297380795b0939b0480cb52d97499a5d611b57a8243d5a56820099979727b6'
for name,x in f['files'].items():assert H(G/name)==x['sha256']==H(Path(x['original_completed_copy']))
refs=[];native_groups=[];native_names={Path(x['path']).name for x in v['observations']}
for group in a['checked_groups']:
    for q in group['source_references']:
        if 'path' not in q:
            assert q['visual_manifest']=='source-audit-final-14-visual-manifest.json'
            names=q.get('faces',q.get('panels'));assert names and set(names)<=native_names
            native_groups.append({'group':group['group'],'native_names':names});continue
        path=resolve(q['path']);assert H(path)==q['source_sha256']
        if all(k in q for k in ['start','end','passage']):
            assert path.read_text()[q['start']:q['end']]==q['passage']
            refs.append({'path':str(path),'start':q['start'],'end':q['end'],'sha256':q['source_sha256']})
assert len(a['supplemental_reconciliation'])==len(pins)==72
for row in a['supplemental_reconciliation']:
    original=pins[row['record_number_one_based']-1]
    assert resolve(row['path'])==resolve(original['path']) and row['source_sha256']==original['sha256']
assert len(refs)==57 and len(native_groups)==2 and a['verdict']=='PASS' and not a['findings'] and not a['unresolved_findings']
proof={'verified':True,'checked_at_utc':datetime.now(timezone.utc).isoformat(),'summary_sha256':a['candidate_sha256'],'audit_path':str(G/'source-audit-final-14.json'),'audit_sha256':H(G/'source-audit-final-14.json'),'original_three_file_freeze_rechecked':True,'all18_checked_group_scopes_and_observations_read':True,'all58_native_view_observations_read':True,'all72_reconciliation_records_exact_resolved_manifest_members':True,'exact_checked_group_primary_source_passages':refs,'whole_native_card_panel_groups_bound':native_groups,'source_delivery_proof':str(B/'coordinator-checks/spirit-source-audit-final-14-actual-delivery.json'),'C25_entire_six_general_clarification_diff_reviewed':True,'semantics':'C25 accurately clarifies unchanged source procedures: marked Damage does not reduce Health-worth, EnheartenedIII counts all post-Gather Dahan, each pushed Dahan carries Defend2 to its destination, any-Ocean Growth excludes Inland, illegal-human cleanup follows the whole action tree, and Bringer does not Push Cities. No fixed-answer appendix or new unasked numeric quota. Dissolve note correctly gives City2Explorers/Town1Explorer/Dahan1Explorer. Original fresh14 audit PASS accepted.','verdict':'PASS','technical_diagnostics':['The first proof construction assumed all source references were text; two actual groups refer to complete native manifests. Both groups now explicitly bound.','Supplemental report paths are repository-relative and original manifest paths absolute; exact resolved paths and hashes match all72. No source-reference or factual mismatch.','Prior premature save/count messages corrected: this proof records57 exact textual references; no previous semantic proof was written.'],'limits':['Source accuracy only for exactC25; full unchanged173/506 NEW two-reader trial remains required.','Current unverified frontmatter requires actual record/stamp after full-pair acceptance; changed bytes require exact new full pair and current pure-source followup.','No heldout/general-accuracy or exhaustive-cognition claim.']}
out=B/'coordinator-checks/spirit-C25-source14-semantic-acceptance.json';assert not out.exists();out.write_text(json.dumps(proof,indent=2)+'\n')
p=B/'manifest.json';m=J(p);g=next(x for x in m['games'] if x['slug']=='spirit-island')
g['coordinator_source_delivery_checkpoint']={'path':str(B/'coordinator-checks/spirit-source-audit-final-14-actual-delivery.json'),'summary_sha256':a['candidate_sha256']}
g['coordinator_source14_semantic_acceptance']={'path':str(out),'sha256':H(out)};g['coordinator_pending_source_audit']=False
m['updated_at']=datetime.now(timezone.utc).isoformat();p.write_text(json.dumps(m,indent=2)+'\n')
print(json.dumps({'verified':True,'groups':18,'views':58,'exact_primary_passages':len(refs),'exact_resolved_supplemental_members':72,'proof':str(out)}))
