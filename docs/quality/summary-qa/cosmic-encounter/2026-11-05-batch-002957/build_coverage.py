from pathlib import Path
import json,hashlib
R=Path(__file__).parent;B=R/'expanded-candidate-05'
Q=json.loads((B/'questions.json').read_text());K=json.loads((B/'answer-key.json').read_text());CM=json.loads((B/'candidate-question-map.json').read_text());FA=json.loads((R/'source-review/faq-question-candidates.json').read_text());AS=json.loads((R/'source-review/alien-catalog.json').read_text())
core=[]
def unit(p,heading,claim,ids,status='mapped-to-asked-rule',note=None):
 core.append({'source_id':f'RB-{len(core)+1:02}','source_file':'extracted/cosmic-encounter-rules.txt','pdf_page':p,'heading':heading,'procedural_claims_tested':claim,'question_ids':ids,'status':status,'note':note})
unit(2,'Game Overview / What is a Colony','Home/foreign definitions, one colony per color/planet, coexistence and foreign-five distribution',['Q002'])
unit(3,'During a Turn','Offense success/deal/loss branches, second-encounter cap and passing left',['Q017'])
unit(3,'Alien Powers and Rules Conflicts','Alien exception overrides ordinary rules; applied to Ooze above ordinary four-ship limit',['Q021'])
unit(4,'Alien Sheets fields','Roles, optional/mandatory use and timing bars, distinct from history', [f'Q{i:03}' for i in range(21,71)])
unit(4,'Cosmic Cards / encounter and reinforcement illustrations','Allowed encounter types versus non-encounter categories; reinforcement role/timing',['Q014','Q152','Q153'])
unit(5,'Cosmic Zap illustration','One use, own-or-other power, no further use current encounter',['Q018','Q019','Q100','Q119'])
unit(5,'Clone flare illustration','Wild artifact retention and later-encounter replay; Super compensation choices/availability',['Q109','Q145'])
unit(5,'Classic Filch flare illustration','Wild illicit taking/caught penalty/reveal and Super changed role/phase',['Q146','Q147'])
unit(6,'Setup steps1–3','Warp/color/planets/ships/markers and unused destiny colors',['Q150'])
unit(6,'Setup steps4–7','Two-flare alien choice, ten-flare deck, hands, first player and Filch-version choice',['Q001','Q150'])
unit(7,'Starting the Turn','Starting encounter-less hand replacement and distinction from later offensive exhaustion',['Q016','Q076'])
unit(7,'Regroup','Mandatory one retrieval to existing colony or original gate exception; laterFAQ named exception separately',['Q003','Q140'])
unit(7,'Destiny: deck/color','Shuffle before last card; color target; own-color redraw/drive-out/reclaim',['Q004','Q005','Q078'])
unit(7,'Destiny: wild/special/hazard','Wild choices, special conditions/color equivalence, inactive base hazard symbols',['Q151'])
unit(8,'Launch','Offensive1–4 ships from own colonies; defense cannot adjust target; stripping and no-ship continuation',['Q006','Q080','Q142'])
unit(8,'Targeting / Defending with Nothing / Bystanders','Ordinary home-system targets, zero home defense, bystanders and selected foreign defense',['Q005','Q008','Q009'])
unit(9,'Alliance','Invite/commit order, player roles, refusal,1–4 from colonies, physical defensive placement',['Q007','Q152'])
unit(9,'Planning','Main-only encounter selection, types, face-down default; defense redraw and offense exhaustion',['Q016','Q152'])
unit(9,'Reveal: attacks','Attack totals and defense ties, plus timing visibility',['Q008','Q152'])
unit(10,'Attack / negotiate','Automatic negotiate loss and compensation trigger',['Q011','Q072'])
unit(10,'Both negotiate','Allied return, minute limit, permitted deal terms/locations, recipient ship sources and leftover gate ships',['Q012','Q094','Q154'])
unit(10,'Morph','Initial copy and attack/negotiate pairings; later value changes and original identity',['Q013','Q082'])
unit(11,'Morph versus Morph counterfactual','Printed impossible counterfactual retained in summary; no legal second Morph in exact base box',[],'excluded-current-core-scenario','Do not manufacture an excluded duplicate-card effect; independent reviewer may challenge this applicability decision.')
unit(11,'If offense won','Landing/reinforcement, losing side warp and bystander survival',['Q009'])
unit(11,'If defense won','Defense stays, offense warp, defensive ally own-colony return and mixed defender rewards',['Q008','Q010'])
unit(11,'Deal made / failed','Success/failure and three-ship penalty',['Q012','Q017'])
unit(11,'Compensation / Rewards distinction','Own actual warp loss, allies excluded, random opponent hand and shortfall',['Q011','Q072','Q073'])
unit(11,'After Resolving','Normal encounter-card discard, second-encounter conditions and pass left',['Q013','Q017','Q152'])
unit(12,'Shared Wins','Simultaneous wins and Tick-Tock deal sharing',['Q020'])
unit(12,'Losing Alien Powers','Immediate home-colony threshold/loss/regain and no last use',['Q018','Q084','Q101'])
unit(12,'Zapping Powers','Use versus non-use clauses, cancellation duration and examples',['Q018','Q068','Q097','Q098','Q099','Q100'])
unit(12,'Timing Conflicts','Offense/defense/others order and specific within-phase timing',['Q019','Q093','Q099','Q118','Q144'])
unit(12,'Driving Out Foreign Colonies','Own-color or self-special eligibility, chosen defense and bystanders',['Q004','Q005','Q143'])
unit(12,'Home Planets Without Colonies','Home owner zero-ship defense',['Q005'])
unit(13,'Stripping / no-colony relocation','Immediate colony loss, no ordinary return to vacated planet, no destination means warp',['Q006','Q142'])
unit(13,'Drawing New Cards','Start/defense/later-offense windows, repeated defense draw, own-player ship returns',['Q016','Q017'])
unit(13,'Card Types','Six base types and Plague Morph branch',['Q089'])
unit(13,'Artifact Cards','Cannot be encounter card; printed instructions/timing; normal discard',['Q153'])
unit(13,'Reinforcement Cards','Roles, Reveal timing, either side and response until all pass',['Q014'])
unit(13,'Flare Cards','Non-encounter category, limits, return, ownSuper/Wild after powerloss/Zap',['Q015','Q095','Q096','Q097','Q098','Q104','Q123'])
unit(14,'Alien Interactions','Oracle before-selection versus Sorcerer after-selection',['Q144'])
unit(14,'Variants','Four Planets/Hidden/Rotating/Freewheeling excluded',[],'excluded-optional-variants')
unit(15,'Technology','Technology setup/research/complete/abandon/acquire excluded',[],'excluded-optional-Technology')
unit(16,'Reference','Duplicate phase/turn/timing procedures mapped above',['Q014','Q017','Q019','Q152'],'duplicate-reference')
aliens=[{'source_file':a['source']['original_file'],'sha256':a['source']['sha256'],'alien':a['alien'],'question_id':f'Q{i+21:03}','tested_claims':'All printed operative ability clauses, setup if present, role, optional/mandatory status, highlighted power-use phases; retain applicable official corrections.','authority':'Original printed image, not catalog/OCR prose.'} for i,a in enumerate(AS['aliens'])]
def resolve(value):
 if not value:return []
 if value in CM:return resolve(CM[value])
 return value.split('/') if value.startswith('Q') else []
