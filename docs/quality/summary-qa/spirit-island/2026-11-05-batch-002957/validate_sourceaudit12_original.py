"""Validate original source12 transport/reference facts, without adopting its incorrect card note."""
from pathlib import Path
from PIL import Image
from bs4 import BeautifulSoup
import hashlib,json,collections,fitz
B=Path(__file__).resolve().parent;ROOT=B.parents[4];H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();load=lambda p:json.loads(Path(p).read_text());checks=[]
def ck(ok,label):
 assert ok,label
 checks.append({'name':label,'passed':True})
r=load(B/'source-audit-final-12.json');l=load(B/'source-audit-final-12-read-ledger.json');v=load(B/'source-audit-final-12-visual-manifest.json');freeze=load(B/'source-audit12-original-freeze.json');actual=load(B/'source-audit12-actual-delivery-validation.json');bounded=load(B/'source-audit12-original-bounded-replay-and-one-range-validation.json');supp=load(B/'supplemental-source-manifest-v4.json')['source_records']
ck(r['candidate_sha256']==H(ROOT/r['candidate'])==H(ROOT/'rules/spirit-island.md')=='9a5b8bb543d32919be5035490de31f70b02b4ba5cfb23fd6a0b5b0b6db8b27f5','exact original current C23 candidate')
for name,data in freeze['files'].items():ck(H(B/name)==data['sha256'],'frozen original '+name)
parts=collections.defaultdict(list)
for row in l['entries']:
 p=ROOT/row['path'];text=p.read_text();a,z=row['start'],row['end'];ck(H(p)==row['source_sha256'] and len(text)==row['character_length'],'whole source identity '+p.name);ck(0<=a<z<=len(text) and z-a<=6000 and hashlib.sha256(text[a:z].encode()).hexdigest()==row['slice_sha256'],'literal source slice '+p.name+str([a,z]));ck(row['output_cap']>=4000 and row['truncated'] is False,'source cap/truncation');parts[row['path']].append(row)
for path,rows in parts.items():
 rows=sorted(rows,key=lambda x:x['start']);length=len((ROOT/path).read_text());ck(rows[0]['start']==0 and rows[-1]['end']==length and all(a['end']==z['start'] for a,z in zip(rows,rows[1:])),'complete contiguous '+Path(path).name);entry=next(x for x in l['coverage'] if x['path']==path);ck(entry['complete_contiguous_coverage'] and entry['range_count']==len(rows) and entry['character_length']==length,'coverage exact '+Path(path).name)
ck(len(parts)==17 and len(l['entries'])==94,'17 complete files94 slices');ck(r['source_delivery']==[{key:x[key] for key in ['path','start','end','source_sha256','slice_sha256','truncated']} for x in l['entries']],'flat report source delivery exact')
images={x['path']:x for x in v['images']};ck(len(images)==57 and v['count']==57 and v['native_panel_count']==16 and v['printed_card_face_count']==33 and v['core_card_count']==31 and v['excluded_BC_exemplar_count']==2,'full57 visual inventory')
for path,row in images.items():
 p=ROOT/path;ck(H(p)==row['source_sha256'] and list(Image.open(p).size)==row['dimensions'],'image exact bytes/dimensions '+p.name);ck(row['detail']=='original','original-detail visual '+p.name)
 if row['dimensions']==[2697,1797]:ck(p.stat().st_size==19419092 and row.get('resized') is False and row.get('cropped') is False,'entire19MB native panel '+p.name)
ck(sum(x['dimensions']==[2697,1797] for x in images.values())==16,'all16 original native panels')
textrefs=imagerefs=0
for group in r['checked_groups']:
 ck(bool(group['group']) and bool(group['scope']) and group['result']=='checked; no unresolved finding','explicit original semantic judgment '+group['group'])
 for ref in group['source_references']:
  p=ROOT/ref['path'];ck(H(p)==ref['source_sha256'],'checked-group source identity '+p.name)
  if 'passage' in ref:
   textrefs+=1;ck(ref['path'] in parts and p.read_text()[ref['start']:ref['end']]==ref['passage'] and ref['passage'],'literal copied source citation '+p.name)
   for sl in ref['delivery_ranges']:ck(any(x['start']==sl['start'] and x['end']==sl['end'] and x['slice_sha256']==sl['slice_sha256'] for x in parts[ref['path']]),'citation recorded source slice binding')
  else:imagerefs+=1;ck(ref['path'] in images,'visual source reference resolves '+p.name)
