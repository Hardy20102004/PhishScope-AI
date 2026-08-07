from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.api import deps
from app.cloud import schemas, tenant_manager

router = APIRouter()

@router.post("/", response_model=schemas.TenantResponse)
def create_tenant(tenant: schemas.TenantCreate, db: Session = Depends(deps.get_db)):
    manager = tenant_manager.TenantManager(db)
    if tenant.parent_id:
        return manager.create_sub_tenant(tenant.parent_id, tenant.name, tenant.description)
    return manager.get_or_create_tenant(tenant.name, tenant.description)

@router.get("/", response_model=List[schemas.TenantResponse])
def list_tenants(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    manager = tenant_manager.TenantManager(db)
    return manager.list_tenants(skip, limit)

@router.get("/{tenant_id}", response_model=schemas.TenantResponse)
def get_tenant(tenant_id: uuid.UUID, db: Session = Depends(deps.get_db)):
    manager = tenant_manager.TenantManager(db)
    tenant = manager.get_tenant(tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant

@router.post("/{tenant_id}/deactivate", response_model=dict)
def deactivate_tenant(tenant_id: uuid.UUID, db: Session = Depends(deps.get_db)):
    manager = tenant_manager.TenantManager(db)
    success = manager.deactivate_tenant(tenant_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return {"status": "success"}
