# ARA — AI Resume Analyzer

ARA is a multi-tenant SaaS that accepts resume uploads, runs AI-powered analysis, and returns structured feedback including skill detection, gap analysis, ATS scoring, and improvement suggestions.

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Next.js 15     │────▶│   FastAPI API   │────▶│   PostgreSQL    │
│   (apps/web)     │     │   (apps/api)    │     │   (port 5432)   │
│   port 3000      │◀────│   port 8000     │────▶│   Redis (6379)  │
└─────────────────┘     │                 │     └─────────────────┘
                         │                 │────▶│   MinIO/S3      │
                         └─────────────────┘     │   (port 9000)   │
                                │                └─────────────────┘
                          ┌─────┴──────┐
                          │ ARQ Worker │────▶ Ollama LLM (port 11434)
                          └────────────┘
```

## Prerequisites

- Python 3.12+
- Node.js 20+
- Docker & Docker Compose
- Ollama (optional, for local LLM analysis)

## Quick Start

### Option A: Docker (Recommended)

Run the entire stack with one command:

```bash
# Copy environment file and customize
cp .env.example .env

# Build and start all services
docker compose up -d --build

# Wait for services to be ready, then open:
open http://localhost:3000
```

This starts PostgreSQL, Redis, MinIO, the API server (with auto-migrations), the background worker, and the Next.js frontend.

### Option B: Local Development

#### 1. Start infrastructure

```bash
docker compose up -d db redis minio
```

#### 2. Install backend dependencies

```bash
pip install -e "apps/api[dev]"
```

#### 3. Run database migrations

```bash
cd apps/api && alembic upgrade head
```

#### 4. Start the API server

```bash
cd apps/api && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### 5. Install frontend dependencies

```bash
pnpm install
```

#### 6. Start the frontend

```bash
cd apps/web && pnpm dev
```

Open http://localhost:3000 to access the application.

## Production Deployment

### Docker Compose (single-server deployment)

```bash
# 1. Configure production environment
cp .env.production .env
# Edit .env with real values:
#   - SECRET_KEY: generate with `openssl rand -hex 32`
#   - DATABASE_URL: set to managed PostgreSQL
#   - CORS_ORIGINS: set to your frontend domain
#   - NEXT_PUBLIC_API_URL: set to your API domain

# 2. Build and start all services
docker compose up -d --build

# 3. Verify health
curl http://localhost:8000/api/v1/health
curl http://localhost:3000
```

### Production Checklist

- [ ] Set `ENVIRONMENT=production` in `.env`
- [ ] Generate a strong `SECRET_KEY` (e.g., `openssl rand -hex 32`)
- [ ] Use managed PostgreSQL (AWS RDS, Neon, Supabase, etc.)
- [ ] Use managed Redis (Upstash, ElastiCache, etc.)
- [ ] Use S3-compatible storage (AWS S3, Cloudflare R2, MinIO)
- [ ] Set `CORS_ORIGINS` to your actual frontend domain
- [ ] Disable Swagger docs by setting `ENVIRONMENT=production`
- [ ] Configure reverse proxy (nginx, Traefik) with TLS
- [ ] Enable structured logging and monitoring
- [ ] Run database migrations as part of deployment: `alembic upgrade head`

### Architecture Considerations

| Component | Production Recommendation |
|-----------|--------------------------|
| API | Horizontal replicas behind load balancer (stateless) |
| Worker | Scale ARQ workers independently based on queue depth |
| Database | Read replicas for reporting; PgBouncer for connection pooling |
| Storage | S3 scales independently; enable SSE encryption |
| Frontend | Serve via CDN; configure `NEXT_PUBLIC_API_URL` |

### PII and Compliance

Resumes contain personal data. Ensure:

- Encryption at rest (S3 SSE, encrypted PostgreSQL volumes)
- Retention policies and user-initiated deletion (endpoint: `DELETE /api/v1/resumes/{id}`)
- Audit logging for access to resume objects
- GDPR/CCPA compliance workflows as needed
## Prerequisites

- Python 3.12+
- Node.js 20+
- Docker & Docker Compose
- Ollama (optional, for local LLM analysis)

## Quick Start

### Option A: Docker (Recommended)

Run the entire stack with one command:

```bash
# Copy environment file and customize
cp .env.example .env

# Build and start all services
docker compose up -d --build

# Wait for services to be ready, then open:
open http://localhost:3000
```

This starts PostgreSQL, Redis, MinIO, the API server (with auto-migrations), the background worker, and the Next.js frontend.

### Option B: Local Development

#### 1. Start infrastructure

```bash
docker compose up -d db redis minio
```

#### 2. Install backend dependencies

```bash
pip install -e "apps/api[dev]"
```

#### 3. Run database migrations

```bash
cd apps/api && alembic upgrade head
```

#### 4. Start the API server

