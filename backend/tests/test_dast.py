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
async def test_dast_target_registration(async_client: AsyncClient, db_session: AsyncSession):
    payload = {
        "name": "Acme Web Portal",
        "base_url": "https://portal.acme.com",
        "target_type": "WEB_APP",
        "auth_method": "OIDC"
    }
    
    response = await async_client.post("/api/v1/dast/targets", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Acme Web Portal"
    assert "id" in data

@pytest.mark.asyncio
async def test_dast_scan_initiation(async_client: AsyncClient, db_session: AsyncSession):
    target_id = str(uuid.uuid4())
    payload = {
        "target_id": target_id,
        "endpoints_tested": 50
    }
    
    response = await async_client.post("/api/v1/dast/scans", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "RUNNING"
    assert "id" in data

@pytest.mark.asyncio
async def test_dast_finding_creation(async_client: AsyncClient, db_session: AsyncSession):
    scan_id = str(uuid.uuid4())
    
    payload = {
        "scan_id": scan_id,
        "vulnerability_name": "Reflected Cross-Site Scripting (XSS)",
        "url": "https://portal.acme.com/search",
        "method": "GET",
        "severity": "HIGH",
        "exploitability_score": 8.0
    }
    
    response = await async_client.post("/api/v1/dast/findings", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["vulnerability_name"] == "Reflected Cross-Site Scripting (XSS)"
    assert data["url"] == "https://portal.acme.com/search"

@pytest.mark.asyncio
async def test_dast_executive_summary(async_client: AsyncClient, db_session: AsyncSession):
    response = await async_client.get("/api/v1/dast/executive-summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_targets" in data
    assert "critical_findings" in data
