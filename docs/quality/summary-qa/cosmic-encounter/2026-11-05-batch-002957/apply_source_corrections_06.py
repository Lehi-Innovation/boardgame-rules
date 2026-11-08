from pathlib import Path
import difflib
import hashlib
import json
import runpy

R=Path(__file__).parent;canonical=R.parents[4]/'rules/cosmic-encounter.md'
before=canonical.read_text();assert before==(R/'repair-freeze-05.md').read_text()
assert hashlib.sha256(before.encode()).hexdigest()=='7505bd4cb6bea19cb70cbf66b966815441824fbc53cc41959942b8f1376dad22'
notes=runpy.run_path(str(R/'assemble_repair.py'),run_name='assembly_metadata_only')['notes']
updates={
 'Mite':('FAQ p8','When Mite Super\'s quoted pickup instruction applies, it allows taking any cards the opponent discards, not only encounter cards.'),
 'Loser':('FAQ p16','Loser Wild is played before encounter cards are selected.'),
 'Oracle':(notes['Oracle'][0]+'; FAQ p6',notes['Oracle'][1]+' In the official Oracle Wild example, play the flare faceup in front of you outside the hands, mix the hands together, take your new hand at random from the mixed cards, then return the flare to hand when its effect finishes.'),
 'Filch':(notes['Filch'][0],notes['Filch'][1].replace('Its printed Wild permits','Its printed Wild, as any player in any phase, permits')),
}
after=before
for alien,(refs,body) in updates.items():
    if alien in notes:
        old=f'**{notes[alien][0]}:** {notes[alien][1]}'
        new=f'**{refs}:** {body}'
        assert after.count(old)==1,alien
        after=after.replace(old,new)
    else:
        start=after.index('#### '+alien+'\n');end=after.find('\n#### ',start+5)
        assert end!=-1
        section=after[start:end].rstrip()+f'\n\n**{refs}:** {body}\n'
        after=after[:start]+section+after[end:]
old='**Cosmic Zap** cancels a power use, including your own, and prevents further uses for that encounter.'
new='**Any player, including an uninvolved bystander, may play Cosmic Zap** on an otherwise legal power use. It cancels that use, including your own, and prevents further uses for that encounter.'
assert after.count(old)==1;after=after.replace(old,new)
assert not (R/'repair-freeze-06.md').exists()
(R/'repair-freeze-06.md').write_text(after)
(R/'repair-freeze-06.patch').write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='repair-freeze-05.md',tofile='repair-freeze-06.md')))
(R/'source-review/source-corrections-06.json').write_text(json.dumps({'basis':'Explicit original printed component permissions and narrowly supplied FAQ flare clauses; no missing full-card field reconstructed.','before_sha256':hashlib.sha256(before.encode()).hexdigest(),'after_sha256':hashlib.sha256(after.encode()).hexdigest(),'primary_sources':['Original rulebook p5 Classic Filch Wild role/phase and Cosmic Zap As Any Player','2018 FAQ p8 extraction774–784 Mite Super quoted pickup clause','2018 FAQ p6 extraction525–530 Oracle Wild hand-mixing example','2018 FAQ p16 extraction1528–1532 Loser Wild timing clause'],'notes_updates':updates,'cosmic_zap_replacement':{'old':old,'new':new},'planning_commitment_extension_added':False,'reserve_wild_derived_pairing_added':False,'human_scope_choices_adopted':False},indent=2,ensure_ascii=False)+'\n')
canonical.write_text(after)
core=R/'core-repair-draft.md';s=core.read_text();assert s.count(old)==1;core.write_text(s.replace(old,new))
assembly=R/'assemble_repair.py';s=assembly.read_text();marker='\ndef assemble():';assert s.count(marker)==1
overrides='\n# Explicit source-backed component/FAQ fragments, corrections06.\n'+''.join('notes['+repr(a)+']='+repr(value)+'\n' for a,value in updates.items())
assembly.write_text(s.replace(marker,overrides+marker))
print('repair-freeze-06',len(after),hashlib.sha256(after.encode()).hexdigest())
