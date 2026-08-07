import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.k8s_security import K8sRBACPolicy
from typing import Dict, Any

class RBACAnalysisEngine:
    """
    Calculates effective privilege and flags over-privileged identities.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def analyze_subject(self, tenant_id: uuid.UUID, cluster_id: uuid.UUID, name: str, s_type: str, ns: str, perms: Dict[str, Any]) -> K8sRBACPolicy:
        # Simple analysis: if verbs contains '*' and resources contains '*', it's overprivileged.
        verbs = perms.get("verbs", [])
        resources = perms.get("resources", [])
        is_over = "*" in verbs and "*" in resources
        
        policy = K8sRBACPolicy(
            tenant_id=tenant_id,
            cluster_id=cluster_id,
            subject_name=name,
            subject_type=s_type,
            namespace=ns,
            effective_permissions=perms,
            is_overprivileged=is_over
        )
        self.db.add(policy)
        await self.db.commit()
        await self.db.refresh(policy)
        return policy
