# ADR-0010: Stock-movement ledger recorded at the persistence boundary

- **Status:** Accepted
- **Date:** 2026-07-26
- **Deciders:** Naveen (BallotDA)

## Context

Stock changed silently through three paths — sale (decrement), purchase (increment), and
manual adjustment — with no audit trail of *why* a quantity changed. A real inventory system
needs a history per product. The three write paths already mutate the product's on-hand
quantity inside a single DB transaction (sale/purchase repos lock the row and commit once).

## Decision

Introduce an append-only **`stock_movements`** ledger. Every change to a product's
`stock_quantity` writes one movement row `(product_id, delta, balance_after, reason,
reference_type, reference_id, note, created_at)` **in the same transaction** as the stock
mutation. Recording happens at the **persistence boundary** (infrastructure), via a small
shared helper called from the sale, purchase, and product repositories — not threaded as a
port through every use-case.

Reasons: `sale`, `purchase`, `adjustment`, `initial`.

## Why (rationale)

- Writing the movement where the stock row is mutated guarantees the ledger can never
  disagree with on-hand quantity (same transaction, atomic).
- Threading a `StockMovementRepository` port through every write use-case would add
  ceremony without changing behavior; the invariant "every stock delta is logged" is a
  persistence-level guarantee. The **read** side (history, inventory view) does use a
  proper repository port + use-cases.

## Alternatives considered

- **Record movements in each use-case (application layer)** — more explicit, but risks a
  use-case forgetting to log, and complicates atomicity (two commits). Rejected.
- **Derive history from sales/purchases only** — misses manual adjustments and initial
  stock, and can't show a single unified timeline. Rejected.

## Deferred / Not doing yet

- Making the ledger the *source of truth* for on-hand (i.e. deriving stock by summing
  movements) — for now the product row stays authoritative and the ledger mirrors it.
- Cost/valuation layers (FIFO/average cost) — later.

## Consequences

- New `stock_movements` table; sale/purchase/product repos each append movements.
- Inventory view can show per-product history and a unified timeline.
- Any *new* code path that changes stock must go through the same helper.
