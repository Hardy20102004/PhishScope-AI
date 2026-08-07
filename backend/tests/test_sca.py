import pytest
import uuid
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

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
async def test_sca_dependency_registration(async_client: AsyncClient, db_session: AsyncSession):
    payload = {
        "ecosystem": "NPM",
        "package_name": "react",
        "version_constraint": "^18.0.0",
        "resolved_version": "18.2.0",
        "dependency_type": "DIRECT"
    }
    
    response = await async_client.post("/api/v1/sca/dependencies", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["package_name"] == "react"
    assert data["resolved_version"] == "18.2.0"
    assert "id" in data

@pytest.mark.asyncio
async def test_sca_package_intelligence(async_client: AsyncClient, db_session: AsyncSession):
    payload = {
        "ecosystem": "PYPI",
        "package_name": "requests",
        "version": "2.31.0",
        "popularity_score": 9.5,
        "maintenance_score": 8.0,
        "known_cves": 0
    }
    
    response = await async_client.post("/api/v1/sca/packages", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["package_name"] == "requests"
    assert data["popularity_score"] == 9.5

@pytest.mark.asyncio
async def test_sca_risk_calculation(async_client: AsyncClient, db_session: AsyncSession):
    dependency_id = str(uuid.uuid4())
    
    payload = {
        "dependency_id": dependency_id,
        "vulnerability_risk": 90.0,
        "license_risk": 0.0,
        "operational_risk": 10.0
    }
    
    response = await async_client.post("/api/v1/sca/risk-scores", json=payload)
    assert response.status_code == 200
    data = response.json()
    # overall_score = (90 * 0.5) + (0 * 0.3) + (10 * 0.2) = 45.0 + 0 + 2.0 = 47.0
    assert data["overall_score"] == 47.0
    assert data["risk_level"] == "MEDIUM"

@pytest.mark.asyncio
async def test_sca_executive_summary(async_client: AsyncClient, db_session: AsyncSession):
    response = await async_client.get("/api/v1/sca/executive-summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_dependencies" in data
    assert "vulnerable_dependencies" in data
