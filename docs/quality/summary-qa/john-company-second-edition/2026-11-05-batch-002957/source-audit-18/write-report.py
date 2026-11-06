from pathlib import Path
import hashlib,json,datetime
O=Path(__file__).resolve().parent; R=O.parents[5]; RUN=O.parent
S=O/'summary-snapshot.md'; live=R/'rules/john-company-second-edition.md'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
expected='7bf5b6a937cdfba4eced73c67722de7c0af63f158d6444a20e21ebbbc667368d'
assert sha(S)==sha(live)==expected
readfile=O/'source-read-record.json';old=json.loads(readfile.read_text()); reads=old if isinstance(old,list) else old['text_reads']
by={}
for rec in reads:
 assert sha(Path(rec['path']))==rec['sha256']
 by.setdefault(rec['path'],set()).update(range(rec['start_physical_LF'],rec['end_physical_LF']+1))
assert set(range(1,494))<=by[str(S)]
assert set(range(1,3017))<=by[str(R/'extracted/john-company-second-edition-rules.txt')]
assert all(x['end_physical_LF']-x['start_physical_LF']<50 for x in reads)
provenance=json.loads((O/'native-derivative-provenance.json').read_text())
for rec in provenance['records']:
 assert sha(Path(rec['source']))==rec['source_sha256'] and sha(Path(rec['derivative']))==rec['derivative_sha256']
visual=[]
notes={
 'rules-physical-page-29.png':'Region Loss sequence, exhausted Army example and control token facing.',
 'rules-physical-page-33.png':'Attack order, substitutes, printed Mounting Defense wording and Foreign Invasion circle shape.',
 'rules-physical-page-42.png':'Firm dividends/expenses, strategy, charter scoring anatomy.',
 'board-physical-page-1.png':'Prize costs/upkeep/VP/windows; initial Power; ordered two zero slots; queue path; Court default VP; Standing/Debt lined and starred spaces; dates; ribbon and sea zones.',
 'bridge_fronts-physical-page-1.png':'Corrected Company Fraud timing and cap wording; Mercantile and Diplomatic zero-dice failures.',
 'bridge_fronts-physical-page-6.png':'Corrected Military Oversight demotion/reappointment and card-specific hiring/Nepotism; Public Demands Impeachment destinations.',
 'bridge_fronts-physical-page-9.png':'1710/1758/1813 setup fronts, corrected control/share markers and Governor General instructions.',
 'bridge_backs-physical-page-9.png':'Three scenario map reverses, closed orders, Elephant positions, flags and 1758 Bengal Governor; printed sheet 20.',
 'firm-value-track.png':'Value 1:-1; 2:0; 3–4:1/2; 5–7:1; 8–9:1 1/2; 10:2.',
 'glencora-card.png':'Recovered extraction U+001E at physical LF1067: native text says 4+ vacancies.'}
for rec in provenance['records']:
 visual.append({**rec,'visually_checked':True,'observations':notes[Path(rec['derivative']).name]})
for n,note in [('board-company-track-details.png','Standing thresholds and initial Power slots.'),('board-left-details.png','Prize and scenario-end/Power award values.'),('cards-Bridge-Fronts-page-9.png','Scenario setup values.')]:
 p=RUN/'supplements/images'/n;visual.append({'path':str(p),'sha256':sha(p),'visually_checked':True,'observations':note,'note':'Provided native crop consulted; conclusions also checked against own rendering of original PDF.'})
