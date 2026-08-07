from sqlalchemy.orm import Session
from app.cloud.models import PlatformCloudAuditLog
import uuid
from typing import Dict, Any, List, Optional
from loguru import logger

class AuditService:
    """
    Immutable audit trail for cloud operations.
    """
    def __init__(self, db: Session):
        self.db = db

    def log_action(self, user_id: uuid.UUID, action: str, resource_id: Optional[str] = None, tenant_id: Optional[uuid.UUID] = None, details: Dict[str, Any] = None) -> PlatformCloudAuditLog:
        logger.info(f"AUDIT [{action}] by User {user_id} on Resource {resource_id}")
        log = PlatformCloudAuditLog(
            user_id=user_id,
            action=action,
            resource_id=resource_id,
            tenant_id=tenant_id,
            details=details or {}
        )
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log

    def get_logs(self, tenant_id: Optional[uuid.UUID] = None, limit: int = 100) -> List[PlatformCloudAuditLog]:
        query = self.db.query(PlatformCloudAuditLog)
        if tenant_id:
            query = query.filter(PlatformCloudAuditLog.tenant_id == tenant_id)
        return query.order_by(PlatformCloudAuditLog.timestamp.desc()).limit(limit).all()
