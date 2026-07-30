import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, Uuid, Boolean, Float
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class CommandStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    DEGRADED = "DEGRADED"
    CRITICAL = "CRITICAL"
    OFFLINE = "OFFLINE"

class EnterpriseHealthMetric(Base):
    __tablename__ = "command_enterprise_health"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    domain = Column(String, index=True, nullable=False) # e.g., SOC, AppSec, Cloud
    health_score = Column(Float, nullable=False)
    status = Column(SQLEnum(CommandStatus), default=CommandStatus.ACTIVE)
    details = Column(JSON, default=dict)
    
    evaluated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class StrategicPlan(Base):
    __tablename__ = "command_strategic_plan"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    horizon = Column(String, nullable=False) # e.g., 5-Year
    
    milestones = Column(JSON, default=list)
    budget_allocation = Column(Float, nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class ExecutiveCopilotSummary(Base):
    __tablename__ = "command_copilot_summary"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    context_window = Column(String, nullable=False) # e.g., "Weekly Review"
    
    observed_evidence = Column(JSON, default=dict)
    calculated_metrics = Column(JSON, default=dict)
    strategic_recommendations = Column(JSON, default=list)
    
    generated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
