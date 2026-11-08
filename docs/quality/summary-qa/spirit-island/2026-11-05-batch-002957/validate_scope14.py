from pathlib import Path
from PIL import Image
from bs4 import BeautifulSoup
import hashlib,json,collections
B=Path(__file__).resolve().parent;ROOT=B.parents[4];load=lambda p:json.loads(Path(p).read_text());H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();checks=[]
def ck(ok,label):
 assert ok,label
 checks.append({'name':label,'passed':True})
k=load(B/'question-key-scope-review-14.json');c=load(B/'coverage-review-14.json');l=load(B/'scope-coverage-14-read-ledger.json');actual=load(B/'scope14-actual-delivery-validation.json');one=load(B/'scope14-one-range-event-validation.json');freeze=load(B/'scope14-original-freeze.json');q=load(B/'expanded-v24/questions.json')['questions'];key=load(B/'expanded-v24/answer-key.json')['answers'];m=load(B/'expanded-v24/asked-fact-map.json')['questions'];scope=load(B/'expanded-v24/core-scope-credit.json')['questions'];ids=[x['id'] for x in q]
for name,row in freeze['files'].items():ck(H(B/name)==row['sha256'],'original frozen '+name)
for report in [k,c]:
 ck(report['benchmark']=='expanded-v24' and report['checked_question_ids']==ids,'all173 exact ordered IDs');ck(report['checked_question_count']==173 and report['checked_required_grading_fact_count']==506,'173/506 actual metadata');ck(report['verdict']==report['fixed_key_verdict']==report['asked_fact_mapping_verdict']=='PASS','reported semantic verdicts');ck(report['asked_fact_map_sha256']==H(B/'expanded-v24/asked-fact-map.json'),'exact asked fact map');
 for field in ['fixed_key_findings','asked_fact_mapping_findings','missing_truly_asked_facts_in_map','missing_truly_asked_facts_in_fixed_key','scope_credit_findings','unresolved_relevant_findings']:ck(report[field]==[],'empty unresolved '+field)
 for path,digest in report['input_hashes'].items():ck(Path(path).is_absolute() and H(path)==digest,'input exact '+Path(path).name)
 ck(Path(report['read_evidence']['ledger_path']).resolve()==(B/'scope-coverage-14-read-ledger.json').resolve() and report['read_evidence']['sha256']==H(B/'scope-coverage-14-read-ledger.json'),'exact ledger reference')
ck(c['coverage_verdict']==c['stopping_verdict']=='PASS' and c['remaining_gap_count']==0 and not c['remaining_gaps'] and c['complete_independent_challenge'],'complete fresh zero-gap challenge')
ck(k['per_question_checks']==c['per_question_checks'],'both full per-question arrays exact');ck(k['primary_source_family_checks']==c['source_to_actual_ask_challenge'],'both full18-family challenges exact')
families={x['topic']:x for x in k['primary_source_family_checks']}
for r,question,answer,mapped,sc in zip(k['per_question_checks'],q,key,m,scope):
 ident=question['id'];facts=[f for cl in mapped['requested_clauses'] for f in cl['required_facts']]
 ck(r['id']==ident and mapped['id']==answer['id']==sc['id']==ident,'row identity '+ident)
 ck(r['literal_question_sha256']==hashlib.sha256(question['question'].encode()).hexdigest(),'literal question '+ident)
 ck(r['fixed_key_answer_sha256']==hashlib.sha256(answer['answer'].encode()).hexdigest(),'literal fixed key '+ident)
 ck(r['required_fact_entries_sha256']==hashlib.sha256(json.dumps(facts,ensure_ascii=False,separators=(',',':')).encode()).hexdigest() and r['required_fact_count']==len(facts),'all exact mapped fact entries '+ident)
 ck(r['literal_ask_checked'] and r['every_required_fact_checked'] and r['fixed_key_verdict']==r['asked_fact_mapping_verdict']=='PASS','all facts attested checked '+ident)
 ck(r['scope_result']==sc['scope_result'],'independent scope result '+ident)
 ck(r['source_family_checks'] and all(name in families and ident in families[name]['actual_question_ids'] for name in r['source_family_checks']),'source family crosswalk '+ident)
