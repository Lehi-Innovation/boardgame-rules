from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import requests, fitz, json, re, hashlib

base = Path(__file__).parent
root = base.parents[4]
items = [
    ('new-angeles-rules', 'https://www.bgames.com.ua/rules/new_angeles_reference.pdf'),
    ('new-angeles-learn-to-play', 'https://fgbradleys.com/wp-content/uploads/rules/Android%20New%20Angeles%20-%20rules.pdf'),
    ('new-angeles-faq', 'https://images-cdn.fantasyflightgames.com/filer_public/a3/31/a3315446-bfb9-4259-890a-33e50e4db270/new_angeles_faq.pdf'),
    ('cosmic-encounter-faq', 'https://images-cdn.fantasyflightgames.com/filer_public/bd/b6/bdb66dce-f409-4877-8433-184373370281/faq_2018-web.pdf'),
]

def fetch(item):
    name, url = item
    try:
        response = requests.get(url, timeout=40)
        response.raise_for_status()
        assert response.content.startswith(b'%PDF'), response.headers.get('content-type')
        pdf = root / 'source_pdfs' / (name + '.pdf')
        assert not pdf.exists(), str(pdf) + ' exists'
        pdf.write_bytes(response.content)
        document = fitz.open(pdf)
        content = '\n\n'.join(f'--- Page {i+1} ---\n' + page.get_text() for i, page in enumerate(document)) + '\n'
        extraction = root / 'extracted' / (name + '.txt')
        assert not extraction.exists()
        extraction.write_text(content)
        return {'name': name, 'url': url, 'pdf_path': str(pdf), 'text_path': str(extraction), 'pages': len(document), 'sha256': hashlib.sha256(response.content).hexdigest(), 'text_sha256': hashlib.sha256(content.encode()).hexdigest(), 'head': content[:400], 'tail': content[-200:]}
    except Exception as error:
        return {'name': name, 'url': url, 'error': str(error)}

results = list(ThreadPoolExecutor(max_workers=4).map(fetch, items))
(base / 'remaining-downloads.json').write_text(json.dumps(results, indent=2) + '\n')
for result in results:
    print(json.dumps(result), flush=True)

try:
    response = requests.get('https://buriedgiant.com/assets/index-Ba4kKz5x.js', timeout=30)
    response.raise_for_status()
    (base / 'publisher-pages' / 'buriedgiant-main.js').write_text(response.text)
    urls = re.findall(r'https?[^\s<>"\x27]+', response.text)
    print('Oath resource URLs', [url[:500] for url in urls if any(word in url.lower() for word in ['oath', 'errata'])])
    for match in list(re.finditer('Law of Oath', response.text))[:5]:
        print('LAW DATA', response.text[max(0, match.start()-300):match.start()+600])
except Exception as error:
    print(str(error))
