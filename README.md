# Countr — Retail ERP for US Stores

> A **BallotDA** product. Working name: **Countr** (provisional — see [ADR-0007](docs/decisions/0007-product-name.md)).

Countr is a retail ERP built for small and mid-size stores in the **United States**. The
first release targets **grocery / convenience stores** and ships the daily driver first:
**Inventory + Billing/POS + basic reports**. Everything else (purchasing, accounting,
multi-store, payroll) grows around that wedge over time.

This product is built **in-house from scratch**. NocoBase (in the sibling `../nocobase/`
folder) is kept **only as an architectural reference**, never forked or embedded — see
[ADR-0001](docs/decisions/0001-build-in-house.md) and
[ADR-0006](docs/decisions/0006-nocobase-as-reference.md).

## Tech stack

| Layer    | Choice                                    |
|----------|-------------------------------------------|
| Frontend | Next.js + React + TypeScript              |
| Backend  | FastAPI (Python)                          |
| Database | PostgreSQL                                |

Full rationale: [ADR-0005](docs/decisions/0005-tech-stack.md).

## Repository layout

```
countr/
├── docs/          # decision log, architecture, progress — read this first
├── backend/       # FastAPI service (clean layered architecture, SOLID)
└── frontend/      # Next.js app (feature-based structure)
```

## Where to start

1. **[docs/](docs/README.md)** — the decision log and how we work.
2. **[docs/architecture/](docs/architecture/README.md)** — folder structure, SOLID, patterns.
3. **[docs/progress/](docs/progress/README.md)** — what's done, what's next.

## Principles (non-negotiable)

- **SOLID** followed strictly across backend and frontend.
- **Clean, layered architecture** — dependencies point inward (domain never imports infrastructure).
- **Every meaningful decision is written down** as an ADR *before or when* it's made.
- **US-market realities are first-class**: sales tax, payments, QuickBooks, retail hardware.
