from pathlib import Path
import json,hashlib,difflib
q=Path('docs/quality/summary-qa/ark-nova/2026-11-04-batch-231507');p=Path('rules/ark-nova.md');h=lambda b:hashlib.sha256(b).hexdigest();guard=json.loads((q/'canonical-write-tracker.json').read_text());assert h(p.read_bytes())==guard['expected_sha256'];before=p.read_text();s=before
old='place a random tile face up on each of the';new='place a random tile **face up** on each of the';assert s.count(old)==1;s=s.replace(old,new)
old='or to play a Conservation Project card from your hand and support it immediately.';new='or to **play a Conservation Project card from your hand and support it immediately**.';assert s.count(old)==1;s=s.replace(old,new)
old='If the new card exceeds the limit, discard the rightmost card.';new='If the new card exceeds the limit, **discard the rightmost card**.';assert s.count(old)==1;s=s.replace(old,new)
old='''      4. **Map-bonus timing depends on its symbol:**
         - **One-time bonus:** take it immediately when uncovered.
         - **Recurring-income bonus:** take it **immediately when uncovered AND again in every break**. Its immediate payment may be before or after the project reward, just like a one-time bonus.'''
new='''      4. **Map-bonus payments:** check both the immediate payment and the later-break column. The immediate payment is before or after the project reward, at your choice.

         | Uncovered bonus | Immediately upon uncovering | Every later break |
         |---|---|---|
         | One-time bonus | Take the bonus now | No repeat |
         | Recurring-income bonus | **Take the bonus now** | **Take that bonus again at every break** |'''
assert s.count(old)==1;s=s.replace(old,new)
old=' In addition you may make exactly **1 donation**: pay the smallest amount of money still visible in the donation area, cover that space with a player token from your supply, and gain **1 conservation point**. The printed donation costs are **2, 5, 5, 7, 7, 10, 10**, then the repeatable **12-money** space; skip spaces blocked at setup. Once all spaces but the last are covered, each subsequent donation costs **12 money** (no further tokens placed). A donation requires having performed at least 1 association task in the same action, needs no worker, and is limited to 1 per Association action.'
new='''
- **Donations — Association II only:**
  - **Eligibility:** your Association card must be upgraded, and you must have performed at least one association task in this same action. A donation needs no worker and is limited to **one per Association action**.
  - **Pay and reward:** pay the smallest amount of money still visible in the donation area, cover that space with a player token from your supply, and gain **1 conservation point**.
  - **Cost ladder:** **2, 5, 5, 7, 7, 10, 10**, then the repeatable **12-money** space; skip spaces blocked at setup.
  - **Final space:** once all spaces but the last are covered, every later donation costs **12 money**, with no further tokens placed.'''
