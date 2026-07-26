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
| POS / checkout (cart, tax, tender, atomic stock decrement) | ✅ | `/app/pos`; sale + items recorded; row-locked stock; receipt |
| Receipts | ✅ (basic) | on-screen receipt after each sale |
| Sales history (recent sales, single receipt) | ✅ (API) | `/api/v1/sales`; UI history page later |
| Flat sales tax (per-item exempt) | ✅ | `COUNTR_DEFAULT_TAX_RATE`; real tax API later |
| Reports (revenue/sales/tax/items, best-sellers, low-stock) | ✅ | `/app/reports`; rolling 1/7/30-day windows |
| Collapsible sidebar navigation (desktop collapse + mobile drawer) | ✅ | `AppShell`; `/app` layout guards once |
| Stock-movement ledger (full audit trail) | ⬜ | later — replaces the simple on-hand counter |
| Buy / purchasing (receive stock, suppliers) | ⬜ | shown as "soon" in sidebar |
| Dedicated Inventory view | ⬜ | shown as "soon" in sidebar |
| Payments integration | ⬜ | ADR when started (Stripe/Square) |
| Real sales-tax API | ⬜ | ADR when started (TaxJar/Avalara) |

Backend tests: 20 passing (health, auth ×5, products ×7, checkout ×6). All layered/SOLID;
use-cases tested with fakes (no DB). Reports = SQL aggregates.

First-layer feature set (POS · Products · Reports) is now in place, unified under the
sidebar shell. Next: deepen (Buy/purchasing, Inventory view, sales history UI) or wire
payments/tax integrations.

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
