from sqlalchemy.orm import Session
from app.cloud.models import Workspace, WorkspaceType, WorkspaceMember, Tenant
import uuid
from loguru import logger
from typing import Optional, List

class WorkspaceManager:
    """
    Manages workspaces and their role-based access control.
    """
    def __init__(self, db: Session):
        self.db = db

    def create_workspace(self, tenant_id: uuid.UUID, name: str, workspace_type: WorkspaceType = WorkspaceType.PRIVATE) -> Workspace:
        tenant = self.db.query(Tenant).filter(Tenant.id == tenant_id).first()
        if not tenant:
            raise ValueError(f"Tenant {tenant_id} not found")

        logger.info(f"Creating workspace '{name}' for tenant {tenant_id}")
        workspace = Workspace(
            tenant_id=tenant_id,
            name=name,
            workspace_type=workspace_type
        )
        self.db.add(workspace)
        self.db.commit()
        self.db.refresh(workspace)
        return workspace

    def get_workspace(self, workspace_id: uuid.UUID) -> Optional[Workspace]:
        return self.db.query(Workspace).filter(Workspace.id == workspace_id).first()

    def list_workspaces(self, tenant_id: uuid.UUID) -> List[Workspace]:
        return self.db.query(Workspace).filter(Workspace.tenant_id == tenant_id).all()

    def add_member(self, workspace_id: uuid.UUID, user_id: uuid.UUID, role: str = "VIEWER") -> WorkspaceMember:
        workspace = self.get_workspace(workspace_id)
        if not workspace:
            raise ValueError("Workspace not found")
            
        existing_member = self.db.query(WorkspaceMember).filter(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id == user_id
        ).first()
        
        if existing_member:
            existing_member.role = role
            member = existing_member
        else:
            member = WorkspaceMember(workspace_id=workspace_id, user_id=user_id, role=role)
            self.db.add(member)
            
        self.db.commit()
        self.db.refresh(member)
        return member

    def remove_member(self, workspace_id: uuid.UUID, user_id: uuid.UUID) -> bool:
        member = self.db.query(WorkspaceMember).filter(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id == user_id
        ).first()
        if member:
            self.db.delete(member)
            self.db.commit()
            return True
        return False
        
    def get_members(self, workspace_id: uuid.UUID) -> List[WorkspaceMember]:
        return self.db.query(WorkspaceMember).filter(WorkspaceMember.workspace_id == workspace_id).all()