coverage=[
 ('Scope, components, limits, cash, public information','17–34','Rules pp1–8; physicalLF1–807'),
 ('All four standard scenario procedures; setup dealing and placements','36–61','Rules pp4–5 physicalLF334–494; native board PDFp1; Bridge Fronts PDFp9; Bridge Backs PDFp9 (printed20); errata physicalLF192–204'),
 ('Prize/Power/Standing/Debt/Stock Exchange/scenario numeric tracks','50–73,109,422,433','native board PDFp1; native Rules p42 chart; Rules p36 physicalLF2588–2601'),
 ('Turn sequence and eligible start-of-turn vote','75–77','Rules pp10,36–38 physicalLF861–887,2588–2601,2678–2688'),
 ('Attrition, retirement, prestige, spouses and discounts','79–89','Rules pp11–12 physicalLF897–1051; p37 physicalLF2651–2674'),
 ('Family action marker, extra actions, no-action, reuse and action costs','91–111','Rules pp13–14 physicalLF1075–1145'),
 ('Hiring pools, fatigue, Nepotism, vacancies and Chairman election','113–138','Rules pp14–16 physicalLF1146–1268'),
 ('Operation navigation, treasury payments and checks','140–146','Rules p17 physicalLF1330–1365; p20 physicalLF1527–1554'),
 ('Bonuses and Company Revenue, debt-cap loans, expectations/dividends','148–160','Rules p27 physicalLF1893–1934; p42 physicalLF2895–2902'),
 ('Storms, exposure and sequential event draws','162–176','Rules p28 physicalLF1938–1961; p25 physicalLF1812–1815; p42 physicalLF2919–2922'),
 ('Writer loss, Cascade recursion and all seven event branches','178–188','Rules pp28,31–33 physicalLF1962–1975,2108–2316; designer article42192767'),
 ('Ordinary Crisis classifier, empire strength/decline and March','190–194,221','Rules pp7,30,32 physicalLF705–727,2044–2082,2185–2219'),
 ('Primary/secondary Company attacks, substitutes, defense outcomes','196–219','Rules pp22,29,33 physicalLF1622–1626,1986–2012,2261–2296; accepted human authority governs >= comparison; designer article42192767 governs Foreign Invasion unrest'),
 ('Parliament drawing, policy selection, vote rounds, coalition and resolution','223–238','Rules pp34–36 physicalLF2329–2367,2524–2587'),
 ('Upkeep, final turn and full Refresh destinations','240–252','Rules p36 physicalLF2602–2621'),
 ('Chairman borrowing/allocation, envoys/transfers, Shipping','256–266','Rules pp18–19 physicalLF1402–1433,1456–1471; p25 physicalLF1812–1815'),
 ('Military Affairs transfers, new officers and Commander selection','268–270','Rules p19 physicalLF1472–1520'),
 ('Presidency uninterrupted operations, trade capacity/routes/rewards','272–278','Rules pp20–21 physicalLF1527–1582; p40 physicalLF2817–2820'),
 ('Local alliances; repeated Deploy; losses; loot cycles and governance','280–315','Rules pp22–23 physicalLF1616–1710; p7 physicalLF713–714; p26 physicalLF1842–1847'),
 ('Governor diminishing checks, ship stages, regiments and tax','317–332','Rules p24 physicalLF1738–1771'),
 ('China creation/check limit/export scaling','334–345','Rules p25 physicalLF1806–1823'),
 ('Governor General transformation, Govern sequence and limits','347–351','Rules p26 physicalLF1839–1889'),
 ('Deregulation special vote and share-value cap','353–362','Rules p36 physicalLF2588–2601; native board PDFp1'),
 ('Firm treasuries, investments, ships, takeover, mergers and dissolution','364–379','Rules pp37–39 physicalLF2625–2768; p41 physicalLF2839–2855'),
 ('Firm strategies, initiative, competitive routes and revenue/value','381–398','Rules p40 physicalLF2772–2822; p42 physicalLF2919–2922'),
 ('Firm expenses, rescue, dividends and Hobnob marker','400–406','Rules pp41–42 physicalLF2826–2855,2887–2918'),
 ('Final Scoring order, Power, Court, failure, firm aggregation and ties','408–435','Rules p9 physicalLF811–853; p37 physicalLF2665–2674; p41 physicalLF2839–2843; native board and p42 firm chart'),
 ('Negotiations, share replacement, promises and final-scoring restrictions','437–456','Rules p8 physicalLF756–807; p9 physicalLF836–847'),
 ('Human interpretation fidelity and attribution','202–217,458–464','human-defense-interpretation-source.json physicalLF5–11; user-approved-scope.json physicalLF5–25; Rules p22 physicalLF1622–1626 and p33 physicalLF2285–2296'),
 ('Company Fraud, Foreign Invasion and included official card corrections','468–474','full-official-errata.txt physicalLF192–247; original-post physicalLF17–61; ruling-thread-2938749.json physicalLF1 articles40838655/40850873; foreign-invasion-designer-ruling.json physicalLF1 article42192767; native Bridge Fronts PDFpp1,6,9'),
 ('Publisher chain and source edition','7,10,474,492','publisher-resources.html physicalLF3065–3076; publisher-pnp-download-provenance.json physicalLF1–8; full-official-errata-provenance.json physicalLF1–18; official-errata-original-post.txt physicalLF59–62; Rules p48 physicalLF3300')]
