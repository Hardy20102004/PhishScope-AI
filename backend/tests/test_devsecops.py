import pytest
import uuid
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.devsecops import PipelineRun, SecurityGate, SDLCWorkflow, DeveloperMetric
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
async def test_devsecops_create_pipeline_run(async_client: AsyncClient, db_session: AsyncSession):
    payload = {
        "ci_provider": "GITHUB_ACTIONS",
        "run_identifier": "run-10293",
        "branch": "main",
        "commit_sha": "abc123def456",
        "sdlc_phase": "BUILD"
    }
    
    response = await async_client.post("/api/v1/devsecops/pipelines", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["ci_provider"] == "GITHUB_ACTIONS"
    assert data["status"] == "QUEUED"
    assert "id" in data

@pytest.mark.asyncio
async def test_devsecops_create_security_gate_blocks_pipeline(async_client: AsyncClient, db_session: AsyncSession):
    # Create Pipeline
    pipe_payload = {
        "ci_provider": "GITLAB_CI",
        "run_identifier": "pipeline-42",
        "branch": "feature/payment",
        "commit_sha": "fff999ggg",
        "status": "RUNNING"
    }
    pipe_resp = await async_client.post("/api/v1/devsecops/pipelines", json=pipe_payload)
    pipe_id = pipe_resp.json()["id"]
    
    # Record failed gate
    gate_payload = {
        "pipeline_run_id": pipe_id,
        "gate_name": "SAST Check",
        "gate_type": "SAST",
        "status": "FAIL",
        "details": {"critical_issues": 3}
    }
    gate_resp = await async_client.post("/api/v1/devsecops/gates", json=gate_payload)
    assert gate_resp.status_code == 200
    
    # Verify pipeline is BLOCKED
    run_id_uuid = uuid.UUID(pipe_id)
    stmt = select(PipelineRun).where(PipelineRun.id == run_id_uuid)
    run = (await db_session.execute(stmt)).scalar_one_or_none()
    assert run is not None
    assert run.status.value == "BLOCKED"

@pytest.mark.asyncio
async def test_devsecops_developer_metrics(async_client: AsyncClient, db_session: AsyncSession):
    payload = {
        "developer_email": "jane.doe@enterprise.com",
        "code_quality_score": 95.5,
        "security_score": 88.0,
        "vulnerabilities_fixed": 12,
        "training_completed": True
    }
    
    resp = await async_client.post("/api/v1/devsecops/developer-metrics", json=payload)
    assert resp.status_code == 200
    
    list_resp = await async_client.get("/api/v1/devsecops/developer-metrics")
    assert list_resp.status_code == 200
    metrics = list_resp.json()
    assert len(metrics) >= 1
    assert metrics[0]["developer_email"] == "jane.doe@enterprise.com"
