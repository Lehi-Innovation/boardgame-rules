import json, hashlib
from pathlib import Path
from collections import Counter
P=Path('/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/ark-nova/2026-11-04-batch-231507')
O=P/'expanded-iteration-02'
PROMPT='''Fresh independent grader for ArkNova94-answer readerA. ReadONLY complete files under QAroot /home/jonny/projects/boardgame-rules/docs/quality/summary-qa/ark-nova/2026-11-04-batch-231507/: expanded-iteration-02/{reader-a.json,summary-snapshot.md,questions.json}; benchmark-v2/{answer-key.json,material-requested-facts.json}; grading-request-scope-01.json. No otherreader, priorgrades/reports/history/rawsources/canonical/browsing/contact. The scopeindex contains only neutralrequired/contextclassification, no earlieranswers/grades. EveryACTUALLYREQUESTEDpartmustbeindividuallyresolved; actualquestioncontrolsscope. Fixedkeysourcefacts unchanged; extra keycontextnotanotherdemand. Ifscopeindexseemsinconsistentwithliteralquestion, explicitlyflagratherthansilentlyoverrule. Gradeall94answersincludingvolunteeredrulings: correctcompleteallactualparts,nocontradiction/no unsupportedsourcecorrectguess;partialmissing/unresolved/ambiguousrequestedpart;incorrectmaterialfalseorcontradictoryruleinclvolunteered. Noborrowingbetweenanswers; meaningfuldefined-abilityshorthandallowedwhenthequestionasksitsinteractionratherthanentiredefinition. Reader'ssupportlabelnotverdict, butexplicitlyunresolvedactualpartcannotpass. Source-correctfactwithoutfrozen-summarysupportisunsupportedguessandnonpassing. Readallinputscompletelyinboundedrecoveredchunks,notjustsearches/hashes. WriteONLY expanded-iteration-02/independent-grade-a.json andownnotesnamedindependent-grade-a-*; noinputedits. Saveexactintendedprompt,inputhashes,fullreadproof,94perquestionjudgmentsinquestionorder: id,requestedparts(part,observedquote,summarysupportquote/line,status),overallgrade correct|partial|incorrect,unsupported_guessbool,reason,andcontext/volunteeredrulingcheck. Counts+nonpassingIDs+borderline/key/scopeconcerns. No assumedPASS,no keywordgrading,no relaxingactualparts.'''
files=['expanded-iteration-02/reader-a.json','expanded-iteration-02/summary-snapshot.md','expanded-iteration-02/questions.json','benchmark-v2/answer-key.json','benchmark-v2/material-requested-facts.json','grading-request-scope-01.json']
raw={f:(P/f).read_bytes() for f in files}
ds={f:json.loads(v) for f,v in raw.items() if f.endswith('.json')}
reader={x['id']:x for x in ds[files[0]]['answers']}
questions=ds[files[2]]['questions']; scope=ds[files[5]]['questions']
lines=raw[files[1]].decode().splitlines()
# These explicit, manually reviewed plans are in question order and scope-part order.
# r = resolved; m = missing; a = ambiguous/unresolved; c = contradictory;
# x = explicitly disputed as context rather than an actually requested part.
# Numbers are exact snapshot line numbers. Multiple lines use '+'.
plans={
'Q01':'r81 r80 r83 r82 r76 r76 r78',
'Q02':'r69 r70 r70 r70 r84',
'Q03':'r104 r104 r104 r106 m106 r106 r106 r108',
'Q04':'r102 r237 r237 r237 r237',
'Q05':'r112 r112 r112 r124',
'Q06':'r147 r147 r147 r148 r148 r148 r148 r152 r115',
'Q07':'c150+152 r152 r152 r152',
'Q08':'r169 r171 r171 r169 r170 r170 r170 r170 r170 r170',
'Q09':'r169 r171 r168 r171 r171 r259',
'Q10':'r106 r106 r171+201 r108 r200',
'Q11':'r196 r197 r197 r188 r188 r198 r198 r189+198 r198 r200 r201',
'Q12':'r202 r202 r202 r202 r202 r202',
'Q13':'r210 r210 r210 r213 r212 r212 r212',
'Q14':'r220+221+222+223 r218 r228 r218 r218 r218',
'Q15':'r221+222 r221+222 r221+222 r221+222 r221 r221 r88 r96',
'Q16':'r223 r223+228 r223 m223 r223 r223 r224 r224 r225 r225 r225',
'Q17':'r226 r226 r226 r226 r226 r226 r226 r226',
'Q18':'r231 r232 r232 r232 r231 r232',
'Q19':'r115 r116 r117 m117 r118 r120+121+122 r121 r121 r123 r123 r124',
'Q20':'r242 r243 r244 r244 r246 r246 r246 r246 r249 r250 r251 r251',
'Q21':'r64 r64 r64 a271',
'Q22':'r75 r75 r75',
'Q23':'r79 r269 r269',
'Q24':'r110 r110 r110 r110 r110',
'Q25':'r177 r177 r177 r177 r177 r180',
'Q28':'r206 r275 r206 r206',
'Q29':'r228 r228 r228 r228 r228 r228 r228 r228 r228 r228',
'Q30':'r290 r290 r290 r290 r290 r290 r290',
'Q31':'r290 r290 r290 r290',
'Q32':'r226 r226 r227 r227',
'Q33':'r294 r294 r294',
'Q34':'r292 r292 r292 r292 r292',
'Q35':'r296 r296 r296 r296 r296 r296 r296',
'Q36':'r302 r302 r302 r302',
'Q37':'r304 r304 r304 r304 r304',
'Q38':'r303 r303 r303 r303 r303',
'Q39':'r322 r322 r322 r322',
'Q40':'r324 r324 r324 r324 r324 r324',
'Q41':'r324 r324 r324',
'Q42':'r305 r305 r305',
'Q43':'r306 r306 r306 r306 r306 r306 r306',
'Q44':'r307 r307 r307',
'Q45':'r310',
'Q46':'r326 r326 r326 r326 r326 r326 r326',
'Q49':'r320 r320 r320 r320 r320 r320 r320 r320',
'Q50':'r320 r320 r320',
'Q51':'r318 r318 r318 r318 r318',
'Q52':'r317 r317 r317',
'Q53':'r328 r328 r328',
'Q54':'r328 r328 r328 r328 r328 r328',
'Q55':'r315 r315 r315 r314',
'Q56':'r316 r316 r316 r316',
'Q57':'r314 r314',
'Q58':'r311 r311 r311 r311 r311',
'Q59':'r325 r325 r325 c325 r325 r325',
'Q63':'r339 r339 r339',
'Q66':'r342 r342',
'Q67':'r343 r343 r343',
'Q68':'r344 r344 r344',
'Q70':'r346 r346 r346 r346',
'Q72':'r348 r348 r348',
'Q75':'r351 r351 r351 r351 r351',
'Q77':'r353 r353 r353 r353 r353 r353',
'Q78':'r354 r354 r354 r354 r354 r354',
'Q80':'r356 r356 r356 r356',
'Q82':'r358 r358 r358 r358 r358',
'Q83':'r359 r359 r359 r359',
'Q85':'r361 r361 r361 r361 r361',
'Q86':'r362 r362 r362 r362 r362 r362',
'Q90':'r367 r367 r367 r367 r367+292',
'Q95':'r371+296 r371+333',
'Q96':'r372 r372+333 r372',
'Q98':'r374 r374 r374',
'Q99':'r375 r375 r375 r375 r375',
'Q100':'r376 r376 r376 r376',
'Q102':'r378 r378 r378 r378 r378 r378',
'Q104':'r380 r380 r380 r380 r380',
'Q106':'r382 r382 r382',
'Q107':'r383 r383 r383 r383+396',
'Q112':'r391 r391 r391',
'Q113':'r392 r392 r392 r392',
'Q114':'r393 r393 r393 r393 r393',
'Q115':'r394 r394 r394 r394 r394 r394',
'Q116':'r395 r395 r395 r395 r395 r395',
'Q119':'r398 r398 r398 r398 r398 r398',
'Q123':'r406 r406 r406',
'Q124':'r408 r408',
'Q125':'r325 r326 r326 r328 a328 r328 m328 r324 r324 r322',
'Q127':'r407 r407 r407 r402',
'Q133':'r305 r305 r305',
'Q134':'r152 r152 r152',
'Q137':'r156 r156 r156 x156',
'Q139':'r244 r244',
'Q140':'r72 r31 r31 r31 r108+200+320'
}
# Q125 also lacks the self-target clause within scope part 2.
plans['Q125']='r325 m326 r326 r328 a328 r328 m328 r324 r324 r322'
reasons={
'Q01':'Resolves starting money, workers, all draw/keep counts, Action sides/order and staggered appeal. Hidden-information context was not demanded.',
'Q02':'Gives the correct base-project counts, two-player-only level/donation blocking and post-hand-selection display reveal.',
'Q03':'The movement algorithm correctly leaves slot 5 alone, and strength, gain timing, cap and after-finishing timing are answered. It never states that spent X-tokens return to supply, included in the scope index as part of their use.',
'Q04':'Rejects a zero-effect regular action and gives the selected-card alternative, movement, one-token gain and five-token exclusion.',
'Q05':'Resolves excess movement, one-token trigger reward, completion of the current turn and next clockwise player. The volunteered reset is correct.',
'Q06':'Distinguishes both draw/snap choices, both thresholds, reputation exception, two-space Break movement and the two requested timing rules.',
'Q07':'The core range rule, Cards-II gate, overflow and inspection answer are correct. However, the volunteered numerical mapping reverses folders and reputation values: folders 1–6 correspond to reputation bands, not spaces 1–6 to folders 1/2–3/etc. This materially misstates display access.',
'Q08':'Resolves both building limits, cost, first/later placement, excluded and restricted spaces, kiosk distance and pavilion appeal.',
'Q09':'Identifies available buildings and special-enclosure caps, excludes unique buildings from Build and gives immediate seven-appeal completion including other effects.',
'Q10':'Correctly permits earlier resources to fund later items, requires payment before own benefits, and differentiates immediate, after-finishing and simultaneous timing.',
'Q11':'The ordered check/pay/house/resolve procedure puts full payment before own effects; per-icon discount includes a double icon without needing a separate arithmetic example. Both housing systems, terrain and effect timing are resolved.',
'Q12':'Gives mixed hand/display play, reputation and folder cost, optional initial reputation at five-plus, end-turn refill and upgrade-conditioned animals.',
'Q13':'Covers construction-only relocation, individual eligibility/capacity/terrain, supply-token marking and the full smallest-enclosure fallback.',
'Q14':'All four strengths, side limits, own-worker repeat escalation and irrelevance of opposing workers are correct.',
'Q15':'All requested acquisition, placement, bonus, duplicate and hand/partner limits are answered. The extra claim that university reputation icons count as zoo icons is false: printed reputation is an acquisition award, not a countable zoo icon.',
'Q16':'The entry/support/bonus/overflow procedure is otherwise correct, but “player-count limit” does not state that the maximum above-board project count equals two/three/four for the corresponding player count. The numeric rule remains underspecified.',
'Q17':'The answer expressly defines bands by the printed standard requirement, excluding actual housing/capacity as the determinant; gives losses/retentions and mandatory special-token priority plus all standard fallbacks.',
'Q18':'Both level budgets, card sources/costs, sequential timing and full-strength money despite the truncated Break movement are resolved.',
'Q19':'Step order, hand limit, kiosk neighbors and income order/refill are correct. “Restock partner zoos/universities” omits the required one-per-kind quantity and exclusion of kinds owned by every player.',
'Q20':'Resolves the milestones, both end-check timings and final-turn sets, cap, VP formula and both tie outcomes. Removal of a selected Bonus token is unrequested context.',
'Q21':'Bonus-tile setup is complete and the answer mentions substitution. It then expressly leaves the actual supplied-quantity limitation unresolved; the correct substitute clause does not cancel that uncertainty.',
'Q22':'Both advanced selection methods and the fixed empty size-three enclosure and already-built kiosk are correct.',
'Q23':'Correct left-edge support-token start, lowest-reserve-first hiring and potential last-worker conservation reward; added Map-A worker context is supported.',
'Q24':'Correct flip, unchanged slot, next-action capability, immediate upgraded conditions and impossibility of upgrading all five.',
'Q25':'Every strength-one-through-five draw/discard pair and both permissible discard sources are correct.',
'Q28':'Names all seven categories and treats bear and Petting Zoo as categories without replacing a bear’s other category.',
'Q29':'All donation conditions, exact cost ladder, blocked-space handling, lowest-visible selection, supply-token source, reward and repeatable no-token twelve are resolved.',
'Q30':'Resolves icon sources/exclusions, self-counting, doubled counting/triggers and card-over-general precedence.',
'Q31':'Correctly counts distinct adjacent terrain hexes and excludes remote connected hexes and decoration.',
'Q32':'Correctly distinguishes the release project play bonus from later support and permits any available Breeding Program level with its shared condition.',
'Q33':'Correct fulfillment versus threshold rewards, highest qualifying threshold and volunteered left/right syntax.',
'Q34':'All five definitions agree with the frozen summary.',
'Q35':'Resolves mandatory legal placement, inability to play if it cannot fit, payment, colored-face orientation/rotation, ordinary terrain rules and non-enclosure/non-terrain status.',
'Q36':'Resolves post-Animals timing, own Action-card movement and named-action versus Determination access to the X-token alternative.',
'Q37':'Identifies the unused base deck, chosen/named retrieval, already-in-play failure and later immediate support above the board. “Into hand” is extra destination detail beyond the literal where-from/where-played question; flagged explicitly as a scope concern.',
'Q38':'Both after-Animals timings, legal destination slots and card shifts are correct.',
'Q39':'All four abilities share the five-appeal floor; appeal/ability ordering and the multiplayer use of alternate text are resolved.',
'Q40':'Correct target-slot placement, nonstacking, minus-two strength for each multiplied execution, X-token recovery and both removal timings.',
'Q41':'Correctly treats low-slot regular actions as requiring enough boost or waiting, and permits the marked card’s X-token alternative. Removal context is supported.',
'Q42':'Correctly allows option changes after each selection and immediate shifting/refill into folder six.',
'Q43':'Host qualification/reuse/type, ordinary housing without a host, later non-flock exclusion and absence of historical proof on release are resolved. “Normal release procedure” is meaningful defined-procedure shorthand for the release interaction.',
'Q44':'Lowest reserve worker becomes immediately available on the notepad, map reward applies if applicable, and no reserves means no effect.',
'Q45':'With no revealed Animal, all revealed cards are discarded and none is taken. Added normal Hunter handling is supported.',
'Q46':'Covers ties/self-target, copied side, own tokens, movement and all three types of card tokens correctly.',
'Q49':'Correct placement, same-base sequential repetitions, one-execution boosts, deferred after-finishing effects, delayed break and used/unused token return.',
'Q50':'Two tokens grant up to three executions; multiplied X-token alternatives obey the cap and cannot mix with a regular execution.',
'Q51':'Peacocking bypasses only the enclosure’s Build-side availability; legal placement, ownership and restricted spaces persist. Posturing retains kiosk rules and sequential placement.',
'Q52':'Correct three/six/nine appeal, at most three in one Petting Zoo and small-animal classification.',
'Q53':'Correct tie choice, positive-conservation requirement and no-effect self-target. Added Pilfering-two duplicate-target handling is supported.',
'Q54':'Resolves target choice, random hand-card source/exclusion, every card/money fallback and sequential fresh choices.',
'Q55':'Correct loss of function, tucked-card discard on release with appeal retained, and Sunbathing discard destination; extra amounts are supported.',
'Q56':'Resolves additional scoring card, expanded discard choice before ten, all remaining cards scored and per-card cap.',
'Q57':'Correct face-down shuffle, random selection and return face up, with supported illustrated selection details.',
'Q58':'Correct display-only Snapping, Sponsor-only Magnet, reputation exceptions, no-Sponsor result and normal end-turn refill.',
'Q59':'It correctly says using a marked card avoids all Venom fees, but then unconditionally says any remaining token at turn end requires two money. That contradicts the required no-token-removed condition and its own earlier exemption.',
'Q63':'All university money tiers, strength-four support and three-university final conservation are correct.',
'Q66':'Correct prior-support count via missing left-edge tokens and one conservation each break.',
'Q67':'“Each pair of different continent/animal-category icons” limits the count to distinct eligible types and complete pairs; both owner and other-player rewards are correct.',
'Q68':'All three effects are correct. In this answer “its owner” refers to the Science Library, whose name is the subject, and the summary explicitly supplies that ownership rule.',
'Q70':'Correct immediate appeal, own-icon free kiosk with ordinary placement/spacing, and five-kiosk final conservation.',
'Q72':'Correct immediate appeal and own new-icon tuck of one hand card for two appeal; tucked cards have no remaining function.',
'Q75':'Correct two supply tokens, one-icon substitution cap, below-board eligibility/exclusion and final support-count test.',
'Q77':'Correct same-action duplicate, no strength cost, normal money/placement, one extra overall, special limit and final full-map appeal.',
'Q78':'Resolves immediate money, terrain coverage/waiver, retained printed icons, covered-terrain effects and capped pair scoring.',
'Q80':'Correct border bonus trigger, any uncovered bonus, repeated choices and final border coverage; resolution-order context is supported.',
'Q82':'Correct immediate token, added release conservation, repeat supports with different animals, per-project per-action cap and separate support counting.',
'Q83':'Correct immediate token, four immunities, redirection ignoring own counters and final five-continent condition.',
'Q85':'Correct permanent marked choice, search/discard, chosen-type bonuses, unchosen-type ban and size-three exception. Numerical definitions are context, not another question.',
'Q86':'Correct immediate money, only-small prerequisite, optional normal-cost extra hand play and display take regardless of reputation even if extra play declined.',
'Q90':'Resolves immediate water-icon appeal, per-hex rather than per-building income, no multiplier for several water neighbors and the final none-isolated test. “Connected” and “isolated” are the summary’s defined terms.',
'Q95':'Identifies the unique building and its placement on Sponsor play, and correct two-draw/keep-one/discard-one bird trigger. Normal placement is a general default rather than a separately asked exception; flagged as scope detail.',
'Q96':'Correct water adjacency, optional up-to-two hand-card sales at four each and discard destination. Ordinary own-zoo scope applies without an “any zoo” exception.',
'Q98':'Correct current-total Hunter amount, two sequential triggers for a double icon and counting the new icons each time. The question asks the Hunter interaction, not a full Hunter definition or building placement.',
'Q99':'Correct building plus three supply tokens, herbivore trigger, optional hand Sponsor for level money with conditions, self-trigger and three total uses.',
'Q100':'Correct both immediate track rewards, two-border-space placement, card alternatives and choice of simultaneous reward order.',
'Q102':'All Side Entrance placement, later adjacency, income exclusions/kiosk adjacency and full-map scoring parts are resolved.',
'Q104':'Correct connected-uncovered building border count, terrain exclusion, inclusion of restricted spaces and separate contiguous-group scoring by six.',
'Q106':'Correct different eligible icons, research exclusion, novelty rewards and only one novelty reward for a double identical new icon.',
'Q107':'Correct free size-five building, large-animal left-side waiver, terrain exclusion and two-condition stacking with Research Institute.',
'Q112':'Correct category-by-category comparison against the right neighbor, empty-category case and four-point cap. Extra enumeration of category/icon sources is not demanded.',
'Q113':'Correct tower-hex adjacency, standard-only bonus, repeat two appeal after release/reoccupation and nonbuilding kiosk status.',
'Q114':'Correct Outdoor Area adjacency, postplacement plus-two for all purposes, mandatory release/relocation use, standard-only effect and nonbuilding status.',
'Q115':'Correct activation, optional first-building start, once-own-turn timing range, excluded turns/breaks and nonbuilding status.',
'Q116':'Correct covered-hex income including multihex/empty enclosures, nonbuilding status and one-of-two free special bonus before Build II with remaining restrictions.',
'Q119':'Correct ordinary H coverage/search/discard, no Archaeologist, all-three level reduction and retained partner/map upgrade restrictions.',
'Q123':'Correct level payment/conditions, hand-only source even with Sponsors II and no Action-card movement.',
'Q124':'Correct 113/41 caps with lost excess; volunteered reputation overflow is also supported.',
'Q125':'Most target comparison is correct, but Hypnosis and Pilfering self-target outcomes are omitted. “Separately targets” does not individually resolve whether the same zoo is pilfered twice when it leads both tracks.',
'Q127':'All four condition types are correct, including distinct Animal/Sponsor partner requirements and terrain exclusion for the waiver.',
'Q133':'Correct two alternatives and up-to-two selections; added choice-by-choice and immediate-refill timing is supported.',
'Q134':'Correct downward gap filling, order preservation and deck refill. The support label is not the verdict: its caveat denies a separate reordering choice while explicitly resolving the actual order-preservation question.',
'Q137':'Correct empty face and immediate once-per-covered-icon reward, with no repeat on occupation. The scope index adds inter-building sequencing beyond the literal question about a standard enclosure’s covered spaces; that disputed context is recorded rather than silently required.',
'Q139':'Correct underneath-pile destination and face-down orientation.',
'Q140':'Correct random starter, clockwise no-round sequence and one ordinary action with additional effects following their respective timing.'
}
context_notes={
'Q01':'Final Scoring secrecy is omitted, but explicitly context only.',
'Q03':'Generic movement resolves original slots 1–3 and unchanged slot 5 without a numbered worked example. The spent-token return omission is not supplied from another answer.',
'Q05':'Reset-by-player-count is volunteered and matches line 112/124; the ordinary cap is not independently requested.',
'Q06':'No extra numerical hand limit or no-money sentence is demanded by the question’s timing request.',
'Q07':'Volunteered range-band mapping is materially reversed; key context about immediate track bonuses is not demanded.',
'Q09':'All volunteered footprints and global four-of-each special supply match lines 162–168.',
'Q11':'Discount is three per matching icon; six for two follows that explicit per-icon rule. Payment-before-own-effects follows the explicitly ordered procedure.',
'Q15':'False volunteered ruling: “University research/reputation icons and partner continent icons count as zoo icons.” Research and continent icons count; acquisition reputation does not become a zoo icon. Break-restock context is otherwise supported.',
'Q16':'Volunteered below-board permanence and retained map bonuses are supported; exact player-count cap is not supplied by the vague limit reference.',
'Q17':'Extra play-only reputation clause agrees with line 226; no need to repeat every release fact in the separate flock answer.',
'Q19':'No borrowing of Q15’s correct restock exception is permitted.',
'Q20':'Face-down discard destination and money-still-available context are supported.',
'Q21':'The support label itself does not fail the answer. Its explicit final clause leaves the actual quantity-limit issue unresolved, unlike Q134’s fully answered order question.',
'Q22':'Map-A recommendation and printed-kiosk reminder match line 75.',
'Q23':'Map-A third-partner worker context matches line 86.',
'Q24':'Four-opportunity explanation is correct; naming the four sources is not separately requested.',
'Q37':'Returning the searched deck is correct context. The literal question asks source and later play location, not an intermediate hand-destination instruction.',
'Q40':'Volunteered target-track selection agrees with line 324.',
'Q41':'Removal after use follows line 324. No separate restatement of ordinary X holding cap is demanded.',
'Q43':'Defined “normal release procedure” is sufficient for the requested flock interaction; it is not permission to ignore the special-token priority.',
'Q45':'The added ordinary Hunter definition agrees with line 310.',
'Q46':'Added legal target slots and other-card own-upgrade checks agree with lines 326–327.',
'Q49':'The question presupposes the two-action use; wording is read as describing that use, not forcing every token to be spent. Different options are context only.',
'Q53':'Added Pilfering-one/two and twice-from-same-zoo rule are source-supported.',
'Q55':'Added Pouch two-appeal and Sunbathing four-money quantities match lines 314–315.',
'Q57':'Scavenging-three illustration matches line 314.',
'Q59':'Contradictory fee condition is material even though the exception appears earlier. Volunteered alternative-X and inability-to-pay rules are supported.',
'Q67':'No research or repeated-type count is licensed by the answer’s explicit different continent/category qualification.',
'Q68':'The recurring payer/recipient pronoun has a clear card antecedent; no outside information is needed.',
'Q78':'Added full-map exclusion of terrain matches line 354.',
'Q80':'Added owner-chosen resolution order matches line 356.',
'Q85':'Small/large numerical definitions are explicitly listed as context by the index and not required again here.',
'Q86':'“Only small animals” excludes size-three as well as large; the added mixed-small/large rejection does not weaken that positive prerequisite.',
'Q90':'“Connected” is the game-defined adjacency-to-covered-space term, not a claim that water must form one continuous region; “none isolated” reinforces that term.',
'Q95':'The answer does not claim any special placement exemption or “any zoo” trigger. Own-zoo/normal-placement are ordinary defaults in lines 296/333.',
'Q96':'Own-zoo trigger is the default in line 333; no volunteered all-player trigger.',
'Q98':'Do not require rock placement or re-expansion of Hunter’s draw/selection/discard definition; those are context for this interaction question.',
'Q100':'General simultaneous-order sentence permits reputation before display selection; it need not name a worked example.',
'Q104':'“Per group of six ... evaluating each group separately” is interpreted as complete sixes within each contiguous group, not merging remainders across groups.',
'Q107':'Research Institute is used as its defined active ability; the question asks stacking, not its activation definition.',
'Q112':'Do not require a new animal-category list or separate Sponsor enumeration in this comparison question.',
'Q113':'Nonbuilding answer specifically resolves kiosk consequences asked by index; no extra building-based benefit is claimed.',
'Q119':'Sponsor level reduction is read as the printed effect on play; no unsupported retroactive payment claim is made.',
'Q124':'Volunteered reputation-overflow rule matches line 152.',
'Q125':'No borrowing of Q46/Q53 self-target clauses or Q53’s explicit same-target-twice clause is allowed.',
'Q127':'Extra reminder-not-track-cap and terrain-waiver exclusion match lines 402/407.',
'Q133':'Immediate refill and choosing anew are supported by line 305.',
'Q134':'“Does not describe a separate reordering choice” is consistent with mandatory preservation and does not leave a requested part unresolved. Extra Digging timing is supported.',
'Q137':'Explicit scope-index disagreement: multi-building sequencing is source-correct but not an additional demand in a singular-enclosure question already answered as immediately on coverage.',
'Q140':'Added Action/Determination and Multiplier exceptions match lines 302/320.'
}
# Explicit individual deficiencies, using exact observed fragments of this answer only.
overrides={
('Q03',5):('each X-token spent adds one strength','Missing the spent token’s return to supply.'),
('Q07',1):('spaces 1–6 correspond to folders 1, 2–3, 4–6, 7–9, 10–12 and 13–15','The extra mapping swaps the labels of the folder numbers and reputation bands.'),
('Q16',4):('if over the player-count limit','Does not resolve that the cap is numerically equal to two/three/four players.'),
('Q19',4):('recall workers and restock partner zoos/universities','Missing one per kind, skip all-owned kinds, and do not duplicate available tiles.'),
('Q21',4):('it does not state a general rule that every component is unlimited or must be available in supplied quantity','Explicitly leaves the quantity-limit issue unanswered despite mentioning suitable substitutes.'),
('Q59',4):('If any Venom token remains at turn end, pay 2 money','Unqualified fee contradicts the no-token-removed condition and the earlier all-fees exemption.'),
('Q125',2):('Hypnosis chooses an affected player among those tied for highest appeal and targets only a card in slot 1, 2 or 3.','No self-target no-effect outcome.'),
('Q125',5):('Pilfering 2 separately targets the highest-appeal zoo and the most-conservation zoo','The duplicate-leader case is not explicitly settled; separate targeting is ambiguous about two pilferings on the same zoo.'),
('Q125',7):('Pilfering 1 targets the highest-appeal zoo','No Pilfering self-target no-effect outcome.'),
('Q137',4):('', 'Disputed scope-index addition: the literal question does not ask the sequence of multiple buildings; immediate once-on-coverage timing is already resolved.')
}
# These are semantic review decisions, not inferred from support labels or keywords.
explicit_overall={q['id']:'correct' for q in questions}
for qid in ['Q03','Q16','Q19','Q21','Q125']: explicit_overall[qid]='partial'
for qid in ['Q07','Q15','Q59']: explicit_overall[qid]='incorrect'
assert len(plans)==len(reasons)==len(explicit_overall)==94
statusnames={'r':'resolved','m':'missing','a':'ambiguous_or_explicitly_unresolved','c':'contradictory','x':'context_not_actually_requested_scope_dispute'}
judgments=[]
for q in questions:
 qid=q['id']; answer=reader[qid]['answer']; parts=scope[qid]['requested_parts']; tokens=plans[qid].split()
 assert len(parts)==len(tokens),(qid,len(parts),len(tokens))
 rows=[]
 for i,(part,tok) in enumerate(zip(parts,tokens),1):
  ns=[int(n) for n in tok[1:].split('+')]
  assert all(lines[n-1].strip() for n in ns),(qid,ns)
  obs,note=overrides.get((qid,i),(answer,'Individually reviewed against the literal question, answer and cited frozen-summary text.'))
  assert obs in answer,(qid,i,obs)
  rows.append({'part':part,'observedquote':obs,'observedquote_scope':'current answer only; complete answer quoted where no narrower deficiency excerpt is needed','summarysupportquote':[{'line':n,'quote':lines[n-1]} for n in ns],'status':statusnames[tok[0]],'note':note})
 check={'status':'no_material_false_or_unsupported_volunteered_ruling_found','note':context_notes.get(qid,'All volunteered content was reviewed against the cited summary rule; no additional contradictory ruling or source-correct unsupported guess found.'),'unrequested_key_context':scope[qid]['unrequested_context']}
 if qid in ['Q07','Q15','Q59']:
  check['status']='material_false_or_contradictory_ruling'
  extra_lines={'Q07':[150,152],'Q15':[90,92,93,94,96,222,290],'Q59':[325]}[qid]
  check['summarysupportquote']=[{'line':n,'quote':lines[n-1]} for n in extra_lines]
  check['observedquote']={'Q07':'spaces 1–6 correspond to folders 1, 2–3, 4–6, 7–9, 10–12 and 13–15','Q15':'University research/reputation icons and partner continent icons count as zoo icons.','Q59':'If any Venom token remains at turn end, pay 2 money'}[qid]
  assert check['observedquote'] in answer
 if qid in ['Q37','Q95','Q137']: check['scope_index_concern']=True
 judgments.append({'id':qid,'question':q['question'],'requestedparts':rows,'overallgrade':explicit_overall[qid],'unsupported_guess':False,'reason':reasons[qid],'context_volunteered_ruling_check':check})
