import React from 'react';
import { Link } from 'react-router-dom';
import { Share2, Network, ShieldAlert, Play, TrendingUp, Sparkles } from 'lucide-react';

const TWIN_METRICS = {
  asset_nodes: 14502,
  identity_nodes: 840,
  active_attack_paths: 14,
  simulations_running: 2,
  enterprise_resilience: 88
};

export default function DigitalTwinDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{DT_STYLES}</style>
      
      {/* Header */}
      <div className="dt-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="dt-header-icon"><Share2 size={24} /></div>
          <div>
            <h1 className="dt-title">Cyber Digital Twin</h1>
            <p className="dt-subtitle">Virtual enterprise model for predictive security & attack path intelligence.</p>
          </div>
        </div>
        <div style={{ display: 'flex', gap: 10 }}>
          <Link to="/digital-twin/assistant" className="dt-btn dt-btn-ai"><Sparkles size={14} /> AI Twin Copilot</Link>
          <Link to="/digital-twin/simulations" className="dt-btn"><Play size={14} /> Run Simulation</Link>
        </div>
      </div>

      {/* Primary KPI Row */}
      <div className="dt-grid-5">
        {[
          { label: 'Enterprise Resilience Score', value: TWIN_METRICS.enterprise_resilience, color: '#10b981', suffix: '%' },
          { label: 'Modeled Assets', value: TWIN_METRICS.asset_nodes, color: '#3b82f6', suffix: '' },
          { label: 'Modeled Identities', value: TWIN_METRICS.identity_nodes, color: '#8b5cf6', suffix: '' },
          { label: 'Critical Attack Paths', value: TWIN_METRICS.active_attack_paths, color: '#ef4444', suffix: '' },
          { label: 'Active Simulations', value: TWIN_METRICS.simulations_running, color: '#f59e0b', suffix: '' }
        ].map(k => (
          <div key={k.label} className="dt-kpi-card" style={{ borderColor: `${k.color}30` }}>
            <span style={{ fontSize: '1.6rem', fontWeight: 800, color: k.color }}>{k.value}{k.suffix}</span>
            <span style={{ fontSize: '0.7rem', color: '#94a3b8' }}>{k.label}</span>
          </div>
        ))}
      </div>

      <div className="dt-main-layout">
        <div className="dt-modules-grid">
          <ModuleCard title="Enterprise Model Explorer" icon={<Network />} link="/digital-twin/explorer" desc="Interactive 3D graph of assets, identities, and trust." color="#3b82f6" />
          <ModuleCard title="Attack Path Intelligence" icon={<ShieldAlert />} link="/digital-twin/attack-paths" desc="Discovered paths from external entry to critical assets." color="#ef4444" />
          <ModuleCard title="Scenario Simulation" icon={<Play />} link="/digital-twin/simulations" desc="'What-if' defensive modeling and control validation." color="#f59e0b" />
          <ModuleCard title="Predictive Analytics" icon={<TrendingUp />} link="/digital-twin/predictive" desc="Forecasted risk trends based on Twin state." color="#10b981" />
        </div>
      </div>
    </div>
  );
}

function ModuleCard({ title, icon, link, desc, color }: any) {
  return (
    <Link to={link} className="dt-mod-card" style={{ '--mod-color': color } as React.CSSProperties}>
      <div className="dt-mod-icon" style={{ color }}>{icon}</div>
      <div className="dt-mod-content">
        <h3 className="dt-mod-title">{title}</h3>
        <p className="dt-mod-desc">{desc}</p>
      </div>
    </Link>
  );
}

const DT_STYLES = `
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
* { box-sizing: border-box; }
.dt-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; flex-wrap: wrap; gap: 16px; }
.dt-header-icon { width: 48px; height: 48px; background: linear-gradient(135deg, #0ea5e9, #0284c7); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.dt-title { font-size: 1.45rem; font-weight: 800; margin: 0 0 2px; text-transform: uppercase; letter-spacing: 0.5px; }
.dt-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.dt-btn { display: inline-flex; align-items: center; gap: 6px; padding: 8px 14px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; color: #e2e8f0; font-size: 0.8rem; text-decoration: none; transition: all 0.2s; }
.dt-btn:hover { background: rgba(255,255,255,0.1); }
.dt-btn-ai { background: rgba(14,165,233,0.15); border-color: rgba(14,165,233,0.3); color: #38bdf8; }
.dt-grid-5 { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 16px; margin-bottom: 24px; }
.dt-kpi-card { display: flex; flex-direction: column; padding: 16px; background: rgba(255,255,255,0.03); border: 1px solid; border-radius: 12px; }
.dt-modules-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; }
.dt-mod-card { display: flex; align-items: flex-start; gap: 16px; padding: 20px; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; text-decoration: none; transition: all 0.2s; }
.dt-mod-card:hover { background: rgba(255,255,255,0.04); border-color: var(--mod-color); transform: translateY(-2px); }
.dt-mod-icon { padding: 12px; background: rgba(255,255,255,0.03); border-radius: 10px; }
.dt-mod-content { flex: 1; }
.dt-mod-title { margin: 0 0 4px; font-size: 0.95rem; font-weight: 700; color: #f8fafc; }
.dt-mod-desc { margin: 0; font-size: 0.75rem; color: #94a3b8; line-height: 1.4; }
`;
