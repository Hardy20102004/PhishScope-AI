import uuid

from sqlalchemy import (
    Boolean,
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
    Uuid,
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class QRInvestigation(Base):
    __tablename__ = "qr_investigations"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    investigation_id = Column(Uuid(as_uuid=True), ForeignKey("investigations.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    
    file_name = Column(String, index=True)
    
    # Relationships
    decoded_payload = relationship("DecodedQRPayload", back_populates="qr_investigation", uselist=False, cascade="all, delete-orphan")
    image_metadata = relationship("QRImageMetadata", back_populates="qr_investigation", uselist=False, cascade="all, delete-orphan")
    visual_tampering = relationship("VisualTamperingData", back_populates="qr_investigation", uselist=False, cascade="all, delete-orphan")
    payment_metadata = relationship("QRPaymentMetadata", back_populates="qr_investigation", uselist=False, cascade="all, delete-orphan")

class DecodedQRPayload(Base):
    __tablename__ = "decoded_qr_payloads"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    qr_investigation_id = Column(Uuid(as_uuid=True), ForeignKey("qr_investigations.id", ondelete="CASCADE"), nullable=False, unique=True)
    
    raw_payload = Column(String)
    payload_type = Column(String) # 'url', 'text', 'payment', 'wifi', etc.
    extracted_url = Column(String, nullable=True)
    
    qr_investigation = relationship("QRInvestigation", back_populates="decoded_payload")

class QRImageMetadata(Base):
    __tablename__ = "qr_image_metadata"
    
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    qr_investigation_id = Column(Uuid(as_uuid=True), ForeignKey("qr_investigations.id", ondelete="CASCADE"), nullable=False, unique=True)
    
    resolution = Column(String)
    file_size_bytes = Column(Integer)
    format = Column(String)
    contains_multiple_qrs = Column(Boolean, default=False)
    
    qr_investigation = relationship("QRInvestigation", back_populates="image_metadata")

class VisualTamperingData(Base):
    __tablename__ = "visual_tampering_data"
    
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    qr_investigation_id = Column(Uuid(as_uuid=True), ForeignKey("qr_investigations.id", ondelete="CASCADE"), nullable=False, unique=True)
    
    has_overlay_sticker = Column(Boolean, default=False)
    has_logo_anomaly = Column(Boolean, default=False)
    tampering_confidence = Column(Float)
    detected_brand = Column(String, nullable=True)
    
    qr_investigation = relationship("QRInvestigation", back_populates="visual_tampering")

class QRPaymentMetadata(Base):
    __tablename__ = "qr_payment_metadata"
    
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    qr_investigation_id = Column(Uuid(as_uuid=True), ForeignKey("qr_investigations.id", ondelete="CASCADE"), nullable=False, unique=True)
    
    payment_network = Column(String) # 'UPI', 'EMVCo', etc.
    merchant_id = Column(String)
    transaction_amount = Column(Float, nullable=True)
    currency = Column(String, nullable=True)
    is_dynamic = Column(Boolean, default=False)
    
    qr_investigation = relationship("QRInvestigation", back_populates="payment_metadata")
