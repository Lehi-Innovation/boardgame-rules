from pathlib import Path
import difflib
import hashlib
import json
import runpy

R=Path(__file__).parent;canonical=R.parents[4]/'rules/cosmic-encounter.md'
before=canonical.read_text();assert before==(R/'repair-freeze-07.md').read_text()
assert hashlib.sha256(before.encode()).hexdigest()=='bc13eeaef3bce5559f63daf43a5d695783a801190c12bc5e39110d7a17c2c642'
intro='The FAQ quotes these Super effect timing clauses; they do not make a flare apply automatically in later encounters. Follow the full card for its other conditions and legal play.\n\n| Original Super flare | Quoted effect timing |\n|---|---|\n| Kamikaze, Machine, Masochist | During each of **your own Regroup phases** |\n| Miser | At the start of each of **your encounters** |\n| Cudgel | Whenever you **use your power** |\n\nThese are effect timing clauses, not a reconstruction of an earlier permitted faceup-placement window (FAQ pp12,16–18).\n\n'
marker='## Scoring / Victory Conditions';assert before.count(marker)==1;after=before.replace(marker,intro+marker)
notes=runpy.run_path(str(R/'assemble_repair.py'),run_name='metadata_only')['notes'];ref,body=notes['Fido']
updated=(ref+'; FAQ p4',body+' For the Fido flare effect described by the FAQ, the forced discard-pile draw takes its top card.')
oldnote=f'**{ref}:** {body}';newnote=f'**{updated[0]}:** {updated[1]}'
assert after.count(oldnote)==1;after=after.replace(oldnote,newnote)
assert not (R/'repair-freeze-08.md').exists()
(R/'repair-freeze-08.md').write_text(after)
(R/'repair-freeze-08.patch').write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='repair-freeze-07.md',tofile='repair-freeze-08.md')))
(R/'source-review/source-corrections-08.json').write_text(json.dumps({'before_sha256':hashlib.sha256(before.encode()).hexdigest(),'after_sha256':hashlib.sha256(after.encode()).hexdigest(),'quoted_Super_effect_timing':intro,'Fido_note':{'old':oldnote,'new':newnote},'primary_sources':['2018 FAQ p16 1470–1473/1551–1554; p17 1581–1584; p18 1653–1656; p12 1125–1127','2018 FAQ p4 280–287 Fido flare described without side identification'],'source_limits':'No missing full flare effect, role, trigger, target, quota or first-play window is inferred.','human_choices_adopted':False},indent=2,ensure_ascii=False)+'\n')
canonical.write_text(after)
core=R/'core-repair-draft.md';s=core.read_text();assert s.count(marker)==1;core.write_text(s.replace(marker,intro+marker))
assembly=R/'assemble_repair.py';s=assembly.read_text();amarker='\ndef assemble():';assert s.count(amarker)==1
assembly.write_text(s.replace(amarker,'\n# Source-described Fido flare acquisition, corrections08.\nnotes[\'Fido\']='+repr(updated)+'\n'+amarker))
print('repair-freeze-08',len(after),hashlib.sha256(after.encode()).hexdigest())
