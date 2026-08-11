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
    from tests.conftest import TestingSessionLocal
    db = TestingSessionLocal()
    try:
        yield AsyncMockSession(db)
    finally:
        db.close()

app.dependency_overrides[get_current_active_user] = mock_get_current_active_user
app.dependency_overrides[get_async_db] = mock_get_async_db

@pytest.mark.asyncio
async def test_iac_template_registration(async_client: AsyncClient, db_session: AsyncSession):
    payload = {
        "name": "EKS Cluster Build",
        "technology": "TERRAFORM",
        "repository_url": "github.com/org/infra",
        "file_path": "modules/eks/main.tf"
    }
    
    response = await async_client.post("/api/v1/iac/templates", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "EKS Cluster Build"
    assert "id" in data

@pytest.mark.asyncio
async def test_iac_finding_registration(async_client: AsyncClient, db_session: AsyncSession):
    template_id = str(uuid.uuid4())
    payload = {
        "template_id": template_id,
        "severity": "CRITICAL",
        "category": "NETWORK",
        "title": "Public Security Group",
        "description": "Port 22 is open to 0.0.0.0/0",
        "resource_id": "aws_security_group.ssh"
    }
    
    response = await async_client.post("/api/v1/iac/findings", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["severity"] == "CRITICAL"
    assert data["resource_id"] == "aws_security_group.ssh"

@pytest.mark.asyncio
async def test_iac_deployment_governance_flow(async_client: AsyncClient, db_session: AsyncSession):
    # 1. Register Deployment Intent
    template_id = str(uuid.uuid4())
    payload = {
        "template_id": template_id,
        "requested_by": str(TEST_USER_ID),
        "status": "PENDING_APPROVAL",
        "risk_score": 85.5
    }
    
    response = await async_client.post("/api/v1/iac/deployments", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "PENDING_APPROVAL"
    deployment_id = data["id"]
    
    # 2. Approve Deployment
    approve_response = await async_client.post(f"/api/v1/iac/deployments/{deployment_id}/approve")
    assert approve_response.status_code == 200
    approve_data = approve_response.json()
    assert approve_data["status"] == "APPROVED"
    assert approve_data["approved_by"] is not None
    assert approve_data["resolved_at"] is not None

@pytest.mark.asyncio
async def test_iac_executive_summary(async_client: AsyncClient, db_session: AsyncSession):
    response = await async_client.get("/api/v1/iac/executive-summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_templates" in data
    assert "critical_findings" in data
