from pathlib import Path
from PIL import Image
import copy,hashlib,json,collections
B=Path(__file__).resolve().parent;load=lambda p:json.loads(Path(p).read_text());H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();HS=lambda s:hashlib.sha256(s.encode()).hexdigest();checks=[]
def ck(ok,label):
 assert ok,label
 checks.append({'name':label,'passed':True})
def changed(a,b,path=''):
 if a==b:return []
 if isinstance(a,dict) and isinstance(b,dict):
  return [p for key in sorted(set(a)|set(b)) for p in ([path+'/'+key] if key not in a or key not in b else changed(a[key],b[key],path+'/'+key))]
 if isinstance(a,list) and isinstance(b,list) and len(a)==len(b):return [p for i,(x,y) in enumerate(zip(a,b)) for p in changed(x,y,path+'/'+str(i))]
 return [path]
k=load(B/'question-key-scope-review-14-corrected.json');c=load(B/'coverage-review-14-corrected.json');main=load(B/'scope-coverage-14-read-ledger-corrected.json');a=load(B/'scope14-own-correction-addendum.json');l=load(B/'scope14-correction-read-ledger.json');oldl=load(B/'scope-coverage-14-read-ledger.json');oldk=load(B/'question-key-scope-review-14.json');oldc=load(B/'coverage-review-14.json');freeze=load(B/'scope14-corrected-original-freeze.json');actual=load(B/'scope14-correction-actual-delivery-validation.json');one=load(B/'scope14-correction-one-range-event-validation.json');base=load(B/'scope14-structural-reference-validation.json');bounded=load(B/'scope14-original-bounded-replay-validation.json')
ck(base['all_passed'] and base['counts']['checks']==2121 and bounded['verified'] and bounded['exact_original_transport_proof_reproduced'],'original complete fresh challenge2121 checks and immutable prefix replay')
for name,row in freeze['files'].items():ck(H(B/name)==row['sha256'],'frozen corrected child output '+name)
for name,row in load(B/'scope14-original-freeze.json')['files'].items():ck(H(B/name)==row['sha256'],'unchanged original child output '+name)
for old,new,oldname,newname in [(oldk,k,'question-key-scope-review-14.json','question-key-scope-review-14-corrected.json'),(oldc,c,'coverage-review-14.json','coverage-review-14-corrected.json'),(oldl,main,'scope-coverage-14-read-ledger.json','scope-coverage-14-read-ledger-corrected.json')]:
 ck(set(changed(old,new))==set(a['field_changes_by_artifact'][newname]),'entire corrected field-change set '+newname)
 for field in ['per_question_checks','input_hashes','scope_credit_validation','scope_validation_counts','text_inputs']:
  if field in old:ck(old[field]==new[field],'exact unaffected '+newname+' '+field)
for report in [k,c]:
 ck(report['checked_question_ids']==oldk['checked_question_ids'] and report['checked_question_count']==173 and report['checked_required_grading_fact_count']==506,'all current173/506 preserved')
 ck(report['verdict']==report['fixed_key_verdict']==report['asked_fact_mapping_verdict']=='PASS' and not report['fixed_key_findings'] and not report['asked_fact_mapping_findings'] and not report['missing_truly_asked_facts_in_map'] and not report['missing_truly_asked_facts_in_fixed_key'],'current key/map PASS0findings')
 ck(Path(report['read_evidence']['ledger_path']).resolve()==(B/'scope-coverage-14-read-ledger-corrected.json').resolve() and report['read_evidence']['sha256']==H(B/'scope-coverage-14-read-ledger-corrected.json'),'corrected main ledger linkage')
 for path,digest in report['input_hashes'].items():ck(H(path)==digest,'all unchanged source/bank capture '+Path(path).name)
ck(c['coverage_verdict']==c['stopping_verdict']=='PASS' and c['remaining_gap_count']==0 and c['remaining_gaps']==[] and c['complete_independent_challenge'],'complete current coverage/stopping PASS')
ck(k['per_question_checks']==c['per_question_checks']==oldk['per_question_checks'] and sum(x['required_fact_count'] for x in k['per_question_checks'])==506,'every question and all506 exact fact-vector hashes preserved')
ck(k['primary_source_family_checks']==c['source_to_actual_ask_challenge'],'both corrected complete18-family challenges agree')
for bindings in [a['original_artifact_bindings'],a['corrected_output_bindings'],l['original_artifact_bindings']]:
 for path,meta in bindings.items():
  digest=meta if isinstance(meta,str) else meta.get('sha256',meta.get('full_byte_sha256'));ck(H(path)==digest,'exact correction artifact binding '+Path(path).name)
