import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, JSON, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

class ReadinessSnapshot(Base):
    __tablename__ = "mf_bt_readiness_snapshots"
    """
    A daily or weekly snapshot of the overall Blue Team maturity score.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    overall_maturity_score: Mapped[float] = mapped_column(Float, default=0.0)
    detection_health_score: Mapped[float] = mapped_column(Float, default=0.0)
    analyst_readiness_score: Mapped[float] = mapped_column(Float, default=0.0)
    
    # Store aggregated JSON metrics to avoid historical table joins
    aggregated_metrics: Mapped[dict] = mapped_column(JSON, default=dict)


class DetectionMetric(Base):
    __tablename__ = "mf_bt_detection_metrics"
    """
    Tracks the performance of specific SIEM/EDR rules.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    rule_name: Mapped[str] = mapped_column(String(255))
    rule_id: Mapped[str] = mapped_column(String(100), index=True)
    data_source: Mapped[str] = mapped_column(String(100)) # e.g. CrowdStrike, Splunk
    
    total_alerts: Mapped[int] = mapped_column(Integer, default=0)
    false_positives: Mapped[int] = mapped_column(Integer, default=0)
    true_positives: Mapped[int] = mapped_column(Integer, default=0)
    
    status: Mapped[str] = mapped_column(String(50), default="HEALTHY") # HEALTHY, NOISY, BROKEN
    
    last_evaluated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class AnalystTeamMetric(Base):
    __tablename__ = "mf_bt_analyst_metrics"
    """
    Aggregated performance data for SOC tiers.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    team_name: Mapped[str] = mapped_column(String(100)) # Tier 1, Tier 2, DFIR
    evaluation_period: Mapped[str] = mapped_column(String(50)) # e.g. "2026-W30"
    
    mean_time_to_triage_mins: Mapped[float] = mapped_column(Float, default=0.0)
    mean_time_to_resolve_mins: Mapped[float] = mapped_column(Float, default=0.0)
    playbook_adherence_percent: Mapped[float] = mapped_column(Float, default=0.0)
