import React from 'react';
import { Link } from 'react-router-dom';
import { AppWindow, Settings, CheckCircle } from 'lucide-react';

const SSO_APPS = [
  { id: '1', name: 'Salesforce', sp_entity_id: 'https://saml.salesforce.com', protocol: 'SAML 2.0', idp: 'Okta Primary', status: 'ACTIVE' },
  { id: '2', name: 'Workday HR', sp_entity_id: 'http://www.workday.com', protocol: 'SAML 2.0', idp: 'Azure AD (Prod)', status: 'ACTIVE' },
  { id: '3', name: 'Internal Wiki', sp_entity_id: 'wiki.internal.corp', protocol: 'OIDC', idp: 'Keycloak', status: 'SUSPENDED' }
];

export default function SSODashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{SSO_STYLES}</style>
      <div className="sso-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="sso-header-icon"><AppWindow size={24} /></div>
          <div>
            <h1 className="sso-title">SSO Applications</h1>
            <p className="sso-subtitle">Inventory of all Enterprise Single Sign-On integrations</p>
          </div>
        </div>
        <Link to="/federation" style={{ color: '#38bdf8', textDecoration: 'none', fontSize: '0.85rem' }}>← Federation Dashboard</Link>
      </div>

      <div className="sso-card">
        <h3 className="sso-card-title">Configured Service Providers (SP)</h3>
        <table className="sso-table">
          <thead>
            <tr><th>Application / SP</th><th>Entity ID (Issuer)</th><th>Protocol</th><th>Routed IdP</th><th>Status</th><th>Action</th></tr>
          </thead>
          <tbody>
            {SSO_APPS.map(app => (
              <tr key={app.id} className="sso-row">
                <td style={{ fontWeight: 600 }}>{app.name}</td>
                <td style={{ color: '#94a3b8', fontSize: '0.8rem', fontFamily: 'monospace' }}>{app.sp_entity_id}</td>
                <td><span className="sso-protocol-badge">{app.protocol}</span></td>
                <td style={{ color: '#cbd5e1' }}>{app.idp}</td>
                <td>
                  <span className={`sso-status sso-${app.status.toLowerCase()}`}>
                    {app.status}
                  </span>
                </td>
                <td>
                  <button className="sso-btn-view"><Settings size={12} /> Config</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const SSO_STYLES = `
.sso-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.sso-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #0ea5e9, #0284c7); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.sso-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.sso-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.sso-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.sso-card-title { font-size: 1rem; font-weight: 600; margin: 0 0 16px; }
.sso-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.sso-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.sso-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.sso-row td { padding: 12px; }
.sso-protocol-badge { padding: 3px 8px; background: rgba(255,255,255,0.05); border-radius: 4px; font-size: 0.75rem; color: #e2e8f0; }
.sso-status { padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.sso-active { background: rgba(16,185,129,0.15); color: #34d399; }
.sso-suspended { background: rgba(239,68,68,0.15); color: #f87171; }
.sso-btn-view { display: inline-flex; align-items: center; gap: 4px; padding: 4px 10px; background: transparent; border: 1px solid rgba(255,255,255,0.1); border-radius: 4px; color: #94a3b8; cursor: pointer; font-size: 0.75rem; }
`;
