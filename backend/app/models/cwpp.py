import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, JSON, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base

class CloudWorkload(Base):
    __tablename__ = "mf_cwpp_workloads"
    """
    Represents a specific runtime instance.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    workload_type: Mapped[str] = mapped_column(String(50)) # VM, CONTAINER, SERVERLESS, POD
    workload_name: Mapped[str] = mapped_column(String(255))
    provider: Mapped[str] = mapped_column(String(50))
    region: Mapped[str] = mapped_column(String(100))
    
    status: Mapped[str] = mapped_column(String(50), default="RUNNING") # RUNNING, STOPPED, TERMINATED
    criticality: Mapped[str] = mapped_column(String(50), default="MEDIUM")
    
    discovered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class RuntimeEvent(Base):
    __tablename__ = "mf_cwpp_runtime_events"
    """
    Represents an observed action on the workload.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    workload_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mf_cwpp_workloads.id", ondelete="CASCADE"), index=True)
    
    event_type: Mapped[str] = mapped_column(String(100)) # PROCESS_START, NETWORK_CONN, FILE_MOD
    process_name: Mapped[str] = mapped_column(String(255), nullable=True)
    command_line: Mapped[str] = mapped_column(Text, nullable=True)
    destination_ip: Mapped[str] = mapped_column(String(100), nullable=True)
    
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class BehaviorAnomaly(Base):
    __tablename__ = "mf_cwpp_anomalies"
    """
    An identified deviation from the baseline behavior.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    workload_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mf_cwpp_workloads.id", ondelete="CASCADE"), index=True)
    event_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mf_cwpp_runtime_events.id", ondelete="CASCADE"), nullable=True)
    
    title: Mapped[str] = mapped_column(String(255))
    severity: Mapped[str] = mapped_column(String(50)) # CRITICAL, HIGH, MEDIUM, LOW
    description: Mapped[str] = mapped_column(Text)
    
    detected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class WorkloadRiskScore(Base):
    __tablename__ = "mf_cwpp_risk_scores"
    """
    The calculated risk of the workload based on its runtime anomalies and criticality.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    workload_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mf_cwpp_workloads.id", ondelete="CASCADE"), index=True, unique=True)
    
    risk_score: Mapped[float] = mapped_column(Float, default=0.0) # 0.0 to 100.0
    
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
