import { createBrowserRouter, Navigate } from "react-router-dom";
import { AuthGuard } from "@/guards/AuthGuard";
import { AuthLayout } from "@/layouts/AuthLayout";
import { DashboardLayout } from "@/layouts/DashboardLayout";
import AdminLayout from '@/pages/admin/AdminLayout';
import Login from "@/pages/auth/Login";
import Register from "@/pages/auth/Register";
import { MemoryDashboard } from '@/features/ai-memory/pages/MemoryDashboard';
import { ContextDashboard } from '@/features/ai-context/pages/ContextDashboard';
import { PromptDashboard } from '@/features/prompt-platform/pages/PromptDashboard';
import { PromptEditor } from '@/features/prompt-platform/pages/PromptEditor';
import { KnowledgeDashboard } from '@/features/rag/pages/KnowledgeDashboard';
import { DocumentExplorer } from '@/features/rag/pages/DocumentExplorer';
import { SearchInterface } from '@/features/rag/pages/SearchInterface';
import { GraphDashboard } from '@/features/knowledge-graph/pages/GraphDashboard';
import { EntityExplorer } from '@/features/knowledge-graph/pages/EntityExplorer';
import { RelationshipViewer } from '@/features/knowledge-graph/pages/RelationshipViewer';
import { DecisionDashboard } from '@/features/decision/pages/DecisionDashboard';
import { ApprovalCenter } from '@/features/decision/pages/ApprovalCenter';
import { ReasoningViewer } from '@/features/decision/components/ReasoningViewer';
import { XAIDashboard } from '@/features/xai/pages/XAIDashboard';
import { EvidenceTrace } from '@/features/xai/components/EvidenceTrace';
import { ModelDashboard } from '@/features/model-manager/pages/ModelDashboard';
import { ProviderRegistry } from '@/features/model-manager/pages/ProviderRegistry';
import { RoutingPolicies } from '@/features/model-manager/pages/RoutingPolicies';
import { Dashboard } from "@/pages/Dashboard";
import NewInvestigation from "@/pages/investigations/NewInvestigation";
import { Workspace } from "@/pages/investigations/Workspace";
import { ThreatIntelDashboard } from "@/pages/threat-intel/Dashboard";
import { IndicatorSearch } from "@/pages/threat-intel/IndicatorSearch";
import { CaseList } from "@/pages/cases/CaseList";
import { CaseWorkspace } from "@/pages/cases/CaseWorkspace";
import { WorkflowDashboard } from '@/features/automation/components/WorkflowDashboard';
import { WorkflowBuilder } from '@/features/automation/components/WorkflowBuilder';
import TenantDashboard from '@/pages/admin/TenantDashboard';
import UserManagement from '@/pages/admin/UserManagement';
import SecurityPolicies from '@/pages/admin/SecurityPolicies';
import AuditLogs from '@/pages/admin/AuditLogs';
import SystemHealth from '@/pages/admin/observability/SystemHealth';
import IncidentManager from '@/pages/admin/observability/IncidentManager';
import MetricsExplorer from '@/pages/admin/observability/MetricsExplorer';
import AIBrainDashboard from "@/pages/ai-brain/AIBrainDashboard";
import ProviderModelManager from "@/pages/ai-brain/ProviderModelManager";
import PromptCapabilityLibrary from "@/pages/ai-brain/PromptCapabilityLibrary";
import ConversationMemoryExplorer from "@/pages/ai-brain/ConversationMemoryExplorer";
import AIObservabilityAudit from "@/pages/ai-brain/AIObservabilityAudit";

// Multi-Agent Framework
import { AIWorkforceDashboard } from "@/features/multi-agent/pages/AIWorkforceDashboard";

// URL Intelligence
import URLInvestigationDashboard from "@/features/url-intelligence/components/URLInvestigationDashboard";

// Website Investigation
import WebsiteInvestigationDashboard from "@/features/website-investigation/components/WebsiteInvestigationDashboard";

// Email Intelligence
import EmailInvestigationDashboard from "@/features/email-intelligence/components/EmailInvestigationDashboard";

// QR Intelligence
import QRInvestigationDashboard from "@/features/qr-intelligence/components/QRInvestigationDashboard";

// Malware Intelligence
import MalwareInvestigationDashboard from "@/features/malware-intelligence/components/MalwareInvestigationDashboard";

// Mobile Device Investigation
import MobileInvestigationDashboard from "@/features/mobile-investigation/components/MobileInvestigationDashboard";

