import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, String, Text, Uuid
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base


class AgentStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"
    DEPRECATED = "DEPRECATED"

class AgentHealth(str, enum.Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    UNREACHABLE = "UNREACHABLE"
    OFFLINE = "OFFLINE"

class TaskStatus(str, enum.Enum):
    PENDING = "PENDING"
    SCHEDULING = "SCHEDULING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    WAITING_FOR_APPROVAL = "WAITING_FOR_APPROVAL"
    CONFLICTED = "CONFLICTED"

class MessageType(str, enum.Enum):
    REQUEST = "REQUEST"
    RESPONSE = "RESPONSE"
    EVENT = "EVENT"
    BROADCAST = "BROADCAST"
    HANDOFF = "HANDOFF"

class MemoryTierExt(str, enum.Enum):
    WORKING = "WORKING"
    EVIDENCE = "EVIDENCE"
    CONVERSATION = "CONVERSATION"
    CASE = "CASE"
    ORGANIZATION = "ORGANIZATION"
    TEMPORARY = "TEMPORARY"
    PERSISTENT = "PERSISTENT"

class ApprovalStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    OVERRIDDEN = "OVERRIDDEN"

class AgentDefinition(Base):
    __tablename__ = "agent_definitions"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    agent_name: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    capabilities_json: Mapped[list] = mapped_column(JSON, default=list)
    supported_tasks_json: Mapped[list] = mapped_column(JSON, default=list)
    version: Mapped[str] = mapped_column(String, default="1.0.0", nullable=False)
    status: Mapped[AgentStatus] = mapped_column(SQLEnum(AgentStatus), default=AgentStatus.ACTIVE, nullable=False)
    health: Mapped[AgentHealth] = mapped_column(SQLEnum(AgentHealth), default=AgentHealth.HEALTHY, nullable=False)
    dependencies_json: Mapped[list] = mapped_column(JSON, default=list)
    owner: Mapped[str] = mapped_column(String, default="System", nullable=False)
    preferred_capability: Mapped[str] = mapped_column(String, nullable=True) # Maps to AI Security Brain Capability Registry
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class AgentTask(Base):
    __tablename__ = "agent_tasks"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    parent_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), nullable=True, index=True) # for task decomposition
    investigation_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), nullable=True, index=True)
    case_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), nullable=True, index=True)
    session_id: Mapped[str] = mapped_column(String, nullable=True, index=True)
    
    task_name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    assigned_agent_id: Mapped[str] = mapped_column(String, nullable=False, index=True) # uses agent_name as ID
    status: Mapped[TaskStatus] = mapped_column(SQLEnum(TaskStatus), default=TaskStatus.PENDING, nullable=False, index=True)
    
    input_payload_json: Mapped[dict] = mapped_column(JSON, default=dict)
    output_findings_json: Mapped[dict] = mapped_column(JSON, default=dict)
    dependency_task_ids_json: Mapped[list] = mapped_column(JSON, default=list)
    
    retry_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    confidence_score: Mapped[float] = mapped_column(Float, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    ended_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class TaskExecutionHistory(Base):
    __tablename__ = "task_execution_history"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    task_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("agent_tasks.id", ondelete="CASCADE"), nullable=False, index=True)
    agent_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    attempt_number: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    latency_ms: Mapped[int] = mapped_column(Integer, nullable=True)
    error_message: Mapped[str] = mapped_column(Text, nullable=True)
    fallback_path_taken: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class AgentMessage(Base):
    __tablename__ = "agent_messages"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    sender_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    receiver_id: Mapped[str] = mapped_column(String, nullable=True, index=True)
    message_type: Mapped[MessageType] = mapped_column(SQLEnum(MessageType), nullable=False, index=True)
    content_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    correlation_id: Mapped[str] = mapped_column(String, nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)


class SharedMemoryItem(Base):
    __tablename__ = "shared_memory_items"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    tier: Mapped[MemoryTierExt] = mapped_column(SQLEnum(MemoryTierExt), nullable=False, index=True)
    key: Mapped[str] = mapped_column(String, nullable=False, index=True)
    content_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    tenant_id: Mapped[str] = mapped_column(String, nullable=True, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class HumanApprovalRequest(Base):
    __tablename__ = "human_approval_requests"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    task_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("agent_tasks.id", ondelete="CASCADE"), nullable=False, index=True)
    requesting_agent_id: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    risk_severity: Mapped[str] = mapped_column(String, default="MODERATE", nullable=False) # LOW, MODERATE, HIGH, CRITICAL
    status: Mapped[ApprovalStatus] = mapped_column(SQLEnum(ApprovalStatus), default=ApprovalStatus.PENDING, nullable=False, index=True)
    reviewer_user_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), nullable=True)
    reviewer_feedback: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    resolved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)


class AgentHealthMetric(Base):
    __tablename__ = "agent_health_metrics"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    agent_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    metric_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    tasks_completed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    tasks_failed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    average_latency_ms: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    token_throughput: Mapped[int] = mapped_column(Integer, default=0, nullable=False)


class AgentAuditLog(Base):
    __tablename__ = "agent_audit_logs"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    agent_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    action_type: Mapped[str] = mapped_column(String, nullable=False, index=True) # TASK_START, TASK_COMPLETE, CONFLICT_DETECTED
    encrypted_payload: Mapped[str] = mapped_column(Text, nullable=False) # AES-256 GCM encrypted
    hmac_signature: Mapped[str] = mapped_column(String, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
