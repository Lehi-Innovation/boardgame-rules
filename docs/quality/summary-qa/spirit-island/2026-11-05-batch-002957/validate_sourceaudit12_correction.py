from pathlib import Path
from PIL import Image
import copy,hashlib,json,collections
B=Path(__file__).resolve().parent;ROOT=B.parents[4];load=lambda p:json.loads(Path(p).read_text());H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();HS=lambda s:hashlib.sha256(s.encode()).hexdigest();checks=[]
def ck(ok,label):
 assert ok,label
 checks.append({'name':label,'passed':True})
def diff(a,b,path=''):
 if a==b:return []
 if isinstance(a,dict) and isinstance(b,dict):return [p for k in sorted(set(a)|set(b)) for p in ([path+'/'+k] if k not in a or k not in b else diff(a[k],b[k],path+'/'+k))]
 if isinstance(a,list) and isinstance(b,list) and len(a)==len(b):return [p for i,(x,y) in enumerate(zip(a,b)) for p in diff(x,y,path+'/'+str(i))]
 return [path]
def at(d,p):
 for k in p.strip('/').split('/'):d=d[int(k)] if isinstance(d,list) else d[k]
 return d
r=load(B/'source-audit-final-12-corrected.json');v=load(B/'source-audit-final-12-corrected-visual-manifest.json');a=load(B/'source-audit12-own-correction-addendum.json');l=load(B/'source-audit12-correction-read-ledger.json');oldr=load(B/'source-audit-final-12.json');oldv=load(B/'source-audit-final-12-visual-manifest.json');oldl=load(B/'source-audit-final-12-read-ledger.json');actual=load(B/'source-audit12-correction-actual-delivery-validation.json');base=load(B/'source-audit12-original-evidence-validation.json')
ck(base['all_passed'] and base['counts']['checks']==903,'original903 physical/reference checks preserved')
for name in ['source-audit12-original-freeze.json','source-audit12-corrected-original-freeze.json']:
 for filename,row in load(B/name)['files'].items():ck(H(B/filename)==row['sha256'],'immutable output '+filename)
ck(load(B/'source-audit12-original-bounded-replay-and-one-range-validation.json')['exact_original_transport_proof_reproduced'],'bounded original94/57 proof byte reproduced')
ck(H(ROOT/'rules/spirit-island.md')==H(B/'source-candidate-23.md')==r['candidate_sha256']==a['candidate_sha256']==l['candidate_sha256'],'unchanged exactC23 canonical and all correction inputs')
ck(r['verdict']==a['corrected_verdict']=='PASS' and r['findings']==a['new_candidate_findings']==[],'corrected PASS0 candidate findings')
ck(r['source_delivery']==oldr['source_delivery'] and r['source_delivery']==[{k:row[k] for k in r['source_delivery'][0]} for row in oldl['entries']],'all original94 rows explicitly preserved as earlier delivery')
ck(len(a['changes'])==4 and a['counts']=={'factual_observation_corrections':1,'observation_clarifications':3,'actual_candidate_findings':0,'unverified_concerns':0},'one factual source-note correction and three clarifications')
report_obs=[];visual_obs=[]
for change in a['changes']:
 for field,target,original,dest in [('report_json_pointers',r,oldr,report_obs),('visual_manifest_json_pointers',v,oldv,visual_obs)]:
  for pointer in change[field]:ck(at(target,pointer)==change['after'] and at(original,pointer)==change['before'],'exact old/new note '+pointer);dest.append(pointer)
 ref=change['candidate_comparison']['candidate_evidence'];p=ROOT/ref['path'];ck(H(p)==ref['candidate_sha256'] and p.read_text()[ref['start']:ref['end']]==ref['passage'],'candidate comparison literal bound '+change['id']);ck(change['candidate_comparison']['actual_candidate_finding'] is False,'no candidate finding '+change['id'])
ck(set(diff(oldv,v))==set(visual_obs+['/correction_phase']),'only four visual observations and correction provenance changed')
rd=diff(oldr,r);ck(set(p for p in rd if p.startswith('/checked_groups/'))==set(report_obs),'only four checked-group observations changed')
ck(all(p in report_obs or p in ['/visual_manifest','/source_delivery_provenance','/correction_phase'] for p in rd),'all report differences are declared notes/provenance')
ck(a['changes']==r['correction_phase']['observation_changes'] and a['new_card_views']==l['new_card_views'],'complete correction changes and33 views exactly aliased')
ck(a['original_source_reuse']==l['original_source_reuse'],'reuse bindings agree')
for ref in a['original_artifacts']:ck(H(ROOT/ref['path'])==ref['sha256'] and ref['preserved_byte_for_byte'],'own original artifact retained '+Path(ref['path']).name)
reuse=l['original_source_reuse'];ck(reuse['source_delivery_count']==94 and reuse['preserved_array_equal'] and reuse['original_ledger_sha256']==H(B/'source-audit-final-12-read-ledger.json'),'94 original reuse explicitly bound')
for field,n in [('candidate_prior_delivery_ranges',9),('complete_FAQ_prior_delivery_ranges',35)]:ck(len(reuse[field])==n,'own complete prior '+field)
for row in oldl['entries']+l['new_text_deliveries']:
 p=ROOT/row['path'];s=p.read_text();start,end=row['start'],row['end'];ck(H(p)==row['source_sha256'] and len(s)==row['character_length'],'unchanged source identity '+p.name);ck(0<=start<end<=len(s) and end-start<=6000 and HS(s[start:end])==row['slice_sha256'] and row['output_cap']>=4000 and row['truncated'] is False,'exact bounded source range '+p.name+str([start,end]))