// Browser Investigation
import BrowserInvestigationDashboard from "@/features/browser-investigation/components/BrowserInvestigationDashboard";

// Network Investigation
import NetworkInvestigationDashboard from "@/features/network-investigation/components/NetworkInvestigationDashboard";

// Cloud Investigation
import CloudInvestigationDashboard from "@/features/cloud-investigation/components/CloudInvestigationDashboard";

// CTEM
import { CTEMDashboard } from "@/features/ctem/pages/CTEMDashboard";

// Command Center
import { CommandCenterDashboard } from "@/features/command-center/pages/CommandCenterDashboard";

// ASPM
import ASPMDashboard from "@/pages/aspm/ASPMDashboard";
import ApplicationInventory from "@/pages/aspm/ApplicationInventory";
import RepositoryDashboard from "@/pages/aspm/RepositoryDashboard";
import RiskDashboard from "@/pages/aspm/RiskDashboard";
import PostureDashboard from "@/pages/aspm/PostureDashboard";

// DevSecOps
import { SecureSDLCDashboard } from "@/pages/devsecops/SecureSDLCDashboard";
import { PipelineDashboard } from "@/pages/devsecops/PipelineDashboard";
import { SecurityGatesDashboard } from "@/pages/devsecops/SecurityGatesDashboard";
import { DeveloperDashboard } from "@/pages/devsecops/DeveloperDashboard";
import { DevSecOpsExecutiveDashboard } from "@/pages/devsecops/DevSecOpsExecutiveDashboard";

// SBOM
import { SBOMExecutiveDashboard } from "@/pages/sbom/SBOMExecutiveDashboard";
import { SBOMDashboard } from "@/pages/sbom/SBOMDashboard";
import { DependencyExplorer as SBOMDependencyExplorer } from "@/pages/sbom/DependencyExplorer";
import { ArtifactInventory } from "@/pages/sbom/ArtifactInventory";
import { ProvenanceDashboard } from "@/pages/sbom/ProvenanceDashboard";

// SAST
import { SASTExecutiveDashboard } from "@/pages/sast/SASTExecutiveDashboard";
import { CodeFindingsDashboard } from "@/pages/sast/CodeFindingsDashboard";
import { RuleCoverageDashboard } from "@/pages/sast/RuleCoverageDashboard";
import { DeveloperGuidance } from "@/pages/sast/DeveloperGuidance";

// DAST
import { DASTExecutiveDashboard } from "@/pages/dast/DASTExecutiveDashboard";
import { ApplicationTargetsDashboard } from "@/pages/dast/ApplicationTargetsDashboard";
import { RuntimeFindingsDashboard } from "@/pages/dast/RuntimeFindingsDashboard";
import { APIAssessmentDashboard } from "@/pages/dast/APIAssessmentDashboard";

// SCA
import { SCAExecutiveDashboard } from "@/pages/sca/SCAExecutiveDashboard";
import { DependencyExplorer as SCADependencyExplorer } from "@/pages/sca/DependencyExplorer";
import { PackageIntelligenceDashboard } from "@/pages/sca/PackageIntelligenceDashboard";
import { LicenseDashboard } from "@/pages/sca/LicenseDashboard";

// Secrets
import { SecretsExecutiveDashboard } from "@/pages/secrets/SecretsExecutiveDashboard";
import { CredentialGovernanceDashboard } from "@/pages/secrets/CredentialGovernanceDashboard";
import { CertificateDashboard } from "@/pages/secrets/CertificateDashboard";
import { ExposureDashboard } from "@/pages/secrets/ExposureDashboard";

// IaC
import { IaCExecutiveDashboard } from "@/pages/iac/IaCExecutiveDashboard";
import { TemplateExplorer } from "@/pages/iac/TemplateExplorer";
import { ConfigurationDashboard } from "@/pages/iac/ConfigurationDashboard";
import { DeploymentGovernanceDashboard } from "@/pages/iac/DeploymentGovernanceDashboard";

// Copilot
import { CopilotDashboard } from "@/pages/copilot/CopilotDashboard";
import { CodeReviewDashboard } from "@/pages/copilot/CodeReviewDashboard";
import { LearningDashboard } from "@/pages/copilot/LearningDashboard";
import { DeveloperAssistantPanel } from "@/pages/copilot/DeveloperAssistantPanel";

