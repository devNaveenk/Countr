# ADR-0005: Tech stack — Next.js + FastAPI + PostgreSQL

- **Status:** Accepted
- **Date:** 2026-07-26
- **Deciders:** Naveen (BallotDA)

## Context

In-house build (ADR-0001) means we choose the stack. It must be productive, hireable in the
US, and able to handle a transactional retail app plus later integrations (payments, tax,
QuickBooks).

## Decision

| Layer     | Choice                                             |
|-----------|----------------------------------------------------|
| Frontend  | **Next.js + React + TypeScript** (App Router)      |
| Backend   | **FastAPI (Python)** with typed Pydantic models    |
| Database  | **PostgreSQL**                                     |

Supporting libraries (initial intent, refined in their own ADRs when adopted):
- Backend: SQLAlchemy 2.x (ORM), Alembic (migrations), Pydantic v2, Uvicorn, pytest.
- Frontend: TypeScript, TanStack Query (server state), a component/UI library, Zod.
- Jobs/async: to be decided when first needed (candidate: a task queue such as Celery/RQ or
  a lightweight scheduler) — its own ADR then.

## Why (rationale)

- **FastAPI** — fast to build, async, first-class typing via Pydantic, excellent auto-docs
  (OpenAPI), huge Python ecosystem for later data/tax/integration work.
- **Next.js + TS** — mature React framework, SSR/routing built in, mobile-friendly by
  default, very hireable.
- **PostgreSQL** — rock-solid, transactional, strong constraints — right for money/stock.
- Clean **frontend/backend separation** over a typed REST (OpenAPI) contract.

## Alternatives considered

- **Node.js backend (NestJS/Fastify)** — was the earlier recommendation (keeps one
  language and closer to NocoBase's Node code for reference). Overridden by preference for
  **Python/FastAPI**; the NocoBase reference value is conceptual, not code-level, so a
  different backend language is fine.
- **Django** — heavier, more opinionated; FastAPI preferred for a typed API-first service.

## Deferred / Not doing yet

- **ORM/migration, job queue, and UI-library** final picks are deferred to the moment we
  first need each, each with its own short ADR. We record the *intent* above but don't lock
  the details prematurely.

## Consequences

- Two deployables (frontend, backend) with a typed API contract between them.
- Python backend means the NocoBase reference is used for *architecture/patterns*, not
  copy-paste.
- Team needs both TS and Python skills.
