from pathlib import Path
import json,hashlib
from PIL import Image
import fitz
O=Path('docs/quality/summary-qa/new-angeles/2026-11-05-batch-002957/coverage-fresh-final-94');D=Path('docs/quality/summary-qa/batches/2026-11-05-batch-002957/source-preflight/new-angeles')
M=[]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def strip(name,grid,indices,out):
 p=D/name; im=Image.open(p);w=im.width//grid[0];h=im.height//grid[1];canvas=Image.new('RGB',(w*len(indices),h));rects=[]
 for j,i in enumerate(indices):
  x=(i%grid[0])*w;y=(i//grid[0])*h;r=[x,y,x+w,y+h];canvas.paste(im.crop(r),(j*w,0));rects.append({'cell_zero_based':i,'rect':r,'output_rect':[j*w,0,(j+1)*w,h]})
 q=O/(out+'.png');canvas.save(q);M.append({'id':out,'source':str(p.resolve()),'source_sha256':sha(p),'source_dimensions':list(im.size),'rectangles':rects,'output':str(q.resolve()),'output_dimensions':list(canvas.size),'output_sha256':sha(q),'transform':'lossless decoded native pixels, no scaling; cells concatenated horizontally'})
for side in ['face','back']:
 for i in range(6):strip('corporation-sheets-'+side+'.jpg',(4,2),[i],f'corp-{side}-{i}')
for side in ['face','back']:
 for i in [0,3]:strip('emergency-cards-'+side+'.png',(4,2),list(range(i,i+3)),f'emergency-{side}-{i}')
for deck in [1,2,5,6,7]:strip(f'action-deck-{deck}-face.png',(7,3),[0,5,10,15],f'action-{deck}-four-unique')
for i in range(0,34,3):strip('asset-cards-face.jpg',(6,6),list(range(i,min(i+3,34))),f'assets-{i:02}')
for i in range(0,12,4):strip('investment-cards-face.jpg',(7,2),list(range(i,min(i+4,12))),f'investments-{i:02}')
for side in ['face','back']:
 for i in range(0,16,3):strip(f'event-cards-{side}.jpg',(10,2),list(range(i,min(i+3,16))),f'events-{side}-{i:02}')
for role,n,g in [('setup',6,(4,2)),('demand',9,(5,2)),('rival',7,(4,2))]:
 ext='png' if role=='demand' else 'jpg'
 for i in range(0,n,3):strip(f'{role}-cards-face.{ext}',g,list(range(i,min(i+3,n))),f'{role}-{i:02}')
for pdf,pages in [('rules',[3,11,16]),('learn-to-play',[3,7,8,9,11,13,14,15])]:
 p=Path(f'source_pdfs/new-angeles-{pdf}.pdf');doc=fitz.open(p)
 for pg in pages:
  page=doc[pg-1];q=O/f'pdf-{pdf}-{pg}.png';pix=page.get_pixmap(matrix=fitz.Matrix(2,2));pix.save(q);M.append({'id':q.stem,'source':str(p.resolve()),'source_sha256':sha(p),'page_one_based':pg,'page_rect':list(page.rect),'scale':2,'output':str(q.resolve()),'output_dimensions':[pix.width,pix.height],'output_sha256':sha(q)})
(O/'native-manifest.json').write_text(json.dumps(M,indent=2));print('Created',len(M),'native views with full lineage')
