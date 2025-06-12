# Personal Data Vault (PDV)

**Mission:**
A secure, user-centric vault for agent frameworks to store and manage personal credentials and data (DIDs, verifiable credentials, payment tokens, preferences).

## Project Status
- **Milestone M1:** Repository initialized with LICENSE, README, and .gitignore.
- **Milestone M2:** Service skeleton with FastAPI, Docker, tests, and CI pipeline.
- **Milestone M3:** Storage layer with SQLAlchemy models, migrations, and SQLite support.
- **Milestone M4:** KMS abstraction with local stub and Vault/AWS providers.

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

### MCP Server

This repo now includes a small [Model Context Protocol](https://modelcontextprotocol.io/) server exposing PDV functionality as MCP tools. The server lives in `src/mcp_server.py` and is mounted under `/mcp` when running the FastAPI app. Any MCP compatible client (e.g. Claude Desktop) can connect to this endpoint to invoke the PDV tools.

Current tools include:

- **Credential Manager** – create, retrieve and revoke credentials.
- **Policy & Consent Engine** – record and check user consent decisions.
- **Proof Generation** – generate a simple signed proof for arbitrary data.

## Contribution
See CONTRIBUTING.md for guidelines.
