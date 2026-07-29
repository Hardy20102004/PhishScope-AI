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
async def test_sast_scan_initiation(async_client: AsyncClient, db_session: AsyncSession):
    payload = {
        "branch": "main",
        "commit_sha": "a1b2c3d4",
        "files_scanned": 120,
        "lines_of_code": 15000
    }
    
    response = await async_client.post("/api/v1/sast/scans", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["branch"] == "main"
    assert data["status"] == "RUNNING"
    assert "id" in data

@pytest.mark.asyncio
async def test_sast_rule_registration(async_client: AsyncClient, db_session: AsyncSession):
    payload = {
        "rule_id": "PX-SAST-001",
        "name": "SQL Injection",
        "description": "Improper neutralization of special elements used in an SQL command.",
        "cwe": "CWE-89",
        "severity": "CRITICAL"
    }
    
    response = await async_client.post("/api/v1/sast/rules", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["rule_id"] == "PX-SAST-001"
    assert data["severity"] == "CRITICAL"
    assert "id" in data

@pytest.mark.asyncio
async def test_sast_finding_creation(async_client: AsyncClient, db_session: AsyncSession):
    scan_id = str(uuid.uuid4())
    
    payload = {
        "scan_id": scan_id,
        "rule_id": "PX-SAST-001",
        "file_path": "src/db/query.js",
        "line_number": 42,
        "severity": "HIGH",
        "exploitability_score": 7.5
    }
    
    response = await async_client.post("/api/v1/sast/findings", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["rule_id"] == "PX-SAST-001"
    assert data["file_path"] == "src/db/query.js"

@pytest.mark.asyncio
async def test_sast_executive_summary(async_client: AsyncClient, db_session: AsyncSession):
    response = await async_client.get("/api/v1/sast/executive-summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_scans" in data
    assert "critical_findings" in data
