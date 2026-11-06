from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import requests,fitz,json,bs4,hashlib
base=Path(__file__).parent;root=base.parents[4]
items=[('oath-law-of-oath','https://www.brdgmz.nl/wp-content/uploads/Spelregels-Oath-English.pdf'),('new-angeles-rules','https://images-cdn.fantasyflightgames.com/filer_public/94/01/9401560d-7476-4020-888f-acb0ffe58499/ad03_rules_reference_2compressed.pdf?download=1'),('new-angeles-learn-to-play','https://images-cdn.fantasyflightgames.com/filer_public/ae/bb/aebb1411-1b59-4bb2-a5c3-142e313a972b/ad03_rulebookcompressed.pdf?download=1')]
def f(item):
 name,url=item
 try:
  r=requests.get(url,timeout=40);r.raise_for_status();assert r.content.startswith(b'%PDF'),r.headers.get('content-type');pdf=root/'source_pdfs'/(name+'.pdf');assert not pdf.exists();pdf.write_bytes(r.content);d=fitz.open(pdf);t='\n\n'.join(f'--- Page {i+1} ---\n'+p.get_text() for i,p in enumerate(d))+'\n';p=root/'extracted'/(name+'.txt');assert not p.exists();p.write_text(t);return {'name':name,'url':url,'pdf_path':str(pdf),'text_path':str(p),'pages':len(d),'sha256':hashlib.sha256(r.content).hexdigest(),'text_sha256':hashlib.sha256(t.encode()).hexdigest(),'head':t[:500],'tail':t[-250:]}
 except Exception as e:return {'name':name,'url':url,'error':str(e)}
rs=list(ThreadPoolExecutor(max_workers=3).map(f,items));(base/'supplemental-downloads.json').write_text(json.dumps(rs,indent=2)+'\n')
for r in rs:print(json.dumps(r))
for name,u in [('buriedgiant-oath','https://buriedgiant.com/oath/'),('leder-rules','https://rules.ledergames.com/?product=oath&locale=en-US&printing=p1')]:
 try:
  r=requests.get(u,timeout=25);(base/'publisher-pages'/(name+'.html')).write_text(r.text);s=bs4.BeautifulSoup(r.text,'html.parser');print(name,'scripts',[requests.compat.urljoin(r.url,a['src']) for a in s.select('script[src]')])
 except Exception as e:print(name,str(e))
