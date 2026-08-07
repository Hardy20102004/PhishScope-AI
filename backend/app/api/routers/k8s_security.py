from typing import Any, List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from sqlalchemy import select

from app.api import deps
from app.models.user import User
from app.models.k8s_security import K8sCluster, K8sRBACPolicy, K8sRiskScore
from app.schemas.k8s_security import (
    K8sClusterResponse,
    K8sRBACPolicyResponse,
    K8sRiskScoreResponse
)

router = APIRouter()

@router.get("/clusters", response_model=List[K8sClusterResponse])
async def get_k8s_clusters(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves all discovered Kubernetes clusters.
    """
    res = await db.execute(select(K8sCluster).where(K8sCluster.tenant_id == current_user.tenant_id))
    return res.scalars().all()

@router.get("/clusters/{cluster_id}/rbac", response_model=List[K8sRBACPolicyResponse])
async def get_rbac_policies(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    cluster_id: uuid.UUID,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves RBAC policies and effective permissions for a specific cluster.
    """
    res = await db.execute(select(K8sRBACPolicy).where(
        K8sRBACPolicy.tenant_id == current_user.tenant_id,
        K8sRBACPolicy.cluster_id == cluster_id
    ))
    return res.scalars().all()

@router.get("/risk", response_model=List[K8sRiskScoreResponse])
async def get_cluster_risk_scores(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves aggregated risk scores for all Kubernetes clusters.
    """
    res = await db.execute(select(K8sRiskScore).where(K8sRiskScore.tenant_id == current_user.tenant_id))
    return res.scalars().all()
