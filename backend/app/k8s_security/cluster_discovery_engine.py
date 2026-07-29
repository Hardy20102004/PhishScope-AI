import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.k8s_security import K8sCluster

class ClusterDiscoveryEngine:
    """
    Inventories Kubernetes clusters.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_cluster(self, tenant_id: uuid.UUID, name: str, provider: str, version: str, region: str) -> K8sCluster:
        cluster = K8sCluster(
            tenant_id=tenant_id,
            cluster_name=name,
            provider=provider,
            version=version,
            region=region,
            status="ACTIVE"
        )
        self.db.add(cluster)
        await self.db.commit()
        await self.db.refresh(cluster)
        return cluster
