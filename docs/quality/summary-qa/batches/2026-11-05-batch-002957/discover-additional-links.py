from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import requests,bs4,json
base=Path(__file__).parent
urls=['https://wizkids.com/sidereal-confluence/','https://buriedgiant.com/oath/','https://rules.ledergames.com/?product=oath&locale=en-US&printing=p1','https://wehrlegig.com/pages/resources']
def f(u):
 try:
  r=requests.get(u,timeout=30);s=bs4.BeautifulSoup(r.text,'html.parser');ls=[{'text':a.get_text(' ',strip=True)[:100],'url':requests.compat.urljoin(r.url,a['href'])} for a in s.select('a[href]') if any(w in (a['href']+' '+a.get_text()).lower() for w in ['.pdf','errata','john company','oath'])];return {'url':u,'status':r.status_code,'links':ls}
 except Exception as e:return {'url':u,'error':str(e)}
r=list(ThreadPoolExecutor(max_workers=4).map(f,urls));(base/'additional-publisher-links.json').write_text(json.dumps(r,indent=2));
for x in r:print(json.dumps(x))
