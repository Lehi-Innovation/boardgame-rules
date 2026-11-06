from pathlib import Path
import json,hashlib,difflib,shutil
q=Path('docs/quality/summary-qa/ark-nova/2026-11-04-batch-231507');p=Path('rules/ark-nova.md');s=p.read_text();h=lambda x:hashlib.sha256(x).hexdigest();t=json.loads((q/'canonical-write-tracker.json').read_text());assert h(p.read_bytes())==t['expected_sha256']
d=q/'expanded12-timing-target-and-map-clarity';d.mkdir();(d/'before.md').write_text(s)
old='''      3. Gain the depicted conservation reward and any depicted reputation. Removing the map token activates its uncovered bonus: take it immediately, before or after the project reward at your choice.
      4. **Recurring bonus:** if the uncovered map bonus is marked as recurring income, gain that same bonus again in every break.'''
new='''      3. Gain the depicted conservation reward and any depicted reputation. Removing the map token also activates its uncovered bonus. Resolve the project reward and the immediate map bonus **in either order, at your choice**.
      4. **Map-bonus timing depends on its symbol:**
         - **One-time bonus:** take it immediately when uncovered.
         - **Recurring-income bonus:** take it **immediately when uncovered AND again in every break**. Its immediate payment may be before or after the project reward, just like a one-time bonus.'''
assert s.count(old)==1;s=s.replace(old,new)
old='| Constriction | Every other zoo with at least 5 appeal that is ahead of yours on appeal and/or conservation. Ahead on one track gives **1 token** (slot 5); ahead on both gives **2 tokens** (slots 4 and 5). |'
new='| Constriction | Every other zoo with at least 5 appeal that is ahead of yours on appeal and/or conservation. Each affected zoo puts tokens on **its own Action cards**: ahead on one track gives **1 token on its slot 5**; ahead on both gives **2 tokens on its slots 4 and 5**. |'
assert s.count(old)==1;s=s.replace(old,new)
old='- **Constriction:** affect all other zoos ahead of yours on appeal and/or conservation. A zoo ahead on one track receives Constriction 1; ahead on both receives Constriction 2. Place tokens on cards in the highest slots (one on 5, or two on 4 and 5).'
new='- **Constriction — affected players and card ownership:** every affected **other zoo** (at least 5 appeal and ahead of yours on appeal and/or conservation) places tokens on **that affected zoo’s own Action cards**. Ahead on one track: one token on **its slot-5 card**. Ahead on both tracks: one token on **each of its slot-4 and slot-5 cards**.'
assert s.count(old)==1;s=s.replace(old,new)
old='Ties for highest appeal or conservation let you choose the affected player; a conservation leader needs at least one conservation point.'
new='''**Tie rule for BOTH Pilfering 1 and Pilfering 2:** you, the acting player, choose the affected zoo among tied leaders. This applies separately to **each** Pilfering 2 selection: tied highest-appeal zoos and tied most-conservation zoos. A conservation leader needs at least one conservation point.'''
assert s.count(old)==1;s=s.replace(old,new)
old='- **Map 5, Park Restaurant:** break income is one money per adjacent **covered hex**, regardless of building type, occupancy or several hexes belonging to one building. The Restaurant is not a building. Its special-enclosure placement bonus gives **one Reptile House or one Large Bird Aviary** free, even before Build II. Choose one, not both, and follow the other normal placement rules.'
new='''- **Map 5, Park Restaurant:**
  - **The Restaurant’s own break income:** one money per adjacent **covered hex**, regardless of building type or occupancy. Empty enclosures qualify; several adjacent hexes belonging to one building each count separately.
  - **Income of adjacent kiosks:** the Restaurant is **not a building** and contributes **zero income to adjacent kiosks**. Those kiosks still count their other qualifying neighboring buildings normally.
  - **Special-enclosure placement bonus:** gain **one Reptile House or one Large Bird Aviary** free, even before Build II. Choose one, not both, and follow the other normal placement rules.'''
assert s.count(old)==1;s=s.replace(old,new)
p.write_text(s);(d/'after.md').write_text(s);(d/'change.diff').write_text(''.join(difflib.unified_diff((d/'before.md').read_text().splitlines(True),s.splitlines(True),fromfile='before.md',tofile='after.md')))
record={'status':'APPLIED_AFTER_COMPLETE_12_FULL_GRADES_AND_NONPASS','before_sha256':t['expected_sha256'],'after_sha256':h(p.read_bytes()),'changes':[{'area':'Project map-bonus timing','basis':'Main raw text829-831: immediate bonus, recurring bonuses again each break, before/after project reward choice. Same facts reformatted into explicit timing branches.','failure':'A12Q16 omits recurrence at breaks.'},{'area':'Pilfering ties','basis':'Glossary raw1369-1373: choose among tied appeal or conservation leaders; scope applies separately to both Pilfering2 selections.','failure':'A12Q53 states tie choice only for Pilfering1.'},{'area':'Constriction ownership','basis':'Glossary raw1277-1292 and existing target table: affected other players receive tokens on their own slot5 or slots4/5 cards.','failure':'B12Q40 says other zoos lead yours then puts tokens on your cards.'},{'area':'Map5 Restaurant and kiosks','basis':'Glossary raw1709-1715: per adjacent covered hex including empty enclosures; Restaurant does not count as building, explicitly for kiosks. Existing SC04 enclosure bonus retained verbatim.','failure':'B12Q116 invents an adjacent-kiosk exception.'}],'question_key_fact_prompt_changes':False,'question_count':95,'new_question_credit':False,'final_trial_results':'expanded-iteration-12/results.json'}
(d/'repair-record.json').write_text(json.dumps(record,indent=2)+'\n');t['expected_sha256']=record['after_sha256'];t['last_change']='Explicit bonus timing branches, shared Pilfering ties, affected-zoo Constriction ownership, Restaurant/kiosk income separation.';(q/'canonical-write-tracker.json').write_text(json.dumps(t,indent=2)+'\n')
r=q/'expanded-iteration-12';shutil.copyfile(r/'results.json',r/'initial-results.json')
print(record['after_sha256'],len(s.splitlines()))
