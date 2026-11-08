"""Preserve both empty-answer readiness outputs before the actual-delivery checkpoint."""
from pathlib import Path
import hashlib
import json
import re
import shutil
import sys

B=Path(__file__).resolve().parent
ROOT=B.parents[4]
D=(B/sys.argv[1]).resolve()
assert D.parent==B and re.fullmatch(r'expanded-iteration-\d{2}',D.name)
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def source_path(raw):
    p=Path(raw)
    return p.resolve() if p.is_absolute() else (ROOT/p).resolve()
prepared=[]
for letter in 'ab':
    source=D/f'reader-{letter}.json'
    data=json.loads(source.read_text())
    assert data['stage']=='delivery_ready' and data['answers']==[]
    assert isinstance(data['reader'],str) and data['reader']
    allowed={(D/'summary-snapshot.md').resolve(),(D/'questions.json').resolve()}
    assert len(data['inputs_read'])==2
    assert {source_path(x['path']) for x in data['inputs_read']}==allowed
    for item in data['inputs_read']:
        p=source_path(item['path']);text=p.read_text()
        assert H(p)==item['sha256'] and len(text)==item.get('character_length',item.get('characters',item.get('unicode_character_length'))) and item['output_cap_tokens']>=4000
        position=0
        for start,end in item['read_ranges']:
            assert start==position and 0<end-start<=6000
            position=end
        assert position==len(text)
    destination=D/f'reader-{letter}-delivery-ready.json'
    freeze=D/f'reader-{letter}-delivery-ready-freeze.json'
    assert not destination.exists() and not freeze.exists()
    prepared.append((source,destination,freeze))
# No copies are made until both complete declarations pass the mechanical checks.
for source,destination,freeze in prepared:
    shutil.copyfile(source,destination)
    assert destination.read_bytes()==source.read_bytes()
    receipt={'path':str(destination),'sha256':H(destination),'characters':len(destination.read_text()),'copied_from_original_working_output':str(source),'stage':'delivery_ready','written_answer_count':0,'completed_reader_trial':False,'actual_public_delivery_verification_still_required':True,'no_private_cognition_claim':True}
    freeze.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt))
