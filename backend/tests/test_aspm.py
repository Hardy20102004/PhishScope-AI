import pytest
import uuid
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.aspm import EnterpriseApplication, CodeRepository, SecurityFinding, ApplicationRisk
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
async def test_aspm_create_application(async_client: AsyncClient, db_session: AsyncSession):
    payload = {
        "name": "Payment Gateway v2",
        "description": "Core payment processing service",
        "owner": "john.doe@enterprise.com",
        "business_unit": "Finance",
        "criticality": "CRITICAL",
        "is_internet_facing": True,
        "has_pii": True
    }
    
    response = await async_client.post("/api/v1/aspm/applications", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Payment Gateway v2"
    assert "id" in data
    
    # Verify in DB
    app_id = uuid.UUID(data["id"])
    stmt = select(EnterpriseApplication).where(EnterpriseApplication.id == app_id)
    res = await db_session.execute(stmt)
    app = res.scalar_one_or_none()
    assert app is not None
    assert app.criticality.value == "CRITICAL"

@pytest.mark.asyncio
async def test_aspm_create_repository(async_client: AsyncClient, db_session: AsyncSession):
    payload = {
        "name": "payment-gateway",
        "url": "https://github.com/enterprise/payment-gateway",
        "provider": "GITHUB",
        "default_branch": "main"
    }
    
    response = await async_client.post("/api/v1/aspm/repositories", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "payment-gateway"
    assert "id" in data

@pytest.mark.asyncio
async def test_aspm_create_finding_and_risk(async_client: AsyncClient, db_session: AsyncSession):
    # 1. Create App
    app_payload = {
        "name": "Vulnerable App",
        "criticality": "HIGH",
        "is_internet_facing": True
    }
    app_resp = await async_client.post("/api/v1/aspm/applications", json=app_payload)
    app_id = app_resp.json()["id"]
    
    # 2. Create Findings
    findings = [
        {
            "application_id": app_id,
            "finding_type": "SAST",
            "severity": "CRITICAL",
            "title": "SQL Injection in Login",
            "description": "Unsanitized input in POST /login",
            "scanner_name": "SonarQube"
        },
        {
            "application_id": app_id,
            "finding_type": "SCA",
            "severity": "HIGH",
            "title": "Log4j Vulnerability",
            "description": "CVE-2021-44228 detected in dependencies",
            "scanner_name": "Snyk"
        }
    ]
    
    for f in findings:
        resp = await async_client.post("/api/v1/aspm/findings", json=f)
        assert resp.status_code == 200
        
    # 3. Calculate Risk
    risk_resp = await async_client.get(f"/api/v1/aspm/applications/{app_id}/risk")
    assert risk_resp.status_code == 200
    risk_data = risk_resp.json()
    
    # Base = 1 Critical (10) + 1 High (5) = 15
    # Criticality = HIGH (x1.2) = 18
    # Internet Facing = True (x1.3) = 23.4
    assert risk_data["overall_risk_score"] > 23.0
    assert risk_data["critical_findings_count"] == 1
    assert risk_data["high_findings_count"] == 1
    
    # 4. Executive Summary
    exec_resp = await async_client.get("/api/v1/aspm/executive-summary")
    assert exec_resp.status_code == 200
    exec_data = exec_resp.json()
    assert exec_data["total_applications"] >= 1
    assert exec_data["open_critical_findings"] >= 1
    assert exec_data["open_high_findings"] >= 1
