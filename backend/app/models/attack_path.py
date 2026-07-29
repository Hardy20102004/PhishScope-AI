import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, JSON, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

class AssetNode(Base):
    __tablename__ = "mf_ap_nodes"
    """
    Represents an entity in the enterprise graph (Endpoint, User, Cloud Role).
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    node_type: Mapped[str] = mapped_column(String(50), index=True) # USER, ENDPOINT, SERVER, CLOUD_ROLE
    name: Mapped[str] = mapped_column(String(255))
    is_critical: Mapped[bool] = mapped_column(Boolean, default=False)
    
    properties: Mapped[dict] = mapped_column(JSON, default=dict)
    
    # Relationships mapping (for simplified SQL adjacency list)
    outgoing_edges = relationship("AssetRelationship", foreign_keys="AssetRelationship.source_node_id", back_populates="source_node", cascade="all, delete-orphan")
    incoming_edges = relationship("AssetRelationship", foreign_keys="AssetRelationship.target_node_id", back_populates="target_node", cascade="all, delete-orphan")


class AssetRelationship(Base):
    __tablename__ = "mf_ap_edges"
    """
    Represents the directed edge between two AssetNodes.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    source_node_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mf_ap_nodes.id", ondelete="CASCADE"), index=True)
    target_node_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mf_ap_nodes.id", ondelete="CASCADE"), index=True)
    
    relationship_type: Mapped[str] = mapped_column(String(100)) # HAS_SESSION, CAN_RDP, ASSUME_ROLE
    
    source_node = relationship("AssetNode", foreign_keys=[source_node_id], back_populates="outgoing_edges")
    target_node = relationship("AssetNode", foreign_keys=[target_node_id], back_populates="incoming_edges")


class SimulatedAttackPath(Base):
    __tablename__ = "mf_ap_simulated_paths"
    """
    A recorded sequence of nodes representing a viable route an attacker could take.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    start_node_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mf_ap_nodes.id", ondelete="CASCADE"))
    target_node_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mf_ap_nodes.id", ondelete="CASCADE"))
    
    # Ordered array of node IDs representing the path
    path_sequence: Mapped[list] = mapped_column(JSON, default=list)
    path_complexity: Mapped[int] = mapped_column(Integer) # Number of hops
    
    discovered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
