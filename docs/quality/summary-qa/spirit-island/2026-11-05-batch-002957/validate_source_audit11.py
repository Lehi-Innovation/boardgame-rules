"""Read-only filesystem and reference validation; perception and judgment are separate."""
from pathlib import Path
import collections
import hashlib
import json
import fitz
from PIL import Image
from bs4 import BeautifulSoup

B = Path(__file__).resolve().parent
ROOT = B.parents[4]
H = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
load = lambda p: json.loads(Path(p).read_text())
r = load(B/'source-audit-final-11.json')
l = load(B/'source-audit-final-11-read-ledger.json')
v = load(B/'source-audit-final-11-visual-manifest.json')
manifest = load(B/'supplemental-source-manifest-v4.json')
checks = []
def check(label, condition):
    assert condition, label
    checks.append({'name':label,'passed':True})

check('exact unchanged current candidate', r['candidate_sha256'] == H(ROOT/r['candidate_path']) == H(ROOT/'rules/spirit-island.md') == 'a5970cf774ee1c803e6f6f27e0bba3fac622e9b16ab7c02deab12539d08a862d')
check('zero reported findings', r['verdict'] == 'PASS' and r['findings'] == [] and r['finding_counts'] == {'MAJOR':0,'MINOR':0,'unresolved':0})
freeze = load(B/'source-audit11-original-freeze.json')
for name,data in freeze['files'].items():
    check('original raw freeze '+name, H(B/name) == data['sha256'])
source_rows = collections.defaultdict(list)
for row in l['text_slices']:
    p = ROOT/row['path']; text = p.read_text(); start,end = row['start'],row['end']
    check('full source hash '+p.name, H(p) == row['source_sha256'])
    check('literal source slice '+p.name, len(text) == row['character_length'] and 0 < end-start <= 6000 and hashlib.sha256(text[start:end].encode()).hexdigest() == row['slice_sha256'])
    check('range cap and truncation metadata', row['output_cap'] >= 4000 and row['truncated'] is False)
    source_rows[row['path']].append(row)
for path,rows in source_rows.items():
    rows.sort(key=lambda x:x['start']);text=(ROOT/path).read_text()
    check('complete contiguous '+Path(path).name, rows[0]['start']==0 and rows[-1]['end']==len(text) and all(a['end']==z['start'] for a,z in zip(rows,rows[1:])))
    coverage=next(x for x in l['coverage'] if x['path']==path)
    check('coverage metadata '+Path(path).name, coverage['contiguous_complete'] and coverage['character_length']==len(text) and coverage['slice_count']==len(rows))
check('all15 sources90 slices',len(source_rows)==len(l['coverage'])==15 and len(l['text_slices'])==90)
check('flat report delivery equals ledger',r['source_delivery']==[{k:x[k] for k in ['path','start','end','source_sha256','slice_sha256','truncated']} for x in l['text_slices']])
for path,digest in load(B/'source-manifest.json')['paths_and_sha256'].items():
    check('assigned source capture hash '+Path(path).name,H(ROOT/path)==digest)
citations=0
for group in r['checked_groups']:
    check('checked group has explicit semantic result',bool(group['name']) and bool(group['scope']) and group['result']=='checked; no unresolved discrepancy')
    for ref in group['sources']:
        p=ROOT/ref['path'];text=p.read_text()
        check('citation uses fully delivered source',ref['path'] in source_rows and H(p)==ref['source_sha256'])
        check('literal primary citation',text[ref['start']:ref['end']]==ref['passage'] and bool(ref['passage']))
        citations+=1
visuals={str((ROOT/x['path']).resolve()):x for x in v['visual_sources']}
check('58 distinct complete visuals',len(visuals)==58 and v['native_panels']==16 and v['printed_card_faces']==33 and v['core_faces']==31 and v['excluded_bc_exemplars']==2)
for path,row in visuals.items():
    p=Path(path)
    with Image.open(p) as img:
        check('visual dimensions '+p.name,list(img.size)==row['dimensions'])
    check('visual exact hash and declared native delivery '+p.name,H(p)==row['source_sha256'] and row['detail']=='original' and row['full_native_image_delivered'] is True)
