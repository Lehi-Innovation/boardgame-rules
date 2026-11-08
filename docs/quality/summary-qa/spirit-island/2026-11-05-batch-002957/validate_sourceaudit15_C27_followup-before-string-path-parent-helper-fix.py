"""Validate exact current-body continuation and honest prior-evidence reuse."""
from pathlib import Path
import hashlib,json
from PIL import Image
B=Path(__file__).resolve().parent
ROOT=B.parents[4]
load=lambda p:json.loads(p.read_text())
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def check(ok,label):
 assert ok,label
 checks.append(label)
def source(p):return (ROOT/p).resolve()
reportpath=B/'source-audit15-current-body-C27-followup.json'
ledgerpath=B/'source-audit15-current-body-C27-followup-read-view-ledger.json'
r,l=load(reportpath),load(ledgerpath)
freeze=load(B/'source-audit15-C27-followup-original-completed/original-freeze.json')
for row in freeze['originals']:
 check(H(Path(row['path']))==H(Path(row['immutable_copy']))==row['sha256'],'entire frozen original unchanged '+Path(row['path']).name)
current=B/'source-candidate-27.md'
check(r['candidate_sha256']==H(current)==H(ROOT/'rules/spirit-island.md'),'exact current canonical body')
check(r['candidate_character_length']==len(current.read_text())==55146 and r['candidate_byte_length']==current.stat().st_size==55350,'current text and byte lengths')
check(r['prior_candidate_sha256']==H(B/'source-candidate-26.md'),'own prior candidate exact')
check(r['whole_current_body_read'] and r['verdict']=='PASS' and not r['findings'] and not r['unverified_current_guide_concerns'] and r['unresolved_current_guide_findings']==0,'reported zero current concerns')
check(r['new_source_delivery']==l['actual_new_text_deliveries'] and r['new_views']==l['actual_new_views']==[],'exact two original new-delivery declarations')
for row in l['actual_new_text_deliveries']:
 p=source(row['path']);s=p.read_text();a,z=row['start'],row['end']
 check(H(p)==row['source_sha256'] and len(s)==row['character_length'],'new source hash and full length '+str([row['path'],a,z]))
 check(0<=a<z<=len(s) and z-a<=6000 and hashlib.sha256(s[a:z].encode()).hexdigest()==row['slice_sha256'] and row['output_cap']>=4000 and row['truncated'] is False,'new literal bounded range '+str([row['path'],a,z]))
for x in l['reused_own_evidence_artifacts']:
 check(H(source(x['path']))==x['source_sha256'],'own prior evidence unchanged '+x['path'])
for x in l['reused_complete_text_perceptions']:
 p=source(x['path']);check(H(p)==x['source_sha256'] and len(p.read_text())==x['character_length'] and x['hash_verified_unchanged'],'reused whole text exact '+x['path'])
for x in l['reused_visual_perceptions']:
 p=source(x['path']);check(H(p)==x['source_sha256'] and list(Image.open(p).size)==x['dimensions'] and x['hash_verified_unchanged'],'reused original native visual exact '+x['path'])
expected=load(B/'expanded-iteration-08/input-manifest.json')['source_hashes']
actual={str(source(x['path'])):x['source_sha256'] for x in l['reused_source_manifest_and_supplement_reconciliation']}
check(len(actual)==len(expected)==79 and actual=={str(source(p)):v for p,v in expected.items()},'all79 unchanged authoritative/locator pins exact')
for x in l['reused_source_manifest_and_supplement_reconciliation']:
 check(H(source(x['path']))==x['source_sha256'] and x['hash_verified_unchanged'],'reused source pin '+x['path'])
old=load(B/'source-audit-final-15.json')
check(len(r['checked_current_scope'])==len(old['checked_groups'])==23,'all23 current scope groups')
oldrefs=newrefs=visualrefs=0
for row,prior in zip(r['checked_current_scope'],old['checked_groups']):
 check(row['group']==prior['group'] and row['primary_sources']==prior['sources'] and row['visual_source_references']==prior['visual_sources'],'exact originally read reference arrays '+row['group'])
 visualrefs+=len(row['visual_source_references'])
 for ref in row['primary_sources']:
  p=source(ref['path']);check(H(p)==ref['source_sha256'] and p.read_text()[ref['start']:ref['end']]==ref['passage'],'reused exact literal primary span '+row['group']);oldrefs+=1
