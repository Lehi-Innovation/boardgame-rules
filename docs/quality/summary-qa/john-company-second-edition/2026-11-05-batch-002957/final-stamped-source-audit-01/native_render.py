import sys,json
from pathlib import Path
from audit_helpers import OUT,SOURCES,sha
sys.path.insert(0,str(OUT/'runtime'))
import fitz
record_path=OUT/'source-read-record.json'
def derivative_record(item):
 d=json.loads(record_path.read_text());d['native_renders'].append(item);record_path.write_text(json.dumps(d,indent=2)+'\n')
for alias in ['board','bridge','fronts']:
 src=SOURCES[alias];doc=fitz.open(src);textpath=OUT/f'{alias}-native-extract.txt'
 textpath.write_text('\n'.join(f'--- PDF physical page {i+1} ---\n{p.get_text()}' for i,p in enumerate(doc)))
 derivative_record({'kind':'native text extraction','original':str(src),'original_sha256':sha(src),'derivative':str(textpath),'derivative_sha256':sha(textpath),'tool':'PyMuPDF 1.28.2 Page.get_text()','pdf_physical_pages':f'1–{len(doc)}'})
 print(alias,'pages',len(doc),'text LF',len(textpath.read_text().split('\n')))
 for i,p in enumerate(doc):print('PAGE',i+1,repr(p.get_text()[:230]))
for alias,pages,scale in [('pdf',[4,5,33,42],1.5),('board',[1],1.5),('bridge',list(range(1,len(fitz.open(SOURCES['bridge']))+1)),1.25),('fronts',[9],1.5)]:
 src=SOURCES[alias];doc=fitz.open(src)
 for page in pages:
  p=doc[page-1];out=OUT/f'{alias}-physical-page-{page:02}.png';p.get_pixmap(matrix=fitz.Matrix(scale,scale)).save(out)
  derivative_record({'kind':'native PDF page render','original':str(src),'original_sha256':sha(src),'pdf_physical_page':page,'printed_page_label':page if alias=='pdf' else None,'derivative':str(out),'derivative_sha256':sha(out),'tool':'PyMuPDF 1.28.2 Page.get_pixmap','matrix':[scale,scale],'clip':None})
