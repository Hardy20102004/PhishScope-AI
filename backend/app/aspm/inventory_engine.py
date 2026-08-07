import uuid
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.aspm import EnterpriseApplication
from app.schemas.aspm import EnterpriseApplicationCreate

class ApplicationInventoryEngine:
    """
    Manages the centralized inventory of all discovered enterprise applications.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_application(self, tenant_id: uuid.UUID, app_in: EnterpriseApplicationCreate) -> EnterpriseApplication:
        # Check if exists
        stmt = select(EnterpriseApplication).where(
            EnterpriseApplication.tenant_id == tenant_id,
            EnterpriseApplication.name == app_in.name
        )
        existing = await self.db.execute(stmt)
        app = existing.scalar_one_or_none()
        
        if app:
            app.description = app_in.description
            app.owner = app_in.owner
            app.business_unit = app_in.business_unit
            app.criticality = app_in.criticality
            app.is_internet_facing = app_in.is_internet_facing
            app.has_pii = app_in.has_pii
            app.metadata_json = app_in.metadata_json
        else:
            app = EnterpriseApplication(
                tenant_id=tenant_id,
                name=app_in.name,
                description=app_in.description,
                owner=app_in.owner,
                business_unit=app_in.business_unit,
                criticality=app_in.criticality,
                is_internet_facing=app_in.is_internet_facing,
                has_pii=app_in.has_pii,
                metadata_json=app_in.metadata_json
            )
            self.db.add(app)
            
        await self.db.commit()
        await self.db.refresh(app)
        return app

    async def get_application(self, app_id: uuid.UUID) -> Optional[EnterpriseApplication]:
        stmt = select(EnterpriseApplication).where(EnterpriseApplication.id == app_id)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def list_applications(self, tenant_id: uuid.UUID) -> List[EnterpriseApplication]:
        stmt = select(EnterpriseApplication).where(EnterpriseApplication.tenant_id == tenant_id)
        res = await self.db.execute(stmt)
        return res.scalars().all()
