# Architecture

Countr is a **typed REST** system: a Next.js frontend talking to a FastAPI backend over an
OpenAPI contract, backed by PostgreSQL. The guiding rule is **clean, layered architecture
with dependencies pointing inward** — the domain knows nothing about the web or the
database.

```
┌─────────────────────────────┐        ┌──────────────────────────────┐
│  Next.js frontend (React/TS)│  HTTP  │  FastAPI backend (Python)    │
│  feature-based UI, API client│──────▶│  layered, SOLID              │──▶ PostgreSQL
└─────────────────────────────┘  JSON  └──────────────────────────────┘
```

## SOLID — how each letter shows up here

- **S — Single Responsibility.** Each layer has one job: routers handle HTTP, use-cases
  orchestrate, domain holds business rules, repositories persist. A file that does two of
  these is a smell.
- **O — Open/Closed.** New behavior is added by new implementations (e.g. a new payment
  provider adapter), not by editing existing tested code.
- **L — Liskov Substitution.** Any concrete repository/adapter must be fully usable through
  its interface — no surprises when swapped (e.g. a fake repo in tests).
- **I — Interface Segregation.** Small, focused interfaces (`ProductRepository`,
  `SalesRepository`) instead of one giant "DAO".
- **D — Dependency Inversion.** High-level code depends on **abstractions** defined in
  `domain/`; concrete DB/external implementations in `infrastructure/` are injected in.
  The domain never imports infrastructure.

## Backend folder structure (FastAPI)

```
backend/app/
├── main.py                      # app factory, wiring
├── api/                         # PRESENTATION — thin HTTP layer
│   └── v1/
│       ├── routes/              # routers per resource (products, sales, ...)
│       └── deps.py              # dependency-injection providers
├── schemas/                     # Pydantic DTOs (request/response models)
├── application/                 # APPLICATION — orchestration
│   ├── use_cases/               # one class/function per user action
│   └── services/                # cross-use-case app services
├── domain/                      # DOMAIN — pure business core (no framework imports)
│   ├── entities/                # business objects + rules
│   └── repositories/            # ABSTRACT repository interfaces (DIP)
├── infrastructure/              # INFRASTRUCTURE — details, swappable
│   ├── db/
│   │   ├── models/              # SQLAlchemy ORM models
│   │   └── session.py           # engine/session
│   ├── repositories/            # concrete repos implementing domain interfaces
│   └── external/                # adapters: payments, sales tax, QuickBooks, storage
└── core/                        # config, settings, security, logging
```

**Dependency rule:** `api → application → domain` and `infrastructure → domain`.
`domain` imports nothing outward. `infrastructure` is only wired in at the edges (`deps.py`,
`main.py`).

## Frontend folder structure (Next.js, App Router)

```
frontend/src/
├── app/                         # routes (App Router)
├── features/                    # feature modules (inventory, pos, reports, ...)
│   └── <feature>/               # components + hooks + api calls for that feature
├── components/
│   ├── ui/                      # generic design-system primitives
│   └── layout/                  # shells, nav, headers
├── lib/
│   └── api/                     # typed API client (from backend OpenAPI)
├── hooks/                       # shared hooks
├── types/                       # shared TS types
└── styles/                      # global styles / theme (branding lives here)
```

**Feature-based, not layer-based** on the frontend: everything for "POS" lives under
`features/pos/`, so features stay cohesive and independently changeable (SRP + OCP at the UI
level).

## Design patterns we lean on

- **Repository** — abstract persistence behind interfaces (`domain/repositories`).
- **Dependency Injection** — FastAPI `Depends` wires concrete implementations to abstract
  ports.
- **Use-Case / Interactor** — each user action is an explicit, testable unit.
- **Adapter** — external services (Stripe/Square, TaxJar/Avalara, QuickBooks, GCS) sit
  behind our own interfaces so vendors can be swapped.
- **DTO** — Pydantic schemas at the boundary; domain entities never leak to the wire.

## US-market concerns as explicit adapters

These are modelled as **ports in `domain/` with adapters in `infrastructure/external/`**, so
they're swappable and testable:

| Concern      | Port (interface)      | Adapter (later)          |
|--------------|-----------------------|--------------------------|
| Sales tax    | `TaxCalculator`       | TaxJar / Avalara         |
| Payments     | `PaymentGateway`      | Stripe / Square          |
| Accounting   | `AccountingSync`      | QuickBooks Online        |
| File storage | `FileStorage`         | Google Cloud Storage     |
| Notifications| `Notifier`            | SMTP/Resend, later Twilio|

Each gets its own ADR when implemented.