for row in r['changed_material']:
 check(row['candidate_source_sha256']==H(current) and not row['findings'],'changed block binding '+row['change_id'])
 for ref in row['primary_citations']:
  p=source(ref['path']);a,z=ref['start'],ref['end'];s=p.read_text();w=ref['received_range']
  check(H(p)==ref['source_sha256'] and s[a:z]==ref['passage'],'new exact changed primary passage '+row['change_id'])
  check(w['start']<=a<z<=w['end'] and any(source(x['path'])==p and x['start']==w['start'] and x['end']==w['end'] and x['slice_sha256']==w['slice_sha256'] for x in l['actual_new_text_deliveries']),'new citation actually within declared reopened source window');newrefs+=1
check(oldrefs==97 and newrefs==6 and visualrefs==65,'97 reused and6 newly applied exact literal references plus65 visual references')
diff=load('/tmp/audit15-C27-derived-diff.json')
check(r['comparison']['source_only_derived_diff']==diff and r['comparison']['exact_changed_blocks']==len(diff['changes'])==2 and r['comparison']['net_character_change']==629,'exact independently reproduced two-block diff')
check(load(B/'source-audit15-C27-derived-diff-independent-reproduction.json')['complete_JSON_bytes_reproduced'],'independent derived bytes reproduction')
qual=r['dissolve_prior_evidence_qualification']
check(H(source(qual['addendum_path']))==qual['addendum_sha256'],'own original note-correction addendum unchanged')
check(qual['corrected_printed_replacements']==[{'source_piece':'City','source_count':1,'destination_piece':'Explorer','destination_count':2},{'source_piece':'Town','source_count':1,'destination_piece':'Explorer','destination_count':1},{'source_piece':'Dahan','source_count':1,'destination_piece':'Explorer','destination_count':1}],'corrected printed payload qualification retained')
actualproof=load(B/'source-audit15-C27-followup-actual-delivery-validation.json')
check(actualproof['verified'] and actualproof['actual_distinct_text_range_deliveries']==14 and actualproof['new_record_interval']==[732,811] and actualproof['new_candidate_whole_contiguous'],'strict14new-event actual-delivery proof')
profilepath=B/'runtime/final_source_audit_15-C27-followup-final-completed-projection.json'
profile=load(profilepath)
check(profile['confirmed_settings']==[{'model':'gpt-6.1-sol','effort':'high'}]*3 and profile['requested_spawn']['fields']['fork_turns']=='none','same initially fresh actual3context pure Sol61/high')
rootpath=B.parents[1]/'batches/2026-11-05-batch-002957/coordinator-checks/spirit-source15-C27-current-body-actual-followup-and-semantic-acceptance.json'
root=load(rootpath)
check(root['verified'] and root['verdict']=='PASS' and root['audit_sha256']==H(reportpath) and root['ledger_sha256']==H(ledgerpath) and root['summary_sha256']==H(current),'independent coordinator exact current-body semantic PASS')
check(root['original_followup_copies_and_runtime_prefix_verified'] and root['whole_current_candidate_newly_received'] and root['all23_current_scope_groups']==23 and root['all79_reused_source_pins_and16_whole_texts57_native_views_rechecked'] and root['exact2_block629_character_diff_independently_reproduced'],'independent lineage/whole-input/primary physical-evidence acceptance')
out={'all_passed':True,'counts':{'checks':len(checks),'blocking_failed_checks':0,'new_exact_single_range_deliveries':14,'new_whole_candidate_slices':10,'new_primary_reopen_windows':3,'new_whole_own_derived_diff':1,'new_images':0,'reused_whole_texts':16,'reused_native_views':57,'reused_authority_and_locator_pins':79,'current_scope_groups':23,'exact_reused_primary_references':97,'exact_changed_primary_references':6,'visual_references':65,'actual_total_same_auditor_contexts':3},'checks':[{'check':x,'passed':True} for x in checks],'candidate_sha256':H(current),'frozen_artifact_sha256':{reportpath.name:H(reportpath),ledgerpath.name:H(ledgerpath)},'actual_delivery_proof_sha256':H(B/'source-audit15-C27-followup-actual-delivery-validation.json'),'completed_model_profile_sha256':H(profilepath),'coordinator_semantic_acceptance':{'path':str(rootpath),'sha256':H(rootpath)},'semantic_adoption':False,'same_original_pure_auditor_not_new_fresh_vote':True,'prior_exact_authority_perception_honestly_reused_not_claimed_anew':True}
p=B/'source-audit15-C27-followup-evidence-validation.json'
assert not p.exists()
p.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'checks':len(checks),'all_passed':True,'blocking_failed_checks':0,'exact_primary_references':oldrefs+newrefs,'coordinator_current_source_semantic_PASS_bound':True,'sha256':H(p)}))