// AppSec Command Center
import { UnifiedAppSecDashboard } from "@/pages/appsec-command-center/UnifiedAppSecDashboard";
import { EngineeringIntelligenceDashboard } from "@/pages/appsec-command-center/EngineeringIntelligenceDashboard";
import { AppSecExecutiveBoard } from "@/pages/appsec-command-center/AppSecExecutiveBoard";

// ISPM — Enterprise Identity Security Posture Management
import ISPMDashboard from "@/pages/ispm/ISPMDashboard";
import IdentityInventoryDashboard from "@/pages/ispm/IdentityInventoryDashboard";
import AccessGovernanceDashboard from "@/pages/ispm/AccessGovernanceDashboard";
import AuthenticationDashboard from "@/pages/ispm/AuthenticationDashboard";
import ZeroTrustDashboard from "@/pages/ispm/ZeroTrustDashboard";
import IdentityRiskDashboard from "@/pages/ispm/IdentityRiskDashboard";
import ISPMAIAssistant from "@/pages/ispm/ISPMAIAssistant";

// ZTA — Enterprise Zero Trust Architecture
import ZTADashboard from "@/pages/zta/ZTADashboard";
import ContinuousVerificationDashboard from "@/pages/zta/ContinuousVerificationDashboard";
import AdaptiveAccessDashboard from "@/pages/zta/AdaptiveAccessDashboard";
import PolicyGovernanceDashboard from "@/pages/zta/PolicyGovernanceDashboard";
import SessionIntelligenceDashboard from "@/pages/zta/SessionIntelligenceDashboard";
import ZTAAIAssistant from "@/pages/zta/ZTAAIAssistant";

// PAM — Enterprise Privileged Access Management
import PAMDashboard from "@/pages/pam/PAMDashboard";
import PrivilegedIdentityDashboard from "@/pages/pam/PrivilegedIdentityDashboard";
import JITAccessDashboard from "@/pages/pam/JITAccessDashboard";
import AdministrativeSessionDashboard from "@/pages/pam/AdministrativeSessionDashboard";
import CredentialGovernanceDashboard from "@/pages/pam/CredentialGovernanceDashboard";
import PrivilegeRiskDashboard from "@/pages/pam/PrivilegeRiskDashboard";
import PAMAIAssistant from "@/pages/pam/PAMAIAssistant";

// ITDR — Enterprise Identity Threat Detection & Response
import ITDRDashboard from "@/pages/itdr/ITDRDashboard";
import IdentityTimelineDashboard from "@/pages/itdr/IdentityTimelineDashboard";
import BehaviorAnalyticsDashboard from "@/pages/itdr/BehaviorAnalyticsDashboard";
import CredentialDefenseDashboard from "@/pages/itdr/CredentialDefenseDashboard";
import InvestigationDashboard from "@/pages/itdr/InvestigationDashboard";
import IdentityRiskDashboard from "@/pages/itdr/IdentityRiskDashboard";
import ITDRAIAssistant from "@/pages/itdr/ITDRAIAssistant";

// IGA — Enterprise Identity Governance & Administration
import IGADashboard from "@/pages/iga/IGADashboard";
import IdentityLifecycleDashboard from "@/pages/iga/IdentityLifecycleDashboard";
import AccessRequestDashboard from "@/pages/iga/AccessRequestDashboard";
import CertificationDashboard from "@/pages/iga/CertificationDashboard";
import EntitlementDashboard from "@/pages/iga/EntitlementDashboard";
import SoDDashboard from "@/pages/iga/SoDDashboard";
import IGAAIAssistant from "@/pages/iga/IGAAIAssistant";

// NHI — Enterprise Machine & Non-Human Identity Security
import NHIDashboard from "@/pages/nhi/NHIDashboard";
import MachineIdentityDashboard from "@/pages/nhi/MachineIdentityDashboard";
import WorkloadIdentityDashboard from "@/pages/nhi/WorkloadIdentityDashboard";
import CertificateDashboard from "@/pages/nhi/CertificateDashboard";
import TrustRelationshipDashboard from "@/pages/nhi/TrustRelationshipDashboard";
import NHILifecycleDashboard from "@/pages/nhi/NHILifecycleDashboard";
import NHIAIAssistant from "@/pages/nhi/NHIAIAssistant";

