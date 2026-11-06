from pathlib import Path
import json,hashlib,datetime,re,collections,shutil
ROOT=Path('/home/jonny/projects/boardgame-rules')
RUN=ROOT/'docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957'
BANK=RUN/'expanded-v12-complete-requested-scope'
OUT=BANK/'luna-iteration-05/source-scope-review-q041-q100'
RULES=ROOT/'extracted/john-company-second-edition-rules.txt'
PDF=ROOT/'source_pdfs/john-company-second-edition-rules.pdf'
PRE=OUT/'full-bank-question-only-prereview.json'
SCOPE=BANK/'requested-fact-scope-reviewed.json'
KEY=BANK/'answer-key.json'
QUESTIONS=BANK/'questions.json'
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def readj(p):return json.loads(p.read_text())
old_names=['question-only-prereview.json','source-read-record.json','input-hashes.json','source-key-scope-review.json','source-key-scope-review.md']
preserved={str(OUT/n):sha(OUT/n) for n in old_names}
pre=readj(PRE)
questions=readj(QUESTIONS)['questions']
scopes=readj(SCOPE)['questions']
keys={r['id']:r for r in readj(KEY)['answers']}
originals={r['id']:r['question'] for r in questions}
assert len(questions)==len(scopes)==len(keys)==len(pre['rows'])==113
assert sum(len(r['material_requested_facts']) for r in scopes)==919
assert all(r['question']==originals[r['id']] for r in scopes)
lines=RULES.read_text().split('\n')
page=0;line_pages={}
for n,line in enumerate(lines,1):
 m=re.match(r'--- Page (\d+) ---',line)
 if m:page=int(m.group(1))
 line_pages[n]=page
E={}
def rule(a,b):
 id=f'R{a}-{b}'
 if id not in E:
  E[id]={'source_path':str(RULES),'edition':'Second Edition, Second Printing 2023','printed_pages':sorted(set(line_pages[n] for n in range(a,b+1))),'physical_LF_start':a,'physical_LF_end':b,'numbering':'text.split("\\n"), one-based','evidence_kind':'verbatim_original_source','quote':'\n'.join(lines[a-1:b])}
 return id
ranges={
1:[(901,916)],2:[(1002,1014),(2651,2658),(917,928)],3:[(1076,1104)],4:[(1128,1145)],5:[(1146,1169)],6:[(1175,1190)],7:[(1331,1365)],8:[(1403,1416)],9:[(1457,1471),(1812,1815)],10:[(1540,1582)],11:[(1617,1650),(707,711),(1651,1666)],12:[(1648,1650),(1674,1710)],13:[(1742,1771),(1361,1365)],14:[(1897,1934)],15:[(2262,2296),(2192,2219)],16:[(2570,2587)],17:[(2588,2601),(2626,2630)],18:[(2679,2724),(1184,1187)],19:[(2773,2822)],20:[(2827,2855),(2888,2918)],21:[(654,666),(2773,2789)],22:[(757,807),(1184,1187),(1039,1042)],23:[(762,807),(843,847)],24:[(416,433),(453,477)],25:[(836,853),(1900,1902),(2008,2012),(2586,2587)],26:[(812,853)],27:[(829,835),(2719,2720),(2665,2674)],28:[(1018,1031)],29:[(1022,1025),(2344,2357)],30:[(1100,1134),(1894,1896),(2719,2720)],31:[(1083,1099)],32:[(1191,1194),(1083,1085)],33:[(1234,1254)],34:[(1417,1433),(1808,1815)],35:[(1472,1520)],36:[(1527,1544)],37:[(1555,1582),(2612,2619)],38:[(1617,1627),(2618,2619)],39:[(1630,1650),(1674,1703)],40:[(1753,1762),(1648,1650)],41:[(1808,1816)],42:[(1817,1823)],43:[(1841,1859)],44:[(1860,1889)],45:[(1943,1954),(1812,1815),(2919,2922)],46:[(1962,1975)],47:[(2111,2123)],48:[(2124,2132)],49:[(2133,2139)],50:[(2192,2208),(707,714)],51:[(2209,2219)],52:[(1987,2012),(2262,2296)],53:[(2045,2082)],54:[(2297,2316)],55:[(2330,2343),(2365,2367)],56:[(2344,2364),(1033,1037)],57:[(2525,2540),(2584,2584)],58:[(2541,2564)],59:[(2602,2621)],60:[(2651,2674)],61:[(2635,2647),(2729,2739),(2773,2779),(2838,2838),(2888,2918)],62:[(2679,2688)],63:[(2729,2740)],64:[(2741,2748)],65:[(2749,2768)],66:[(2782,2785),(2913,2922)],67:[(2689,2724),(2845,2850)],68:[(2749,2768),(2852,2855)],69:[(2648,2650),(2839,2843)],70:[(2665,2674),(2839,2843)],71:[],72:[(358,388),(2626,2630)],73:[],74:[],75:[(825,828)],76:[(2588,2601),(2361,2364),(814,816)],77:[(2297,2316)],78:[],79:[(335,388)],80:[(862,887),(898,900),(2679,2682)],81:[(917,928)],82:[(707,714),(1693,1703),(2216,2218)],83:[],84:[(1076,1082),(1135,1145)],85:[(1331,1339),(1853,1857),(1816,1816)],86:[(1939,1961),(1812,1815),(2919,2922)],87:[(698,701),(715,727),(2186,2212)],88:[(1617,1627),(2262,2296)],89:[(2186,2191)],90:[(2216,2219)],91:[(2365,2367)],92:[(2827,2830)],93:[(1864,1872),(1344,1354),(662,668),(1821,1823)],94:[(1003,1009),(779,785)],95:[(1403,1416)],96:[(1107,1121),(1458,1471)],97:[(1344,1354),(1549,1575),(2817,2820),(2870,2879)],98:[(1681,1692)],99:[(1697,1707)],100:[(1903,1916),(1812,1815)],101:[(2888,2918)],102:[(843,847)],103:[(1344,1354),(1417,1433),(1812,1815)],104:[(1472,1484)],105:[(1580,1582)],106:[(1999,2007)],107:[(2679,2688),(2773,2775)],108:[(2750,2768)],109:[],110:[(1617,1647),(1341,1364)],111:[(1039,1042),(821,822)],112:[(1925,1934),(2895,2902)],113:[(1080,1088)]}
rowev={n:[rule(*ab) for ab in rs] for n,rs in ranges.items()}
def supplementary(id,path,quote,**kw):
 E[id]={'source_path':str(path),'evidence_kind':'verbatim_original_source','quote':quote,**kw}
 return id
foreign_path=RUN/'supplements/foreign-invasion-designer-ruling.json'
foreign=readj(foreign_path)
supplementary('FOREIGN-DESIGNER',foreign_path,foreign['body'],article_id='42192767',author_id=11406,date='2023-04-30',original_url=foreign['canonical_link'])
human_path=RUN/'human-defense-interpretation-source.json';human=readj(human_path)
supplementary('HUMAN-DEFENSE',human_path,'\n'.join(human['messages_in_order']),authority='User-approved interpretation, not independently verified publisher email',adopted_rule=human['normative_authority_for_summary'])
approved_path=ROOT/'docs/quality/summary-qa/batches/2026-11-05-batch-002957/john-company-user-approved-scope.json';approved=readj(approved_path)
supplementary('APPROVED-SCOPE',approved_path,'\n'.join(x['text'] for x in approved['human_messages']),authority=approved['authority'],adopted_rule=approved['adopted_rule'])
errata_path=RUN/'supplements/full-official-errata.txt';err=errata_path.read_text().split('\n')
def errata_span(id,startneedle,endneedle):
 a=next(i for i,v in enumerate(err) if startneedle in v)
 b=next((i for i in range(a+1,len(err)) if endneedle in err[i]),len(err))
 supplementary(id,errata_path,'\n'.join(err[a:b]),physical_LF_start=a+1,physical_LF_end=b,numbering='text.split("\\n"), one-based',unpaginated=True)