app=[
 {'application':'Firm special retirements qualify for London display selection.','basis':'Rules p37 physicalLF2651–2660 says otherwise like any retirement; p12 physicalLF1003–1014 controls selection and exhausted display.','assessment':'Justified source application, not a guess.'},
 {'application':'Company-controlled Deploy has zero tower trophies and surviving-officers+1 minimum loot.','basis':'Rules p22 physicalLF1630–1647 explicitly permits such targets with effect and zero defense; p23 physicalLF1675–1696 supplies loot minimum/trophies.','assessment':'Justified source application.'},
 {'application':'Successful Governor General cash is a family bonus from bank.','basis':'Rules p6 physicalLF662–668 explains highlighted personal extra-income boxes; p26 physicalLF1870–1872 is the corresponding highlighted payment.','assessment':'Justified source application.'},
 {'application':'Firm scoring rounds each player’s aggregate once and precedes special retirement/ordinary scoring.','basis':'Rules p37 physicalLF2665–2674; debtor penalty fixed at -1 by p41 physicalLF2839–2843.','assessment':'Justified source application.'},
 {'application':'Last dominated-region loss removes surviving capital flag irrespective of event.','basis':'Rules p7 physicalLF713–714 says if ever reduced to only capital; it applies to Rebellion and Company conquest as well as ordinary Invasion.','assessment':'Justified source application.'},
 {'application':'Only the newly exhausted combined defense strength >= attack controls Crisis defense.','basis':'Explicit human authority in both read and hashed scope files; not inferred from printed equal wording. Local-alliance indivisibility remains Rules p22 physicalLF1622–1626.','assessment':'Authorized interpretation; faithfully attributed. No publisher email verification dependency or citation-based cap.'}
]
record={'physical_line_rule':"UTF-8 text.split('\\n'); numbering is physical LF, never splitlines().",'maximum_physical_lines_per_read':50,'text_reads':reads,'native_visual_reads':visual,'coverage':{'candidate_complete':True,'candidate_physical_LF_lines':493,'multiplayer_rules_complete':True,'multiplayer_rules_physical_LF_range':[1,3016],'edition_identification':[3252,3306],'excluded_source':'Rules pp43–46 Crown and optional Draft procedure; optional Draft lines encountered only incidentally on setup page.','U+001E':{'physical_LF_line':1067,'handling':'Counted as part of one physical LF line; native p12 crop recovers 4+ vacancies.'}},'truncation':'No missing or truncated relevant physical-LF text remained; native shape/chart/RS information recovered visually.'}
readfile.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
verdicts={'official_claims':'PASS','human_interpretation_fidelity':'PASS','overall_scoped_result':'PASS','scoped_signoff':True,'unqualified_independently_verified_official_core_signoff':False,'publisher_email_signoff':False,'publisher_email_independently_verified':False}
audit={'audit':'Fresh independent source-only final audit 18','completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'candidate':str(live),'snapshot':str(S),'snapshot_sha256':expected,'scope':{'players':'Standard 3–6-player multiplayer','scenarios':['1710','1758','1813','Long 1710'],'firms':'Included','normative_authorities':'Official originals and included official corrections/rulings, plus explicit human >= newly exhausted defense-strength interpretation.','component_boundary':'Individual powers, exact dealt holdings and scenario map configurations read from components; common procedures and included corrected-card effects audited.','excluded':['Crown','solo','two-player','optional Draft']},'machine_verdicts':verdicts,'findings':[],'finding_counts':{'critical':0,'major':0,'minor':0,'total':0},'coverage':[{'area':a,'summary_physical_LF':b,'controlling_original':c,'result':'PASS'} for a,b,c in coverage],'justified_source_applications':app,'independence':{'candidate_frozen_before_reading':True,'only_permitted_source_evidence_consulted':True,'no_parent_history_or_qa_evidence_used':True,'no_web_or_communication_used':True,'technical_renderer_discovery':'Designated source-audit-16/runtime did not exist. Found and imported package files only from /tmp/joco-source-pdf; no neighboring game or audit content accessed.','canonical_or_other_evidence_edited':False},'stability':{'candidate_matches_snapshot':True,'expected_live_sha256':expected,'text_source_hashes_verified':True,'native_source_and_derivative_hashes_verified':True,'completion_verification_file':'verification.json'},'provenance_files':['manifest.json','native-derivative-provenance.json','source-read-record.json','verification.json']}
(O/'source-audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
md=['# Independent source-only final audit 18','','**PASS for the authorized scope. Zero findings.** Official claims: PASS. Human-interpretation fidelity: PASS.','','Audited standard 3–6-player multiplayer across 1710, 1758, 1813 and Long 1710, including firms. Individual component powers/dealt holdings/maps remain component references as authorized; common procedures and included corrected-card effects were checked. Crown, solo/two-player and optional Draft are excluded.','','The >= defense comparison is expressly attributed to the user and agrees with both hashed human-authority files. This scoped signoff does not assert independently verified publisher email or unqualified independently verified official-core accuracy. No further email or public-verification dependency was imposed.','','Snapshot SHA-256: `'+expected+'`. Candidate and snapshot match. No canonical or other evidence was edited.','','## Evidence and coverage','','The entire 493-physical-LF candidate and every physical LF of multiplayer Rules pp1–42 (1–3016) were read in separate responses bounded to 50 physical LF lines. The printing statement on Rules p48 was also checked. Physical line numbering uses `text.split("\\n")`; U+001E at physical LF1067 remains within its original line, with native p12 recovering “4+ vacancies.” All relevant full errata text, provenance, original designer post, exact two rulings and both human scope files were read. Publisher links were checked in the preserved publisher resource HTML. Native originals were rendered and visually checked for charts, setup cards/maps and corrected effects. No truncated or missing relevant text remains.','','| Area | Summary physical LF | Controlling originals |','|---|---|---|']
for a,b,c in coverage:md.append('| '+a+' | '+b+' | '+c+' |')
md+=['','','## Source applications','','These applications are supported rather than guessed:']
for x in app:md.append('- '+x['application']+' '+x['basis']+' '+x['assessment'])
md+=['','','## Findings','','None. Critical 0; major 0; minor 0.','','## Integrity and artifacts','','`manifest.json` records all consulted source hashes and derivative/artifact hashes. `native-derivative-provenance.json` records original PDFs, physical pages, printed-page distinctions, rendering scales and crop bounds. `source-read-record.json` contains every bounded text read and native visual inspection. `verification.json` records the completion rehash and live-candidate equality.','','The designated source-audit-16/runtime package directory was absent. Technical renderer discovery found PyMuPDF package files under `/tmp/joco-source-pdf`; no neighboring audit or game evidence was opened.']
(O/'source-audit.md').write_text('\n'.join(md)+'\n')
for name in ['bridge_fronts-physical-page-4.png','bridge_fronts-physical-page-5.png']:
 p=O/name
 if p.exists():p.unlink()
sources={Path(x['path']) for x in reads if Path(x['path'])!=S}
for x in provenance['records']:sources.add(Path(x['source']))
for x in visual:
 if 'path' in x:sources.add(Path(x['path']))
sources.add(live)
entries=[{'path':str(p),'role':'source','bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(sources)]
entries +=[{'path':str(p),'role':'snapshot' if p==S else 'derivative_or_audit_artifact','bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(O.iterdir()) if p.is_file() and p.name not in ['manifest.json','verification.json']]
manifest={'sha_algorithm':'SHA-256','candidate_sha256':expected,'entries':entries,'self_reference_policy':'manifest and final verification excluded from artifact entries to avoid recursive hashes; verification records manifest hash.'}
(O/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
checks=[{'path':x['path'],'expected':x['sha256'],'actual':sha(Path(x['path'])),'matches':sha(Path(x['path']))==x['sha256']} for x in entries]
assert all(x['matches'] for x in checks)
assert sha(live)==sha(S)==expected
verification={'verified_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'all_recorded_hashes_match':True,'candidate_live_matches_frozen_snapshot':True,'live_sha256':sha(live),'snapshot_sha256':sha(S),'manifest_sha256':sha(O/'manifest.json'),'checks':checks}
(O/'verification.json').write_text(json.dumps(verification,indent=2)+'\n')
print(json.dumps({'verdicts':verdicts,'findings':0,'snapshot_sha256':expected,'verified_entries':len(checks),'source_reads':len(reads),'native_checks':len(visual),'report':str(O/'source-audit.md')}))
