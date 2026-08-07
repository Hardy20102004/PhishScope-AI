from typing import Any, List
import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.api import deps
from app.models.user import User
from app.models.sbom import SBOMRecord, SoftwareArtifact, SoftwareDependency, ProvenanceMetadata, IntegrityStatus
from app.schemas.sbom import (
    SBOMRecordCreate, SBOMRecordResponse,
    SoftwareArtifactCreate, SoftwareArtifactResponse,
    SoftwareDependencyCreate, SoftwareDependencyResponse,
    ProvenanceMetadataCreate, ProvenanceMetadataResponse,
    SBOMExecutiveSummary
)

from app.sbom.sbom_management_engine import SBOMManagementEngine
from app.sbom.artifact_inventory_engine import ArtifactInventoryEngine
from app.sbom.dependency_discovery_engine import DependencyDiscoveryEngine
from app.sbom.provenance_verification_engine import ProvenanceVerificationEngine

router = APIRouter()

@router.post("/records", response_model=SBOMRecordResponse)
async def ingest_sbom(
    sbom_in: SBOMRecordCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = SBOMManagementEngine(db)
    return await engine.ingest_sbom(current_user.tenant_id, sbom_in)

@router.get("/records", response_model=List[SBOMRecordResponse])
async def list_sboms(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = SBOMManagementEngine(db)
    return await engine.list_sboms(current_user.tenant_id)

@router.get("/artifacts", response_model=List[SoftwareArtifactResponse])
async def list_artifacts(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = ArtifactInventoryEngine(db)
    return await engine.list_artifacts(current_user.tenant_id)

@router.get("/dependencies", response_model=List[SoftwareDependencyResponse])
async def list_dependencies(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = DependencyDiscoveryEngine(db)
    return await engine.list_dependencies(current_user.tenant_id)

@router.post("/provenance/verify", response_model=ProvenanceMetadataResponse)
async def verify_provenance(
    prov_in: ProvenanceMetadataCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = ProvenanceVerificationEngine(db)
    return await engine.verify_provenance(current_user.tenant_id, prov_in)

@router.get("/executive-summary", response_model=SBOMExecutiveSummary)
async def get_executive_summary(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    
    stmt = select(func.count(SBOMRecord.id)).where(SBOMRecord.tenant_id == current_user.tenant_id)
    total_sboms = (await db.execute(stmt)).scalar_one_or_none() or 0
    
    stmt = select(func.count(SoftwareArtifact.id)).where(SoftwareArtifact.tenant_id == current_user.tenant_id)
    total_artifacts = (await db.execute(stmt)).scalar_one_or_none() or 0
    
    stmt = select(func.count(SoftwareDependency.id)).where(SoftwareDependency.tenant_id == current_user.tenant_id)
    total_dependencies = (await db.execute(stmt)).scalar_one_or_none() or 0
    
    stmt = select(func.count(ProvenanceMetadata.id)).where(
        ProvenanceMetadata.tenant_id == current_user.tenant_id,
        ProvenanceMetadata.integrity_status == IntegrityStatus.UNVERIFIED
    )
    unverified_provenance = (await db.execute(stmt)).scalar_one_or_none() or 0
    
    return SBOMExecutiveSummary(
        total_sboms=total_sboms,
        total_artifacts=total_artifacts,
        total_dependencies=total_dependencies,
        unverified_provenance=unverified_provenance,
        average_supply_chain_score=78.5 # Placeholder
    )
