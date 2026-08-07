import uuid
from datetime import datetime, timezone

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base


class MobileDevice(Base):
    __tablename__ = "mobile_devices"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    
    device_id: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    platform: Mapped[str] = mapped_column(String, nullable=False) # iOS, Android
    os_version: Mapped[str] = mapped_column(String, nullable=True)
    push_token: Mapped[str] = mapped_column(String, nullable=True)
    
    is_biometric_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_compliant: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False) # For MDM checks
    
    sync_state_json: Mapped[dict] = mapped_column(JSON, default=dict)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    last_sync_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
