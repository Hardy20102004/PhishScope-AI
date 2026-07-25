from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey, Enum, JSON, DateTime
from sqlalchemy.orm import relationship
import uuid
import enum
from datetime import datetime
from app.db.base_class import Base

class KnowledgeAssetStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    PROCESSING = "PROCESSING"
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"
    ERROR = "ERROR"

class KnowledgeAsset(Base):
    __tablename__ = "rag_knowledge_assets"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    source_type = Column(String, nullable=False) # e.g., PDF, URL, MD, POLICY
    source_uri = Column(String, nullable=True)
    tenant_id = Column(String, nullable=True)
    author = Column(String, nullable=True)
    status = Column(Enum(KnowledgeAssetStatus), default=KnowledgeAssetStatus.DRAFT)
    metadata_json = Column(JSON, default=dict)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    chunks = relationship("DocumentChunk", back_populates="asset", cascade="all, delete-orphan")

class DocumentChunk(Base):
    __tablename__ = "rag_document_chunks"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    asset_id = Column(String, ForeignKey("rag_knowledge_assets.id", ondelete="CASCADE"), nullable=False)
    
    chunk_index = Column(Integer, nullable=False)
    content = Column(String, nullable=False)
    
    # Store embedding as JSON for SQLite mock vector search
    vector_embedding = Column(JSON, nullable=True) 
    
    metadata_json = Column(JSON, default=dict) # E.g., page_number, section_title
    
    asset = relationship("KnowledgeAsset", back_populates="chunks")

class RAGAnalyticsLog(Base):
    __tablename__ = "rag_analytics_logs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    query_text = Column(String, nullable=False)
    user_id = Column(String, nullable=True)
    search_type = Column(String, nullable=False) # HYBRID, VECTOR, KEYWORD
    latency_ms = Column(Float, nullable=False)
    results_count = Column(Integer, nullable=False)
    success = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
