import React from 'react';
import { Link } from 'react-router-dom';
import { Shield, Fingerprint, Lock, Globe, Server, UserCheck, Key, Eye, Activity, Bot } from 'lucide-react';

const CC_METRICS = {
  active_identities: 12450,
  machine_identities: 3820,
  federated_trusts: 142,
  avg_trust_score: 88,
  critical_risks: 3,
  pending_approvals: 12
};

export default function IdentityCommandCenterDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{CC_STYLES}</style>
      
      {/* Header */}
      <div className="icc-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="icc-header-icon"><Shield size={24} /></div>
          <div>
            <h1 className="icc-title">Identity Security Command Center</h1>
            <p className="icc-subtitle">Unified apex governance over Zero Trust, Privileged Access, Threat Detection, and Identity Intel.</p>
          </div>
        </div>
        <div style={{ display: 'flex', gap: 10 }}>
          <Link to="/identity-cc/assistant" className="icc-btn icc-btn-ai"><Bot size={14} /> AI Copilot</Link>
          <Link to="/identity-cc/board" className="icc-btn"><Eye size={14} /> Board View</Link>
        </div>
      </div>

      {/* Primary KPI Row */}
      <div className="icc-grid-6">
        {[
          { label: 'Human Identities', value: CC_METRICS.active_identities, color: '#3b82f6' },
          { label: 'Machine Identities', value: CC_METRICS.machine_identities, color: '#8b5cf6' },
          { label: 'Federated Trusts', value: CC_METRICS.federated_trusts, color: '#0ea5e9' },
          { label: 'Global Trust Score', value: CC_METRICS.avg_trust_score, color: '#10b981' },
          { label: 'Critical ITDR Risks', value: CC_METRICS.critical_risks, color: '#ef4444' },
          { label: 'Gov Approvals', value: CC_METRICS.pending_approvals, color: '#f59e0b' }
        ].map(k => (
          <div key={k.label} className="icc-kpi-card" style={{ borderColor: `${k.color}30` }}>
            <span style={{ fontSize: '1.6rem', fontWeight: 800, color: k.color }}>{k.value}</span>
            <span style={{ fontSize: '0.7rem', color: '#94a3b8' }}>{k.label}</span>
          </div>
        ))}
      </div>

      <div className="icc-main-layout">
        {/* Module Sub-dashboards */}
        <div className="icc-modules-grid">
          <ModuleCard title="Zero Trust Operations" icon={<Lock />} link="/identity-cc/zero-trust" desc="Continuous verification & access boundaries." color="#10b981" />
          <ModuleCard title="Unified Governance" icon={<UserCheck />} link="/identity-cc/governance" desc="IGA & PAM lifecycle approvals." color="#f59e0b" />
          <ModuleCard title="Identity Risk & ITDR" icon={<Activity />} link="/identity-cc/risk" desc="Aggregated risk scores & threat detection." color="#ef4444" />
          <ModuleCard title="Machine & Cloud IAM" icon={<Server />} link="/nhi" desc="Workloads, service accounts & secrets." color="#8b5cf6" />
          <ModuleCard title="Passwordless Auth" icon={<Fingerprint />} link="/authn" desc="FIDO2, passkeys & biometrics." color="#3b82f6" />
          <ModuleCard title="Federation & SSO" icon={<Globe />} link="/federation" desc="Cross-domain trust pipelines." color="#0ea5e9" />
        </div>
      </div>
    </div>
  );
}

function ModuleCard({ title, icon, link, desc, color }: any) {
  return (
    <Link to={link} className="icc-mod-card" style={{ '--mod-color': color } as React.CSSProperties}>
      <div className="icc-mod-icon" style={{ color }}>{icon}</div>
      <div className="icc-mod-content">
        <h3 className="icc-mod-title">{title}</h3>
        <p className="icc-mod-desc">{desc}</p>
      </div>
    </Link>
  );
}

const CC_STYLES = `
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
* { box-sizing: border-box; }
.icc-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; flex-wrap: wrap; gap: 16px; }
.icc-header-icon { width: 48px; height: 48px; background: linear-gradient(135deg, #1e293b, #0f172a); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.icc-title { font-size: 1.45rem; font-weight: 800; margin: 0 0 2px; text-transform: uppercase; letter-spacing: 0.5px; }
.icc-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.icc-btn { display: inline-flex; align-items: center; gap: 6px; padding: 8px 14px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; color: #e2e8f0; font-size: 0.8rem; text-decoration: none; transition: all 0.2s; }
.icc-btn:hover { background: rgba(255,255,255,0.1); }
.icc-btn-ai { background: rgba(99,102,241,0.15); border-color: rgba(99,102,241,0.3); color: #a5b4fc; }
.icc-grid-6 { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 16px; margin-bottom: 24px; }
.icc-kpi-card { display: flex; flex-direction: column; padding: 16px; background: rgba(255,255,255,0.03); border: 1px solid; border-radius: 12px; }
.icc-modules-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; }
.icc-mod-card { display: flex; align-items: flex-start; gap: 16px; padding: 20px; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; text-decoration: none; transition: all 0.2s; }
.icc-mod-card:hover { background: rgba(255,255,255,0.04); border-color: var(--mod-color); transform: translateY(-2px); }
.icc-mod-icon { padding: 12px; background: rgba(255,255,255,0.03); border-radius: 10px; }
.icc-mod-content { flex: 1; }
.icc-mod-title { margin: 0 0 4px; font-size: 0.95rem; font-weight: 700; color: #f8fafc; }
.icc-mod-desc { margin: 0; font-size: 0.75rem; color: #94a3b8; line-height: 1.4; }
`;
