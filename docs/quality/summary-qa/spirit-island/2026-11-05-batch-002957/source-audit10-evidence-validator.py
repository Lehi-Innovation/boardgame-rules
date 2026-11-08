#!/usr/bin/env python3
"""Read-only deterministic audit10 evidence validator. Writes no file; JSON on stdout."""
import hashlib,json,sys
from pathlib import Path
from collections import defaultdict,Counter
import fitz
from PIL import Image
from bs4 import BeautifulSoup
ROOT=Path('/home/jonny/projects/boardgame-rules')
B=ROOT/'docs/quality/summary-qa/spirit-island/2026-11-05-batch-002957'
EXPECTED='44746aca66da318da103537bbde4a690ed65b1c952936c0e5649487371a62e00'
def digest(b):return hashlib.sha256(b).hexdigest()
def read(p):return p.read_bytes()
def obj(p):return json.loads(read(p))
def resolve(p):return (ROOT/p).resolve()
def relative(p):return str(p.resolve().relative_to(ROOT)) if p.resolve().is_relative_to(ROOT) else __import__('os').path.relpath(p.resolve(),ROOT)
checks={};sources={}
def check(label,v):
 checks[label]=bool(v)
 if not v:raise AssertionError(label)
def source(p,expected=None):
 p=resolve(p) if isinstance(p,str) else p.resolve();h=digest(read(p));sources[relative(p)]=h
 if expected is not None:check('source-byte-hashes',h==expected and checks.get('source-byte-hashes',True))
 return p
