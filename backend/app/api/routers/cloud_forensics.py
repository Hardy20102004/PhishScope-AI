from typing import Any
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models.user import User
from app.schemas.cloud_forensics import (
    CloudEnvironmentCreate,
    CloudEnvironmentResponse
)

from app.cloud_forensics.evidence_manager import EvidenceManager
from app.cloud_forensics.audit_engine import AuditEngine
from app.cloud_forensics.container_engine import ContainerEngine
from app.cloud_forensics.kubernetes_engine import KubernetesEngine

router = APIRouter()

@router.post("/environments", response_model=CloudEnvironmentResponse, status_code=status.HTTP_201_CREATED)
async def analyze_cloud_environment(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    env_in: CloudEnvironmentCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Ingests cloud evidence (Audit Logs, K8s manifests, Container configs) and runs forensic analysis.
    """
    # 1. Register Environment
    mgr = EvidenceManager(db)
    env = await mgr.register_environment(
        tenant_id=current_user.tenant_id,
        provider=env_in.provider,
        account_id=env_in.account_id,
        region=env_in.region,
        inv_id=env_in.investigation_id
    )
    
    # 2. Extract Audit Logs
    audit_eng = AuditEngine(db)
    await audit_eng.analyze_logs(env.id)
    
    # 3. Analyze Containers
    container_eng = ContainerEngine(db)
    await container_eng.analyze_containers(env.id)
    
    # 4. Analyze Kubernetes
    k8s_eng = KubernetesEngine(db)
    await k8s_eng.analyze_kubernetes(env.id)
        
    await db.refresh(env, ["audit_logs", "containers", "kubernetes_pods"])
    return env
