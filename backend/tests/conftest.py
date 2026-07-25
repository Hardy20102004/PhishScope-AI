import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.db.session import SessionLocal

@pytest.fixture
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
async def async_client():
    """
    Provides an asynchronous HTTPX client for testing FastAPI endpoints.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
