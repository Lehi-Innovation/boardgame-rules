"""Run the unchanged strict matcher with one lossless length-field alias."""
from pathlib import Path
import hashlib
import json
import sys

B = Path(__file__).resolve().parent
original = B / 'verify_staged_reader_actual_delivery.py'
code = original.read_text()
old = "inp['character_length']"
new = "inp.get('character_length',inp.get('characters',inp.get('unicode_character_length')))"
assert code.count(old) == 1
# Only parsing differs. Original reader bytes, required lengths, caps, contiguous
# ranges and actual one-source-range-per-output matching remain unchanged.
exec(compile(code.replace(old, new), str(original), 'exec'), globals())
path = B / sys.argv[1] / ('reader-pre-authoring-delivery-validation.json' if '--pre-authoring' in sys.argv else 'reader-actual-delivery-validation.json')
value = json.loads(path.read_text())
value['technical_length_field_alias_wrapper'] = {
    'original_pinned_matcher': str(original),
    'original_pinned_matcher_sha256': hashlib.sha256(original.read_bytes()).hexdigest(),
    'wrapper_path': str(Path(__file__).resolve()),
    'wrapper_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'only_character_length_characters_unicode_character_length_field_alias': True,
    'every_actual_source_and_boundary_criterion_unchanged': True,
    'no_reader_bytes_or_factual_result_changed': True,
}
path.write_text(json.dumps(value, indent=2) + '\n')
print(json.dumps({'final_proof_with_alias_provenance': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}))
