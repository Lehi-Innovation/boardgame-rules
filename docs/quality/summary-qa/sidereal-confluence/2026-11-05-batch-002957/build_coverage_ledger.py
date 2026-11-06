from pathlib import Path
import json,hashlib,datetime
ROOT=Path(__file__).resolve().parent
bank=ROOT/'expanded-v2'; qs=json.loads((bank/'questions.json').read_text())['questions'];key=json.loads((bank/'answer-key.json').read_text())['answers'];km={e['id']:e for e in key}
units=[]
def unit(name,refs,ids,note=''):
 units.append({'source_procedural_unit':name,'source_references':refs,'questions':ids,'actually_asked_fact_ids':[f['id'] for i in ids for f in km[i]['required_facts']],'coverage_note':note or 'These questions ask operative facts in this source group; contextual key background earns no coverage credit.'})
unit('Resource types, point privacy, ship interchangeability and physical shortages',['Booklet pp1–2 Components; p7 shortage paragraph'],['Q18','Q23','Q25'])
unit('Card ownership, one-turn loans and permanent cards',['Booklet pp2,6,9 cards and return procedure'],['Q03'])
unit('Printed card entry symbols and actual output previews',['Booklet p2 card diagrams; p6 research example'],['Q21','Q26','Q57'])
unit('Species selection and starting player/table setup',['Booklet pp3–5 complete setup and diagrams'],['Q21','Q22'])
unit('Ordinary phases and Trade-end boundary',['Booklet p6 Phases/Trade'],['Q01','Q66'])
unit('Binding future/multilateral contingent agreements and failed delivery',['Booklet p6 Trade complete agreement paragraphs'],['Q02','Q24'])
unit('Trade-only exchanges, Economy silence, permitted bid negotiations',['Booklet pp6–8 phase restrictions'],['Q30','Q56'])
unit('Invention alternatives, team flip, access timing and actual awards',['Booklet p6 research procedure and diagram; p8 sharing'],['Q04','Q29','Q57','Q66'])
unit('Violet entry exception and free converters',['Booklet pp2,6–7 entry/white converter diagrams'],['Q26'])
unit('Two upgrade routes, owner restriction, spent-card destination/use limit and renamed cards',['Booklet pp6–7 upgrade procedure and examples'],['Q05','Q27','Q51','Q67'])
unit('Colony flips, climate-specific consumption, discard orientation and ordered cycling',['Booklet pp2,7 colony rules/diagram'],['Q27','Q28'])
unit('Economy support check, acquisition above support and white-converter operation',['Booklet pp7–8 support/Economy'],['Q06','Q26','Q31'])
unit('Simultaneous production forbids chaining all goods',['Booklet p7 Economy; Faderan back Transmutive Decomposer and Grindstone'],['Q06','Q43','Q60'],'Generic no-chaining applies to resources, points and ships. Replacing the converter name with Transmutive Decomposer without a new timing/exception is not another novel question.')
unit('Donation storage, next-Trade disposal, gift refusal and donation points',['Booklet p7 complete donation paragraphs'],['Q07','Q10'])
unit('Wild input/output size and matching-color exceptions',['Booklet p7 wild paragraphs; Eni Et/Unity/Zeth originals'],['Q12','Q18','Q35','Q50','Q52','Q65'])
unit('Technology sharing, central splay, per-invention bonus and unique era IV',['Booklet p8 sharing before Bidding'],['Q04','Q29','Q66'],'Announcement and central splay are part of the broad how-invention/sharing method but not separate omission gates where not asked. All material bonus/access/timing branches are expressly asked.')
unit('Secret bid allocation, total announcement, empty piles, simultaneous reveals, purchase/pass and rank',['Booklet p8 Bidding allocation and both reveal procedures'],['Q08'])
unit('Bid tie comparison by relevant card type then species number',['Booklet p8 ordinary tie paragraph'],['Q08','Q46','Q48'])
unit('Track cleanup, minimum-one aging, slide/refill front-up',['Booklet pp8–9 Bidding cleanup'],['Q09'])
unit('End-of-turn loans and Confluence advancement/remaining phase counters',['Booklet p9 Ending Turn; original Turn6 reverse386/396'],['Q03','Q58'])
unit('Final donation retention, leftover groups, all-group scoring, no score tiebreak',['Booklet p9 Ending Game; final Confluence fronts; designer26690049'],['Q10','Q55','Q59','Q60'])
unit('Exact final-turn sequence, current final bonus and no extra round/bidding',['Booklet pp1,4,9; original Confluence cards; direct designer26690049'],['Q58','Q59','Q60','Q61'])
unit('Final input versus output colors, no post-Economy invention and final Zeth exception',['Direct original-designer26690049 and26803262'],['Q60','Q61'])
unit('Caylion colony bid halving/fractions/minimum boundary; research exception',['Caylion front Halved Colonization Bids'],['Q11','Q32'])
unit('Caylion seedling starting/acquisition/non-grant/upgrade/trade/discard/production exceptions',['Caylion front complete Seedling Tokens'],['Q11','Q33','Q63'])
unit('Caylion violet-upgrade resource available immediately',['Caylion front Upgrading the Economy'],['Q34'])
unit('Eni Et cannot run own interest, may upgrade, upgraded cards retain rules even without growth',['Eni Et front Interest Converters and depicted card'],['Q12','Q52'])
unit('Eni Et all-wild versus mixed colored/wild inputs, intact gray passage and no gray multiplication',['Eni Et front Unity Wild Resources'],['Q12','Q35','Q52'])
unit('Faderan Acknowledgments cannot circulate, mandatory per-invention return and common-pool reward',['Faderan original front plus full2019 photo'],['Q13','Q39'])
unit('Faderan shuffled hidden deck, one shared converter once, printed4-white/jungle cost, ordinary loans',['Faderan original front; booklet p2 deck converter; printed relic deck'],['Q03','Q14','Q36'])
unit('Automated Transport Network entry and transferable support including Im’dril',['Faderan back; original printed61/396'],['Q37'])
unit('Contextual Integrator Cache entry count/ceiling and unchanged behavior on trade',['Faderan back Cache first paragraphs; printed60/396'],['Q38'])
unit('Cache mandatory cube-cost reduction versus octagon no-discount, usual token point',['Faderan back Cache continuation; front Acknowledgments'],['Q39'])
unit('Paradise Converter any-climate cost, two points, Trade-once and destination',['Faderan back Paradise Converter'],['Q40'])
unit('Star’s Ruin one-time current bonus reward; terminology resolved by actual card',['Faderan back; original printed66/396'],['Q41'])
unit('Gift first trade beneficiaries, repeat-trade zero, Faderan-first and no automatic return',['Faderan back Gift complete cross-column paragraph; printed59/396'],['Q42'])
unit('Nalgorian Grindstone preexisting point payment/inability and simultaneous production',['Faderan back Grindstone; printed65/396'],['Q43'])
unit('Relic Detector additional any-climate/three-green converter may coexist with deck; nontrade exception',['Faderan back Relic Detector; printed62/396'],['Q14','Q62'])
unit('Transmutive Decomposer may not use freshly produced ships',['Faderan back Transmutive Decomposer; printed64/396'],['Q06'],'Explicit no-chaining restatement; ordinary printed entry/production values use card-output procedure rather than an all-card memorization question.')
unit('Im’dril support matching, splitting, combining and cross-species loans',['Im’dril front Fleet Support with full diagram and continuation'],['Q15'])
unit('Im’dril fleet discovery/starred start and no ordinary colony support',['Im’dril front Fleets/No Colonies; Faderan support exception'],['Q21','Q37','Q44'])
unit('Kjas split only at own opportunity, near-even halves, reinsert rank, no re-split, per-half buy/pass and updated count',['Kjas front complete Military Might'],['Q16','Q53'])
unit('Kjas counts twice only colony setup; starts two colonies',['Kjas front Expansionist; Booklet pp3–4'],['Q21','Q22'])
unit('Kjas three territory tiles, card status, top entry, bottom upgrade, Trade and loan',['Kjas front Territory Tiles and illustrated two-converter tile'],['Q45'])
unit('Kt fixed starting card pairs, independent upgrades and pair loans',['Kt front Nonlinear Thinking and pair diagram'],['Q17'])
unit('Kt nullspace entry has no extra output, permanent transfer, consumed removed not deck',['Kt front Nullspace Drive'],['Q17','Q64'])
unit('Kt unlimited colonies, always wins colony ties, normal research count then infinity tiebreak',['Kt front Boundless Expansion/Dangerously Fast'],['Q46'])
unit('Unity gray-size substitution, mixed inputs including gray and Zeth immunity',['Unity front Flexible Output/Input'],['Q18','Q65'])
unit('Unity any-climate entry/upgrade, one support and four out-of-play computer worlds',['Unity front Flexible Colonization/Computer Worlds'],['Q47'])
unit('Yengii private inventions, incoming shared tech, separate splay, reduced bonus, invented cards not counted as research teams',['Yengii front Secretive and continuation'],['Q19','Q48'])
unit('Yengii licensed own matching card permanent/same Trade and cannot restore spent card',['Yengii front Licensing'],['Q19'])
unit('Zeth Envoys output to same recipient with token, cannot refuse gift, stash trade-only and no token circulation',['Zeth front Envoys'],['Q49'])
unit('Zeth last-of-turn red converters, one target each/no twice at one, shortage,size not color, envoy discount not consumed,wild immunity',['Zeth front complete Theft; direct designer final exception'],['Q20','Q50','Q61'])
unit('Zeth protection from actual trade versus gifts and explicit donation-trade acceptance/refusal',['Zeth front complete Protection Racket'],['Q20','Q54'])
accept=[{'id':q['id'],'wording':q['question'],'novelty':km[q['id']]['novelty'],'source_references':km[q['id']]['source_references']} for q in qs[20:]]
reject=[
 {'candidate':'Another ordinary colony tie with changed player names/counts','decision':'reject','reason':'Same fewer-relevant-cards then higher-species priority already asked by Q08; original candidate removed before first expanded freeze.'},
 {'candidate':'Different seven/eight/nine Acknowledgment counts for Cache entry','decision':'reject','reason':'Same ceiling-divide-by-three branch as Q38, cosmetic numeric change.'},
 {'candidate':'Different five/even-sized Kjas split example','decision':'reject','reason':'Near-even division/rank and updated-count branches already asked in Q16 and per-half legality Q53.'},
 {'candidate':'Different converter funded by same-Economy resource/ship output, including Transmutive Decomposer','decision':'reject','reason':'Q06 asks no same-Economy output chaining; naming another ordinary converter introduces no new timing exception. Grindstone Q43 separately asks point cost and zero-point inability.'},
 {'candidate':'Other plain relic entry/output quantities','decision':'reject','reason':'Printed entry/converter outputs follow already-covered entry/production procedure; changed colors/counts are not independent novelty. All eight reverse-sheet special procedures and Detector nontrade exception are covered.'},
 {'candidate':'Final Envoys donation resources rather than another donation output','decision':'reject','reason':'Final retention in Q10 applies to all generated donation goods; Envoys recipient bundling in Q49 adds no source-defined contrary final exception. No unsourced last-token ruling used.'},
 {'candidate':'Another small/ship final scoring example after mixed remainder Q55','decision':'reject','reason':'Same combining group rule; number substitution not another branch.'},
 {'candidate':'Precise-resource fractions, timed Trade, handicapping, 2020 Remastered or expansion effects','decision':'reject','reason':'Explicitly excluded scope; no core novelty credit.'},
 {'candidate':'Hypothetical simultaneous impossible promises or nonexistent reduced-cost/relic effects absent from assigned core sources','decision':'reject','reason':'No positive source-supported distinct branch; do not invent a rule for speculative setup.'}
]
ledger={'game':'Sidereal Confluence','benchmark_version':'expanded-v2','question_count':len(qs),'source_scope':'Original2017 booklet plus all9 original species sheets, accepted original printed phase/relic components and labeled contemporaneous primary designer clarifications; no Remastered/expansion/optional variant','coverage_standard':'Only actual asked clauses/required facts count; contextual key background alone does not count. Accept new rule/outcome branch/consequential timing/priority/exception; reject cosmetic and mechanical recombinations.','core_procedural_units':units,'accepted_questions':accept,'rejection_ledger':reject,'passes':[{'pass':1,'focus':'Complete booklet setup, general Trade/Economy/Confluence, donations, bid and scoring procedures against seed','new_questions':'Part of Q21–Q66; see per-question acceptance records','status':'additions accepted'},{'pass':2,'focus':'All9 species, all8 reverse relic procedures, component/source recovery and final designer clarifications; explicitly ask prior context atoms','new_questions':'Remainder of Q21–Q66','status':'additions accepted'},{'pass':3,'focus':'Ownership differences between alternative upgrade routes on loaned cards','new_questions':['Q67'],'status':'one addition; reset stopping check'},{'pass':4,'focus':'Revisit every mapped booklet/component procedural group; vary resources, bid magnitudes, order, size, scarcity and actor','new_questions':[],'accepted_count':0,'reason':'Only repeats of covered outcomes or excluded/unsupported candidates remained; rejected cases recorded.'},{'pass':5,'focus':'Revisit all9 species and final-turn interactions, priority, timing, gifting, ownership, count changes and specific exceptions','new_questions':[],'accepted_count':0,'reason':'No new source-defined branch beyond all mapped actual questions; existing general rules cover mechanical restatements.'}],'coverage_stopping_rule':{'all_core_procedural_groups_mapped':True,'consecutive_zero_addition_passes':2,'fresh_independent_challenge':'pending','working_saturation_only':True},'uncovered_essential_source_gaps':[],'scope_limits':['Not every ordinary converter’s printed numeric input/output is a separate question; such quantities remain read from physical cards.','Strategy, fiction, physical component-count trivia and optional variants are not core procedural coverage.','This is a known fixed-set tool-assisted regression, not held-out accuracy or proof that every conceivable scenario exists in the bank.']}
(ROOT/'coverage-ledger.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n')
text='# Source procedural coverage and novelty ledger\n\n'+str(len(qs))+' questions; '+str(len(units))+' source procedure groups. Two sequential zero-addition passes follow the final accepted ownership case. Independent challenge pending.\n\n'
for u in units:text+='- '+u['source_procedural_unit']+': '+', '.join(u['questions'])+' ('+'; '.join(u['source_references'])+').\n'
text+='\nRejected candidates:\n\n'
for e in reject:text+='- '+e['candidate']+': '+e['reason']+'\n'
(ROOT/'coverage-map.md').write_text(text)
print('Mapped',len(units),'procedural groups; accepted',len(accept),'additions; two zero-addition passes recorded')