errata_span('ERRATA-SETUP','1813 Setup Card','Mercantile Connection')
errata_span('ERRATA-CARDS','Mercantile Connection','Law Card - War Against France')
errata_span('ERRATA-FRAUD','\tCompany Fraud','\tLaw Card - Public Demands Impeachment')
thread_path=RUN/'supplements/ruling-thread-2938749.json';thread=readj(thread_path)
def articles(x):
 if isinstance(x,dict):
  if 'body' in x:yield x
  else:
   for y in x.values():yield from articles(y)
 elif isinstance(x,list):
  for y in x:yield from articles(y)
arts=list(articles(thread));start=next(x for x in arts if str(x.get('id'))=='40838655');ruling=next(x for x in arts if str(x.get('id'))=='40850873')
supplementary('FRAUD-DESIGNER',thread_path,start['body']+'\n\nDESIGNER REPLY: '+ruling['body'],article_ids=['40838655','40850873'],designer_author_id=11406,original_url=ruling['canonical_link'],note='The designer explicitly endorses option 2, actual Company Balance removed. Other commenters were not treated as rule authority.')
# Extract only the allowed original PDFs, not pre-existing derivatives or neighboring files.
import fitz
board_path=RUN/'supplements/pnp/Board/John Company Game Board.pdf'
front_path=RUN/'supplements/pnp/Cards/John Company Cards (Bridge, Fronts).pdf'
back_path=RUN/'supplements/pnp/Cards/John Company Cards (Bridge, Bridge).pdf'
frontdoc=fitz.open(front_path);backdoc=fitz.open(back_path)
for p in [1,2,5,6,7,9]:
 supplementary(f'FRONTS-P{p}',front_path,frontdoc[p-1].get_text(),pdf_page=p,note='Direct PDF extraction. Relevant scenario/card prose also checked in native page images where needed; unusual control-character glyphs do not substitute for graphic inspection.')
