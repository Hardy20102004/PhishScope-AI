import pytest
import uuid
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone, timedelta

from app.main import app
from app.api.deps import get_current_active_user, get_async_db
from app.models.user import User
from app.db.session import SessionLocal
from tests.conftest import AsyncMockSession

TEST_TENANT_ID = uuid.uuid4()
TEST_USER_ID = uuid.uuid4()

async def mock_get_current_active_user():
    user = User()
    user.id = TEST_USER_ID
    user.tenant_id = TEST_TENANT_ID
    return user

async def mock_get_async_db():
    db = SessionLocal()
    try:
        yield AsyncMockSession(db)
    finally:
        db.close()

app.dependency_overrides[get_current_active_user] = mock_get_current_active_user
app.dependency_overrides[get_async_db] = mock_get_async_db

@pytest.mark.asyncio
async def test_secrets_inventory_registration(async_client: AsyncClient, db_session: AsyncSession):
    payload = {
        "secret_type": "API_KEY",
        "name": "Stripe Prod Key",
        "identifier_hash": "a1b2c3d4",
        "location_uri": "github.com/org/repo/.env",
        "lifecycle_status": "ACTIVE"
    }
    
    response = await async_client.post("/api/v1/secrets/inventory", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Stripe Prod Key"
    assert data["secret_type"] == "API_KEY"
    assert "id" in data

@pytest.mark.asyncio
async def test_secrets_exposure_registration(async_client: AsyncClient, db_session: AsyncSession):
    secret_id = str(uuid.uuid4())
    payload = {
        "secret_id": secret_id,
        "exposure_type": "HARDCODED",
        "severity": "CRITICAL",
        "details": "Found in commit 1234abcd"
    }
    
    response = await async_client.post("/api/v1/secrets/exposures", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["exposure_type"] == "HARDCODED"
    assert data["severity"] == "CRITICAL"

@pytest.mark.asyncio
async def test_secrets_policy_registration(async_client: AsyncClient, db_session: AsyncSession):
    payload = {
        "name": "Database Rotation Policy",
        "description": "Rotate DB creds every 30 days",
        "target_secret_type": "DATABASE_CREDENTIAL",
        "max_age_days": 30
    }
    
    response = await async_client.post("/api/v1/secrets/policies", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Database Rotation Policy"
    assert data["max_age_days"] == 30

@pytest.mark.asyncio
async def test_secrets_executive_summary(async_client: AsyncClient, db_session: AsyncSession):
    response = await async_client.get("/api/v1/secrets/executive-summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_active_secrets" in data
    assert "total_exposures" in data
