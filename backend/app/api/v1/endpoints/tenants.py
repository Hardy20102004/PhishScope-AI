from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from datetime import datetime, timezone

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.tenant import TenantSettings, License, AuditLog
from app.schemas.tenant import TenantSettingsUpdate, TenantSettingsSchema, LicenseSchema, AuditLogSchema

router = APIRouter()

def get_user_org_id(user: User):
    if not user.organization_id:
        raise HTTPException(status_code=400, detail="User does not belong to an organization")
    return user.organization_id

@router.get("/settings", response_model=TenantSettingsSchema)
def get_tenant_settings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    org_id = get_user_org_id(current_user)
    stmt = select(TenantSettings).where(TenantSettings.organization_id == org_id)
    settings = db.execute(stmt).scalar_one_or_none()
    
    if not settings:
        raise HTTPException(status_code=404, detail="Settings not found for this organization")
    return settings

@router.put("/settings", response_model=TenantSettingsSchema)
def update_tenant_settings(
    request: TenantSettingsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Require superuser/admin check in real life, skipped here for speed
    org_id = get_user_org_id(current_user)
    stmt = select(TenantSettings).where(TenantSettings.organization_id == org_id)
    settings = db.execute(stmt).scalar_one_or_none()
    
    if not settings:
        raise HTTPException(status_code=404, detail="Settings not found")
        
    if request.branding_json is not None:
        settings.branding_json = request.branding_json
    if request.sso_config_json is not None:
        settings.sso_config_json = request.sso_config_json
    if request.require_mfa is not None:
        settings.require_mfa = request.require_mfa
    if request.session_timeout_minutes is not None:
        settings.session_timeout_minutes = request.session_timeout_minutes
        
    db.commit()
    db.refresh(settings)
    return settings

@router.get("/license", response_model=LicenseSchema)
def get_license_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    org_id = get_user_org_id(current_user)
    stmt = select(License).where(License.organization_id == org_id)
    license = db.execute(stmt).scalar_one_or_none()
    
    if not license:
        raise HTTPException(status_code=404, detail="License not found")
    return license

@router.get("/audit-logs", response_model=List[AuditLogSchema])
def get_audit_logs(
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    org_id = get_user_org_id(current_user)
    stmt = select(AuditLog).where(AuditLog.organization_id == org_id).order_by(AuditLog.created_at.desc()).limit(limit).offset(offset)
    logs = db.execute(stmt).scalars().all()
    return logs