ck(all(a['invariance_validation'].values()),'all documented invariants true')
ck(a['original_card_observation_accuracy_verdict']=='FAIL' and a['corrected_card_observation_accuracy_verdict']=='PASS' and a['substantive_card_observation_errors']==2 and a['clarified_card_observations']==3 and a['other_card_observations_unchanged']==28,'original errors explicitly preserved2errors3clarifications28unchanged')
ck(a['own_report_phrase_correction']==l['own_report_phrase_correction'] and not a['own_report_phrase_correction']['changes_fixed_key_or_map'],'Shadows report-only clarification no key/map mutation')
for name,ref in a['primary_supplementary_passages'].items():
 p=Path(ref['path']);start,end=ref['unicode_range'];ck(H(p)==ref['file_sha256'] and HS(p.read_text()[start:end])==ref['passage_utf8_sha256'],'exact supplementary primary reference '+name)
oldinputs={x['path']:x for x in oldl['text_inputs']}
ck(len(l['reused_complete_primary_deliveries'])==22,'all22 old complete inputs bound as reuse')
for row in l['reused_complete_primary_deliveries']:
 ck(row['path'] in oldinputs and row['sha256']==oldinputs[row['path']]['full_byte_sha256']==H(row['path']) and row['original_ledger_sha256']==H(B/'scope-coverage-14-read-ledger.json'),'exact own original complete reuse '+Path(row['path']).name)
newranges=whole=focused=0
for file in l['new_text_reads']:
 p=Path(file['path']);text=p.read_text();ck(H(p)==file['full_byte_sha256'] and len(text)==file['character_length'],'new input identity '+p.name);ranges=[]
 for row in file['slices']:
  start,end=row['start'],row['end'];ck(0<=start<end<=len(text) and end-start<=6000 and row['truncated'] is False and HS(text[start:end])==row['slice_utf8_sha256'],'new exact bounded literal '+p.name+str([start,end]));ranges.append((start,end));newranges+=1
 if file['complete_new_delivery']:
  whole+=1;ranges.sort();ck(ranges[0][0]==0 and ranges[-1][1]==len(text) and all(x[1]==y[0] for x,y in zip(ranges,ranges[1:])),'whole new own artifact '+p.name)
 else:
  focused+=1;ref=file['original_complete_delivery_binding'];ck(file['path'] in oldinputs and ref['ledger_sha256']==H(B/'scope-coverage-14-read-ledger.json') and ref['full_byte_sha256']==H(p),'focused reopen supplements own full earlier source '+p.name)
ck(newranges==114 and whole==focused==3,'114 new source ranges:3whole own artifacts3focused reopens')
ck(actual['verified'] and actual['actual_distinct_text_range_deliveries']==114 and actual['unique_visual_sources']==actual['public_image_blocks']==33 and all(x['event_ordinal']>=1138 for x in actual['text_deliveries']),'actual114/33 correction-only source delivery after original boundary1138')
ck(one['verified'] and one['events_checked']==114 and one['all114_claimed_ranges_matched_to_separate_single_range_events'],'one literal range per114 new actual events')
oldimages={x['path']:x for x in oldl['images']};newimages={x['path']:x for x in main['images']};views=l['new_card_views'];ck(len(views)==len({x['path'] for x in views})==33,'all33 new full card views')
for seq,row in enumerate(views,1):
 p=Path(row['path']);ck(row['view_sequence']==seq and H(p)==row['full_byte_sha256'] and list(Image.open(p).size)==row['dimensions'],'exact card recheck source '+p.name);ck(row['detail']=='original' and row['new_view'] and row['fully_viewed'] and row['viewed_region_xyxy']==[0,0,*row['dimensions']],'whole original new face '+p.name);ck(HS(row['symbol_transcription'])==row['symbol_transcription_sha256'],'normalized-note self hash (not OCR verification) '+p.name);ck(row['old_observation']==oldimages[str(p)]['observations'] and row['new_observation']==newimages[str(p)]['observations'],'exact old/new observation linkage '+p.name)
