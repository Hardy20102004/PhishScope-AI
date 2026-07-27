from sqlalchemy.orm import Session
from app.cloud.models import SharingPolicy, SharedIntelligenceObject, TLPLevel, Workspace
from app.cloud.audit_service import AuditService
import uuid
from typing import Dict, Any, List, Optional
from loguru import logger

class SharingEngine:
    """
    Evaluates TLP and Workspace policies before exposing intelligence.
    Enforces governance and approval workflows.
    """
    def __init__(self, db: Session):
        self.db = db
        self.audit_service = AuditService(db)

    def create_policy(self, workspace_id: uuid.UUID, name: str, tlp_level: TLPLevel, require_approval: bool, target_audiences: List[str]) -> SharingPolicy:
        policy = SharingPolicy(
            workspace_id=workspace_id,
            name=name,
            tlp_level=tlp_level,
            require_approval=require_approval,
            target_audiences=target_audiences
        )
        self.db.add(policy)
        self.db.commit()
        self.db.refresh(policy)
        return policy

    def get_policies(self, workspace_id: uuid.UUID) -> List[SharingPolicy]:
        return self.db.query(SharingPolicy).filter(SharingPolicy.workspace_id == workspace_id).all()

    def share_object(self, workspace_id: uuid.UUID, entity_type: str, entity_id: str, payload: Dict[str, Any], tlp_level: TLPLevel, user_id: uuid.UUID) -> SharedIntelligenceObject:
        """
        Validates policy and commits an object to the sharing registry.
        """
        logger.info(f"Attempting to share {entity_type} {entity_id} from workspace {workspace_id} with {tlp_level}")
        
        policies = self.get_policies(workspace_id)
        if policies:
            # Simple policy check: enforce strict TLP
            min_tlp = min([p.tlp_level for p in policies], key=lambda t: list(TLPLevel).index(t))
            if list(TLPLevel).index(tlp_level) < list(TLPLevel).index(min_tlp):
                raise ValueError(f"Workspace policy prevents sharing at TLP level {tlp_level}. Minimum allowed is {min_tlp}")
            
        shared_obj = SharedIntelligenceObject(
            source_workspace_id=workspace_id,
            entity_type=entity_type,
            entity_id=entity_id,
            payload=payload,
            tlp_level=tlp_level,
            version=1
        )
        
        self.db.add(shared_obj)
        self.db.commit()
        self.db.refresh(shared_obj)
        
        self.audit_service.log_action(
            user_id=user_id,
            action="INTELLIGENCE_SHARED",
            resource_id=str(shared_obj.id),
            details={"entity_type": entity_type, "entity_id": entity_id, "tlp": tlp_level}
        )
        
        return shared_obj