supplementary('BACKS-P9',back_path,backdoc[8].get_text(),pdf_page=9,note='Original Situation in India diagrams; Q079 asks to follow the chosen diagram, not to enumerate its map states.')
E['BOARD-PRIZES']={'source_path':str(board_path),'pdf_page':1,'evidence_kind':'native_pdf_visual_transcription','original_labels':['£2','£4','£8','£14','£20'],'transcribed_table':{'columns':['cost','upkeep','VP','windows'],'rows':[[2,0,0,0],[4,1,2,1],[8,2,4,2],[14,3,8,3],[20,4,12,4]]},'visual_artifact':str(OUT/'full-bank-board-native-left.png'),'note':'Numbers and repeated window icons inspected on the native original board. Zero upkeep/windows are blank on the first prize; values are per member.'}
E['BOARD-STOCK']={'source_path':str(board_path),'pdf_page':1,'evidence_kind':'native_pdf_visual_transcription','transcription':'Stock Exchange arrow path: £2 → £3 → £3 → £4 → £5. Two separate £3 spaces.','visual_artifact':str(OUT/'full-bank-board-native-left.png')}
E['BOARD-TURNS']={'source_path':str(board_path),'pdf_page':1,'evidence_kind':'native_pdf_visual_transcription','transcription':'1710 date at turn 1; 1758 at turn 3; 1813 at turn 5. End arrows: 1710 after turn 5; 1758 after turn 7; 1813 after turn 8.','visual_artifact':str(OUT/'full-bank-board-native-left.png')}
E['BOARD-POWER-AWARDS']={'source_path':str(board_path),'pdf_page':1,'evidence_kind':'native_pdf_visual_transcription','original_labels':['Power Award','If tied for first, take the lower award.'],'transcribed_table':{'final_turns_1_to_3':{'first':3,'second':1},'final_turns_4_to_6':{'first':5,'second':2},'final_turns_7_to_8':{'first':8,'second':4}},'visual_artifact':str(OUT/'full-bank-board-native-left.png')}
E['BOARD-TRACKS']={'source_path':str(board_path),'pdf_page':1,'evidence_kind':'native_pdf_visual_transcription','original_labels':['Social','Company Share','Shipping','Manufacturing','S','Company Standing','Company Debt'],'transcription':'Power initial positions: Social at 2; Company Share at 1; Shipping then Manufacturing at the two zero-Power spaces, Manufacturing bottom/right and Shipping next/left on the connected path. Standing lined £4, £6, £8; star £4. Debt lined 5,6,7,8; star 8. S is above £10 Expectations.','visual_artifact':str(OUT/'full-bank-board-native-left.png')}
E['BOARD-RIBBON']={'source_path':str(board_path),'pdf_page':1,'evidence_kind':'native_pdf_visual_transcription','transcription':'Chairman → Director of Trade (Governor General overlay slot) → Manager of Shipping → Military Affairs → Presidency of Bombay → Presidency of Madras → Presidency of Bengal → China if opened. Firms if Deregulation appears between Family and Hiring.','visual_artifact':str(OUT/'full-bank-board-native-overview.png')}
E['RULES33-CIRCLE']={'source_path':str(PDF),'printed_page':33,'pdf_page':33,'evidence_kind':'native_pdf_visual_transcription','quote':'If the Elephant was fully within a Company-controlled region that was invaded, perform an Elephant’s March using ● for the shape. (Otherwise this event does not move the Elephant.)','visual_artifact':str(OUT/'full-bank-rules-page-33.png'),'note':'● is the solid circle icon omitted by the supplied original text extraction at LF2316.'}
E['RULES42-CHARTER']={'source_path':str(PDF),'printed_page':42,'pdf_page':42,'evidence_kind':'native_pdf_visual_transcription','transcribed_table':{'firm_value':[1,2,3,4,5,6,7,8,9,10],'VP_per_share':[-1,0,0.5,0.5,1,1,1,1.5,1.5,2]},'visual_artifact':str(OUT/'full-bank-rules-charter-value-zoom.png'),'note':'Charter illustration enlarged from the original rules PDF; all ten positions inspected.'}
extra={15:['FOREIGN-DESIGNER','HUMAN-DEFENSE','APPROVED-SCOPE'],30:['BOARD-STOCK'],54:['FOREIGN-DESIGNER','RULES33-CIRCLE'],71:['BOARD-PRIZES'],72:['BOARD-TURNS'],73:['FRONTS-P9','ERRATA-SETUP'],74:['FRONTS-P9','ERRATA-SETUP'],75:['BOARD-POWER-AWARDS'],76:['BOARD-TRACKS'],77:['FOREIGN-DESIGNER'],78:['ERRATA-CARDS','FRAUD-DESIGNER','FRONTS-P1','FRONTS-P6'],79:['BACKS-P9'],82:[],83:['RULES42-CHARTER'],85:['BOARD-RIBBON'],88:['HUMAN-DEFENSE','APPROVED-SCOPE'],106:['FOREIGN-DESIGNER'],109:['ERRATA-FRAUD','FRONTS-P1']}
for n,ids in extra.items():rowev[n].extend(ids)
# Authored row rationales from exact question clauses, not another answer or any reader result.
why={
1:'The roll, modifier, outcome thresholds and three retirement destinations directly answer the three interrogatives.',
2:'Eligibility includes ordinary pensioner and qualifying firm special retirements. Order, cash/windows/PM tiebreakers, display exhaustion/refill/orientation and unused pensioners are all expressly requested; peeking is contextual here and directly asked by Q094.',
3:'The question requests both marker/law mechanics and a numeric application. Once-per-turn vacancy extra cannot be doubled with the repeated action; three writers is required in the stated fixture.',
4:'New-share creation and leftover-applicant movement require rightmost-first, Debt reduction and preserved order. Purchase price itself is contextual because the final clause asks where the original money went.',
5:'Vacancy order, consent pool, promoted fatigue and vacancy fallbacks are explicit. The Chairman-election exception qualifies the requested consent rule.',
6:'Eligibility, pure majority, first-to-support rule, deadlock choice and share representation/trade restriction are requested. Taking the title is clearly implied by being elected; a separate announcement by the former Chairman is administrative context.',
7:'General check resources/payment, lowest-die thresholds, retries, catastrophe consequences/destinations and no-dead-action rule are requested. A generic disclaimer about special offices does not supply a requested destination.',
8:'Borrowing amount/count, majority consent, Chairman share, Debt cap and complete allocation are substantive requested duties. Balance reduction follows the asked allocation operation, unlike unasked expense-marker mechanics in Q100.',
9:'Budget-spending obligation, each acquisition price, eligible destinations including China, owner consent and no-unfitted-ship prerequisite are all explicit requested categories.',
10:'The enumerated Trade subjects require reachability, penalties, capacity/route, insufficient writers, protected homes, personal bonuses and success limit. General Trade revenue/rate have their own exact questions Q097; no imported answer is needed for this response.',
11:'Target eligibility/exclusions, active-resource dice, empire penalty and loss-check timing/owner/destination are all requested. Counting the target once follows combined-empire strength rather than adding it twice.',
12:'Loot and trophy calculation, control/overlay/card destinations and catastrophe changes are requested. Distribution and Elephant redirect are contextual to this wording and independently asked by Q098/Q099.',
13:'How Administer works across repeated attempts is a broad procedural request: dice depletion, success options including both construction stages, personal bonus, tax/failure unrest and stop/catastrophe conditions all belong.',
14:'The question requests emergency borrowing, Standing changes and the sequence of expectations/dividends. The broad Standing clause supports expectation and enthusiasm effects; separate immediate game-ending consequences are contextual and asked by Q025.',
15:'Targets, order, primary/secondary strength, defense actor/fallback/exhaustion and successful results are asked. The greater-than-or-equal comparison is authorized human interpretation, distinct from the literal original equality wording. No official-email claim is required.',
16:'Threshold including zero, card/token/PM/policy consequences and full resolution order directly answer fail-versus-pass outcomes, including common vote-card cleanup.',
17:'Scenario/timing eligibility, lined/starred conditions, pass/fail effects and ordinary-voting exceptions are explicit; all listed atoms are required or clear implications.',
18:'Formation and investment mechanisms, eligibility, source/destination of the £5, share/workshop restrictions and cap behavior are requested. No unrelated firm acquisition mechanics are required.',
19:'Strategy, check and order-fill timing, initiative, capacity, refilling and Value growth are explicitly asked. The source requires waiting for the President’s successful Trade roll before ordinary order filling; absent/nontrading fallback is separately stated in the current list.',
20:'Cost formula, treasury funding, dividend calculation and failure outcomes to shares/ships/charter/workshops are requested. Exact Revenue order, marker/sweep/waiver mechanics are contextual to this row and separately asked by Q092/Q101.',
21:'Unlimited supplies/tracks, limited-supply fallback and normal/temporary hidden information are the question’s complete categories; provisional firm secrecy is a relevant exception.',
22:'All positive and negative trade categories, Chairman restriction, share replacement/destinations and used-blackmail ban are requested. Luxury VP adjustment and private peeking are not independently demanded here.',
23:'Enforceability, promise force/timing/endgame limits, unfulfillable simultaneous calls and no-double-activation directly answer the exact wording.',
24:'Extra setup cards, holdings distribution, luxury VP and display construction are requested. The office family member goes to the office; its matching card is taken by the player, not placed at that office.',
25:'End triggers, immediate-versus-finish-phase exceptions and Final Scoring negotiation/promise limits are explicit; card permission qualifies the requested prohibition.',
26:'The question asks all Power sources, tie awards and victory ties. Equivalent Power descriptions are sufficient; no demand to recite category labels in a particular order.',
27:'Survival/failure share/workshop and final-retirement consequences are exactly asked. Firm investment status qualifies workshop scoring; firm-special-retirement timing is contextual here.',
28:'Transfer ban, permanent spouse restrictions, immediate required trades, discount magnitude/stacking/personal use and frequency all answer requested effects.',
29:'The question asks fitted ship persistence and repurchase eligibility after either specified shipyard-return cause, not unrelated loss-of-VP rules.',
30:'All family action prices and immediate placements/effects, votes, income and failure scoring are requested. The five distinct exchange prices answer the requested purchase-cost list; they are not an invented aggregate.',
31:'Mandatory prize cannibalization with VP loss and no-action/marker fallback are exactly asked; applying it to firm-share creation is contextual here.',
32:'The empty-Court procedure and both shortage fallbacks are explicit; prize VP loss is a necessary consequence of the requested shortage case.',
33:'Each listed office’s hirer, candidate pool, ordered fallbacks and exclusions are requested. The Commander exclusion from Governor eligibility is substantive.',
34:'Successful Envoy choices, immediate China creation/hiring result, repetition and transfer timing are requested. Naming the Chairman and writer candidate pool for China is a separate hiring detail, directly asked by Q033/Q041.',
35:'Action order and Commander appointment/replacement eligibility are requested. Army transfer quantities/placements are contextual here and explicitly asked by Q104.',
36:'Presidency order authority, offered actions, decline/interruption rules and vacant-President Chairman limits are all requested.',
37:'Ship exhaustion and writer/divider return are asked. Affiliation must be preserved on return; the detailed divider-placement trigger is contextual and separately asked by Q105.',
38:'Alliance purchase/exhaustion timing, funding, indivisibility and once-only use for Deploy/defense are asked. These are real restrictions, not dispensable examples.',
39:'The specified own-region case asks only its penalty, loot minimum and trophies. Permission to target and all success-cleanup procedures are contextual to that fixture.',
40:'Success count and construction/finished destinations are asked, along with regiment treatment (Army placement, strength, bank loot and loss immunity). Lack of any other effect while unfinished is true but not independently asked by the location clauses.',
41:'Preserved two-question review applies: creation/hiring/ship-only treasury/timing/Eastern status required; transfer actors contextual; four-purpose enumeration not independently required if Eastern equivalence is clear.',
42:'Each yes/no eligibility limit and dice/revenue/bonus formula is explicitly asked; non-Company exports must be excluded.',
43:'The law’s effects on Governors, unfinished ships, Director/fatigue and future conquest/loss procedures are asked. Treasury and operation-slot continuity are part of the asked Director replacement.',
44:'Guaranteed revenue, six/failure/tax unrest, mandatory per-region choice, all choice destinations/restrictions and success cap are asked. The created ship is specifically a Company ship.',
45:'All storm outcomes and exemptions by fatigue/ownership/China/firm strategy/Hobnob are expressly requested.',
46:'Writer/token handling and Cascade propagation/closed-target fallback/per-region limits are requested; multiple incoming effects differ from initiating multiple Cascades.',
47:'All three named event locations/resolution sequences and the empty-stack Shuffle reversal are requested.',
48:'Leader location, sovereign versus dominated resolution and the restricted Elephant movement are substantive parts of resolving the named event.',
49:'Border versus fully-inside Peace effects and subsequent March are explicit; do not import border tower growth into the wholly-inside case.',
50:'Strengths, strict comparison and flag/capital/no-flag-supply effects are asked; the failed attacker’s tower loss is contextual to this exact question.',
51:'Regional strength inclusion/exclusion, tie failure and capital tower loss are exactly asked. Successful Rebellion cleanup is contextual here and asked by Q090.',
52:'The broad request to list Region Loss destinations includes Commander/Governor/overlay/ship/unrest/dome/flag/control-token treatment, plus officer checks, loot status, escalating Standing and separate regional resolution.',
53:'March destination exception and each posture branch/fully-formed-empire fallback are asked. Imperial Ambitions is not interchangeable with normal top-stack destination.',
54:'All Foreign Invasion targets, die strength, success-only orders/flags/towers and conditional circle March are asked; unrest exclusion is supported by the authorized designer ruling.',
55:'Drawing stop/selection/dilemma rules and the directional first-matching policy choice with target/consequence are requested. Reading the law and initial support are contextual and Q091 asks support separately.',
56:'Tax/window/bonus amounts, nonpayment consequences, affected prestige enterprises and Power swaps/highest-target exception are requested by the broad policy-procedure wording.',
57:'Vote sources/prices, single-use card votes across rounds, round order/authority and mandatory stop are asked. Unlimited track bookkeeping and final cleanup are optional context here.',
58:'Direction of vote switching, Opposition Leader/ties, coalition consent/counting and PM prohibition/promise exception are explicit.',
59:'Final-turn upkeep, unpaid member/VP consequences, skip-Refresh branch and all ordinary Refresh items are expressly requested.',
60:'Special-retirement frequency/piece/cash cap/discounts/ineligibility and Final Scoring timing are asked. Ordinary prestige rules remain optional background to this row.',
61:'Each fund origin/destination/use and no-family-cash-transfer restriction is requested. Post-dividend India sweep is contextual here and Q101 directly asks it.',
62:'Phase position and conflict decision makers are asked; Investments ordering and strategy simultaneity are contextual to this wording, with Q107 asking Investments order.',
63:'Consent, permitted/prohibited ship types, fitting/buyback prices and both payment destinations are all explicitly asked.',
64:'Hostile takeover initiator eligibility/consent and movement/preservation/reset of firm assets/markers/charter are requested; initiator shareholding is not a prerequisite.',
65:'Consent, highest-Value/tie choice, excess-share consent and secondary treasury/charter outcomes are asked. Ships/share consolidation is contextual here and expressly Q108.',
66:'No bid/trade/dividends, mandatory expenses, retained retirement marker and storm exemption directly answer each Hobnob clause.',
67:'Cap eligibility, admissible investment resources/restrictions, expense use, lost rescue remainder and per-investment Value loss are requested. Normal manager consent is contextual to this narrow row.',
68:'The one-other-firm limit and responsibility/timing for both sets of expenses are requested differences. Unchanged all-shareholder consent is true background, not a requested difference; Q065 explicitly asks merger legality.',
69:'Full-shareholder dissolution consent and share/ship/workshop destinations/status are asked. Penalty amount and charter reset are fuller dissolution context, separately covered by Q020/Q070.',
70:'Timing relative to normal scoring, firm-share/prison amounts, fractional summing/rounding and applicability regardless Company outcome directly answer the question.',
71:'Every cell in the five-prize cost/upkeep/VP/windows table is explicitly requested; zero entries must not be invented as nonzero costs.',
72:'Each scenario’s start/end turns and Deregulation status are explicit. Long 1710 uses normal 1710 setup through turn 8.',
73:'Both scenario initial finance/laws/regiments/Company ships and 1758 Bengal control token are explicit; original scenario cards and errata agree.',
74:'Every listed 1813 setup category is explicit; share-value token, boxed GG law/overlay, China and three control tokens are real mandatory changes.',
75:'Each award pair and tied-first lower-only consequence are directly requested, with native board values verified.',
76:'Initial positions include the distinct order of the two zero-Power spaces; the question also requests lined/starred thresholds and S, verified on the native board.',
77:'The question asks whether unrest increases either quantity and what happens to orders. It does not ask for the base attack/tower formula; those formulas are explanatory context and Q054 directly requests them.',
78:'Each specified corrected-card edge case is requested. Fraud timing/dice/raw amount are optional here and directly asked by Q109.',
79:'Shared initial Balance/VP/alliance/loot locations and scenario-instruction/map/date/PM setup are explicit. It does not ask to enumerate every depicted initial region.',
80:'Complete phase order, conditional Firms insertion and entire first-turn London skip are explicitly requested.',
81:'Chairman/former fallback, clockwise order, optional retirement and pensioner/VP/cash destinations/timing are all explicit.',
82:'The question asks capital flag disposition and whether the loss cause matters. That cleanup is required for both named causes; the explanatory label no longer an empire is not an additional mandatory sentence.',
83:'All ten Value-to-VP outcomes are explicitly requested, not the broader fractional-totaling procedure.',
84:'First player, clockwise sequence and completion gate before New Shares are the exact requested facts.',
85:'Complete office sequence, GG replacement slot and vacant-office skip are requested. Internal Presidency sequencing is contextual here.',
86:'Storm opening/order, eligible ships/exemptions/zone mappings and die-controlled sequential event count are requested; no detailed storm result table is demanded here.',
87:'Elephant attacker/defender and Crisis branch, including wholly-inside Company Rebellion, plus sovereign/dominated visual markers are requested.',
88:'The fixture, whole-alliance exhaustion, success consequences, non-reuse and user-only/general interpretation attribution are all directly requested. No private email inspection is assumed.',
89:'The timing and all successful/failed ordinary Invasion/Rebellion cases are directly asked; March destination/posture is contextual to this row.',
90:'Sovereignty, flag return and order closure/Cascade exception are explicitly requested. Cascade must be conditioned on orders already all closed, not after every successful closure.',
91:'Initial Votes marker position and source of starting support are requested; PM/read-aloud/detail-of-card-location are contextual here.',
92:'Start-of-Revenue placement, initiative/other firms order and windows/PM tiebreakers are all explicit.',
93:'Funding treasury, paid-die rate/no penalty and bonus amount/recipient/source are explicitly requested. Bank sourcing is an ordinary take-a-bonus inference from the action and parallel personal bonus text, not a literal bank word in the Govern paragraph.',
94:'Both inspection permissions are explicit; there is no unconditional right to inspect another player’s held blackmail.',
95:'Interleaving, free-three advances, each further majority consent, Chairman share and track end all directly answer the borrowing-limit question.',
96:'All six cash recipients are asked. Stating bank for all six suffices; individual amount/ownership discussion is not a separate requirement.',
97:'Rate/funding, ordinary full-order revenue/destination and the firm-filled half-rounded-down/unmodified-bonus exception are all explicit.',
98:'Surviving participant eligibility, Commander-first/clockwise £1 rounds, bank shares for regiments/alliance pieces and repetition/cash exhaustion are explicitly requested.',
99:'The conditional inward redirect and its intended Company Rebellion meaning are explicitly requested.',
100:'Preserved review applies: full expense census/rates/Army/Commander/sea-zone/China qualifications required. A separate Balance-marker instruction and Eastern rationale are correct context, not extra requested clauses.',
101:'Waiver scope/manager consent, actual-total dividend cube and track position plus India-to-London remainder are all asked.',
102:'Endgame blackmail ban and explicit card-text exception are the exact two requested facts.',
103:'Envoy cash treasury/rate/penalty and transfer number/type/origins/destinations/China eligibility are explicitly requested; no success-outcome expansion is required.',
104:'Transfer count/type/destination/top-half plus assignment of all trainees to any Army/top-half are explicitly requested.',
105:'Placement trigger, connecting route location and retained affiliation for Refresh directly answer the question.',
106:'The ordinary Invasion closure/Cascade condition and no duplicate step for Rebellion/Foreign Invasion are asked. Explaining that those types already close orders is correct but not an independent required rationale.',
107:'No fixed order, anytime actions, no-further-wishes stopping gate and subsequent Strategy are requested; anytime is equivalent to no fixed order, not an extra response sentence.',
108:'Only secondary ship/share consolidation into primary is asked; no unasked treasury or legality procedure is imported.',
109:'Corrected timing, own-officeholder dice and twice-highest raw amount are explicit; cap arithmetic is outside this question’s pre-cap request.',
110:'Success repetition, continued target/no-dead-action rules, still-active resources and catastrophe stop are all explicit; success does not refresh exhausted resources.',
111:'One-use effect, retained card/player area/faceup and retained printed Power are explicit. Still counts clearly implies the relevant faceup/facedown Power rule; no separate recital of both orientations is required.',
112:'Every dividend choice/count/funding/affordability/cost/payout/Chairman/waiver/Standing threshold is explicitly requested. Equality is excluded by strictly greater.',
113:'Initial marker absence and inability to double the first normal action directly answer the question; the second is a clear implication of the first and the phase-start repeat rule.'}
assert set(why)==set(range(1,114))
# Exact fact-level findings; untouched keys/scopes are never rewritten.
F={}
def finding(q,i,category,after,phrase,reason,coverage,source_ids=None,truth='supported'):
 id=f'Q{q:03d}';row=next(r for r in scopes if r['id']==id)
 assert phrase in originals[id],(id,phrase)
 f={'finding_id':f'FB-{id}-{i:02d}','question_id':id,'mandatory_atom_index_1_based':i,'exact_before':row['material_requested_facts'][i-1],'exact_after_mandatory':after,'category':category,'exact_question_phrase':phrase,'exact_question':originals[id],'source_truth_verdict':truth,'asked_scope_verdict':category,'source_evidence_ids':source_ids or rowev[q],'independent_reason':reason,'coverage_consequence':coverage,'proposal_version':'full-bank-source-asked-scope-v1','application':'Recommendation only; not applied to any question, key, scope, summary or grade.'}
 F[(q,i)]=f
