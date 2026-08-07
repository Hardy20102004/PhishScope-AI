import React from 'react';
import { Link } from 'react-router-dom';
import { Shield, Server, Activity, Users, Sparkles } from 'lucide-react';

const RESILIENCE_METRICS = {
  overall_readiness: 88,
  critical_services: 12,
  dr_tests_passed: 4,
  active_tabletops: 1
};

export default function ResilienceDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{RES_STYLES}</style>
      
      {/* Header */}
      <div className="res-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="res-header-icon"><Shield size={24} /></div>
          <div>
            <h1 className="res-title">Cyber Resilience & Continuity</h1>
            <p className="res-subtitle">Continuous operational readiness and disaster recovery</p>
          </div>
        </div>
        <div style={{ display: 'flex', gap: 10 }}>
          <Link to="/cyber-resilience/assistant" className="res-btn res-btn-ai"><Sparkles size={14} /> AI Resilience Copilot</Link>
          <button className="res-btn"><Activity size={14} /> Generate Readiness Report</button>
        </div>
      </div>

      {/* KPI Row */}
      <div className="res-grid-4">
        {[
          { label: 'Overall Readiness Score', value: RESILIENCE_METRICS.overall_readiness, color: '#10b981', suffix: '%' },
          { label: 'Critical Biz Services', value: RESILIENCE_METRICS.critical_services, color: '#3b82f6', suffix: '' },
          { label: 'DR Tests Passed (Q3)', value: RESILIENCE_METRICS.dr_tests_passed, color: '#8b5cf6', suffix: '' },
          { label: 'Active Tabletop Exercises', value: RESILIENCE_METRICS.active_tabletops, color: '#f59e0b', suffix: '' }
        ].map(k => (
          <div key={k.label} className="res-kpi-card" style={{ borderColor: `${k.color}30` }}>
            <span style={{ fontSize: '1.6rem', fontWeight: 800, color: k.color }}>{k.value}{k.suffix}</span>
            <span style={{ fontSize: '0.7rem', color: '#94a3b8' }}>{k.label}</span>
          </div>
        ))}
      </div>

      {/* Navigation Modules */}
      <div className="res-main-layout">
        <div className="res-modules-grid">
          <ModuleCard title="Business Continuity" icon={<Activity />} link="/cyber-resilience/bcp" desc="Critical services, dependencies, and RTO/RPO objectives." color="#3b82f6" />
          <ModuleCard title="Disaster Recovery" icon={<Server />} link="/cyber-resilience/dr" desc="Infrastructure backup, cloud recovery, and DR test history." color="#8b5cf6" />
          <ModuleCard title="Tabletop Exercises" icon={<Users />} link="/cyber-resilience/tabletops" desc="Crisis simulation scenarios and readiness validation." color="#f59e0b" />
        </div>
      </div>
    </div>
  );
}

function ModuleCard({ title, icon, link, desc, color }: any) {
  return (
    <Link to={link} className="res-mod-card" style={{ '--mod-color': color } as React.CSSProperties}>
      <div className="res-mod-icon" style={{ color }}>{icon}</div>
      <div className="res-mod-content">
        <h3 className="res-mod-title">{title}</h3>
        <p className="res-mod-desc">{desc}</p>
      </div>
    </Link>
  );
}

const RES_STYLES = `
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
* { box-sizing: border-box; }
.res-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; flex-wrap: wrap; gap: 16px; }
.res-header-icon { width: 48px; height: 48px; background: linear-gradient(135deg, #10b981, #059669); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.res-title { font-size: 1.45rem; font-weight: 800; margin: 0 0 2px; text-transform: uppercase; letter-spacing: 0.5px; }
.res-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.res-btn { display: inline-flex; align-items: center; gap: 6px; padding: 8px 14px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; color: #e2e8f0; font-size: 0.8rem; text-decoration: none; cursor: pointer; transition: all 0.2s; }
.res-btn:hover { background: rgba(255,255,255,0.1); }
.res-btn-ai { background: rgba(16,185,129,0.15); border-color: rgba(16,185,129,0.3); color: #34d399; }
.res-grid-4 { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; margin-bottom: 24px; }
.res-kpi-card { display: flex; flex-direction: column; padding: 16px; background: rgba(255,255,255,0.03); border: 1px solid; border-radius: 12px; }
.res-modules-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; }
.res-mod-card { display: flex; align-items: flex-start; gap: 16px; padding: 20px; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; text-decoration: none; transition: all 0.2s; }
.res-mod-card:hover { background: rgba(255,255,255,0.04); border-color: var(--mod-color); transform: translateY(-2px); }
.res-mod-icon { padding: 12px; background: rgba(255,255,255,0.03); border-radius: 10px; }
.res-mod-content { flex: 1; }
.res-mod-title { margin: 0 0 4px; font-size: 0.95rem; font-weight: 700; color: #f8fafc; }
.res-mod-desc { margin: 0; font-size: 0.75rem; color: #94a3b8; line-height: 1.4; }
`;