panels=[x for x in v['visual_sources'] if x['kind']=='original Spirit panel']
check('all16 original native panels',len(panels)==16 and all((ROOT/x['path']).stat().st_size==19419092 and x['dimensions']==[2697,1797] for x in panels))
check('all33 complete printed faces',sum(x['kind']=='printed card face' for x in v['visual_sources'])==33)
for group in r['checked_groups']:
    check('group visual references resolve',all(str((ROOT/p).resolve()) in visuals for p in group['visual_source_paths']))
reconciliation=r['supplemental_record_reconciliation']
check('all72 supplemental dispositions exactly once',len(reconciliation)==72 and [x['record_index_zero_based'] for x in reconciliation]==list(range(72)))
for row,source in zip(reconciliation,manifest['source_records']):
    p=ROOT/row['path']
    check('supplemental exact identity '+str(row['record_index_zero_based']),p.resolve()==Path(source['path']).resolve() and H(p)==source['sha256']==row['sha256_actual']==row['sha256_expected'] and row['hash_matches'])
    check('supplemental explicit role '+str(row['record_index_zero_based']),bool(row['role']) and bool(row['reconciliation']))
    if row['role']=='completely read text':
        check('mandatory supplemental prose actually in ledger',row['path'] in source_rows)
    if row['role']=='directly viewed primary or faithful render':
        check('supplemental primary image in visual list',str(p.resolve()) in visuals)
html_path=Path(manifest['source_records'][35]['path'])
soup=BeautifulSoup(html_path.read_text(),'html.parser')
for tag in soup(['script','style','noscript','template']):tag.decompose()
visible=soup.get_text('\n',strip=True)
publisher=ROOT/next(p for p in source_rows if p.endswith('audit11-publisher-branch-claw-visible.txt'))
check('independent complete publisher prose derivation',visible==publisher.read_text() and len(visible)==4329)
pixels=[]
core_document=fitz.open(ROOT/'source_pdfs/spirit-island-rules.pdf')
for row in v['visual_sources']:
    if row['kind'] not in ['independent core PDF render','independent expansion legend render']:continue
    pdf=ROOT/'source_pdfs/spirit-island-rules.pdf' if row['kind']=='independent core PDF render' else ROOT/manifest['source_records'][1]['path']
    # Reproduce the recorded renderer sequence, including one shared CORE document.
    # Reopening it for each page changes a small cached-font raster on page 7.
    document=core_document if row['kind']=='independent core PDF render' else fitz.open(pdf)
    try:
        page=document[row['page']-1]
        with Image.open(ROOT/row['path']) as image:
            target=image.convert('RGB');matched=[]
            for scale in [1.5]:
                pix=page.get_pixmap(matrix=fitz.Matrix(scale,scale),alpha=False)
                if (pix.width,pix.height)==target.size and pix.samples==target.tobytes():matched.append(scale)
            check('PDF original page pixels '+Path(row['path']).name,bool(matched))
            pixels.append({'path':row['path'],'page':row['page'],'matching_scale':matched})
    finally:
        if document is not core_document:document.close()
core_document.close()
check('all five independent source-book page renders verified',len(pixels)==5)
actual=load(B/'source-audit11-actual-delivery-validation.json')
check('actual full90 text and58 native visual delivery',actual['verified'] and actual['text_sources']==15 and actual['actual_distinct_text_range_deliveries']==90 and actual['unique_visual_sources']==58 and actual['public_image_blocks']==58)
proof={'all_passed':True,'checks':checks,'counts':{'checks':len(checks),'blocking_failed_checks':0,'successful_text_slices':90,'complete_text_sources':15,'visual_sources':58,'actual_image_deliveries':58,'mandatory_supplemental_records':72,'literal_primary_citations':citations},'pdf_pixel_checks':pixels,'candidate_sha256':r['candidate_sha256'],'frozen_artifact_sha256':{n:H(B/n) for n in ['source-audit-final-11.json','source-audit-final-11-read-ledger.json','source-audit-final-11-visual-manifest.json','source-audit11-actual-delivery-validation.json']},'limitation':'Filesystem/reference and actual delivery checks are distinct from cognition. Parent semantic review and the independent source judgment are separately recorded.'}
dest=B/'source-audit11-evidence-validation.json'
assert not dest.exists()
dest.write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps({'all_passed':True,'counts':proof['counts'],'pdf_pixel_checks':pixels}))
