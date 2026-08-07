# PHOENIX Backend Foundation

This is the core backend for the PHOENIX AI-Powered Digital Scam Investigation Platform.

## Architecture

Built with:
- **Python 3.12+**
- **FastAPI** (Web Framework)
- **SQLAlchemy 2.x** (ORM)
- **Pydantic v2** (Data Validation)
- **PostgreSQL** (Primary Database)
- **Redis & Celery** (Async Task Queue)

## Getting Started

1. Create a virtual environment: `python3 -m venv venv`
2. Activate: `source venv/bin/activate`
3. Install dependencies: `pip install -e ".[dev]"`
4. Run server: `uvicorn app.main:app --reload`
