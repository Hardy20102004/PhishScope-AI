import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, Uuid
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class InvestigationType(str, enum.Enum):
    URL = "URL"
    WEBSITE = "WEBSITE"
    DOMAIN = "DOMAIN"
    EMAIL = "EMAIL"
    MESSAGING = "MESSAGING"
    QR = "QR"
    FILE = "FILE"
    APK = "APK"

class InvestigationStatus(str, enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class Investigation(Base):
    __tablename__ = "investigations"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    target = Column(String, index=True, nullable=False)
    type = Column(SQLEnum(InvestigationType), nullable=False)
    status = Column(SQLEnum(InvestigationStatus), default=InvestigationStatus.PENDING, nullable=False)
    
    risk_score = Column(Integer, nullable=True) # 0-100
    risk_level = Column(String, nullable=True) # LOW, MEDIUM, HIGH, CRITICAL
    
    evidence = Column(JSON, default=dict)
    findings = Column(JSON, default=list)
    error_message = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    user_id = Column(Uuid(as_uuid=True), ForeignKey("users.id"), nullable=False)
    case_id = Column(Uuid(as_uuid=True), ForeignKey("cases.id", ondelete="SET NULL"), nullable=True, index=True)
    
    case = relationship("Case", back_populates="investigations")
