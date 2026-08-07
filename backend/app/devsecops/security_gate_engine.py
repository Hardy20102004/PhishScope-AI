import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.devsecops import SecurityGate, PipelineRun, PipelineStatus, GateStatus
from app.schemas.devsecops import SecurityGateCreate

class SecurityGateEngine:
    """
    Evaluates rules (Code Quality, SAST, SCA, Secrets) to determine if a pipeline can proceed.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def record_gate_result(self, tenant_id: uuid.UUID, gate_in: SecurityGateCreate) -> SecurityGate:
        gate = SecurityGate(
            tenant_id=tenant_id,
            pipeline_run_id=gate_in.pipeline_run_id,
            gate_name=gate_in.gate_name,
            gate_type=gate_in.gate_type,
            status=gate_in.status,
            details=gate_in.details
        )
        self.db.add(gate)
        
        # If gate failed, block pipeline
        if gate_in.status == GateStatus.FAIL:
            stmt = select(PipelineRun).where(PipelineRun.id == gate_in.pipeline_run_id)
            run = (await self.db.execute(stmt)).scalar_one_or_none()
            if run:
                run.status = PipelineStatus.BLOCKED
                
        await self.db.commit()
        await self.db.refresh(gate)
        return gate

    async def get_gates_for_pipeline(self, pipeline_run_id: uuid.UUID) -> List[SecurityGate]:
        stmt = select(SecurityGate).where(SecurityGate.pipeline_run_id == pipeline_run_id)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())
