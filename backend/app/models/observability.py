import uuid
from datetime import datetime, timezone

from sqlalchemy import JSON, DateTime, Float, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    severity: Mapped[str] = mapped_column(String, nullable=False) # e.g., CRITICAL, HIGH, WARNING, INFO
    status: Mapped[str] = mapped_column(String, nullable=False, default="OPEN") # OPEN, RESOLVED
    
    component: Mapped[str] = mapped_column(String, nullable=False) # e.g., 'API', 'DATABASE', 'THREAT_FEED'
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    resolved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

class SystemMetric(Base):
    __tablename__ = "system_metrics"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    metric_name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(String, nullable=False) # e.g., 'ms', 'bytes', 'count'
    
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    tags_json: Mapped[dict] = mapped_column(JSON, default=dict)
