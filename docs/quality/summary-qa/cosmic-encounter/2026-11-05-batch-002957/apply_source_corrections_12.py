"""Keep Mind Wild's later-event deck restriction explicit."""
from pathlib import Path
import difflib
import hashlib
import json

R = Path(__file__).parent.resolve()
canonical = R.parents[4] / 'rules/cosmic-encounter.md'
before = canonical.read_text()
assert hashlib.sha256(canonical.read_bytes()).hexdigest() == '9ac061be94b0b0dfc173741e3f0f3eb6582f8845599e9c77477979387049ba12'
old = 'For the rest of this encounter, each time that same player must draw a card, you may draw it instead'
new = 'For the rest of this encounter, each time that same player must draw a card from the cosmic deck, you may draw it instead'
assert before.count(old) == 1
authoring = R / 'assemble_repair.py'
authoring_text = authoring.read_text()
assert authoring_text.count(old) == 1
for name in ['repair-freeze-12.md', 'repair-freeze-12.patch', 'source-review/source-corrections-12.json']:
    assert not (R / name).exists()
after = before.replace(old, new)
authoring.write_text(authoring_text.replace(old, new))
canonical.write_text(after)
(R / 'repair-freeze-12.md').write_text(after)
(R / 'repair-freeze-12.patch').write_text(''.join(difflib.unified_diff(
    before.splitlines(True), after.splitlines(True), fromfile='repair-freeze-11.md', tofile='repair-freeze-12.md')))
(R / 'source-review/source-corrections-12.json').write_text(json.dumps({
    'before_sha256': hashlib.sha256(before.encode()).hexdigest(),
    'after_sha256': hashlib.sha256(after.encode()).hexdigest(),
    'old': old, 'new': new,
    'primary_source': 'Retained official May6 2009 FAQ Mind Flare erratum L46–L48: each time that player must draw a card from the deck, you may draw it instead.',
    'reason': 'Repeat the deck-origin restriction for later events instead of relying on the initial cosmic-deck trigger to qualify all later draws. Base scope has no reward deck or optional Technology.',
    'not_asserted': 'No permission to intercept cards acquired from a hand or discard pile, and no reconstruction of absent flare fields.',
    'question_action': 'Existing Q148 asks which later draws; its next explicit key will preserve origin and per-event optionality.',
    'human_choices_adopted': False,
    'prior_exact11_audit_result_preserved': True,
}, indent=2, ensure_ascii=False) + '\n')
print('freeze12', hashlib.sha256(after.encode()).hexdigest(), len(after))
