import React from 'react';
import { Link } from 'react-router-dom';
import { Target, Activity, ShieldAlert, Cpu, Share2, Eye, Server, Lock, Search, Sparkles } from 'lucide-react';

const FUSION_METRICS = {
  enterprise_risk_index: 24, // 0-100 (lower is better)
  active_incidents: 4,
  correlated_threats: 12,
  attack_surface_score: 92,
  identity_health: 88,
  cloud_health: 95
};

export default function CyberFusionDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{CF_STYLES}</style>
      
      {/* Header */}
      <div className="cf-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="cf-header-icon"><Target size={24} /></div>
          <div>
            <h1 className="cf-title">Cyber Fusion Center</h1>
            <p className="cf-subtitle">The apex operating picture correlating SOC, Cloud, AppSec, and Identity Security.</p>
          </div>
        </div>
        <div style={{ display: 'flex', gap: 10 }}>
          <Link to="/cyber-fusion/assistant" className="cf-btn cf-btn-ai"><Sparkles size={14} /> AI Fusion Copilot</Link>
          <Link to="/cyber-fusion/executive" className="cf-btn"><Eye size={14} /> Executive View</Link>
        </div>
      </div>

      {/* Primary KPI Row */}
      <div className="cf-grid-6">
        {[
          { label: 'Enterprise Risk Index', value: FUSION_METRICS.enterprise_risk_index, color: '#10b981', prefix: '' },
          { label: 'Active Incidents (SOC)', value: FUSION_METRICS.active_incidents, color: '#ef4444', prefix: '' },
          { label: 'Correlated Threats', value: FUSION_METRICS.correlated_threats, color: '#f59e0b', prefix: '' },
          { label: 'Attack Surface Health', value: FUSION_METRICS.attack_surface_score, color: '#3b82f6', prefix: '%' },
          { label: 'Identity CC Health', value: FUSION_METRICS.identity_health, color: '#8b5cf6', prefix: '%' },
          { label: 'Cloud CC Health', value: FUSION_METRICS.cloud_health, color: '#0ea5e9', prefix: '%' }
        ].map(k => (
          <div key={k.label} className="cf-kpi-card" style={{ borderColor: `${k.color}30` }}>
            <span style={{ fontSize: '1.6rem', fontWeight: 800, color: k.color }}>{k.value}{k.prefix}</span>
            <span style={{ fontSize: '0.7rem', color: '#94a3b8' }}>{k.label}</span>
          </div>
        ))}
      </div>

      <div className="cf-main-layout">
        <div className="cf-modules-grid">
          <ModuleCard title="Cross-Domain Correlation" icon={<Share2 />} link="/cyber-fusion/correlation" desc="Attack chains spanning Cloud, Network, and Identity." color="#ef4444" />
          <ModuleCard title="Unified Attack Surface" icon={<Activity />} link="/cyber-fusion/attack-surface" desc="Vulnerabilities, CSPM, and AppSec posture." color="#3b82f6" />
          <ModuleCard title="Security Operations (SOC)" icon={<ShieldAlert />} link="/soc" desc="SIEM, SOAR, and Incident Response." color="#f59e0b" />
          <ModuleCard title="Identity Command Center" icon={<Lock />} link="/identity-cc" desc="Enterprise IAM, PAM, and Zero Trust." color="#8b5cf6" />
          <ModuleCard title="Cloud Security Center" icon={<Server />} link="/cloud" desc="Multi-cloud posture and workload protection." color="#0ea5e9" />
          <ModuleCard title="Digital Forensics (DFIR)" icon={<Search />} link="/dfir" desc="Deep-dive endpoint and memory analysis." color="#10b981" />
        </div>
      </div>
    </div>
  );
}

function ModuleCard({ title, icon, link, desc, color }: any) {
  return (
    <Link to={link} className="cf-mod-card" style={{ '--mod-color': color } as React.CSSProperties}>
      <div className="cf-mod-icon" style={{ color }}>{icon}</div>
      <div className="cf-mod-content">
        <h3 className="cf-mod-title">{title}</h3>
        <p className="cf-mod-desc">{desc}</p>
      </div>
    </Link>
  );
}

const CF_STYLES = `
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
* { box-sizing: border-box; }
.cf-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; flex-wrap: wrap; gap: 16px; }
.cf-header-icon { width: 48px; height: 48px; background: linear-gradient(135deg, #3b82f6, #1d4ed8); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.cf-title { font-size: 1.45rem; font-weight: 800; margin: 0 0 2px; text-transform: uppercase; letter-spacing: 0.5px; }
.cf-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.cf-btn { display: inline-flex; align-items: center; gap: 6px; padding: 8px 14px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; color: #e2e8f0; font-size: 0.8rem; text-decoration: none; transition: all 0.2s; }
.cf-btn:hover { background: rgba(255,255,255,0.1); }
.cf-btn-ai { background: rgba(16,185,129,0.15); border-color: rgba(16,185,129,0.3); color: #34d399; }
.cf-grid-6 { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 16px; margin-bottom: 24px; }
.cf-kpi-card { display: flex; flex-direction: column; padding: 16px; background: rgba(255,255,255,0.03); border: 1px solid; border-radius: 12px; }
.cf-modules-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; }
.cf-mod-card { display: flex; align-items: flex-start; gap: 16px; padding: 20px; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; text-decoration: none; transition: all 0.2s; }
.cf-mod-card:hover { background: rgba(255,255,255,0.04); border-color: var(--mod-color); transform: translateY(-2px); }
.cf-mod-icon { padding: 12px; background: rgba(255,255,255,0.03); border-radius: 10px; }
.cf-mod-content { flex: 1; }
.cf-mod-title { margin: 0 0 4px; font-size: 0.95rem; font-weight: 700; color: #f8fafc; }
.cf-mod-desc { margin: 0; font-size: 0.75rem; color: #94a3b8; line-height: 1.4; }
`;
