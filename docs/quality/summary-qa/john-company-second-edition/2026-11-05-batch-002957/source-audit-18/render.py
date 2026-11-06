from pathlib import Path
import pymupdf,json,hashlib
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[5]
RUN=OUT.parent
items=[
 ('rules',ROOT/'source_pdfs/john-company-second-edition-rules.pdf',[28,32,41],1.6),
 ('board',RUN/'supplements/pnp/Board/John Company Game Board.pdf',[0],1.6),
 ('bridge_fronts',RUN/'supplements/pnp/Cards/John Company Cards (Bridge, Fronts).pdf',[0,5],1.8),
 ('bridge_fronts',RUN/'supplements/pnp/Cards/John Company Cards (Bridge, Fronts).pdf',[8],1.6),
 ('bridge_backs',RUN/'supplements/pnp/Cards/John Company Cards (Bridge, Bridge).pdf',[8],1.6)]
records=[]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for label,p,pages,scale in items:
 d=pymupdf.open(p)
 for pn in pages:
  dest=OUT/f'{label}-physical-page-{pn+1}.png'
  d[pn].get_pixmap(matrix=pymupdf.Matrix(scale,scale)).save(dest)
  records.append({'source':str(p),'source_sha256':sha(p),'physical_pdf_page_1_based':pn+1,'printed_page':20 if label=='bridge_backs' else pn+1,'scale':scale,'clip':None,'derivative':str(dest),'derivative_sha256':sha(dest)})
p=ROOT/'source_pdfs/john-company-second-edition-rules.pdf';d=pymupdf.open(p)
for pn,clip,name in [(41,(55,545,315,665),'firm-value-track'),(11,(315,620,390,725),'glencora-card')]:
 scale=8 if name=='glencora-card' else 3
 dest=OUT/f'{name}.png';d[pn].get_pixmap(matrix=pymupdf.Matrix(scale,scale),clip=pymupdf.Rect(*clip)).save(dest)
 records.append({'source':str(p),'source_sha256':sha(p),'physical_pdf_page_1_based':pn+1,'printed_page':pn+1,'scale':scale,'clip':clip,'derivative':str(dest),'derivative_sha256':sha(dest)})
(OUT/'native-derivative-provenance.json').write_text(json.dumps({'renderer':'PyMuPDF','version':pymupdf.VersionBind,'package_origin':pymupdf.__file__,'records':records},indent=2)+'\n')
print('rendered',len(records),'native derivatives')