ck(dict(collections.Counter(x['scope_result'] for x in k['per_question_checks']))==k['scope_validation_counts']=={'base_supported':156,'mixed_supported_and_noncredited':14,'noncredited_pending_base_proof':3},'156/14/3 question-row scope counts')
qualified=[x['id'] for x in scope if x['scope_result']!='base_supported'];ck([x['id'] for x in k['scope_credit_validation']]==qualified,'all17 qualified regressions explicitly checked');ck(all(x['all_existing_regression_grading_retained'] and x['unsupported_clause_current_base_novelty_credit']==0 for x in k['scope_credit_validation']),'all qualified hard grading retained')
raw=unique=partition=0
for file in l['text_inputs']:
 p=Path(file['path']);text=p.read_text();ck(H(p)==file['full_byte_sha256'] and len(text)==file['character_length'],'whole source identity '+p.name);ranges=set()
 for row in file['slices']:
  a,z=row['start'],row['end'];ck(0<=a<z<=len(text) and z-a<=6000 and row['truncated'] is False and hashlib.sha256(text[a:z].encode()).hexdigest()==row['slice_utf8_sha256'],'exact bounded literal '+p.name+str([a,z]));ranges.add((a,z));raw+=1
 cursor=0;chosen=[]
 while cursor<len(text):
  ends=[z for a,z in ranges if a==cursor];ck(bool(ends),'contiguous next '+p.name+str(cursor));end=max(ends);chosen.append((cursor,end));cursor=end
 ck(cursor==len(text) and file['complete_contiguous_delivery'],'complete whole-file delivery '+p.name);unique+=len(ranges);partition+=len(chosen)
ck(len(l['text_inputs'])==22 and raw==245 and unique==231 and partition==229,'22 whole inputs/229partition+2focused+14rereads');ck(actual['verified'] and actual['actual_distinct_text_range_deliveries']==245 and len({x['event_ordinal'] for x in actual['text_deliveries']})==245,'all245 actual distinct source events');ck(one['verified'] and one['events_checked']==245 and one['all245_claimed_ranges_matched_to_separate_single_range_events'],'one literal range per all245 source events')
images={x['path']:x for x in l['images']};ck(len(images)==54,'54 distinct visual sources')
for path,row in images.items():
 p=Path(path);ck(H(p)==row['full_byte_sha256'] and list(Image.open(p).size)==row['dimensions'],'image exact identity '+p.name);ck(row['detail']=='original' and row['fully_viewed'] and row['viewed_region_xyxy']==[0,0,*row['dimensions']],'whole original visual '+p.name)
 if row['dimensions']==[2697,1797]:ck(p.stat().st_size==19419092,'full native19MB '+p.name)
manifest=load(B/'supplemental-source-manifest-v4.json')['source_records']
for i,row in enumerate(manifest):ck(H(row['path'])==row['sha256'],'assigned supplemental source hash '+str(i))
required_images=[row['path'] for i,row in enumerate(manifest) if Path(row['path']).suffix.lower() in ['.jpg','.png'] and i!=39];ck(all(path in images for path in required_images),'every mandatory manifest image present');ck(len([x for x in images.values() if x['dimensions']==[2697,1797]])==16,'all16 full original Spirit panels');ck(actual['unique_visual_sources']==54 and actual['public_image_blocks']==58,'54 unique sources/58 original image deliveries');ck(sum(len(x['public_image_deliveries']) for x in actual['visuals'])==58 and all(v['detail']=='original' for x in actual['visuals'] for v in x['public_image_deliveries']),'all58 deliveries are assigned canonical original bytes')
der=l['publisher_visible_prose_derivation'];soup=BeautifulSoup(Path(der['input_path']).read_text(),'html.parser')
for node in soup(['script','style','template','noscript']):node.decompose()
ck(soup.get_text('\n',strip=True)==Path(der['output_path']).read_text() and H(der['output_path'])==der['output_sha256'],'independent complete publisher visible prose')
profile=load(B/'runtime/scope_and_coverage_14-final-completed-projection.json');ck(len(profile['turn_contexts'])==2 and all(x=={'model':'gpt-6.1-sol','effort':'high'} for x in profile['confirmed_settings']) and profile['requested_spawn']['fields']['fork_turns']=='none','fresh actual2 model contexts6.1high originalnone')
working=load(B/'working45-46-adoption.json');ck(working['question_count']==173 and working['mapped_fact_count']==506 and working['new_question_counts']==[0,0],'prior current actual working0/0 gate')
output={'all_passed':True,'counts':{'checks':len(checks),'blocking_failed_checks':0,'questions':173,'mapped_fact_entries':506,'whole_text_inputs':22,'recorded_actual_source_events':245,'unique_source_ranges':231,'contiguous_partition_ranges':229,'additional_focused_reopens':2,'duplicate_reread_rows':14,'unique_visual_sources':54,'actual_original_image_deliveries':58,'native_panels':16},'checks':checks,'frozen_artifact_sha256':{name:H(B/name) for name in freeze['files']},'actual_transport_proof_sha256':H(B/'scope14-actual-delivery-validation.json'),'one_range_proof_sha256':H(B/'scope14-one-range-event-validation.json'),'limitations':'Source transport, literal input equality and attested full review remain distinct from cognition. Full parent semantic review and current independent coverage adoption are separate; no guide source audit or reader QA approval is implied.'};p=B/'scope14-structural-reference-validation.json';assert not p.exists();p.write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({'all_passed':True,'counts':output['counts'],'sha256':H(p)}))
