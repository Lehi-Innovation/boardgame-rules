from pathlib import Path
import json,hashlib,fitz
from PIL import Image
R=Path('/home/jonny/projects/boardgame-rules');B=R/'docs/quality/summary-qa/spirit-island/2026-11-05-batch-002957';F=R/'docs/quality/summary-qa/batches/2026-11-05-batch-002957/source-preflight/spirit-island';P=F/'original-spirit-panels';C=B/'card-scope-source';sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
paths=[B/'source-audit-final-09.json',B/'source-audit-final-09-read-ledger.json',B/'source-audit-final-09-visual-manifest.json'];frozen={str(p.relative_to(R)):sha(p) for p in paths};a,l,v=[json.loads(p.read_text()) for p in paths];rows=l['source_delivery'];errors=[];checks=[]
def check(label,condition):
 checks.append({'check':label,'pass':bool(condition)})
 if not condition:errors.append(label)
def at(p):return Path(p) if Path(p).is_absolute() else R/p
cand=B/'source-candidate-20.md';raw=cand.read_bytes();s=raw.decode();check('candidate exact sha256/bytes/Unicode chars',sha(cand)==a['candidate_sha256']=='63da3a8f472025ad10028eba03c11ec1ad00b2455cb3e70a08bafa6ae90bdb24' and len(raw)==52590 and len(s)==52388)
flat=[{k:r[k] for k in ['path','start','end','source_sha256','slice_sha256','truncated']} for r in rows];check('flat source_delivery equals richer ledger rows exactly',flat==a['source_delivery'])
required=[B/'final-source-audit-09-prompt.txt',B/'source-manifest.json',B/'supplemental-source-manifest-v4.json',cand,R/'extracted/spirit-island-rules.txt',F/'living-faq-core-game.txt',F/'living-faq-setup.txt',C/'what-do-range-boosts-affect.txt',C/'range-in-text-of-powers-that-target-spirits.txt',C/'core-second-printing.txt',B/'novelty11-source-scratch/novelty11-publisher-updates.txt']+[P/x for x in ['README.md','panel-download-map.json','download-integrity.json','independent-printed-photo-corroboration.json']]
actual={at(r['path']).resolve() for r in rows};check('mandatory text inventory exact15 inputs',actual==set(p.resolve() for p in required))
for path in sorted(actual):
 rs=sorted([r for r in rows if at(r['path']).resolve()==path],key=lambda r:r['start']);txt=path.read_text();raw=path.read_bytes();pos=0
 for r in rs:
  check(f'{path.relative_to(R)} [{r["start"]},{r["end"]}) contiguous/hash/cap',r['start']==pos and 0<r['end']-r['start']<=6000 and r['end']<=len(txt) and r['source_sha256']==sha(path) and r['slice_sha256']==hashlib.sha256(txt[r['start']:r['end']].encode()).hexdigest() and r['character_length']==len(txt) and r['bytes']==len(raw) and r['output_cap']>=4000 and r['truncated'] is False);pos=r['end']
 check(f'{path.relative_to(R)} complete EOF',pos==len(txt))
manifest=json.loads((B/'supplemental-source-manifest-v4.json').read_text());recorded={at(x['path']).resolve():x for x in v['images']}
primary=[x for x in manifest['source_records'] if x.get('role')=='primary printed card face'];panels=[x for x in manifest['source_records'] if x.get('role')=='primary printed original-base Spirit panel facsimile'];check('33 card faces and16 original panels in permitted manifest',len(primary)==33 and len(panels)==16)
for x in primary+panels:
 p=Path(x['path']);check(f'{p.name} full-image manifest/actual byte hash',p.resolve() in recorded and sha(p)==x['sha256']==recorded[p.resolve()]['sha256'])
 for_dims=Image.open(p).size
 if x in panels:check(f'{p.name} native2697x1797',for_dims==(2697,1797))
