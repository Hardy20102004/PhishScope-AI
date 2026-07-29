from typing import Any, List
import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.api import deps
from app.models.user import User
from app.models.sca import SCADependency, SCALicense, SCARiskScore, SCARiskLevel
from app.schemas.sca import (
    SCADependencyCreate, SCADependencyResponse,
    SCAPackageIntelligenceCreate, SCAPackageIntelligenceResponse,
    SCALicenseCreate, SCALicenseResponse,
    SCARiskScoreCreate, SCARiskScoreResponse,
    SCAExecutiveSummary
)

from app.sca.dependency_discovery_engine import DependencyDiscoveryEngine
from app.sca.package_intelligence_engine import PackageIntelligenceEngine
from app.sca.license_analysis_engine import LicenseAnalysisEngine
from app.sca.supply_chain_risk_engine import SupplyChainRiskEngine

router = APIRouter()

@router.post("/dependencies", response_model=SCADependencyResponse)
async def register_dependency(
    dep_in: SCADependencyCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = DependencyDiscoveryEngine(db)
    return await engine.register_dependency(current_user.tenant_id, dep_in)

@router.get("/dependencies", response_model=List[SCADependencyResponse])
async def list_dependencies(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = DependencyDiscoveryEngine(db)
    return await engine.list_dependencies(current_user.tenant_id)

@router.post("/packages", response_model=SCAPackageIntelligenceResponse)
async def register_package_intelligence(
    pkg_in: SCAPackageIntelligenceCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = PackageIntelligenceEngine(db)
    return await engine.register_package_intelligence(current_user.tenant_id, pkg_in)

@router.post("/licenses", response_model=SCALicenseResponse)
async def register_license(
    lic_in: SCALicenseCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = LicenseAnalysisEngine(db)
    return await engine.register_license(current_user.tenant_id, lic_in)

@router.get("/licenses", response_model=List[SCALicenseResponse])
async def list_licenses(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = LicenseAnalysisEngine(db)
    return await engine.list_licenses(current_user.tenant_id)

@router.post("/risk-scores", response_model=SCARiskScoreResponse)
async def calculate_risk(
    score_in: SCARiskScoreCreate,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    engine = SupplyChainRiskEngine(db)
    return await engine.calculate_risk(current_user.tenant_id, score_in)

@router.get("/executive-summary", response_model=SCAExecutiveSummary)
async def get_executive_summary(
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    
    stmt = select(func.count(SCADependency.id)).where(SCADependency.tenant_id == current_user.tenant_id)
    total_deps = (await db.execute(stmt)).scalar_one_or_none() or 0
    
    stmt = select(func.count(SCARiskScore.id)).where(
        SCARiskScore.tenant_id == current_user.tenant_id,
        SCARiskScore.risk_level.in_([SCARiskLevel.CRITICAL, SCARiskLevel.HIGH])
    )
    vulnerable_deps = (await db.execute(stmt)).scalar_one_or_none() or 0
    
    stmt = select(func.count(SCALicense.id)).where(
        SCALicense.tenant_id == current_user.tenant_id,
        SCALicense.is_approved == False
    )
    license_violations = (await db.execute(stmt)).scalar_one_or_none() or 0
    
    return SCAExecutiveSummary(
        total_dependencies=total_deps,
        vulnerable_dependencies=vulnerable_deps,
        license_violations=license_violations,
        average_risk_score=45.5, # Placeholder
        abandoned_packages=12
    )
