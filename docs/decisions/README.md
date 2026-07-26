# Decision Log (ADRs)

An **ADR** (Architecture Decision Record) captures one decision: the context at the time,
what we chose, why, and what we deferred. They are **append-only** — we never edit a past
ADR's decision; if things change we add a new ADR that *supersedes* it.

## Why we do this

Six months from now nobody remembers *why* a choice was made. Without that "why", teams
re-open settled debates, or worse, undo a good decision because its reasoning was invisible.
This log is the antidote.

## File naming

`NNNN-short-slug.md` — four-digit sequence, kebab-case slug. e.g. `0008-payments-provider.md`.

## Template

Copy [`_template.md`](_template.md) for every new ADR.

## Status values

- **Proposed** — under discussion, not yet acted on.
- **Accepted** — decided; we are building on it.
- **Deferred** — consciously postponed (record *why* and *when to revisit*).
- **Superseded by ADR-NNNN** — replaced by a later decision (keep the old file).

## Index

| ADR | Title | Status | Date |
|-----|-------|--------|------|
| [0001](0001-build-in-house.md) | Build in-house instead of forking NocoBase | Accepted | 2026-07-26 |
| [0002](0002-product-scope.md) | Product scope: retail ERP for US stores | Accepted | 2026-07-26 |
| [0003](0003-wedge-module.md) | First module: Inventory + Billing/POS | Accepted | 2026-07-26 |
| [0004](0004-target-niche.md) | First niche: grocery / convenience stores | Accepted | 2026-07-26 |
| [0005](0005-tech-stack.md) | Tech stack: Next.js + FastAPI + PostgreSQL | Accepted | 2026-07-26 |
| [0006](0006-nocobase-as-reference.md) | Keep NocoBase as reference only | Accepted | 2026-07-26 |
| [0007](0007-product-name.md) | Working product name: "Countr" (provisional) | Accepted | 2026-07-26 |
| [0008](0008-brand-relationship.md) | Countr is a deliberate new retail vertical under BallotDA | Accepted | 2026-07-26 |
