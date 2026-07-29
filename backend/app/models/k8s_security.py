import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, JSON, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base

class K8sCluster(Base):
    __tablename__ = "mf_k8s_clusters"
    """
    Inventory of discovered Kubernetes clusters.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    cluster_name: Mapped[str] = mapped_column(String(255))
    provider: Mapped[str] = mapped_column(String(50)) # EKS, AKS, GKE, SELF_MANAGED
    version: Mapped[str] = mapped_column(String(50))
    region: Mapped[str] = mapped_column(String(100))
    
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE")
    
    discovered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class K8sRBACPolicy(Base):
    __tablename__ = "mf_k8s_rbac_policies"
    """
    Represents Service Accounts and their effective permissions.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    cluster_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mf_k8s_clusters.id", ondelete="CASCADE"), index=True)
    
    subject_name: Mapped[str] = mapped_column(String(255))
    subject_type: Mapped[str] = mapped_column(String(50)) # User, Group, ServiceAccount
    namespace: Mapped[str] = mapped_column(String(100), nullable=True)
    
    effective_permissions: Mapped[dict] = mapped_column(JSON) # e.g. {"verbs": ["*"], "resources": ["secrets"]}
    is_overprivileged: Mapped[bool] = mapped_column(Boolean, default=False)
    
    analyzed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class K8sRiskScore(Base):
    __tablename__ = "mf_k8s_risk_scores"
    """
    Aggregated risk score of a cluster.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    
    cluster_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mf_k8s_clusters.id", ondelete="CASCADE"), index=True, unique=True)
    
    risk_score: Mapped[float] = mapped_column(Float, default=0.0) # 0.0 to 100.0
    rbac_issues_count: Mapped[int] = mapped_column(Integer, default=0)
    admission_issues_count: Mapped[int] = mapped_column(Integer, default=0)
    
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
