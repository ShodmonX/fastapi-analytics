# FastAPI Analytics

A modern, asynchronous, and production-ready **FastAPI Analytics** built
with FastAPI.
Features include Docker, Alembic migrations, Pytest (90%+ coverage),
and GitHub Actions CI.

![Tests](https://github.com/ShodmonX/fastapi-analytics/workflows/Tests/badge.svg)
![Coverage](https://codecov.io/gh/ShodmonX/fastapi-analytics/branch/main/graph/badge.svg)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green)

## 🚀 Features

-   Fully async **FastAPI** backend
-   **PostgreSQL** with SQLAlchemy 2.0 (async)
-   **Pydantic v2** schemas
-   **Alembic** for database migrations
-   **Docker** & docker-compose (development + production)
-   **Pytest** with 80%+ coverage (async tests)
-   **GitHub Actions** CI integration

## 🛠 Tech Stack

-   FastAPI
-   PostgreSQL + asyncpg
-   SQLAlchemy 2.0 (async)
-   Alembic
-   Pydantic-settings
-   Docker / docker-compose
-   Pytest + httpx
-   GitHub Actions

## ⚡ Quick Start (Recommended: Docker)

``` bash
git clone https://github.com/ShodmonX/fastapi-analytics.git
cd blog-api
cp .env.example .env
docker compose up --build -d
docker compose exec web alembic upgrade head
```

## Project Structure
``` bash
.
├── alembic
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions
│       ├── cef7facba168_initial_revision.py
├── alembic.ini
├── app
│   ├── core
│   │   ├── config.py
│   ├── crud
│   │   ├── analytics.py
│   ├── db
│   │   ├── base.py
│   │   └── session.py
│   ├── main.py
│   ├── models
│   │   ├── activity.py
│   ├── routers
│   │   ├── analytics.py
│   └── schemas
│       ├── analytics.py
├── docker-compose.yml
├── Dockerfile
├── generate_fake_events.py
├── LICENSE
├── pyproject.toml
├── pytest.ini
├── README.md
├── requirements.txt
├── run.py
└── tests
    ├── conftest.py
    ├── test_db.py
    └── test_endpoints.py
```

### URLs

-   API Root: http://localhost:8080
-   Swagger UI: http://localhost:8080/docs
-   Health Check: http://localhost:8080/

## 🔧 Manual Setup (Without Docker)

``` bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload
```

## 🔐 Environment Variables (.env)

    API_TITLE=FASTAPI ANALYTICS
    API_VERSION=0.1.0
    DEBUG=1

## API Endpoints

| Method | Endpoint                                | Description                        |
|--------|-----------------------------------------|------------------------------------|
| POST   | `/analytics/`                           | Add activity                       |
| GET    | `/analytics/`                           | Get activities                     |
| GET    | `/analytics/users/{user_id}/`           | Get user activity                  |
| GET    | `/analytics/stats/`                     | Get Statistics                     |
| GET    | `/analytics/top-events/`                | Get top events                     |
| GET    | `/analytics/users/{user_id}/last-seen/` | Get user last seen                 |
| GET    | `/`                                     | Server holatini tekshirish         |

## 🧪 Testing

``` bash
pytest
pytest --cov=app
```

## 🚀 Production Deployment

-   Render.com
-   Railway
-   Fly.io

### VPS (e.g., Contabo)

``` bash
docker-compose -f docker-compose.yml up -d
```

## 👨‍💻 Author

ShodmonX -- 2025
GitHub: https://github.com/ShodmonX

## ✨ Contributing

Contributions are welcome!

## 📜 License

[MIT License](LICENCE)