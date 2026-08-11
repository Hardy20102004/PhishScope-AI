import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status
import uuid
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

from app.models.appsec_command_center import GovernanceDecisionStatus

@pytest.mark.asyncio
async def test_ingest_and_list_consolidated_findings(
    async_client: AsyncClient, db_session: AsyncSession
):
    finding_data = {
        "application_id": "payment-service",
        "source_scanner": "SAST",
        "severity": "HIGH",
        "cwe_id": "CWE-89",
        "title": "SQL Injection found in login endpoint",
        "description": "Unsanitized user input is directly concatenated into the SQL query.",
        "is_remediated": False
    }

    # Ingest
    r = await async_client.post(
        "/api/v1/appsec-command-center/consolidated-findings",
        json=finding_data,
    )
    assert r.status_code == status.HTTP_200_OK
    created_finding = r.json()
    assert created_finding["title"] == finding_data["title"]
    assert "id" in created_finding

    # List
    r = await async_client.get(
        "/api/v1/appsec-command-center/consolidated-findings",
    )
    assert r.status_code == status.HTTP_200_OK
    findings = r.json()
    assert len(findings) >= 1
    assert any(f["id"] == created_finding["id"] for f in findings)


@pytest.mark.asyncio
async def test_engineering_intelligence(
    async_client: AsyncClient, db_session: AsyncSession
):
    metric_data = {
        "application_id": "payment-service",
        "mean_time_to_remediate_days": 2.5,
        "deployment_frequency_per_week": 14.0,
        "security_friction_score": 12.5
    }

    # Log metric
    r = await async_client.post(
        "/api/v1/appsec-command-center/engineering-intelligence",
        json=metric_data,
    )
    assert r.status_code == status.HTTP_200_OK

    # Get metrics
    r = await async_client.get(
        "/api/v1/appsec-command-center/engineering-intelligence",
    )
    assert r.status_code == status.HTTP_200_OK
    metrics = r.json()
    assert len(metrics) >= 1


@pytest.mark.asyncio
async def test_executive_summary(
    async_client: AsyncClient, db_session: AsyncSession
):
    metric_data = {
        "enterprise_risk_score": 35.5,
        "compliance_posture": 92.0,
        "total_critical_vulnerabilities": 12
    }

    # Log
    r = await async_client.post(
        "/api/v1/appsec-command-center/executive-summary",
        json=metric_data,
    )
    assert r.status_code == status.HTTP_200_OK

    # Get
    r = await async_client.get(
        "/api/v1/appsec-command-center/executive-summary",
    )
    assert r.status_code == status.HTTP_200_OK
    metrics = r.json()
    assert len(metrics) >= 1


@pytest.mark.asyncio
async def test_governance_decision(
    async_client: AsyncClient, db_session: AsyncSession
):
    decision_data = {
        "policy_name": "Block builds on HIGH SAST findings",
        "proposed_change": "Change current policy from non-blocking to blocking for any SAST finding with severity HIGH or above."
    }

    # Propose
    r = await async_client.post(
        "/api/v1/appsec-command-center/governance",
        json=decision_data,
    )
    assert r.status_code == status.HTTP_200_OK
    decision = r.json()
    assert decision["status"] == "PENDING"
    decision_id = decision["id"]

    # Approve
    r = await async_client.post(
        f"/api/v1/appsec-command-center/governance/{decision_id}/approve",
    )
    assert r.status_code == status.HTTP_200_OK
    approved_decision = r.json()
    assert approved_decision["status"] == "APPROVED"
    assert approved_decision["approved_by"] is not None
