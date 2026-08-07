import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.cwpp import RuntimeEvent

class RuntimeVisibilityEngine:
    """
    Ingests process, network, and file events from the workload operating system.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def log_event(self, tenant_id: uuid.UUID, workload_id: uuid.UUID, e_type: str, proc: str = None, cmd: str = None, dest_ip: str = None) -> RuntimeEvent:
        event = RuntimeEvent(
            tenant_id=tenant_id,
            workload_id=workload_id,
            event_type=e_type,
            process_name=proc,
            command_line=cmd,
            destination_ip=dest_ip
        )
        self.db.add(event)
        await self.db.commit()
        await self.db.refresh(event)
        return event