assert s.count(old)==1;s=s.replace(old,new)
old='''| Ability | Target selection and special cases |
|---|---|
| Venom X | Every other zoo with higher appeal than yours and at least 5 appeal. |
| Hypnosis | The zoo with highest appeal and at least 5 appeal; choose among ties. If that zoo is yours, no effect. Copy only slot **1, 2 or 3**. |
| Pilfering 1 | The zoo with highest appeal and at least 5 appeal; choose among ties. A self-target has no effect. |
| Pilfering 2 | Resolve the highest-appeal target and the most-conservation target separately, each with at least 5 appeal. The conservation target must have at least 1 conservation. Choose ties; a self-target has no effect. If one zoo leads both tracks, pilfer from it twice. |
| Constriction | Every other zoo with at least 5 appeal that is ahead of yours on appeal and/or conservation. Each affected zoo puts tokens on **its own Action cards**: ahead on one track gives **1 token on its slot 5**; ahead on both gives **2 tokens on its slots 4 and 5**. |'''
new='''| Ability | Target selection and special cases | If the selected zoo is your own |
|---|---|---|
| Venom X | Every other zoo with higher appeal than yours and at least 5 appeal. | You are never a target. |
| Hypnosis | The zoo with highest appeal and at least 5 appeal; choose among ties. Copy only slot **1, 2 or 3**. | **No effect.** |
| Pilfering 1 | The zoo with highest appeal and at least 5 appeal; choose among ties. | **No effect.** |
| Pilfering 2 | Resolve the highest-appeal target and the most-conservation target separately, each with at least 5 appeal. The conservation target must have at least 1 conservation. Choose ties. If one zoo leads both tracks, pilfer from it twice. | **That selection has no effect**; resolve the other selection normally. |
| Constriction | Every other zoo with at least 5 appeal that is ahead of yours on appeal and/or conservation. Each affected zoo puts tokens on **its own Action cards**: ahead on one track gives **1 token on its slot 5**; ahead on both gives **2 tokens on its slots 4 and 5**. | You are never a target. |'''
assert s.count(old)==1;s=s.replace(old,new)
old='- F: 2 appeal per water-icon/rock-icon pair, maximum three pairs.';new='- F: **2 appeal per water-icon/rock-icon pair**. Count at most **3 pairs**, for a maximum of **6 appeal**.';assert s.count(old)==1;s=s.replace(old,new)
d=q/'expanded14-procedure-and-cap-clarity';d.mkdir();(d/'before.md').write_text(before);p.write_text(s);(d/'after.md').write_text(s);(d/'change.diff').write_text(''.join(difflib.unified_diff(before.splitlines(True),s.splitlines(True),fromfile='before.md',tofile='after.md')))
m=json.loads((q/'neutral-source-manifest.json').read_text());assert len(m['sources'])==7 and all(h(Path(x['path']).read_bytes())==x['sha256'] for x in m['sources']);record={'status':'APPLIED_AFTER_COMPLETE_B14_FULL_GRADES_AND_DECISIVE_NONPASS; A14_FULL_EXPORT_WILL_BE_COMPLETED','before_sha256':guard['expected_sha256'],'after_sha256':h(p.read_bytes()),'changes':[{'area':'Project play, overflow and map-bonus timing','basis':'Main raw801-831: immediate support on play, rightmost overflow discard, map bonus now plus recurring break income. Existing instructions emphasized; bonus timing shown in two-time-point table.','failure':'B14Q16 omits immediate-support condition, rightmost selection and recurring bonus timing. Coordinator independently confirms R5/R6 omissions; accepted neutralQ16 applies, no extra judge.'},{'area':'Bonus tile setup','basis':'Original main setup and existing summaryline64: all four random tiles face up. Only emphasis changes.','failure':'B14Q21 omits orientation.'},{'area':'Donations','basis':'Main AssociationII raw882-896 plus source diagram cost ladder: donation only with upgraded action, at least one task, one per action, no worker, supply token and smallest-cost ladder. Existing SideII paragraph split by eligibility/payment/cost/final-space.','failure':'B14Q29 has only bare sectionlabel for AssociationII eligibility.'},{'area':'DiversityResearcher219 cap','basis':'Original glossary219 and existing summary:2Appeal per water-rock pair, at most3pairs; maximum6Appeal is exact arithmetic.','failure':'B14Q78 says max3 without units.'},{'area':'Self-target selection','basis':'Original glossaryHypnosis/Pilfering and existing table: self-target has no effect, separate Pi2 selections. Existing rules moved into separate table column.','failure':'B14Q125 omits self-target outcomes.'}],'question_key_fact_reader_prompt_changes':False,'question_count':95,'new_question_credit':False,'all_seven_source_hashes_unchanged':True,'decisive_trial_report':'expanded-iteration-14/independent-grade-b.json'};(d/'repair-record.json').write_text(json.dumps(record,indent=2)+'\n');guard['expected_sha256']=record['after_sha256'];guard['last_change']='Project timing table; donation eligibility phases; self-target column; explicit219 cap units; Bonus-tile face-up emphasis.';(q/'canonical-write-tracker.json').write_text(json.dumps(guard,indent=2)+'\n');print(record['after_sha256'],len(s.splitlines()))