for name in ['corroborating-all-spirits-2017.jpg','corroborating-2017-bringer-track-crop.png','corroborating-river-2018.jpg']:
 p=P/name;x=next(x for x in manifest['source_records'] if x.get('file')==name);check(f'{name} identity photo hash/manifest',p.resolve() in recorded and sha(p)==x['sha256']==recorded[p.resolve()]['sha256'])
for p,x in recorded.items():check(f'{p.name} actual bytes/dimensions match visual row',sha(p)==x['sha256'] and p.stat().st_size==x['bytes'] and list(Image.open(p).size)==x['dimensions'])
renderproof=[];out=Path('/tmp/audit09-evidence-rerenders');out.mkdir(exist_ok=True)
for src,pages,prefix,expect in [(R/'source_pdfs/spirit-island-rules.pdf',[6,7,17,32],'audit09-core','64012c21460d3aee0f5c2c0d1048811a4dd4b4aebd03284ee4706a6a1f8e630e'),(C/'branch-claw-rulebook.pdf',[6],'audit09-bc','7827216ab5f7bc1e8805d1a47adf2517d42fd88cc6961307a35f4bcccbef52ac')]:
 check(f'{src.name} original source sha256',sha(src)==expect);d=fitz.open(src)
 for page in pages:
  original=B/f'pdf-inspection/audit09/{prefix}-p{page}.png';new=out/original.name;d[page-1].get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(new);check(f'{original.name} exact rerender matches original',sha(new)==sha(original));renderproof.append({'original_path':str(original.relative_to(R)),'original_sha256':sha(original),'proof_path':str(new),'proof_sha256':sha(new),'source_pdf':str(src.relative_to(R)),'source_pdf_sha256':sha(src),'printed_page':page,'zero_based_page_index':page-1,'matrix':[1.5,1.5],'render_api':'PyMuPDF page.get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(path)','fitz_version':fitz.VersionBind,'parameter_basis':'Actual audit09 render command in this auditor’s tool-call history; original artifacts preserved.'})
canonical=R/'rules/spirit-island.md';canonical_check={'performed':'bytes-only comparison; canonical prose not delivered or used as rules input','equal':canonical.read_bytes()==raw if False else canonical.read_bytes()==cand.read_bytes(),'canonical_sha256':sha(canonical),'candidate_sha256':sha(cand)}
check('all three originals preserved across validation',all(sha(R/p)==h for p,h in frozen.items()))
proof={'validator':'evidence-only; no new semantic verdict','artifact_hashes':frozen,'candidate_identity':{'sha256':sha(cand),'bytes':len(cand.read_bytes()),'characters':len(cand.read_text())},'filesystem_checks':checks,'filesystem_errors':errors,'source_delivery_rows':len(rows),'text_input_count':len(actual),'visual_observation_count':len(v['images']),'exact_render_provenance':renderproof,'canonical_bytes_only':canonical_check,'historical_receipt_attestation':{'basis':'Auditor’s actual conversation tool responses, not inferred from existence or content of ledger files.','text':'All required text received/read in90 separate contiguous slices with5000-token explicit caps. No response truncated. Initial manifests received separately and first slices reread for ledger capture.','images':'All33 card faces,16 full original panels,3 identity images and5 PDF renders actually received and visually inspected. Full native source images used; later image-detail option set original when tool made it available.','separation':'Machine checks prove present bytes/ranges/hash equality and reproduction, not historical reading or perception.'},'validator_path':'/tmp/audit09-evidence-validator.py','validator_sha256':sha('/tmp/audit09-evidence-validator.py')}
Path('/tmp/audit09-evidence-proof.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps({'passed':not errors,'checks':len(checks),'errors':errors,'artifacts':frozen,'validator_sha256':sha('/tmp/audit09-evidence-validator.py'),'proof_path':'/tmp/audit09-evidence-proof.json','proof_sha256':sha('/tmp/audit09-evidence-proof.json'),'canonical_bytes_equal':canonical_check['equal']},indent=2))
