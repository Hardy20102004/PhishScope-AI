# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa: F401
from app.models.user import User  # noqa: F401
from app.models.investigation import Investigation  # noqa: F401
from app.models.threat_intel import Indicator, ThreatFeedResult, IndicatorCorrelation  # noqa: F401
from app.models.alert_management import Alert, AlertEvidence, AlertCorrelationGroup, AlertAssignment, AlertLifecycleEvent  # noqa: F401
from app.models.detection import DetectionRule, DetectionRuleVersion, RuleTestResult, RuleApprovalRecord  # noqa: F401
from app.models.ai_triage import AITriageGroup, AlertRecommendation, AnalystFeedback, AssetBusinessContext  # noqa: F401
from app.models.threat_hunting import HuntSession, HuntQuery, HuntHypothesis, HuntEvidence  # noqa: F401
from app.models.incident_response import Incident, DFIRCase, EvidenceRecord, ChainOfCustodyLog, IncidentTask  # noqa: F401
from app.models.soar import Playbook, ExecutionHistory, ApprovalRecord  # noqa: F401
from app.models.collaboration import CollabWorkspace, ChatMessage, AnalystNote, AnalystPresence  # noqa: F401
from app.models.executive import ExecutiveMetric, BusinessRiskScore, ExecutiveReport  # noqa: F401
from app.models.soc_copilot import CopilotSession, CopilotChatMessage, CopilotReasoningLog  # noqa: F401
from app.models.digital_twin import SimulationScenario, TwinAssetNode, AttackPathGraph, ResilienceMetric  # noqa: F401
from app.models.disk_forensics import DiskImage, DiskPartition, ForensicArtifact  # noqa: F401
from app.models.memory_forensics import MemoryImage, MemoryProcess, MemoryNetworkConnection  # noqa: F401
from app.models.mobile_forensics import ForensicMobileDevice, ForensicMobileCommunication, ForensicMobileLocation  # noqa: F401
from app.models.browser_forensics import BrowserProfile, BrowserHistory, ForensicBrowserExtension  # noqa: F401
from app.models.email_forensics import Mailbox, EmailMessage, EmailHeader  # noqa: F401
from app.models.malware_analysis import MalwareSample, StaticAnalysis, MalwareString, YaraMatch, MalwareCapability  # noqa: F401
from app.models.cloud_forensics import CloudEnvironment, CloudAuditLog, ContainerMetadata, KubernetesPod  # noqa: F401
from app.models.unified_timeline import UnifiedInvestigation, UnifiedTimelineEvent, EvidenceCorrelation  # noqa: F401
from app.models.reporting_engine import EvidenceItem, ChainOfCustodyRecord, ForensicReport, ReportSection  # noqa: F401
from app.models.bas_platform import BasScenario, BasSimulation, BasValidationResult  # noqa: F401
from app.models.red_team import RedTeamCampaign, AuthorizationRecord, CampaignFinding  # noqa: F401
from app.models.blue_team import ReadinessSnapshot, DetectionMetric, AnalystTeamMetric  # noqa: F401
from app.models.continuous_validation import SecurityPostureSnapshot, SecurityDriftRecord, CVOptimizationRecommendation  # noqa: F401
from app.models.attack_path import AssetNode, AssetRelationship, SimulatedAttackPath  # noqa: F401
from app.models.detection_gap import MitreCoverageMetric, DetectionGapRecord, ControlOptimizationPlan  # noqa: F401
from app.models.cyber_resilience import BusinessServiceNode, RecoveryObjective, DisasterRecoveryTest, ResilienceAssessment  # noqa: F401
from app.models.executive_intelligence import GovernanceMetric, BusinessImpactIndicator, InvestmentROI, DecisionSupportBrief  # noqa: F401
from app.models.strategic_defense import StrategicForecast, OptimizationRoadmap, StrategicRecommendation, DecisionApprovalLog  # noqa: F401
from app.models.cspm import CSPMCloudAsset, CloudMisconfiguration, ComplianceFinding  # noqa: F401
from app.models.cwpp import CloudWorkload, RuntimeEvent, BehaviorAnomaly, WorkloadRiskScore  # noqa: F401
from app.models.k8s_security import K8sCluster, K8sRBACPolicy, K8sRiskScore  # noqa: F401
from app.models.ciem import CIEMCloudIdentity, CloudEntitlement, CiemIdentityRiskScore, AccessReview  # noqa: F401
from app.models.cdr import CloudTelemetryEvent, CloudDetection, CDRCloudInvestigation, ResponseAction  # noqa: F401
from app.models.dspm import CloudDataAsset, DataClassification, DataExposureFinding, DataAccessGovernance  # noqa: F401
from app.models.multi_cloud import UnifiedCloudAsset, CrossCloudRelationship, UnifiedRiskScore, ComplianceTrend  # noqa: F401
from app.models.governance import SecurityPolicy, GovernanceWorkflow, GovernanceApprovalRecord, AutomationLog  # noqa: F401
from app.models.ctem import AttackSurfaceNode, BusinessContextBoundary, CloudExposureFinding, RemediationPlan  # noqa: F401
from app.models.case_management import Case, CaseTask, TimelineEvent, DecisionLog  # noqa: F401
from app.models.reporting import ReportTemplate, Report, ExportRecord, EvidenceManifest  # noqa: F401
from app.models.automation import Workflow, WorkflowVersion, WorkflowExecution  # noqa: F401
from app.models.extension import ExtensionDevice  # noqa: F401
from app.models.mobile import MobileDevice  # noqa: F401
from app.models.tenant import Organization, TenantSettings, License, AuditLog  # noqa: F401
from app.models.observability import ObservabilityIncident, SystemMetric  # noqa: F401
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
from app.models.aspm import EnterpriseApplication, CodeRepository, ApplicationDependency, SecurityFinding, ApplicationRisk, ASPMAuditLog  # noqa: F401
from app.models.devsecops import PipelineRun, SecurityGate, SDLCWorkflow, DeveloperMetric, DevSecOpsAuditLog  # noqa: F401
from app.models.sbom import SBOMRecord, SoftwareArtifact, SoftwareDependency, ProvenanceMetadata, SupplyChainRiskScore, SBOMAuditLog  # noqa: F401
from app.models.sast import SASTScan, SASTRule, SASTFinding, SASTGuidance, SASTAuditLog  # noqa: F401
from app.models.dast import DASTTarget, DASTScan, DASTFinding, DASTGuidance, DASTAuditLog  # noqa: F401
from app.models.sca import SCADependency, SCAPackageIntelligence, SCALicense, SCARiskScore, SCAGuidance, SCAAuditLog  # noqa: F401
from app.models.secrets import SecretMetadata, SecretExposure, SecretPolicy, SecretGuidance, SecretsAuditLog  # noqa: F401
from app.models.iac import IaCTemplate, IaCConfigurationFinding, IaCPolicy, IaCDeploymentGovernance, IaCGuidance, IaCAuditLog  # noqa: F401
from app.models.copilot import DeveloperCopilotSession, CodeReviewRecord, CodeReviewFinding, DeveloperLearningProgress, EngineeringMetric, CopilotConversation, CopilotMessage, GeneratedReport  # noqa: F401
from app.models.appsec_command_center import AppSecExecutiveMetric, EngineeringProductivityMetric, AppSecConsolidatedFinding, AppSecGovernanceDecision  # noqa: F401
from app.models.data_fabric import MetadataNode, LineageEdge, QualityMetric  # noqa: F401
from app.models.knowledge_evolution import OntologyNode, SchemaRecommendation, EvolutionQualityMetric  # noqa: F401
from app.models.cyber_governance import CyberGovernanceKPI, GovernancePolicy, RiskOversightMetric, BoardReportSummary  # noqa: F401
from app.models.cyber_command import EnterpriseHealthMetric, StrategicPlan, ExecutiveCopilotSummary  # noqa: F401
from app.models.cyber_os import PlatformRegistryEntry, UnifiedObservabilityMetric, GlobalSystemLog  # noqa: F401
from app.models.orchestration import WorkflowRecord, TaskAssignment, PlaybookDefinition, OrchestrationDecisionLog  # noqa: F401
from app.models.ispm import ISPMProviderRegistry, EnterpriseIdentity, IdentityRiskScore  # noqa: F401
from app.models.predictive_risk import RiskForecast, StrategicPlan as PredictiveStrategicPlan, InvestmentScenario, ExecutiveDecision  # noqa: F401
from app.models.cyber_fusion import FusionRecord, CrossDomainRiskScore, StrategicRecommendation  # noqa: F401