try:
 rp=B/'source-audit-final-10.json';lp=B/'source-audit-final-10-read-ledger.json';vp=B/'source-audit-final-10-visual-manifest.json'
 report,ledger,visual=obj(rp),obj(lp),obj(vp)
 cp=source(report['candidate'],EXPECTED)
 check('candidate-bindings',all(x['candidate_sha256']==EXPECTED for x in [report,ledger,visual]))
 check('pass-zero-unresolved',report['verdict']=='PASS' and report['findings']==[] and report['completion']['unresolved_findings']==0)
 rows=ledger['rows'];by=defaultdict(list)
 for r in rows:
  p=source(r['path'],r['source_sha256']);t=read(p).decode('utf-8');s,e=r['start'],r['end'];
  check('bounded-unicode-ranges',isinstance(s,int) and isinstance(e,int) and 0<=s<e<=len(t) and e-s<=6000 and checks.get('bounded-unicode-ranges',True))
  check('text-lengths',r['character_length']==len(t) and checks.get('text-lengths',True))
  check('utf8-slice-hashes',digest(t[s:e].encode())==r['slice_sha256'] and checks.get('utf8-slice-hashes',True))
  check('caps-and-truncation-records',r['output_cap']>=4000 and r['truncated'] is False and bool(r['delivery_attestation']) and checks.get('caps-and-truncation-records',True))
  by[r['path']].append((s,e))
 for p,ranges in by.items():
  pos=0
  for s,e in sorted(set(ranges)):
   check('complete-contiguous-text',s==pos and checks.get('complete-contiguous-text',True));pos=e
  check('complete-contiguous-text',pos==len(read(resolve(p)).decode()) and checks.get('complete-contiguous-text',True))
 expectedrows=[{k:r[k] for k in ['path','start','end','source_sha256','slice_sha256','truncated']} for r in rows]
 check('report-delivery-rows-exact-no-dedup',report['source_delivery']==expectedrows)
 check('coverage-source-inventory',set(by)=={x['path'] for x in ledger['complete_sources']})
 mandatory=[report['candidate'],'extracted/spirit-island-rules.txt',relative(B/'source-manifest.json'),relative(B/'supplemental-source-manifest-v4.json')]
 P=ROOT/'docs/quality/summary-qa/batches/2026-11-05-batch-002957/source-preflight/spirit-island'
 mandatory += [relative(P/f) for f in ['living-faq-core-game.txt','living-faq-setup.txt','provenance.json']]
 mandatory += [relative(B/'card-scope-source'/f) for f in ['what-do-range-boosts-affect.txt','range-in-text-of-powers-that-target-spirits.txt','core-second-printing.txt']]
 mandatory += [relative(P/'original-spirit-panels'/f) for f in ['README.md','panel-download-map.json','download-integrity.json','independent-printed-photo-corroboration.json']]
 mandatory += [relative(B/'novelty11-source-scratch/novelty11-publisher-updates.txt'),relative(B/'pdf-inspection/audit10/audit10-publisher-visible.txt')]
 check('all-mandatory-text-roles',set(mandatory)<=set(by))
 sm=obj(B/'source-manifest.json');supp=obj(B/'supplemental-source-manifest-v4.json')
 for p,h in sm['paths_and_sha256'].items():source(p,h)
 source(B/'source-manifest.json');source(B/'supplemental-source-manifest-v4.json')
 ds=report['supplemental_manifest']['dispositions'];check('all-72-manifest-dispositions',len(supp['source_records'])==len(ds)==72 and ds==visual['supplemental_record_dispositions'])
 for i,(r,d) in enumerate(zip(supp['source_records'],ds)):
  p=source(r['path'],r['sha256'])
  check('manifest-disposition-bindings',d['record_index']==i and d['path']==relative(p) and d['manifest_sha256']==d['actual_sha256']==r['sha256'] and bool(d['reason']) and bool(d['disposition']) and checks.get('manifest-disposition-bindings',True))
 vs=visual['visuals'];ids={x['id'] for x in vs};check('unique-visual-ids',len(ids)==len(vs))
 for v in vs:
  p=source(v['path'],v['source_sha256']);im=Image.open(p)
  check('image-dimensions-and-observation-bindings',v['dimensions']==list(im.size) and v['detail']=='original' and bool(v['region']) and bool(v['observations']) and bool(v['inspection_attestation']) and checks.get('image-dimensions-and-observation-bindings',True))
 panels=[x for x in vs if x['kind'].startswith('original-core-panel-')];cards=[x for x in vs if x['kind']=='printed-card']
 check('all-16-native-panels',len(panels)==16 and all(v['dimensions']==[2697,1797] for v in panels) and len({v['path'] for v in panels})==16)
 check('all-33-printed-faces',len(cards)==33 and len({v['path'] for v in cards})==33)
 check('all-primary-visual-role-bindings',all(any(v['path']==relative(Path(r['path'])) for v in vs) for r in supp['source_records'] if r.get('role') in ['primary printed card face','primary printed original-base Spirit panel facsimile']))
 for d in ds:
  check('disposition-evidence-targets',all((v in ids or v in by) for v in d['bindings']) and checks.get('disposition-evidence-targets',True))
 for v in [x for x in vs if x['kind']=='direct-pdf-render']:
  pr=v['render_provenance'];p=source(pr['path'],pr['sha256']);doc=fitz.open(p);pix=doc[pr['pdf_page_1_based']-1].get_pixmap(matrix=fitz.Matrix(pr['matrix_scale'],pr['matrix_scale']));im=Image.open(resolve(v['path'])).convert('RGB')
  check('direct-pdf-render-pixels',pix.width==im.width and pix.height==im.height and pix.samples==im.tobytes() and checks.get('direct-pdf-render-pixels',True))
 check('direct-core-pages-6-7-17-32',sorted(v['page'] for v in vs if v['kind']=='direct-pdf-render' and v['render_provenance']['path']=='source_pdfs/spirit-island-rules.pdf')==[6,7,17,32])
 der=visual['publisher_visible_prose_derivation'];p=source(der['source_path'],der['source_sha256']);soup=BeautifulSoup(read(p),'html.parser')
 for x in soup(['script','style','noscript','template']):x.decompose()
 out=soup.get_text('\n',strip=True).encode();source(der['derived_path'],der['derived_sha256']);check('publisher-visible-prose-derivation',out==read(resolve(der['derived_path'])))
 for g in report['checked_groups']:
  check('checked-groups-evidence',bool(g['scope_checked']) and bool(g['source_references']) and all(x in ids for x in g['visual_references']) and checks.get('checked-groups-evidence',True))
  for r in g['source_references']:
   p=source(r['path'],r['source_sha256']);t=read(p).decode();check('exact-source-passages',t[r['start']:r['end']]==r['passage'] and checks.get('exact-source-passages',True))
 artifacts={relative(p):digest(read(p)) for p in [rp,lp,vp]}
 proof={'audit_id':'source-audit-final-10','candidate_sha256':EXPECTED,'artifact_sha256':artifacts,'source_sha256':dict(sorted(sources.items())),'validator_sha256':digest(read(Path(__file__))), 'filesystem_checks':dict(sorted(checks.items())),'counts':{'text_deliveries':len(rows),'complete_text_sources':len(by),'mandatory_text_roles':len(mandatory),'supplemental_records':len(ds),'visual_inspections':len(vs),'native_panels':len(panels),'printed_card_faces':len(cards),'direct_pdf_renders':sum(x['kind']=='direct-pdf-render' for x in vs),'checked_groups':len(report['checked_groups']),'findings':len(report['findings'])},'attestations_not_proved_by_filesystem':['Auditor actually received and read all recorded complete literal text slices.','Auditor independently viewed all listed complete original-resolution images.','Semantic comparison and PASS conclusion are the auditor\'s independent judgement.','No prohibited peer/history/question/answer/coverage/runtime input was inspected.'],'read_only_validator':True,'result':'PASS'}
 print(json.dumps(proof,sort_keys=True,separators=(',',':')))
except Exception as e:
 print(json.dumps({'audit_id':'source-audit-final-10','result':'FAIL','error':str(e),'checks_completed':checks},sort_keys=True,separators=(',',':')));sys.exit(1)
