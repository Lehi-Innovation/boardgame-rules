from pathlib import Path
from PIL import Image
from bs4 import BeautifulSoup
import hashlib,json,collections
B=Path(__file__).resolve().parent;ROOT=B.parents[4]
load=lambda p:json.loads(Path(p).read_text());H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();checks=[]
def ck(ok,label):
 assert ok,label
 checks.append(label)
r=load(B/'working-source-sweeps-45-46.json');l=load(B/'working-source-sweeps-45-46-read-ledger.json');v=load(B/'working-source-sweeps-45-46-visual-manifest.json');p=load(B/'working45-46-actual-delivery-validation.json');freeze=load(B/'working45-46-original-freeze.json');oldl=load(B/'novelty-adjudication-18/read-ledger.json');oldp=load(B/'novelty-adjudication-18/actual-delivery-validation.json');oldv=load(B/'novelty-adjudication-18/visual-manifest.json');boundary=load(B/'novelty-adjudication-18/completed-runtime-boundary.json')
for name,meta in freeze['files'].items():ck(H(B/name)==meta['sha256'],'immutable original '+name)
profile=load(B/'runtime/working45_46-final-completed-projection.json');ck(len(profile['confirmed_settings'])==3 and all(x=={'model':'gpt-6.1-sol','effort':'high'} for x in profile['confirmed_settings']),'three actual contexts correct');ck(profile['requested_spawn']['fields']['fork_turns']=='none','original fresh none');ck(sum(x['source_record']['runtime_line_ordinal']>=boundary['record_count'] for x in profile['turn_contexts'])==2,'two working-phase contexts after immutable original boundary')
with Path(profile['session_path']).open('rb') as f:ck(hashlib.sha256(f.read(boundary['prefix_bytes'])).hexdigest()==boundary['prefix_sha256'],'immutable original runtime prefix')
for row in r['input_bindings']:ck(H(row['path'])==row['full_byte_sha256'],'input hash '+row['path'])
q=load(B/'expanded-v24/questions.json')['questions'];ids=[x['id'] for x in q];m=load(B/'expanded-v24/asked-fact-map.json');ck(len(q)==173 and m['required_fact_count']==506,'current173/506');ck(r['all173_checked_ids']==ids,'all173 IDs')
for sweep in r['passes']:
 ck(sweep['checked_question_ids']==ids and sweep['mapped_fact_count']==506,'complete pass '+str(sweep['pass_number']));ck(sweep['new_question_count']==0 and not sweep['complete_survivors'] and not sweep['proposed_question_answer_minimum_fact_objects'],'zero survivors '+str(sweep['pass_number']));ck(len(sweep['actual_source_and_ask_work'])==18,'18 independently described families '+str(sweep['pass_number']))
ck(r['passes'][0]['actual_source_and_ask_work']!=r['passes'][1]['actual_source_and_ask_work'],'separately written actual sweeps');ck(not r['complete_remaining_base_procedure_proposal_set'],'complete empty survivor set');ck([x['id'] for x in r['current_actual_ask_and_fact_checks']]==ids,'all current asks checked');ck(all(x['checked_in_pass45'] and x['checked_separately_in_pass46'] for x in r['current_actual_ask_and_fact_checks']),'every actual ask twice');ck(r['no_questions_added_or_narrowed'],'no question changes')
rawranges=0;unique=0
for f in l['new_delivered_text_files']:
 path=Path(f['path']);text=path.read_text();ck(H(path)==f['full_byte_sha256'],'new file hash '+path.name);seen=set()
 for sl in f['slices']:
  a,z=sl['range'];ck(0<z-a<=6000 and hashlib.sha256(text[a:z].encode()).hexdigest()==sl['slice_utf8_sha256'] and not sl['truncated'],'exact bounded slice '+path.name+str([a,z]));seen.add((a,z));rawranges+=1
 ck(sorted(seen)==[tuple(x) for x in f['unique_ranges']],'unique range declaration '+path.name);unique+=len(seen)
 if f['complete_new_delivery']:
  cursor=0
  for a,z in sorted(seen):ck(a==cursor,'contiguous '+path.name+str(a));cursor=z
  ck(cursor==len(text),'whole new file '+path.name)