ck(dict(collections.Counter(x['comparison_with_original_observation'] for x in views))=={'error':2,'unchanged':28,'clarification':3},'all33 comparison outcomes')
for row in a['observation_corrections']:
 ref=row['primary_evidence'];p=Path(ref['path']);ck(H(p)==ref['sha256'] and ref['native_dimensions']==list(Image.open(p).size),'changed observation primary source '+p.name);ck(row['changes_key_map_scope_or_coverage_verdict'] is False,'documented non-key/map change '+p.name)
# Keep the child output immutable; resolve one optional threshold transcription with an explicit parent primary-face erratum.
erratum=load(B/'scope14-parent-tree-transcription-erratum.json');effective=load(B/'scope14-effective-correction-read-ledger.json');patched=copy.deepcopy(l);index=int(erratum['json_pointer'].split('/')[2]);ck(patched['new_card_views'][index]['symbol_transcription']==erratum['old_text'],'optional Tree transcription old value recorded');patched['new_card_views'][index]['symbol_transcription']=erratum['corrected_text'];patched['new_card_views'][index]['symbol_transcription_sha256']=erratum['corrected_text_sha256'];parent_meta=effective['parent_derived_erratum'];ck(parent_meta['sha256']==H(B/'scope14-parent-tree-transcription-erratum.json'),'explicit parent erratum linkage');patched['parent_derived_erratum']=parent_meta;ck(patched==effective,'only explicit optional transcription/hash and parent provenance differ');ck(H(erratum['primary_face']['path'])==erratum['primary_face']['sha256'] and HS(erratum['corrected_text'])==erratum['corrected_text_sha256'],'Tree Air primary image/hash binding; parent visual judgment separate');ck(all(x['new_observation']==y['new_observation'] for x,y in zip(l['new_card_views'],effective['new_card_views'])),'all operative observations preserved under auxiliary erratum')
profile=load(B/'runtime/scope_and_coverage_14-corrected-final-completed-projection.json');ck(len(profile['turn_contexts'])==3 and all(x=={'model':'gpt-6.1-sol','effort':'high'} for x in profile['confirmed_settings']) and profile['requested_spawn']['fields']['fork_turns']=='none','all3 actual contexts6.1high originalnone');ck(sum(x['source_record']['runtime_line_ordinal']>=1138 for x in profile['turn_contexts'])==1,'one correction phase actual model context')
out={'all_passed':True,'counts':{'checks':len(checks),'blocking_failed_checks':0,'questions':173,'mapped_fact_entries':506,'original_complete_fresh_challenge_checks':2121,'new_text_inputs':6,'new_whole_own_artifact_inputs':3,'new_focused_reopen_inputs':3,'new_actual_source_ranges':114,'reused_own_complete_text_inputs':22,'new_full_card_views':33,'original_note_errors':2,'card_note_clarifications':3,'report_phrase_clarifications':1,'explicit_parent_optional_transcription_errata':1,'actual_total_model_contexts':3,'actual_original_model_contexts':2,'actual_correction_model_contexts':1},'checks':checks,'frozen_artifact_sha256':{name:H(B/name) for name in freeze['files']},'actual_correction_proof_sha256':H(B/'scope14-correction-actual-delivery-validation.json'),'one_range_correction_proof_sha256':H(B/'scope14-correction-one-range-event-validation.json'),'effective_correction_read_ledger_sha256':H(B/'scope14-effective-correction-read-ledger.json'),'parent_erratum_sha256':H(B/'scope14-parent-tree-transcription-erratum.json'),'limitations':'Normalized optional payload notes are not an OCR ground-truth corpus or additional tested requirements. Original printed images remain authority; B&C numerical payloads are excluded. All relevant procedural observations and current173/506 bindings are preserved. Current coverage adoption and parent semantic judgment are separate.'};p=B/'scope14-corrected-structural-reference-validation.json';assert not p.exists();p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'all_passed':True,'counts':out['counts'],'sha256':H(p)}))
