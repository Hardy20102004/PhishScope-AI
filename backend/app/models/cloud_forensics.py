import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

class CloudEnvironment(Base):
    __tablename__ = "mf_cloud_environments"
    """
    Metadata tracking the ingested cloud context (AWS Account, K8s Cluster, etc).
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    investigation_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("investigations.id", ondelete="CASCADE"), index=True, nullable=True)
    
    provider: Mapped[str] = mapped_column(String(50)) # AWS, GCP, Azure, K8s
    account_id: Mapped[str] = mapped_column(String(100), nullable=True)
    region: Mapped[str] = mapped_column(String(50), nullable=True)
    
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    audit_logs = relationship("CloudAuditLog", back_populates="environment", cascade="all, delete-orphan")
    containers = relationship("ContainerMetadata", back_populates="environment", cascade="all, delete-orphan")
    kubernetes_pods = relationship("KubernetesPod", back_populates="environment", cascade="all, delete-orphan")


class CloudAuditLog(Base):
    __tablename__ = "mf_cloud_audit_logs"
    """
    Parsed administrative/identity events (e.g. AWS CloudTrail).
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    env_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mf_cloud_environments.id", ondelete="CASCADE"), index=True)
    
    event_name: Mapped[str] = mapped_column(String(100), index=True)
    event_source: Mapped[str] = mapped_column(String(100)) # e.g. s3.amazonaws.com
    actor_identity: Mapped[str] = mapped_column(String(255)) # IAM Role or User
    source_ip: Mapped[str] = mapped_column(String(50))
    
    is_anomalous: Mapped[bool] = mapped_column(Boolean, default=False)
    anomaly_reason: Mapped[str] = mapped_column(Text, nullable=True)
    
    raw_event: Mapped[dict] = mapped_column(JSON)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    
    environment = relationship("CloudEnvironment", back_populates="audit_logs")


class ContainerMetadata(Base):
    __tablename__ = "mf_container_metadata"
    """
    Configuration state of a Docker/Containerd workload.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    env_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mf_cloud_environments.id", ondelete="CASCADE"), index=True)
    
    container_id: Mapped[str] = mapped_column(String(100), index=True)
    image_name: Mapped[str] = mapped_column(String(255))
    
    is_privileged: Mapped[bool] = mapped_column(Boolean, default=False)
    mounts_host_root: Mapped[bool] = mapped_column(Boolean, default=False)
    mounts_docker_sock: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # JSON containing env vars, cmd, etc.
    config_dump: Mapped[dict] = mapped_column(JSON)
    
    is_compromised: Mapped[bool] = mapped_column(Boolean, default=False)
    
    environment = relationship("CloudEnvironment", back_populates="containers")


class KubernetesPod(Base):
    __tablename__ = "mf_kubernetes_pods"
    """
    Configuration state of a K8s Pod.
    """
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    env_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("mf_cloud_environments.id", ondelete="CASCADE"), index=True)
    
    namespace: Mapped[str] = mapped_column(String(100))
    pod_name: Mapped[str] = mapped_column(String(255))
    service_account: Mapped[str] = mapped_column(String(255))
    
    host_network: Mapped[bool] = mapped_column(Boolean, default=False)
    host_pid: Mapped[bool] = mapped_column(Boolean, default=False)
    
    raw_manifest: Mapped[dict] = mapped_column(JSON)
    
    environment = relationship("CloudEnvironment", back_populates="kubernetes_pods")
