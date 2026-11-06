from pathlib import Path
import fitz,json,hashlib,re
root=Path('/home/jonny/projects/boardgame-rules');run=root/'docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957';out=run/'source-audit-17';r=json.loads((out/'source-read-record.json').read_text())
for p,pages in [(root/'source_pdfs/john-company-second-edition-rules.pdf',[32,41]),(run/'supplements/pnp/Cards/John Company Cards (Bridge, Fronts).pdf',[8]),(run/'supplements/pnp/Cards/John Company Cards (Bridge, Bridge).pdf',[8])]:
 d=fitz.open(p)
 for idx in pages:
  name=p.stem.replace(' ','-')+f'-page-{idx+1}.png';dest=out/name;d[idx].get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(dest)
  r['native_derivatives'].append({'path':str(dest),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'source':str(p),'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'pdf_page_one_based':idx+1,'method':'PyMuPDF get_pixmap 1.5 scale','visually_inspected':False})
p=run/'supplements/publisher-resources.html';s=p.read_text();matches=[]
for m in re.finditer(r'<a\b[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>',s,re.S):
 t=re.sub('<[^>]*>',' ',m.group(2));t=' '.join(t.split())
 if any(q in (t+' '+m.group(1)).lower() for q in ['john','errata','4poovyp','v1p712']):matches.append({'physicalLF':s[:m.start()].count('\n')+1,'text':t,'href':m.group(1)})
dest=out/'publisher-resource-links.json';dest.write_text(json.dumps(matches,indent=2));r['native_derivatives'].append({'path':str(dest),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'source':str(p),'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'method':'All matching HTML anchor href/text extracted with original physicalLF'})
(out/'source-read-record.json').write_text(json.dumps(r,indent=2));print('Rendered primary pages; publisher links:',len(matches))
