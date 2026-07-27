import enum
import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Enum, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class ForecastDomain(str, enum.Enum):
    INFRASTRUCTURE_REUSE = "INFRASTRUCTURE_REUSE"
    CAMPAIGN_EVOLUTION = "CAMPAIGN_EVOLUTION"
    THREAT_ACTOR_SHIFT = "THREAT_ACTOR_SHIFT"
    MALWARE_TREND = "MALWARE_TREND"
    INDUSTRY_TARGETING = "INDUSTRY_TARGETING"
    REGIONAL_TREND = "REGIONAL_TREND"

class ForecastStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    MATERIALIZED = "MATERIALIZED"
    DISPROVEN = "DISPROVEN"
    EXPIRED = "EXPIRED"

class ThreatForecast(Base):
    __tablename__ = "threat_forecasts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False, index=True)
    description = Column(String, nullable=False)
    domain = Column(Enum(ForecastDomain), nullable=False, index=True)
    status = Column(Enum(ForecastStatus), default=ForecastStatus.ACTIVE)
    
    tenant_id = Column(String, nullable=True, index=True)
    
    # Mathematical confidence bounded 0.0 - 1.0
    confidence_score = Column(Float, default=0.5)
    uncertainty_score = Column(Float, default=0.5) # Captures missing data gaps
    
    time_horizon_start = Column(DateTime, nullable=True)
    time_horizon_end = Column(DateTime, nullable=True)
    
    properties_json = Column(JSON, default=dict)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    scenarios = relationship("ForecastScenario", back_populates="forecast", cascade="all, delete-orphan")
    evidence = relationship("ForecastEvidence", back_populates="forecast", cascade="all, delete-orphan")


class ForecastScenario(Base):
    """Alternative outcomes for the parent forecast."""
    __tablename__ = "forecast_scenarios"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    forecast_id = Column(String, ForeignKey("threat_forecasts.id", ondelete="CASCADE"), nullable=False, index=True)
    
    scenario_name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    probability = Column(Float, default=0.0) # 0.0 - 1.0
    
    forecast = relationship("ThreatForecast", back_populates="scenarios")


class ForecastEvidence(Base):
    """Links the forecast to concrete entities in the Knowledge Graph or Timeline."""
    __tablename__ = "forecast_evidence"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    forecast_id = Column(String, ForeignKey("threat_forecasts.id", ondelete="CASCADE"), nullable=False, index=True)
    
    evidence_type = Column(String, nullable=False) # e.g., KNOWLEDGE_GRAPH_NODE, TIMELINE_EVENT
    reference_id = Column(String, nullable=False) # ID of the node or event
    explanation = Column(String, nullable=True) # Why this evidence supports the forecast
    
    forecast = relationship("ThreatForecast", back_populates="evidence")
