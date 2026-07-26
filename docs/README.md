# Countr Documentation

This folder is the **memory of the project**. If a decision isn't written here, it didn't
happen. Read this before writing code.

## Structure

| Folder | What lives here |
|--------|-----------------|
| [decisions/](decisions/README.md) | **The decision log (ADRs).** Every meaningful choice — what we decided, *when*, *why then*, and what we deliberately deferred. |
| [architecture/](architecture/README.md) | System design, folder structure, SOLID & design-pattern rules. |
| [progress/](progress/README.md) | Living tracker — for each decided item: how much is done, how much remains. |
| [guides/](guides/) | How-to docs (local setup, running, deploy) — added as we build. |

## How we work (the discipline)

1. **Before a real decision is locked, add an ADR.** Even a small one. It records the
   context *at that moment* so future-us understands why past-us chose this.
2. **When something is deferred, that is also a decision** — record it in the ADR under
   "Deferred / Not doing yet" with the reason, so we never re-argue it from zero.
3. **When work starts or finishes, update [progress/](progress/README.md).** Docs and
   reality must never drift.
4. **Supersede, don't rewrite history.** If a decision changes, write a *new* ADR that
   supersedes the old one and link both ways. Old ADRs stay as-is.

## Quick index of key decisions

| ADR | Decision | Status |
|-----|----------|--------|
| [0001](decisions/0001-build-in-house.md) | Build in-house, not on a NocoBase fork | Accepted |
| [0002](decisions/0002-product-scope.md) | Product = retail ERP for US stores | Accepted |
| [0003](decisions/0003-wedge-module.md) | First module = Inventory + Billing/POS | Accepted |
| [0004](decisions/0004-target-niche.md) | First niche = grocery / convenience | Accepted |
| [0005](decisions/0005-tech-stack.md) | Next.js + FastAPI + PostgreSQL | Accepted |
| [0006](decisions/0006-nocobase-as-reference.md) | Keep NocoBase as reference only | Accepted |
| [0007](decisions/0007-product-name.md) | Working name "Countr" (provisional) | Accepted |
| [0008](decisions/0008-brand-relationship.md) | Countr = new retail vertical under BallotDA | Accepted |
