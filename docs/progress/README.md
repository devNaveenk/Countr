# Progress Tracker

Living status of decided work. Update this **whenever work starts or finishes** — docs and
reality must not drift. For each item: what's done, what remains.

_Last updated: 2026-07-26_

## Legend
✅ done · 🟡 in progress · ⬜ not started · ⏸️ deferred (see ADR)

## Phase 0 — Foundation & docs

| Item | Status | Notes |
|------|--------|-------|
| Project decisions captured as ADRs (0001–0007) | ✅ | `docs/decisions/` |
| Docs structure (decisions / architecture / progress / guides) | ✅ | `docs/` |
| Architecture + SOLID + folder-structure spec | ✅ | `docs/architecture/` |
| Product folder created, separate from NocoBase | ✅ | `countr/` |
| Backend/frontend directory skeleton | ✅ | dirs in place; apps not yet initialized |
| Backend app initialized (FastAPI, deps, config, DB session) | ⬜ | next step |
| Frontend app initialized (Next.js + TS) | ⬜ | next step |
| Local dev setup guide | ⬜ | `docs/guides/` |
| Git repo for Countr (separate from nocobase) | ⬜ | init + first commit |

## Phase 1 — Wedge module: Inventory + Billing/POS (ADR-0003)

_High-level; broken into tasks when Phase 0 is done._

| Area | Status |
|------|--------|
| Product catalog (items, categories, barcodes, units, price) | ⬜ |
| Stock levels & adjustments | ⬜ |
| POS / checkout screen (fast barcode entry, cart, tender) | ⬜ |
| Receipts | ⬜ |
| Basic reports (sales, stock) | ⬜ |
| Auth + roles (owner, cashier) | ⬜ |
| Sales tax integration | ⬜ (ADR when started) |
| Payments integration | ⬜ (ADR when started) |

## Deferred (conscious — do not re-plan yet)

| Item | Deferred by |
|------|-------------|
| Purchasing / suppliers / POs | ADR-0003 |
| Accounting + QuickBooks sync | ADR-0003 |
| Multi-store | ADR-0003 |
| Employees / payroll | ADR-0003 |
| CRM / loyalty | ADR-0003 |
| Other store niches (liquor, auto-parts) | ADR-0004 |
| Final product name + trademark/domain | ADR-0007 |
| Removing the NocoBase reference folder | ADR-0006 |
