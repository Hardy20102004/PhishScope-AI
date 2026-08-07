import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ctem import BusinessContextBoundary
from sqlalchemy import select

class BusinessContextEngine:
    """
    Overlays business criticality metadata onto the physical asset graph at the boundary level.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def define_boundary(self, tenant_id: uuid.UUID, name: str, b_type: str, identifier: str, criticality: str) -> BusinessContextBoundary:
        boundary = BusinessContextBoundary(
            tenant_id=tenant_id,
            boundary_name=name,
            boundary_type=b_type,
            boundary_identifier=identifier,
            business_criticality=criticality
        )
        self.db.add(boundary)
        await self.db.commit()
        await self.db.refresh(boundary)
        return boundary
        
    async def get_criticality_multiplier(self, tenant_id: uuid.UUID, boundary_identifier: str) -> float:
        # Simplistic mapping for the prototype
        res = await self.db.execute(
            select(BusinessContextBoundary)
            .where(BusinessContextBoundary.tenant_id == tenant_id)
            .where(BusinessContextBoundary.boundary_identifier == boundary_identifier)
        )
        boundary = res.scalars().first()
        
        if not boundary:
            return 1.0 # Standard multiplier
            
        if boundary.business_criticality == "TIER_1":
            return 2.5
        elif boundary.business_criticality == "TIER_2":
            return 1.5
            
        return 1.0
