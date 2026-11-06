from concurrent.futures import ThreadPoolExecutor
import requests,bs4,json,pathlib
urls=['https://wehrlegig.com/products/john-company-second-edition','https://ledergames.com/pages/resources','https://www.rprod.com/en/games/so-clover','https://shop.greaterthangames.com/products/spirit-island','https://restorationgames.com/unmatched/','https://wizkids.com/sidereal-confluence-trading-and-negotiation-in-the-elysian-quadrant/','https://www.fantasyflightgames.com/en/products/new-angeles/','https://www.lonesharkgames.com/lords-of-vegas/']
base=pathlib.Path(__file__).parent/'publisher-pages';base.mkdir(exist_ok=True)
def fetch(u):
 try:
  r=requests.get(u,timeout=40);s=bs4.BeautifulSoup(r.text,'html.parser');links=[]
  for a in s.select('a[href]'):
   h=a['href'];t=a.get_text(' ',strip=True)
   if any(x in (h+' '+t).lower() for x in ['.pdf','rule','errata','clover','oath','sidereal']):links.append({'text':t[:100],'url':requests.compat.urljoin(r.url,h)})
  d={'url':u,'final_url':r.url,'status':r.status_code,'links':links};(base/(u.split('/')[2]+'.html')).write_text(r.text);return d
 except Exception as e:return {'url':u,'error':str(e)}
results=list(ThreadPoolExecutor(max_workers=8).map(fetch,urls));(base/'links.json').write_text(json.dumps(results,indent=2));
for d in results:
 print(json.dumps(d))
