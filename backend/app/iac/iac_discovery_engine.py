import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.iac import IaCTemplate
from app.schemas.iac import IaCTemplateCreate

class IaCDiscoveryEngine:
    """
    Inventories templates from repos.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_template(self, tenant_id: uuid.UUID, template_in: IaCTemplateCreate) -> IaCTemplate:
        template = IaCTemplate(
            tenant_id=tenant_id,
            name=template_in.name,
            technology=template_in.technology,
            repository_url=template_in.repository_url,
            file_path=template_in.file_path
        )
        self.db.add(template)
        await self.db.commit()
        await self.db.refresh(template)
        return template

    async def list_templates(self, tenant_id: uuid.UUID) -> List[IaCTemplate]:
        stmt = select(IaCTemplate).where(IaCTemplate.tenant_id == tenant_id)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())
