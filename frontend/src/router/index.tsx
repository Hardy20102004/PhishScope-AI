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
