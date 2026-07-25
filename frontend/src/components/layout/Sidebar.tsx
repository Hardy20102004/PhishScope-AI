import { Link, useLocation } from "react-router-dom"
import { ShieldAlert, LayoutDashboard, ShieldCheck, Activity, Settings, GitBranch, Cpu, Users, Database, FileText, FileCode, BookOpen, Share2, BrainCircuit, Lightbulb } from "lucide-react"
import { cn } from "@/utils/cn"

export function Sidebar() {
  const location = useLocation()
  
  const navItems = [
    { name: "Command Center", path: "/dashboard", icon: <LayoutDashboard size={20} /> },
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
    { name: "Investigations", path: "/investigations", icon: <ShieldAlert size={20} /> },
    { name: "Threat Intel", path: "/threat-intel/dashboard", icon: <Activity size={20} /> },
    { name: "Automation", path: "/automation", icon: <GitBranch size={20} /> },
    { name: "Policies", path: "/admin/policies", icon: <ShieldCheck size={20} /> },
    { name: "Settings", path: "/settings", icon: <Settings size={20} /> },
  ]

  return (
    <div className="flex h-full w-64 flex-col border-r bg-card text-card-foreground">
      <div className="flex h-16 items-center border-b px-6">
        <ShieldAlert className="mr-2 h-6 w-6 text-primary" />
        <span className="text-lg font-bold tracking-tight">PHOENIX</span>
      </div>
      
      <div className="flex-1 overflow-auto py-4">
        <nav className="space-y-1 px-3">
          {navItems.map((item) => {
            const isActive = location.pathname.startsWith(item.path)
            return (
              <Link
                key={item.name}
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
