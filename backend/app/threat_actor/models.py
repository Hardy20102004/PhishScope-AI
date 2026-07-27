import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Uuid, JSON, Enum, Text, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.db.base_class import Base

class ThreatActorStatus(str, enum.Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    UNKNOWN = "Unknown"

class ThreatActor(Base):
    __tablename__ = "threat_actors"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    motivations: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    objectives: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    target_sectors: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    target_regions: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    
    first_observed: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    last_observed: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    status: Mapped[ThreatActorStatus] = mapped_column(Enum(ThreatActorStatus), default=ThreatActorStatus.UNKNOWN)
    confidence: Mapped[float] = mapped_column(Float, default=0.0) # Overall confidence in profile
    
    tenant_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    aliases: Mapped[List["ActorAlias"]] = relationship("ActorAlias", back_populates="actor", cascade="all, delete-orphan")
    campaigns: Mapped[List["ThreatActorCampaign"]] = relationship("ThreatActorCampaign", back_populates="actor")
    ttp_associations: Mapped[List["TTPAssociation"]] = relationship("TTPAssociation", back_populates="actor")
    infrastructure: Mapped[List["InfrastructureAssociation"]] = relationship("InfrastructureAssociation", back_populates="actor")
    malware: Mapped[List["MalwareAssociation"]] = relationship("MalwareAssociation", back_populates="actor")

class ActorAlias(Base):
    __tablename__ = "threat_actor_aliases"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    actor_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("threat_actors.id", ondelete="CASCADE"), index=True)
    alias_name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    source: Mapped[Optional[str]] = mapped_column(String(255), nullable=True) # E.g., CrowdStrike (assigns this alias)
    
    actor: Mapped["ThreatActor"] = relationship("ThreatActor", back_populates="aliases")

class ThreatActorCampaign(Base):
    __tablename__ = "threat_campaigns"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    actor_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid(as_uuid=True), ForeignKey("threat_actors.id", ondelete="SET NULL"), index=True)
    
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    target_sectors: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    target_regions: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    
    start_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    end_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    actor: Mapped[Optional["ThreatActor"]] = relationship("ThreatActor", back_populates="campaigns")

class TTPAssociation(Base):
    __tablename__ = "threat_actor_ttps"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    actor_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("threat_actors.id", ondelete="CASCADE"), index=True)
    
    # MITRE ATT&CK Mapping
    mitre_id: Mapped[str] = mapped_column(String(50), index=True, nullable=False) # e.g., T1548
    tactic: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    technique_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    actor: Mapped["ThreatActor"] = relationship("ThreatActor", back_populates="ttp_associations")

class InfrastructureAssociation(Base):
    __tablename__ = "threat_actor_infrastructure"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    actor_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("threat_actors.id", ondelete="CASCADE"), index=True)
    
    # Links to the IOC Correlation Engine's central Indicator table
    indicator_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("indicator.id", ondelete="CASCADE"), index=True)
    usage: Mapped[Optional[str]] = mapped_column(String(255), nullable=True) # C2, Phishing, Exploit Delivery
    
    actor: Mapped["ThreatActor"] = relationship("ThreatActor", back_populates="infrastructure")

class MalwareAssociation(Base):
    __tablename__ = "threat_actor_malware"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    actor_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("threat_actors.id", ondelete="CASCADE"), index=True)
    malware_family: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    role: Mapped[Optional[str]] = mapped_column(String(255), nullable=True) # Loader, Stealer, Ransomware
    
    actor: Mapped["ThreatActor"] = relationship("ThreatActor", back_populates="malware")

class AttributionEvidence(Base):
    """
    Separates Observed Facts from Analytical Inferences.
    """
    __tablename__ = "attribution_evidence"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    actor_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("threat_actors.id", ondelete="CASCADE"), index=True)
    
    # Could link to infrastructure, campaigns, or malware associations
    reference_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid(as_uuid=True), index=True, nullable=True)
    reference_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True) # 'Infrastructure', 'Campaign'
    
    is_observed_fact: Mapped[bool] = mapped_column(Boolean, default=True) # True = Fact, False = Inference
    description: Mapped[str] = mapped_column(Text, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, default=1.0)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
