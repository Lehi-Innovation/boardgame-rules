from pathlib import Path
import hashlib,json,datetime
R=Path('/home/jonny/projects/boardgame-rules')
A=R/'docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/source-audit-15'
Q='docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957'
S=Q+'/supplements/'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
log=json.loads((A/'source-read-record.json').read_text())
snapshot_sha=sha(A/'summary-snapshot.md')
assert snapshot_sha=='2060a7965d422e2ecfcf20b5201dadb52cf5efb135c2df0f6be0ceb2cb72d316'
assert sha(R/'rules/john-company-second-edition.md')==snapshot_sha
sources={v['path']:v['sha256'] for v in log['reads'] if v['path']!=str(R/'rules/john-company-second-edition.md')}
for path,h in sources.items():assert sha(Path(path))==h

def evidence(candidate,source,anchor,quote,assessment):
 return {'candidate_lines':candidate,'source':str(R/source),'anchor':anchor,'exact_quote':quote,'assessment':assessment,'verdict':'PASS'}
checks=[
evidence([21,61],S+'pnp/Cards/John Company Cards (Bridge, Fronts).txt','Scenario cards 74–76, native PDF p9; original board turn/Standing/Debt tracks','Place the Bengal control token in the Bengal Presidency.','All four scenario scopes, initial treasuries/laws/military/Company ships, corrected control/share-value tokens, final turn marks, Power rates, prize costs/upkeep/windows and lined/starred thresholds agree. Exact starting personal holdings and India configurations are explicitly delegated to the components.'),
evidence([75,87],'extracted/john-company-second-edition-rules.txt','Rules pp10–12, London Season / Prestige Cards, logical lines 897–1042','If there are no cards remaining in the display, all remaining players are skipped.','Phase order, first-turn skip, attrition modifiers, retirement payment timing, display priority, no immediate replacements, full end-step discard/refill and spouse/blackmail limits agree.'),
evidence([91,136],'extracted/john-company-second-edition-rules.txt','Rules pp13–16, Family / New Company Shares / Hiring, logical lines 1076–1255','This does not apply to electing the Chairman.','Opportunity-marker timing, once-per-turn vacancy bonus, costs, stock queue, forced prize reuse, ascending promotion order, vacancy behavior, Chairman election/empty Court and normal Commander exemption agree. Office cards remain the source for printed candidate pools.'),
evidence([140,158],'extracted/john-company-second-edition-rules.txt','Rules p17 Success Checks and p27 Revenue, logical lines 1331–1366 and 1894–1935','If the Company Debt marker is already on the rightmost space, you still take out emergency loans','Office treasury ownership, no dead actions, check outcomes, normal catastrophe, Revenue costs, emergency loans at maximum Debt, Standing penalties and strict dividend enthusiasm threshold agree.'),
evidence([252,274],'extracted/john-company-second-edition-rules.txt','Rules pp18–21, office operations / Trade, logical lines 1403–1613','Each President may only successfully trade at most once per game turn.','Chairman debt/allocation, envoy-before-transfers, Shipping costs/bank recipient/mandatory spending, Military Affairs order and Presidency interruption boundaries agree. Trade uses its own connected route, writers before tokens, one order per ship and Presidency home privileges.'),
evidence([276,311],'extracted/john-company-second-edition-rules.txt','Rules pp22–23, Commanders / Deploy / successful control, logical lines 1617–1711','Each piece can only be used once on the turn they are purchased','Alliance purchase/consent and whole-piece exhaustion, legal deployment targets, full empire penalty, officer loss checks per attempt, loot minimum/cycling/bank shares, trophies and ordered destinations of control token/overlay/card agree. Reopening an already controlled region retains minimum loot and no tower trophies.'),
evidence([313,347],'extracted/john-company-second-edition-rules.txt','Rules pp24–26, Governors / China / Governor General, logical lines 1739–1890','Then lower the number of dice in the pool by 1 regardless of its result.','Governor shrinking pools, unrest and bonus timing, two separate shipbuilding successes, regiment/Tax destinations; China creation/immediate hiring/single attempt/export scaling; and Governor General conversion/check/benefit limits agree.'),
evidence([160,198],'extracted/john-company-second-edition-rules.txt','Rules pp28–33, Storms / Cascades / Events / Crisis / Foreign Invasion','Each region can only Cascade once during the resolution of each event tile.','Storm eligibility/results, event draw and location rules, Cascade receiving/initiation distinction, every event type, normal Invasion/Rebellion strict comparisons, empire destruction/decline and separate primary/secondary Company attack strengths agree.'),
evidence([200,219],'extracted/john-company-second-edition-rules.txt','Rules p29 Region Loss; p30 Elephant’s March; p33 Vacant Commander','The player acting as Commander will not lose or gain trophies.','Commander/Military Affairs/Chairman substitution, trophy consequences, rout, Governor removal, spent loot token orientation, loss of association, cumulative Standing losses, phase completion on failure and Elephant routing agree. The defense comparator itself is separately judged against the accepted human source.'),
evidence([221,248],'extracted/john-company-second-edition-rules.txt','Rules pp34–36, Parliament / Voting / Upkeep and Refresh','The Prime Minister must stop at the first space that matches the icon','Law draw/dilemma stopping, pre-vote policy selection, card votes once across rounds, opposition/coalitions/PM restrictions, zero-pass threshold, policy-before-law order, tax/bonus recipients and complete upkeep/refresh timing agree.'),
evidence([349,396],'extracted/john-company-second-edition-rules.txt','Rules pp36–42, Deregulation / Firms','A firm with 10 shares may still be invested in, but will not create any further shares.','Deregulation timing/result boundaries; London versus India funds; shareholder special retirement; investment restrictions, takeover/merger/dissolution; one trade attempt, secret strategy/revealed bid, initiative/ties, route/ship+1/repeated-order revenues; expenses/emergency rescue/dividends/marker/Hobnob/storms agree.'),
evidence([398,425],'extracted/john-company-second-edition-rules.txt','Rules p9 Final Scoring; p37 Firms in Final Scoring; p42 charter diagram','Then, regardless of Company success or failure, shareholders may perform one special retirement','Firm scoring with per-player final rounding and Debtor’s Prison precedes special firm retirement, then ordinary power/Court/outcome scoring. Board and charter confirm rates and tie awards. Company success/failure, final attrition versus random failure card, windows and PM-order ties agree.'),
evidence([429,446],'extracted/john-company-second-edition-rules.txt','Rules p8 Negotiation; p9 Game End','Negotiations involving immediate transfers are binding.','Transferable assets, family-piece replacement on share trades, private blackmail peeks, no repeated activation, promise timing/conflicts and no negotiations/promises at Final Scoring agree.'),
evidence([460,464],S+'full-official-errata.txt','Official internal errata, core/setup/card corrections; original official post; allowed original ruling thread articles 40850873 and 42192767','If reduced to zero dice, treat roll as failure.','Applicable procedural and setup errata are incorporated. Company Fraud cap and corrected Revenue timing, Foreign Invasion unrest/tower and single-closure ruling, impeachment destinations and former-Commander eligibility are accurate. Dates and article attribution match the retained originals.'),
evidence([208,215],Q+'/human-defense-interpretation-source.json','Exact human messages and normative authority, lines 5–11','Just accept my answer. You can note it as my interpretation.','Total newly exhausted defense strength at least attack defeats the Crisis, including full alliance strength. The strength-2 versus strength-1 example applies it correctly, preserves normal successful-defense consequences and does not reuse an exhausted alliance.'),
evidence([448,454],Q+'/human-defense-interpretation-source.json','Human normative authority and provenance, lines 10–11','"publisher_email_independently_verified": false','The candidate expressly labels this user-supplied interpretation and never claims independently verified publisher/designer/email authority for it. The reported private email is provenance only and creates no citation blocker in this scoped audit.')
]
report={
 'audit_id':'source-audit-15','audit_kind':'new independent final source-only audit','created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'candidate':str(R/'rules/john-company-second-edition.md'),'snapshot':str(A/'summary-snapshot.md'),'summary_sha256':snapshot_sha,
 'scope':'Official standard 3–6-player multiplayer core, all 1710/1758/1813/Long 1710 scenarios and firms, plus the exact attributed human total-newly-exhausted defense strength >= attack interpretation. Used with printed components for their individual powers/restrictions, values, holdings and map configurations. Crown and optional draft excluded.',
 'independence':{'repair_or_key_or_grading_role':False,'candidate_edited':False,'prior_reviews_or_history_consulted':False,'web_research_used':False,'reader_or_reviewer_contact':False,'communication_or_status_tools_used':False},
 'independent_official_claims_verdict':'PASS',
 'independent_official_claims_boundary':'PASS for official claims within the declared procedural summary and component-authoritative scope, excluding the expressly identified human defense comparator. This is not an unqualified all-official-core or independently verified email signoff.',
 'user_interpretation_fidelity_verdict':'PASS','overall_scoped_verdict':'PASS','scoped_signoff':True,
 'unqualified_independently_verified_official_core_signoff':False,'publisher_email_independently_verified':False,'new_public_publisher_citation_required':False,
 'findings':[],'severity_counts':{'critical':0,'major':0,'minor':0,'material':0},
 'conclusion':'No material source, fidelity or attribution issue found in the frozen candidate within the assigned normative scope.',
 'coverage':log['scope_coverage'],'source_checks':checks,
 'source_hierarchy_notes':[
 'The assigned Second Printing rulebook and applicable official errata/rulings govern over abbreviated or older component-aid wording, including Region Loss closing only for a normal Invasion Crisis.',
 'The human source is accepted normative for the defense-strength comparator. Rules p33 literally uses equality language; the summary makes the user-attributed >= interpretation explicit. This difference is intentional and is not scored as a defect.',
 'Individual printed law/card exceptions remain operative under the explicit component-authoritative boundary. In particular Military Oversight uses its printed hiring/Nepotism procedure, Royal Protection can cancel emergency loans, and Deregulation uses its printed support icons. The general ordinary procedures do not displace those printed effects.',
 'Company Fraud ruling article 40850873 selects alternative 2 from the original question (Balance 10, doubled roll 12 => payout 10); the retained 2023 Foreign Invasion ruling excludes unrest from its primary roll and resulting towers.'
 ],
 'read_record':str(A/'source-read-record.json'),'output_truncations':[],'unresolved_source_questions':[]
}
(A/'source-audit.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
lines=[
 '# Independent source-only audit 15',
 '',
 '**Overall scoped verdict: PASS. Scoped signoff: true.** No material source, fidelity or attribution issue found.',
 '',
 f'Frozen candidate SHA-256: `{snapshot_sha}`.',
 '',
 'Independent official-claims verdict: **PASS within the declared procedural/component scope**. User-interpretation fidelity: **PASS**. Unqualified independently verified official-core signoff: **false**. Publisher email independently verified: **false**; no additional public citation is required for the accepted human interpretation.',
 '',
 'The scope is standard multiplayer for 3–6 players, every standard scenario and firms, plus the exact attributed human defense comparator. Crown and optional draft are excluded. Individual component powers/restrictions, holdings, printed values and India configurations remain component-authoritative.',
 '',
 'The full 482-line candidate and all assigned rulebook text through page 42 (logical lines 1–3015) were read without gaps. Twenty-two native original PDF views covered rulebook/action/map/event/firm diagrams, both player-aid faces, the board, scenario fronts/backs, law cards and firm charter. Applicable errata, both designer rulings and original publisher provenance were inspected. All source hashes are in manifest.json. No previous review, repair, answer key, reader, grade or history artifact was consulted; the candidate was not edited.',
 '',
 'There are **no findings** at any severity. The following checks document the evidence supporting the verdict.',
 '',
 '| Candidate lines | Original source anchor | Result |',
 '|---|---|---|'
]
for v in checks:
 lines.append('| '+str(v['candidate_lines'][0])+'–'+str(v['candidate_lines'][1])+' | '+v['anchor'].replace('|','/')+' | '+v['assessment'].replace('|','/')+' |')
lines += ['', 'The JSON audit retains exact supporting quotes and source paths for these checks. Its absence of findings does not claim that the private email was inspected. The rulebook’s printed equality wording and the user’s adopted strength comparison remain distinctly attributed.', '', 'Source precedence and printed exceptions:', '']
for n in report['source_hierarchy_notes']:lines.append('- '+n)
lines += ['', 'Read limits and completeness: all displayed text outputs stayed within safe token caps. No output was truncated; no recovery was required. The read record documents every text range and each viewed native derivative. Text line numbers use Python str.splitlines(); page and section names are the primary human anchors.', '', 'Native rendering used PyMuPDF 1.28.2 installed temporarily inside this audit folder. No web-source research was performed. The original candidate and frozen snapshot hashes still match at audit completion.', '']
(A/'source-audit.md').write_text('\n'.join(lines))
manifest={'audit_id':'source-audit-15','summary_sha256':snapshot_sha,'candidate':str(R/'rules/john-company-second-edition.md'),'snapshot':str(A/'summary-snapshot.md'),'candidate_sha256_at_completion':sha(R/'rules/john-company-second-edition.md'),'source_hashes':sources,'artifacts':{},'renderer':'PyMuPDF 1.28.2','scope':'Official multiplayer pp1–42/all standard scenarios/firms plus attributed human defense interpretation','native_pdf_derivatives':[]}
for p in sorted(A.glob('*.png')):manifest['native_pdf_derivatives'].append({'path':str(p),'sha256':sha(p)})
for name in ['summary-snapshot.md','source-audit.json','source-audit.md','source-read-record.json','read_source.py','build_audit.py']:
 manifest['artifacts'][name]=sha(A/name)
(A/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'verdict':report['overall_scoped_verdict'],'scoped_signoff':report['scoped_signoff'],'findings':0,'summary_sha256':snapshot_sha,'source_inputs':len(sources),'native_views':22,'artifacts':['source-audit.json','source-audit.md','manifest.json','source-read-record.json','summary-snapshot.md']},indent=2))
