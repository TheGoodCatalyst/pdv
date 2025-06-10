# Personal Data Vault (PDV)

**Mission:**
A secure, user-centric vault for agent frameworks to store and manage personal credentials and data (DIDs, verifiable credentials, payment tokens, preferences).

## Project Status
- **Milestone M1:** Repository initialized with LICENSE, README, and .gitignore.
- **Milestone M2:** Service skeleton with FastAPI, Docker, tests, and CI pipeline.
- **Milestone M3:** Storage layer with SQLAlchemy models, migrations, and SQLite support.

## Repository Structure
```
pdv-vault/
├── LICENSE
├── README.md
├── .gitignore
├── src/
│   ├── main.py
│   ├── api/
│   │   └── health.py
│   ├── core/
│   └── storage/
│       ├── database.py
│       ├── models.py
│       └── migrations/
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── Dockerfile
├── docker-compose.yml
├── .github/workflows/
│   └── ci.yml
└── tests/
    ├── test_health.py
    └── test_storage.py
```

## Getting Started

1. **Clone the repo**
   ```bash
   git clone https://github.com/<ORG>/pdv-vault.git
   cd pdv-vault
   ```

## Prerequisites
- Docker & Docker Compose
- Python 3.10+

## Run locally
```bash
docker-compose up --build
```

## Contribution
See CONTRIBUTING.md for guidelines.
