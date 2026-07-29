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
async def test_copilot_session_init(async_client: AsyncClient, db_session: AsyncSession):
    payload = {
        "repository_context": "github.com/org/payment-service",
        "environment": "VS_CODE",
        "status": "ACTIVE"
    }
    
    response = await async_client.post("/api/v1/copilot/sessions", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["environment"] == "VS_CODE"
    assert data["developer_id"] == str(TEST_USER_ID)
    assert "id" in data

@pytest.mark.asyncio
async def test_copilot_review_submission(async_client: AsyncClient, db_session: AsyncSession):
    # 1. Submit review
    payload = {
        "repository_url": "github.com/org/payment-service",
        "pull_request_id": "PR-102",
        "commit_hash": "a1b2c3d4"
    }
    
    response = await async_client.post("/api/v1/copilot/review", json=payload)
    assert response.status_code == 200
    review_data = response.json()
    assert review_data["status"] == "COMPLETED"
    review_id = review_data["id"]
    
    # 2. Add finding
    finding_payload = {
        "review_id": review_id,
        "file_path": "src/payment.py",
        "line_number": 42,
        "severity": "HIGH",
        "cwe_id": "CWE-89",
        "description": "Potential SQL Injection",
        "suggestion": "Use parameterized queries"
    }
    
    finding_res = await async_client.post("/api/v1/copilot/review/findings", json=finding_payload)
    assert finding_res.status_code == 200
    assert finding_res.json()["cwe_id"] == "CWE-89"

@pytest.mark.asyncio
async def test_copilot_learning_progress(async_client: AsyncClient, db_session: AsyncSession):
    payload = {
        "topic": "OWASP Top 10 - Injection",
        "modules_completed": 1
    }
    
    response = await async_client.post("/api/v1/copilot/learning", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["modules_completed"] == 1

@pytest.mark.asyncio
async def test_copilot_engineering_intelligence(async_client: AsyncClient, db_session: AsyncSession):
    payload = {
        "project_name": "payment-service",
        "technical_debt_score": 35.5,
        "security_trend_score": 8.2
    }
    
    response = await async_client.post("/api/v1/copilot/intelligence", json=payload)
    assert response.status_code == 200
    
    get_response = await async_client.get("/api/v1/copilot/intelligence")
    assert get_response.status_code == 200
    metrics = get_response.json()
    assert len(metrics) > 0
    assert metrics[0]["technical_debt_score"] == 35.5
