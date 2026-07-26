# Progress Tracker

Living status of decided work. Update this **whenever work starts or finishes** — docs and
reality must not drift. For each item: what's done, what remains.

_Last updated: 2026-07-26 (Products/catalog module shipped)_

## Legend
✅ done · 🟡 in progress · ⬜ not started · ⏸️ deferred (see ADR)

## Phase 0 — Foundation & docs

| Item | Status | Notes |
|------|--------|-------|
| Project decisions captured as ADRs (0001–0008) | ✅ | `docs/decisions/` |
| Docs structure (decisions / architecture / progress / guides) | ✅ | `docs/` |
| Architecture + SOLID + folder-structure spec | ✅ | `docs/architecture/` |
| Product folder created, separate from NocoBase | ✅ | `countr/` |
| Backend/frontend directory skeleton | ✅ | in place |
| Backend app initialized (FastAPI, deps, config, DB session) | ✅ | venv + deps installed; `app.main:app` runs |
| Working vertical slice (health: route→use-case→repo→DB port) | ✅ | `/api/v1/health` returns 200; unit tests pass |
| Frontend app initialized (Next.js + TS + Tailwind) | ✅ | App Router, src dir, feature-based structure, typed API client |
| Local dev setup guide | ✅ | `docs/guides/local-setup.md` |
| Git repo for Countr (separate from nocobase) | ✅ | init + first commit `59d8814` (branch `main`) |
| Remote for Countr repo (GitHub) | ⬜ | not created yet — decide account/org + repo name |
| PostgreSQL running locally + first migration (Alembic) | ⬜ | health shows `degraded` until DB is up |

## Phase 1 — Wedge module: Inventory + Billing/POS (ADR-0003)

| Area | Status | Notes |
|------|--------|-------|
| Auth + roles (owner, cashier) | ✅ | register/login/JWT, `/me`, protected routes; roles modeled |
| Product catalog (items, barcode, category, unit, cost/sell price, tax) | ✅ | full CRUD backend + `/app/products` UI; search, low-stock filter, archive |
| Stock levels & adjustments | ✅ | on-hand qty + guarded adjust (no negative); low-stock flag |
| Stock-movement ledger (audit trail of every change) | ⬜ | next — replaces the simple on-hand counter |
| POS / checkout screen (barcode entry, cart, tender) | ⬜ | next major module |
| Receipts | ⬜ | |
| Basic reports (sales, stock) | ⬜ | |
| Sales tax integration | ⬜ | ADR when started (TaxJar/Avalara) |
| Payments integration | ⬜ | ADR when started (Stripe/Square) |

Backend tests: 14 passing (health, auth ×5, products ×7). All layered/SOLID; use-cases
tested with fakes (no DB).

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
