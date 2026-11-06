from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import requests,fitz,json,hashlib,urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
base=Path(__file__).parent;root=base.parents[4]
items=[('oath-current-law','https://buriedgiant.com/oath/Oath_Law_of_Oath.pdf',True),('oath-current-playbook','https://buriedgiant.com/oath/Oath_Playbook.pdf',True),('new-angeles-rules','https://www.bgames.com.ua/rules/new_angeles_reference.pdf',False),('new-angeles-learn-to-play','https://www.bgames.com.ua/rules/new_angeles.pdf',False),('new-angeles-faq','https://images.fantasyflightgames.com/filer_public/a3/31/a3315446-bfb9-4259-890a-33e50e4db270/new_angeles_faq.pdf',True)]
def fetch(it):
 name,url,verify=it
 try:
  r=requests.get(url,timeout=35,verify=verify);r.raise_for_status();assert r.content.startswith(b'%PDF'),r.headers.get('Content-Type');p=root/'source_pdfs'/(name+'.pdf');assert not p.exists();p.write_bytes(r.content);d=fitz.open(p);t='\n\n'.join(f'--- Page {i+1} ---\n'+p.get_text() for i,p in enumerate(d))+'\n';tp=root/'extracted'/(name+'.txt');assert not tp.exists();tp.write_text(t)
  return {'name':name,'url':url,'pdf_path':str(p),'text_path':str(tp),'pages':len(d),'sha256':hashlib.sha256(r.content).hexdigest(),'text_sha256':hashlib.sha256(t.encode()).hexdigest(),'tls_verified':verify,'head':t[:500],'tail':t[-250:]}
 except Exception as e:return {'name':name,'url':url,'error':str(e)}
rs=list(ThreadPoolExecutor(max_workers=5).map(fetch,items));(base/'oath-new-angeles-downloads.json').write_text(json.dumps(rs,indent=2)+'\n')
for r in rs:print(json.dumps(r),flush=True)
