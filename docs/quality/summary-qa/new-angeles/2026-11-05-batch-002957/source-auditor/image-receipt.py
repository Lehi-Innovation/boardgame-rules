import sys,io,json,base64,hashlib,datetime
from pathlib import Path
from PIL import Image
out=Path(__file__).parent
for line in sys.stdin:
 try:
  d=json.loads(line); raw=base64.b64decode(d['url'].split(',',1)[1]); im=Image.open(io.BytesIO(raw)).convert('RGB'); source=Image.open(d['path']).convert('RGB')
  r={'path':d['path'],'detail_requested':'original','detail_forwarded':'original','timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'runtime_image_block_bytes_sha256':hashlib.sha256(raw).hexdigest(),'runtime_decoded_dimensions':list(im.size),'runtime_decoded_rgb_sha256':hashlib.sha256(im.tobytes()).hexdigest(),'source_dimensions':list(source.size),'source_decoded_rgb_sha256':hashlib.sha256(source.tobytes()).hexdigest(),'pixel_equal_to_native_source':im.size==source.size and im.tobytes()==source.tobytes(),'purpose':d.get('purpose','native semantic source inspection')}
  with (out/'image-delivery-receipts.jsonl').open('a') as f:f.write(json.dumps(r)+'\n')
  print(json.dumps(r),flush=True)
 except Exception as e:print(str(e),flush=True)
