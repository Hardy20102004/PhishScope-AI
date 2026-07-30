import { Link, useLocation } from "react-router-dom"
import { ShieldAlert, LayoutDashboard, ShieldCheck, Activity, Settings, GitBranch, Cpu, Users, Database, FileText, FileCode, BookOpen, Share2, BrainCircuit, Lightbulb, CloudLightning, Globe, Fingerprint, Target, Shield, Network, LineChart, Briefcase, Crosshair } from "lucide-react"
import { cn } from "@/utils/cn"

export function Sidebar() {
  const location = useLocation()
  
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
    ]
  }

  const NavItem = ({ item }: { item: any }) => {
    const isActive = location.pathname === item.path || location.pathname.startsWith(`${item.path}/`)
    return (
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
  }

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
      
      <div className="flex-1 overflow-y-auto py-6 px-3">
        <nav className="space-y-1">
          <NavGroup label="Unified Command">
            {navItems.unified.map((item, index) => (
              <NavItem key={index} item={item} />
            ))}
          </NavGroup>
          <NavGroup label="Defensive Operations">
            {navItems.defensive.map((item, index) => (
              <NavItem key={index} item={item} />
            ))}
          </NavGroup>
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
