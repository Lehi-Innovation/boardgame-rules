from pathlib import Path
import json,hashlib
R=Path(__file__).parent
Q=json.loads((R/'expanded-draft-01/questions.json').read_text());K=json.loads((R/'expanded-draft-01/answer-key.json').read_text())
Q['benchmark_version']=K['benchmark_version']='expanded-candidate-05'
faq=json.loads((R/'source-review/faq-question-candidates.json').read_text())
core=json.loads((R/'source-review/core-question-candidates.json').read_text())
ledger=[];maps={}
def refs(c):return [f"{s['file']} PDF pp{','.join(map(str,s['pdf_pages']))} extraction lines{s['lines'][0]}–{s['lines'][1]} ({s['id']})" for s in c['source_passages']]
def append(question,facts,background,sources,label,novelty,candidate):
 ident=f'Q{len(Q["questions"])+1:03}'
 Q['questions'].append({'id':ident,'question':question})
 K['answers'].append({'id':ident,'required_facts':facts,'contextual_background':background,'source_references':sources})
 ledger.append({'candidate':candidate,'label':label,'decision':'accepted-distinct-rule-or-branch','question_id':ident,'novelty':novelty})
 maps[candidate]=ident
 return ident
merges={'FAQC005':'Q028','FAQC016':'Q028','FAQC019':'Q043','FAQC030':'Q042','FAQC076':'Q068','FAQC079':'Q070'}
rejects={
 'FAQC009':('nonprocedural-scope-context','No official two-player variant is not a distinct current-standard encounter rule; player count retained as scope context.'),
 'FAQC051':('excluded-optional-setup-relaxation','Standard printed Gambler restriction and conflict recovery are tested; optional FAQ relaxation is outside the declared standard setup.'),
 'FAQC077':('duplicate-covered-by-alien-procedure','Q069 already asks corrected timing and actual third-system colony requirement; Q005 covers home-owner defense with zero ships. No new ruling branch.'),
 'FAQC047':('merged-with-complete-printed-component-procedure','Core classic-Filch procedure question includes this exact reveal/Zap exception; count it once there.')}
for c in faq['candidates']:
 cid=c['id'];f=c['required_asked_facts'][:];question=c['question'];source=refs(c)
 if cid=='FAQC053':f=[x.replace('qualifying higher attack','qualifying attack') for x in f]
 if cid=='FAQC044':
  question+=' Must the opponent have sufficient cards for the chosen compensation amount?'
  f+=['The opponent must have sufficient cards for the chosen amount.'];source+=['Original rulebook p5 printed Clone Super illustration']
 if cid=='FAQC056':
  question+=' May Human play Cosmic Zap on its own power use?'
  f+=['Yes; Cosmic Zap can target its own player\'s power use.'];source+=['Original rulebook p5 printed Cosmic Zap illustration']
 if cid in merges:
  ident=merges[cid];idx=next(i for i,x in enumerate(Q['questions']) if x['id']==ident)
  Q['questions'][idx]['question']+=' '+question
  # Q070 already contains the full no-cap/opponent-only FAQ fact; make its cap explicitly asked without duplicate facts.
  if cid!='FAQC079':
   for fact in f:
    if fact not in K['answers'][idx]['required_facts']:K['answers'][idx]['required_facts'].append(fact)
  K['answers'][idx]['source_references']+=source
  maps[cid]=ident;ledger.append({'candidate':cid,'label':c['label'],'decision':'merged-into-unfrozen-alien-question','question_id':ident,'novelty':c['novelty_rationale']});continue
 if cid in rejects:
  decision,why=rejects[cid];maps[cid]='Q069/Q005' if cid=='FAQC077' else 'CORE-C05' if cid=='FAQC047' else None
  ledger.append({'candidate':cid,'label':c['label'],'decision':decision,'reason':why,'question_id':maps[cid]});continue
 ident=append(question,f,c['contextual_background_not_scored'],source,c['label'],c['novelty_rationale'],cid)
 if cid=='FAQC020':ledger[-1]['scope_challenge_required']='Explicit base FAQ conditional; reviewer must examine whether all-planets occupation can be current-core state before ordinary victory, rather than needing excluded expansion/variant.'
for c in core['candidates']:
 append(c['question'],c['required_facts'],c['contextual_background'],c['source_references'],c['candidate_id'],c['novelty'],c['candidate_id'])