finding(6,3,'contextual_only',None,'How is a Chairman elected','Stating the more-than-half threshold, eligibility and first-to-support resolution answers the election rule. The separate administrative act of the former Chairman announcing that already-required threshold is not another material election requirement.','No meaningful distinct core-procedure gap: majority election and former-Chairman deadlock authority remain required in Q006. The announcement itself has no separate exact question.',[rule(1175,1187)])
finding(7,12,'contextual_only',None,'catastrophic destinations','The question requests general catastrophic destinations, not a generic warning that special rules can differ. This atom names no specific exception or destination and should not be separately mandatory. Specific named office exceptions must still be respected where applicable.','No distinct procedure is dropped by removing a generic qualification. Concrete Deploy/Administer/China exceptions remain directly asked in Q012/Q013/Q042.',[rule(1361,1365),rule(1708,1710)])
finding(14,9,'contextual_only',None,'how does Standing change','Immediate game end on reaching the failure space is true, but describes an endgame transition rather than a Standing change or the asked expense-shortfall procedure.','Covered explicitly by Q025: “When does the game end” and its mandatory ordinary failure atom. No core gap.',[rule(1900,1902),rule(836,847)])
finding(19,9,'requested_precision_clarification','After the President makes a successful Trade roll, fill orders in initiative order; if the President is vacant or does not trade, use the stated later fallback.','when checks and order filling occur','The ordinary filling gate is the President’s successful Trade roll, not merely the firm’s successful check at Presidency start. The existing atom is compatible in context but underspecifies the timing expressly asked. This retains a genuine requirement.','No new procedure or question is added: clarify the already-asked timing and retain the existing vacant/nontrading fallback atoms 14–15.',[rule(2791,2809)],truth='supported_in_context_but_incomplete_timing_wording')
finding(24,5,'source_error_requested_destination','Place a family member in the listed office and take the matching office card.','distribute holdings','The source says to place the family member on the office space and take the matching office card. The mandatory atom literally puts both card and member in the office, which is the wrong card destination.','Corrects the explicitly requested distribution of office holdings; no coverage loss or extra obligation.',[rule(420,425)],truth='wrong_card_destination_as_written')
finding(34,3,'mixed_requested_and_contextual','Creating China triggers immediate hiring.','What can successful Special Envoys accomplish','Immediate hiring is a substantive result of creating China. The separate hiring actor (Chairman) and candidate pool (any writer) answer how China is hired, which this question does not independently ask. Do not require those two details again under the accomplishments clause.','Q033 asks who hires China/candidates; Q041 asks how it is hired and retains Chairman/any-writer scope. Immediate hiring remains in Q034. No gap.',[rule(1423,1428),rule(1808,1811)])
finding(40,3,'contextual_only',None,'where is it during construction and where does it go','No other effect is a true usability restriction, but the ship clauses ask success count and locations, not what an unfinished ship can do. A complete answer can give both build stages and destinations without this extra clause.','Explicitly covered by Q013’s broad Administer request and current atom 15, which includes partially built ship/no other effect. No gap.',[rule(1753,1757)])
finding(41,5,'mixed_requested_and_contextual','Ships in China count as Eastern sea-zone ships.','what ships count Eastern','Preserve the original independent two-question verdict: identity/Eastern treatment is asked; individually enumerating all four source purposes is not. A clear general equivalence conveys those applicable consequences.','Q045/Q086 directly ask storms, Q100 expenses, and Q041 retains general Eastern status. Events/laws applications remain part of that equivalence, without a separate per-purpose recital. Shipping destinations are now independently verifiable in Q009 and Q103.',[rule(1812,1815)])
finding(44,7,'requested_precision_clarification','Place a Company ship in any sea zone, including China.','options per region','The shipbuilding option creates a Company ship, not an arbitrary player-owned ship. The short current atom can be read correctly in context, but preserve the source type when stating the asked option.','Strengthens precision of the already-requested option; no new requirement or coverage loss.',[rule(1870,1878)],truth='supported_in_context_with_ship_type_implicit')
finding(68,2,'contextual_only',None,'How does emergency merger differ from a normal multi-firm merger','All-shareholder consent is unchanged from a normal negotiated merger. The question asks differences and whose expenses must be paid, not a restatement of normal legality. The one-other-firm restriction and both expense obligations remain mandatory.','All-shareholder consent is explicitly requested under Q065 “What makes a merger legal” and its atom 1. No gap.',[rule(2760,2762),rule(2852,2855)])
finding(77,2,'contextual_only',None,'does unrest increase a Foreign Invasion primary attack or its resulting tower strength','No unrest contribution answers the primary-attack part. Requiring the base die formula as a separate fact demands an unasked explanation of how the attack is calculated.','Q054 explicitly asks to “calculate strength” and retains attack-die atoms 6–7. No gap.',[rule(2303,2312),'FOREIGN-DESIGNER'])
finding(77,3,'contextual_only',None,'does unrest increase a Foreign Invasion primary attack or its resulting tower strength','No unrest contribution also answers the resulting-tower part. Half-die rounded-down is the correct base formula but not a separate requested answer to whether unrest increases it.','Q054 asks tower changes and retains half-die rounded-down atom 14. No gap.',[rule(2303,2312),'FOREIGN-DESIGNER'])
finding(82,3,'contextual_only',None,'Does the capital keep its starred flag','The question asks flag disposition and whether the cause matters. No/return the capital flag regardless of the two causes fully answers it. The source’s no-longer-an-empire label is a correct explanation rather than an additional requested assertion.','Capital-flag cleanup and both triggering causes remain required in Q082. No meaningful distinct procedure is lost: flag removal is the operational Empire Decline rule. The explanatory status label has no separate interrogative.',[rule(707,714)])
finding(90,4,'requested_precision_clarification','Perform a Cascade only if every order in the rebelling region was already closed.','including when every order there is already closed','The question and key supply the condition, so read the atom conditionally. Its standalone “Then” wording must not become an instruction to close open orders and also Cascade every time. This is a source-precision correction preserving the requested exception.','Restores an explicitly asked condition, rather than relaxing it. Q051/Q046 overlap but cannot substitute for answering Q090.',[rule(2216,2219)],truth='supported_only_with_the_question_and_key_condition')
finding(100,1,'contextual_only',None,'At the Company’s ordinary Revenue expense calculation','Preserve the two-question verdict: this phrase identifies the setting. The actual interrogatives request cost categories/rates, Commander exclusion and China inclusion, not a separate Balance-marker instruction.','FLAG CG-01: no other exact bank question independently asks which account pays/decrements ordinary Company expenses. Q014 asks emergency shortfall handling; Q112 asks dividend funding. Removing this unasked separate atom exposes a narrow core funding/debit coverage gap; do not cure it by imposing it on Q100.',[rule(1903,1906)])
finding(100,7,'mixed_requested_and_contextual','China-assigned ships are included in those £1-per-ship expenses.','do ships assigned to China count','Inclusion at the stated £1 ship rate is required. Eastern classification is a correct explanation, not a separately necessary rationale for the yes/no answer. This preserves the existing independent review.','Q041 directly requests Eastern identity; Q100 retains cost/inclusion. No gap.',[rule(1812,1815),rule(1903,1906)])
finding(106,4,'contextual_only',None,'Does Region Loss impose a second order-closing/Cascade step for a loss caused by Rebellion or Foreign Invasion','The requested no-duplicate-step answer is already mandatory in atom 3. This extra atom explains why. The question does not independently ask the reason. A correct no with the right condition is sufficient.','The independent closing procedures are directly asked by Q090 for Rebellion and Q054/Q077 for Foreign Invasion; duplicate prevention remains required by Q106 atom 3. No gap.',[rule(1999,2007),'FOREIGN-DESIGNER'])
assert len(F)==17
# Atom-specific equivalence and source-inference notes. These do not demand additional answer clauses.
notes={
(2,1):'An eligible firm special retirement counts like a pensioner retirement. No need to repeat the full special-retirement eligibility procedure here.',
(6,5):'Being elected/becoming Chairman clearly implies taking the title; do not require a separate title sentence.',
(9,8):'The no-unfitted-ships prerequisite applies to Company-ship buying, not all Shipping acquisitions.',
(11,9):'Total target empire strength counts the target once. The original example and empire definition resolve the terse additive wording; do not double-count it.',
(14,11):'Affirm under the express broad “how does Standing change” clause, even though the supplied generic justification points only to the timing clause.',
(14,13):'Affirm the source-supported enthusiasm change under the broad Standing interrogative. A narrower emergency-loans-only reading is possible, so this is not a basis for adding unrelated dividend calculations.',
(15,13):'Human-approved >= rule is normative in this assigned scope and must be attributed appropriately if discussed; it is not a literal quote of the printed equality test.',
(21,12):'Temporary firm secrecy is a relevant hidden-information exception, not permission to hide all firm information.',
(30,1):'Free follows the enlistment procedure’s lack of a cash payment; it is not a literal printed £0 charge.',
(30,3):'Free follows the enlistment procedure’s lack of a cash payment; it is not a literal printed £0 charge.',
(40,5):'The broad regiment-treatment clause reasonably includes placement in the associated Army. Do not expand it to unrelated Commander operations.',
(52,13):'Region Loss checks all officers in the associated Army, unlike Deploy checking only officers exhausted for that action.',
(64,3):'No initiating shareholding requirement appears in the complete takeover prerequisites; this is a source-supported eligibility implication.',
(67,6):'“Unused rescue cash after paying expenses is lost” clearly conveys the expenses use; no separate sentence is needed.',
(70,4):'Sum firm-share points/fractions first, then round the remaining fraction down; do not independently round each firm/share.',
(76,12):'The two zero-value spaces remain distinct positions on the native connected Power path.',
(82,1):'Returning the capital flag clearly answers no; no separate literal no is required.',
(86,5):'No storm checks when the die shows no storms follows the die’s zone procedure; number of event tiles still follows its printed number.',
(88,9):'The question explicitly asks official status; do not require a volunteered source disclaimer in other defense questions that do not ask it.',
(90,4):'Condition is present in both exact question and expected answer. Finding is to prevent loss of that condition in standalone atom use, not to accuse the correct expected answer of unconditional Cascade.',
(93,6):'The Govern paragraph says take £1, not literally from the bank. Bank source is inferred from personal-bonus convention and parallel office payouts; do not misquote LF1870 as containing bank.',
(100,5):'Commanders are excluded from the officer expense, not an exemption for the associated Army or its officers.',
(107,2):'No fixed order/anytime actions are equivalent parts of one requested rule; either clear statement can satisfy both.',
(111,4):'“The printed Power still counts after use” suffices. It implies the relevant faceup rule; do not require an additional unrelated statement about unplayed facedown cards.',
(112,3):'Affordability is the ordinary cash-availability implication of paying from Company Balance, not permission to borrow for dividends.',
(113,2):'Clear implication of no initial action placement plus the start-of-phase repeat condition is sufficient.'}
truth_inference={(30,1),(30,3),(64,3),(86,5),(93,6),(112,3),(113,2),(11,9)}
rows=[]
for r in scopes:
 qid=r['id'];n=int(qid[1:]);alist=[]
 for i,fact in enumerate(r['material_requested_facts'],1):
  j=r['fact_justifications'][i-1] if i<=len(r.get('fact_justifications',[])) else {}
  candidate=j.get('question_clause','')
  exact_clause=candidate if candidate and candidate in originals[qid] else originals[qid]
  d={'atom_id':f'{qid}.A{i:02d}','index_1_based':i,'proposed_mandatory_fact':fact,'exact_question_phrase':exact_clause,'source_evidence_ids':rowev[n],'source_truth_verdict':'supported_by_clear_rule_implication' if (n,i) in truth_inference else 'supported','asked_scope_verdict':'affirmed_requested_or_clearly_implied','scope_reason':why[n],'acceptance_standard':'Equivalent wording or clear implications satisfy the atom. Do not require separate recitation where one statement answers overlapping atoms.'}
  if (n,i) in notes:d['specific_acceptance_or_source_note']=notes[(n,i)]
  if (n,i) in F:
   f=F[(n,i)];d.update({'finding_id':f['finding_id'],'source_evidence_ids':f['source_evidence_ids'],'source_truth_verdict':f['source_truth_verdict'],'asked_scope_verdict':f['category'],'scope_reason':f['independent_reason'],'exact_question_phrase':f['exact_question_phrase'],'recommended_after_mandatory':f['exact_after_mandatory'],'coverage_consequence':f['coverage_consequence']})
  alist.append(d)
 # Correct model answers may include fuller background. Never convert all key clauses into requirements.
 kr=keys[qid]
 rows.append({'id':qid,'exact_question':originals[qid],'mandatory_atom_count':len(alist),'source_evidence_ids':rowev[n],'question_scope_rationale':why[n],'key_entry_review':{'expected_answer':kr['expected_answer'],'source_references_as_supplied':kr.get('source_references'),'verdict':'Source-supported in the intended context; see any atom-level destination/condition precision findings. Contextual key prose is not automatically mandatory.','novelty_field_use':'Not evidence for askedness or source truth; other questions were checked by their exact fixed wording.'},'existing_contextual_extras_review':{'extras':r.get('contextual_key_extras',[]),'verdict':'Not imported into mandatory scope. Exact other-question coverage is listed below where consequential to a correction; no prior coverage/history claim was adopted without checking the fixed question.'},'mandatory_atom_reviews':alist,'row_verdict':'explicit_findings' if any((n,i) in F for i in range(1,len(alist)+1)) else 'affirmed','findings':[F[(n,i)]['finding_id'] for i in range(1,len(alist)+1) if (n,i) in F]})
