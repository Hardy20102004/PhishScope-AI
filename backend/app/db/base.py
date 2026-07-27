# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa: F401
from app.models.user import User  # noqa: F401
from app.models.investigation import Investigation  # noqa: F401
from app.models.threat_intel import Indicator, ThreatFeedResult, IndicatorCorrelation  # noqa: F401
from app.models.copilot import CopilotConversation, CopilotMessage, GeneratedReport  # noqa: F401
from app.models.case_management import Case, CaseTask, TimelineEvent, DecisionLog  # noqa: F401
from app.models.reporting import ReportTemplate, Report, ExportRecord, EvidenceManifest  # noqa: F401
from app.models.automation import Workflow, WorkflowVersion, WorkflowExecution  # noqa: F401
from app.models.extension import ExtensionDevice  # noqa: F401
from app.models.mobile import MobileDevice  # noqa: F401
from app.models.tenant import Organization, TenantSettings, License, AuditLog  # noqa: F401
from app.models.observability import Incident, SystemMetric  # noqa: F401
from app.models.ai_brain import (  # noqa: F401
    AIProviderConfig, AIModelEntry, AICapabilityMapping, AIPromptTemplate,
    AIMemoryStore, AIPolicyRule, AIAuditLogRecord, TokenUsageRecord
)
from app.models.multi_agent import (  # noqa: F401
    AgentDefinition, AgentTask, TaskExecutionHistory, AgentMessage,
    SharedMemoryItem, HumanApprovalRequest, AgentHealthMetric, AgentAuditLog
)
from app.models.ai_memory import MemoryItem, MemoryRelationship, MemoryAuditLog  # noqa: F401
from app.models.ai_context import ContextTemplate, ContextCacheEntry, ContextAuditLog, ContextPolicy  # noqa: F401
from app.models.prompt_platform import PromptTemplate, PromptVersion, PromptAnalyticsLog  # noqa: F401
from app.models.rag import KnowledgeAsset, DocumentChunk, RAGAnalyticsLog  # noqa: F401
from app.models.knowledge_graph import GraphEntity, GraphRelationship  # noqa: F401
from app.models.decision import DecisionRecord, DecisionEvidenceLink, ApprovalWorkflow  # noqa: F401
from app.models.xai import ExplanationRecord, EvidenceAttribution  # noqa: F401
from app.models.model_manager import AIProvider, AIModel, RoutingPolicy, ModelCostLog  # noqa: F401
from app.models.url_intelligence import (  # noqa: F401
    URLInvestigationDetails, ParsedURL, RedirectChain,
    DomainInfrastructure, CertificateData, BrandIntelligence
)
from app.models.website_investigation import (  # noqa: F401
    WebsiteInvestigation, PageSnapshot, JavaScriptMetadata,
    FormMetadata, SecurityHeaderData, VisualAnalysisData
)
from app.models.email_intelligence import (  # noqa: F401
    EmailInvestigation, EmailHeaderData, AuthenticationResult,
    RoutingHop, AttachmentMetadata, ExtractedURL, CampaignCorrelation
)
from app.models.qr_intelligence import (  # noqa: F401
    QRInvestigation, DecodedQRPayload, QRImageMetadata,
    VisualTamperingData, QRPaymentMetadata
)
from app.models.malware_intelligence import (  # noqa: F401
    MalwareInvestigation, MalwareMetadata, MalwareHashes,
    StaticAnalysisData, SignatureMatch, ExtractedIOC, ThreatCorrelation
)
from app.models.mobile_investigation import (  # noqa: F401
    MobileInvestigation, DeviceMetadata, MobileApplication,
    MobileCommunication, MobileLocation, MobileTimelineEvent, ExtractedMobileIOC
)
from app.models.browser_investigation import (  # noqa: F401
    BrowserInvestigation, BrowserHistoryRecord, BrowserCookie,
    BrowserExtension, BrowserDownload, BrowserTimelineEvent, ExtractedBrowserIOC
)
from app.models.network_investigation import (  # noqa: F401
    NetworkInvestigation, NetworkFlowRecord, DNSRecord,
    HTTPMetadata, TLSMetadata, NetworkTimelineEvent, ExtractedNetworkIOC
)
from app.models.cloud_investigation import (  # noqa: F401
    CloudInvestigation, CloudAsset, CloudIdentity,
    CloudConfiguration, CloudAuditEvent, CloudTimelineEvent, ExtractedCloudIOC
)
from app.ti_feed.models import (  # noqa: F401
    FeedRegistry, FeedVersion, FeedIndicator, FeedAuditLog
)
from app.threat_actor.models import (  # noqa: F401
    ThreatActor, ActorAlias, ThreatActorCampaign, TTPAssociation,
    InfrastructureAssociation, MalwareAssociation, AttributionEvidence
)
from app.campaign_engine.models import (  # noqa: F401
    Campaign as CampaignRegistry, CampaignInfrastructure, 
    CampaignVictim, CampaignTimeline, CampaignEvidence
)
from app.attack_graph.models import (  # noqa: F401
    GraphSnapshot, AttackPath, ImpactAnalysis
)
from app.reputation_engine.models import (  # noqa: F401
    ReputationProfile, ReputationHistory, ReputationEvidence
)
from app.cloud.models import (  # noqa: F401
    Tenant, Workspace, SharingPolicy, SharedIntelligenceObject, FederationSyncRecord
)
