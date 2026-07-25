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
from app.models.url_intelligence import (
    URLInvestigationDetails, ParsedURL, RedirectChain,
    DomainInfrastructure, CertificateData, BrandIntelligence
)
from app.models.website_investigation import (
    WebsiteInvestigation, PageSnapshot, JavaScriptMetadata,
    FormMetadata, SecurityHeaderData, VisualAnalysisData
)
from app.models.email_intelligence import (
    EmailInvestigation, EmailHeaderData, AuthenticationResult,
    RoutingHop, AttachmentMetadata, ExtractedURL, CampaignCorrelation
)
from app.models.qr_intelligence import (
    QRInvestigation, DecodedQRPayload, QRImageMetadata,
    VisualTamperingData, QRPaymentMetadata
)
from app.models.malware_intelligence import (
    MalwareInvestigation, MalwareMetadata, MalwareHashes,
    StaticAnalysisData, SignatureMatch, ExtractedIOC, ThreatCorrelation
)
from app.models.mobile_investigation import (
    MobileInvestigation, DeviceMetadata, MobileApplication,
    MobileCommunication, MobileLocation, MobileTimelineEvent, ExtractedMobileIOC
)
from app.models.browser_investigation import (
    BrowserInvestigation, BrowserHistoryRecord, BrowserCookie,
    BrowserExtension, BrowserDownload, BrowserTimelineEvent, ExtractedBrowserIOC
)
from app.models.network_investigation import (
    NetworkInvestigation, NetworkFlowRecord, DNSRecord,
    HTTPMetadata, TLSMetadata, NetworkTimelineEvent, ExtractedNetworkIOC
)
from app.models.cloud_investigation import (
    CloudInvestigation, CloudAsset, CloudIdentity,
    CloudConfiguration, CloudAuditEvent, CloudTimelineEvent, ExtractedCloudIOC
)