append('For the original classic Filch Super shown in the rulebook, which player role and phase are printed, whose used encounter card may be filched, and must the user have participated in that encounter?', ['As any player during Reveal.','May filch any other player\'s used encounter card whether involved or not.'],[],['Original rulebook p5 printed classic Filch Super illustration'],'Classic Filch Super changed role and timing','Printed exception changes normal Filch eligibility and phase, rather than reskinning the alien power.','CORE-C06')
append('Under the retained official Mind Wild erratum, when can the flare be played, which later draws does that one play intercept, what does the user do with each intercepted card, and may the information be shared?', ['Play when another player draws a card from the cosmic deck.','For rest of encounter intercept cards that same player must draw, not every player\'s later draws.','User draws, inspects, and gives each card to that player.','May not share the information with other players.'],[],['Official May6 2009 FAQ p1 Mind Flare erratum, cached extraction L43–49'],'Corrected Mind Wild target and information','Ongoing-duration question does not ask the chosen-player restriction, draw/inspect/give procedure or secrecy.','CORE-C07')
append('Under the retained Reincarnator Wild erratum, what event and target restrictions permit giving the flare to another player, when does that target replace its power, and which replacement aliens are rejected?', ['After another player besides Reincarnator loses or fails a deal, may give them the flare.','Immediately after end of encounter target discards current power and draws a new one.','Reject Game Setup and disallowed aliens and draw again.'],[],['Official May6 2009 FAQ p1 Reincarnator Flare erratum, cached extraction L50–58'],'Corrected Reincarnator Wild replacement procedure','FAQC067 covers delayed timing/self-target/incarnation Super but not full printed replacement event and candidate exclusions.','CORE-C08')
append('Before choosing aliens, how are the warp, player planets, ships and colony markers set up in a standard game, which destiny cards are removed or retained, and may both Filch flare versions be included?', ['Warp in center; each player chooses a color and takes its five planets.','Each player has twenty ships, four on each home planet.','Colony markers begin beside the warp at zero foreign colonies.','Remove destiny cards for unused player colors; retain used colors, wilds and specials and shuffle.','Use either standard or classic Filch flare, only one version; return the other to box.'],[],['Original rulebook p6 Setup steps1–3,5; p5 Alternate Filch'],'Standard physical setup and Filch-version exclusion','SeedQ001 tests alien/flare selection, hands and first player only, not the physical setup or unused-color and duplicate-Filch exclusions.','CORE-C09')
append('In an ordinary encounter, what opponent and system choices does a wild destiny card permit, how does a special destiny card determine the defense and location, what color does a special count as for color-sensitive effects, and do hazard symbols change base play?', ['Wild permits choosing another player, encountered in that player\'s home system.','Special states defense conditions and location; follow its text.','For effects special is treated as the designated defense\'s color.','Hazard symbols have no effect in this original base game.'],[],['Original rulebook p7 Destiny'],'Wild/special destiny branches and inert hazards','Own-color redraw/Blue targets in seed do not ask wildcard choice, special substitution or hazard-symbol relevance.','CORE-C10')
append('May the two main players invite one another as allies? Without an exception, may an uninvited other player join, may an invitee refuse, and how many ships from where does each joining ally commit? After alliances, which players select encounter cards, which types are legal, how are they placed/revealed, and when are they normally discarded?', ['Neither main player may invite the other.','Non-main players normally need invitation; may decline all invitations.','Each ally commits one to four own ships from any own colonies.','Only offense and defense select one encounter card each: attack, negotiate or Morph.','Normally placed facedown at Planning and revealed simultaneously at Reveal, subject to powers.','Normally discard revealed encounter cards after resolving encounter, unless an effect changes destination.'],[],['Original rulebook p9 Alliance/Planning/Reveal,p11 After Resolving Encounter'],'Ally eligibility/commitment and ordinary card procedure','SeedQ007 asks invitation/commitment order and defensive placement; its key has count facts not explicitly asked. This asks actors, commitment sources/count, refusal, main-only card selection, face state and normal discard.','CORE-C11')
append('Can an artifact be selected as the encounter card, how do you determine when and how it may be played, and what is its normal destination after play?', ['Artifacts cannot be played as encounter cards.','Each artifact\'s printed timing and instructions determine when/how it can be played.','Normally discard an artifact after playing it.'],[],['Original rulebook p13 Artifact Cards'],'Generic artifact procedure','Clone Wild asks a retention exception; this explicitly asks the ordinary artifact category, printed-timing rule and discard destination.','CORE-C12')
append('When a deal grants a colony, must the recipient use only its ships on the hyperspace gate or may it use other ships, and which ship location is excluded? After the deal, where do any remaining offensive gate ships return?', ['Any of the recipient\'s own ships not in the warp may establish its deal colony; not restricted to gate ships.','Any offensive ships remaining on gate after the deal return to any of offense\'s existing colonies.'],[],['Original rulebook p10 If Both Players Reveal Negotiate Cards'],'Deal colony ship sources and remaining gate ships','SeedQ012 asks allies, exchange terms and planet eligibility but does not ask recipient ship sources or unused offensive gate-ship return.','CORE-C13')
append('A defensive ally has three defender rewards. May it draw a card, inspect it and then decide whether the remaining rewards will be more cards or warp ships? When must it commit to the full mix of reward sources?', ['Must declare all reward sources before taking any rewards, including the complete base cosmic-card/warp-ship mix.','Cannot inspect an initial draw before deciding remaining reward sources.'],['The reward-deck components in the source example remain excluded; only its general all-sources commitment rule is tested.'],['Official FAQ through2018 p8, Reward Deck, extractionlines759–765; independently identified source auditPSA-001'],'Declare all reward sources before collection','Newly recovered base-relevant timing rule from a mixed expansion section; existing Q010 tests mixing benefits, not when that mix is committed.','CORE-C14')
# Remove duplicate exact calculation facts where the original sheet example already contains the same asked result.
for ident,prefix in [('Q024','15 becomes7'),('Q045','15→51')]:
 for a in K['answers']:
  if a['id']==ident:a['required_facts']=[x for x in a['required_facts'] if not x.startswith(prefix)]
