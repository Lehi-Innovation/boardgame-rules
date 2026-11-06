"""Decode this public Tabletop Simulator BSON document; preserve its raw bytes."""
from pathlib import Path
import json
import struct

base = Path(__file__).parent
raw = base / 'official-workshop.bson'
if not raw.exists():
    (base / 'official-workshop.json').rename(raw)
data = raw.read_bytes()

def document(start):
    size = struct.unpack_from('<i', data, start)[0]
    end = start + size
    assert size >= 5 and data[end-1] == 0
    pos = start + 4
    out = {}
    while pos < end-1:
        typ = data[pos]
        pos += 1
        stop = data.index(b'\0', pos)
        key = data[pos:stop].decode('utf-8')
        pos = stop + 1
        if typ in (3, 4):
            value, pos = document(pos)
            if typ == 4:
                assert list(value) == [str(i) for i in range(len(value))]
                value = list(value.values())
        elif typ == 2:
            n = struct.unpack_from('<i', data, pos)[0]
            assert n > 0 and data[pos+4+n-1] == 0
            value = data[pos+4:pos+4+n-1].decode('utf-8')
            pos += 4+n
        elif typ in (1, 16, 18, 9):
            fmt = {1: '<d', 16: '<i', 18: '<q', 9: '<q'}[typ]
            value = struct.unpack_from(fmt, data, pos)[0]
            pos += struct.calcsize(fmt)
        elif typ == 8:
            assert data[pos] in (0, 1)
            value = bool(data[pos])
            pos += 1
        elif typ == 10:
            value = None
        else:
            raise ValueError(('unsupported BSON type', typ, key, pos))
        assert key not in out
        out[key] = value
    assert pos == end-1
    return out, end

decoded, end = document(0)
assert end == len(data)
(base / 'official-workshop.json').write_text(json.dumps(decoded, indent=2, ensure_ascii=False) + '\n')

def walk(value):
    if isinstance(value, dict):
        nickname = value.get('Nickname', '')
        if any(hero in nickname.lower() for hero in ['arthur', 'alice', 'sinbad', 'medusa']):
            print(json.dumps({k: value.get(k) for k in ['Name', 'Nickname', 'Description', 'CardID', 'CustomImage', 'CustomDeck']}, ensure_ascii=False)[:1500])
        for child in value.values():
            walk(child)
    elif isinstance(value, list):
        for child in value:
            walk(child)

print('Decoded bytes:', len(data), 'SaveName:', decoded.get('SaveName'))
walk(decoded)
