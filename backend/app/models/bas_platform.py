import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, JSON, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

class BasScenario(Base):
    __tablename__ = "mf_bas_scenarios"
    """
    Defines a reusable template for a simulated attack.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    tactic: Mapped[str] = mapped_column(String(100)) # e.g. Initial Access
    technique_id: Mapped[str] = mapped_column(String(50)) # e.g. T1566
    
    # JSON array defining the technical steps (e.g. payload drop, execute)
    execution_steps: Mapped[list] = mapped_column(JSON, default=list) 
    
    simulations = relationship("BasSimulation", back_populates="scenario", cascade="all, delete-orphan")


class BasSimulation(Base):
    __tablename__ = "mf_bas_simulations"
    """
    An executed instance of a BAS scenario.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    scenario_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mf_bas_scenarios.id", ondelete="CASCADE"), index=True)
    
    status: Mapped[str] = mapped_column(String(50)) # PENDING, RUNNING, COMPLETED, FAILED
    
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    
    overall_score: Mapped[float] = mapped_column(Float, default=0.0) # 0.0 to 100.0 readiness score
    
    scenario = relationship("BasScenario", back_populates="simulations")
    results = relationship("BasValidationResult", back_populates="simulation", cascade="all, delete-orphan")


class BasValidationResult(Base):
    __tablename__ = "mf_bas_validation_results"
    """
    The outcome of a specific simulation step against a security control.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    simulation_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mf_bas_simulations.id", ondelete="CASCADE"), index=True)
    
    step_name: Mapped[str] = mapped_column(String(255))
    expected_control: Mapped[str] = mapped_column(String(100)) # SIEM, EDR, NDR
    
    was_detected: Mapped[bool] = mapped_column(Boolean, default=False)
    was_blocked: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # E.g. the specific SIEM alert ID that caught it
    detection_reference: Mapped[str] = mapped_column(String(255), nullable=True)
    
    simulation = relationship("BasSimulation", back_populates="results")
