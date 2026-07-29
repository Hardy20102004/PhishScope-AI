import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

class SimulationScenario(Base):
    __tablename__ = "dt_simulation_scenarios"
    """
    Defines the parameters of a 'what-if' scenario.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    
    # Parameters representing the 'what-if'
    alert_volume_multiplier: Mapped[float] = mapped_column(Float, default=1.0) # e.g. 1.2 = 20% increase
    analyst_headcount: Mapped[int] = mapped_column(Integer, default=10)
    automation_rate: Mapped[float] = mapped_column(Float, default=0.5) # e.g. 0.5 = 50% automated
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    results = relationship("SimulationResult", back_populates="scenario", cascade="all, delete-orphan")


class SimulationResult(Base):
    __tablename__ = "dt_simulation_results"
    """
    The forecasted output metrics for a given scenario.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    scenario_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("dt_simulation_scenarios.id", ondelete="CASCADE"), index=True)
    
    forecasted_mttr_mins: Mapped[float] = mapped_column(Float)
    forecasted_sla_breach_rate: Mapped[float] = mapped_column(Float)
    analyst_utilization_rate: Mapped[float] = mapped_column(Float)
    
    simulated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    scenario = relationship("SimulationScenario", back_populates="results")
    recommendations = relationship("OptimizationRecommendation", back_populates="result", cascade="all, delete-orphan")


class OptimizationRecommendation(Base):
    __tablename__ = "dt_optimization_recommendations"
    """
    AI-generated strategic recommendations to mitigate bottlenecks found in a simulation.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    result_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("dt_simulation_results.id", ondelete="CASCADE"), index=True)
    
    category: Mapped[str] = mapped_column(String(50)) # STAFFING, AUTOMATION, WORKFLOW
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    expected_impact: Mapped[str] = mapped_column(Text) # e.g., "Reduces MTTR by 15 mins"
    
    result = relationship("SimulationResult", back_populates="recommendations")