```bash
cd apps/api && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### 5. Install frontend dependencies

```bash
pnpm install
```

#### 6. Start the frontend

```bash
cd apps/web && pnpm dev
```

Open http://localhost:3000 to access the application.

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register a new user + organization |
| POST | `/api/v1/auth/login` | Login, returns JWT token |
| GET | `/api/v1/auth/me` | Get current user info (requires auth) |

### Health

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/health` | Simple health check |
| GET | `/api/v1/ready` | Readiness check (includes DB check) |

### Resumes

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/resumes/upload` | Upload a PDF resume |
| GET | `/api/v1/resumes` | List resumes for current org |
| GET | `/api/v1/resumes/{id}` | Get resume details |
| DELETE | `/api/v1/resumes/{id}` | Delete resume and associated analysis |

### Analysis

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/analysis/jobs` | Create analysis job for a resume |
| GET | `/api/v1/analysis/jobs` | List analysis jobs for current org |
| GET | `/api/v1/analysis/jobs/{id}` | Get analysis job detail with results |

### Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Configuration

Configuration is managed via environment variables in `.env`:

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `postgresql+psycopg://postgres:...@localhost:5432/ara_db` | PostgreSQL connection string |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis connection string |
| `SECRET_KEY` | `change-me` | JWT signing key |
| `CORS_ORIGINS` | `http://localhost:3000` | Allowed CORS origins |
| `S3_ENDPOINT` | `http://localhost:9000` | S3/MinIO endpoint |
| `S3_ACCESS_KEY` | `ara_minio` | S3 access key |
| `S3_SECRET_KEY` | `ara_minio_secret` | S3 secret key |
| `S3_BUCKET` | `resumes` | S3 bucket for resume storage |
| `LLM_PROVIDER` | `ollama` | LLM provider (`ollama`) |
| `LLM_API_BASE` | `http://localhost:11434` | LLM API endpoint |
| `LLM_MODEL` | `qwen2.5-coder:7b` | LLM model name |

## Project Structure

```
├── apps/
│   ├── api/                    # FastAPI backend
│   │   ├── app/
│   │   │   ├── api/v1/endpoints/   # Route handlers
│   │   │   ├── core/               # Config, security, logging
│   │   │   ├── db/                 # Database session
│   │   │   ├── models/             # SQLAlchemy ORM models
│   │   │   ├── repositories/       # Database query layer
│   │   │   ├── schemas/            # Pydantic request/response DTOs
│   │   │   ├── services/           # Business logic
│   │   │   ├── storage/            # S3/MinIO client
│   │   │   └── workers/            # ARQ background jobs
│   │   ├── alembic/                # Database migrations
│   │   └── tests/
│   └── web/                    # Next.js 15 frontend
│       ├── app/
│       │   ├── dashboard/          # Dashboard pages
│       │   ├── login/              # Login page
│       │   └── page.tsx            # Landing page
│       ├── components/             # React components
│       └── lib/                    # API client, auth, utilities
├── packages/
│   └── shared-types/           # TypeScript DTOs
├── infra/docker/               # Docker configs
├── docker-compose.yml          # Local infrastructure
└── .env                         # Environment variables
```

## Backend Architecture

The backend follows a layered architecture:

```
api/v1/endpoints/  →  HTTP, validation, status codes
       ↓
   services/       →  Business rules, orchestration
       ↓
 repositories/    →  Database queries
       ↓
   models/         →  SQLAlchemy ORM
```

### Data Model

All tenant-owned records include `organization_id` for multi-tenancy.

| Table | Purpose |
|-------|---------|
| `organizations` | Tenant boundary |
| `users` | Authenticated users, belong to one org |
| `resumes` | File metadata, extracted text, storage key |
| `analysis_jobs` | Async job lifecycle (pending → processing → completed/failed) |
| `analysis_results` | Structured JSON output from LLM |

## Frontend

- **Next.js 15** with App Router
- **Tailwind CSS v4** with CSS-first configuration
- **Axios** for API communication
- **shadcn/ui** component system

### Authentication Flow

1. User registers via `/register` (creates organization + user)
2. User logs in via `/login`, receives JWT token
3. Token is stored in `localStorage` and sent as `Authorization: Bearer <token>` header
4. Protected routes redirect to `/login` if no token exists

### Available Pages

- `/` - Landing page
- `/login` - Authentication
- `/dashboard` - Overview with resume/analysis counts
- `/dashboard/resumes` - Resume management (list, delete, analyze)
- `/dashboard/upload` - Upload new resumes
- `/dashboard/analysis` - Analysis history with scores

## Development

### Running tests

```bash
# Backend
cd apps/api && pytest

# Frontend
pnpm lint
```

### Database migrations

```bash
cd apps/api
alembic revision --autogenerate -m "description"
alembic upgrade head
```

### Adding new API endpoints

1. Add Pydantic schemas in `apps/api/app/schemas/__init__.py`
2. Add SQLAlchemy queries in `apps/api/app/repositories/__init__.py`
3. Add business logic in `apps/api/app/services/`
4. Add route handler in `apps/api/app/api/v1/endpoints/`
5. Register in `apps/api/app/api/v1/router.py`

## License

MIT