import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, Uuid, Boolean, Float
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class OSComponentStatus(str, enum.Enum):
    ONLINE = "ONLINE"
    DEGRADED = "DEGRADED"
    OFFLINE = "OFFLINE"
    MAINTENANCE = "MAINTENANCE"

class PlatformRegistryEntry(Base):
    __tablename__ = "cyberos_platform_registry"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    module_name = Column(String, index=True, nullable=False) # e.g., "SOC", "DFIR", "CyberGovernance"
    version = Column(String, nullable=False)
    api_endpoint_prefix = Column(String, nullable=False)
    
    status = Column(SQLEnum(OSComponentStatus), default=OSComponentStatus.ONLINE)
    capabilities = Column(JSON, default=list) # e.g., ["threat_intel", "identity"]
    
    registered_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    last_heartbeat = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class UnifiedObservabilityMetric(Base):
    __tablename__ = "cyberos_observability"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    metric_type = Column(String, index=True, nullable=False) # API_LATENCY, CPU_USAGE, MEMORY, DB_POOL
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=False) # ms, %, bytes
    
    source_module = Column(String, nullable=False) # CyberOS, SOC, etc.
    
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

class GlobalSystemLog(Base):
    __tablename__ = "cyberos_global_log"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    severity = Column(String, index=True, nullable=False) # INFO, WARNING, ERROR, CRITICAL
    source_module = Column(String, index=True, nullable=False)
    
    message = Column(String, nullable=False)
    context_data = Column(JSON, default=dict)
    
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
