# Ten-game QA commit checkpoint — 2026-11-07

The user stopped the coordinator goal and requested a local commit of all work so far. Seven games completed their documented QA scope; Spirit Island remains incomplete, and Cosmic Encounter and New Angeles await external rulings. All QA subagents are stopped. Nothing was pushed or deployed. This checkpoint does not complete or waive any remaining QA gate.

| Game | Questions | Scored pairs | Final/last closed reader scores | Source audit | Status | Evidence |
|---|---:|---:|---|---|---|---|
| So Clover! | 20 | 6 | A20/20; B20/20 | PASS within documented scope | Complete | [chat](codex://threads/01a1aaa1-7482-7400-9e88-21f4cb9de263); [report](../../../../../docs/quality/summary-qa/so-clover/2026-11-05-batch-002957/README.md) |
| John Company: Second Edition | 116 | 31 | A116/116; B116/116 | PASS within documented scope | Complete | [chat](codex://threads/01a1aaa2-7c89-7c92-bca8-a89efc3fe4d7); [report](../../../../../docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/final-completion-report.md) |
| Oath: Chronicles of Empire and Exile | 104 | 26 | A104/104; B104/104 | PASS within documented scope | Complete | [chat](codex://threads/01a1aad5-d462-7b90-9cb0-ed14a110aee7); [report](../../../../../docs/quality/summary-qa/oath-chronicles-of-empire-and-exile/2026-11-05-batch-002957/README.md) |
| Root | 81 | 24 | A81/81; B81/81 | PASS within documented scope | Complete | [chat](codex://threads/01a1aa9d-614e-7493-a3f2-715a8c52e03d); [report](../../../../../docs/quality/summary-qa/root/2026-11-05-batch-002957/current-snapshot-revalidation-2026-11-07/README.md) |
| Spirit Island | 173 | 12 | A171C/0P/2I; B171C/0P/2I (trial11) | C29 accuracy PASS | Incomplete; trial12 stopped ungraded | [chat](codex://threads/01a1ac01-c763-7bb1-901e-7458891630b8); [report](../../../../../docs/quality/summary-qa/spirit-island/2026-11-05-batch-002957/COMMIT-CHECKPOINT-NOTES.md) |
| Unmatched: Battle of Legends, Volume One | 67 | 14 | A67/67; B67/67 | PASS within documented scope | Complete | [chat](codex://threads/01a1ad02-d3f0-7083-bb2c-847ca80bb819); [report](../../../../../docs/quality/summary-qa/unmatched/2026-11-05-batch-002957/report.md) |
| Sidereal Confluence | 86 | 12 | A86/86; B86/86 | PASS within documented scope | Complete | [chat](codex://threads/01a1b0b3-0030-70b2-8947-7a940fdf364f); [report](../../../../../docs/quality/summary-qa/sidereal-confluence/2026-11-05-batch-002957/report.md) |
| Lords of Vegas | 39 | 11 | A39/39; B39/39 | PASS within documented scope | Complete | [chat](codex://threads/01a1b2c1-d5d1-7333-8948-72708b3d1f3e); [report](../../../../../docs/quality/summary-qa/lords-of-vegas/2026-11-05-batch-002957/README.md) |
| Cosmic Encounter | 168 | 9 | A168/168; B168/168 (supported bank) | Accuracy PASS; authority gap | Incomplete; external ruling needed | [chat](codex://threads/01a1b3c7-0daa-70f1-9158-0e75d24cbb22); [report](../../../../../docs/quality/summary-qa/cosmic-encounter/2026-11-05-batch-002957/COMMIT-CHECKPOINT-NOTES.md) |
| New Angeles | 94 | 8 | A94/94; B94/94 (supported bank) | Accuracy PASS; authority gap | Incomplete; external ruling needed | [chat](codex://threads/01a1b3fc-466c-7322-8413-9e59ff041286); [report](../../../../../docs/quality/summary-qa/new-angeles/2026-11-05-batch-002957/COMMIT-CHECKPOINT-NOTES.md) |

Spirit Island trial12 has preserved partial originals A136/173 and B173/173, with neither final review nor grading completed; it is not another scored pair. Reader A also reported a workspace-credit failure, recorded in its game notes. Unmatched also retains one aborted unscored dispatch; Lords of Vegas retains one canceled unscored attempt. Sidereal Confluence retains two separately graded, unselected complete outputs in addition to its 12 scored pairs.

John Company: Applies the user-approved >= defense-strength interpretation; publisher email not independently verified.

Lords of Vegas completion is PASS_FOR_DECLARED_EXPANDED_V10_SOURCE_LIMITS_BENCHMARK; the source does not identify who physically throws the free boss-tie roll.

Coverage describes working saturation within each documented source and edition scope on a known fixed, tool-assisted bank. It is not exhaustive scenario coverage or a general model-accuracy claim.

The three incomplete games have game-specific COMMIT-CHECKPOINT-NOTES.md files and registry review_notes. Spirit Island and New Angeles have validated registry status (structural checks only) and unverified summaries/catalog entries. Cosmic Encounter retains its historical registry status and minor_issues summary stamp dated 2026-07-03; neither represents completion of this QA run. No semantic-audit record, source verdict or verification stamp was promoted for an incomplete game.

The checkpoint synchronizes only these three catalog entries and registry blocks; unrelated catalog entries and index lines are preserved. All ten selected summaries passed structural validation. Final catalog and staged-diff checks are recorded under commit-checkpoint/.

The staged whitespace check reports trailing whitespace or blank EOF lines in 159 preserved QA source/historical evidence files. These hash-bound originals remain unchanged; the current checkpoint notes, canonical summaries and catalog edits pass the whitespace check. Structural validation and catalog consistency passed.
