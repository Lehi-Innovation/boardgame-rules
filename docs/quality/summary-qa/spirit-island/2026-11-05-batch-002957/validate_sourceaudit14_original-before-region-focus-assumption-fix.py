"""Validate frozen source14 transport, source identities, references and render reproduction."""
from pathlib import Path
from functools import lru_cache
import collections,hashlib,json,shutil
from PIL import Image
from bs4 import BeautifulSoup
import fitz
B=Path(__file__).resolve().parent;ROOT=B.parents[4];load=lambda p:json.loads(Path(p).read_text())
@lru_cache(None)
def H(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
checks=[]
def ck(ok,label):
 assert ok,label
 checks.append({'check':label,'pass':True})
r=load(B/'source-audit-final-14.json');l=load(B/'source-audit-final-14-read-ledger.json');v=load(B/'source-audit-final-14-visual-manifest.json');freeze=load(B/'source-audit14-original-freeze.json');actual=load(B/'source-audit14-original-actual-delivery-validation.json');supp=load(B/'supplemental-source-manifest-v4.json')['source_records'];profile=load(B/'runtime/final_source_audit_14-final-completed-projection.json')
ck(r['candidate_sha256']==H(ROOT/r['candidate_path'])==H(B/'source-candidate-25.md')==H(ROOT/'rules/spirit-island.md')=='f0297380795b0939b0480cb52d97499a5d611b57a8243d5a56820099979727b6','exactC25 binding')
for n,x in freeze['files'].items():ck(H(B/n)==x['sha256']==H(x['original_completed_copy']),'original freeze unchanged '+n)
ck(profile['confirmed_settings']==[{'model':'gpt-6.1-sol','effort':'high'}] and profile['requested_spawn']['fields']['fork_turns']=='none','actual single initially fresh proper model context')
allowed={Path(p).resolve() for p in load(B/'source-manifest.json')['paths_and_sha256']}|{Path(x['path']).resolve() for x in supp}|{(B/n).resolve() for n in ['source-manifest.json','supplemental-source-manifest-v4.json','source-candidate-25.md']}
for d in l['independent_derivatives']:
 original=(ROOT/d['primary_path']).resolve();derived=(ROOT/d['derived_path']).resolve();ck(original in allowed and H(original)==d['primary_sha256'],'primary publisher identity');soup=BeautifulSoup(original.read_text(),'html.parser')
 for x in soup(['script','style','noscript','template','head']):x.decompose()
 prose=soup.get_text('\n',strip=True);ck(prose==derived.read_text()==d['complete_derived_text'] and H(derived)==d['derived_sha256'],'full documented visible prose independently reproduced');allowed.add(derived)
 dest=B/'pdf-inspection/audit14/publisher-branch-claw-visible-prose-preserved.txt';dest.parent.mkdir(parents=True,exist_ok=True)
 if dest.exists():ck(dest.read_bytes()==derived.read_bytes(),'preserved prose copy exact')
 else:shutil.copyfile(derived,dest)
parts=collections.defaultdict(list)
for x in l['source_delivery']:
 p=(ROOT/x['path']).resolve();s=p.read_text();a,z=x['start'],x['end'];ck(p in allowed,'allowed actual text '+p.name);ck(H(p)==x['source_sha256'] and len(s)==x['character_length'] and p.stat().st_size==x['byte_length'],'whole text identity '+p.name);ck(0<=a<z<=len(s) and z-a<=6000 and hashlib.sha256(s[a:z].encode()).hexdigest()==x['slice_sha256'],'exact bounded text '+p.name+str([a,z]));ck(x['output_cap']>=4000 and x['truncated'] is False and bool(x['truncation_check']),'declared cap and no truncation '+p.name);parts[x['path']].append(x)
for path,rows in parts.items():
 p=(ROOT/path).resolve();rows=sorted(rows,key=lambda x:x['start']);ck(rows[0]['start']==0 and rows[-1]['end']==len(p.read_text()) and all(x['end']==y['start'] for x,y in zip(rows,rows[1:])),'whole contiguous file '+p.name);entry=next(x for x in l['files'] if x['path']==path);ck(entry['complete_contiguous_delivery'] and entry['range_count']==len(rows) and entry['character_length']==len(p.read_text()) and entry['source_sha256']==H(p) and entry['byte_length']==p.stat().st_size,'whole file declared identity '+p.name)
ck(len(parts)==len(l['files'])==15 and len(l['source_delivery'])==91,'all15 complete files91 slices');ck({Path(p).name for p in parts}=={'source-manifest.json','supplemental-source-manifest-v4.json','source-candidate-25.md','spirit-island-rules.txt','living-faq-core-game.txt','living-faq-setup.txt','what-do-range-boosts-affect.txt','range-in-text-of-powers-that-target-spirits.txt','core-second-printing.txt','audit14-publisher-branch-claw-visible.txt','README.md','panel-download-map.json','download-integrity.json','independent-printed-photo-corroboration.json','novelty11-publisher-updates.txt'},'exact mandatory whole text inventory')
ck(r['source_delivery']==[{k:x[k] for k in ['path','start','end','source_sha256','slice_sha256','truncated']} for x in l['source_delivery']],'flat report delivery unchanged')
images={x['path']:x for x in v['observations']};ck(len(images)==len(v['observations'])==58,'58 distinct visual sources')
for path,row in images.items():
 p=(ROOT/path).resolve();ck(H(p)==row['sha256'] and p.stat().st_size==row['byte_length'] and list(Image.open(p).size)==row['dimensions'],'visual identity '+p.name);ck(row['viewed'] and row['detail_requested']==row['detail_forwarded']=='original' and row['region']=='entire image' and row['resized_or_cropped_for_delivery'] is False,'entire original detail '+p.name)
 if row['dimensions']==[2697,1797]:ck(p.stat().st_size==19419092,'whole19MB panel '+p.name)
native=[x for x in images.values() if x['dimensions']==[2697,1797]];ck(len(native)==16 and {Path(x['path']).name for x in native}=={s+'-'+side+'.png' for s in ['lightning','river','earth','shadows','green','thunderspeaker','ocean','bringer'] for side in ['front','back']},'all16 exact original-eight panels')
faces={str(Path(x['path']).resolve()) for x in supp if Path(x['path']).parent==(B/'card-scope-source') and Path(x['path']).suffix=='.jpg' and Path(x['path']).name!='all-named-card-title-corner-strips.jpg'};ck(len(faces)==33 and faces<={str((ROOT/x).resolve()) for x in images},'all33 full assigned faces')
ck(v['full_card_faces']==33 and v['original_core_card_faces']==31 and v['expansion_exclusion_exemplars']==2 and v['native_panel_views']==16,'declared exact core/exemplar inventory')
refs=0;visualrefs=0;guide=(B/'source-candidate-25.md').read_text();source_ref_receipts=[]
for group in r['checked_groups']:
 ck(bool(group['scope']) and bool(group['observations']) and group['result']=='checked; no unresolved finding' and bool(group['source_references']),'scoped human group '+group['group']);loc=group['candidate_location'];a=loc['start'];ck((ROOT/loc['path']).resolve()==(B/'source-candidate-25.md') and guide.startswith(loc['anchor'],a) and guide[:a].count('\n')+1==loc['line_one_based'],'exact candidate group anchor '+group['group'])
 for ref in group['source_references']:
  if 'start' in ref:
   refs+=1;p=(ROOT/ref['path']).resolve();s=p.read_text();a,z=ref['start'],ref['end'];ck(p in allowed and H(p)==ref['source_sha256'] and 0<=a<z<=len(s),'exact primary reference '+p.name);ck(ref['passage']==s[a:z],'literal primary passage '+p.name);source_ref_receipts.append({'path':str(p),'range':[a,z],'sha256':H(p),'passage_sha256':hashlib.sha256(s[a:z].encode()).hexdigest()})
  else:
   visualrefs+=1;ck(ref['visual_manifest']=='source-audit-final-14-visual-manifest.json','visual group reference manifest');names=ref.get('faces',ref.get('panels',[]));ck(bool(names) and all(x in {Path(p).name for p in images} for x in names),'all group image references resolve')
ck(len(r['checked_groups'])==18 and refs+visualrefs==59,'all18 groups59 references')
ck(r['supplemental_reconciliation']==v['membership_reconciliation'] and len(r['supplemental_reconciliation'])==len(supp)==72,'all72 roles identical preserved lists')
for i,(row,src) in enumerate(zip(r['supplemental_reconciliation'],supp),1):
 p=Path(src['path']).resolve();ck(row['record_number_one_based']==i and (ROOT/row['path']).resolve()==p and row['source_sha256']==src['sha256']==H(p) and row['manifest_hash_verified'] and bool(row['assigned_role']) and bool(row['independent_basis']),'independent justified supplemental hash/role '+str(i))
renders=[x['render_provenance'] for x in images.values() if 'render_provenance' in x];ck(len(renders)==v['independent_pdf_renders']==5,'five independent renders')
bydoc=collections.defaultdict(list)
for row in renders:bydoc[row['source_pdf']].append(row)
for pdf,rows in bydoc.items():
 rows.sort(key=lambda x:x['render_order']);doc=fitz.open(ROOT/pdf)
 for order,row in enumerate(rows,1):
  ck(H(ROOT/pdf)==row['pdf_sha256'] and row['render_order']==order and row['sha256']==H(ROOT/row['path']),'exact source/render provenance');pix=doc[row['page_one_based']-1].get_pixmap(matrix=fitz.Matrix(*row['matrix_scale']),alpha=False)
  with Image.open(ROOT/row['path']) as source:ck(source.size==(pix.width,pix.height) and source.convert('RGB').tobytes()==pix.samples,'pixel exact shared-document reproduction '+pdf+str(row['page_one_based']))
 doc.close()
ck([x['page_one_based'] for x in bydoc['source_pdfs/spirit-island-rules.pdf']]==[6,7,17,32],'all4 ordered CORE pages')
ck(actual['verified'] and actual['text_sources']==15 and actual['actual_distinct_text_range_deliveries']==91 and actual['unique_visual_sources']==actual['public_image_blocks']==58,'bounded original actual transport complete')
out={'all_passed':True,'semantic_adoption':False,'candidate_sha256':H(B/'source-candidate-25.md'),'counts':{'checks':len(checks),'blocking_failed_checks':0,'complete_text_files':15,'actual_text_ranges':91,'unique_visuals':58,'native_panels':16,'full_faces':33,'independent_pdf_renders':5,'checked_groups':18,'literal_primary_ranges':refs,'visual_group_references':visualrefs,'supplemental_reconciliations':72},'checks':checks,'primary_reference_receipts':source_ref_receipts,'frozen_artifact_sha256':{n:x['sha256'] for n,x in freeze['files'].items()},'original_actual_transport_sha256':H(B/'source-audit14-original-actual-delivery-validation.json'),'completed_model_projection_sha256':H(B/'runtime/final_source_audit_14-final-completed-projection.json'),'source13_counts_and_false_parent_flag_not_imported':True,'limitations':'Physical/literal/source identity checks only. Human source interpretations and PASS require separate complete semantic review. Public tool delivery is distinct from cognition. Publisher visible prose removes head as explicitly documented; it need not include invisible title metadata.'};p=B/'source-audit14-original-evidence-validation.json';assert not p.exists();p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['checks','primary_reference_receipts']}))
