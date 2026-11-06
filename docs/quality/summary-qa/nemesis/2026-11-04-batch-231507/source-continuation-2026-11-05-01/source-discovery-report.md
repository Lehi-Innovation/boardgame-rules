# Nemesis source investigation — 5 November 2026

The resumed investigation found a narrow primary-source clarification for **successful Egg Melee**, plus stronger localized wording for **first-death Pod unlocking**. It did not verify a publisher/designer forum ruling that resolves the remaining cases. Full-core completion is not established.

This report concerns original Nemesis, basic board, standard semi-cooperative play and the six original characters. No Lockdown, Retaliation, expansion or campaign answer is substituted for an original-game rule. No one was contacted and nothing was posted.

## Discovery method and limits

I reviewed the prior source-gap and provenance notes before searching. Those already recorded the original manual and the current official FAQ, whose actual cover is v2.2 despite the v2.1 filename. They did not retain a query-level BGG search history. This continuation therefore does not claim to know or exclude every earlier search query.

The [query ledger](query-ledger.json) retains **81 distinct query strings** across the connected search service and TinyFish. Raw requests/results, failed fetches and terminal browser results are saved alongside it. The [candidate ledger](source-candidate-ledger.json) classifies 17 leads/sources, including secondary discussions, publisher-hosted manuals and excluded derivative material. Counts describe retained searches, not exhaustive web coverage or independent authorities.

Direct BGG reads and TinyFish fetches were blocked. Two separate browser runs terminated at Cloudflare verification without retrieving the requested forum contents, including the coordinator-suggested explicit lite configuration. The local Computer Use initialization failed before any UI input because its runtime rejected the workspace URI. An approved public-network read reached BGG, but the tested XML/API/HTML endpoints returned 401, 404 or 403. See [access limitations](access-limitations.json). Access failures do not prove that no ruling exists.

Search snippets, community claims, aggregation labels and developer badges were not silently promoted to original-game publisher authority. In particular, the repository's own published summary surfaced in results and was excluded as potentially circular evidence.

## SG01 — all eight Adults already in Combat

