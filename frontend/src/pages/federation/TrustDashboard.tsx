import React from 'react';
import { Link } from 'react-router-dom';
import { Link as LinkIcon, Network } from 'lucide-react';

const TRUSTS = [
  { id: '1', name: 'Azure AD to AWS IAM', idp: 'Azure AD (Prod)', sp: 'AWS Identity Center', type: 'SAML 2.0', status: 'ACTIVE' },
  { id: '2', name: 'Vendor B2B Portal', idp: 'Okta External', sp: 'Custom B2B App', type: 'OIDC', status: 'ACTIVE' },
  { id: '3', name: 'Legacy HR Connect', idp: 'Active Directory FS', sp: 'Workday HR', type: 'WS-Federation', status: 'DEPRECATED' }
];

export default function TrustDashboard() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#0a0a12', minHeight: '100vh', padding: 24, color: '#e2e8f0' }}>
      <style>{TRUST_STYLES}</style>
      <div className="trst-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div className="trst-header-icon"><Network size={24} /></div>
          <div>
            <h1 className="trst-title">Trust Relationships</h1>
            <p className="trst-subtitle">Manage IdP to SP mapping and cross-domain B2B trust</p>
          </div>
        </div>
        <Link to="/federation" style={{ color: '#38bdf8', textDecoration: 'none', fontSize: '0.85rem' }}>← Federation Dashboard</Link>
      </div>

      <div className="trst-card">
        <h3 className="trst-card-title"><LinkIcon size={16} /> Configured Federation Trusts</h3>
        <table className="trst-table">
          <thead>
            <tr><th>Trust Name</th><th>Identity Provider (Source)</th><th>Service Provider (Target)</th><th>Protocol</th><th>Status</th></tr>
          </thead>
          <tbody>
            {TRUSTS.map(trst => (
              <tr key={trst.id} className="trst-row">
                <td style={{ fontWeight: 600 }}>{trst.name}</td>
                <td style={{ color: '#38bdf8' }}>{trst.idp}</td>
                <td style={{ color: '#10b981' }}>{trst.sp}</td>
                <td>{trst.type}</td>
                <td>
                  <span className={`trst-status trst-${trst.status.toLowerCase()}`}>
                    {trst.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const TRUST_STYLES = `
.trst-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.trst-header-icon { width: 44px; height: 44px; background: linear-gradient(135deg, #0ea5e9, #0284c7); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; }
.trst-title { font-size: 1.35rem; font-weight: 800; margin: 0 0 2px; }
.trst-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
.trst-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; }
.trst-card-title { display: flex; align-items: center; gap: 8px; font-size: 1rem; font-weight: 600; margin: 0 0 16px; }
.trst-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left; }
.trst-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #64748b; font-weight: 500; }
.trst-row { border-bottom: 1px solid rgba(255,255,255,0.05); }
.trst-row td { padding: 12px; }
.trst-status { padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.trst-active { background: rgba(16,185,129,0.15); color: #34d399; }
.trst-deprecated { background: rgba(100,116,139,0.2); color: #94a3b8; text-decoration: line-through; }
`;
