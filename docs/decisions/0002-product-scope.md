# ADR-0002: Product scope — retail ERP for US stores

- **Status:** Accepted
- **Date:** 2026-07-26
- **Deciders:** Naveen (BallotDA)

## Context

BallotDA is a **brand/umbrella** under which multiple products ship, each with its own
individual name. We needed to fix what *this* product is. Early conversation drifted
(election-related ideas were floated because of the brand name) before settling.

## Decision

This product is a **retail ERP for stores / shopkeepers, targeting the United States
market**. It is a complete store-operations system, delivered incrementally (see ADR-0003
for the first module).

## Why (rationale)

- Clear, well-understood domain with real, paying SMB buyers.
- US market is large; the SMB long-tail (small independent stores) is underserved by
  expensive incumbents.
- ERP is a normal (if large) web application — a good fit for the in-house decision
  (ADR-0001).

## Alternatives considered

- **Election-related product** — dropped; the brand name is not a product constraint, and
  retail ERP is the actual target.
- **Generic "no-code ERP builder"** — dropped; that's a platform, not a product (see
  ADR-0001).

## Deferred / Not doing yet

- **"Complete ERP" all at once** is explicitly deferred — it's a multi-year scope. We ship
  a wedge first (ADR-0003) and grow purchasing, accounting, multi-store, payroll around it.
- **Other BallotDA products** are out of scope for this repo.

## Consequences

- Every feature is judged by: *does a shopkeeper pay for this?*
- US-specific realities become first-class requirements: sales tax, payments, QuickBooks,
  retail hardware (tracked in architecture + future ADRs).