The exact [all-eight-in-Combat Reddit question](https://www.reddit.com/r/NemesisCrew/comments/1ri8dhy/encounter_adult_token_what_8_adults_on_board_and/) was retrieved. Community replies propose incompatible destinations or substitutes and contain explicit uncertainty; no applicable publisher/designer identity was established.

A [BGG miniature-exhaustion discussion](https://boardgamegeek.com/thread/2234628/clarification-needed-breeder-and-out-of-miniatures) concerns Breeders in campaign mission 3, with community house-rule proposals. It is neither the exact original-core Adult case nor verified official authority.

The newly retained original Polish, French and German manuals all repeat the non-Combat-only removal procedure, followed by an instruction to place an Adult. They supply no all-in-Combat fallback. **SG01 remains unresolved.**

## SG02 — Queen Egg after Nest destruction

The strongest lead is numbered clarification 26 in [Unofficial Rules Clarifications Not In The FAQ](https://boardgamegeek.com/thread/2615378/unofficial-rules-clarifications-not-in-the-faq). Other discussions and [Mira's D11 aggregation](https://miralibrary.com/games/nemesis) attribute permanent Nest destruction despite new Eggs to Awaken Realms. A [Czech discussion](https://www.zatrolene-hry.cz/spolecenska-hra/nemesis-7574/otazky/zniceni-hnizda-29640/) reports screenshots of publisher communication and points to that compilation and the specific [destroyed-Nest evolution thread](https://boardgamegeek.com/thread/2727750/destroyed-nest-intruder-evolution).

Neither the cited screenshot/original statement nor its sender, original date and exact applicability could be verified. The compilation date attributed by an aggregator is not the original publisher reply date. The specific thread's indexed snippet supports adding Eggs without undoing destruction, but its reply author was not verified. A separate [2019 discussion](https://boardgamegeek.com/thread/2322484/another-play-session-another-set-of-rule-clarifica) contains conflicting community answers. A [carried-Egg discussion](https://boardgamegeek.com/thread/2135532/nest-eggs-and-intruder-board/page/2) attributes a statement to Adam about returning a previously carried Egg; that is not automatically the Queen-generation case.

All four language manuals support the Queen's Egg-addition instruction without a destroyed-Nest exception. They do not explicitly settle destroyed-marker persistence/reset or the Objective result. **SG02 remains unresolved for those consequences**, with a specific unverified primary-source lead preserved.

## SG03 — successful Egg Melee clarified; missed execution still limited

The original English normal Melee procedure draws one Contamination card. The publisher-hosted original [Polish manual, p.25](https://awakenrealms.com/images/download/Nemesis/PL/NEMESIS_RULEBOOK_280x280mm_PL.pdf#page=25) and [French manual, p.25](https://awakenrealms.com/images/download/Nemesis/FR/NEMESIS_RULEBOOK_280x280mm_FR.pdf#page=25) explicitly place the no-Contamination/no-Wound exception under a miss. A fresh [source-only independent review](language-source-review.json) concluded that a **successful Egg Melee retains the ordinary one-card Contamination draw**. These compatible explicit conditions corroborate the English normal procedure; no language hierarchy is asserted.

The ordinary pre-roll draw and the miss-conditioned no-draw instruction still lack an explicit ordered reconciliation. No refund, delayed draw or blanket Egg immunity was invented. The old successful-hit uncertainty is resolved narrowly; the missed-execution timing limitation is retained separately in [source gaps v2](source-gaps-v2.json).

The [Larva/Egg melee discussion](https://boardgamegeek.com/thread/2344081/larva-or-egg-melee-attack) contains competing community readings. No official affiliation was established for its respondents. A [Paweł Samborski statement about attacking Eggs during Combat](https://boardgamegeek.com/thread/2261832/clarification-eggs-in-combat) is an adjacent-case lead; combat legality does not settle Contamination on a hit.

The primary-source correction is explicitly versioned in [source version 02](source-version-02.json) and [v8 key corrections](benchmark-v8-corrections.json). Q18's wording is unchanged. Its actual asked outcome facts are graded without an automatic deduction for unasked refund-versus-delay details; see the [coordinator clarification](requested-parts-clarification-v8.json). The residual playability gap independently prevents full-core completion.

## SG04 — later death after Pods were relocked

The [French](https://awakenrealms.com/images/download/Nemesis/FR/NEMESIS_RULEBOOK_280x280mm_FR.pdf#page=26) and [German](https://awakenrealms.com/images/download/Nemesis/DE/NEMESIS_RULEBOOK_280x280mm_DE.pdf#page=26) original manuals consistently specify first death in the Pod section as well as the detailed critical-moment rule. They support first-death-only within those editions.

English and Polish retain the broader Pod-overview wording alongside their first-death rules. No retrieved authority declares the clearer localizations an English erratum or establishes controlling language precedence. The independent review therefore retains **SG04 as unresolved for an unqualified English-source ruling**. No exact-case primary forum ruling was verified in the bounded search.

## Preserved primary evidence and QA continuation

All three publisher-hosted language PDFs were downloaded completely, fingerprinted and checked as original 28-page manuals with the six core characters. [Verified provenance](official-language-manuals-verified.json) records URLs, sizes, hashes and extractions. Their production metadata is from 2019; metadata dates do not establish rules-version precedence. An initial extraction attempt failed because `pdftotext` was unavailable after download; that record is preserved, and extraction was completed using the existing PyMuPDF installation.

The new source audit also found compatible explicit Slime-before-Exploration timing and an omitted Larva-removal instruction on the illustrated Antidote card in the existing English manual. Those are source-supported summary repairs, not new forum authority. The independent whole-bank review decides whether each printed fact needs a new question or only correction/clarification within an existing request.

The sealed old banks, source-gap record, reader raws, grades and snapshots remain unchanged. [Current continuation status](game-status.json) and the eventual final QA report distinguish the old v7 coordinator overlay, the new v8 results, and later diagnostic/final-bank results. No stamping, shared registry work, commit or publication was performed. Missing primary authority and incomplete reader/source gates remain visible; neither search volume nor a narrower supported correction is a complete PASS.
