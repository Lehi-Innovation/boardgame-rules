from pathlib import Path
import json,hashlib,shutil,difflib
B=Path(__file__).parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();p=Path('rules/spirit-island.md');before=p.read_text();assert p.read_bytes()==(B/'source-candidate-11.md').read_bytes()
s=before.replace('Resolve the base effect and every met threshold in printed order.','Resolve the base effect and every met threshold in printed order **unless explicit timing text says otherwise**: “First” and “Before” can place a threshold instruction ahead of earlier-printed base instructions.')
s=s.replace('**Dissolve the Bonds of Kinship** line 3 Pushes all Explorers; its Invaders damaging each other do so simultaneously.','**Dissolve the Bonds of Kinship** line 3 Pushes all Explorers; its Invaders damaging each other do so simultaneously, **before** the Explorer Push as the threshold specifies.')
s=s.replace('**Wrap in Wings of Sunlight** grants no Defend if zero Dahan move:','**Wrap in Wings of Sunlight** resolves its threshold’s **First, Gather up to 3 Dahan** before its base Move; those gathered Dahan may then move and allow the destination’s Defend. It grants no Defend if zero Dahan move:')
needle="Tidal Boon's “if Dahan are pushed” clause applies only to that Power's own Push."
assert needle in s
s=s.replace(needle,needle+' When Ocean uses Tidal Boon, Ocean may move Dahan pushed to its Ocean by that use to **any Coastal land**, including a nonadjacent one, instead of Drowning them. Ocean chooses; this alternative is optional. [Original core card text]')
needle='- **Location-dependent effects:**'
assert needle in s
s=s.replace(needle,'- **Dread Apparitions Fear sources:** While its effect is active, Power-generated Fear in its target land adds **Defend 1 per Fear**. Fear from **To Dream a Thousand Deaths** counts; normal Fear for destroying Towns/Cities does not, even when a Power caused the destruction. [Original core card text]\n'+needle)
assert s!=before and 'this alternative is optional' in s and 'Dread Apparitions Fear sources' in s
p.write_text(s);(B/'core-card-procedural-exceptions-clarification.patch').write_text(''.join(difflib.unified_diff(before.splitlines(True),s.splitlines(True),fromfile='source-candidate-11.md',tofile='rules/spirit-island.md')))
dst=B/'source-candidate-12.md';assert not dst.exists();shutil.copyfile(p,dst)
(B/'source-candidate-12-manifest.json').write_text(json.dumps({'summary':str(dst.resolve()),'sha256':H(dst),'source_manifest':'source-manifest.json','additional_authoritative_sources':'supplemental-source-manifest-v2.json','supersedes':'source-candidate-11.md','changes':'Consolidated review07 core procedural exceptions: Dread Fear-source eligibility, Ocean’s optional Tidal alternative and explicit First/Before threshold timing. Repositioning-before-empty and individual Spirit Phase order were already explicit.','new_final_source_audit_required_after_scope_stabilization':True},indent=2)+'\n')
(B/'expanded-v13/build-status.json').write_text(json.dumps({'bank_and_map_frozen':True,'summary_edit_completed':True,'initial_attempt':'build_expanded_v13.py froze bank/map but stopped before any canonical mutation because the Tidal prose anchor differed. No bank/key/map file was overwritten.','completion_script':'../finish_summary_v13.py','reader_outputs_exist':False},indent=2)+'\n')
print('Candidate12',len(s),'characters; SHA256',H(dst))
