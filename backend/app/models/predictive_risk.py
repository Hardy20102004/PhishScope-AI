"""
PHOENIX X — Phase X-094
Enterprise Predictive Cyber Risk, Executive Forecasting & Strategic Security Planning Platform
Database Models
"""
import enum
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from sqlalchemy import (
    Boolean, DateTime, Float, ForeignKey, Integer,
    String, Text, JSON, Enum
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base

# ─────────────────────────────────────────────────────────────────────────────
# Enumerations
# ─────────────────────────────────────────────────────────────────────────────

class ForecastInterval(str, enum.Enum):
    QUARTERLY = "QUARTERLY"
    ANNUAL = "ANNUAL"
    THREE_YEAR = "THREE_YEAR"

class PlanStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    PROPOSED = "PROPOSED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    IMPLEMENTED = "IMPLEMENTED"

class ApprovalGate(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    DENIED = "DENIED"

# ─────────────────────────────────────────────────────────────────────────────
# Forecasting & Risk Projections
# ─────────────────────────────────────────────────────────────────────────────

class RiskForecast(Base):
    """
    Represents forecasted risk trends across various enterprise domains.
    """
    __tablename__ = "predictive_risk_forecasts"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    domain: Mapped[str] = mapped_column(String(100), nullable=False) # e.g. "Cloud", "Identity", "AppSec"
    interval: Mapped[ForecastInterval] = mapped_column(Enum(ForecastInterval), nullable=False)
    
    current_risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    projected_risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    confidence_interval: Mapped[float] = mapped_column(Float, default=0.0)
    
    underlying_assumptions: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=list)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class StrategicPlan(Base):
    """
    Captures long-term security capability goals and maturity projections.
    """
    __tablename__ = "predictive_strategic_plans"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    
    target_maturity_level: Mapped[int] = mapped_column(Integer, default=1)
    status: Mapped[PlanStatus] = mapped_column(Enum(PlanStatus), default=PlanStatus.DRAFT)
    
    milestones: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

# ─────────────────────────────────────────────────────────────────────────────
# Investments & Governance
# ─────────────────────────────────────────────────────────────────────────────

class InvestmentScenario(Base):
    """
    Represents potential budget allocations and the forecasted ROI (risk reduction).
    """
    __tablename__ = "predictive_investment_scenarios"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    budget_estimate_usd: Mapped[float] = mapped_column(Float, default=0.0)
    
    forecasted_risk_reduction: Mapped[float] = mapped_column(Float, default=0.0) # Percentage reduction
    resource_allocations: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    
    analyzed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class ExecutiveDecision(Base):
    """
    Logs the executive approval gates for strategic security plans.
    """
    __tablename__ = "predictive_executive_decisions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    reference_id: Mapped[str] = mapped_column(String(255), nullable=False) # e.g. StrategicPlan ID or InvestmentScenario ID
    reference_type: Mapped[str] = mapped_column(String(50), nullable=False)
    
    decision: Mapped[ApprovalGate] = mapped_column(Enum(ApprovalGate), default=ApprovalGate.PENDING)
    justification: Mapped[str] = mapped_column(Text, nullable=True)
    
    approver_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    decided_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