counts=dict(Counter(j['overallgrade'] for j in judgments))
chunks=[(0,12,'011a12'),(12,24,'a20fa0'),(24,36,'33f09b'),(36,48,'a0f274'),(48,60,'f48bfc'),(60,72,'b80496'),(72,84,'d236e7'),(84,94,'5c9069')]
proof=[]
for a,b,receipt in chunks:
 ids=[q['id'] for q in questions[a:b]]
 proof.append({'kind':'bounded complete JSON semantic-content read','question_positions_1_based':[a+1,b],'ids':ids,'tool_output_chunk_id':receipt,'files': [files[i] for i in [0,2,3,4,5]],'read_content':'Complete question, reader answer/support/evidence, key record including all extra fields, material facts record including all extra fields, and scope record; serialized without eliding values. All top-level non-record metadata was fully printed in the first chunk.','output_truncated':False})
for a,b,receipt in [(1,145,'6ce31c'),(146,275,'908545'),(276,350,'950ff1'),(351,426,'aa5b49')]:
 segment='\n'.join(lines[a-1:b])
 proof.append({'kind':'bounded complete summary text read','file':files[1],'inclusive_lines':[a,b],'tool_output_chunk_id':receipt,'line_span_sha256_utf8_without_final_newline':hashlib.sha256(segment.encode()).hexdigest(),'output_truncated':False})