ck(rawranges==201 and unique==189,'201 raw/189 unique slices');ck(p['actual_distinct_text_range_deliveries']==189 and len({x['event_ordinal'] for x in p['text_deliveries']})==189,'189 separate proper actual public text events');ck(all(x['event_ordinal']>=549 for x in p['text_deliveries']),'new working events only')
oldfiles={x['path']:x for x in oldl['files']}
for f in l['own_hash_verified_complete_primary_text_reuse']:
 old=oldfiles[f['path']];ck(all(f[k]==value for k,value in old.items()),'own reused file exact original ledger '+Path(f['path']).name);ck(H(f['path'])==f['full_byte_sha256'],'own reused current hash '+Path(f['path']).name);ck(f['public_delivery_events']==[x for x in oldp['text_deliveries'] if x['path']==f['path']],'own reused exact actual receipts '+Path(f['path']).name)
ck(len(l['own_hash_verified_complete_primary_text_reuse'])==6,'six own whole primary text reuses')
oldimages={x['path']:x for x in oldv['images']};seenpaths=set();native=set();new=0;reuse=0
for row in v['images']:
 path=Path(row['path']);digest=row.get('sha256',row.get('full_byte_sha256'));dims=row.get('dimensions',row.get('native_dimensions'));ck(H(path)==digest,'image exact bytes '+path.name);ck(list(Image.open(path).size)==dims,'image actual dimensions '+path.name);seenpaths.add(str(path))
 if dims==[2697,1797]:native.add(str(path));ck(path.stat().st_size==19419092,'full native19MB '+path.name)
 if row.get('newly_viewed'):
  new+=1;ck(row['detail']=='original' and row['whole_region']==[0,0,*dims],'whole original view '+path.name)
 else:
  reuse+=1;ck({k:x for k,x in row.items() if k not in ['disposition','original_visual_manifest','actual_delivery_proof']}==oldimages[str(path)],'exact own previous image '+path.name)
ck(len(native)==16 and len(seenpaths)==53 and len(v['images'])==54,'16 native/53 unique/54 records');ck(new==46 and reuse==8 and p['public_image_blocks']==46,'46 new/8 reused original images');ck(len(p['visuals'])==46,'all new image byte receipts')
roles=r['source_corpus']['all72_supplemental_dispositions'];supp=load(B/'supplemental-source-manifest-v4.json')['source_records'];ck(len(roles)==len(supp)==72,'all72 dispositions')
for i,(row,entry) in enumerate(zip(roles,supp)):
 ck(row['record_index']==i and row['path']==entry['path'] and row['full_byte_sha256']==entry['sha256']==H(row['path']),'supplemental role exact source '+str(i))
ck(roles==l['supplemental_record_dispositions']==v['supplemental_record_dispositions'],'all three role lists exactly equal')
der=l['publisher_visible_prose_derivation'];soup=BeautifulSoup(Path(der['input']['path']).read_text(),'html.parser')
for node in soup(['script','style']):node.decompose()
ck(soup.get_text('\n',strip=True)==Path(der['output']['path']).read_text(),'independent publisher complete visible prose exact')
ck(len(r['remaining_findings'])==2 and all(x['new_question_count']==0 for x in r['remaining_findings']),'only two metadata pointer corrections')
ck(H(ROOT/'rules/spirit-island.md')=='a5970cf774ee1c803e6f6f27e0bba3fac622e9b16ab7c02deab12539d08a862d','C22 remains exact before semantic repair')
out={'verified':True,'check_count':len(checks),'checks':checks,'candidate_sha256':H(ROOT/'rules/spirit-island.md'),'bank':'expanded-v24','question_count':173,'mapped_fact_count':506,'working_new_question_counts':[0,0],'fresh_stopping_challenger_still_required':True,'delivery_proof_sha256':H(B/'working45-46-actual-delivery-validation.json'),'current_bank_given_fields_and_all_primary_citations_verified_by':'prepare_working4546_root_review.py','limitations':'Hashes, exact input equality, source transport and review completeness support these working sweeps; they do not prove cognition or universal absence. Independent fresh whole-corpus challenge remains required.'}
pout=B/'working45-46-evidence-validation.json';assert not pout.exists();pout.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'verified':True,'checks':len(checks),'sha256':H(pout)}))
