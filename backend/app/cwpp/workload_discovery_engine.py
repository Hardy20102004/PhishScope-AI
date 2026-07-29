import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.cwpp import CloudWorkload

class WorkloadDiscoveryEngine:
    """
    Inventories active and stopped compute workloads (VMs, Containers, Serverless).
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_workload(self, tenant_id: uuid.UUID, w_type: str, name: str, provider: str, region: str) -> CloudWorkload:
        workload = CloudWorkload(
            tenant_id=tenant_id,
            workload_type=w_type,
            workload_name=name,
            provider=provider,
            region=region,
            status="RUNNING"
        )
        self.db.add(workload)
        await self.db.commit()
        await self.db.refresh(workload)
        return workload
