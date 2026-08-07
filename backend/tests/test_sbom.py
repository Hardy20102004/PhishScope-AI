import pytest
import uuid
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.sbom import SBOMRecord, SoftwareArtifact, SoftwareDependency, ProvenanceMetadata, IntegrityStatus
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
async def test_sbom_ingestion(async_client: AsyncClient, db_session: AsyncSession):
    payload = {
        "name": "Acme API Service",
        "version": "1.0.42",
        "format": "CYCLONEDX",
        "component_count": 105,
        "raw_data": {"bomFormat": "CycloneDX", "specVersion": "1.4", "components": []}
    }
    
    response = await async_client.post("/api/v1/sbom/records", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Acme API Service"
    assert data["format"] == "CYCLONEDX"
    assert "id" in data

@pytest.mark.asyncio
async def test_sbom_provenance_verification(async_client: AsyncClient, db_session: AsyncSession):
    # Register an artifact first
    # In a real scenario, we'd mock an artifact endpoint, but for test isolation we'll just insert
    # We can use the real endpoint since we don't have a POST /artifacts, we'd normally seed the DB.
    # We'll just generate a random UUID for the artifact_id for the purpose of the test
    # since we bypassed foreign keys in mock DB.
    
    payload = {
        "artifact_id": str(uuid.uuid4()),
        "builder_id": "https://github.com/acme/api-service/.github/workflows/build.yml",
        "build_type": "https://slsa.dev/provenance/v0.2",
        "slsa_level": 3
    }
    
    response = await async_client.post("/api/v1/sbom/provenance/verify", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["integrity_status"] == "VERIFIED"
    assert data["slsa_level"] == 3

@pytest.mark.asyncio
async def test_sbom_executive_summary(async_client: AsyncClient, db_session: AsyncSession):
    response = await async_client.get("/api/v1/sbom/executive-summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_sboms" in data
    assert "average_supply_chain_score" in data