concerns=[
 {'id':'Q03','type':'borderline_requested_scope','decision':'partial','detail':'The index specifically requires return of a spent X-token. The literal “what can X-tokens do” is less explicit about disposal, but the use procedure includes it; retained as required rather than silently relaxing the index. Movement need not separately enumerate slot 5 because the given algorithm excludes it.'},
 {'id':'Q07','type':'volunteered_error','decision':'incorrect','detail':'The numerically reversed mapping is substantive, even though the preceding generic range definition is right.'},
 {'id':'Q11','type':'semantic_completeness','decision':'correct','detail':'Per-icon discount resolves double-icon arithmetic and the ordered pay-before-resolve procedure resolves up-front cost; do not demand duplicate negative wording.'},
 {'id':'Q15','type':'volunteered_error','decision':'incorrect','detail':'Acquisition reputation is a track reward. Counting it as a zoo icon is a false extra rule, not merely omission.'},
 {'id':'Q16','type':'ambiguous_numeric_rule','decision':'partial','detail':'“Player-count limit” identifies a dependency but does not individually give the cap equal to the player count. No inference from other answers was used.'},
 {'id':'Q17','type':'semantic_completeness','decision':'correct','detail':'Explicit identification of printed standard size as the category determinant resolves actual tile/capacity exclusion without repeating a negative sentence.'},
 {'id':'Q21','type':'explicit_unresolved_part','decision':'partial','detail':'Correct substitute wording coexists with an express refusal to settle the actual quantity-limit question; cannot pass merely because the support label is ignored.'},
 {'id':'Q37','type':'scope_index_literal_question_mismatch','decision':'correct','detail':'Index embeds “into hand” in its first part. The literal question asks where cards come from and where later played, not their intermediate destination. Answer resolves the actual source and later destination. This is an explicit scope dispute, not a change to the factual key.'},
 {'id':'Q43','type':'defined_procedure_shorthand','decision':'correct','detail':'The question asks the flock/release interaction, so “normal release procedure” can refer to the defined release/fallback procedure. No details are borrowed from the reader’s Q17.'},
 {'id':'Q49','type':'optional_multiplier_wording','decision':'correct','detail':'The question asks how the two actions are resolved. The answer describes a chosen multiplied use; it does not clearly assert compulsory spending of every Multiplier.'},
 {'id':'Q59','type':'internal_material_contradiction','decision':'incorrect','detail':'The fee sentence lacks the otherwise/no-token-removed condition. Do not silently append the condition because an earlier sentence states the exemption.'},
 {'id':'Q68','type':'pronoun_resolution','decision':'correct','detail':'“Its owner” refers to the named Science Library subject; no explicit wrong player is assigned.'},
 {'id':'Q90','type':'defined_term_shorthand','decision':'correct','detail':'Connected/isolated are game terms defined in the same frozen summary; the answer uses both consistently, without claiming connected terrain regions suffice.'},
 {'id':'Q95','type':'scope_detail','decision':'correct','detail':'“Under normal rules” is an ordinary default for placing the named unique building rather than a separate placement-exception demand in this literal question. Answer requires placement and claims no exemption. Own-zoo is the Sponsor-reference default, not an all-player trigger.'},
 {'id':'Q98','type':'unrequested_key_context','decision':'correct','detail':'Question requests Hunter X interaction and duplicate icon behavior, not the entire Hunter definition or rock adjacency; index appropriately classifies those as context.'},
 {'id':'Q104','type':'semantic_completeness','decision':'correct','detail':'“Per group of six ... evaluating each group separately” means complete sixes within each contiguous group, not pooling remainders; no worked arithmetic example is requested.'},
 {'id':'Q125','type':'missing_cases','decision':'partial','detail':'Self-target outcomes are absent. Duplicate leader is ambiguous in the word “separately”; an explicit twice-from-same-zoo result appears elsewhere but was not borrowed.'},
 {'id':'Q134','type':'support_label_and_uncertainty','decision':'correct','detail':'Unlike Q21, all literal parts are explicitly resolved. A separate reordering choice is denied consistently with the mandatory keep-order rule. The reader’s partial label is not a grading verdict.'},
 {'id':'Q137','type':'scope_index_literal_question_mismatch','decision':'correct','detail':'Index requires a separate multi-building sequencing statement. Literal question asks about one standard enclosure’s face and when/how often its covered placement bonuses are gained. “Each ... immediately once when covered” resolves that actual request. Inter-building sequencing remains source-correct context, flagged explicitly rather than silently overriding the index.'}
]
result={
 'grader':'independent-grade-a','reader':'reader-a','intended_prompt_exact':PROMPT,
 'input_hashes':[{'path':str(P/f),'sha256':hashlib.sha256(v).hexdigest(),'bytes':len(v),'lines':len(v.splitlines())} for f,v in raw.items()],
 'fullreadproof':{'complete':True,'method':'All six permitted inputs read completely. Summary read verbatim in four recovered bounded ranges. All JSON keys and values read completely in eight paired bounded ranges, including all five files’ metadata. No raw sources, other reader, prior grade/report/history, canonical summary, browsing, or external contact used. Hashing was only provenance, not a substitute for reading.','chunks':proof},
 'rubric':{'actual_question_controls_scope':True,'source_key_unchanged':True,'no_cross_answer_borrowing':True,'labels_not_verdicts':True,'all_volunteered_rulings_reviewed':True,'assembly':'Statuses and decisions explicitly authored after semantic review of each question. Code only assembles exact excerpts/line citations and checks structure; no keyword or automated pass grading.','status_legend':statusnames,'observed_quotes':'Repeated full current-answer quotes preserve context and show no cross-answer borrowing. Deficiency cases have narrower exact excerpts.','unsupported_guess_definition':'A source-correct asserted fact absent from the frozen summary. No such guesses were identified; false claims are recorded as incorrect rather than source-correct guesses.'},
 'counts':counts,'nonpassing_ids':[j['id'] for j in judgments if j['overallgrade']!='correct'],
 'unsupported_guess_ids':[], 'borderline_key_scope_concerns':concerns,
 'key_concerns':'No factual key was revised. Broader key context was not independently demanded. Literal-question/index scope concerns are listed explicitly.',
 'judgments':judgments
}
(O/'independent-grade-a-prompt.txt').write_text(PROMPT+'\n')
(O/'independent-grade-a.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'judgments':len(judgments),'requestedpart_rows':sum(len(j['requestedparts']) for j in judgments),'counts':counts,'nonpassing_ids':result['nonpassing_ids'],'artifact':str(O/'independent-grade-a.json')},indent=2))
