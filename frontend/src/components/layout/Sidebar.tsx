import { Link, useLocation } from "react-router-dom"
import { 
  ShieldAlert, 
  LayoutDashboard, 
  Globe, 
  QrCode, 
  Mail, 
  Bug, 
  Search, 
  Briefcase, 
  Cpu, 
  HardDrive, 
  Smartphone, 
  Activity, 
  PlusCircle, 
  Shield, 
  Sparkles
} from "lucide-react"
import { cn } from "@/utils/cn"

interface NavItemProps {
  item: {
    name: string;
    path: string;
    icon: React.ReactNode;
    badge?: string;
  }
}

const NavItem = ({ item }: NavItemProps) => {
  const location = useLocation()
  const isActive = location.pathname === item.path || (item.path !== "/" && location.pathname.startsWith(`${item.path}`))
  
  return (
    <Link
      to={item.path}
      className={cn(
        "flex items-center justify-between rounded-lg px-3 py-2 text-sm font-medium transition-all duration-150",
        isActive
          ? "bg-primary text-primary-foreground shadow-sm font-semibold"
          : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
      )}
    >
      <div className="flex items-center">
        {item.icon}
        <span className="ml-3">{item.name}</span>
      </div>
      {item.badge && (
        <span className={cn(
          "text-[10px] font-bold px-1.5 py-0.5 rounded-full uppercase tracking-wider",
          isActive ? "bg-primary-foreground/20 text-primary-foreground" : "bg-primary/10 text-primary"
        )}>
          {item.badge}
        </span>
      )}
    </Link>
  )
}

const NavGroup = ({ label, children }: { label: string, children: React.ReactNode }) => (
  <div className="mb-5">
    <h3 className="px-3 mb-2 text-[11px] font-bold text-muted-foreground uppercase tracking-widest">{label}</h3>
    <div className="space-y-1">{children}</div>
  </div>
)

export function Sidebar() {
  const navItems = {
    phishing: [
      { name: "URL Intelligence", path: "/url-intelligence", icon: <Globe size={18} />, badge: "Gemini AI" },
      { name: "QR Threat Analysis", path: "/qr-intelligence", icon: <QrCode size={18} /> },
      { name: "Malware Intelligence", path: "/malware-intelligence", icon: <Bug size={18} /> },
    ],
    operations: [
      { name: "SOC Dashboard", path: "/dashboard", icon: <LayoutDashboard size={18} /> },
      { name: "New Scan / Investigation", path: "/investigations/new", icon: <PlusCircle size={18} /> },
      { name: "Cases & FIR Tracker", path: "/cases", icon: <Briefcase size={18} /> },
      { name: "Threat Intelligence Feed", path: "/threat-intel/dashboard", icon: <Activity size={18} /> },
    ],
    forensics: [
      { name: "Disk Forensics (DFIR)", path: "/disk-forensics", icon: <HardDrive size={18} /> },
      { name: "Mobile Device Forensics", path: "/mobile-investigation", icon: <Smartphone size={18} /> },
      { name: "AI Security Brain", path: "/ai-brain", icon: <Cpu size={18} /> },
    ]
  }

  return (
    <div className="flex h-full w-64 flex-col border-r bg-card text-card-foreground shadow-sm select-none">
      {/* Header */}
      <div className="flex h-16 items-center border-b px-5 bg-gradient-to-r from-card to-secondary/30">
        <div className="flex items-center justify-center p-1.5 rounded-lg bg-primary/10 text-primary mr-3">
          <ShieldAlert className="h-6 w-6" />
        </div>
        <div className="flex flex-col">
          <span className="text-base font-extrabold tracking-tight text-foreground flex items-center gap-1.5">
            PhishScope <span className="text-xs px-1.5 py-0.2 rounded bg-primary text-primary-foreground font-bold">AI</span>
          </span>
          <span className="text-[10px] text-muted-foreground font-medium">UP Police Cyber Cell</span>
        </div>
      </div>
      
      {/* Navigation */}
      <div className="flex-1 overflow-y-auto py-5 px-3">
        <nav className="space-y-1">
          <NavGroup label="Phishing & Threat Scanners">
            {navItems.phishing.map((item, index) => (
              <NavItem key={index} item={item} />
            ))}
          </NavGroup>

          <NavGroup label="Cyber Crime Operations">
            {navItems.operations.map((item, index) => (
              <NavItem key={index} item={item} />
            ))}
          </NavGroup>

          <NavGroup label="Digital Forensics & AI">
            {navItems.forensics.map((item, index) => (
              <NavItem key={index} item={item} />
            ))}
          </NavGroup>
        </nav>
      </div>
      
      {/* Footer Info */}
      <div className="border-t p-3 bg-secondary/20">
        <div className="rounded-lg border bg-card p-3 text-xs shadow-2xs">
          <div className="flex items-center justify-between font-semibold text-foreground mb-1">
            <span className="flex items-center gap-1.5">
              <Sparkles size={13} className="text-primary" /> Gemini AI Engine
            </span>
            <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
          </div>
          <p className="text-[11px] text-muted-foreground">3.6-flash · Active</p>
        </div>
      </div>
    </div>
  )
}