assert len(rows)==113
all_atoms=[a for r in rows for a in r['mandatory_atom_reviews']]
counts=collections.Counter(a['asked_scope_verdict'] for a in all_atoms)
assert len(all_atoms)==919 and sum(counts.values())==919
coverage_gap={'id':'CG-01','core_procedure':'Ordinary Company expense funding/debit from Company Balance','triggered_by_finding':'FB-Q100-01','original_source_evidence_ids':[rule(1903,1906)],'exact_question_checks':{'Q100':originals['Q100'],'Q014':originals['Q014'],'Q112':originals['Q112']},'assessment':'No other exact question independently asks which funds pay ordinary Company expenses or instructs the ordinary Balance debit. Q014 asks a revenue shortfall and emergency borrowing/Standing/sequence; Q112 explicitly asks dividend funding. Treating Q100’s unasked marker instruction as context therefore leaves a narrow but meaningful funding/debit procedure without an explicit interrogative. The expense census/rates remain fully tested.','action':'Flag for future bank design; do not silently retain an unasked mandatory clause, alter a question, or pad with a recombination in this review.'}
report={
 'report_version':'full-bank-source-asked-scope-v1','created_at_utc':now,
 'independence':'Source/question-only. No reader responses, grades, summaries, audit reports, canonical rules markdown, histories, runtime/status tools or neighboring QA artifacts were opened. Full allowed bank files were parsed for questions/answers/mandatory scope; incidental metadata was not treated as evidence. No desired score or reader outcome was supplied.',
 'scope':'Standard multiplayer 3–6, all assigned standard scenarios and firms; official rules/errata/rulings plus expressly attributed human-approved total newly exhausted defense strength >= attack interpretation. Crown/solo/two-player and optional setup draft are not benchmark scope.',
 'staging':{'question_only_prereview_path':str(PRE),'question_only_prereview_saved_before_full_keys_and_scope':True,'full_prereview_rows':113,'previous_two_question_review_preserved_paths':list(preserved),'previous_two_question_review_hashes':preserved,'method':'Exact-question decomposition was saved first. Then every current mandatory fact and fuller key answer was read, independently compared with original rules and allowed supplements, and accounted for individually below. Clear implications count; no answer from another question is imported to cure a response omission.'},
 'accounting':{'questions_reviewed':113,'mandatory_atoms_reviewed':919,'unreviewed_questions':0,'unreviewed_mandatory_atoms':0,'verdict_counts':dict(counts),'affirmed_atoms':counts['affirmed_requested_or_clearly_implied'],'atoms_with_explicit_findings':len(F),'questions_with_findings':sum(bool(r['findings']) for r in rows),'all_others_affirmed':'Every atom not listed as an explicit finding is individually affirmed with a question phrase, original-source evidence IDs and row-specific requested-scope rationale.'},
 'concrete_findings_summary':{'source_destination_error':'Q024 atom 5 puts the office card at the office. Original setup places the member there and tells the player to take its matching card.','requested_condition_precision':['Q019 atom 9: ordinary order filling waits for the President’s successful Trade roll; preserve its stated fallback.','Q044 atom 7: created ship is a Company ship.','Q090 atom 4: Cascade only if all orders were already closed. The existing key/question already supply the condition.'],'scope_findings':'Ten wholly contextual current atoms and three mixed atoms contain independently unasked procedures/explanations. Exact before/after proposals follow; three mixed atoms retain their genuinely asked core.','coverage':'Most moved facts are expressly requested elsewhere or do not constitute a distinct procedure. CG-01 flags ordinary Company expense funding/debit as an explicit-interrogative coverage gap after the Q100 scope correction; no question or key was edited.'},
 'correction_proposals':list(F.values()),'coverage_gaps':[coverage_gap],
 'cross_question_coverage_checks':[
 {'fact':'Shipping ships may go to China','asked_by':'Q009','exact_question_phrase':'State ship costs, destinations, consent requirements and the prerequisite for buying Company ships.','current_mandatory_atom':'Q009.A07','source_evidence_ids':[rule(1812,1815),rule(1457,1471)],'verdict':'Verified from full fixed question/scope; Q041 may keep this as context.'},
 {'fact':'Director ship transfers may go to China','asked_by':'Q103','exact_question_phrase':'which origins and destinations are eligible, including China?','current_mandatory_atom':'Q103.A07','source_evidence_ids':[rule(1432,1433),rule(1812,1815)],'verdict':'Verified from full fixed question/scope; no current full-bank gap in China transfer eligibility.'},
 {'fact':'China hiring actor/pool','asked_by':['Q033','Q041'],'exact_question_phrases':['Who hires the Director, Shipping, Military Affairs, Presidents, Governors and China','how is it hired'],'current_mandatory_atoms':['Q033.A05','Q041.A02'],'source_evidence_ids':[rule(1253,1254),rule(1808,1811)]},
 {'fact':'Unfinished Company ship has no other effect','asked_by':'Q013','exact_question_phrase':'How does Governor Administer work across repeated attempts','current_mandatory_atom':'Q013.A15','source_evidence_ids':[rule(1753,1757)]},
 {'fact':'All merging shareholders consent','asked_by':'Q065','exact_question_phrase':'What makes a merger legal','current_mandatory_atom':'Q065.A01','source_evidence_ids':[rule(2760,2762)]},
 {'fact':'Foreign Invasion attack/tower base formulas','asked_by':'Q054','exact_question_phrase':'calculate strength, alter towers/flags/orders','current_mandatory_atoms':['Q054.A06','Q054.A07','Q054.A14'],'source_evidence_ids':[rule(2303,2312),'FOREIGN-DESIGNER']},
 {'fact':'Rebellion/Foreign Invasion own order closure procedures','asked_by':['Q090','Q054','Q077'],'exact_question_phrases':['what happens to the rebel region’s sovereignty, flag and orders','alter towers/flags/orders','What happens to orders?'],'current_mandatory_atoms':['Q090.A03','Q090.A04','Q054.A09','Q054.A10','Q077.A04','Q077.A05'],'source_evidence_ids':[rule(2216,2218),rule(2303,2307)]}
 ],
 'genuine_scope_boundaries':[
 {'question':'Q014','assessment':'The broad how does Standing change wording reasonably reaches Public Embarrassment, Expectations and Public Enthusiasm. Retain expectation/enthusiasm changes; do not use the narrower supplied timing-only justifications to erase them. Immediate game end is a different procedural transition, identified separately.'},
 {'question':'Q034','assessment':'What successful Envoys accomplish includes immediate hiring as part of creating China. Hiring actor/candidate details are a narrower how-is-it-hired request, present explicitly in other questions. Only those contextual subcomponents move.'},
 {'question':'Q040','assessment':'How are Governor regiments treated is broad enough to include placement in the associated Army and the stated officer-like/bank-loot/no-loss behavior. Keep those real restrictions. The ship location clauses do not independently ask unfinished usability.'},
 {'question':'Q041','assessment':'General Eastern identity clearly implies the rule’s applicable purposes; the fixed source bounds must not be contradicted. Do not require exhaustive named-purpose recall from a which-ships question.'},
 {'question':'Q111','assessment':'Retained Power after using the faceup card answers the exact question. The atom’s faceup/facedown language is satisfied by that clear implication, without a separate recital about unused cards.'}
 ],
 'source_truth_inference_limits':['Q093’s bank bonus source is an inference from take-a-personal-bonus convention and parallel office income, not a verbatim bank word in the Govern paragraph.','Free enlistment, no initial marker doubling, no takeover shareholding prerequisite and ordinary dividend affordability are clear structural implications of complete original procedures. These are individually marked as such.','Q015/Q088 use the expressly authorized human >= interpretation instead of pretending the printed equality sentence literally says >=. The reported private publisher email was not inspected.'],
 'rows':rows,'source_evidence_registry':E,
 'prohibited_mutations':'No questions, keys, scopes, summaries or current grades were edited. The five original two-question review outputs and all authorized inputs remain byte-identical. Recommendations do not change or predict grades.',
 'limitations':['Original designer/source copies supplied in the run are accepted as the authorized original evidence; no internet fetch or external provenance verification was performed.','The full-bank review uses only exact fixed bank questions and authorized original rules/supplements. No existing broad audit or reader artifact was consulted.','Incidental nonquestion metadata embedded in allowed JSON files is not evidence of any actual runtime, score or approval state.','A per-atom source reference may point to a shared complete procedure quote; supporting evidence is centralized in the registry to avoid duplicating the same original passage hundreds of times. Native graphic tables are transcribed from the original PDF, not from existing audit crops.']}
