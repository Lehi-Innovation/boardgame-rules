# PRD-04 — Transactions & Trust

> **Grounding note:** **Nothing transactional exists in this repository.** No payments, orders, offers, shipping, user identity, ratings, or fraud logic — confirmed by exhaustive search (the only "trade"/"auction"/"bid" hits are board game mechanics in rules content and test fixtures). This PRD records the decisions a transactions track must make, plus the few genuinely transferable patterns the codebase offers. Every product mechanism below is [INFERRED] or [OPEN QUESTION].

## Transaction flow

Proposed skeleton, with zero code basis [INFERRED]:

```
offer → acceptance → payment → fulfillment (ship) → delivery confirmation → settlement/review
```

[OPEN QUESTION: is there an offer/negotiation step at all, or fixed-price buy-now only? Depends on the PRD-02 pricing decision.]

The one transferable engineering pattern [code-backed, analogous]: the pipeline's claim-based state machine (`scripts/registry.py:claim_games_by_status()`):
- Transitions are atomic under a lock; transient states carry `claimed_at` timestamps; abandoned work is reclaimed after a timeout (1 hour); failures restore to a retryable state rather than dangling.
- Transactions need exactly this shape: `payment_pending`, `awaiting_shipment` etc. as owned, time-bounded states with explicit timeout behavior (auto-cancel, auto-refund, escalate). The discipline exists in the codebase; the domain does not.

## Payment handling

[OPEN QUESTION: no payment integration exists or is hinted at. `.env.example` contains only `BGG_API_TOKEN` and `ANTHROPIC_API_KEY`. Decisions needed: PSP (Stripe Connect is the conventional choice for peer-to-peer marketplaces), escrow vs direct charge, fee model, refunds, tax/compliance footprint. None of these have any basis in the repo — this is a from-scratch track.]

## Shipping

[OPEN QUESTION: nothing exists. Decisions needed: label integration vs seller-arranged shipping, who pays, tracking-number capture as the trigger for the `shipped` state, international scope. Board-game-specific concern worth recording: weight/dimension data is not in the catalog — BGG version objects carry weight/size, which is another argument for fetching BGG versions when the Edition entity is added (PRD-01).]

## Trust signals

[OPEN QUESTION: no users → no ratings, reviews, or seller history. All to be designed.]

Transferable trust *patterns* that do exist [code-backed, analogous — these shaped the project's culture and could shape the marketplace's]:

1. **Tiered verification with human escalation** — `scripts/quality_check.py` auto-validates or flags with machine-readable `review_notes`; CLAUDE.md designates `flagged` a terminal state "requiring human attention." Analog: automated listing/transaction checks that escalate to human moderation with recorded reasons.
2. **Confidence labeling** — the `rules-lookup` skill requires every answer to state its source tier and confidence ("high / medium / low"), and marks intuition-sourced content "unverified" in PRs. Analog: provenance-labeled trust badges (verified photos vs seller-claimed condition).
3. **Calibration before automation** — the pipeline design reviewed the first 20–30 outputs manually before enabling auto-accept. Analog: manual review of early disputes/listings before automating moderation thresholds.
4. **Uncertainty phrase scanning** — `UNCERTAINTY_PHRASES` in `quality_check.py` flags hedging text. Analog: scan listing descriptions for risk phrases ("not sure if complete", "untested").

## Dispute handling

[OPEN QUESTION: nothing exists. The Components sections of rules files (exact piece counts) are the repo's one concrete contribution: they provide an objective reference for "item not as described — missing components" disputes, e.g. checking a Concordia copy against its documented "72 cards total" manifest. [INFERRED]]

## Fraud and safety logic

None present. No rate limiting, identity verification, anomaly detection, or banning machinery — and no user accounts to attach them to. [OPEN QUESTION: minimum-viable trust stack for launch — email verification? PSP-delegated KYC? Listing-volume limits for new sellers?] [NEEDS REVIEW: this entire PRD needs a product owner decision pass before any engineering planning]