// AUTHN — Enterprise Passwordless Authentication Platform
import AuthnDashboard from "@/pages/authn/AuthnDashboard";
import PasskeyDashboard from "@/pages/authn/PasskeyDashboard";
import EnrollmentDashboard from "@/pages/authn/EnrollmentDashboard";
import AssuranceDashboard from "@/pages/authn/AssuranceDashboard";
import AuthnPolicyDashboard from "@/pages/authn/AuthnPolicyDashboard";
import AuthnAIAssistant from "@/pages/authn/AuthnAIAssistant";

// FEDERATION — Enterprise Federated Identity Platform
import FederationDashboard from "@/pages/federation/FederationDashboard";
import SSODashboard from "@/pages/federation/SSODashboard";
import TrustDashboard from "@/pages/federation/TrustDashboard";
import ProtocolDashboard from "@/pages/federation/ProtocolDashboard";
import MetadataDashboard from "@/pages/federation/MetadataDashboard";
import FederationAIAssistant from "@/pages/federation/FederationAIAssistant";

// IDENTITY_INTEL — Enterprise Identity Intelligence Platform
import IdentityIntelDashboard from "@/pages/identity_intel/IdentityIntelDashboard";
import BehaviorDashboard from "@/pages/identity_intel/BehaviorDashboard";
import AdaptiveTrustDashboard from "@/pages/identity_intel/AdaptiveTrustDashboard";
import IdentityRiskDashboard from "@/pages/identity_intel/IdentityRiskDashboard";
import ExecutiveIntelDashboard from "@/pages/identity_intel/ExecutiveIntelDashboard";
import IdentityIntelAIAssistant from "@/pages/identity_intel/IdentityIntelAIAssistant";

// IDENTITY_COMMAND_CENTER — Enterprise Unified Identity Security Command Center
import IdentityCommandCenterDashboard from "@/pages/identity_cc/IdentityCommandCenterDashboard";
import UnifiedZeroTrustDashboard from "@/pages/identity_cc/UnifiedZeroTrustDashboard";
import UnifiedGovernanceDashboard from "@/pages/identity_cc/UnifiedGovernanceDashboard";
import UnifiedRiskDashboard from "@/pages/identity_cc/UnifiedRiskDashboard";
import BoardReportingDashboard from "@/pages/identity_cc/BoardReportingDashboard";
import IdentityCCAIAssistant from "@/pages/identity_cc/IdentityCCAIAssistant";

// CYBER_FUSION — Enterprise Cyber Fusion Center
import CyberFusionDashboard from "@/pages/cyber_fusion/CyberFusionDashboard";
import CrossDomainCorrelationDashboard from "@/pages/cyber_fusion/CrossDomainCorrelationDashboard";
import AttackSurfaceDashboard from "@/pages/cyber_fusion/AttackSurfaceDashboard";
import StrategicExecutiveDashboard from "@/pages/cyber_fusion/StrategicExecutiveDashboard";
import CyberFusionAIAssistant from "@/pages/cyber_fusion/CyberFusionAIAssistant";

// ORCHESTRATION — Enterprise AI Security Orchestration Platform
import OrchestrationDashboard from "@/pages/orchestration/OrchestrationDashboard";
import PlaybookDashboard from "@/pages/orchestration/PlaybookDashboard";
import TaskDashboard from "@/pages/orchestration/TaskDashboard";
import DecisionDashboard from "@/pages/orchestration/DecisionDashboard";
import OrchestrationAIAssistant from "@/pages/orchestration/OrchestrationAIAssistant";

// DIGITAL_TWIN — Enterprise Cyber Digital Twin Platform
import DigitalTwinDashboard from "@/pages/digital_twin/DigitalTwinDashboard";
import EnterpriseModelExplorer from "@/pages/digital_twin/EnterpriseModelExplorer";
import AttackPathDashboard from "@/pages/digital_twin/AttackPathDashboard";
import ScenarioSimulationDashboard from "@/pages/digital_twin/ScenarioSimulationDashboard";
import DigitalTwinAIAssistant from "@/pages/digital_twin/DigitalTwinAIAssistant";

// PREDICTIVE_RISK — Enterprise Predictive Cyber Risk & Strategy Platform
import PredictiveRiskDashboard from "@/pages/predictive_risk/PredictiveRiskDashboard";
import ExecutiveForecastDashboard from "@/pages/predictive_risk/ExecutiveForecastDashboard";
import InvestmentPrioritizationDashboard from "@/pages/predictive_risk/InvestmentPrioritizationDashboard";
import StrategicPlanningDashboard from "@/pages/predictive_risk/StrategicPlanningDashboard";
import PredictiveAIAssistant from "@/pages/predictive_risk/PredictiveAIAssistant";

