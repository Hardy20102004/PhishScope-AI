import { Link, useLocation } from "react-router-dom"
import { ShieldAlert, LayoutDashboard, ShieldCheck, Activity, Settings, GitBranch, Cpu, Users, Database, FileText, FileCode, BookOpen, Share2, BrainCircuit, Lightbulb, CloudLightning, Globe, Fingerprint, Target, Shield, Network, LineChart, Briefcase, Crosshair } from "lucide-react"
import { cn } from "@/utils/cn"

export function Sidebar() {
  const location = useLocation()
  
  const navItems = [
    { name: "Command Center", path: "/command-center", icon: <Globe size={20} /> },
    { name: "SOC Dashboard", path: "/dashboard", icon: <LayoutDashboard size={20} /> },
    { name: "AI Workforce", path: "/multi-agent/dashboard", icon: <Users size={20} /> },
    { name: "AI Security Brain", path: "/ai-brain", icon: <Cpu size={20} /> },
    { name: "AI Memory Engine", path: "/ai-memory", icon: <Database size={20} /> },
  const navItems = {
    unified: [
      { name: "Cyber Fusion Center", path: "/cyber-fusion", icon: <Target size={20} /> },
      { name: "Cyber Digital Twin", path: "/digital-twin", icon: <Network size={20} /> },
      { name: "Predictive Risk & Strategy", path: "/predictive-risk", icon: <LineChart size={20} /> },
      { name: "Cyber Resilience & BCP", path: "/cyber-resilience", icon: <Shield size={20} /> },
      { name: "Security Data Fabric", path: "/data-fabric", icon: <Database size={20} /> },
      { name: "Knowledge Evolution", path: "/knowledge-evolution", icon: <BrainCircuit size={20} /> },
      { name: "Cyber Governance", path: "/cyber-governance", icon: <Briefcase size={20} /> },
      { name: "Command Center", path: "/command-center", icon: <Globe size={20} /> },
      { name: "Unified Cyber Command", path: "/cyber-command", icon: <Crosshair size={20} /> },
      { name: "SOC Dashboard", path: "/dashboard", icon: <LayoutDashboard size={20} /> },
    ],
    defensive: [
      { name: "Orchestration & SOAR", path: "/orchestration", icon: <GitBranch size={20} /> },
      { name: "AI Workforce", path: "/multi-agent/dashboard", icon: <Users size={20} /> },
      { name: "AI Security Brain", path: "/ai-brain", icon: <Cpu size={20} /> },
      { name: "AI Memory Engine", path: "/ai-memory", icon: <Database size={20} /> },
      { name: "AI Context Engine", path: "/ai-context", icon: <FileText size={20} /> },
      { name: "Prompt Platform", path: "/prompt-platform", icon: <FileCode size={20} /> },
      { name: "RAG Knowledge", path: "/rag", icon: <BookOpen size={20} /> },
      { name: "Knowledge Graph", path: "/knowledge-graph", icon: <Share2 size={20} /> },
      { name: "Decision Engine", path: "/decision", icon: <BrainCircuit size={20} /> },
      { name: "Explainable AI", path: "/xai", icon: <Lightbulb size={20} /> },
      { name: "Model Manager", path: "/models", icon: <Cpu size={20} /> },
      { name: "Cases", path: "/cases", icon: <ShieldAlert size={20} /> },
      { name: "Investigations", path: "/investigations/new", icon: <ShieldAlert size={20} /> },
      { name: "Threat Intel", path: "/threat-intel/dashboard", icon: <Activity size={20} /> },
      { name: "Automation", path: "/automation", icon: <GitBranch size={20} /> },
      { name: "Cloud Exposure", path: "/ctem/dashboard", icon: <CloudLightning size={20} /> },
      { name: "Identity Security (ISPM)", path: "/ispm", icon: <Fingerprint size={20} /> },
      { name: "Zero Trust (ZTA)", path: "/zta", icon: <ShieldCheck size={20} /> },
      { name: "Privileged Access (PAM)", path: "/pam", icon: <ShieldAlert size={20} /> },
      { name: "Identity Threats (ITDR)", path: "/itdr", icon: <Target size={20} /> },
      { name: "Identity Governance (IGA)", path: "/iga", icon: <BookOpen size={20} /> },
      { name: "Machine Identity (NHI)", path: "/nhi", icon: <Cpu size={20} /> },
      { name: "Passwordless (AUTHN)", path: "/authn", icon: <Fingerprint size={20} /> },
      { name: "Federation & SSO", path: "/federation", icon: <Globe size={20} /> },
      { name: "Identity Intel", path: "/identity-intel", icon: <BrainCircuit size={20} /> },
      { name: "Command Center", path: "/identity-cc", icon: <Shield size={20} /> },
      { name: "Policies", path: "/admin/policies", icon: <ShieldCheck size={20} /> },
      { name: "Settings", path: "/admin/dashboard", icon: <Settings size={20} /> },
    ]
  }

  const NavItem = ({ item, isActive }: { item: any, isActive: boolean }) => (
    <Link
      to={item.path}
      className={cn(
        "flex items-center rounded-md px-3 py-2 text-sm font-medium transition-colors",
        isActive
          ? "bg-primary/10 text-primary"
          : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
      )}
    >
      {item.icon}
      <span className="ml-3">{item.name}</span>
    </Link>
  )

  const NavGroup = ({ label, children }: { label: string, children: React.ReactNode }) => (
    <div className="mb-6">
      <h3 className="px-3 mb-2 text-xs font-semibold text-muted-foreground uppercase tracking-wider">{label}</h3>
      <div className="space-y-1">{children}</div>
    </div>
  )

  return (
    <div className="flex h-full w-64 flex-col border-r bg-card text-card-foreground">
      <div className="flex h-16 items-center border-b px-6">
        <ShieldAlert className="mr-2 h-6 w-6 text-primary" />
        <span className="text-lg font-bold tracking-tight">PHOENIX</span>
      </div>
      
                className={cn(
                  "flex items-center rounded-md px-3 py-2 text-sm font-medium transition-colors",
                  isActive
                    ? "bg-primary/10 text-primary"
                    : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
                )}
              >
                {item.icon}
                <span className="ml-3">{item.name}</span>
              </Link>
            )
          })}
        </nav>
      </div>
      
      <div className="border-t p-4">
        <div className="rounded-lg bg-secondary p-4 text-xs">
          <p className="font-semibold text-foreground">Environment</p>
          <p className="text-muted-foreground">SOC Production (Tier 1)</p>
        </div>
      </div>
    </div>
  )
}
