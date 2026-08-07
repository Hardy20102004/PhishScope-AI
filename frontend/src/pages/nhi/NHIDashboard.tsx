import React from 'react';
import { Link } from 'react-router-dom';
import { Cpu, Server, Key, AlertTriangle, Link as LinkIcon, RefreshCw, Bot } from 'lucide-react';

const NHI_DATA = {
  total_identities: 14050,
  expiring_certificates: 12,
  unrotated_credentials: 45,
  critical_risks: 3,
  active_trust_relationships: 2540,
  recent_risks: [
    { id: 'RSK-001', name: 'prod-db-service-acc', issue: 'API Key Unrotated > 90 Days', severity: 'CRITICAL', env: 'AWS Production' },
    { id: 'RSK-002', name: 'payments-api-cert', issue: 'Certificate expires in 14 days', severity: 'HIGH', env: 'Kubernetes (US-East)' },
    { id: 'RSK-003', name: 'dev-ci-pipeline', issue: 'Overly permissive IAM role attached', severity: 'HIGH', env: 'GCP Development' }
  ]
};

export default function NHIDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{NHI_STYLES}</style>
      
      {/* Header */}
      <div className="nhi-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="nhi-header-icon"><Cpu size={24} /></div>
          <div>
            <h1 className="nhi-title">Machine Identity Security (NHI)</h1>
            <p className="nhi-subtitle">Govern non-human identities, workloads, certificates, and trust chains</p>
          </div>
        </div>
        <div style={{ display: 'flex', gap: 10 }}>
          <Link to="/nhi/assistant" className="nhi-btn nhi-btn-ai"><Bot size={14} /> Ask NHI AI</Link>
        </div>
      </div>

      {/* KPI Row */}
      <div className="nhi-grid-5">
        {[
          { label: 'Total Machine Identities', value: NHI_DATA.total_identities, color: '#3b82f6' },
          { label: 'Expiring Certificates', value: NHI_DATA.expiring_certificates, color: '#f59e0b' },
          { label: 'Unrotated Credentials', value: NHI_DATA.unrotated_credentials, color: '#ef4444' },
          { label: 'Critical Risks', value: NHI_DATA.critical_risks, color: '#b91c1c' },
          { label: 'Trust Relationships', value: NHI_DATA.active_trust_relationships, color: '#10b981' }
        ].map(k => (
          <div key={k.label} className="nhi-kpi-card" style={{ borderColor: `${k.color}30` }}>
            <span style={{ fontSize: '1.8rem', fontWeight: 800, color: k.color }}>{k.value.toLocaleString()}</span>
            <span style={{ fontSize: '0.75rem', color: '#94a3b8' }}>{k.label}</span>
          </div>
        ))}
      </div>

      <div className="nhi-main-layout">
        <div className="nhi-left-col">
          {/* Recent Risks */}
          <div className="nhi-card">
            <h3 className="nhi-card-title"><AlertTriangle size={16} color="#ef4444" /> Urgent Machine Identity Risks</h3>
            <div className="nhi-list">
              {NHI_DATA.recent_risks.map((rsk) => (
                <div key={rsk.id} className="nhi-list-item">
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                    <strong style={{ color: '#e2e8f0', fontSize: '0.85rem' }}>{rsk.name}</strong>
                    <span className={`nhi-badge nhi-badge-${rsk.severity.toLowerCase()}`}>{rsk.severity}</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <p style={{ margin: 0, fontSize: '0.75rem', color: '#cbd5e1' }}>{rsk.issue}</p>
                    <span style={{ fontSize: '0.7rem', color: '#64748b' }}>{rsk.env}</span>
                  </div>
                </div>
              ))}
            </div>
            <Link to="/nhi/identities" style={{ display: 'block', textAlign: 'center', marginTop: 12, color: '#3b82f6', fontSize: '0.8rem', textDecoration: 'none' }}>View All Identities →</Link>
          </div>
        </div>
        
        <div className="nhi-right-col">
          {/* Quick Actions / Navigation */}
          <div className="nhi-card">
            <h3 className="nhi-card-title">NHI Modules</h3>
            <div className="nhi-module-links">
              <Link to="/nhi/identities" className="nhi-mod-link"><Cpu size={16} /> Service Accounts & API Keys</Link>
              <Link to="/nhi/workloads" className="nhi-mod-link"><Server size={16} /> Workload Identities</Link>
              <Link to="/nhi/certificates" className="nhi-mod-link"><Key size={16} /> Certificate Governance</Link>
              <Link to="/nhi/trust" className="nhi-mod-link"><LinkIcon size={16} /> Trust Relationships</Link>
              <Link to="/nhi/lifecycle" className="nhi-mod-link"><RefreshCw size={16} /> Lifecycle & Rotation</Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

const NHI_STYLES = `
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
* { box-sizing: border-box; }
.nhi-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; flex-wrap: wrap; gap: 16px; }
.nhi-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #3b82f6, #1d4ed8); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.nhi-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.nhi-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.nhi-btn { display: inline-flex; align-items: center; gap: 6px; padding: 8px 14px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; color: #e2e8f0; font-size: 0.8rem; text-decoration: none; transition: all 0.2s; }
.nhi-btn:hover { background: rgba(255,255,255,0.1); }
.nhi-btn-ai { background: rgba(59,130,246,0.15); border-color: rgba(59,130,246,0.3); color: #93c5fd; }
.nhi-grid-5 { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; margin-bottom: 16px; }
.nhi-kpi-card { display: flex; flex-direction: column; padding: 16px; background: rgba(255,255,255,0.03); border: 1px solid; border-radius: 12px; }
.nhi-main-layout { display: grid; grid-template-columns: 2fr 1fr; gap: 16px; }
@media(max-width: 900px) { .nhi-main-layout { grid-template-columns: 1fr; } }
.nhi-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; margin-bottom: 16px; }
.nhi-card-title { display: flex; align-items: center; gap: 8px; font-size: 0.9rem; font-weight: 600; color: #94a3b8; margin: 0 0 16px; }
.nhi-list { display: flex; flex-direction: column; gap: 10px; }
.nhi-list-item { padding: 12px; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 8px; transition: all 0.2s; }
.nhi-list-item:hover { background: rgba(255,255,255,0.04); }
.nhi-badge { padding: 2px 6px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.nhi-badge-critical { color: #fca5a5; background: rgba(239,68,68,0.2); }
.nhi-badge-high { color: #fdba74; background: rgba(249,115,22,0.2); }
.nhi-module-links { display: flex; flex-direction: column; gap: 8px; }
.nhi-mod-link { display: flex; align-items: center; gap: 10px; padding: 10px 14px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; color: #cbd5e1; font-size: 0.85rem; text-decoration: none; transition: all 0.2s; }
.nhi-mod-link:hover { background: rgba(59,130,246,0.1); border-color: rgba(59,130,246,0.3); color: #fff; }
`;