faqmap=[]
for item in FA['accepted_historical_faq_passage_map']:
 row=dict(item);ids=list(item.get('seed_explicitly_asked_by',[]))
 for c in item.get('candidate_ids',[]):ids+=resolve(CM.get(c))
 row['question_ids']=sorted(set(ids));row['counted_tested_coverage']=bool(row['question_ids'])
 if item['source_id']=='FAQ-Q312':row.update(question_ids=[],counted_tested_coverage=False,disposition='excluded-optional-Technology',parent_override='Energy Cloak is outside declared scope; historical source matrix preserved.')
 if item['source_id'] in ['FAQ-Q014','FAQ-Q032']:row.update(counted_tested_coverage=False,disposition='pending-authority-conflict',parent_override='No dependent outcome key frozen pending coordinator human/sourced resolution.')
 faqmap.append(row)
faqmap.append({'source_id':'FAQ-Q108','historical_scope_status':'excluded','pdf_pages':[8],'lines':[759,765],'question_ids':['Q155'],'counted_tested_coverage':True,'disposition':'accepted-in-part-after-independent-source-audit','reason':'Declare all reward sources before taking any; base warp/cosmic-card choice explicitly in example. Reward deck remains excluded.','correction_record':str((R/'source-review/faq-scope-refinement-01.json').resolve())})
historic=[{'pdf_page':1,'heading':'Macron retained erratum','cache_lines':[10,25],'question_ids':['Q042','Q122']},{'pdf_page':1,'heading':'Spiff retained erratum','cache_lines':[26,32],'question_ids':['Q059']},{'pdf_page':1,'heading':'Warrior retained erratum','cache_lines':[33,42],'question_ids':['Q068','Q078']},{'pdf_page':1,'heading':'Mind Wild retained erratum','cache_lines':[43,49],'question_ids':['Q148']},{'pdf_page':1,'heading':'Reincarnator Wild retained erratum','cache_lines':[50,58],'question_ids':['Q130','Q149']}]
out={'bank_version':Q['benchmark_version'],'question_count':len(Q['questions']),'status':'parent-map awaiting independent source/novelty/key-scope challenge; not completion','core_rulebook_passages':core,'original_fifty_printed_abilities':aliens,'applicable_2018_faq':faqmap,'retained_2009_errata':historic,'all_2018_entries_scope_matrix':str((R/'source-review/faq-scope.json').resolve()),'known_pending_authority':[{'topic':'reinforcement/negotiate','source':'2018FAQpp3/4','question_ids':[],'status':'coordinator asked human; no answer received'},{'topic':'ordinary reveal / Calculator equal values / Hate equal values','source':'original setup and printed sheets versus FAQ example','question_ids':[],'status':'coordinator handling; questions ask only independent original printed rules until actual resolution'}],'scope_challenges':[{'question_id':'Q086','issue':'All defensive-system planets already occupied: establish positive current-base relevance rather than excluded win-extension variant.'},{'question_id':'Q143','issue':'Original rulebook expressly gives self-special conditional; verify current-core applicability and do not import expansion-only enabling effect.'}],'contextual_key_background_warning':'Seed key includes background not all explicitly asked; fresh per-question scope mapping must separate it before expanded blind testing. Do not credit such background as tested coverage.'}
(B/'coverage-map.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print('Core passage records',len(core),'aliens',len(aliens),'FAQ mapped rows',len(faqmap),'pending/excluded FAQ',sum(not x['counted_tested_coverage'] for x in faqmap))
