# ARA — AI Resume Analyzer

Production-ready monorepo scaffold for an AI Resume Analyzer SaaS.

## Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js 15 (App Router), TypeScript, Tailwind CSS v4, shadcn/ui |
| Backend | FastAPI, SQLAlchemy 2.0, Alembic, Pydantic v2 |
| Database | PostgreSQL 16 |
| Queue | Redis + ARQ worker |
| Storage | MinIO (S3-compatible) |
| Monorepo | pnpm workspaces |

## Repository layout

```
ara/
├── apps/
│   ├── api/          # FastAPI backend
│   └── web/          # Next.js frontend
├── packages/
│   └── shared-types/ # Shared TypeScript API types
├── infra/docker/     # Docker build files
├── docker-compose.yml
└── architecture.md
```

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (or Docker Engine + Compose)
- [Node.js 20+](https://nodejs.org/) and [pnpm 9+](https://pnpm.io/)
- [Python 3.12+](https://www.python.org/) (for local API development)

## Quick start

### 1. Environment

```sh
cp .env.example .env
```

Edit `.env` and set a strong `SECRET_KEY` for anything beyond local dev.

> **Security:** `.env` is gitignored and must never be committed. Only `.env.example` (placeholder values) belongs in the repo. If `.env` is ever committed by mistake, rotate all secrets and remove it from history with `git rm --cached .env`.

### 2. Infrastructure (Docker)

```sh
make up
make migrate
```

Services:

| Service | URL |
|---------|-----|
| Web | http://localhost:3000 |
| API | http://localhost:8000 |
| API docs | http://localhost:8000/docs |
| MinIO console | http://localhost:9001 |

### 3. Local development (without Docker for app code)

**API:**

```sh
cd apps/api
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

**Worker:**

```sh
cd apps/api
arq app.workers.WorkerSettings
```

**Web:**

```sh
pnpm install
pnpm dev:web
```

## API endpoints (stubs)

All business endpoints return `501 Not Implemented` until you wire services.

- `GET /api/v1/health` — liveness
- `GET /api/v1/ready` — readiness (checks DB)
- `POST /api/v1/auth/register` — user + org registration
- `POST /api/v1/auth/login` — JWT login
- `GET /api/v1/resumes/` — list resumes
- `POST /api/v1/resumes/upload-url` — presigned upload URL
- `POST /api/v1/analysis/jobs` — enqueue analysis
- `GET /api/v1/analysis/jobs/{id}` — job status + result

## Implementation order

1. Auth (register, login, JWT dependency)
2. Resume upload (presigned URL → MinIO → metadata in Postgres)
3. Analysis worker (text extraction → LLM → persist result)
4. Frontend pages (upload, job polling, results)

See [architecture.md](./architecture.md) for flows, data model, and deployment notes.

## Scripts

| Command | Description |
|---------|-------------|
| `pnpm dev` | Run web + API in parallel (local) |
| `pnpm dev:web` | Next.js dev server |
| `pnpm dev:api` | Uvicorn with reload |
| `make up` | Start Docker stack |
| `make migrate` | Run Alembic migrations |
| `make down` | Stop Docker stack |

## License

Private — add your license here.
