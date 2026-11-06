import sys
sys.dont_write_bytecode=True
from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent
A=HERE.parent/'final-stamped-source-audit-01'
rr=json.loads((A/'source-read-record.json').read_text())
# Only the manifest-bound installed rendering library is imported; no auditor helpers.
sys.path.insert(0,str(A/'runtime'))
import pymupdf
def sha(b):return hashlib.sha256(b).hexdigest()
docs={}
receipts=[]
for item in rr['native_renders']:
    original=item['original']
    if original not in docs:docs[original]=pymupdf.open(original)
    doc=docs[original]
    record={'original':original,'original_sha256':sha(Path(original).read_bytes()),'derivative':item['derivative'],'declared_sha256':item['derivative_sha256'],'declared_tool':item['tool'],'pdf_page_count':len(doc),'method':'Independent in-memory reproduction; no original audit scripts executed'}
    if item['kind']=='native text extraction':
        b='\n'.join(f'--- PDF physical page {i+1} ---\n{p.get_text()}' for i,p in enumerate(doc)).encode()
        record['physical_pages']=item['pdf_physical_pages']
    else:
        page=doc[item['pdf_physical_page']-1]
        clip=item.get('clip')
        pix=page.get_pixmap(matrix=pymupdf.Matrix(*item['matrix']),clip=pymupdf.Rect(clip) if clip else None)
        b=pix.tobytes('png')
        text_lines=page.get_text().split('\n')
        numeric=[{'extracted_line_zero_based':i,'text':s} for i,s in enumerate(text_lines) if s.strip().isdigit() and (i<5 or i>len(text_lines)-7)]
        record.update({'physical_page':item['pdf_physical_page'],'printed_page_label_declared':item['printed_page_label'],'pdf_metadata_page_label':page.get_label(),'edge_numeric_text':numeric,'matrix':item['matrix'],'clip':clip,'png_width':pix.width,'png_height':pix.height,'png_channels':pix.n})
    record.update({'reproduced_sha256':sha(b),'reproduced_bytes':len(b),'matches_original_binding':record['original_sha256']==item['original_sha256'],'matches_derivative':sha(b)==item['derivative_sha256'],'matches_existing_derivative_bytes':b==Path(item['derivative']).read_bytes()})
    receipts.append(record)
(HERE/'native-reproduction-receipts.json').write_text(json.dumps({'pymupdf_version':pymupdf.VersionBind,'mupdf_version':pymupdf.VersionFitz,'pymupdf_module_path':pymupdf.__file__,'receipts':receipts},indent=2)+'\n')
for d in docs.values():d.close()
print(json.dumps({'pymupdf_version':pymupdf.VersionBind,'all_native_derivatives':len(receipts),'exact_matches':sum(x['matches_derivative'] and x['matches_existing_derivative_bytes'] for x in receipts),'printed_page_evidence':[{k:r[k] for k in ['physical_page','printed_page_label_declared','edge_numeric_text']} for r in receipts if 'physical_page' in r]}))