# Re-read only inputs to confirm no mutations, not reader/status data.
all_inputs=[RULES,PDF,QUESTIONS,KEY,SCOPE,PRE,errata_path,RUN/'supplements/official-errata-original-post.txt',foreign_path,thread_path,human_path,approved_path,board_path,front_path,back_path]
hashes={str(p):sha(p) for p in all_inputs}
for p,h in preserved.items():assert sha(Path(p))==h
hash_record={'created_at_utc':now,'algorithm':'SHA-256','authorized_inputs_and_staged_prereview':hashes,'preserved_two_question_artifacts':preserved,'all_preserved_two_question_hashes_unchanged':True}
(OUT/'full-bank-input-hashes.json').write_text(json.dumps(hash_record,ensure_ascii=False,indent=2)+'\n')
read_record={'created_at_utc':now,'sequence':['Read all exact questions; authored/saved full-bank-question-only-prereview.json before full key/scope.','Read every full-bank expected_answer and all 919 material_requested_facts in bounded batches; repeated the few truncated boundary entries.','Read original extracted Rules physical LF1–2930 (blank lines suppressed only in display; original indices use split("\\n")); relevant text procedures complete through p41, with p42 inspected visually in full.','Read full allowed errata/original post and original Foreign Invasion/Fraud ruling bodies; read exact human interpretation records.','Extracted native authorized PnP PDFs; visually inspected original board, original scenario cards p9, Rules p33 circle and p42 charter at enlarged scale.','Authored row/atom verdicts, exact corrections and coverage consequences; checked 113/919 accounting and preservation hashes.'],
 'read_original_rules_text':{'path':str(RULES),'physical_LF_ranges':[[1,900],[901,1750],[1750,2330],[2330,2930]],'numbering':'text.split("\\n"), one-based'},
 'original_pdf_visual_inspection':[{'path':str(board_path),'pages':[1],'artifacts':['full-bank-board-native-overview.png','full-bank-board-native-left.png']},{'path':str(PDF),'pages':[33,42],'artifacts':['full-bank-rules-page-33.png','full-bank-rules-page-42.png','full-bank-rules-charter-value-zoom.png']},{'path':str(front_path),'pages':[9],'artifacts':['full-bank-scenario-cards-fronts-p9.png']}],
 'original_pdf_text_inspection':[{'path':str(front_path),'pages':[1,2,5,6,7,9]},{'path':str(back_path),'pages':[9]},{'path':str(board_path),'pages':[1],'note':'Text extraction omits outlined numbers; use native visual inspection for values.'}],
 'original_supplements_read':[str(p) for p in [errata_path,RUN/'supplements/official-errata-original-post.txt',foreign_path,thread_path,human_path,approved_path]],
 'bank_files_read':[str(QUESTIONS),str(KEY),str(SCOPE)],'infrastructure':'Used existing project .venv PyMuPDF for native PDF rendering after default Python lacked it; no additional source content or existing QA image was opened. No dependency installation succeeded or was needed.',
 'not_read':'No canonical rules markdown, summary, reader response, grade, prior broad audit/review/history, neighboring QA artifact, actual runtime/status or collaboration tool was opened.',
 'source_evidence_registry':E}