// CYBER_RESILIENCE — Enterprise Cyber Resilience & BCP
import ResilienceDashboard from "@/pages/cyber_resilience/ResilienceDashboard";
import BusinessContinuityDashboard from "@/pages/cyber_resilience/BusinessContinuityDashboard";
import DisasterRecoveryDashboard from "@/pages/cyber_resilience/DisasterRecoveryDashboard";
import TabletopExerciseDashboard from "@/pages/cyber_resilience/TabletopExerciseDashboard";
import ResilienceAIAssistant from "@/pages/cyber_resilience/ResilienceAIAssistant";

export const router = createBrowserRouter([
  {
    element: <AuthLayout />,
    children: [
      {
        path: "login",
        element: <Login />,
      },
      {
        path: "register",
        element: <Register />,
      },
    ],
  },
  {
    element: <AuthGuard />,
    children: [
      {
        element: <DashboardLayout />,
        children: [
          {
            path: "/",
            element: <Navigate to="/dashboard" replace />,
          },
          {
            path: "dashboard",
            element: <Dashboard />,
          },
          {
            path: "ai-brain",
            element: <AIBrainDashboard />,
          },
          {
            path: "ai-brain/models",
            element: <ProviderModelManager />,
          },
          {
            path: "ai-brain/prompts",
            element: <PromptCapabilityLibrary />,
          },
          {
            path: "ai-brain/memory",
            element: <ConversationMemoryExplorer />,
          },
          {
            path: "ai-brain/observability",
            element: <AIObservabilityAudit />,
          },
          {
            path: "multi-agent/dashboard",
            element: <AIWorkforceDashboard />,
          },
          {
            path: 'ai-memory',
            element: <MemoryDashboard />
          },
          {
            path: 'ai-context',
            element: <ContextDashboard />
          },
          {
            path: 'prompt-platform',
            element: <PromptDashboard />
          },
          {
            path: 'prompt-platform/editor/:id',
            element: <PromptEditor />
          },
          {
            path: 'rag',
            element: <KnowledgeDashboard />
          },
          {
            path: 'rag/library',
            element: <DocumentExplorer />
          },
          {
            path: 'rag/search',
            element: <SearchInterface />
          },
          {
            path: 'knowledge-graph',
            element: <GraphDashboard />
          },
          {
            path: 'knowledge-graph/explore',
            element: <EntityExplorer />
          },
          {
            path: 'knowledge-graph/viewer',
            element: <RelationshipViewer />
          },
          {
            path: 'decision',
            element: <DecisionDashboard />
          },
          {
            path: 'decision/approval',
            element: <ApprovalCenter />
          },
          {
            path: 'decision/view/:id',
            element: <ReasoningViewer />
          },
          {
            path: 'xai',
            element: <XAIDashboard />
          },
          {
            path: 'xai/view/:decisionId',
            element: <EvidenceTrace />
          },
          {
            path: 'models',
            element: <ModelDashboard />
          },
          {
            path: 'models/registry',
            element: <ProviderRegistry />
          },
          {
            path: 'models/routing',
            element: <RoutingPolicies />
          },
          {
            path: "investigations/new",
            element: <NewInvestigation />,
          },
          {
            path: "investigations/:id",
            element: <Workspace />,
          },
          {
            path: "url-intelligence",
            element: <URLInvestigationDashboard />,
          },
          {
            path: "website-investigation",
            element: <WebsiteInvestigationDashboard />,
          },
          {
            path: "email-intelligence",
            element: <EmailInvestigationDashboard />,
          },
          {
            path: "qr-intelligence",
            element: <QRInvestigationDashboard />,
          },
          {
            path: "malware-intelligence",
            element: <MalwareInvestigationDashboard />,
          },
          {
            path: "mobile-investigation",
            element: <MobileInvestigationDashboard />,
          },
          {
            path: "browser-investigation",
            element: <BrowserInvestigationDashboard />,
          },
          {
            path: "network-investigation",
            element: <NetworkInvestigationDashboard />,
          },
          {
            path: "cloud-investigation",
            element: <CloudInvestigationDashboard />,
          },
          {
            path: "ctem/dashboard",
            element: <CTEMDashboard />,
          },
          {
            path: "command-center",
            element: <CommandCenterDashboard />,
          },
          {
            path: "aspm/dashboard",
            element: <ASPMDashboard />,
          },
          {
            path: "aspm/applications",
            element: <ApplicationInventory />,
          },
          {
            path: "aspm/repositories",
            element: <RepositoryDashboard />,
          },
          {
            path: "aspm/risk",
            element: <RiskDashboard />,
          },
          {
            path: "aspm/posture",
            element: <PostureDashboard />,
          },
          {
            path: "devsecops/dashboard",
            element: <DevSecOpsExecutiveDashboard />,
          },
          {
            path: "devsecops/sdlc",
            element: <SecureSDLCDashboard />,
          },
          {
            path: "devsecops/pipelines",
            element: <PipelineDashboard />,
          },
          {
            path: "devsecops/gates",
            element: <SecurityGatesDashboard />,
          },
          {
            path: "devsecops/developers",
            element: <DeveloperDashboard />,
          },
          {
            path: "sbom/dashboard",
            element: <SBOMExecutiveDashboard />,
          },
          {
            path: "sbom/records",
            element: <SBOMDashboard />,
          },
          {
            path: "sbom/dependencies",
            element: <SBOMDependencyExplorer />,
          },
          {
            path: "sbom/artifacts",
            element: <ArtifactInventory />,
          },
          {
            path: "sbom/provenance",
            element: <ProvenanceDashboard />,
          },
          {
            path: "sast/dashboard",
            element: <SASTExecutiveDashboard />,
          },
          {
            path: "sast/findings",
            element: <CodeFindingsDashboard />,
          },
          {
            path: "sast/rules",
            element: <RuleCoverageDashboard />,
          },
          {
            path: "sast/guidance",
            element: <DeveloperGuidance />,
          },
          {
            path: "dast/dashboard",
            element: <DASTExecutiveDashboard />,
          },
          {
            path: "dast/targets",
            element: <ApplicationTargetsDashboard />,
          },
          {
            path: "dast/findings",
            element: <RuntimeFindingsDashboard />,
          },
          {
            path: "dast/api-assessment",
            element: <APIAssessmentDashboard />,
          },
          {
            path: "sca/dashboard",
            element: <SCAExecutiveDashboard />,
          },
          {
            path: "sca/dependencies",
            element: <SCADependencyExplorer />,
          },
          {
            path: "sca/packages",
            element: <PackageIntelligenceDashboard />,
          },
          {
            path: "sca/licenses",
            element: <LicenseDashboard />,
          },
          {
            path: "secrets/dashboard",
            element: <SecretsExecutiveDashboard />,
          },
          {
            path: "secrets/credentials",
            element: <CredentialGovernanceDashboard />,
          },
          {
            path: "secrets/certificates",
            element: <CertificateDashboard />,
          },
          {
            path: "secrets/exposures",
            element: <ExposureDashboard />,
          },
          {
            path: "iac/dashboard",
            element: <IaCExecutiveDashboard />,
          },
          {
            path: "iac/templates",
            element: <TemplateExplorer />,
          },
          {
            path: "iac/configurations",
            element: <ConfigurationDashboard />,
          },
          {
            path: "iac/governance",
            element: <DeploymentGovernanceDashboard />,
          },
          {
            path: "copilot/dashboard",
            element: <CopilotDashboard />,
          },
          {
            path: "copilot/code-review",
            element: <CodeReviewDashboard />,
          },
          {
            path: "copilot/learning",
            element: <LearningDashboard />,
          },
          {
            path: "copilot/assistant",
            element: <DeveloperAssistantPanel />,
          },
          {
            path: "appsec-command-center/dashboard",
            element: <UnifiedAppSecDashboard />,
          },
          {
            path: "appsec-command-center/engineering",
            element: <EngineeringIntelligenceDashboard />,
          },
          {
            path: "appsec-command-center/executive",
            element: <AppSecExecutiveBoard />,
          },
          // ── ISPM — Enterprise Identity Security Posture Management ──
          {
            path: "ispm",
            element: <ISPMDashboard />,
          },
          {
            path: "ispm/inventory",
            element: <IdentityInventoryDashboard />,
          },
          {
            path: "ispm/governance",
            element: <AccessGovernanceDashboard />,
          },
          {
            path: "ispm/authentication",
            element: <AuthenticationDashboard />,
          },
          {
            path: "ispm/zero-trust",
            element: <ZeroTrustDashboard />,
          },
          {
            path: "ispm/risk",
            element: <IdentityRiskDashboard />,
          },
          {
            path: "ispm/ai-assistant",
            element: <ISPMAIAssistant />,
          },

          {
            path: "threat-intel/dashboard",
            element: <ThreatIntelDashboard />,
          },
          {
            path: "threat-intel/search",
            element: <IndicatorSearch />,
          },
          {
            path: "cases",
            element: <CaseList />,
          },
          {
            path: "cases/:id",
            element: <CaseWorkspace />,
          },
          {
            path: "automation",
            element: <WorkflowDashboard />,
          },
          {
            path: "automation/builder/:id",
            element: <WorkflowBuilder />,
          },
          {
            path: "zta",
            element: <ZTADashboard />,
          },
          {
            path: "zta/verify",
            element: <ContinuousVerificationDashboard />,
          },
          {
            path: "zta/access",
            element: <AdaptiveAccessDashboard />,
          },
          {
            path: "zta/policies",
            element: <PolicyGovernanceDashboard />,
          },
          {
            path: "zta/sessions",
            element: <SessionIntelligenceDashboard />,
          },
          {
            path: "zta/assistant",
            element: <ZTAAIAssistant />,
          },
          {
            path: "pam",
            element: <PAMDashboard />,
          },
          {
            path: "pam/identities",
            element: <PrivilegedIdentityDashboard />,
          },
          {
            path: "pam/jit",
            element: <JITAccessDashboard />,
          },
          {
            path: "pam/sessions",
            element: <AdministrativeSessionDashboard />,
          },
          {
            path: "pam/credentials",
            element: <CredentialGovernanceDashboard />,
          },
          {
            path: "pam/risk",
            element: <PrivilegeRiskDashboard />,
          },
          {
            path: "pam/assistant",
            element: <PAMAIAssistant />,
          },
          {
            path: "itdr",
            element: <ITDRDashboard />,
          },
          {
            path: "itdr/timeline",
            element: <IdentityTimelineDashboard />,
          },
          {
            path: "itdr/behavior",
            element: <BehaviorAnalyticsDashboard />,
          },
          {
            path: "itdr/credentials",
            element: <CredentialDefenseDashboard />,
          },
          {
            path: "itdr/investigations",
            element: <InvestigationDashboard />,
          },
          {
            path: "itdr/risk",
            element: <IdentityRiskDashboard />,
          },
          {
            path: "itdr/assistant",
            element: <ITDRAIAssistant />,
          },
          {
            path: "iga",
            element: <IGADashboard />,
          },
          {
            path: "iga/lifecycle",
            element: <IdentityLifecycleDashboard />,
          },
          {
            path: "iga/requests",
            element: <AccessRequestDashboard />,
          },
          {
            path: "iga/certifications",
            element: <CertificationDashboard />,
          },
          {
            path: "iga/entitlements",
            element: <EntitlementDashboard />,
          },
          {
            path: "iga/sod",
            element: <SoDDashboard />,
          },
          {
            path: "iga/assistant",
            element: <IGAAIAssistant />,
          },
          {
            path: "nhi",
            element: <NHIDashboard />,
          },
          {
            path: "nhi/identities",
            element: <MachineIdentityDashboard />,
          },
          {
            path: "nhi/workloads",
            element: <WorkloadIdentityDashboard />,
          },
          {
            path: "nhi/certificates",
            element: <CertificateDashboard />,
          },
          {
            path: "nhi/trust",
            element: <TrustRelationshipDashboard />,
          },
          {
            path: "nhi/lifecycle",
            element: <NHILifecycleDashboard />,
          },
          {
            path: "nhi/assistant",
            element: <NHIAIAssistant />,
          },
          {
            path: "authn",
            element: <AuthnDashboard />,
          },
          {
            path: "authn/passkeys",
            element: <PasskeyDashboard />,
          },
          {
            path: "authn/enrollments",
            element: <EnrollmentDashboard />,
          },
          {
            path: "authn/assurance",
            element: <AssuranceDashboard />,
          },
          {
            path: "authn/policies",
            element: <AuthnPolicyDashboard />,
          },
          {
            path: "authn/assistant",
            element: <AuthnAIAssistant />,
          },
          {
            path: "federation",
            element: <FederationDashboard />,
          },
          {
            path: "federation/sso",
            element: <SSODashboard />,
          },
          {
            path: "federation/trusts",
            element: <TrustDashboard />,
          },
          {
            path: "federation/protocols",
            element: <ProtocolDashboard />,
          },
          {
            path: "federation/metadata",
            element: <MetadataDashboard />,
          },
          {
            path: "federation/assistant",
            element: <FederationAIAssistant />,
          },
          {
            path: "identity-intel",
            element: <IdentityIntelDashboard />,
          },
          {
            path: "identity-intel/behavior",
            element: <BehaviorDashboard />,
          },
          {
            path: "identity-intel/trust",
            element: <AdaptiveTrustDashboard />,
          },
          {
            path: "identity-intel/risk",
            element: <IdentityRiskDashboard />,
          },
          {
            path: "identity-intel/executive",
            element: <ExecutiveIntelDashboard />,
          },
          {
            path: "identity-intel/assistant",
            element: <IdentityIntelAIAssistant />,
          },
          {
            path: "identity-cc",
            element: <IdentityCommandCenterDashboard />,
          },
          {
            path: "identity-cc/zero-trust",
            element: <UnifiedZeroTrustDashboard />,
          },
          {
            path: "identity-cc/governance",
            element: <UnifiedGovernanceDashboard />,
          },
          {
            path: "identity-cc/risk",
            element: <UnifiedRiskDashboard />,
          },
          {
            path: "identity-cc/board",
            element: <BoardReportingDashboard />,
          },
          {
            path: "identity-cc/assistant",
            element: <IdentityCCAIAssistant />,
          },
          {
            path: "cyber-fusion",
            element: <CyberFusionDashboard />,
          },
          {
            path: "cyber-fusion/correlation",
            element: <CrossDomainCorrelationDashboard />,
          },
          {
            path: "cyber-fusion/attack-surface",
            element: <AttackSurfaceDashboard />,
          },
          {
            path: "cyber-fusion/executive",
            element: <StrategicExecutiveDashboard />,
          },
          {
            path: "cyber-fusion/assistant",
            element: <CyberFusionAIAssistant />,
          },
          {
            path: "orchestration",
            element: <OrchestrationDashboard />,
          },
          {
            path: "orchestration/playbooks",
            element: <PlaybookDashboard />,
          },
          {
            path: "orchestration/tasks",
            element: <TaskDashboard />,
          },
          {
            path: "orchestration/decisions",
            element: <DecisionDashboard />,
          },
          {
            path: "orchestration/assistant",
            element: <OrchestrationAIAssistant />,
          },
          {
            path: "digital-twin",
            element: <DigitalTwinDashboard />,
          },
          {
            path: "digital-twin/explorer",
            element: <EnterpriseModelExplorer />,
          },
          {
            path: "digital-twin/attack-paths",
            element: <AttackPathDashboard />,
          },
          {
            path: "digital-twin/simulations",
            element: <ScenarioSimulationDashboard />,
          },
          {
            path: "digital-twin/assistant",
            element: <DigitalTwinAIAssistant />,
          },
          {
            path: "predictive-risk",
            element: <PredictiveRiskDashboard />,
          },
          {
            path: "predictive-risk/forecasts",
            element: <ExecutiveForecastDashboard />,
          },
          {
            path: "predictive-risk/investments",
            element: <InvestmentPrioritizationDashboard />,
          },
          {
            path: "predictive-risk/plans",
            element: <StrategicPlanningDashboard />,
          },
          {
            path: "predictive-risk/assistant",
            element: <PredictiveAIAssistant />,
          },
          {
            path: "cyber-resilience",
            element: <ResilienceDashboard />,
          },
          {
            path: "cyber-resilience/bcp",
            element: <BusinessContinuityDashboard />,
          },
          {
            path: "cyber-resilience/dr",
            element: <DisasterRecoveryDashboard />,
          },
          {
            path: "cyber-resilience/tabletops",
            element: <TabletopExerciseDashboard />,
          },
          {
            path: "cyber-resilience/assistant",
            element: <ResilienceAIAssistant />,
          },
        ],
      },
      {
        path: "admin",
        element: <AdminLayout />,
        children: [
          {
            path: "dashboard",
            element: <TenantDashboard />,
          },
          {
            path: "users",
            element: <UserManagement />,
          },
          {
            path: "policies",
            element: <SecurityPolicies />,
          },
          {
            path: "audit-logs",
            element: <AuditLogs />,
          },
          {
            path: "observability/health",
            element: <SystemHealth />,
          },
          {
            path: "observability/incidents",
            element: <IncidentManager />,
          },
          {
            path: "observability/metrics",
            element: <MetricsExplorer />,
          },
        ]
      }
    ],
  },
]);