ck(len(r['checked_groups'])==21 and textrefs==72 and imagerefs==61,'all21 groups72 literal61visual references')
roles=r['supplemental_source_reconciliation'];ck(len(roles)==72,'all72 source dispositions')
for i,(role,entry) in enumerate(zip(roles,supp),1):ck(role['record_index']==i and (ROOT/role['path']).resolve()==Path(entry['path']).resolve() and role['source_sha256']==entry['sha256']==H(entry['path']) and role['manifest_hash_matches'] and bool(role['disposition']),'exact supplemental role '+str(i))
der=v['independent_source_html_derivation'];soup=BeautifulSoup((ROOT/der['input']).read_text(),'html.parser')
for node in soup(['script','style']):node.decompose()
ck(soup.get_text('\n',strip=True)==(ROOT/der['output']).read_text() and H(ROOT/der['output'])==der['output_sha256'],'complete independently derived publisher prose')
renders=sorted([row for row in v['images'] if 'matrix_scale' in row],key=lambda x:x['render_order']);ck([x['page'] for x in renders]==[6,7,17,32],'four independently rendered original CORE pages in recorded order');doc=fitz.open(ROOT/'source_pdfs/spirit-island-rules.pdf')
for row in renders:
 ck(row['original_pdf_sha256']==H(ROOT/row['original_pdf']) and row['matrix_scale']==[1.5,1.5],'exact original PDF/render method');pix=doc[row['page']-1].get_pixmap(matrix=fitz.Matrix(*row['matrix_scale']),alpha=False)
 with Image.open(ROOT/row['path']) as source:ck(source.size==(pix.width,pix.height) and source.convert('RGB').tobytes()==pix.samples,'exact independently reproduced PDF pixels p'+str(row['page']))
doc.close();ck(actual['verified'] and actual['text_sources']==17 and actual['actual_distinct_text_range_deliveries']==94 and actual['unique_visual_sources']==actual['public_image_blocks']==57,'original actual94text/57image transport');ck(bounded['verified'] and bounded['exact_original_transport_proof_reproduced'] and bounded['all94_actual_text_events_each_contain_one_known_source_range'] and bounded['record_cutoff_exclusive']==805,'immutable original transport prefix805/no future borrowing')
profile=load(B/'runtime/final_source_audit_12-final-completed-projection.json');ck(len(profile['turn_contexts'])==1 and profile['confirmed_settings']==[{'model':'gpt-6.1-sol','effort':'high'}] and profile['requested_spawn']['fields']['fork_turns']=='none','original fresh one actual6.1high context')
out={'all_passed':True,'counts':{'checks':len(checks),'blocking_failed_checks':0,'whole_text_inputs':17,'literal_ranges':94,'visual_sources':57,'actual_image_deliveries':57,'native_panels':16,'full_card_faces':33,'supplemental_roles':72,'checked_groups':21,'literal_primary_citations':72,'visual_references':61,'independent_CORE_page_renders':4},'checks':checks,'candidate_sha256':r['candidate_sha256'],'original_raw_hashes':{name:H(B/name) for name in freeze['files']},'original_actual_transport_sha256':H(B/'source-audit12-actual-delivery-validation.json'),'original_bounded_replay_sha256':H(B/'source-audit12-original-bounded-replay-and-one-range-validation.json'),'semantic_adoption':False,'known_card_observation_error_pending_own_correction':'Dissolve Town-to-two-Explorers note is incorrect. Physical/reference checks passing does not erase this semantic evidence error. Corrected full33-face recheck and parent judgment review required.','limitations':'Only filesystem, source references, pixels, exact recorded public source transport and original model metadata validated here. No current source-audit or full QA approval.'};p=B/'source-audit12-original-evidence-validation.json';assert not p.exists();p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'all_passed':True,'counts':out['counts'],'semantic_adoption':False,'sha256':H(p)}))
