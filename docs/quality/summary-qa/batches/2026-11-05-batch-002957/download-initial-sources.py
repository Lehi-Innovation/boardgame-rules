from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import requests,fitz,hashlib,json,datetime
from zoneinfo import ZoneInfo
base=Path(__file__).parent;root=base.parents[4]
items=[
('oath-chronicles-of-empire-and-exile','https://cdn.shopify.com/s/files/1/0106/0162/7706/files/Oath_Law_of_Oath_web_Oct_20_2020.pdf','oath-law-of-oath.pdf'),
('sidereal-confluence','https://eadn-wc03-13179282.nxedge.io/posters/repository/wizkids/SC_Rule%20Book_061017_Web5.pdf','sidereal-confluence-rules.pdf'),
('so-clover','https://cdn.svc.asmodee.net/production-rprod/storage/downloads/games/so-clover/sc-en01-rules-16197761427wP8d.pdf','so-clover-rules.pdf'),
('john-company-second-edition','https://www.dropbox.com/scl/fi/v1p712l0dkgiqa0jx0vr8/John-Company-Rules.pdf?rlkey=xtek9x06fla1cb5d8b8ov3q7b&dl=1','john-company-second-edition-rules.pdf'),
('spirit-island','https://www.dropbox.com/scl/fi/5wzghwnbsi39msyy6vvox/Spirit-Island-CORE-Rulebook.pdf?rlkey=86i7aofqbzhulezjr7z0ssyff&dl=1','spirit-island-rules.pdf'),
('unmatched','https://iellogames.com/wp-content/uploads/2021/02/Unmatched-BoL-1_Rulebook_EN_Light.pdf','unmatched-rules.pdf'),
('lords-of-vegas','https://lonesharkgames.com/wp-content/uploads/2024/08/Lords-of-Vegas-Mayfair-Base-Game-Rulebook.pdf','lords-of-vegas-rules.pdf'),
('cosmic-encounter','https://images-cdn.fantasyflightgames.com/ffg_content/Cosmic%20Encounter/cosmic-encounter-rulebook.pdf','cosmic-encounter-2008-rules.pdf'),
('new-angeles','https://images-cdn.fantasyflightgames.com/filer_public/94/01/9401560d-7476-4020-888f-acb0ffe58499/ad03_rules_reference_2compressed.pdf','new-angeles-rules.pdf'),
('new-angeles','https://images-cdn.fantasyflightgames.com/filer_public/ae/bb/aebb1411-1b59-4bb2-a5c3-142e313a972b/ad03_rulebookcompressed.pdf','new-angeles-learn-to-play.pdf')]
def fetch(item):
 slug,url,filename=item
 try:
  r=requests.get(url,timeout=45);r.raise_for_status();assert r.content.startswith(b'%PDF'),r.headers.get('Content-Type')
  path=root/'source_pdfs'/filename;assert not path.exists(),str(path)+' exists';path.write_bytes(r.content);doc=fitz.open(path)
  text='\n\n'.join(f'--- Page {i+1} ---\n'+p.get_text() for i,p in enumerate(doc))+'\n'
  outname=filename.removesuffix('.pdf')+'.txt';textpath=root/'extracted'/outname
  if textpath.exists():
   (base/'initial-shared-files'/'extracted').mkdir(exist_ok=True);(base/'initial-shared-files'/'extracted'/outname).write_bytes(textpath.read_bytes())
  assert not textpath.exists() or slug=='cosmic-encounter',str(textpath)+' exists';textpath.write_text(text)
  return {'slug':slug,'url':url,'final_url':r.url,'pdf_path':str(path),'text_path':str(textpath),'pages':len(doc),'bytes':len(r.content),'sha256':hashlib.sha256(r.content).hexdigest(),'text_sha256':hashlib.sha256(text.encode()).hexdigest(),'text_characters':len(text),'downloaded_at':datetime.datetime.now(ZoneInfo('America/Phoenix')).isoformat(),'first_text':text[:450]}
 except Exception as e:return {'slug':slug,'url':url,'error':str(e)}
results=list(ThreadPoolExecutor(max_workers=8).map(fetch,items));(base/'source-downloads.json').write_text(json.dumps(results,indent=2)+'\n')
for d in results:print(json.dumps(d))
