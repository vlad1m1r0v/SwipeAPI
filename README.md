# SwipeAPI

A production-grade REST API for a real-estate marketplace platform, connecting property owners, real-estate agents, developers (builders) and admins in a single role-based backend.

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Asyncpg-4169E1?logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-6-DC382D?logo=redis&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-5.5-37814A?logo=celery&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white)
![Poetry](https://img.shields.io/badge/Poetry-dependency%20manager-60A5FA?logo=poetry&logoColor=white)

## About The Project

SwipeAPI is an asynchronous, modular monolith backend for an online real-estate marketplace. It lets private property owners publish apartments and announcements, lets developers (builders) manage residential complexes and approve "add to complex" requests from users, and gives admins moderation tooling (notary directory, blacklist, complaint handling).

The service solves the coordination problem between buyers, sellers, agents and developers by centralising listings, complex catalogues, paid promotions, subscriptions and user balances in one consistent API. The target audience is mobile/web real-estate platforms that need an enterprise-grade marketplace backend out of the box.

## Key Tech Stack

| Layer | Technology |
| --- | --- |
| Backend | Python 3.11+, FastAPI 0.115, Pydantic v2, Uvicorn / Gunicorn |
| ORM / Data | SQLAlchemy 2.0, Advanced-Alchemy 1.4, Alembic migrations, Asyncpg (async) + Psycopg2 (sync) |
| Database | PostgreSQL |
| Caching / Broker | Redis 6 (in-memory store, Celery broker & result backend) |
| Background Tasks | Celery 5.5 + Celery Beat (scheduled jobs) |
| Dependency Injection | Dishka 1.5 (shared across FastAPI and Celery) |
| Auth & Security | PyJWT (RS256), Bcrypt, Itsdangerous-signed password-reset tokens |
| Email | FastAPI-Mail + Jinja2 HTML templates |
| DevOps / Deployment | Docker (server / worker / beat / nginx images), Poetry, Make, pre-commit (Ruff + Mypy) |

## Core Features

- **Role-based authentication & authorization** — `user`, `builder` and `admin` roles with dedicated guards (`user_from_token`, `builder_from_token`, `admin_from_token`), RS256 JWT access (15 min) + refresh (30 days) token pair, token refresh flow.
- **Password management** — update, forgot/reset flows backed by expiring signed tokens and asynchronous HTML emails.
- **User accounts** — profile, contact & agent-contact data, notification settings, balance (top-up endpoint) and monthly subscription with optional auto-renewal.
- **Subscription lifecycle** — daily Celery Beat job (`daily_withdrawal`) automatically debits the balance and extends the subscription for users with auto-renewal enabled.
- **Apartments & announcements** — CRUD for apartments (with gallery and floor-plan images), announcement publishing, relevance tracking, view counting, favourites and saved search filters (max 5 per user).
- **Advanced listing search** — multi-criteria filtering (price, area, rooms, finishing, district, complex type/status, property type, billing options) combined with saved filters and priority ordering.
- **Paid promotions** — highlight colour, custom phrase, boost and big-advert placements with one-month expiry dates, priced and deducted atomically from the user's balance.
- **Developer (builder) module** — residential complex profiles with advantages, infrastructure, formalization & payment settings, news, documents and photo galleries.
- **"Add to complex" requests** — users request to join a developer's complex; builders approve or reject, guarded by unique apartment/floor/riser constraints.
- **Buildings catalogue** — blocks, floors, sections and risers hierarchy exposed via a shared grid endpoint.
- **Notary directory** — admin-managed directory of notaries with media uploads.
- **Admin moderation** — user management with search, blacklist, complaint review; announcements with open complaints are excluded from the public feed.
- **Media handling** — local file storage with automatic cleanup of orphaned images/files on record update or deletion.
- **Consistent API contract** — unified `SuccessResponse` envelope, centralized exception mapping and auto-generated OpenAPI response examples.

## Architecture & Engineering Highlights

- **Modular monolith** organized into domain modules (`auth`, `user`, `admin`, `builder`, `buildings`, `apartments`, `notaries`, `requests`, `announcements`), each following the same **endpoints → services → repositories → models + schemas** layering.
- **Advanced-Alchemy repository/service pattern** — reusable `SQLAlchemyAsyncRepositoryService` base classes give uniform CRUD, pagination (`OffsetPagination`/`LimitOffset`) and schema serialization across modules.
- **Dishka DI** with `APP`/`REQUEST` scopes provides the same container graph to both the FastAPI app and Celery workers, keeping dependency wiring declarative and testable.
- **Dual-engine database access** — an async engine (Asyncpg) serves the API while a synchronous engine (Psycopg2) backs Celery tasks, both sharing one `DBConfig`.
- **Custom query optimization** — hand-tuned repository queries use correlated/aggregated subqueries for denormalized fields (total floors per block, views & favourites counts), `joinedload`/`selectinload` eager loading to avoid N+1, and a bespoke `list_and_count` that returns paginated rows together with a distinct total.
- **Scheduled background processing** — Celery Beat runs `daily_withdrawal` (subscription renewals) and `daily_announcement_status_change` (announcement relevance after 7 days) at midnight UTC.
- **Centralized error handling** — a unified error envelope (`status / error.code / error.details`) with DB integrity errors mapped to 409/404 and a custom 422 validator, so every response shape is predictable.
- **Transactional integrity** — promotion purchases verify the balance, then update promotion expiry dates and debit the balance in the same transaction.
- **Self-documenting API** — Pydantic v2 schemas, `generate_examples` response documentation, `response_model_exclude_none` and built-in Swagger/ReDoc.

## Quick Start / Getting Started

### Prerequisites

- Python **3.11+** and [Poetry](https://python-poetry.org/)
- PostgreSQL and Redis running locally (or via Docker)
- OpenSSL (used to generate JWT keys)
- Docker (optional, for containerized setup)

### Local setup

1. Clone the repository and install dependencies:

   ```bash
   git clone <repo-url> && cd SwipeAPI
   poetry install
   ```

2. Configure environment variables:

   ```bash
   cp .env.example .env
   ```

   Fill in `DB_*`, `EMAIL_*`, `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND`, `REDIS_STORAGE_URL`, `SIGN_SECRET`, `SIGN_SALT` and `SERVER_URL`.

3. Generate the asymmetric JWT keys:

   ```bash
   make certificates
   ```

4. Apply database migrations:

   ```bash
   make migration-upgrade
   ```

5. (Optional) Seed demo data:

   ```bash
   make seed
   ```

6. Run the API server, and in separate terminals the Celery worker and beat:

   ```bash
   make server    # uvicorn server:server --port 8000 --workers 4
   make worker    # celery -A worker.celery worker
   make beat      # celery -A worker.celery beat
   ```

   The API is available at `http://localhost:8000`, with interactive docs at [`http://localhost:8000/docs`](http://localhost:8000/docs) (Swagger UI) and [`/redoc`](http://localhost:8000/redoc).

### Docker

The repository ships production-ready Dockerfiles for every service under `deploy/` (`server`, `worker`, `beat` on `python:3.11-slim`, plus an `nginx` reverse proxy that serves `/media/` and proxies to the FastAPI container). Orchestrate all services with Docker Compose:

```bash
docker-compose up --build
```

> Note: a root `docker-compose.yml` is not committed yet — create one referencing the images under `deploy/` (the nginx config expects the API on the `fastapi` hostname, port 8000).

## API Endpoints Overview

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/auth/user/register` | Register a new user account and receive an access/refresh token pair |
| `POST` | `/auth/user/login` | Authenticate a user and issue JWT tokens |
| `POST` | `/auth/tokens/refresh` | Rotate a refresh token into a new token pair |
| `GET` | `/announcements` | List/filter published announcements (price, area, rooms, complex, ...) |
| `GET` | `/announcements/{announcement_id}` | Announcement detail (tracks a view per request) |
| `POST` | `/user/announcements` | Create an announcement for an owned apartment |
| `GET` | `/user/profile` | Fetch the current user's profile (contact, subscription, balance, settings) |
| `POST` | `/user/balance/deposit` | Top up the user's balance |
| `POST` | `/user/requests` | Submit an "add to complex" request |
| `POST` | `/builder/requests/{request_id}/approve` | Approve a user's request to join the builder's complex |

Full interactive documentation: **Swagger UI** at `/docs` and **ReDoc** at `/redoc`.

## Future Roadmap

1. **Full-text search** — replace `ILIKE` filters with PostgreSQL full-text search (or a dedicated search engine such as Elasticsearch/Meilisearch) for fast, relevance-ranked listing search.
2. **Real payment integration** — connect subscription renewals and balance top-ups to a payment gateway (Stripe/Fondy) and introduce transactional ledger records, replacing the manual deposit endpoint.
3. **Read-model caching & resilience** — cache hot feed endpoints in Redis, add rate limiting, retry/backoff for Celery tasks, and ship a committed `docker-compose.yml` for one-command orchestration.
