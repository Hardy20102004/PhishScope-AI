import React from 'react';
import { Link } from 'react-router-dom';
import { Globe, Link as LinkIcon, AppWindow, ShieldAlert, FileKey, Bot } from 'lucide-react';

const FED_DATA = {
  total_trusts: 142,
  sso_applications: 340,
  protocol_violations: 12,
  expiring_metadata: 3,
  critical_risks: 2,
  recent_risks: [
    { id: 'RSK-001', name: 'Salesforce (Prod)', issue: 'SAML assertions are unencrypted', severity: 'CRITICAL', env: 'Okta' },
    { id: 'RSK-002', name: 'Partner B2B Portal', issue: 'Signing certificate expires in 7 days', severity: 'HIGH', env: 'Azure AD' },
    { id: 'RSK-003', name: 'Internal HR App', issue: 'OAuth Redirect URI contains wildcard', severity: 'HIGH', env: 'PingIdentity' }
  ]
};

export default function FederationDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{FED_STYLES}</style>
      
      {/* Header */}
      <div className="fed-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="fed-header-icon"><Globe size={24} /></div>
          <div>
            <h1 className="fed-title">Federated Identity & SSO</h1>
            <p className="fed-subtitle">Govern cross-domain trust, SSO apps, and federation protocols</p>
          </div>
        </div>
        <div style={{ display: 'flex', gap: 10 }}>
          <Link to="/federation/assistant" className="fed-btn fed-btn-ai"><Bot size={14} /> Ask Federation AI</Link>
        </div>
      </div>

      {/* KPI Row */}
      <div className="fed-grid-5">
        {[
          { label: 'Active Trust Relationships', value: FED_DATA.total_trusts, color: '#3b82f6' },
          { label: 'SSO Applications', value: FED_DATA.sso_applications, color: '#10b981' },
          { label: 'Protocol Violations', value: FED_DATA.protocol_violations, color: '#f59e0b' },
          { label: 'Expiring Metadata Certs', value: FED_DATA.expiring_metadata, color: '#f97316' },
          { label: 'Critical Risks', value: FED_DATA.critical_risks, color: '#ef4444' }
        ].map(k => (
          <div key={k.label} className="fed-kpi-card" style={{ borderColor: `${k.color}30` }}>
            <span style={{ fontSize: '1.8rem', fontWeight: 800, color: k.color }}>{k.value}</span>
            <span style={{ fontSize: '0.75rem', color: '#94a3b8' }}>{k.label}</span>
          </div>
        ))}
      </div>

      <div className="fed-main-layout">
        <div className="fed-left-col">
          {/* Recent Risks */}
          <div className="fed-card">
            <h3 className="fed-card-title"><ShieldAlert size={16} color="#ef4444" /> Urgent Federation Risks</h3>
            <div className="fed-list">
              {FED_DATA.recent_risks.map((rsk) => (
                <div key={rsk.id} className="fed-list-item">
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                    <strong style={{ color: '#e2e8f0', fontSize: '0.85rem' }}>{rsk.name}</strong>
                    <span className={`fed-badge fed-badge-${rsk.severity.toLowerCase()}`}>{rsk.severity}</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <p style={{ margin: 0, fontSize: '0.75rem', color: '#cbd5e1' }}>{rsk.issue}</p>
                    <span style={{ fontSize: '0.7rem', color: '#64748b' }}>{rsk.env}</span>
                  </div>
                </div>
              ))}
            </div>
            <Link to="/federation/trusts" style={{ display: 'block', textAlign: 'center', marginTop: 12, color: '#3b82f6', fontSize: '0.8rem', textDecoration: 'none' }}>View All Trust Relationships →</Link>
          </div>
        </div>
        
        <div className="fed-right-col">
          {/* Quick Actions / Navigation */}
          <div className="fed-card">
            <h3 className="fed-card-title">FEDERATION Modules</h3>
            <div className="fed-module-links">
              <Link to="/federation/trusts" className="fed-mod-link"><LinkIcon size={16} /> Trust Relationships</Link>
              <Link to="/federation/sso" className="fed-mod-link"><AppWindow size={16} /> SSO Applications</Link>
              <Link to="/federation/protocols" className="fed-mod-link"><ShieldAlert size={16} /> Protocol Validation</Link>
              <Link to="/federation/metadata" className="fed-mod-link"><FileKey size={16} /> Metadata & Certificates</Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

const FED_STYLES = `
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
* { box-sizing: border-box; }
.fed-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; flex-wrap: wrap; gap: 16px; }
.fed-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #0ea5e9, #0284c7); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.fed-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.fed-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.fed-btn { display: inline-flex; align-items: center; gap: 6px; padding: 8px 14px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; color: #e2e8f0; font-size: 0.8rem; text-decoration: none; transition: all 0.2s; }
.fed-btn:hover { background: rgba(255,255,255,0.1); }
.fed-btn-ai { background: rgba(14,165,233,0.15); border-color: rgba(14,165,233,0.3); color: #7dd3fc; }
.fed-grid-5 { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; margin-bottom: 16px; }
.fed-kpi-card { display: flex; flex-direction: column; padding: 16px; background: rgba(255,255,255,0.03); border: 1px solid; border-radius: 12px; }
.fed-main-layout { display: grid; grid-template-columns: 2fr 1fr; gap: 16px; }
@media(max-width: 900px) { .fed-main-layout { grid-template-columns: 1fr; } }
.fed-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; margin-bottom: 16px; }
.fed-card-title { display: flex; align-items: center; gap: 8px; font-size: 0.9rem; font-weight: 600; color: #94a3b8; margin: 0 0 16px; }
.fed-list { display: flex; flex-direction: column; gap: 10px; }
.fed-list-item { padding: 12px; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 8px; transition: all 0.2s; }
.fed-list-item:hover { background: rgba(255,255,255,0.04); }
.fed-badge { padding: 2px 6px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.fed-badge-critical { color: #fca5a5; background: rgba(239,68,68,0.2); }
.fed-badge-high { color: #fdba74; background: rgba(249,115,22,0.2); }
.fed-module-links { display: flex; flex-direction: column; gap: 8px; }
.fed-mod-link { display: flex; align-items: center; gap: 10px; padding: 10px 14px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; color: #cbd5e1; font-size: 0.85rem; text-decoration: none; transition: all 0.2s; }
.fed-mod-link:hover { background: rgba(14,165,233,0.1); border-color: rgba(14,165,233,0.3); color: #fff; }
`;
