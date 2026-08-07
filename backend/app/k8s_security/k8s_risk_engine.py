import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.k8s_security import K8sRiskScore, K8sRBACPolicy
from sqlalchemy import select

class K8sRiskEngine:
    """
    Aggregates RBAC and config issues to generate a cluster risk score.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def update_cluster_risk(self, tenant_id: uuid.UUID, cluster_id: uuid.UUID) -> K8sRiskScore:
        # Get all overprivileged RBAC policies
        res = await self.db.execute(select(K8sRBACPolicy).where(
            K8sRBACPolicy.cluster_id == cluster_id,
            K8sRBACPolicy.is_overprivileged == True
        ))
        issues_count = len(res.scalars().all())
        
        score = min(issues_count * 20.0, 100.0) # 20 risk points per overprivileged account
        
        res = await self.db.execute(select(K8sRiskScore).where(K8sRiskScore.cluster_id == cluster_id))
        risk_record = res.scalars().first()
        
        if not risk_record:
            risk_record = K8sRiskScore(tenant_id=tenant_id, cluster_id=cluster_id, risk_score=score, rbac_issues_count=issues_count)
            self.db.add(risk_record)
        else:
            risk_record.risk_score = score
            risk_record.rbac_issues_count = issues_count
            
        await self.db.commit()
        await self.db.refresh(risk_record)
        return risk_record
