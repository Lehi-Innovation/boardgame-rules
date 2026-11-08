"""Clarify legal ship origins and integrate an FAQ limit into operative text."""
from pathlib import Path
import hashlib
import difflib
import json

R = Path(__file__).parent.resolve()
canonical = R.parents[4] / 'rules/cosmic-encounter.md'
before = canonical.read_text()
assert hashlib.sha256(canonical.read_bytes()).hexdigest() == '06ba4636268efbf5ea63841f6540e59981e82ae3ea84314d9d4c5569723d4af3'
changes = [
    ('moving up to four ships from other colonies there to reclaim it automatically.',
     'moving up to four of your ships from any of your other existing home or foreign colonies onto that empty home planet to reclaim it automatically.',
     'Original2008 rulebook p7 extraction549–553 and p8 extraction617–624: other colonies, including home and foreign origins.'),
    ("May free ANY player's ships from warp back to any colonies that player has as part of deal.",
     "As part of your deal, may free your negotiating opponent's ships from the warp, returning them to any existing colonies that opponent has.",
     'Official2018FAQ p22 extraction2088–2090 restricts liberation to the negotiating opponent; the existing FAQ paragraph already states that correction.'),
    ('Read these together with the shared power/colony rules above.',
     'General encounter, ship-return, hand-replacement, tie and timing rules still apply unless an individual effect explicitly changes them. Read each power together with those shared procedures above.',
     'Original rulebook general power/encounter system and p14 interaction procedure; shared rules remain applicable outside an expressly changed field.'),
]
after = before
for old, new, _ in changes:
    assert after.count(old) == 1
    after = after.replace(old, new)
core = R / 'core-repair-draft.md'
core_text = core.read_text()
for index in [0, 2]:
    old, new, _ = changes[index]
    assert core_text.count(old) == 1
    core_text = core_text.replace(old, new)
assembler = R / 'assemble_repair.py'
script = assembler.read_text()
anchor = "   s+='- '+x+'\\n'"
assert script.count(anchor) == 1
old, new, _ = changes[1]
script = script.replace(anchor, "   if a['alien']=='Zombie':\n    x=x.replace(" + repr(old) + ', ' + repr(new) + ')\n' + anchor)
for name in ['repair-freeze-13.md', 'repair-freeze-13.patch', 'source-review/source-corrections-13.json']:
    assert not (R / name).exists()
core.write_text(core_text)
assembler.write_text(script)
canonical.write_text(after)
(R / 'repair-freeze-13.md').write_text(after)
(R / 'repair-freeze-13.patch').write_text(''.join(difflib.unified_diff(
    before.splitlines(True), after.splitlines(True), fromfile='repair-freeze-12.md', tofile='repair-freeze-13.md')))
(R / 'source-review/source-corrections-13.json').write_text(json.dumps({
    'before_sha256': hashlib.sha256(before.encode()).hexdigest(),
    'after_sha256': hashlib.sha256(after.encode()).hexdigest(),
    'changes': [{'old': a, 'new': b, 'primary_source': c} for a, b, c in changes],
    'reason': 'Make source versus destination unambiguous; make the operative Zombie permission agree with its already-present FAQ correction; explicitly connect power entries to common procedures.',
    'source_catalog_or_native_assets_edited': False,
    'questions_or_key_changed': False,
    'human_choices_adopted': False,
    'prior_raw_outputs_and_grades_preserved': True,
}, indent=2, ensure_ascii=False) + '\n')
print('freeze13', hashlib.sha256(after.encode()).hexdigest(), len(after))
