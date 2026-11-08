"""Restore the retained printed Mind Wild choice for each later draw."""
from pathlib import Path
import difflib
import hashlib
import json

R = Path(__file__).parent.resolve()
WORK = R.parents[4]
canonical = WORK / 'rules/cosmic-encounter.md'
old = 'For the rest of this encounter, draw each card that same player must draw, inspect it and give it to them; do not share that information.'
new = 'For the rest of this encounter, each time that same player must draw a card, you may draw it instead, inspect it and give it to them; choose separately for each draw and do not share that information.'
before = canonical.read_text()
assert hashlib.sha256(canonical.read_bytes()).hexdigest() == '14cb67cfc93eca486cc449dd933cd8cd5bb710dc8fc018e2255b3dc70b149a02'
assert before.count(old) == 1
for name in ['repair-freeze-11.md', 'repair-freeze-11.patch', 'source-review/source-corrections-11.json']:
    assert not (R / name).exists()
after = before.replace(old, new)
authoring = R / 'assemble_repair.py'
authoring_text = authoring.read_text()
assert authoring_text.count(old) == 1
authoring.write_text(authoring_text.replace(old, new))
canonical.write_text(after)
(R / 'repair-freeze-11.md').write_text(after)
(R / 'repair-freeze-11.patch').write_text(''.join(difflib.unified_diff(
    before.splitlines(True), after.splitlines(True), fromfile='repair-freeze-10.md', tofile='repair-freeze-11.md')))
(R / 'source-review/source-corrections-11.json').write_text(json.dumps({
    'before_sha256': hashlib.sha256(before.encode()).hexdigest(),
    'after_sha256': hashlib.sha256(after.encode()).hexdigest(),
    'old': old, 'new': new,
    'primary_source': 'Retained official May6 2009FAQ p1 Mind Flare erratum, cached L43–L49.',
    'reason': 'The corrected text says each time the targeted player must draw, you may draw it instead. Preserve that separate option rather than implying compulsory interception.',
    'independent_source_audit_finding': 'source-only-audit-15.json/A15-01',
    'coverage_action': 'Explicit per-draw optionality will be added to the existing Mind Wild question before any expanded test.',
    'human_choices_adopted': False,
}, indent=2, ensure_ascii=False) + '\n')
print('freeze11', hashlib.sha256(after.encode()).hexdigest(), len(after))