(OUT/'full-bank-source-read-record.json').write_text(json.dumps(read_record,ensure_ascii=False,indent=2)+'\n')
(OUT/'full-bank-source-scope-review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
# Human-readable report includes all 919 atom rows and a complete original-source quote appendix.
md=['# Full-bank independent source/question scope challenge — v1','',f"Reviewed **113 questions and all 919 current mandatory atoms**: **{counts['affirmed_requested_or_clearly_implied']} affirmed**, **17 with explicit findings**. No sample, readers, grades or summaries were used. The original two-question review remains unchanged.",'',
'One literal source error concerns the setup office-card destination. Three wording clarifications preserve genuinely asked source conditions/type/timing. Ten fully contextual atoms and three mixed atoms require scope correction. Most contextual facts are explicitly covered by other exact questions. **CG-01 flags ordinary Company expense funding/debit as a narrow meaningful coverage gap after moving the unasked Q100 Balance instruction to context.**','',
'## Independence and staging','',report['independence'],'',report['staging']['method'],'',
'`full-bank-question-only-prereview.json` was saved before the full answer key and scope were opened. All five prior review artifacts are preserved byte for byte; see the new input-hash record. The prior Q041/Q100 judgments are incorporated without modifying their original files.','',
'## Exact proposed corrections','', 'Proposal version: `full-bank-source-asked-scope-v1`. These are recommendations only. Correct fuller expected answers may retain optional explanations; mandatory-scope corrections do not authorize changing any live artifact.','']
for f in F.values():
 md.extend([f"### {f['finding_id']} — {f['category']}",'',f"Question: {f['exact_question']}",'',f"Requested phrase: “{f['exact_question_phrase']}”",'',f"Before (atom {f['mandatory_atom_index_1_based']}): {f['exact_before']}",'',f"After mandatory scope: {f['exact_after_mandatory'] if f['exact_after_mandatory'] is not None else 'Move to optional context; no independent mandatory clause.'}",'',f"Source truth: **{f['source_truth_verdict']}**. Evidence: "+', '.join(f['source_evidence_ids'])+'.','',f['independent_reason'],'','Coverage consequence: '+f['coverage_consequence'],''])
md.extend(['## Coverage gap','', '**CG-01 — '+coverage_gap['core_procedure']+'**','',coverage_gap['assessment'],'',coverage_gap['action'],'',
'## Complete 113-question / 919-atom accounting','', 'Each row below cites the exact original question, a row-specific scope rationale and original-source registry IDs. Every current atom has a separate verdict. Shared IDs resolve to exact original quotations/pages/LF ranges in the appendix. Equivalent wording and clear implications satisfy overlapping atoms without a demand for repeated sentences.',''])
def escape(s):return str(s).replace('|','\\|').replace('\n',' ')
for r in rows:
 md.extend([f"### {r['id']} — {r['mandatory_atom_count']} atoms; {r['row_verdict']}",'',r['exact_question'],'',r['question_scope_rationale'],'','Original source evidence: '+', '.join(r['source_evidence_ids'])+'.','', '| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |','|---|---|---|---|---|'])
 for a in r['mandatory_atom_reviews']:
  md.append('| '+ ' | '.join(escape(x) for x in [a['atom_id'],a['proposed_mandatory_fact'],a['source_truth_verdict'],a['asked_scope_verdict'],', '.join(a['source_evidence_ids'])+(' / '+a['finding_id'] if 'finding_id' in a else '')])+' |')
 md.append('')
 specific=[a for a in r['mandatory_atom_reviews'] if a.get('specific_acceptance_or_source_note')]
 for a in specific:md.extend([f"{a['atom_id']}: {a['specific_acceptance_or_source_note']}",''])
 if r['existing_contextual_extras_review']['extras']:md.extend(['Existing optional key context (not promoted to mandatory): '+ '; '.join(r['existing_contextual_extras_review']['extras'])+'.',''])
md.extend(['## Source quote and graphic-transcription appendix','', 'LF indices refer to the original extraction split on literal newline (`text.split("\\n")`), not `splitlines()`. Native graphic transcriptions are identified as such and are not presented as prose quotations.',''])
for id,e in E.items():
 md.extend([f'### {id}','',e['source_path'],''])
 loc=[]
 if 'printed_pages' in e:loc.append('Rules printed p'+','.join(map(str,e['printed_pages'])))
 if 'physical_LF_start' in e:loc.append(f"physical LF{e['physical_LF_start']}–{e['physical_LF_end']}")
 if 'pdf_page' in e:loc.append(f"PDF p{e['pdf_page']}")
 if 'original_url' in e:loc.append(e['original_url'])
 md.extend([e['evidence_kind']+('; '+ '; '.join(loc) if loc else ''),''])
 if 'quote' in e:md.extend(['> '+e['quote'].replace('\n','\n> '),''])
 if 'transcription' in e:md.extend([e['transcription'],''])
 if 'transcribed_table' in e:md.extend(['```json',json.dumps(e['transcribed_table'],ensure_ascii=False,indent=2),'```',''])
 if 'visual_artifact' in e:md.extend(['Visual evidence: '+e['visual_artifact'],''])
 if 'note' in e:md.extend([e['note'],''])
md.extend(['## Limits and preservation',''])
for x in report['limitations']+report['source_truth_inference_limits']:md.append('- '+x)
md.extend(['',report['prohibited_mutations'],''])
(OUT/'full-bank-source-scope-review.md').write_text('\n'.join(md))
# Remove only this review's failed dependency-cache directories; leave all original artifacts and sources alone.
for n in ['.full-bank-pdf-runtime','.full-bank-uv-cache']:
 p=OUT/n
 if p.exists():shutil.rmtree(p)
for n in ['full-bank-question-only-prereview.json','full-bank-source-read-record.json','full-bank-input-hashes.json','full-bank-source-scope-review.json']:
 readj(OUT/n)
for p,h in preserved.items():assert sha(Path(p))==h
print(json.dumps({'questions_reviewed':len(rows),'atoms_accounted':len(all_atoms),'verdict_counts':dict(counts),'findings':len(F),'preserved_previous_artifacts':True,'saved':['full-bank-question-only-prereview.json','full-bank-source-scope-review.json','full-bank-source-scope-review.md','full-bank-source-read-record.json','full-bank-input-hashes.json']},indent=2))
