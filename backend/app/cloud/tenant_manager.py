from sqlalchemy.orm import Session
from app.cloud.models import Tenant
import uuid
from loguru import logger
from typing import Optional, List

class TenantManager:
    """
    Manages organizational boundaries and multi-tier tenant hierarchies.
    """
    def __init__(self, db: Session):
        self.db = db

    def get_tenant(self, tenant_id: uuid.UUID) -> Optional[Tenant]:
        return self.db.query(Tenant).filter(Tenant.id == tenant_id).first()

    def get_or_create_tenant(self, name: str, description: str = None, parent_id: uuid.UUID = None) -> Tenant:
        tenant = self.db.query(Tenant).filter(Tenant.name == name).first()
        if not tenant:
            logger.info(f"Creating new tenant: {name}")
            tenant = Tenant(name=name, description=description, parent_id=parent_id)
            self.db.add(tenant)
            self.db.commit()
            self.db.refresh(tenant)
        return tenant

    def create_sub_tenant(self, parent_id: uuid.UUID, name: str, description: str = None) -> Tenant:
        parent = self.get_tenant(parent_id)
        if not parent:
            raise ValueError("Parent tenant does not exist")
        return self.get_or_create_tenant(name=name, description=description, parent_id=parent_id)

    def list_tenants(self, skip: int = 0, limit: int = 100) -> List[Tenant]:
        return self.db.query(Tenant).offset(skip).limit(limit).all()

    def get_sub_tenants(self, tenant_id: uuid.UUID) -> List[Tenant]:
        return self.db.query(Tenant).filter(Tenant.parent_id == tenant_id).all()

    def deactivate_tenant(self, tenant_id: uuid.UUID) -> bool:
        tenant = self.get_tenant(tenant_id)
        if tenant:
            tenant.is_active = False
            self.db.commit()
            return True
        return False
