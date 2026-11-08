from pathlib import Path
import difflib
import hashlib
import json
import runpy

R=Path(__file__).parent;canonical=R.parents[4]/'rules/cosmic-encounter.md'
before=canonical.read_text();assert before==(R/'repair-freeze-06.md').read_text()
assert hashlib.sha256(before.encode()).hexdigest()=='c9fd69b1b94c010727a022c34e3c9ef4281d6ce58e35bdebb55e2d0af5f61bc0'
old='- Special: follow its conditions, defense and location.'
new='- Special: follow its conditions, defense and location. The original rulebook\'s illustrated special card chooses the other player with the most current foreign colonies, excluding offense. Break a tie toward offense\'s left, choosing the first tied eligible player there; encounter that player in their home system (rulebook p7).'
assert before.count(old)==1;after=before.replace(old,new)
notes=runpy.run_path(str(R/'assemble_repair.py'),run_name='metadata_only')['notes'];ref,body=notes['Gambler']
updated=(ref+'; FAQ p5',body+' The losing player chooses extra penalty ships under their control outside the encounter, ordinarily ships on their colonies in this original-base scope.')
oldnote=f'**{ref}:** {body}';newnote=f'**{updated[0]}:** {updated[1]}'
assert after.count(oldnote)==1;after=after.replace(oldnote,newnote)
assert not (R/'repair-freeze-07.md').exists()
(R/'repair-freeze-07.md').write_text(after)
(R/'repair-freeze-07.patch').write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='repair-freeze-06.md',tofile='repair-freeze-07.md')))
(R/'source-review/source-corrections-07.json').write_text(json.dumps({'before_sha256':hashlib.sha256(before.encode()).hexdigest(),'after_sha256':hashlib.sha256(after.encode()).hexdigest(),'special_card':{'old':old,'new':new,'primary':'Original rulebook p7 illustrated special, extraction603–612'},'gambler_note':{'old':oldnote,'new':newnote,'primary':'Original Gambler non-involved restriction plus FAQp5 extraction419–423/450–453'},'source_precision':'Ordinarily is non-exhaustive; no unsupported extra holding/location rule.','human_choices_adopted':False},indent=2,ensure_ascii=False)+'\n')
canonical.write_text(after)
core=R/'core-repair-draft.md';s=core.read_text();assert s.count(old)==1;core.write_text(s.replace(old,new))
assembly=R/'assemble_repair.py';s=assembly.read_text();marker='\ndef assemble():';assert s.count(marker)==1
assembly.write_text(s.replace(marker,'\n# Source-backed Gambler positive-holdings precision, corrections07.\nnotes[\'Gambler\']='+repr(updated)+'\n'+marker))
print('repair-freeze-07',len(after),hashlib.sha256(after.encode()).hexdigest())
