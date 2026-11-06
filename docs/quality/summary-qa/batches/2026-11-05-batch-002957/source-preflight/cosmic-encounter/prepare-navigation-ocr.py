"""Create navigation-only OCR; unchanged original images remain the authority."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess

base = Path(__file__).resolve().parent
source = json.loads((base / 'original-alien-sheet-provenance.json').read_text())
assert source['all_50_exact_archival_hashes']
output = base / 'navigational-ocr'
output.mkdir(exist_ok=False)
version = subprocess.run(['tesseract', '--version'], check=True, capture_output=True, text=True).stdout.splitlines()[0]

def extract(asset):
    path = Path(asset['original_file'])
    assert path.parent == base / 'alien-sheets-original'
    before = hashlib.sha256(path.read_bytes()).hexdigest()
    assert before == asset['original_sha256']
    result = subprocess.run(['tesseract', str(path), 'stdout', '-l', 'eng', '--psm', '11'], check=True, capture_output=True, text=True)
    text_path = output / (path.stem + '.txt')
    text_path.write_text(result.stdout)
    assert hashlib.sha256(path.read_bytes()).hexdigest() == before
    return {'alien': asset['alien'], 'original_image': str(path), 'source_sha256': before,
            'ocr_path': str(text_path), 'ocr_sha256': hashlib.sha256(text_path.read_bytes()).hexdigest(),
            'characters': len(result.stdout)}

with ThreadPoolExecutor(max_workers=4) as pool:
    entries = list(pool.map(extract, source['assets']))
combined = ''.join('\n\n## ' + e['alien'] + '\nSOURCE IMAGE: ' + e['original_image'] + '\n\n' + Path(e['ocr_path']).read_text() for e in entries)
(output / 'all-fifty-navigation.txt').write_text(combined)
manifest = {'created_at_utc': datetime.now(timezone.utc).isoformat(), 'method': version + ' eng --psm 11, unmodified original image input',
            'status': 'NAVIGATION_ONLY', 'warning': 'OCR may misread numbers, restrictions, names or graphical timing bars. Visually inspect all fifty original images. OCR does not replace source authority or native inspection.',
            'all_original_images_unchanged': True, 'entries': entries}
(output / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(json.dumps({'images': len(entries), 'navigation_characters': len(combined), 'all_original_images_unchanged': True, 'authority': 'Original images only; OCR navigation requires visual verification.'}))
