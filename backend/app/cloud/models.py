import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Uuid, JSON, Enum, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.db.base_class import Base

class TLPLevel(str, enum.Enum):
    RED = "TLP:RED"
    AMBER = "TLP:AMBER"
    GREEN = "TLP:GREEN"
    CLEAR = "TLP:CLEAR"
    
class WorkspaceType(str, enum.Enum):
    PRIVATE = "PRIVATE"
    SHARED = "SHARED"
    INCIDENT = "INCIDENT"
    CAMPAIGN = "CAMPAIGN"
    THREAT_HUNTING = "THREAT_HUNTING"
    RESEARCH = "RESEARCH"
    READ_ONLY = "READ_ONLY"
    COLLABORATION = "COLLABORATION"

class Tenant(Base):
    """
    Represents an Organization or major Department (Multi-Tenant boundary).
    """
    __tablename__ = "cloud_tenants"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid(as_uuid=True), ForeignKey("cloud_tenants.id", ondelete="SET NULL"), nullable=True)
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    workspaces: Mapped[List["Workspace"]] = relationship("Workspace", back_populates="tenant", cascade="all, delete-orphan")
    sub_tenants: Mapped[List["Tenant"]] = relationship("Tenant", back_populates="parent")
    parent: Mapped[Optional["Tenant"]] = relationship("Tenant", back_populates="sub_tenants", remote_side=[id])


class Workspace(Base):
    """
    Logical container for investigations, campaigns, and intelligence objects.
    """
    __tablename__ = "cloud_workspaces"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("cloud_tenants.id", ondelete="CASCADE"), index=True)
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    workspace_type: Mapped[WorkspaceType] = mapped_column(Enum(WorkspaceType), default=WorkspaceType.PRIVATE)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="workspaces")
    members: Mapped[List["WorkspaceMember"]] = relationship("WorkspaceMember", back_populates="workspace", cascade="all, delete-orphan")
    sharing_policies: Mapped[List["SharingPolicy"]] = relationship("SharingPolicy", back_populates="workspace", cascade="all, delete-orphan")


class WorkspaceMember(Base):
    """
    Associates users with a workspace and specifies their RBAC role.
    """
    __tablename__ = "cloud_workspace_members"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("cloud_workspaces.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), index=True, nullable=False) # Refers to actual User model in main app
    
    role: Mapped[str] = mapped_column(String(50), default="VIEWER") # OWNER, EDITOR, VIEWER, CONTRIBUTOR
    added_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    workspace: Mapped["Workspace"] = relationship("Workspace", back_populates="members")


class SharingPolicy(Base):
    """
    Defines how intelligence can leave a workspace.
    """
    __tablename__ = "cloud_sharing_policies"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("cloud_workspaces.id", ondelete="CASCADE"), index=True)
    
    name: Mapped[str] = mapped_column(String(255), nullable=False, default="Default Policy")
    tlp_level: Mapped[TLPLevel] = mapped_column(Enum(TLPLevel), default=TLPLevel.AMBER)
    require_approval: Mapped[bool] = mapped_column(Boolean, default=True)
    anonymize_source: Mapped[bool] = mapped_column(Boolean, default=True)
    target_audiences: Mapped[List[str]] = mapped_column(JSON, default=list) # e.g. ["INTERNAL", "PARTNERS", "PUBLIC"]
    expiration_days: Mapped[Optional[int]] = mapped_column(Integer, nullable=True) # How many days until sharing expires
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    workspace: Mapped["Workspace"] = relationship("Workspace", back_populates="sharing_policies")


class SharedIntelligenceObject(Base):
    """
    A specific piece of intelligence (e.g., STIX bundle) flagged for federation/sharing.
    """
    __tablename__ = "cloud_shared_objects"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_workspace_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("cloud_workspaces.id"), index=True)
    
    entity_type: Mapped[str] = mapped_column(String(100), nullable=False) # 'Campaign', 'Threat Actor', 'Indicator'
    entity_id: Mapped[str] = mapped_column(String(255), nullable=False)
    
    payload: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False) # The actual intelligence data
    tlp_level: Mapped[TLPLevel] = mapped_column(Enum(TLPLevel), default=TLPLevel.AMBER)
    confidence: Mapped[int] = mapped_column(Integer, default=50) # 0-100
    
    version: Mapped[int] = mapped_column(Integer, default=1)
    
    shared_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class FederationNode(Base):
    """
    Represents an external TAXII/STIX node for federation.
    """
    __tablename__ = "cloud_federation_nodes"
    
    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(String(1024), nullable=False)
    
    node_type: Mapped[str] = mapped_column(String(100), default="PARTNER") # GOVERNMENT, PARTNER, ISAC, INTERNAL
    auth_method: Mapped[str] = mapped_column(String(50), default="MTLS") # API_KEY, OAUTH2, MTLS
    auth_config: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict) # Vault refs
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class FederationSyncRecord(Base):
    """
    Ledger of intelligence pushed/pulled from external nodes.
    """
    __tablename__ = "cloud_federation_syncs"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    node_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("cloud_federation_nodes.id", ondelete="CASCADE"), index=True)
    
    sync_type: Mapped[str] = mapped_column(String(50), nullable=False) # 'PUSH', 'PULL', 'FULL_SYNC', 'INCREMENTAL'
    objects_synced: Mapped[int] = mapped_column(default=0)
    conflicts_resolved: Mapped[int] = mapped_column(default=0)
    status: Mapped[str] = mapped_column(String(50), default="SUCCESS")
    
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class ConflictRecord(Base):
    """
    Tracks conflicts encountered during synchronization.
    """
    __tablename__ = "cloud_conflict_records"
    
    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_id: Mapped[str] = mapped_column(String(255), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(100), nullable=False)
    
    local_version: Mapped[int] = mapped_column(Integer, nullable=False)
    remote_version: Mapped[int] = mapped_column(Integer, nullable=False)
    
    resolution_strategy: Mapped[str] = mapped_column(String(50), nullable=False) # KEEP_LOCAL, ACCEPT_REMOTE, MANUAL_MERGE
    status: Mapped[str] = mapped_column(String(50), default="PENDING")
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class PlatformCloudAuditLog(Base):
    """
    Immutable audit trail for cloud operations (Sharing, Approvals, Admin changes).
    """
    __tablename__ = "cloud_platform_audit_logs"
    
    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid(as_uuid=True), nullable=True)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    
    action: Mapped[str] = mapped_column(String(255), nullable=False) # e.g. "SHARE_APPROVED", "WORKSPACE_CREATED"
    resource_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    details: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class CloudAnalytics(Base):
    """
    Pre-aggregated metrics for the Cloud Dashboard.
    """
    __tablename__ = "cloud_analytics_metrics"
    
    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    metric_name: Mapped[str] = mapped_column(String(100), index=True, nullable=False) # e.g., 'sharing_volume_24h', 'federation_health'
    metric_value: Mapped[float] = mapped_column(nullable=False)
    dimensions: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict) # e.g., {"tenant_id": "...", "node_id": "..."}
    
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
