from pathlib import Path
from PIL import Image
import json,hashlib
out=Path(__file__).parent; src=Path('docs/quality/summary-qa/batches/2026-11-05-batch-002957/source-preflight/new-angeles')
prov=json.loads((src/'printed-component-provenance.json').read_text()); records=[]
for asset in prov['assets']:
 role=asset['role'];side=asset['side'];p=Path(asset['path']);im=Image.open(p).convert('RGB');w,h=im.size;cols,rows=asset['grid']
 if role=='emergency-cards' and side=='back':continue
 if role=='event-cards' and side=='back':continue
 if role in ['setup-cards','rival-cards','demand-cards']:continue
 if role=='corporation-sheets': groups=[[i] for i in range(6)]
 elif role=='emergency-cards':groups=[list(range(3)),list(range(3,6))]
 elif role.startswith('action-deck'):groups=[list(range(0,7)),list(range(7,14)),list(range(14,20))]
 elif role=='asset-cards':groups=[list(range(i,min(i+6,34))) for i in range(0,34,6)]
 elif role=='investment-cards':groups=[list(range(0,7)),list(range(7,12))]
 elif role=='event-cards':groups=[list(range(i,min(i+4,16))) for i in range(0,16,4)]
 for j,ids in enumerate(groups):
  # Bounding native rectangle, including intervening cells when rows cross.
  boxes=[(i%cols*w//cols,i//cols*h//rows,(i%cols+1)*w//cols,(i//cols+1)*h//rows) for i in ids]
  box=(min(b[0] for b in boxes),min(b[1] for b in boxes),max(b[2] for b in boxes),max(b[3] for b in boxes))
  crop=im.crop(box); dest=out/f'{role}-{side}-{j:02d}.png';crop.save(dest)
  records.append({'path':str(dest.resolve()),'parent':str(p.resolve()),'parent_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'parent_dimensions':[w,h],'parent_rgb_sha256':hashlib.sha256(im.tobytes()).hexdigest(),'rectangle':list(box),'cells':ids,'grid':[cols,rows],'dimensions':list(crop.size),'rgb_sha256':hashlib.sha256(crop.tobytes()).hexdigest(),'file_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'pixel_equality_verified':Image.open(dest).convert('RGB').tobytes()==im.crop(box).tobytes()})
(out/'native-crop-manifest.json').write_text(json.dumps(records,indent=2))
print(len(records));print('\n'.join(f'{i}: {Path(r["path"]).name} {r["dimensions"]}' for i,r in enumerate(records)))
