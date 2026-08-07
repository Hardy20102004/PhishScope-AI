import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ctem import CloudExposureFinding
from app.ctem.business_context_engine import BusinessContextEngine

class ExposurePrioritizationEngine:
    """
    Calculates the true risk of an exposure by combining raw severity with business context.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_and_prioritize_finding(self, tenant_id: uuid.UUID, node_id: uuid.UUID, finding_type: str, name: str, raw_severity: float, boundary_identifier: str) -> CloudExposureFinding:
        # Calculate context
        bce = BusinessContextEngine(self.db)
        multiplier = await bce.get_criticality_multiplier(tenant_id, boundary_identifier)
        
        contextual_score = raw_severity * multiplier
        
        finding = CloudExposureFinding(
            tenant_id=tenant_id,
            attack_surface_node_id=node_id,
            finding_type=finding_type,
            finding_name=name,
            raw_severity=raw_severity,
            contextual_risk_score=contextual_score,
            status="OPEN"
        )
        self.db.add(finding)
        await self.db.commit()
        await self.db.refresh(finding)
        return finding
