# Local development setup

## Prerequisites
- Python 3.12+
- Node.js 20+ and npm
- PostgreSQL 15+ running locally (or Docker)

## 1. Database (PostgreSQL)

Create a database and user matching `backend/.env.example`:

```sql
CREATE USER countr WITH PASSWORD 'countr';
CREATE DATABASE countr OWNER countr;
```

(Or run Postgres via Docker — a `docker-compose.yml` will be added when we containerize.)

## 2. Backend (FastAPI)

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env          # adjust DATABASE_URL if needed
uvicorn app.main:app --reload # http://localhost:8000  (docs at /docs)
```

Check it: open http://localhost:8000/api/v1/health — `status` is `ok` when the DB is
reachable, `degraded` otherwise (the API still responds).

Run tests / lint / types:
```bash
pytest            # unit tests (no DB needed)
ruff check .      # lint
mypy app          # type check
```

## 3. Frontend (Next.js)

```bash
cd frontend
npm install
cp .env.local.example .env.local
npm run dev                   # http://localhost:3000
```

## Notes
- Backend and frontend are separate deployables talking over a typed REST API
  (`/api/v1`). See `docs/architecture/README.md`.
- Never commit `.env` / `.env.local` — only the `*.example` files are tracked.
