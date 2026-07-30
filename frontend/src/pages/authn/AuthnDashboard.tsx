import React from 'react';
import { Link } from 'react-router-dom';
import { Fingerprint, Key, ShieldCheck, AlertTriangle, Shield, CheckCircle, Bot } from 'lucide-react';

const AUTHN_DATA = {
  total_enrollments: 4520,
  passkey_adoption_rate: 68.4,
  legacy_auth_count: 312,
  critical_risks: 14,
  high_assurance_identities: 3100,
  recent_risks: [
    { id: 'RSK-001', name: 'david.smith (Admin)', issue: 'No Phishing-Resistant MFA enrolled', severity: 'CRITICAL', env: 'Production' },
    { id: 'RSK-002', name: 'Contractors Group', issue: 'Legacy SMS OTP still active', severity: 'HIGH', env: 'Azure AD' },
    { id: 'RSK-003', name: 'sarah.connor', issue: 'Recovery email unverified for 180 days', severity: 'MEDIUM', env: 'Okta' }
  ]
};

export default function AuthnDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{AUTHN_STYLES}</style>
      
      {/* Header */}
      <div className="authn-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="authn-header-icon"><Fingerprint size={24} /></div>
          <div>
            <h1 className="authn-title">Passwordless Authentication (AUTHN)</h1>
            <p className="authn-subtitle">Govern passkeys, FIDO2 tokens, and modern authentication posture</p>
          </div>
        </div>
        <div style={{ display: 'flex', gap: 10 }}>
          <Link to="/authn/assistant" className="authn-btn authn-btn-ai"><Bot size={14} /> Ask Authn AI</Link>
        </div>
      </div>

      {/* KPI Row */}
      <div className="authn-grid-5">
        {[
          { label: 'Total Enrollments', value: AUTHN_DATA.total_enrollments, color: '#8b5cf6' },
          { label: 'Passkey Adoption', value: \`\${AUTHN_DATA.passkey_adoption_rate}%\`, color: '#10b981' },
          { label: 'High Assurance (AAL3)', value: AUTHN_DATA.high_assurance_identities, color: '#3b82f6' },
          { label: 'Legacy Auth (Passwords)', value: AUTHN_DATA.legacy_auth_count, color: '#f59e0b' },
          { label: 'Critical Risks', value: AUTHN_DATA.critical_risks, color: '#ef4444' }
        ].map(k => (
          <div key={k.label} className="authn-kpi-card" style={{ borderColor: `${k.color}30` }}>
            <span style={{ fontSize: '1.8rem', fontWeight: 800, color: k.color }}>{k.value}</span>
            <span style={{ fontSize: '0.75rem', color: '#94a3b8' }}>{k.label}</span>
          </div>
        ))}
      </div>

      <div className="authn-main-layout">
        <div className="authn-left-col">
          {/* Recent Risks */}
          <div className="authn-card">
            <h3 className="authn-card-title"><AlertTriangle size={16} color="#ef4444" /> Urgent Authentication Risks</h3>
            <div className="authn-list">
              {AUTHN_DATA.recent_risks.map((rsk) => (
                <div key={rsk.id} className="authn-list-item">
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                    <strong style={{ color: '#e2e8f0', fontSize: '0.85rem' }}>{rsk.name}</strong>
                    <span className={`authn-badge authn-badge-${rsk.severity.toLowerCase()}`}>{rsk.severity}</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <p style={{ margin: 0, fontSize: '0.75rem', color: '#cbd5e1' }}>{rsk.issue}</p>
                    <span style={{ fontSize: '0.7rem', color: '#64748b' }}>{rsk.env}</span>
                  </div>
                </div>
              ))}
            </div>
            <Link to="/authn/enrollments" style={{ display: 'block', textAlign: 'center', marginTop: 12, color: '#8b5cf6', fontSize: '0.8rem', textDecoration: 'none' }}>View All Enrollments →</Link>
          </div>
        </div>
        
        <div className="authn-right-col">
          {/* Quick Actions / Navigation */}
          <div className="authn-card">
            <h3 className="authn-card-title">AUTHN Modules</h3>
            <div className="authn-module-links">
              <Link to="/authn/passkeys" className="authn-mod-link"><Fingerprint size={16} /> Passkey Inventory</Link>
              <Link to="/authn/enrollments" className="authn-mod-link"><Key size={16} /> User Enrollments</Link>
              <Link to="/authn/assurance" className="authn-mod-link"><ShieldCheck size={16} /> Assurance Levels (AAL)</Link>
              <Link to="/authn/policies" className="authn-mod-link"><Shield size={16} /> Authentication Policies</Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

const AUTHN_STYLES = `
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
* { box-sizing: border-box; }
.authn-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; flex-wrap: wrap; gap: 16px; }
.authn-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #8b5cf6, #6d28d9); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.authn-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.authn-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.authn-btn { display: inline-flex; align-items: center; gap: 6px; padding: 8px 14px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; color: #e2e8f0; font-size: 0.8rem; text-decoration: none; transition: all 0.2s; }
.authn-btn:hover { background: rgba(255,255,255,0.1); }
.authn-btn-ai { background: rgba(139,92,246,0.15); border-color: rgba(139,92,246,0.3); color: #c4b5fd; }
.authn-grid-5 { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; margin-bottom: 16px; }
.authn-kpi-card { display: flex; flex-direction: column; padding: 16px; background: rgba(255,255,255,0.03); border: 1px solid; border-radius: 12px; }
.authn-main-layout { display: grid; grid-template-columns: 2fr 1fr; gap: 16px; }
@media(max-width: 900px) { .authn-main-layout { grid-template-columns: 1fr; } }
.authn-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; margin-bottom: 16px; }
.authn-card-title { display: flex; align-items: center; gap: 8px; font-size: 0.9rem; font-weight: 600; color: #94a3b8; margin: 0 0 16px; }
.authn-list { display: flex; flex-direction: column; gap: 10px; }
.authn-list-item { padding: 12px; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 8px; transition: all 0.2s; }
.authn-list-item:hover { background: rgba(255,255,255,0.04); }
.authn-badge { padding: 2px 6px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.authn-badge-critical { color: #fca5a5; background: rgba(239,68,68,0.2); }
.authn-badge-high { color: #fdba74; background: rgba(249,115,22,0.2); }
.authn-badge-medium { color: #fde047; background: rgba(234,179,8,0.2); }
.authn-module-links { display: flex; flex-direction: column; gap: 8px; }
.authn-mod-link { display: flex; align-items: center; gap: 10px; padding: 10px 14px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; color: #cbd5e1; font-size: 0.85rem; text-decoration: none; transition: all 0.2s; }
.authn-mod-link:hover { background: rgba(139,92,246,0.1); border-color: rgba(139,92,246,0.3); color: #fff; }
`;
