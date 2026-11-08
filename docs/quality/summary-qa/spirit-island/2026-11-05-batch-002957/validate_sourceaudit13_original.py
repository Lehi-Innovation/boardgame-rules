"""Validate frozen original source13 evidence; do not adopt its erroneous card note."""
from pathlib import Path
from functools import lru_cache
from PIL import Image
from bs4 import BeautifulSoup
import hashlib,json,collections,fitz
B=Path(__file__).resolve().parent;ROOT=B.parents[4]
load=lambda p:json.loads(Path(p).read_text())
@lru_cache(None)
def H(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
checks=[]
def ck(ok,label):
 assert ok,label
 checks.append({'name':label,'passed':True})
r=load(B/'source-audit-final-13.json');l=load(B/'source-audit-final-13-read-ledger.json');v=load(B/'source-audit-final-13-visual-manifest.json');f=load(B/'source-audit13-original-freeze.json');actual=load(B/'source-audit13-original-actual-delivery-validation.json');boundary=load(B/'source-audit13-original-completed-runtime-boundary.json');supp=load(B/'supplemental-source-manifest-v4.json')['source_records']
ck(r['candidate_sha256']==H(ROOT/r['candidate_path'])==H(B/'source-candidate-24.md')==H(ROOT/'rules/spirit-island.md')=='954d203e6d2b1a59a5835381e786b01e0a88d86218ba1bde663018b2c6cab1de','exact C24 report/candidate/canonical binding')
for name,row in f['files'].items():
 ck(H(B/name)==row['sha256']==H(row['original_completed_copy']),'unchanged full original freeze '+name)
allowed={Path(p).resolve() for p in load(B/'source-manifest.json')['paths_and_sha256']}|{Path(x['path']).resolve() for x in supp}|{(B/n).resolve() for n in ['source-manifest.json','supplemental-source-manifest-v4.json','source-candidate-24.md','pdf-inspection/audit13/publisher-branch-claw-visible-prose.txt']}
parts=collections.defaultdict(list)
for row in l['deliveries']:
 p=(ROOT/row['path']).resolve();s=p.read_text();a,z=row['start'],row['end']
 ck(p in allowed,'allowed original authority/candidate/manifest/derivative '+p.name)
 ck(H(p)==row['source_sha256'] and len(s)==row['character_length'] and len(p.read_bytes())==row['byte_length'],'whole source identity/length '+p.name)
 ck(0<=a<z<=len(s) and z-a<=6000 and hashlib.sha256(s[a:z].encode()).hexdigest()==row['slice_sha256'],'exact <=6000 source slice '+p.name+str([a,z]))
 ck(row['output_cap']>=4000 and row['truncated'] is False,'explicit cap/nontruncation '+p.name+str([a,z]));parts[row['path']].append(row)
for path,rows in parts.items():
 rows=sorted(rows,key=lambda x:x['start']);p=ROOT/path;s=p.read_text();ranges=[[x['start'],x['end']] for x in rows]
 ck(ranges[0][0]==0 and ranges[-1][1]==len(s) and all(a[1]==z[0] for a,z in zip(ranges,ranges[1:])),'complete contiguous whole text '+p.name)
 listed=[x for x in l['source_files'] if x['path']==path];ck(len(listed)==1,'one whole-source ledger row '+p.name);entry=listed[0]
 ck(entry['complete_contiguous_coverage'] and entry['delivered_ranges']==ranges and entry['character_length']==len(s) and entry['byte_length']==p.stat().st_size and entry['source_sha256']==H(p),'whole-source ledger identity/ranges '+p.name)
expected_names={'source-manifest.json','supplemental-source-manifest-v4.json','source-candidate-24.md','spirit-island-rules.txt','living-faq-core-game.txt','living-faq-setup.txt','what-do-range-boosts-affect.txt','range-in-text-of-powers-that-target-spirits.txt','core-second-printing.txt','publisher-branch-claw-visible-prose.txt','novelty11-publisher-updates.txt','README.md','panel-download-map.json','download-integrity.json','independent-printed-photo-corroboration.json'}
ck({Path(x).name for x in parts}==expected_names and len(parts)==len(l['source_files'])==15 and len(l['deliveries'])==90,'all15 mandatory whole texts and90 literal ranges')
ck(r['source_delivery']==[{k:x[k] for k in ['path','start','end','source_sha256','slice_sha256','truncated']} for x in l['deliveries']],'report flat source-delivery exact')
images={x['path']:x for x in v['visual_sources']};ck(len(images)==len(v['visual_sources'])==57,'57 unique visual sources')
for path,row in images.items():
 p=ROOT/path;digest=row.get('source_sha256',row.get('sha256'))
 ck(H(p)==digest and list(Image.open(p).size)==row['dimensions'],'visual exact identity/dimensions '+p.name)
 ck(row['delivery_detail']=='original','declared original-detail view '+p.name)
 if 'resized_or_cropped_by_auditor' in row:ck(row['resized_or_cropped_by_auditor'] is False,'no auditor resize/crop '+p.name)
 if row['dimensions']==[2697,1797]:ck(p.stat().st_size==19419092,'entire19MB native panel '+p.name)
natives=[x for x in images.values() if x['dimensions']==[2697,1797]]
ck(len(natives)==16 and {Path(x['path']).name for x in natives}=={s+'-'+side+'.png' for s in ['lightning','river','earth','shadows','green','thunderspeaker','ocean','bringer'] for side in ['front','back']},'all16 original-eight native front/back panels')
faces={str(Path(x['path']).resolve()) for x in supp if Path(x['path']).parent==(B/'card-scope-source') and Path(x['path']).suffix=='.jpg' and Path(x['path']).name!='all-named-card-title-corner-strips.jpg'}
ck(len(faces)==33 and faces<={(ROOT/x).as_posix() for x in images},'all33 original full card faces from manifest')
ck(v['all_33_printed_faces_viewed'] and v['original_core_faces']==31 and v['B_and_C_exclusion_faces']==2 and v['all_16_original_spirit_panels_viewed_natively'],'declared complete core/exemplar/panel view inventory')
textrefs=visualrefs=anchors=0;citations=[]
for gi,g in enumerate(r['checked_groups']):
 ck(bool(g['scope_checked']) and bool(g['candidate_sections']) and g['result']=='checked; no unresolved finding' and bool(g['sources']),'explicit scoped original judgment '+g['group'])
 for si,ref in enumerate(g['sources']):
  p=ROOT/ref['path'];ck(H(p)==ref['source_sha256'],'source reference exact hash '+p.name)
  if 'character_range' in ref:
   textrefs+=1;s=p.read_text();a,z=ref['character_range'];ck(ref['path'] in parts and 0<=a<z<=len(s),'exact reconstructible primary range '+p.name)
   if ref.get('anchor'):
    anchors+=1;ck(ref['anchor'] in s[a:z],'literal authoritative anchor within cited range '+ref['anchor'])
   if ref.get('passage') is not None:ck(ref['passage'] in s[a:z],'literal copied source passage '+p.name)
   citations.append({'group_index':gi,'reference_index':si,'path':ref['path'],'source_sha256':ref['source_sha256'],'range':[a,z],'exact_range_text_sha256':hashlib.sha256(s[a:z].encode()).hexdigest(),'anchor':ref.get('anchor'),'passage_field_is_null':ref.get('passage') is None})
  else:
   visualrefs+=1;ck(ref['path'] in images and bool(ref['visual_region']),'visual reference resolves '+p.name)
ck(len(r['checked_groups'])==25 and textrefs==100 and visualrefs==95 and anchors==69,'all25 groups/100 reconstructible ranges/69 literal anchors/95visual references')
roles=r['supplemental_record_reconciliation'];ck(len(roles)==len(supp)==72,'all72 source roles')
for i,(row,src) in enumerate(zip(roles,supp),1):
 p=Path(src['path']);ck(row['record_number']==i and (ROOT/row['path']).resolve()==p.resolve() and row['manifest_sha256']==row['independently_computed_sha256']==src['sha256']==H(p) and row['hash_matches'] and bool(row['review_role']) and bool(row['authority_limit']) and bool(row['justification']),'exact justified supplemental disposition '+str(i))
 if row['review_role']=='fully_viewed_image':ck(row['path'] in images,'claimed whole-image role actually in visual ledger '+p.name)
 if row['review_role']=='completely_read_text':ck(row['path'] in parts,'claimed whole-text role actually in read ledger '+p.name)
der=v['publisher_html_derivation'];soup=BeautifulSoup((ROOT/der['source_path']).read_text(),'html.parser')
for node in soup(['script','style','noscript','template']):node.decompose()
visible=soup.get_text('\n',strip=True)
ck(H(ROOT/der['source_path'])==der['source_sha256'] and visible==(ROOT/der['visible_prose_derivative']).read_text() and H(ROOT/der['visible_prose_derivative'])==der['derivative_sha256'] and len(visible)==4329,'independently reproduced complete publisher visible prose')
renders=sorted([x for x in images.values() if 'matrix_scale' in x],key=lambda x:x['render_order']);ck([x['one_based_page'] for x in renders]==[6,7,17,32],'all4 independent CORE renders ordered')
doc=fitz.open(ROOT/'source_pdfs/spirit-island-rules.pdf')
for row in renders:
 ck(row['original_pdf_sha256']==H(ROOT/row['original_pdf']) and row['matrix_scale']==[1.5,1.5],'exact source PDF/render method')
 pix=doc[row['one_based_page']-1].get_pixmap(matrix=fitz.Matrix(*row['matrix_scale']),alpha=False)
 with Image.open(ROOT/row['path']) as source:ck(source.size==(pix.width,pix.height) and source.convert('RGB').tobytes()==pix.samples,'pixel-exact independent render reproduction p'+str(row['one_based_page']))
doc.close()
profile=load(B/'runtime/final_source_audit_13-original-final-completed-projection.json')
ck(len(profile['turn_contexts'])==1 and profile['confirmed_settings']==[{'model':'gpt-6.1-sol','effort':'high'}] and profile['requested_spawn']['fields']['fork_turns']=='none','one original fresh6.1Sol/high/forknone actual context')
ck(actual['verified'] and actual['text_sources']==15 and actual['actual_distinct_text_range_deliveries']==90 and actual['unique_visual_sources']==actual['public_image_blocks']==57 and actual['record_cutoff_exclusive']==boundary['record_count']==739 and actual['original_boundary_sha256']==H(B/'source-audit13-original-completed-runtime-boundary.json') and actual['one_source_range_per_matched_output_event'],'original actual90 text/57 images, single source range per event, immutable739-record boundary')
receipt=load(B/'source-audit13-root-original-review-receipt.json');ck(receipt['all_new_human_fields_preserved_and_received'] and len(receipt['single_range_actual_read_events'])==20 and receipt['projection_sha256']==H(B/'source-audit13-root-original-semantic-projection.json') and not receipt['semantic_adoption'],'full parent original judgment review, known error unadopted')
cp=B/'source-audit13-original-verified-primary-reference-ranges.json';assert not cp.exists();cp.write_text(json.dumps(citations,indent=2)+'\n')
out={'all_passed':True,'candidate_sha256':r['candidate_sha256'],'counts':{'checks':len(checks),'blocking_failed_checks':0,'whole_text_inputs':len(parts),'literal_ranges':len(l['deliveries']),'visual_sources':len(images),'actual_image_deliveries':actual['public_image_blocks'],'native_panels':len(natives),'full_card_faces':len(faces),'supplemental_roles':len(roles),'checked_groups':len(r['checked_groups']),'exact_primary_range_references':textrefs,'literal_FAQ_anchors':anchors,'visual_references':visualrefs,'independent_CORE_page_renders':len(renders)},'checks':checks,'frozen_artifact_sha256':{n:H(B/n) for n in f['files']},'actual_original_transport_sha256':H(B/'source-audit13-original-actual-delivery-validation.json'),'original_runtime_boundary_sha256':H(B/'source-audit13-original-completed-runtime-boundary.json'),'parent_review_receipt_sha256':H(B/'source-audit13-root-original-review-receipt.json'),'semantic_adoption':False,'known_original_source_note_error':'Dissolve City-to-two-Explorers transcription; own source-only full33-face correction/recheck pending. No guide body change.','limitations':'Passing source identity, range/anchor, image, pixel and public-transport checks does not erase the identified source-note error or establish a corrected semantic PASS. Null passage fields are accepted through their exact reconstructible source ranges/69 literal anchors; no metadata-shape failure inferred.'}
p=B/'source-audit13-original-evidence-validation.json';assert not p.exists();p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'all_passed':True,'counts':out['counts'],'semantic_adoption':False,'sha256':H(p)}))