out=R/'expanded-candidate-05';out.mkdir(exist_ok=True)
for name,data in [('questions.json',Q),('answer-key.json',K),('acceptance-rejection-ledger.json',ledger),('candidate-question-map.json',maps)]:
 (out/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
(out/'question-bank.md').write_text('# Expanded candidate bank — source/coverage review pending\n\n'+ '\n\n'.join(f"## {q['id']}\n\n{q['question']}\n\n"+'\n'.join('- '+f for f in a['required_facts'])+'\n\nSources: '+ '; '.join(a['source_references']) for q,a in zip(Q['questions'],K['answers']))+'\n')
scope=[]
for q,a in zip(Q['questions'],K['answers']):
 scope.append({'id':q['id'],'actual_question':q['question'],'asked_clause_groups':[{'clause':q['question'],'required_fact_ids':[f"{q['id']}-F{i+1:02}" for i in range(len(a['required_facts']))]}],'required_answer_facts':[{'fact_id':f"{q['id']}-F{i+1:02}",'fact':f,'parent_scope_status':'candidate-needs-fresh-scope-validation'} for i,f in enumerate(a['required_facts'])],'contextual_key_background':a['contextual_background'],'scope_note':'Fresh reviewer must split any contextual key-only parts from actual asked clauses, especially frozen seed entries; no source-wide scoring caps.'})
(out/'question-scope-map-candidate.json').write_text(json.dumps({'version':'candidate-05','status':'not-final-scope-map; fresh validation required','questions':scope},indent=2,ensure_ascii=False)+'\n')
seedq=json.loads((R/'seed-v1/questions.json').read_text());seedk=json.loads((R/'seed-v1/answer-key.json').read_text())
assert Q['questions'][:20]==seedq['questions'];assert K['answers'][:20]==seedk['answers']
priorq=json.loads((R/'expanded-candidate-04/questions.json').read_text());priork=json.loads((R/'expanded-candidate-04/answer-key.json').read_text())
assert Q['questions'][:len(priorq['questions'])]==priorq['questions'];assert K['answers'][:len(priork['answers'])]==priork['answers']
(out/'input-manifest.json').write_text(json.dumps({'frozen_for_source_coverage_review_only':True,'original_seed_entries_preserved':True,'question_count':len(Q['questions']),'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir() if p.is_file() and p.name!='input-manifest.json'}},indent=2)+'\n')
print('Expanded candidate count',len(Q['questions']),'facts',sum(len(a['required_facts']) for a in K['answers']))
