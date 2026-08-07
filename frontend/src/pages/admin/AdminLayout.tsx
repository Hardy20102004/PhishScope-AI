import { Outlet, NavLink } from 'react-router-dom';
import { Settings, Users, ShieldAlert, FileText, Database, Activity, AlertTriangle, BarChart3 } from 'lucide-react';
import { clsx } from 'clsx';

export default function AdminLayout() {
  const navItems = [
    { to: '/admin/dashboard', icon: Database, label: 'Tenant Status' },
    { to: '/admin/users', icon: Users, label: 'Directory' },
    { to: '/admin/policies', icon: ShieldAlert, label: 'Security Policies' },
    { to: '/admin/audit-logs', icon: FileText, label: 'Audit Logs' },
    { to: '/admin/observability/health', icon: Activity, label: 'System Health' },
    { to: '/admin/observability/incidents', icon: AlertTriangle, label: 'Incidents' },
    { to: '/admin/observability/metrics', icon: BarChart3, label: 'Metrics Explorer' },
    { to: '/admin/dashboard', icon: Settings, label: 'Settings' },
  ];

  return (
    <div className="flex h-[calc(100vh-4rem)]">
      {/* Admin Sidebar */}
      <div className="w-64 border-r border-slate-800 bg-slate-900/50 p-4 flex flex-col gap-2">
        <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-4 px-2">
          Enterprise Admin
        </div>
        
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              clsx(
                'flex items-center gap-3 px-3 py-2 rounded-md transition-colors text-sm font-medium',
                isActive
                  ? 'bg-blue-500/10 text-blue-400'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
              )
            }
          >
            <item.icon className="w-4 h-4" />
            {item.label}
          </NavLink>
        ))}
      </div>

      {/* Admin Content Area */}
      <div className="flex-1 overflow-auto bg-slate-950 p-8">
        <Outlet />
      </div>
    </div>
  );
}