groups=collections.defaultdict(list)
for row in l['new_text_deliveries']:groups[row['path']].append(row)
whole=partial=0
for path,rows in groups.items():
 ranges=sorted((x['start'],x['end']) for x in rows);s=(ROOT/path).read_text()
 if Path(path).name=='living-faq-core-game.txt':partial+=len(rows);ck(len(rows)==2 and len(s)==207859,'two focused FAQ reopens only')
 else:whole+=1;ck(ranges[0][0]==0 and ranges[-1][1]==len(s) and all(x[1]==y[0] for x,y in zip(ranges,ranges[1:])),'new whole own artifact '+Path(path).name)
ck(whole==3 and partial==2 and len(l['new_text_deliveries'])==51,'three whole own artifacts49ranges and two focused reopens')
ck(actual['verified'] and actual['actual_distinct_text_range_deliveries']==51 and actual['unique_visual_sources']==actual['public_image_blocks']==34 and all(x['event_ordinal']>=805 for x in actual['text_deliveries']),'actual correction-only51/34 after original boundary805')
views=l['new_card_views']+[l['additional_native_panel_view']];ck(len(views)==len({x['path'] for x in views})==34,'33 full cards plus native Shadows')
for row in views:
 p=ROOT/row['path'];ck(H(p)==row['source_sha256'] and list(Image.open(p).size)==row['dimensions'],'exact original image '+p.name);ck(row['detail_requested']==row['detail_forwarded']=='original' and not row['resized'] and not row['cropped'] and row['actually_received_and_rechecked'],'whole original new view '+p.name)
profile=load(B/'runtime/final_source_audit_12-corrected-final-completed-projection.json');ck(len(profile['turn_contexts'])==2 and all(x=={'model':'gpt-6.1-sol','effort':'high'} for x in profile['confirmed_settings']) and profile['requested_spawn']['fields']['fork_turns']=='none','all2 actual model contexts61high initialnone')
# Replay the public correction matcher without writing over its frozen proof.
code=(B/'verify_sourceaudit12_correction_actual_delivery.py').read_text();code=code[:code.index('dest = B /')];ns={'__file__':str(B/'verify_sourceaudit12_correction_actual_delivery.py')};exec(compile(code,'correction-public-payload-replay','exec'),ns);ck((json.dumps(ns['proof'],indent=2)+'\n').encode()==(B/'source-audit12-correction-actual-delivery-validation.json').read_bytes(),'actual correction proof byte reproduced')
snips=[(ROOT/x['path']).read_text()[x['start']:x['end']] for x in l['new_text_deliveries']];outputs={x['ordinal']:x for x in ns['outputs']};events=[]
for idx,receipt in enumerate(ns['receipts']):
 output=outputs[receipt['event_ordinal']];primary=snips[idx];texts=[x['text'] for x in output['texts']];ck(sum(t.count(primary) for t in texts)==1,'one full primary range event '+str(receipt['event_ordinal']));residual=[t.replace(primary,'',1) for t in texts];ck(not any(s in t for s in snips for t in residual),'no second complete known range outside literal '+str(receipt['event_ordinal']));ck(not any(primary in s and s!=primary and s in t for s in snips for t in texts),'no overlarge source superrange '+str(receipt['event_ordinal']));events.append({'event_ordinal':receipt['event_ordinal'],'one_literal_source_range':True})
one={'verified':True,'events_checked':51,'all51_claimed_ranges_matched_to_separate_single_range_events':True,'post_original_boundary_records':805,'actual_proof_sha256':H(B/'source-audit12-correction-actual-delivery-validation.json'),'events':events,'no_private_runtime_bodies_copied':True};p=B/'source-audit12-correction-one-range-event-validation.json';assert not p.exists();p.write_text(json.dumps(one,indent=2)+'\n')
names=list(load(B/'source-audit12-corrected-original-freeze.json')['files'])+['source-audit12-original-evidence-validation.json','source-audit12-original-bounded-replay-and-one-range-validation.json','source-audit12-correction-actual-delivery-validation.json','source-audit12-correction-one-range-event-validation.json','source-audit12-corrected-root-review-receipt.json']
for n in names:ck((B/n).exists(),'evidence exists '+n)
out={'all_passed':True,'candidate_sha256':r['candidate_sha256'],'counts':{'checks':len(checks),'blocking_failed_checks':0,'original_physical_checks':903,'new_text_ranges':51,'new_whole_own_artifacts':3,'focused_FAQ_reopens':2,'new_full_card_views':33,'new_native_panel_views':1,'original_text_ranges':94,'original_whole_text_inputs':17,'original_visual_sources':57,'actual_model_contexts':2,'candidate_findings':0},'checks':checks,'frozen_artifact_sha256':{n:H(B/n) for n in names},'limitations':'Transport/hash/structure verification is separate from semantic judgment. Original observations are selective procedural notes, not complete card-number transcriptions. Full parent corrected semantic projection reviewed separately; original documents remain authoritative.'};p=B/'source-audit12-corrected-evidence-validation.json';assert not p.exists();p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'all_passed':True,'counts':out['counts'],'sha256':H(p)}))
