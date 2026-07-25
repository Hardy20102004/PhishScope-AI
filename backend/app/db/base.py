# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base
from app.models.user import User
from app.models.investigation import Investigation
from app.models.threat_intel import Indicator, ThreatFeedResult, IndicatorCorrelation
from app.models.copilot import CopilotConversation, CopilotMessage, GeneratedReport
from app.models.case_management import Case, CaseTask, TimelineEvent, DecisionLog
from app.models.reporting import ReportTemplate, Report, ExportRecord, EvidenceManifest
from app.models.automation import Workflow, WorkflowVersion, WorkflowExecution
from app.models.extension import ExtensionDevice
from app.models.mobile import MobileDevice
from app.models.tenant import Organization, TenantSettings, License, AuditLog
from app.models.observability import Incident, SystemMetric
from app.models.ai_brain import (
    AIProviderConfig, AIModelEntry, AICapabilityMapping, AIPromptTemplate,
    AIMemoryStore, AIPolicyRule, AIAuditLogRecord, TokenUsageRecord
)
from app.models.multi_agent import (
    AgentDefinition, AgentTask, TaskExecutionHistory, AgentMessage,
    SharedMemoryItem, HumanApprovalRequest, AgentHealthMetric, AgentAuditLog
)
from app.models.ai_memory import MemoryItem, MemoryRelationship, MemoryAuditLog
from app.models.ai_context import ContextTemplate, ContextCacheEntry, ContextAuditLog, ContextPolicy
from app.models.prompt_platform import PromptTemplate, PromptVersion, PromptAnalyticsLog
from app.models.rag import KnowledgeAsset, DocumentChunk, RAGAnalyticsLog
from app.models.knowledge_graph import GraphEntity, GraphRelationship
from app.models.decision import DecisionRecord, DecisionEvidenceLink, ApprovalWorkflow
from app.models.xai import ExplanationRecord, EvidenceAttribution
from app.models.model_manager import AIProvider, AIModel, RoutingPolicy, ModelCostLog
