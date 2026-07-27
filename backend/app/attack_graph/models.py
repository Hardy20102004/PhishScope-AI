import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Uuid, JSON, Enum, Text, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.db.base_class import Base

class GraphSnapshot(Base):
    """
    Saves a specific layout and state of a generated Attack Graph for sharing/history.
    """
    __tablename__ = "attack_graph_snapshots"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Stores the JSON representation of nodes and links
    graph_data: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False) 
    
    tenant_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class AttackPath(Base):
    """
    Stores computed critical paths (e.g. Actor -> C2 -> Victim)
    """
    __tablename__ = "attack_graph_paths"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    
    source_entity_id: Mapped[str] = mapped_column(String(255), index=True, nullable=False) # Refers to KG Entity ID
    target_entity_id: Mapped[str] = mapped_column(String(255), index=True, nullable=False) # Refers to KG Entity ID
    
    # List of Entity IDs representing the path
    path_sequence: Mapped[List[str]] = mapped_column(JSON, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, default=1.0)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class ImpactAnalysis(Base):
    """
    Stores calculated centrality metrics for specific nodes.
    """
    __tablename__ = "attack_graph_impact"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_id: Mapped[str] = mapped_column(String(255), index=True, nullable=False) # Refers to KG Entity ID
    
    degree_centrality: Mapped[float] = mapped_column(Float, default=0.0)
    betweenness_centrality: Mapped[float] = mapped_column(Float, default=0.0)
    blast_radius: Mapped[int] = mapped_column(Integer, default=0) # Number of reachable nodes within 3 hops
    
    computed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
